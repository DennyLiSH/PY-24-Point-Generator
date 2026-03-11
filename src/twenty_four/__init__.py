"""24点游戏出题器。

一个命令行工具，用于生成和求解24点数学游戏题目。
"""

from .exceptions import (
    InvalidOperatorError,
    ProblemGenerationError,
    SolverError,
    TwentyFourError,
)
from .generator import Problem, ProblemGenerator
from .solver import has_solution, solve_24

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "Problem",
    "ProblemGenerator",
    "solve_24",
    "has_solution",
    "TwentyFourError",
    "ProblemGenerationError",
    "SolverError",
    "InvalidOperatorError",
]
