"""String - APDL 字符串函数封装

导出 APDL 内置字符串函数。
"""

from sapdl.core.ast import StringFuncNode


class String:
    """APDL 字符串函数封装

    提供常用的 APDL 字符串函数，返回 StringFuncNode。
    """

    # ==================== 数值转换 ====================

    @staticmethod
    def valchr(a8) -> StringFuncNode:
        """将字符串转换为双精度数值 VALCHR

        将表示十进制数值的字符串转换为双精度数值。

        Args:
            a8: 表示十进制数值的字符串

        Returns:
            StringFuncNode: VALCHR(STR)
        """
        return StringFuncNode("VALCHR", a8)

    @staticmethod
    def valoct(a8) -> StringFuncNode:
        """将八进制字符串转换为双精度数值 VALOCT

        将表示八进制数值的字符串转换为双精度数值。

        Args:
            a8: 表示八进制数值的字符串

        Returns:
            StringFuncNode: VALOCT(STR)
        """
        return StringFuncNode("VALOCT", a8)

    @staticmethod
    def valhex(a8) -> StringFuncNode:
        """将十六进制字符串转换为双精度数值 VALHEX

        将表示十六进制数值的字符串转换为双精度数值。

        Args:
            a8: 表示十六进制数值的字符串

        Returns:
            StringFuncNode: VALHEX(STR)
        """
        return StringFuncNode("VALHEX", a8)

    @staticmethod
    def chrval(dp) -> StringFuncNode:
        """将双精度数值转换为字符串 CHRVAL

        Args:
            dp: 双精度数值

        Returns:
            StringFuncNode: CHRVAL(DP)
        """
        return StringFuncNode("CHRVAL", dp)

    @staticmethod
    def chroct(dp) -> StringFuncNode:
        """将整数转换为八进制字符串 CHROCT

        Args:
            dp: 整数数值

        Returns:
            StringFuncNode: CHROCT(DP)
        """
        return StringFuncNode("CHROCT", dp)

    @staticmethod
    def chrhex(dp) -> StringFuncNode:
        """将整数转换为十六进制字符串 CHRHEX

        Args:
            dp: 整数数值

        Returns:
            StringFuncNode: CHRHEX(DP)
        """
        return StringFuncNode("CHRHEX", dp)

    # ==================== 字符串操作 ====================

    @staticmethod
    def strlen(string) -> StringFuncNode:
        """返回字符串长度 STRLENG

        Args:
            string: 字符串参数

        Returns:
            StringFuncNode: STRLENG(STR)
        """
        return StringFuncNode("STRLENG", string)

    @staticmethod
    def strsub(str1, nloc, nchar) -> StringFuncNode:
        """提取子串 STRSUB

        从字符串 str1 中从 nloc 位置开始提取 nchar 个字符。
        nloc 为 1-based 索引。

        Args:
            str1: 原字符串
            nloc: 起始位置（1-based）
            nchar: 提取字符数

        Returns:
            StringFuncNode: STRSUB(STR1, NLOC, NCHAR)
        """
        return StringFuncNode("STRSUB", str1, nloc, nchar)

    @staticmethod
    def strcat(str1, str2) -> StringFuncNode:
        """字符串连接 STRCAT

        将 str2 追加到 str1 末尾生成新字符串。

        Args:
            str1: 第一个字符串
            str2: 第二个字符串

        Returns:
            StringFuncNode: STRCAT(STR1, STR2)
        """
        return StringFuncNode("STRCAT", str1, str2)

    @staticmethod
    def strfill(str1, str2, nloc) -> StringFuncNode:
        """在指定位置插入字符串 STRFILL

        将 str2 插入到 str1 的 nloc 位置。

        Args:
            str1: 原字符串
            str2: 要插入的字符串
            nloc: 插入位置（1-based）

        Returns:
            StringFuncNode: STRFILL(STR1, STR2, NLOC)
        """
        return StringFuncNode("STRFILL", str1, str2, nloc)

    @staticmethod
    def strcomp(str1) -> StringFuncNode:
        """移除字符串中所有空格 STRCOMP

        Args:
            str1: 原字符串

        Returns:
            StringFuncNode: STRCOMP(STR1)
        """
        return StringFuncNode("STRCOMP", str1)

    @staticmethod
    def strleft(str1) -> StringFuncNode:
        """左对齐字符串 STRLEFT

        去除字符串尾部空格。

        Args:
            str1: 原字符串

        Returns:
            StringFuncNode: STRLEFT(STR1)
        """
        return StringFuncNode("STRLEFT", str1)

    @staticmethod
    def strpos(str1, str2) -> StringFuncNode:
        """返回子串位置 STRPOS

        返回 str2 在 str1 中首次出现的起始位置（1-based），
        未找到则返回 0。

        Args:
            str1: 被搜索的字符串
            str2: 要搜索的子串

        Returns:
            StringFuncNode: STRPOS(STR1, STR2)
        """
        return StringFuncNode("STRPOS", str1, str2)

    @staticmethod
    def upcase(str1) -> StringFuncNode:
        """字符串转大写 UPCASE

        Args:
            str1: 原字符串

        Returns:
            StringFuncNode: UPCASE(STR1)
        """
        return StringFuncNode("UPCASE", str1)

    @staticmethod
    def lwcase(str1) -> StringFuncNode:
        """字符串转小写 LWCASE

        Args:
            str1: 原字符串

        Returns:
            StringFuncNode: LWCASE(STR1)
        """
        return StringFuncNode("LWCASE", str1)

    # ==================== 文件名操作 ====================

    @staticmethod
    def join(directory, filename, extension=None) -> StringFuncNode:
        """连接目录和文件名生成路径字符串 JOIN

        Args:
            directory: 目录路径
            filename: 文件名
            extension: 文件扩展名（可选，有扩展名时用 dir/filename.ext）

        Returns:
            StringFuncNode: JOIN('directory', 'filename', 'extension')
        """
        if extension is None:
            return StringFuncNode("JOIN", directory, filename)
        return StringFuncNode("JOIN", directory, filename, extension)

    @staticmethod
    def split(pathstring, option) -> StringFuncNode:
        """从路径字符串中提取指定部分 SPLIT

        Args:
            pathstring: 路径字符串
            option: 提取选项
                - 'DIR': 提取目录部分
                - 'FILE': 提取完整文件名（含扩展名）
                - 'NAME': 提取文件名（不含扩展名）
                - 'EXT': 提取文件扩展名

        Returns:
            StringFuncNode: SPLIT('PathString', 'OPTION')
        """
        return StringFuncNode("SPLIT", pathstring, option)
