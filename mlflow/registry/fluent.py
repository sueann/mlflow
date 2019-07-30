from mlflow.registry.client import MlflowRegistryClient

def register_model_version(name, artifact_uri):
    """
    Registers a new version of RegisteredModel named ``name``, creating such a RegisteredModel if
    one does not exist.
    :param name: name of the RegisteredModel the new model version belongs to.
    :param artifact_uri: location of the model files to associate with the model version. Use a
    ``runs:/`` URI if you'd like to associate a ``run_id`` with the model version as well.
    :return: ModelVersion object corresponding to the newly created model version.
    """
    raise NotImplementedError()

def list_model_versions(name):
    """
    List all model versions for the RegisteredModel with name ``name``.
    :param name: name of the RegisteredModel for which to list the model versions.
    :return: List of ModelVersion objects.
    """
    raise NotImplementedError()
