"""Tests for launcher.grpc_launcher module."""

from unittest.mock import MagicMock, patch

from sapdl.launcher import GrpcLauncher


class TestGrpcLauncher:
    """Test cases for GrpcLauncher class."""

    def test_init_sets_ansys_path(self):
        """Test __init__ sets ansys_path from find_mapdl."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch("sapdl.launcher.grpc_launcher.GrpcLauncher._init"):
                launcher = GrpcLauncher()
                assert launcher.ansys_path == "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"

    def test_init_uses_default_workdir(self):
        """Test __init__ uses MAPDL_INITIAL_WORKDIR as default."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "_init") as mock_init:
                GrpcLauncher()
                mock_init.assert_called_once_with(None, "file")

    def test_init_accepts_custom_workdir(self):
        """Test __init__ accepts custom workdir."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "_init") as mock_init:
                GrpcLauncher(workdir="D:\\WORK")
                mock_init.assert_called_once_with("D:\\WORK", "file")

    def test_init_accepts_custom_jobname(self):
        """Test __init__ accepts custom jobname."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "_init") as mock_init:
                GrpcLauncher(jobname="myname")
                mock_init.assert_called_once_with(None, "myname")

    def test_init_calls_connect(self):
        """Test __init__ calls connect."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "connect") as mock_connect:
                launcher = GrpcLauncher()
                mock_connect.assert_called_once()

    def test_init_creates_workdir(self):
        """Test _init creates workdir if not exists."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch("os.makedirs") as mock_makedirs:
                with patch.object(GrpcLauncher, "connect"):
                    launcher = GrpcLauncher(workdir="D:\\TEST")
                    mock_makedirs.assert_called_once_with("D:\\TEST", exist_ok=True)

    def test_run_calls_input_strings(self):
        """Test run calls mapdl.input_strings."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "connect"):
                launcher = GrpcLauncher()
                launcher.mapdl = MagicMock()
                launcher.mapdl.input_strings.return_value = "result"

                result = launcher.run("TEST COMMAND")
                launcher.mapdl.input_strings.assert_called_once_with("TEST COMMAND")
                assert result == "result"

    def test_run_file_calls_run_with_input_command(self):
        """Test run_file calls run with /INPUT command."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "connect"):
                launcher = GrpcLauncher()
                launcher.mapdl = MagicMock()
                launcher.run_file("test.apdl")
                launcher.mapdl.input_strings.assert_called_once_with("/INPUT,'test.apdl'")

    def test_run_str_calls_run(self):
        """Test run_str calls run with the string."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "connect"):
                launcher = GrpcLauncher()
                launcher.mapdl = MagicMock()
                launcher.run_str("TEST")
                launcher.mapdl.input_strings.assert_called_once_with("TEST")

    def test_run_passes_command_as_str(self):
        """Test run converts command to string."""
        with patch("sapdl.launcher.grpc_launcher.find_mapdl") as mock_find:
            mock_find.return_value = "C:\\ANSYS\\bin\\winx64\\MAPDL.exe"
            with patch.object(GrpcLauncher, "connect"):
                launcher = GrpcLauncher()
                launcher.mapdl = MagicMock()
                launcher.mapdl.input_strings.return_value = None

                launcher.run(123)
                launcher.mapdl.input_strings.assert_called_once_with("123")
