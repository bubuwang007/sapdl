"""Tests for launcher.utils module."""

import os
import re
from unittest.mock import patch

import pytest

from sapdl.launcher import utils


class TestFindAnsys:
    """Test cases for find_ansys function."""

    def test_no_ansys_installed(self):
        """Test when no ANSYS environment variables exist."""
        with patch.dict(os.environ, {}, clear=True):
            result = utils.find_ansys()
            assert result is None

    def test_single_ansys_version(self):
        """Test with single ANSYS version installed."""
        env = {"ANSYS191_DIR": "C:\\Program Files\\ANSYS\\v191"}
        with patch.dict(os.environ, env, clear=True):
            result = utils.find_ansys()
            assert result == "C:\\Program Files\\ANSYS\\v191"

    def test_multiple_ansys_versions_returns_latest(self):
        """Test with multiple ANSYS versions returns latest."""
        env = {
            "ANSYS191_DIR": "C:\\ANSYS\\v191",
            "ANSYS211_DIR": "C:\\ANSYS\\v211",
            "ANSYS195_DIR": "C:\\ANSYS\\v195",
        }
        with patch.dict(os.environ, env, clear=True):
            result = utils.find_ansys()
            assert result == "C:\\ANSYS\\v211"


class TestFindMechanicalApdl:
    """Test cases for find_mechanical_apdl function."""

    def test_ansys_path_from_config(self, tmp_path):
        """Test using ANSYS_PATH from config."""
        ansys_bin = tmp_path / "bin" / "winx64"
        ansys_bin.mkdir(parents=True)
        launcher = ansys_bin / "launcher.exe"
        launcher.touch()

        with patch.object(utils, "ANSYS_PATH", str(tmp_path)):
            result = utils.find_mechanical_apdl()
            assert result == str(launcher)

    def test_launcher_not_found(self, tmp_path):
        """Test FileNotFoundError when launcher.exe does not exist."""
        ansys_bin = tmp_path / "bin" / "winx64"
        ansys_bin.mkdir(parents=True)

        with patch.object(utils, "ANSYS_PATH", str(tmp_path)):
            with pytest.raises(FileNotFoundError, match="does not exist"):
                utils.find_mechanical_apdl()


class TestFindMapdl:
    """Test cases for find_mapdl function."""

    def test_ansys_path_from_config(self, tmp_path):
        """Test using ANSYS_PATH from config."""
        ansys_bin = tmp_path / "bin" / "winx64"
        ansys_bin.mkdir(parents=True)
        mapdl = ansys_bin / "MAPDL.exe"
        mapdl.touch()

        with patch.object(utils, "ANSYS_PATH", str(tmp_path)):
            result = utils.find_mapdl()
            assert result == str(mapdl)

    def test_mapdl_not_found(self, tmp_path):
        """Test FileNotFoundError when MAPDL.exe does not exist."""
        ansys_bin = tmp_path / "bin" / "winx64"
        ansys_bin.mkdir(parents=True)

        with patch.object(utils, "ANSYS_PATH", str(tmp_path)):
            with pytest.raises(FileNotFoundError, match="does not exist"):
                utils.find_mapdl()


class TestTempfilePath:
    """Test cases for tempfile_path function."""

    def test_returns_correct_path(self):
        """Test the path is correctly joined."""
        with patch.object(utils, "ANSYS_TEMPFILE_PATH", "C:\\temp"):
            result = utils.tempfile_path("test.txt")
            assert result == "C:\\temp\\test.txt"


class TestStamp:
    """Test cases for stamp function."""

    def test_returns_tuple_of_commands_and_path(self):
        """Test stamp returns APDL commands and result file path."""
        with patch.object(utils, "ANSYS_TEMPFILE_PATH", "C:\\temp"):
            cmds, resfile = utils.stamp()
            assert isinstance(cmds, str)
            assert isinstance(resfile, str)
            assert "_STAMP=" in cmds
            assert "*CFOPEN," in cmds
            assert "*CFCLOS" in cmds
            assert resfile.startswith("C:\\temp\\")

    def test_stamp_value_is_integer(self):
        """Test stamp value is a valid integer."""
        with patch.object(utils, "ANSYS_TEMPFILE_PATH", "C:\\temp"):
            cmds, _ = utils.stamp()
            match = re.search(r"_STAMP='(\d+)'", cmds)
            assert match is not None
            stamp_val = int(match.group(1))
            assert stamp_val > 0


class TestWriteTempfile:
    """Test cases for write_tempfile function."""

    def test_writes_content_to_file(self, tmp_path):
        """Test content is written to correct path."""
        with patch.object(utils, "ANSYS_TEMPFILE_PATH", str(tmp_path)):
            content = "test content"
            result = utils.write_tempfile("test.txt", content)

            assert result == str(tmp_path / "test.txt")
            with open(result) as f:
                assert f.read() == content


class TestWriteWithStamp:
    """Test cases for write_with_stamp function."""

    def test_writes_content_and_stamp(self, tmp_path):
        """Test content and stamp are written to file."""
        with patch.object(utils, "ANSYS_TEMPFILE_PATH", str(tmp_path)):
            content = "test content"
            filepath, resfile = utils.write_with_stamp("test.txt", content)

            assert filepath == str(tmp_path / "test.txt")
            assert resfile.startswith(str(tmp_path))

            with open(filepath) as f:
                file_content = f.read()
                assert content in file_content
                assert "_STAMP=" in file_content
