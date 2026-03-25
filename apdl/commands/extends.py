

class Extends:

    def clear(self, start:bool=True, **kwargs):
        """Clear the database.

        APDL Command: ``/CLEAR``

        Resets the ANSYS database to the conditions at the beginning
        of the problem.  Sets the import and Boolean options back to
        the ANSYS default. All items are deleted from the database and
        memory values are set to zero for items derived from database
        information.  All files are left intact.  This command is
        useful between multiple analyses in the same run, or between
        passes of a multi-pass analysis (such as between the
        substructure generation, use, and expansion passes).  Should
        not be used in a do-loop since loop counters will be reset.
        on the same line as the ``/CLEAR`` command.

        ``/CLEAR`` resets the jobname to match the currently open
        session .LOG and .ERR files. This will return the jobname to
        its original value, or to the most recent value specified on
        ``/FILNAME`` with KEY = 1.

        This command is valid only at the Begin level.

        Examples
        --------
        >>> mapdl.clear()
        """
        command = f"/CLEAR,{'START' if start else 'NOSTART'}"
        return self.run(command, **kwargs)