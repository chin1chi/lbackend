import pickle
import json
from abc import ABC, abstractmethod
from typing import Any


class AbstractSerializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def deserialize(self, obj: Any) -> Any:
        pass


class PickleSerializer(AbstractSerializer):
    def serialize(self, obj: Any) -> bytes:
        return pickle.dumps(obj)

    def deserialize(self, obj: Any) -> Any:
        return pickle.loads(obj)


class JSONSerializer(AbstractSerializer):
    def serialize(self, obj: Any) -> bytes:
        return json.dumps(obj)

    def deserialize(self, obj: Any) -> Any:
        return json.loads(obj)