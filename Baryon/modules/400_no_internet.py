import os
import stat
from pathlib import Path
from shutil import which

from modules import BaryonModule
from modules import ModuleReturn



class NoInternet(BaryonModule):
    """
    Runs a command by a group that has blocked Internet access

    required:
    1. Create new group:
        `groupadd GROUPNAME`
    2. Add user to group:
        `usermod -a -G GROUPNAME USERNAME`
    3. Add iptables rule for dropping network activity for group:
        `iptables -N LOG_AND_DROP
        `iptables -A LOG_AND_DROP -j LOG --log-prefix "Source host denied "
        `iptables -A LOG_AND_DROP -j DROP
        `iptables -A OUTPUT ! -o lo -m owner --gid-owner GROUPNAME -j LOG_AND_DROP`

        Note: Don't forget to make the changes permanent, so it would be applied automatically after reboot.
        ARCH: `sudo iptables-save -f /etc/iptables/iptables.rules`
    """
    @staticmethod
    def create_executable(groupname) -> str:
        executable = r"""#!/bin/python
import subprocess
import sys

if __name__ == "__main__":
    command = ""
    for arg in sys.argv[1:]:
        command += " " + arg.replace(" ", "\\ ")
    subprocess.run(f"sg {GROUPNAME} -c '{command.strip()}'", shell=True)
"""
        executable = executable.replace("{GROUPNAME}", groupname)
        baryon_cache = Path('~/.cache/baryon/').expanduser()
        baryon_cache.mkdir(parents=True, exist_ok=True)

        no_internet_file = baryon_cache / "no-internet"

        with open(no_internet_file, mode="w") as fp:
            fp.write(executable)
        st = os.stat(no_internet_file)
        os.chmod(no_internet_file, st.st_mode | stat.S_IEXEC)

        return str(no_internet_file)

    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, is_scriptevaluator=False,
                   **kwargs) -> ModuleReturn:

        if not is_scriptevaluator and bool(int(os.environ.get("BARYON_NO_INTERNET", 0))):
            __no_internet_group = os.environ.get("BARYON_NO_INTERNET_GROUP", "no-internet")
            if which("sg") is not None:
                no_internet_file = NoInternet.create_executable(__no_internet_group)

                pre_command.append(no_internet_file)
        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 400


def get_module() -> BaryonModule:
    return NoInternet()
