"""
Module providing a Python CRUD interface to MLflow registered models and
model versions.
"""

from mlflow.entities import RegisteredModel, ModelVersion
from mlflow.registry import utils


class MlflowRegistryClient(object):
    """
    Client of an MLflow Model Registry Server that creates and manages registered models and model versions.
    """
    def __init__(self, registry_uri=None):
        """
        :param registry_uri: Address of local or remote registry server. If not provided, defaults
                             to the service set by ``mlflow.registry.set_tracking_uri``. <TODO: link to docs>
        """
        self.registry_uri = registry_uri or utils.get_registry_uri()

    # RegisteredModel methods

    def create_registered_model(self, name):
        raise NotImplementedError()

    def rename_registered_model(self, name, new_name):
        raise NotImplementedError()

    def delete_registered_model(self, name):
        raise NotImplementedError()

    def list_registered_models(self):
        raise NotImplementedError()

    # ModelVersion methods

    def create_model_version(self, name, source):
        # we may need to copy from source to local context then upload to dbfs if registry is on databricks
        # or, initially we only support dbfs -> dbfs copy and handle it on the server
        # can the mlflow server read from s3/azure blob locations mounted onto dbfs?
        raise NotImplementedError()

    def get_model_version(self, name, source):
        raise NotImplementedError()

    def update_model_version(self, name, version, stage):
        # Q: should we ship OSS MLflow with a fixed set of stages?
        raise NotImplementedError()

    def delete_model_version(self, name, version):
        """
        Delete the model and associated metadata. Unique ID and model version number cannot be reused.
        """
        raise NotImplementedError()

    def search_model_versions(self, filter, max_results, order_by, page_token):
        raise NotImplementedError()
