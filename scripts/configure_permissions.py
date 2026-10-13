"""Preview or apply a checked-in profile to project settings. Python 3.8+."""
import argparse
import json
import os
from pathlib import Path
import stat
import tempfile

PROFILES = ("readonly", "localdev", "fulldev")


def redirected(path):
    """Reject symlinks and Windows junction/reparse destinations."""
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def load_profile(name):
    if name not in PROFILES:
        raise ValueError("Unknown profile: {}".format(name))
    root = Path(__file__).resolve().parents[1]
    with (root / "profiles" / (name + ".json")).open(encoding="utf-8") as stream:
        return json.load(stream)["permissions"]


def configure(name, project, apply=False):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be a directory")
    directory = project / ".claude"
    destination = directory / "settings.json"
    if redirected(directory):
        raise ValueError("Refusing a symlink/reparse settings destination")
    if directory.exists() and not directory.is_dir():
        raise ValueError(".claude is not a directory")
    if redirected(destination):
        raise ValueError("Refusing a symlink/reparse settings destination")
    original = destination.read_bytes() if destination.exists() else None
    settings = json.loads(original.decode("utf-8-sig")) if original is not None else {}
    if not isinstance(settings, dict):
        raise ValueError("Settings must contain a JSON object")
    profile = load_profile(name)
    settings["permissions"] = profile
    result = {"profile": name, "target": str(destination), "applied": bool(apply),
              "permissions": profile}
    if not apply:
        return result
    directory.mkdir(exist_ok=True)
    current = destination.read_bytes() if destination.exists() else None
    if current != original or redirected(directory) or redirected(destination):
        raise ValueError("Settings changed during configuration")
    serialized = (json.dumps(settings, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    fd, temporary = tempfile.mkstemp(prefix=".permissions-", suffix=".tmp", dir=str(directory))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(serialized)
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=PROFILES)
    parser.add_argument("--project", default=".")
    parser.add_argument("--apply", action="store_true", help="Write settings; otherwise preview only")
    args = parser.parse_args()
    try:
        result = configure(args.profile, args.project, args.apply)
    except (OSError, ValueError) as error:
        parser.exit(2, "Configuration refused: {}\n".format(error))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
