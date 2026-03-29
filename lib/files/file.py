# SPDX-License-Identifier: MIT
#
# SAPDL - APDL File Wrapper
# Mimics Python's open() file interface using APDL *CFOPEN/*VWRITE/*VREAD/*CFCLOS

import re
from typing import List, Optional, Union
from sapdl.core.ast import BlockNode, CommandNode


class Format:
    """APDL format specification helper.

    Converts Python-style format specifications into Fortran format strings
    required by APDL ``*VWRITE`` commands.

    Fortran format codes supported:

    ========== ===============================================
    Code       Description
    ========== ===============================================
    ``F``      Real number with fixed decimal (e.g. F10.4)
    ``I``      Integer (e.g. I5)
    ``A``      Character/alphanumeric (e.g. A8)
    ``E``      Real in scientific notation (e.g. E12.5)
    ``D``      Double precision scientific (e.g. D12.5)
    ``G``      General format (auto-selects F/E)
    ========== ===============================================

    Examples
    --------
    Named constructors for each Fortran type::

        Format.f(10, 4)    # '(F10.4)'  - real, 10 wide, 4 decimals
        Format.i(5)        # '(I5)'     - integer, 5 wide
        Format.s(8)        # '(A8)'     - string, 8 characters
        Format.e(12, 5)    # '(E12.5)'  - scientific, 12 wide, 5 decimals
        Format.g(12, 5)    # '(G12.5)'  - general

    Repeat count for multiple values per line::

        Format.f(10, 4, n=2)   # '(2F10.4)' - two floats per line
        Format.i(5, n=3)       # '(3I5)'    - three integers per line

    Python format spec shortcut ``Format.of()``::

        Format.of('10.4f')   # '(F10.4)'
        Format.of('5i')      # '(I5)'
        Format.of('8s')      # '(A8)'
        Format.of('12.5e')   # '(E12.5)'
        Format.of('10.4')    # '(F10.4)'  - f is default for numeric
        Format.of('3f10.4') # '(3F10.4)' - with repeat count

    ``Format`` is string-like, so it can be assigned directly to ``File.format``::

        f.format = Format.f(10, 4)   # works
        f.format = Format.of('10.4') # works
        f.format = '(F10.4)'        # still works (plain str)

    ``str()`` or ``()`` returns the Fortran format string::

        fmt = Format.f(10, 4)
        str(fmt)   # '(F10.4)'
        fmt()      # '(F10.4)'
    """

    # (python char -> fortran code, default width, default prec)
    _PY_FMT_MAP = {
        "f": ("F", 10, 4),
        "i": ("I", 5, 0),
        "e": ("E", 12, 5),
        "g": ("G", 12, 5),
        "s": ("A", 8, 0),
        "d": ("I", 5, 0),
    }

    def __init__(
        self,
        code: str,
        width: int = 10,
        prec: int = 4,
        n: int = 1,
    ):
        """Construct a Format.

        Parameters
        ----------
        code : str
            Fortran format code: ``F``, ``I``, ``A``, ``E``, ``D``, or ``G``.
        width : int
            Total field width. Default is 10.
        prec : int
            Number of decimal places (F/E/D/G) or characters (A). Default is 4.
        n : int
            Repeat count — number of values per output line.
            For example, ``Format.f(10, 4, n=2)`` produces ``(2F10.4)``.
            Default is 1.
        """
        self._code = code.upper()
        self._width = width
        self._prec = prec
        self._n = n

    @classmethod
    def f(cls, width: int = 10, prec: int = 4, n: int = 1) -> "Format":
        """Real number with fixed decimal (Fortran F format)."""
        return cls("F", width, prec, n)

    @classmethod
    def i(cls, width: int = 5, n: int = 1) -> "Format":
        """Integer (Fortran I format)."""
        return cls("I", width, 0, n)

    @classmethod
    def s(cls, width: int = 8) -> "Format":
        """Character/alphanumeric string (Fortran A format)."""
        return cls("A", width, 0, 1)

    @classmethod
    def e(cls, width: int = 12, prec: int = 5, n: int = 1) -> "Format":
        """Real in scientific notation (Fortran E format)."""
        return cls("E", width, prec, n)

    @classmethod
    def d(cls, width: int = 12, prec: int = 5, n: int = 1) -> "Format":
        """Double precision scientific notation (Fortran D format)."""
        return cls("D", width, prec, n)

    @classmethod
    def g(cls, width: int = 12, prec: int = 5, n: int = 1) -> "Format":
        """General format (Fortran G format), auto-selects F or E."""
        return cls("G", width, prec, n)

    @classmethod
    def of(cls, spec: str) -> "Format":
        """Parse a Python-style format specification into a Format.

        Supports: ``'[n][width[.prec]][fmt]'``

        The format letter is optional — if omitted, ``f`` is assumed for
        numeric specs and ``s`` for character specs.

        Examples::

            '10'      -> '(F10.4)'  float, defaults prec
            '10.4'   -> '(F10.4)'  float, width 10, prec 4
            '10.4f'  -> '(F10.4)'  float
            '5i'     -> '(I5)'     integer
            '12.5e'  -> '(E12.5)'  scientific
            '8s'     -> '(A8)'     string
            '3f10.4' -> '(3F10.4)' with repeat count
        """
        spec = spec.strip()
        if not spec:
            return cls("F", 10, 4, 1)

        # Extract optional leading repeat count: "3F10.4" -> n=3, rest="F10.4"
        repeat_match = re.match(r"^(\d+)([a-zA-Z])", spec)
        if repeat_match:
            n = int(repeat_match.group(1))
            rest = repeat_match.group(2) + spec[repeat_match.end() :]
        else:
            n = 1
            rest = spec

        # Extract trailing fmt letter
        fmt_code = None
        for i, ch in enumerate(reversed(rest)):
            if ch.isalpha():
                fmt_code = ch.lower()
                rest = rest[: len(rest) - i - 1]
                break

        # Parse width and precision from what remains
        width, prec = 10, 4
        if "." in rest:
            w_part, p_part = rest.split(".", 1)
            if w_part:
                width = int(w_part)
            if p_part:
                prec = int(p_part)
        elif rest:
            width = int(rest)

        # Map Python fmt code to Fortran
        if fmt_code is None:
            fmt_code = "f" if prec > 0 or width > 5 else "i"

        fortran_code, default_w, default_p = cls._PY_FMT_MAP.get(fmt_code, ("F", 10, 4))

        # Use class defaults when user only specified the fmt letter
        if width == default_w and prec == default_p and fmt_code is not None:
            width = default_w
            prec = default_p

        return cls(fortran_code, width, prec, n)

    def __str__(self) -> str:
        """Fortran format string, e.g. ``'(F10.4)'``."""
        if self._n == 1:
            if self._code in ("I", "A"):
                return f"({self._code}{self._width})"
            return f"({self._code}{self._width}.{self._prec})"
        if self._code in ("I", "A"):
            return f"({self._n}{self._code}{self._width})"
        return f"({self._n}{self._code}{self._width}.{self._prec})"

    def __call__(self) -> str:
        """Shorthand for ``str(self)``."""
        return str(self)


