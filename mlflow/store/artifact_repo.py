import os
import tempfile
from abc import abstractmethod, ABCMeta

from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE, RESOURCE_DOES_NOT_EXIST
from mlflow.utils.file_utils import build_path


class ArtifactRepository:
    """
    Abstract artifact repo that defines how to upload (log) and download potentially large
    artifacts from different storage backends.
    """

    __metaclass__ = ABCMeta

    def __init__(self, artifact_uri):
        # TODO(ML-6262) - we want this to be something like artifact_uri_base, which may contain
        #  e.g. auth info. Or, ArtifactRepository could only have classmethods that work with
        #  absolute URIs. RunArtifactRepo could contain artifact_uri and construct the absolute
        #  URI to the underlying artifact repos.
        self.artifact_uri = artifact_uri

    # TODO(ML-6262) - ideally this becomes protected
    @abstractmethod
    def get_path_module(self):
        """
        :return: The Python path module that should be used for parsing and modifying artifact
                 paths. For example, if the artifact repository's URI scheme uses POSIX paths,
                 this method may return the ``posixpath`` module.
        """

    # TODO(ML-6262): we probably want a standard set of functions to deal with URIs -- just so RunArtifactRepository
    #  can use it. e.g.
    #    def get_absolute_uri(base_path, relative_path)
    #  would be nice even without the change of method arguments to absolute URIs.
    #   --- Actually don't need it if we just use absolute URIs everywhere.

    # TODO(ML-6262) - artifact_path should be required, unless you are RunArtifactRepository
    #   actually the most convenient would be if the artifact_path could be an absolute URI -or- a relative path
    #   The goal would be to eliminate the need to do any URI parsing as a user of ArtifactRepository.
    #   [Weirdness] __init__ takes in a URI but it will ignore any part of actual path (non-metadata)
    #   In a way, artifact repositories are a weird concept. All functions could take in absolute URIs and do the
    #   parsing right there.
    #   Only when you have a run context, does it become useful to have relative paths. Even there, it can take in
    #   the Runs URI and have the same functions. Also doing "parsing" as needed.
    #  > All these classes can be static classes.
    #  The only times ``get_artifact_repository`` seems used, the object is used only *once*.

    # TODO(ML-6262) - we can have a higher-level set of functions that correspond to ArtifactRepository methods
    #   that take in a URI and initializes the correct ArtifactRepository and does the action.
    #   For Runs, there is tracking/client.py.
    #   For other URIs, it is simple enough to do artifact_repository_registry.get_artifact_repository(URI).xxx(..., URI)
    #   though it is a bit redundant. We can create an artifacts module (maybe store.artifacts __init__.py).
    #   This is essentially what store/cli.py does. Why don't we have a corresponding API (like we do in tracking I believe)?

    @abstractmethod
    def log_artifact(self, local_file, artifact_path=None):
        """
        Log a local file as an artifact, optionally taking an ``artifact_path`` to place it in a
        subpath of ``artifact_uri``. Artifacts can be organized into directories, so you can
        place the artifact in a directory this way.

        :param local_file: Path to artifact to log
        :param artifact_path: Directory within the repo's artifact directory in which to log the
                              artifact
        """
        pass

    @abstractmethod
    def log_artifacts(self, local_dir, artifact_path=None):
        """
        Log the files in the specified local directory as artifacts, optionally taking
        an ``artifact_path`` to place them in a subpath of ``artifact_uri``.

        :param local_dir: Directory of local artifacts to log
        :param artifact_path: Directory within the repo's artifact directory in which to log the
                              artifacts
        """
        pass

    @abstractmethod
    def list_artifacts(self, path):
        """
        Return all the artifacts for directly under path (which is assumed to be within
        the artifact repo's ``artifact_uri``). If ``path`` is a file, returns
        an empty list. Will error if ``path`` is neither a file nor a directory.

        :param path: Relative source path that contain desired artifacts

        :return: List of artifacts as FileInfo listed directly under path.
        """
        pass

    def download_artifacts(self, artifact_path, dst_path=None):
        """
        Download an artifact file or directory to a local directory if applicable, and return a
        local path for it.
        The caller is responsible for managing the lifecycle of the downloaded artifacts.

        :param path: Source path to the desired artifacts, relative to the repo's artifact directory
        :param dst_path: Absolute path of the local filesystem destination directory to which to
                         download the specified artifacts. This directory must already exist. If
                         unspecified, the artifacts will be downloaded to a new, uniquely-named
                         directory on the local filesystem.

        :return: Absolute path of the local filesystem location containing the downloaded artifacts.
        """
        # TODO: Probably need to add a more efficient method to stream just a single artifact
        # without downloading it, or to get a pre-signed URL for cloud storage.

        def download_artifacts_into(artifact_path, dest_dir):
            basename = self.get_path_module().basename(artifact_path)
            local_path = build_path(dest_dir, basename)
            listing = self.list_artifacts(artifact_path)
            if len(listing) > 0:
                # Artifact_path is a directory, so make a directory for it and download everything
                if not os.path.exists(local_path):
                    os.mkdir(local_path)
                for file_info in listing:
                    download_artifacts_into(artifact_path=file_info.path, dest_dir=local_path)
            else:
                self._download_file(remote_file_path=artifact_path, local_path=local_path)
            return local_path

        if dst_path is None:
            dst_path = os.path.abspath(tempfile.mkdtemp())

        if not os.path.exists(dst_path):
            raise MlflowException(
                    message=(
                        "The destination path for downloaded artifacts does not"
                        " exist! Destination path: {dst_path}".format(dst_path=dst_path)),
                    error_code=RESOURCE_DOES_NOT_EXIST)
        elif not os.path.isdir(dst_path):
            raise MlflowException(
                    message=(
                        "The destination path for downloaded artifacts must be a directory!"
                        " Destination path: {dst_path}".format(dst_path=dst_path)),
                    error_code=INVALID_PARAMETER_VALUE)

        return download_artifacts_into(artifact_path, dst_path)

    @abstractmethod
    def _download_file(self, remote_file_path, local_path):
        """
        Download the file at the specified relative remote path and saves
        it at the specified local path.

        :param remote_file_path: Source path to the remote file, relative to the root
                                 directory of the artifact repository.
        :param local_path: The path to which to save the downloaded file.
        """
        pass
