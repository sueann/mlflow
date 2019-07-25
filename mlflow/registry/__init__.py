"""
The ``mlflow.registry`` module provides a Python CRUD interface to MLflow Model Registry.
This is a lower level API that directly translates to MLflow `REST API <../rest-api.html>`_
calls. For a higher level API for registering models, use the :py:mod:`mlflow` module.
"""

from mlflow.registry.client import MlflowRegistryClient
from mlflow.registry.utils import set_registry_uri, get_registry_uri, _REGISTRY_URI_ENV_VAR

__all__ = [
    "MlflowRegistryClient",
    "get_registry_uri",
    "set_registry_uri",
    "_REGISTRY_URI_ENV_VAR",
]
