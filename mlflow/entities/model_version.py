from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import ModelVersion as ProtoModelVersion


class ModelVersion(_MLflowObject):
    """
    ModelVersion object.
    """

    def __init__(self, model_name, version):
        super(ModelVersion, self).__init__()
        self._model_name = model_name
        self._version = version

    @property
    def model_name(self):
        return self._model_name

    @property
    def version(self):
        return self._version

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.model_name, proto.version)

    def to_proto(self):
        proto = ProtoModelVersion()
        proto.model_name = self.model_name
        proto.version = self.version
        return proto
