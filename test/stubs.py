"""
Fake clients and data structures to use in tests
"""

from typing import Any, Dict, List


class FakeMessage:
    def __init__(self, value: Any):
        self.value = value


class FakeKafkaClient:
    def __init__(self, topic: str | None = None) -> None:
        self.topic = topic
        self.storage: Dict[str, List[List[FakeMessage]]] = {}

    def poll(self):
        return self

    def values(self):
        return self.storage[self.topic]

    def send(self, topic: str, value: bytes):
        if topic not in self.storage:
            self.storage[topic] = []
        self.storage[topic].append([FakeMessage(value=value)])

    def n_messages_were_sent(self, topic: str, n_messages: int) -> bool:
        qty_received = len(self.storage[topic])
        return n_messages == qty_received


class FakePostgresClient:
    def __init__(self, *args, **kwargs):
        self.storage = []

    def write(self, data):
        self.storage.append(data)

    def n_messages_were_stored(self, n_messages: int) -> bool:
        qty_received = len(self.storage)
        return n_messages == qty_received
