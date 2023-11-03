from abc import abstractmethod, ABC
from enum import Enum


class ModuleReturn(Enum):
    EXIT = -1
    SKIP = 0
    NEXT = 1


class ToolType(Enum):
    PROTON = "proton"
    OTHER = "other"


class BaryonModule(ABC):
    @abstractmethod
    def module_run(self, pre_command: list, command: list, command_args: list, tool_type=ToolType.OTHER,
                   verb=None, is_scriptevaluator=None, **kwargs) -> ModuleReturn:
        raise NotImplementedError

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, tool_type=ToolType.OTHER,
                   verb=None, is_scriptevaluator=None, **kwargs):
        return 0


def proton_index(command):
    for i, cmd in enumerate(command[:-1]):
        if "proton" in cmd and "run" in command[i + 1]:
            return i
    return -1
