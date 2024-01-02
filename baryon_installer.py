#!/usr/bin/env python3

import argparse
import os
import shutil
import stat
from copy import deepcopy
from pathlib import Path

# acf patch required https://github.com/ValvePython/vdf/pull/55
import vdf

parser = argparse.ArgumentParser()
parser.add_argument("--steam-dir", "-s", default="~/.steam/root/", action="store")
parser.add_argument("--create_shortcut", default=False, action="store_true")
parser.add_argument("--reinstall", default=False, action="store_true")
args = parser.parse_args()


def get_appid():
    __baryon = b'baryon'
    return int("".join(str(letter % 32) for letter in __baryon))


APPID = get_appid()


def generate_toolmanifest():
    __manifest = {"manifest": {}}
    manifest = __manifest["manifest"]
    manifest["commandline"] = "/baryon --verb=%verb% --"
    manifest["version"] = "2"
    manifest["use_tool_subprocess_reaper"] = "1"
    manifest["unlisted"] = "1"
    manifest["compatmanager_layer_name"] = "baryon"
    return vdf.dumps(__manifest, pretty=True)


def generate_compatibilitytool():
    __compatibilitytool = {"compatibilitytools": {"compat_tools": {"baryon": {}}}}
    baryon = __compatibilitytool["compatibilitytools"]["compat_tools"]["baryon"]
    baryon["appid"] = str(APPID)
    baryon["install_path"] = "."
    baryon["display_name"] = "Baryon"
    baryon["from_oslist"] = "linux"
    baryon["to_oslist"] = "linux"
    return vdf.dumps(__compatibilitytool, pretty=True)


def generate_appmanifest(baryon_dir):
    __appmanifest = {"AppState": {}}
    appstate = __appmanifest["AppState"]
    appstate["appid"] = str(APPID)
    appstate["Universe"] = "1"
    appstate["name"] = "Baryon"
    appstate["StateFlags"] = "4"
    appstate["installdir"] = baryon_dir
    return vdf.dumps(__appmanifest, pretty=True, acf=True)


if __name__ == '__main__':
    if os.geteuid() < 1000:
        raise PermissionError("Don't run with system rights")

    __steam_dir = Path(args.steam_dir).expanduser().resolve().absolute()
    __steamapps_dir = __steam_dir / "steamapps"
    __userdata_dir = __steam_dir / "userdata"
    __baryon_dir = __steam_dir / "compatibilitytools.d" / "Baryon"

    for path in [__steam_dir, __steamapps_dir, __userdata_dir]:
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"{str(path)} directory does not found")

    if __baryon_dir.exists() and not args.reinstall:
        raise FileExistsError("Baryon already installed, use --reinstall argument")

    shutil.rmtree(__baryon_dir, ignore_errors=True)
    __baryon_dir.mkdir(parents=True)
    shutil.copytree(Path(os.path.abspath(__file__)).parent / "Baryon", __baryon_dir, dirs_exist_ok=True)
    baryon_exec = __baryon_dir / "baryon"
    baryon_exec.chmod(baryon_exec.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    with open(__baryon_dir / "toolmanifest.vdf", "w") as toolmanifest_vdf:
        toolmanifest_vdf.write(generate_toolmanifest())
    with open(__baryon_dir / "compatibilitytool.vdf", "w") as toolmanifest_vdf:
        toolmanifest_vdf.write(generate_compatibilitytool())
    with open(__baryon_dir / "baryon.appid", "w") as baryon_appid:
        baryon_appid.write(str(APPID))
    with open(__steamapps_dir / f"appmanifest_{str(APPID)}.acf", "w") as appmanifest_acf:
        appmanifest_acf.write(generate_appmanifest(str(__baryon_dir.resolve().absolute())))
