

#
# # TODO(ML-6262) - should this support Runs URI? there is no run context here. and it does not assume a tracking server
# #  is available in the context. this utils module could use better separation of methods based on what context is
# #  assumed (tracking vs models / deploy vs projects ...). It is also confusing to talk about tracking URIs and artifact
# #  URIs in the same file / module.
# def _download_artifact_from_uri(artifact_uri, output_path=None):
#     """
#     :param artifact_uri: The *absolute* URI of the artifact to download.
#     :param output_path: The local filesystem path to which to download the artifact. If unspecified,
#                         a local output path will be created.
#     """
#     store = _get_store(artifact_uri=artifact_uri)
#     artifact_path_module = \
#         get_artifact_repository(artifact_uri, store).get_path_module()
#     artifact_src_dir = artifact_path_module.dirname(artifact_uri)
#     artifact_src_relative_path = artifact_path_module.basename(artifact_uri)
#     artifact_repo = get_artifact_repository(
#         artifact_uri=artifact_src_dir, store=store)
#     return artifact_repo.download_artifacts(
#         artifact_path=artifact_src_relative_path, dst_path=output_path)