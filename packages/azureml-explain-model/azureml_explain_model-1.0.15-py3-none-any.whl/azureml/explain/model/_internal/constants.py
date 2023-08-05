# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines constants for explain model."""


class BackCompat(object):
    """Constants necessary for supporting old versions of our product"""
    NAME = 'name'
    OLD_NAME = 'old_name'
    OVERALL_FEATURE_ORDER = 'overall_feature_order'
    OVERALL_IMPORTANCE_ORDER = 'overall_importance_order'
    OVERALL_SUMMARY = 'overall_summary'
    PER_CLASS_FEATURE_ORDER = 'per_class_feature_order'
    PER_CLASS_IMPORTANCE_ORDER = 'per_class_importance_order'
    PER_CLASS_SUMMARY = 'per_class_summary'


class ExplanationParams(object):
    """Constants for explanation parameters"""
    EXPECTED_VALUES = 'expected_values'
    CLASSES = 'classes'


class History(object):
    """Constants related to uploading assets to run history"""
    BLOCK_SIZE = 'block_size'
    CLASSES = 'classes'
    EXPECTED_VALUES = 'expected_values'
    EXPLANATION = 'explanation'
    EXPLANATION_ASSET = 'explanation_asset'
    EXPLANATION_ASSET_TYPE_V1 = 'azureml.v1.model.explanation'
    EXPLANATION_ASSET_TYPE_V2 = 'azureml.v2.model.explanation'
    FEATURE_NAMES = 'feature_names'
    FEATURES = 'features'
    GLOBAL_IMPORTANCE_NAMES = 'global_importance_names'
    GLOBAL_IMPORTANCE_RANK = 'global_importance_rank'
    GLOBAL_IMPORTANCE_VALUES = 'global_importance_values'
    LOCAL_IMPORTANCE_VALUES = 'local_importance_values'
    MAX_NUM_BLOCKS = 'max_num_blocks'
    METADATA_ARTIFACT = 'metadata_artifact_path'
    NAME = 'name'
    NUM_BLOCKS = 'num_blocks'
    NUM_CLASSES = 'num_classes'
    NUM_FEATURES = 'num_features'
    PER_CLASS_NAMES = 'per_class_importance_names'
    PER_CLASS_RANK = 'per_class_importance_rank'
    PER_CLASS_VALUES = 'per_class_importance_values'
    PREFIX = 'prefix'
    RICH_METADATA = 'rich_metadata'
    SHAP_VALUES = 'shap_values'
    TYPE = 'type'
    VERSION = 'version'
    VERSION_TYPE = 'version_type'


class ExplainType(object):
    """Constants for model and explainer type information, useful for visualization"""
    CLASSIFICATION = 'classification'
    DATA = 'data_type'
    EXPLAIN = 'explain_type'
    EXPLAINER = 'explainer'
    MODEL = 'model_type'
    REGRESSION = 'regression'
    SHAP = 'shap'
    TABULAR = 'tabular'
    TEXT = 'text'


class IO(object):
    """File input and output related constants"""
    UTF8 = 'utf-8'


class ExplainParams(object):
    """Constants for explain model (explain_local and explain_global) parameters"""
    CLASSES = 'classes'
    CLASSIFICATION = 'classification'
    EXPECTED_VALUES = 'expected_values'
    FEATURES = 'features'
    GLOBAL_IMPORTANCE_NAMES = 'global_importance_names'
    GLOBAL_IMPORTANCE_VALUES = 'global_importance_values'
    GLOBAL_IMPORTANCE_RANK = 'global_importance_rank'
    LOCAL_EXPLANATION = 'local_explanation'
    LOCAL_IMPORTANCE_VALUES = 'local_importance_values'
    ORDER = 'order'
    PER_CLASS_NAMES = 'per_class_names'
    PER_CLASS_RANK = 'per_class_rank'
    PER_CLASS_VALUES = 'per_class_values'
    SCORING_MODEL = 'scoring_model'
    EXPLAIN_SUBSET = 'explain_subset'
    SILENT = 'silent'
    NSAMPLES = 'nsamples'
    SAMPLING_POLICY = 'sampling_policy'
    CREATE_SCORING_MODEL = 'create_scoring_model'
    TOP_K = 'top_k'
    NCLUSTERS = 'nclusters'


class Defaults(object):
    """Constants for default values to explain methods"""
    AUTO = 'auto'
    # hdbscan is an unsupervised learning library to find the optimal number of clusters in a dataset
    # See this github repo for more details: https://github.com/scikit-learn-contrib/hdbscan
    HDBSCAN = 'hdbscan'
    MAX_DIM = 50


class Attributes(object):
    """Constants for attributes"""
    EXPECTED_VALUE = 'expected_value'


class Dynamic(object):
    """Constants for dynamically generated classes"""
    LOCAL_EXPLANATION = 'DynamicLocalExplanation'
    GLOBAL_EXPLANATION = 'DynamicGlobalExplanation'


class Tensorflow(object):
    """Tensorflow and tensorboard related constants"""
    TFLOG = 'tflog'
    CPU0 = '/CPU:0'


class SKLearn(object):
    """Scikit-learn related constants"""
    PREDICTIONS = 'predictions'
    LABELS = 'labels'
    EXAMPLES = 'examples'
    BALL_TREE = 'ball_tree'


class Spacy(object):
    """Spacy related constants"""
    NER = 'ner'
    TAGGER = 'tagger'
    EN = 'en'
