import os

from modules import BaryonModule
from modules import ModuleReturn


class Renice(BaryonModule):
    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, **kwargs) -> ModuleReturn:
        if bool(int(os.environ.get("BARYON_RENICE", 0))):
            # be careful your OS must allow you to set nice value less than 0 without root
            __niceness = str(os.environ.get("BARYON_NICE", "-11"))
            pre_command.insert(0, ["nice", f"-{__niceness}"])

        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 200


def get_module() -> BaryonModule:
    return Renice()
