from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import RegisteredModel as ProtoRegisteredModel


class RegisteredModel(_MLflowObject):
    """
    RegisteredModel object.
    """

    def __init__(self, name):
        super(RegisteredModel, self).__init__()
        self._name = name

    @property
    def name(self):
        """String name of the registered model."""
        return self._name

    def _set_name(self, new_name):
        self._name = new_name

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.name)

    def to_proto(self):
        proto = ProtoRegisteredModel()
        proto.name = self._name
        return proto
