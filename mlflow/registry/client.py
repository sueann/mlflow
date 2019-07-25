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
    """
    Create: This is an API or UI flow to create an entity in Model Registry with a unique name. When created, this RegisteredModel is an empty collection. Multiple ModelVersion entities may be added for this RegisteredModel--they all have the same name inherited from the RegisteredModel and unique version number.
    POST 2.0/mlflow/registered-models/create
    Rename: Change the name for this model. Name uniqueness guarantee with the registry needs to be satisfied after name change.
    PUT/PATCH or POST 2.0/mlflow/registered-models/update
    Delete a RegisteredModel. All ModelVersion entities associated with this name will also be deleted.
    DELETE 2.0/mlflow/registered-models/delete
    List all RegisteredModels will return a list of RegisteredModel entities
    GET 2.0/mlflow/registered-models/list
    """

    # ModelVersion methods
    """
    Register a new version: Adds a new model within RegisteredModel, of the given name. Incrementally generate a new version and generate a unique identifier. Models have a source (run_id, "runs://…" source URI, or a URI path the model). This model needs to be copied into registry.
    POST 2.0/mlflow/model-versions/create
    Delete the model and associated metadata. Unique ID and model version number cannot be reused.
    DELETE 2.0/mlflow/model-versions/delete
    Update metadata for ModelVersions
        PUT/PATCH or POST 2.0/mlflow/model-versions/update
    Get metadata for ModelVersions.
        GET 2.0/mlflow/model-versions/get-info
    Search registry for ModelVersions using associated metadata.
    GET 2.0/mlflow/model-versions/search
    List all ModelVersions for a RegisteredModel
        GET 2.0/mlflow/model-versions/search (reuse search API for this)
    
    Transitions, comments, ACLs are edge features and will be accessed by the REST API and UI only.
    """


