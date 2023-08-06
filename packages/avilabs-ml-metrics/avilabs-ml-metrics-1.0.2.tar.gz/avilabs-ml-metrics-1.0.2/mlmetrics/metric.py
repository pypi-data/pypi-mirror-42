from abc import ABC, abstractmethod
from typing import Iterator, Tuple, List


class Metric(ABC):
    @abstractmethod
    def log(self, **kwargs) -> None:
        raise NotImplemented()

    @abstractmethod
    def start_snapshot(self) -> None:
        raise NotImplemented()

    @abstractmethod
    def stop_snapshot(self) -> None:
        raise NotImplemented()

    @abstractmethod
    def logs(self, start=-1, end=-1, **filters) -> Iterator[Tuple]:
        raise NotImplemented()

    @abstractmethod
    def snapshots(self, start=-1, end=-1, **filters) -> Iterator[List[Tuple]]:
        raise NotImplemented()

    @abstractmethod
    def close(self) -> None:
        raise NotImplemented()
