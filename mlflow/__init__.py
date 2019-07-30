"""
The ``mlflow`` module provides an API for starting and managing MLflow runs.
For example:

.. code:: python

    import mlflow
    mlflow.start_run()
    mlflow.log_param("my", "param")
    mlflow.log_metric("score", 100)
    mlflow.end_run()

You can also use syntax like this:

.. code:: python

    with mlflow.start_run() as run:
        ...

which automatically terminates the run at the end of the block.

The tracking API is not currently threadsafe. Any concurrent callers to the tracking API must
implement mutual exclusion manually.

For a lower level API, see the :py:mod:`mlflow.tracking` module.
"""
from mlflow.version import VERSION as __version__
from mlflow.utils.logging_utils import _configure_mlflow_loggers
import mlflow.tracking.fluent

# Filter annoying Cython warnings that serve no good purpose, and so before
# importing other modules.
# See: https://github.com/numpy/numpy/pull/432/commits/170ed4e33d6196d7
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")  # noqa: E402
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")  # noqa: E402
# log a deprecated warning only once per function per module
warnings.filterwarnings("module", category=DeprecationWarning)

# pylint: disable=wrong-import-position
import mlflow.projects as projects  # noqa
import mlflow.tracking as tracking  # noqa

_configure_mlflow_loggers(root_module_name=__name__)

ActiveRun = mlflow.tracking.fluent.ActiveRun
log_param = mlflow.tracking.fluent.log_param
log_metric = mlflow.tracking.fluent.log_metric
set_tag = mlflow.tracking.fluent.set_tag
delete_tag = mlflow.tracking.fluent.delete_tag
log_artifacts = mlflow.tracking.fluent.log_artifacts
log_artifact = mlflow.tracking.fluent.log_artifact
active_run = mlflow.tracking.fluent.active_run
start_run = mlflow.tracking.fluent.start_run
end_run = mlflow.tracking.fluent.end_run
search_runs = mlflow.tracking.fluent.search_runs
get_artifact_uri = mlflow.tracking.fluent.get_artifact_uri
set_tracking_uri = tracking.set_tracking_uri
get_tracking_uri = tracking.get_tracking_uri
create_experiment = mlflow.tracking.fluent.create_experiment
set_experiment = mlflow.tracking.fluent.set_experiment
log_params = mlflow.tracking.fluent.log_params
log_metrics = mlflow.tracking.fluent.log_metrics
set_tags = mlflow.tracking.fluent.set_tags
# register_model - handles both models and versions
# search? not sure if needed

run = projects.run


__all__ = ["ActiveRun", "log_param", "log_params", "log_metric", "log_metrics", "set_tag",
           "set_tags", "delete_tag", "log_artifacts", "log_artifact", "active_run", "start_run",
           "end_run", "search_runs", "get_artifact_uri", "set_tracking_uri", "create_experiment",
           "set_experiment", "run"]
