"""Math - APDL 数学函数封装

导出 APDL 内置数学函数。
"""

from sapdl.core.ast import FunctionCallNode


class Math:
    """APDL 数学函数封装

    提供常用的 APDL 数学函数，返回 FunctionCallNode。
    """

    PI = 3.141592653589793
    E = 2.718281828459045

    @staticmethod
    def abs(expr) -> FunctionCallNode:
        """绝对值 ABS"""
        return FunctionCallNode("ABS", expr)

    @staticmethod
    def cxabs(x, y) -> FunctionCallNode:
        """复数绝对值 CXABS"""
        return FunctionCallNode("CXABS", x, y)

    @staticmethod
    def sign(value, sign_value) -> FunctionCallNode:
        """符号函数 SIGN"""
        return FunctionCallNode("SIGN", value, sign_value)

    @staticmethod
    def exp(expr) -> FunctionCallNode:
        """指数函数 EXP"""
        return FunctionCallNode("EXP", expr)

    @staticmethod
    def log(expr) -> FunctionCallNode:
        """自然对数 LOG"""
        return FunctionCallNode("LOG", expr)

    @staticmethod
    def log10(expr) -> FunctionCallNode:
        """常用对数 LOG10"""
        return FunctionCallNode("LOG10", expr)

    @staticmethod
    def sqrt(expr) -> FunctionCallNode:
        """平方根 SQRT"""
        return FunctionCallNode("SQRT", expr)

    @staticmethod
    def round(expr) -> FunctionCallNode:
        """四舍五入 NINT"""
        return FunctionCallNode("NINT", expr)

    @staticmethod
    def floor(expr) -> FunctionCallNode:
        """向下取整"""
        return FunctionCallNode("FLOOR", expr)

    @staticmethod
    def ceil(expr) -> FunctionCallNode:
        """向上取整"""
        return FunctionCallNode("CEIL", expr)

    @staticmethod
    def mod(a, b) -> FunctionCallNode:
        """取模 MOD"""
        return FunctionCallNode("MOD", a, b)

    @staticmethod
    def rand(start, end) -> FunctionCallNode:
        """均匀分布随机数 RAND"""
        return FunctionCallNode("RAND", start, end)

    @staticmethod
    def gdis(mean, std) -> FunctionCallNode:
        """高斯分布随机数 GDIS"""
        return FunctionCallNode("GDIS", mean, std)

    @staticmethod
    def sin(angle) -> FunctionCallNode:
        """正弦 SIN"""
        return FunctionCallNode("SIN", angle)

    @staticmethod
    def cos(angle) -> FunctionCallNode:
        """余弦 COS"""
        return FunctionCallNode("COS", angle)

    @staticmethod
    def tan(angle) -> FunctionCallNode:
        """正切 TAN"""
        return FunctionCallNode("TAN", angle)

    @staticmethod
    def asin(value) -> FunctionCallNode:
        """反正弦 ASIN"""
        return FunctionCallNode("ASIN", value)

    @staticmethod
    def acos(value) -> FunctionCallNode:
        """反余弦 ACOS"""
        return FunctionCallNode("ACOS", value)

    @staticmethod
    def atan(value) -> FunctionCallNode:
        """反正切 ATAN"""
        return FunctionCallNode("ATAN", value)

    @staticmethod
    def atan2(y, x) -> FunctionCallNode:
        """二参数反正切 ATAN2"""
        return FunctionCallNode("ATAN2", y, x)

    @staticmethod
    def sinh(value) -> FunctionCallNode:
        """双曲正弦 SINH"""
        return FunctionCallNode("SINH", value)

    @staticmethod
    def cosh(value) -> FunctionCallNode:
        """双曲余弦 COSH"""
        return FunctionCallNode("COSH", value)

    @staticmethod
    def tanh(value) -> FunctionCallNode:
        """双曲正切 TANH"""
        return FunctionCallNode("TANH", value)

    @staticmethod
    def large_int(x, y) -> FunctionCallNode:
        """大整数 LARGEINT"""
        return FunctionCallNode("LARGEINT", x, y)