class File:
    """APDL file-like object.

    Provides a Pythonic file interface backed by APDL's ``*CFOPEN``,
    ``*VWRITE``, and ``*CFCLOS`` commands.

    The format specification is sent as a separate line immediately after
    ``*VWRITE``, as required by APDL.

    Examples
    --------
    Write values with explicit format::

        with cmd.file('output.txt') as f:
            f.format = Format.f(10, 4)
            f.write(3.14159)
            f.write(2.71828)

    Write values with Python-style format shortcut::

        with cmd.file('output.txt') as f:
            f.format = Format.of('10.4f')
            f.write(3.14159, 2.71828)   # one line, two values
            f.write(1.41421)             # next line

    Read array from file::

        with cmd.file('data.txt') as f:
            f.format = Format.of('2F6.0')   # 2 values per line
            f.vread('A')                   # reads into APDL array A

    Parameters
    ----------
    run : callable
        A callable that accepts an APDL command string and executes it
        (typically ``Commands.run``).
    fname : str
        File name (may include path, up to 248 characters).
    ext : str, optional
        File extension (up to 8 characters). Default is ''.
    mode : str, optional
        File mode. Only ``'w'`` (write) is supported for now.
        Default is ``'w'``.
    append : bool, optional
        If True, append to existing file instead of overwriting.
        Default is False.
    """

    def __init__(
        self,
        fname: str,
        ext: str = "",
        mode: str = "w",
        append: bool = False,
        mac=None,
    ):
        self._fname = fname
        self._ext = ext
        self._mode = mode
        self._append = append
        self._closed = False
        self._format: Optional[str] = None
        self.mac = mac

    @property
    def format(self) -> Optional[str]:
        """Format specification for ``*VWRITE`` or ``*VREAD``.

        Accepts a plain Fortran format string (e.g. ``'(F10.4)'``) or a
        ``Format`` object, which is automatically converted via ``str()``.
        """
        return self._format

    @format.setter
    def format(self, value: Union[str, Format]) -> None:
        self._format = str(value) if isinstance(value, Format) else value

    @property
    def closed(self) -> bool:
        """True after ``close()`` has been called."""
        return self._closed

    def open(self) -> "File":
        """Opens the file with ``*CFOPEN``.

        Returns
        -------
        File
            self

        Raises
        ------
        ValueError
            If the file is already open or mode is not supported.
        """
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if self._mode != "w":
            raise ValueError(
                f"Unsupported mode: '{self._mode}' (only 'w' is supported)"
            )
        loc = "APPEND" if self._append else ""

        self.mac.body.add(CommandNode(f"*CFOPEN,{self._fname},{self._ext},,{loc}"))
        return self

    def close(self) -> None:
        """Closes the file with ``*CFCLOS``."""
        if not self._closed:
            self._run("*CFCLOS,")
            self._closed = True

    def write(self, *values: Union[str, float, int]) -> None:
        """Writes values to the file using ``*VWRITE``.

        The format must be set beforehand via the ``format`` property::

            f.format = Format.f(10, 4)
            f.write(3.14)

        Parameters
        ----------
        *values : str, float, or int
            Values to write. Up to 19 values per call.

        Raises
        ------
        ValueError
            If format is not set, file is closed, or mode is not write.
        """
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if self._mode != "w":
            raise ValueError(f"File not open for writing (mode='{self._mode}')")
        if not self._format:
            raise ValueError("format must be set before writing")
        vals = ",".join(str(v) for v in values) if values else ""
        self._run(f"*VWRITE,{vals}")
        self._run(self._format)

    def writelines(self, lines: List[str]) -> None:
        """Writes each string in ``lines`` as a separate line.

        The format must be set beforehand. Each string is written with a
        single ``*VWRITE`` call.

        Parameters
        ----------
        lines : list of str
            Strings to write, one per line.

        Raises
        ------
        ValueError
            If format is not set or file is not open for writing.
        """
        for line in lines:
            self.write(line)

    def __enter__(self) -> "File":
        """Enters the context, opens the file."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exits the context, closes the file."""
        self.close()
