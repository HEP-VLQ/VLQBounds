from abc import ABC, abstractmethod
from typing import Optional


class Result(ABC):
    def __init__(self) -> None:
        self._result: Optional[int] = None
        self._channel: Optional[int] = None
        self._obs_ratio: Optional[float] = None
        self._exp_ratio: Optional[float] = None

    @abstractmethod
    def set_result(self, position: int) -> None:
        pass

    def __str__(self) -> str:
        return (
            f"Exclusion result: {self._result} (1 = allowed, 0 = excluded)\n"
            f"Channel         : {self._channel if self._channel is not None else 'N/A'}\n"
            f"Observed ratio  : {self._obs_ratio if self._obs_ratio is not None else 'N/A'}\n"
            f"Expected Ratio  : {self._exp_ratio if self._exp_ratio is not None else 'N/A'}"
        )
