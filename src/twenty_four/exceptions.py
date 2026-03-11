"""自定义异常模块。

提供24点游戏专用的异常层次结构。
"""


class TwentyFourError(Exception):
    """24点游戏基础异常。

    所有24点游戏相关异常的基类。
    """


class ProblemGenerationError(TwentyFourError):
    """题目生成失败。

    当无法在指定尝试次数内生成有解题目时抛出。

    Attributes:
        max_attempts: 最大尝试次数。
    """

    def __init__(self, max_attempts: int) -> None:
        self.max_attempts = max_attempts
        super().__init__(f"无法在 {max_attempts} 次尝试内生成有解题目")


class SolverError(TwentyFourError):
    """求解器错误。

    求解过程中出现的错误基类。
    """


class InvalidOperatorError(SolverError):
    """无效运算符。

    当遇到不支持的运算符时抛出。

    Attributes:
        op: 无效的运算符。
    """

    def __init__(self, op: str) -> None:
        self.op = op
        super().__init__(f"未知运算符: {op}")
