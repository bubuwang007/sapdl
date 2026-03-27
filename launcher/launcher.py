class Launcher:
    """Abstract base class for ANSYS launchers."""

    def run_file(self, filename: str):
        """Run an APDL script file."""
        raise NotImplementedError

    def run_str(self, string: str):
        """Run an APDL command string."""
        raise NotImplementedError
