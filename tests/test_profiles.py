import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("configure_permissions", ROOT / "scripts/configure_permissions.py")
configuration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(configuration)


class ProfileTests(unittest.TestCase):
    def test_readonly_has_no_execution_or_writes(self):
        rules = configuration.load_profile("readonly")
        self.assertEqual(rules["defaultMode"], "dontAsk")
        self.assertEqual(set(rules["allow"]), {"Read", "Grep", "Glob"})
        for tool in ("Bash", "Edit", "Write", "NotebookEdit"):
            self.assertIn(tool, rules["deny"])

    def test_development_profiles_require_risky_git_approval(self):
        for name in ("localdev", "fulldev"):
            rules = configuration.load_profile(name)
            self.assertEqual(rules["defaultMode"], "default")
            for command in ("push", "reset", "clean", "branch", "checkout", "rebase", "config", "remote"):
                self.assertIn("Bash(git {} *)".format(command), rules["ask"])
            forbidden = {"Bash", "Bash(*)", "Bash(git *)", "Bash(git:*)", "Bash(python *)",
                         "Bash(python3 *)", "Bash(bash *)", "Bash(sh *)", "Bash(docker *)", "Bash(ssh *)"}
            self.assertFalse(forbidden.intersection(rules["allow"]))
            self.assertIn("Edit(./**)", rules["allow"])

    def test_localdev_does_not_auto_allow_remote_git(self):
        rules = configuration.load_profile("localdev")
        for command in ("push", "pull", "fetch"):
            self.assertIn("Bash(git {} *)".format(command), rules["ask"])
            self.assertNotIn("Bash(git {} *)".format(command), rules["allow"])

    def test_apply_replaces_unsafe_permissions_preserving_other_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / ".claude"
            folder.mkdir()
            path = folder / "settings.json"
            settings = {"permissions": {"allow": ["Bash"], "defaultMode": "bypassPermissions",
                                        "additionalDirectories": ["/"]},
                        "enabledPlugins": {"example": True}, "env": {"EXAMPLE": "placeholder"}}
            path.write_text(json.dumps(settings), encoding="utf-8")
            configuration.configure("readonly", temporary, apply=True)
            actual = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(actual["permissions"], configuration.load_profile("readonly"))
            self.assertEqual(actual["enabledPlugins"], settings["enabledPlugins"])
            self.assertEqual(actual["env"], settings["env"])
            first = path.read_bytes()
            configuration.configure("readonly", temporary, apply=True)
            self.assertEqual(path.read_bytes(), first)

    def test_preview_does_not_create_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.assertFalse(configuration.configure("localdev", temporary)["applied"])
            self.assertFalse((Path(temporary) / ".claude").exists())

    def test_invalid_json_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / ".claude"
            folder.mkdir()
            path = folder / "settings.json"
            path.write_text("invalid", encoding="utf-8")
            with self.assertRaises(ValueError):
                configuration.configure("readonly", temporary, apply=True)
            self.assertEqual(path.read_text(), "invalid")

    def test_non_object_and_unknown_profile_are_rejected(self):
        with self.assertRaises(ValueError):
            configuration.load_profile("bypassPermissions")
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / ".claude"
            folder.mkdir()
            (folder / "settings.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                configuration.configure("readonly", temporary, apply=True)

    def test_file_in_place_of_settings_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            (Path(temporary) / ".claude").write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                configuration.configure("readonly", temporary, apply=True)

    def test_symlink_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / ".claude"
            folder.mkdir()
            other = Path(temporary) / "other.json"
            other.write_text("{}", encoding="utf-8")
            try:
                (folder / "settings.json").symlink_to(other)
            except OSError:
                self.skipTest("Host does not permit symlinks")
            with self.assertRaises(ValueError):
                configuration.configure("readonly", temporary, apply=True)
            self.assertEqual(other.read_text(), "{}")

    def test_windows_reparse_attribute_is_rejected(self):
        path = mock.Mock()
        path.lstat.return_value = type("WindowsStat", (), {"st_mode": 0o040755, "st_file_attributes": 0x400})()
        self.assertTrue(configuration.redirected(path))


if __name__ == "__main__":
    unittest.main()
