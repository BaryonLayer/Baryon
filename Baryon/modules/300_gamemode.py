import os
from shutil import which

from modules import BaryonModule
from modules import ModuleReturn


class Gamemode(BaryonModule):
    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, is_scriptevaluator=False,
                   **kwargs) -> ModuleReturn:
        if not is_scriptevaluator and bool(int(os.environ.get("BARYON_GAMEMODE", 0))):
            if which("gamemoderun") is not None:
                pre_command.insert(0, "gamemoderun")

        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 300


def get_module() -> BaryonModule:
    return Gamemode()
