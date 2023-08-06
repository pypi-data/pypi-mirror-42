# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the explanations that are returned from explaining models."""

import os
import numpy as np
import uuid

from azureml.core import Experiment, Run
from azureml._restclient.assets_client import AssetsClient
from azureml._restclient.constants import RUN_ORIGIN
from azureml.exceptions import UserErrorException
from azureml.explain.model._internal.common import _sort_values, _sort_feature_list_multiclass, \
    _order_imp, unsort_1d, unsort_2d
from azureml.explain.model._internal.model_summary import ModelSummary
from azureml.explain.model._internal.results import _download_artifact, _create_download_dir
from azureml._logging import ChainedIdentity
from azureml.explain.model._internal.constants import Dynamic, ExplainParams, ExplanationParams, ExplainType, \
    History, BackCompat
from azureml.explain.model._internal.common import module_logger

from ..common.explanation_utils import ArtifactUploader


class BaseExplanation(ChainedIdentity):
    """Defines the common explanation returned by explainers."""

    def __init__(self, method, features=None, explanation_id=None, **kwargs):
        """Create the common explanation from the given feature names.

        :param method: The explanation method used to explain the model (e.g. SHAP, LIME)
        :type method: str
        :param features: The feature names.
        :type features: Union[list[str], list[int]]
        :param explanation_id: The unique identifier for the explanation.
        :type explanation_id: str
        """
        super(BaseExplanation, self).__init__(**kwargs)
        self._logger.debug('Initializing BaseExplanation')
        self._method = method
        self._features = features
        self._id = explanation_id or str(uuid.uuid4())

    @property
    def method(self):
        """Get the explanation method.

        :return: The explanation method.
        :rtype: str
        """
        return self._method

    @property
    def features(self):
        """Get the feature names.

        :return: The feature names.
        :rtype: list[str]
        """
        return self._features

    @property
    def id(self):
        """Get the explanation id.

        :return: The explanation id.
        :rtype: str
        """
        return self._id

    @staticmethod
    def _does_quack(explanation):
        """Validate that the explanation object passed in is a valid BaseExplanation.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not hasattr(explanation, History.METHOD) or not isinstance(explanation.method, str):
            return False
        if not hasattr(explanation, History.ID) or not isinstance(explanation.id, str):
            return False
        if not hasattr(explanation, History.FEATURES):
            return False
        return True


class LocalExplanation(BaseExplanation):
    """Defines the common local explanation returned by explainers."""

    def __init__(self, local_importance_values=None, **kwargs):
        """Create the local explanation from the explainer's feature importance values.

        :param local_importance_values: The feature importance values.
        :type local_importance_values: numpy.ndarray
        """
        super(LocalExplanation, self).__init__(**kwargs)
        self._logger.debug('Initializing LocalExplanation')
        self._local_importance_values = local_importance_values

    @property
    def local_importance_values(self):
        """Get the feature importance values in original order.

        :return: For a model with a single output such as regression, this
            returns a list of feature importance values for each data point. For models with vector outputs this
            function returns a list of such lists, one for each output. The dimension of this matrix
            is (# examples x # features).
        :rtype: list[list[float]] or list[list[list[float]]]
        """
        return self._local_importance_values.tolist()

    def get_local_importance_rank(self):
        """Get local feature importance rank or indexes.

        For example, if original features are
        [f0, f1, f2, f3] and in local importance order for the first data point they are [f2, f3, f0, f1],
        local_importance_rank[0] would be [2, 3, 0, 1] (or local_importance_rank[0][0] if classification)

        :return: The feature indexes sorted by importance.
        :rtype: list[list[int]] or list[list[list[int]]]
        """
        return _order_imp(self._local_importance_values).tolist()

    def get_ranked_local_names(self, top_k=None):
        """Get feature names sorted by local feature importance values, highest to lowest.

        :param top_k: If specified, only the top k names will be returned.
        :type top_k: int
        :return: The list of sorted features unless feature names are unavailable, feature indexes otherwise.
        :rtype: list[list[int or str]] or list[list[list[int or str]]]
        """
        if self._features is not None:
            self._ranked_per_class_names = _sort_values(self._features, self.get_local_importance_rank())
            ranked_per_class_names = self._ranked_per_class_names
        else:
            ranked_per_class_names = np.array(self.get_local_importance_rank())

        if top_k is not None:
            ranked_per_class_names = ranked_per_class_names[:, :top_k]
        return ranked_per_class_names.tolist()

    def get_ranked_local_values(self, top_k=None):
        """Get local feature importance sorted from highest to lowest.

        :param top_k: If specified, only the top k values will be returned.
        :type top_k: int
        :return: The list of sorted values.
        :rtype: list[list[float]] or list[list[list[float]]]
        """
        return_length = top_k or np.shape(self._local_importance_values)[1]
        row_indexes = np.arange(len(self._local_importance_values))[:, np.newaxis]
        self._ranked_local_values = self._local_importance_values[row_indexes, self.get_local_importance_rank()]
        return self._ranked_local_values[:, :return_length].tolist()

    @classmethod
    def _does_quack(cls, explanation):
        """Validate that the explanation object passed in is a valid LocalExplanation.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not super()._does_quack(explanation):
            return False
        if not hasattr(explanation, History.LOCAL_IMPORTANCE_VALUES):
            return False
        if not isinstance(explanation.local_importance_values, list):
            return False
        return True


class GlobalExplanation(BaseExplanation):
    """Defines the common global explanation returned by explainers."""

    def __init__(self,
                 global_importance_values=None,
                 global_importance_rank=None,
                 ranked_global_names=None,
                 ranked_global_values=None,
                 **kwargs):
        """Create the global explanation from the explainer's overall importance values and order.

        :param global_importance_values: The feature importance values in the order of the original features.
        :type global_importance_values: numpy.ndarray
        :param global_importance_rank: The feature indexes sorted by importance.
        :type global_importance_rank: numpy.ndarray
        :param ranked_global_names: The feature names sorted by importance.
        :type ranked_global_names: list[str]
        :param ranked_global_values: The feature importance values sorted by importance.
        :type ranked_global_values: numpy.ndarray
        """
        super(GlobalExplanation, self).__init__(**kwargs)
        self._logger.debug('Initializing GlobalExplanation')
        self._global_importance_values = global_importance_values
        self._global_importance_rank = global_importance_rank
        self._ranked_global_names = ranked_global_names
        self._ranked_global_values = ranked_global_values

    @property
    def global_importance_values(self):
        """Get the global feature importance values.

        Values will be in their original order, the same as features, unless top_k was passed into
        upload_model_explanation or download_model_explanation. In those cases, returns the most important k values
        in highest to lowest importance order.

        :return: The model level feature importance values.
        :rtype: list[float]
        """
        if self._global_importance_values is None:
            return self._ranked_global_values
        return self._global_importance_values.tolist()

    @property
    def global_importance_rank(self):
        """Get the overall feature importance rank or indexes.

        For example, if original features are
        [f0, f1, f2, f3] and in global importance order they are [f2, f3, f0, f1], global_importance_rank
        would be [2, 3, 0, 1].

        :return: The feature indexes sorted by importance.
        :rtype: list[int]
        """
        return self._global_importance_rank.tolist()

    def get_ranked_global_names(self, top_k=None):
        """Get feature names sorted by global feature importance values, highest to lowest.

        :param top_k: If specified, only the top k names will be returned.
        :type top_k: int
        :return: The list of sorted features unless feature names are unavailable, feature indexes otherwise.
        :rtype: list[str] or list[int]
        """
        if self._ranked_global_names is None and self._features is not None:
            self._ranked_global_names = _sort_values(self._features, self._global_importance_rank)

        if self._ranked_global_names is not None:
            ranked_global_names = self._ranked_global_names
        else:
            ranked_global_names = self._global_importance_rank

        if top_k:
            return ranked_global_names[:top_k].tolist()
        return ranked_global_names.tolist()

    def get_ranked_global_values(self, top_k=None):
        """Get global feature importance sorted from highest to lowest.

        :param top_k: If specified, only the top k values will be returned.
        :type top_k: int
        :return: The list of sorted values.
        :rtype: list[float]
        """
        if self._ranked_global_values is None:
            self._ranked_global_values = _sort_values(self._global_importance_values,
                                                      self._global_importance_rank)
        if top_k:
            return self._ranked_global_values[:top_k].tolist()
        return self._ranked_global_values.tolist()

    @classmethod
    def _does_quack(cls, explanation):
        """Validate that the explanation object passed in is a valid GlobalExplanation.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not super()._does_quack(explanation):
            return False
        if not hasattr(explanation, History.GLOBAL_IMPORTANCE_VALUES) or explanation.global_importance_values is None:
            return False
        if not hasattr(explanation, History.GLOBAL_IMPORTANCE_RANK) or explanation.global_importance_rank is None:
            return False
        return True


class TextExplanation(LocalExplanation):
    """Defines the mixin for text explanations."""

    def __init__(self, **kwargs):
        """Create the text explanation."""
        super(TextExplanation, self).__init__(**kwargs)
        order = _order_imp(np.abs(self.local_importance_values))
        self._local_importance_rank = _sort_values(self._features, order)
        self._logger.debug('Initializing TextExplanation')
        if len(order.shape) == 3:
            i = np.arange(order.shape[0])[:, np.newaxis]
            j = np.arange(order.shape[1])[:, np.newaxis]
            self._ordered_local_importance_values = np.array(self.local_importance_values)[i, j, order]
        else:
            self._ordered_local_importance_values = self.local_importance_values

    @property
    def local_importance_rank(self):
        """Feature names sorted by importance.

        This property exists for text explanations only and not for local because currently
        we are doing text explanations for a single document and it is more difficult to
        define order for multiple instances.  Note this is subject to change if we eventually
        add global explanations for text explainers.

        :return: The feature names sorted by importance.
        :rtype: list
        """
        return self._local_importance_rank.tolist()

    @property
    def ordered_local_importance_values(self):
        """Get the feature importance values ordered by importance.

        This property exists for text explanations only and not for local because currently
        we are doing text explanations for a single document and it is more difficult to
        define order for multiple instances.  Note this is subject to change if we eventually
        add global explanations for text explainers.

        :return: For a model with a single output such as regression, this
            returns a list of feature importance values. For models with vector outputs this function
            returns a list of such lists, one for each output. The dimension of this matrix
            is (# examples x # features).
        :rtype: list
        """
        return self._ordered_local_importance_values

    @classmethod
    def _does_quack(cls, explanation):
        """Validate that the explanation object passed in is a valid TextExplanation.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not super()._does_quack(explanation):
            return False
        if not hasattr(explanation, History.LOCAL_IMPORTANCE_RANK) or explanation.local_importance_rank is None:
            return False
        if (not hasattr(explanation, History.ORDERED_LOCAL_IMPORTANCE_VALUES) or
                explanation.ordered_local_importance_values is None):
            return False
        return True


class ExpectedValuesMixin(object):
    """Defines the mixin for expected values."""

    def __init__(self, expected_values=None, **kwargs):
        """Create the expected values mixin and set the expected values.

        :param expected_values: The expected values of the model.
        :type expected_values: np.array
        """
        super(ExpectedValuesMixin, self).__init__(**kwargs)
        self._expected_values = expected_values

    @property
    def expected_values(self):
        """Get the expected values.

        :return: The expected value of the model applied to the set of initialization examples.
        :rtype: list
        """
        return self._expected_values.tolist()

    @staticmethod
    def _does_quack(explanation):
        """Validate that the explanation object passed in is a valid ExpectedValuesMixin.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not hasattr(explanation, History.EXPECTED_VALUES) or explanation.expected_values is None:
            return False
        return True


class ClassesMixin(object):
    """Defines the mixin for classes.

    This mixin is added when the user specifies classes in the classification
    scenario when creating a global or local explanation.
    This is activated when the user specifies the classes parameter for global
    or local explanations.
    """

    def __init__(self, classes=None, **kwargs):
        """Create the classes mixin and set the classes.

        :param classes: Class names as a list of strings. The order of
            the class names should match that of the model output.
        :type classes: list[str]
        """
        super(ClassesMixin, self).__init__(**kwargs)
        self._classes = classes

    @property
    def classes(self):
        """Get the classes.

        :return: The list of classes.
        :rtype: list
        """
        return self._classes

    @staticmethod
    def _does_quack(explanation):
        """Validate that the explanation object passed in is a valid ClassesMixin.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        return hasattr(explanation, History.CLASSES)


class PerClassMixin(ClassesMixin):
    """Defines the mixin for per class aggregated information.

    This mixin is added for the classification scenario for global
    explanations.  The per class importance values are group averages of
    local importance values across different classes.
    """

    def __init__(self,
                 per_class_values=None,
                 per_class_rank=None,
                 ranked_per_class_names=None,
                 ranked_per_class_values=None,
                 **kwargs):
        """Create the per class mixin from the explainer's importance values and order.

        :param per_class_values: The feature importance values for each class in the order of the original features.
        :type per_class_values: numpy.ndarray
        :param per_class_importance_rank: The feature indexes for each class sorted by importance.
        :type per_class_importance_rank: numpy.ndarray
        :param ranked_per_class_names: The feature names for each class sorted by importance.
        :type ranked_per_class_names: list[str]
        :param ranked_per_class_values: The feature importance values sorted by importance.
        :type ranked_per_class_values: numpy.ndarray
        """
        super(PerClassMixin, self).__init__(**kwargs)
        self._per_class_values = per_class_values
        self._per_class_rank = per_class_rank
        self._ranked_per_class_names = ranked_per_class_names
        self._ranked_per_class_values = ranked_per_class_values

    @property
    def per_class_values(self):
        """Get the per class importance values.

        Values will be in their original order, the same as features, unless top_k was passed into
        upload_model_explanation or download_model_explanation. In those cases, returns the most important k values
        in highest to lowest importance order.

        :return: The model level per class feature importance values in original feature order.
        :rtype: list
        """
        if self._per_class_values is None:
            return self._ranked_per_class_values.tolist()
        return self._per_class_values.tolist()

    @property
    def per_class_rank(self):
        """Get the per class importance rank or indexes.

        For example, if original features are
        [f0, f1, f2, f3] and in per class importance order they are [[f2, f3, f0, f1], [f0, f2, f3, f1]],
        per_class_rank would be [[2, 3, 0, 1], [0, 2, 3, 1]].

        :return: The per class indexes that would sort per_class_values.
        :rtype: list
        """
        return self._per_class_rank.tolist()

    def get_ranked_per_class_names(self, top_k=None):
        """Get feature names sorted by per class feature importance values, highest to lowest.

        :param top_k: If specified, only the top k names will be returned.
        :type top_k: int
        :return: The list of sorted features unless feature names are unavailable, feature indexes otherwise.
        :rtype: list[list[str]] or list[list[int]]
        """
        if self._ranked_per_class_names is None and self._features is not None:
            self._ranked_per_class_names = _sort_values(self._features, self._per_class_rank)

        if self._ranked_per_class_names is not None:
            ranked_per_class_names = self._ranked_per_class_names
        else:
            ranked_per_class_names = self._per_class_rank

        if top_k:
            ranked_per_class_names = ranked_per_class_names[:, :top_k]
        return ranked_per_class_names.tolist()

    def get_ranked_per_class_values(self, top_k=None):
        """Get per class feature importance sorted from highest to lowest.

        :param top_k: If specified, only the top k values will be returned.
        :type top_k: int
        :return: The list of sorted values.
        :rtype: list[list[float]]
        """
        if self._ranked_per_class_values is None:
            row_indexes = np.arange(len(self._per_class_values))[:, np.newaxis]
            self._ranked_per_class_values = self._per_class_values[row_indexes, self._per_class_rank]
        if top_k:
            return self._ranked_per_class_values[:, :top_k].tolist()
        return self._ranked_per_class_values.tolist()

    @classmethod
    def _does_quack(cls, explanation):
        """Validate that the explanation object passed in is a valid PerClassMixin.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not super()._does_quack(explanation):
            return False
        if not hasattr(explanation, History.PER_CLASS_VALUES) or explanation.per_class_values is None:
            return False
        if not hasattr(explanation, History.PER_CLASS_RANK) or explanation.per_class_rank is None:
            return False
        return True


class HasScoringModel(object):
    """Defines an explanation that can be operationalized for real-time scoring."""

    def __init__(self, scoring_model=None, **kwargs):
        """Create the operationalization explanation from scoring model.

        :param scoring_model: The scoring model.
        :type scoring_model: ScoringModel
        """
        super(HasScoringModel, self).__init__(**kwargs)
        self._scoring_model = scoring_model

    @property
    def scoring_model(self):
        """Return the scoring model.

        :rtype: ScoringModel
        :return: The scoring model.
        """
        return self._scoring_model

    @staticmethod
    def _does_quack(explanation):
        """Validate that the explanation object passed in is a valid HasScoringModel.

        :param explanation: The explanation to be validated.
        :type explanation: object
        :return: True if valid else False
        :rtype: bool
        """
        if not hasattr(explanation, ExplainParams.SCORING_MODEL) or explanation.scoring_model is None:
            return False
        return True


def upload_model_explanation(run, explanation, max_num_blocks=None, block_size=None, top_k=None, comment=None):
    """Upload the model explanation information to run history.

    :param run: A model explanation run to save explanation information to.
    :type run: azureml.core.run.Run
    :param explanation: The explanation information to save.
    :type explanation: BaseExplanation
    :param max_num_blocks: The maximum number of blocks to store.
    :type max_num_blocks: int
    :param block_size: The size of each block for the summary stored in artifacts storage.
    :type block_size: int
    :param top_k: Number of important features stored in the explanation. If specified, only the
        names and values corresponding to the top K most important features will be returned/stored.
        If this is the case, global_importance_values and per_class_values will contain the top k sorted values
        instead of the usual full list of unsorted values.
    :type top_k: int
    :param comment: A string specified by user to identify the explanation. Displayed when listing
        explanations.  Allows the user to identify the explanations they have uploaded.
    :type comment: str
    """
    uploader = ArtifactUploader(run, max_num_blocks=max_num_blocks, block_size=block_size)
    assets_client = AssetsClient(run.experiment.workspace.service_context)
    text_explanation = TextExplanation._does_quack(explanation)
    classification = ClassesMixin._does_quack(explanation)
    if classification:
        model_type = ExplainType.CLASSIFICATION
    else:
        model_type = ExplainType.REGRESSION
    if text_explanation:
        explainer_type = ExplainType.TEXT
    else:
        explainer_type = ExplainType.TABULAR
    # save model type and explainer type
    run.add_properties({ExplainType.MODEL: model_type, ExplainType.EXPLAINER: explainer_type})
    summary_object = ModelSummary()
    single_artifact_list = []
    sharded_artifact_list = []

    if BaseExplanation._does_quack(explanation) and explanation.features is not None:
        features = explanation.features if isinstance(explanation.features, list) else explanation.features.tolist()
        single_artifact_list.append((History.FEATURES, features, None))

    if LocalExplanation._does_quack(explanation):
        single_artifact_list.append((History.LOCAL_IMPORTANCE_VALUES, explanation.local_importance_values, None))

    if ExpectedValuesMixin._does_quack(explanation):
        single_artifact_list.append((History.EXPECTED_VALUES, explanation.expected_values, None))

    if GlobalExplanation._does_quack(explanation):
        global_importance_rank = explanation.global_importance_rank
        ranked_global_values = explanation.get_ranked_global_values()
        global_length = top_k if top_k is not None else len(global_importance_rank)
        global_importance_rank = global_importance_rank[:global_length]
        ranked_global_values = ranked_global_values[:global_length]

        if classification and PerClassMixin._does_quack(explanation):
            per_class_rank = np.array(explanation.per_class_rank)
            ranked_per_class_values = np.array(explanation.get_ranked_per_class_values())
            per_class_length = top_k if top_k is not None else per_class_rank.shape[1]
            per_class_rank = per_class_rank[:, :per_class_length]
            ranked_per_class_values = ranked_per_class_values[:, :per_class_length]
        if explanation.features is not None:
            ranked_global_names = explanation.get_ranked_global_names()
            if isinstance(ranked_global_names[0], str):
                global_ordered_features = ranked_global_names
            else:
                global_ordered_features = _sort_values(explanation.features,
                                                       global_importance_rank).tolist()
            global_ordered_features = global_ordered_features[:global_length]
            sharded_artifact_list.append((History.GLOBAL_IMPORTANCE_NAMES, np.array(global_ordered_features)))

            if classification and PerClassMixin._does_quack(explanation):
                ranked_per_class_names = explanation.get_ranked_per_class_names()
                if isinstance(ranked_per_class_names[0][0], str):
                    per_class_ordered_features = ranked_per_class_names
                else:
                    per_class_ordered_features = _sort_feature_list_multiclass(explanation.features,
                                                                               per_class_rank)
                per_class_ordered_features = np.array(per_class_ordered_features)
                per_class_ordered_features = per_class_ordered_features[:, :per_class_length]
                sharded_artifact_list.append((History.PER_CLASS_NAMES, per_class_ordered_features))

        sharded_artifact_list.append((History.GLOBAL_IMPORTANCE_RANK, np.array(global_importance_rank)))
        sharded_artifact_list.append((History.GLOBAL_IMPORTANCE_VALUES, np.array(ranked_global_values)))

        if classification and PerClassMixin._does_quack(explanation):
            sharded_artifact_list.append((History.PER_CLASS_RANK, per_class_rank))
            sharded_artifact_list.append((History.PER_CLASS_VALUES, ranked_per_class_values))

    if classification and explanation.classes is not None:
        classes = explanation.classes
        if isinstance(classes, np.ndarray):
            classes = classes.tolist()
        single_artifact_list.append((History.CLASSES, classes, {History.NUM_CLASSES: len(classes)}))

    uploader.upload_single_artifact_list(summary_object, single_artifact_list, explanation.id)
    uploader.upload_sharded_artifact_list(summary_object, sharded_artifact_list, explanation.id)

    # upload rich metadata information
    upload_dir = uploader._create_upload_dir(explanation.id)
    uploader._upload_artifact(upload_dir, History.RICH_METADATA, summary_object.get_metadata_dictionary())
    artifact_list = summary_object.get_artifacts()
    artifact_path = os.path.normpath('{}/{}/{}/{}'.format(RUN_ORIGIN, run.id, upload_dir, History.RICH_METADATA))

    artifact_list.append({History.PREFIX: artifact_path})
    assets_client.create_asset(
        History.EXPLANATION_ASSET,
        summary_object.get_artifacts(),
        metadata_dict={
            ExplainType.MODEL: ExplainType.CLASSIFICATION if classification else ExplainType.REGRESSION,
            ExplainType.DATA: explainer_type,
            ExplainType.EXPLAIN: explanation.method,
            History.METADATA_ARTIFACT: artifact_path,
            History.VERSION: History.EXPLANATION_ASSET_TYPE_V3,
            History.EXPLANATION_ID: explanation.id,
            History.COMMENT: comment},
        run_id=run.id,
        properties={History.TYPE: History.EXPLANATION,
                    History.EXPLANATION_ID: explanation.id}
    )


def download_model_explanation(run, explanation_id=None, top_k=None):
    """Get an explanation for a given run from run history.

    :param run: The run from which the explanation was generated
    :type run: azureml.core.run.Run
    :param explanation_id: If specified, tries to download the asset from the run with the given explanation ID.
        If unspecified, grabs an arbitrary explanation asset from the run.
    :type explanation_id: str
    :param top_k: If specified, limit the ordered data returned to the most important features and values.
        If this is the case, global_importance_values and per_class_values will contain the top k sorted values
        instead of the usual full list of unsorted values.
    :type top_k: int
    :return: The explanation as it was uploaded to run history
    :rtype: BaseExplanation
    """
    kwargs = {}
    download_dir = _create_download_dir()
    assets_client = AssetsClient(run.experiment.workspace.service_context)
    explanation_assets = assets_client.get_assets_by_run_id_and_name(run.id, History.EXPLANATION_ASSET)

    # in case there's some issue with asset service, check
    if len(explanation_assets) > 0:
        module_logger.debug('Found at least one explanation asset, taking the first one')
        if explanation_id is not None:
            explanation_asset = None
            for asset in explanation_assets:
                if (History.EXPLANATION_ID in asset.additional_properties[History.PROPERTIES] and
                        asset.additional_properties[History.PROPERTIES][History.EXPLANATION_ID] == explanation_id):
                    explanation_asset = asset
            if explanation_asset is None:
                error_string = 'Could not find an explanation asset with id ' + explanation_id
                module_logger.debug(error_string)
                raise UserErrorException(error_string)
        else:
            explanation_asset = explanation_assets[0]
            if History.EXPLANATION_ID in explanation_asset.additional_properties[History.PROPERTIES]:
                explanation_id = explanation_asset.additional_properties[History.PROPERTIES][History.EXPLANATION_ID]

    else:
        # if no asset, we can't do anything
        module_logger.debug('Did not find any explanation assets')
        return None

    # everything that might be available from the asset for construction an explanation
    local_importance_vals = None

    if (History.VERSION in explanation_asset.meta and
            (explanation_asset.meta[History.VERSION] == History.EXPLANATION_ASSET_TYPE_V2 or
             explanation_asset.meta[History.VERSION] == History.EXPLANATION_ASSET_TYPE_V3)):

        module_logger.debug('Explanation asset is version {}'.format(explanation_asset.meta[History.VERSION]))
        if ExplainType.EXPLAIN in explanation_asset.meta:
            explanation_method = explanation_asset.meta[ExplainType.EXPLAIN]
        else:
            # backwards compatibilty as of February 2019
            explanation_method = ExplainType.SHAP
        metadata_artifact_name = explanation_asset.meta[History.METADATA_ARTIFACT]
        storage_metadata = _download_artifact(run, download_dir, metadata_artifact_name,
                                              explanation_id=explanation_id)
        # classification and local importances are stored differently in v2/3 assets than in v1
        classification = explanation_asset.meta[ExplainType.MODEL] == ExplainType.CLASSIFICATION
        if History.LOCAL_IMPORTANCE_VALUES in storage_metadata:
            module_logger.debug('Downloading local importance values from v2/3')
            local_importance_vals = np.array(_download_artifact(run, download_dir, History.LOCAL_IMPORTANCE_VALUES,
                                                                explanation_id=explanation_id))
        kwargs[ExplainParams.FEATURES] = _download_artifact(run, download_dir, History.FEATURES,
                                                            explanation_id=explanation_id)
    else:
        # v1 asset backwards compatibility as of January 2019
        module_logger.debug('Explanation asset is v1 version')
        # shap was the only option at the time
        explanation_method = ExplainType.SHAP
        storage_metadata = _get_v2_metadata_from_v1(explanation_asset.meta)
        classification = History.PER_CLASS_VALUES in storage_metadata
        module_logger.debug('Downloading local importance values from v1')
        local_importance_vals = np.array(_download_artifact(run, download_dir, BackCompat.SHAP_VALUES))
        kwargs[ExplainParams.FEATURES] = _download_artifact(run, download_dir, BackCompat.FEATURE_NAMES)

    kwargs[ExplainParams.METHOD] = explanation_method
    kwargs[ExplainParams.CLASSIFICATION] = classification
    if History.EXPECTED_VALUES in storage_metadata:
        module_logger.debug('Downloading expected values')
        expected_values_artifact = _download_artifact(run, download_dir, History.EXPECTED_VALUES,
                                                      explanation_id=explanation_id)
        kwargs[ExplainParams.EXPECTED_VALUES] = np.array(expected_values_artifact)

    if local_importance_vals is not None:
        module_logger.debug('Creating local explanation')
        local_explanation = _create_local_explanation(local_importance_values=local_importance_vals,
                                                      explanation_id=explanation_id,
                                                      **kwargs)
        kwargs[ExplainParams.LOCAL_EXPLANATION] = local_explanation
        if History.GLOBAL_IMPORTANCE_VALUES not in storage_metadata:
            module_logger.debug('Global importance values not found, returning local explanation')
            return local_explanation

    # Include everything available on storage metadata
    if History.CLASSES in storage_metadata:
        module_logger.debug('Downloading class names')
        kwargs[ExplainParams.CLASSES] = _download_artifact(run, download_dir, History.CLASSES,
                                                           explanation_id=explanation_id)

    download_list = [
        (History.GLOBAL_IMPORTANCE_NAMES, ExplainParams.GLOBAL_IMPORTANCE_NAMES),
        (History.GLOBAL_IMPORTANCE_RANK, ExplainParams.GLOBAL_IMPORTANCE_RANK),
        (History.GLOBAL_IMPORTANCE_VALUES, ExplainParams.GLOBAL_IMPORTANCE_VALUES),
        (History.PER_CLASS_NAMES, ExplainParams.PER_CLASS_NAMES),
        (History.PER_CLASS_RANK, ExplainParams.PER_CLASS_RANK),
        (History.PER_CLASS_VALUES, ExplainParams.PER_CLASS_VALUES)
    ]

    downloads = _download_sharded_data_from_list(download_list, storage_metadata, run, download_dir,
                                                 explanation_id=explanation_id, top_k=top_k)
    kwargs[History.GLOBAL_IMPORTANCE_RANK] = downloads[History.GLOBAL_IMPORTANCE_RANK]

    if History.PER_CLASS_RANK in downloads:
        kwargs[History.PER_CLASS_RANK] = downloads[History.PER_CLASS_RANK]

    if top_k is None and len(kwargs[History.GLOBAL_IMPORTANCE_RANK]) == len(kwargs[History.FEATURES]):
        # if we retrieve the whole explanation, we can reconstruct unsorted value order
        global_importance_values_unsorted = unsort_1d(downloads[History.GLOBAL_IMPORTANCE_VALUES],
                                                      downloads[History.GLOBAL_IMPORTANCE_RANK])
        kwargs[History.GLOBAL_IMPORTANCE_VALUES] = global_importance_values_unsorted

        if History.PER_CLASS_RANK in downloads:
            per_class_importance_values_unsorted = unsort_2d(downloads[History.PER_CLASS_VALUES],
                                                             downloads[History.PER_CLASS_RANK])
            kwargs[History.PER_CLASS_VALUES] = per_class_importance_values_unsorted
    else:
        # if we only retrieve top k, unsorted values cannot be fully reconstructed
        kwargs.update({
            History.RANKED_GLOBAL_NAMES: downloads[History.GLOBAL_IMPORTANCE_NAMES],
            History.RANKED_GLOBAL_VALUES: downloads[History.GLOBAL_IMPORTANCE_VALUES],
        })

        if History.PER_CLASS_RANK in downloads:
            kwargs.update({
                History.RANKED_PER_CLASS_NAMES: downloads[History.PER_CLASS_NAMES],
                History.RANKED_PER_CLASS_VALUES: downloads[History.PER_CLASS_VALUES],
            })

    return _create_global_explanation(explanation_id=explanation_id, **kwargs)


def download_model_explanation_from_run_id(workspace, experiment_name, run_id, top_k=None):
    """Get an explanation for a given run id from run history.

    :param workspace: An object that represents a workspace.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of an experiment.
    :type experiment_name: str
    :param run_id: A GUID that represents a run.
    :type run_id: str
    :param top_k: If specified, limit the ordered data returned to the most important features and values
    :type top_k: int
    :return: The explanation as it was uploaded to run history
    :rtype: BaseExplanation
    """
    module_logger.debug('Constructing run from workspace, experiment, and run ID')
    experiment = Experiment(workspace, experiment_name)
    run = Run(experiment, run_id=run_id)
    return download_model_explanation(run, top_k=top_k)


def list_model_explanations(run):
    """Return a dictionary of metadata for all model explanations available on a given run.

    :param run: The run from which the explanations were generated
    :type run: azureml.core.run.Run
    :return: A dictionary of explanation metadata such as id, data type, explanation method, model type,
        and upload time, sorted by upload time
    :rtype: dict
    """
    module_logger.debug('Listing model explanations')
    assets_client = AssetsClient(run.experiment.workspace.service_context)
    explanation_assets = assets_client.get_assets_by_run_id_and_name(run.id, History.EXPLANATION_ASSET)
    output_summary = []
    for asset in explanation_assets:
        meta_dict = {
            History.ID: asset.meta[History.EXPLANATION_ID] if History.EXPLANATION_ID in asset.meta else None,
            History.COMMENT: asset.meta[History.COMMENT] if History.COMMENT in asset.meta else None,
            ExplainType.DATA: asset.meta[ExplainType.DATA] if ExplainType.DATA in asset.meta else None,
            ExplainType.EXPLAIN: asset.meta[ExplainType.EXPLAIN] if ExplainType.EXPLAIN in asset.meta else None,
            ExplainType.MODEL: asset.meta[ExplainType.MODEL] if ExplainType.MODEL in asset.meta else None,
            History.UPLOAD_TIME: asset.created_time
        }
        output_summary.append(meta_dict)
    return sorted(output_summary, key=lambda meta: meta[History.UPLOAD_TIME])


def list_model_explanations_from_run_id(workspace, experiment_name, run_id):
    """Get an explanation for a given run id from run history.

    :param workspace: An object that represents a workspace.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of an experiment.
    :type experiment_name: str
    :param run_id: A GUID that represents a run.
    :type run_id: str
    :return: A dictionary of explanation metadata such as id, data type, explanation method, model type,
        and created time
    :rtype: dict
    """
    module_logger.debug('Constructing run from workspace, experiment, and run ID')
    experiment = Experiment(workspace, experiment_name)
    run = Run(experiment, run_id=run_id)
    return list_model_explanations(run)


def _download_sharded_data(run, download_dir, storage_metadata, name, explanation_id=None, top_k=None):
    """Download and aggregate a chunk of data from its sharded storage format.

    :param run: The run from which the explanation was generated
    :type run: azureml.core.run.Run
    :param download_dir: The directory to which the asset's files should be downloaded
    :type download_dir: str
    :param storage_metadata: The metadata dictionary for the asset's stored data
    :type storage_metadata: dict[str: dict[str: Union(str, int)]]
    :param name: The name/data type of the chunk to download_dir
    :type name: str
    :param explanation_id: The explanation ID the data is stored under.
        If None, it is assumed that the asset is using an old storage format.
    :type explanation_id: str
    :param top_k: If specified, limit the ordered data returned to the most important features and values
    :type top_k: int
    :return: The data chunk, anything from 1D to 3D, int or str
    """
    num_columns_to_return = int(storage_metadata[name][History.NUM_FEATURES])
    if top_k is not None:
        module_logger.debug('Top k is set, potentially reducing number of columns returned')
        num_columns_to_return = min(top_k, num_columns_to_return)
    num_blocks = int(storage_metadata[name][History.NUM_BLOCKS])
    if BackCompat.OLD_NAME in storage_metadata[name]:
        module_logger.debug('Working with constructed metadata from a v1 asset')
        # Backwards compatibility as of January 2019
        name = storage_metadata[name][BackCompat.OLD_NAME]
    # Backwards compatibility as of February 2019
    connector = '/' if explanation_id is not None else '_'
    artifact = _download_artifact(run, download_dir, '{}{}0'.format(name, connector), explanation_id=explanation_id)
    full_data = np.array(artifact)
    concat_dim = full_data.ndim - 1
    # Get the blocks
    for idx in range(1, num_blocks):
        block_name = '{}{}{}'.format(name, connector, idx)
        block = np.array(_download_artifact(run, download_dir, block_name))
        full_data = np.concatenate([full_data, block], axis=concat_dim)
        num_columns_read = full_data.shape[concat_dim]
        if num_columns_read >= num_columns_to_return:
            break
    full_data_list = full_data[..., :num_columns_to_return]
    return full_data_list


def _get_v2_metadata_from_v1(v1_metadata):
    """Convert the v1 asset metadata dict to a v2 asset metadata dict.

    :param v1_metadata: a flat dict of v1 metadata
    :type v1_metadta: dict[str: int]
    :return: a rich dict of v2 metadata
    :rtype: dict[str: dict[str: Union(str, int)]]
    """
    storage_metadata = {
        History.GLOBAL_IMPORTANCE_NAMES: _get_v2_shard_from_v1(v1_metadata,
                                                               BackCompat.OVERALL_FEATURE_ORDER,
                                                               History.GLOBAL_IMPORTANCE_NAMES),
        History.GLOBAL_IMPORTANCE_RANK: _get_v2_shard_from_v1(v1_metadata,
                                                              BackCompat.OVERALL_IMPORTANCE_ORDER,
                                                              History.GLOBAL_IMPORTANCE_RANK),
        History.GLOBAL_IMPORTANCE_VALUES: _get_v2_shard_from_v1(v1_metadata,
                                                                BackCompat.OVERALL_SUMMARY,
                                                                History.GLOBAL_IMPORTANCE_VALUES)
    }

    # these fields may or may not exist on v1 assets
    if History.BLOCK_SIZE + '_' + BackCompat.PER_CLASS_FEATURE_ORDER in v1_metadata:
        storage_metadata[History.PER_CLASS_NAMES] = \
            _get_v2_shard_from_v1(v1_metadata, BackCompat.PER_CLASS_FEATURE_ORDER, History.PER_CLASS_NAMES)
        storage_metadata[History.PER_CLASS_RANK] = \
            _get_v2_shard_from_v1(v1_metadata, BackCompat.PER_CLASS_IMPORTANCE_ORDER, History.PER_CLASS_RANK)
        storage_metadata[History.PER_CLASS_VALUES] = \
            _get_v2_shard_from_v1(v1_metadata, BackCompat.PER_CLASS_SUMMARY, History.PER_CLASS_VALUES)
    if History.NUM_CLASSES in v1_metadata:
        class_dict = {
            BackCompat.NAME: History.CLASSES,
            History.NUM_CLASSES: v1_metadata[History.NUM_CLASSES]
        }
        storage_metadata[History.CLASSES] = class_dict
    return storage_metadata


def _get_v2_shard_from_v1(v1_metadata, v1_name, v2_name):
    """Get specific metadata for v2 shards from v1 metadata.

    :param v1_metadata: a flat dict of v1 metadata
    :type v1_metadta: dict[str: int]
    :param v1_name: The v1 name for the chunked data
    :type v1_name: str
    :param v2_name: The v2 name for the chunked data
    :type v2_name: str
    :return: The dict of shard metadata
    :rtype: dict[str: str | int]
    """
    return {
        History.NAME: v2_name,
        BackCompat.OLD_NAME: v1_name,
        History.BLOCK_SIZE: v1_metadata[History.BLOCK_SIZE + '_' + v1_name],
        History.MAX_NUM_BLOCKS: v1_metadata[History.MAX_NUM_BLOCKS + '_' + v1_name],
        History.NUM_BLOCKS: v1_metadata[History.NUM_BLOCKS + '_' + v1_name],
        History.NUM_FEATURES: v1_metadata[History.NUM_FEATURES + '_' + v1_name]
    }


def _download_sharded_data_from_list(data_tuples, storage_metadata, run, download_dir, explanation_id=None,
                                     top_k=None):
    """Check each data name in the list.

    If available on the stored explanation, download the sharded chunks and reconstruct the explanation.

    :param data_tuples: A list of data names and dict key names for each kind of data to download
    :type data_tuples: list[(str, str)]
    :param storage_metadata: The metadata dictionary for the asset's stored data
    :type storage_metadata: dict[str: dict[str: Union(str, int)]]
    :param run: The run from which the explanation was generated
    :type run: azureml.core.run.Run
    :param download_dir: The directory to which the asset's files should be downloaded
    :type download_dir: str
    :param explanation_id: The explanation ID the data is stored under.
        If None, it is assumed that the asset is using an old storage format.
    :type explanation_id: str
    :param top_k: If specified, limit the ordered data returned to the most important features and values
    :type top_k: int
    :return: A dictionary of the data that was able to be downloaded from run history
    :rtype: dict
    """
    output_kwargs = {}
    for history_name, key_name in data_tuples:
        if history_name in storage_metadata:
            module_logger.debug('Downloading ' + history_name)
            values = _download_sharded_data(run, download_dir, storage_metadata, history_name,
                                            explanation_id=explanation_id, top_k=top_k)
            output_kwargs[key_name] = np.array(values)
    return output_kwargs


def _create_local_explanation(expected_values=None, classification=True,
                              scoring_model=None, text_explanation=False, explanation_id=None, **kwargs):
    """Dynamically creates an explanation based on local type and specified data.

    :param expected_values: The expected values of the model.
    :type expected_values: list
    :param classification: Indicates if this is a classification or regression explanation.
    :type classification: bool
    :param scoring_model: The scoring model.
    :type scoring_model: ScoringModel
    :param text_explanation: Indicates if this is a text explanation.
    :type text_explanation: bool
    :param explanation_id: If specified, puts the local explanation under a preexisting explanation object.
        If not, a new unique identifier will be created for the explanation.
    :type explanation_id: str
    :return: The local explanation
    :rtype: LocalExplanation
    """
    exp_id = explanation_id or str(uuid.uuid4())
    if text_explanation:
        mixins = [TextExplanation]
    else:
        mixins = [LocalExplanation]
    if expected_values is not None:
        mixins.append(ExpectedValuesMixin)
        kwargs[ExplanationParams.EXPECTED_VALUES] = expected_values
    if scoring_model is not None:
        mixins.append(HasScoringModel)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
    if classification:
        mixins.append(ClassesMixin)
    DynamicLocalExplanation = type(Dynamic.LOCAL_EXPLANATION, tuple(mixins), {})
    local_explanation = DynamicLocalExplanation(explanation_id=exp_id, **kwargs)
    return local_explanation


def _create_global_explanation(local_explanation=None, expected_values=None,
                               classification=True, scoring_model=None,
                               text_explanation=False, explanation_id=None, **kwargs):
    """Dynamically creates an explanation based on global type and specified data.

    :param local_explanation: The local explanation information to include with global,
        can be done when the global explanation is a summary of local explanations.
    :type local_explanation: LocalExplanation
        :param expected_values: The expected values of the model.
        :type expected_values: list
    :param classification: Indicates if this is a classification or regression explanation.
    :type classification: bool
    :param scoring_model: The scoring model.
    :type scoring_model: ScoringModel
    :param text_explanation: Indicates if this is a text explanation.
    :type text_explanation: bool
    :param explanation_id: If specified, puts the global explanation under a preexisting explanation object.
        If not, a new unique identifier will be created for the explanation.
    :type explanation_id: str
    :return: The global explanation
    :rtype: GlobalExplanation
    """
    if local_explanation is not None and LocalExplanation._does_quack(local_explanation):
        exp_id = local_explanation.id
    else:
        exp_id = explanation_id or str(uuid.uuid4())
    mixins = [GlobalExplanation]
    # Special case: for aggregate explanations, we can include both global
    # and local explanations for the user as an optimization, so they
    # don't have to call both explain_global and explain_local and redo the
    # same computation twice
    if local_explanation is not None:
        mixins.append(LocalExplanation)
        kwargs[ExplainParams.LOCAL_IMPORTANCE_VALUES] = np.array(local_explanation.local_importance_values)
    # In the mimic case, we don't aggregate so we can't have per class information
    # but currently in other cases when we aggregate local explanations we get per class
    if classification:
        if local_explanation is not None:
            mixins.append(PerClassMixin)
        else:
            mixins.append(ClassesMixin)
    if expected_values is not None:
        mixins.append(ExpectedValuesMixin)
        kwargs[ExplanationParams.EXPECTED_VALUES] = expected_values
    if scoring_model is not None:
        mixins.append(HasScoringModel)
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
    DynamicGlobalExplanation = type(Dynamic.GLOBAL_EXPLANATION, tuple(mixins), {})
    global_explanation = DynamicGlobalExplanation(explanation_id=exp_id, **kwargs)
    return global_explanation


def _aggregate_global_from_local_explanation(local_explanation=None, include_local=True,
                                             features=None, explanation_id=None, **kwargs):
    """Aggregate the local explanation information to global through averaging.

    :param local_explanation: The local explanation to summarize.
    :type local_explanation: LocalExplanation
    :param include_local: Whether the global explanation should also include local information.
    :type include_local: bool
    :param features: A list of feature names.
    :type features: list[str]
    :param explanation_id: If specified, puts the aggregated explanation under a preexisting explanation object.
        If not, a new unique identifier will be created for the explanation.
    :type explanation_id: str
    """
    if local_explanation is not None and LocalExplanation._does_quack(local_explanation):
        exp_id = local_explanation.id
    else:
        exp_id = explanation_id or str(uuid.uuid4())
    features = local_explanation.features
    kwargs[ExplainParams.FEATURES] = features
    local_importance_values = np.array(local_explanation.local_importance_values)
    classification = ClassesMixin._does_quack(local_explanation)
    if classification:
        per_class_values = np.mean(np.absolute(local_importance_values), axis=1)
        per_class_rank = _order_imp(per_class_values)
        global_importance_values = np.mean(per_class_values, axis=0)
        global_importance_rank = _order_imp(global_importance_values)
        kwargs[ExplainParams.PER_CLASS_VALUES] = per_class_values
        kwargs[ExplainParams.PER_CLASS_RANK] = per_class_rank
    else:
        global_importance_values = np.mean(np.absolute(local_importance_values), axis=0)
        global_importance_rank = _order_imp(global_importance_values)

    kwargs[ExplainParams.GLOBAL_IMPORTANCE_RANK] = global_importance_rank
    kwargs[ExplainParams.GLOBAL_IMPORTANCE_VALUES] = global_importance_values
    expected_values = None
    if ExpectedValuesMixin._does_quack(local_explanation):
        expected_values = np.array(local_explanation.expected_values)
    scoring_model = None
    if HasScoringModel._does_quack(local_explanation):
        scoring_model = local_explanation.scoring_model
    if include_local:
        kwargs[ExplainParams.LOCAL_EXPLANATION] = local_explanation
    return _create_global_explanation(expected_values=expected_values, classification=classification,
                                      scoring_model=scoring_model, explanation_id=exp_id, **kwargs)
