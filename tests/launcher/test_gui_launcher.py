"""Tests for launcher.gui_launcher module."""

from unittest.mock import patch

import pytest

from sapdl.launcher import GUILauncher


class TestFindAnsysWindows:
    """Test cases for find_ansys_windows utility."""

    def test_returns_empty_dict_when_no_windows(self):
        """Test empty dict when no windows found."""
        from sapdl.launcher.utils import find_ansys_windows

        with patch("win32gui.EnumWindows") as mock_enum:
            mock_enum.return_value = None

            def side_effect(cb, _):
                # No windows enumerated
                pass

            mock_enum.side_effect = side_effect
            result = find_ansys_windows()
            assert result == {}


class TestGUILauncher:
    """Test cases for GUILauncher class."""

    def test_init_without_connect_skips_connection(self):
        """Test __init__ with connect=False does not call connect."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                launcher = GUILauncher(connect=False)
                assert launcher.ansys_path == "C:\\ANSYS\\bin\\launcher.exe"

    def test_init_raises_when_not_running_and_not_connecting(self):
        """Test __init__ raises Exception when ANSYS not running and connect=False."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(
                GUILauncher, "check_ansys_is_running", return_value=False
            ):
                with pytest.raises(Exception, match="ANSYS is not running"):
                    GUILauncher(connect=False)

    def test_send_input_returns_false_when_no_main_window(self):
        """Test _send_input returns False when hwnd_main is None."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                launcher = GUILauncher(connect=False)
                launcher.hwnd_main = None
                result = launcher._send_input("test.apdl")
                assert result is False

    def test_waiting_returns_true_immediately_when_file_exists(self, tmp_path):
        """Test waiting returns True if file already exists."""
        test_file = tmp_path / "result.txt"
        test_file.touch()

        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                launcher = GUILauncher(connect=False)
                result = launcher.waiting(str(test_file), timeout=1.0)
                assert result is True

    def test_waiting_returns_false_on_timeout(self, tmp_path):
        """Test waiting returns False after timeout."""
        resfile = tmp_path / "nonexistent.txt"

        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                launcher = GUILauncher(connect=False)
                result = launcher.waiting(str(resfile), timeout=0.1, interval=0.05)
                assert result is False

    def test_run_raises_exception_on_failure(self):
        """Test run raises Exception when waiting fails."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                with patch(
                    "sapdl.launcher.gui_launcher.write_with_stamp"
                ) as mock_stamp:
                    mock_stamp.return_value = ("path.apdl", "result.txt")
                    with patch.object(GUILauncher, "_send_input", return_value=True):
                        with patch.object(GUILauncher, "waiting", return_value=False):
                            launcher = GUILauncher(connect=False)
                            with pytest.raises(Exception, match="Running failed"):
                                launcher.run("TEST COMMAND")

    def test_run_file_calls_run_with_input_command(self):
        """Test run_file calls run with /INPUT command."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                with patch.object(GUILauncher, "run") as mock_run:
                    launcher = GUILauncher(connect=False)
                    launcher.run_file("test.apdl")
                    mock_run.assert_called_once_with("/INPUT,'test.apdl'")

    def test_run_str_calls_run(self):
        """Test run_str calls run with the string."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch.object(GUILauncher, "check_ansys_is_running", return_value=True):
                with patch.object(GUILauncher, "run") as mock_run:
                    launcher = GUILauncher(connect=False)
                    launcher.run_str("TEST")
                    mock_run.assert_called_once_with("TEST")


class TestCheckAnsysIsRunning:
    """Test cases for check_ansys_is_running method."""

    def test_returns_false_when_no_windows(self):
        """Test returns False when no ANSYS windows found."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            with patch(
                "sapdl.launcher.gui_launcher.find_ansys_windows", return_value={}
            ):
                with patch("win32gui.GetForegroundWindow", return_value=0):
                    with patch.object(GUILauncher, "connect"):
                        launcher = GUILauncher(connect=True)
                    result = launcher.check_ansys_is_running()
                    assert result is False

    def test_returns_true_when_both_windows_found(self):
        """Test returns True when main and input windows are found."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            windows = {
                100: "ANSYS MECHANICAL",
                200: "MECHANICAL APDL",
            }
            with patch(
                "sapdl.launcher.gui_launcher.find_ansys_windows", return_value=windows
            ):
                with patch("win32gui.GetForegroundWindow", return_value=0):
                    launcher = GUILauncher(connect=False)
                    result = launcher.check_ansys_is_running()
                    assert result is True
                    assert launcher.hwnd_main == 100
                    assert 200 in launcher.hwnd_input

    def test_ignores_distributed_in_input_window(self):
        """Test DISTRIBUTED in title is ignored for input window."""
        with patch("sapdl.launcher.gui_launcher.find_mechanical_apdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\launcher.exe"
            windows = {
                100: "ANSYS MECHANICAL",
                200: "MECHANICAL APDL - DISTRIBUTED",
            }
            with patch(
                "sapdl.launcher.gui_launcher.find_ansys_windows", return_value=windows
            ):
                with patch("win32gui.GetForegroundWindow", return_value=0):
                    with patch.object(GUILauncher, "connect"):
                        launcher = GUILauncher(connect=True)
                    result = launcher.check_ansys_is_running()
                    # Should have main but no input (DISTRIBUTED excluded)
                    assert result is False
                    assert launcher.hwnd_main == 100
                    assert 200 not in launcher.hwnd_input


class TestLauncherBaseClass:
    """Test cases for Launcher abstract base class."""

    def test_run_file_raises_not_implemented(self):
        """Test run_file raises NotImplementedError."""
        from sapdl.launcher.launcher import Launcher

        launcher = Launcher()
        with pytest.raises(NotImplementedError):
            launcher.run_file("test.apdl")

    def test_run_str_raises_not_implemented(self):
        """Test run_str raises NotImplementedError."""
        from sapdl.launcher.launcher import Launcher

        launcher = Launcher()
        with pytest.raises(NotImplementedError):
            launcher.run_str("TEST")
