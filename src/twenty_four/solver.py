"""24点游戏求解算法模块。

使用递归归约法求解给定4个数字是否能通过四则运算得到24。
采用Fraction避免浮点精度问题。
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

TARGET = Fraction(24)
OPERATORS = ("+", "-", "*", "/")


@dataclass
class Expression:
    """表达式节点，支持构建表达式树。"""

    value: Fraction  # 数值
    repr: str  # 字符串表示（无括号）
    display: str  # 带括号的显示形式

    def __hash__(self) -> int:
        return hash((self.value, self.display))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expression):
            return NotImplemented
        return self.value == other.value and self.display == other.display


def _apply_operator(a: Expression, b: Expression, op: str) -> Expression | None:
    """应用运算符，返回新表达式。

    Args:
        a: 第一个操作数
        b: 第二个操作数
        op: 运算符 (+, -, *, /)

    Returns:
        新的表达式，如果运算无效（如除零）返回 None
    """
    if op == "+":
        return Expression(
            value=a.value + b.value,
            repr=f"{a.repr}+{b.repr}",
            display=f"({a.display}+{b.display})",
        )
    elif op == "-":
        return Expression(
            value=a.value - b.value,
            repr=f"{a.repr}-{b.repr}",
            display=f"({a.display}-{b.display})",
        )
    elif op == "*":
        return Expression(
            value=a.value * b.value,
            repr=f"{a.repr}*{b.repr}",
            display=f"({a.display}*{b.display})",
        )
    elif op == "/":
        if b.value == 0:
            return None
        return Expression(
            value=a.value / b.value,
            repr=f"{a.repr}/{b.repr}",
            display=f"({a.display}/{b.display})",
        )
    return None


def _solve_recursive(
    expressions: list[Expression],
    results: set[str],
) -> None:
    """递归求解所有可能的表达式组合。

    Args:
        expressions: 当前的表达式列表
        results: 存储结果的集合
    """
    if len(expressions) == 1:
        if expressions[0].value == TARGET:
            # 去掉最外层括号
            display = expressions[0].display
            if display.startswith("(") and display.endswith(")"):
                display = display[1:-1]
            results.add(display)
        return

    # 从当前表达式中任选两个进行运算
    for i in range(len(expressions)):
        for j in range(len(expressions)):
            if i == j:
                continue

            a, b = expressions[i], expressions[j]
            remaining = [expressions[k] for k in range(len(expressions)) if k != i and k != j]

            for op in OPERATORS:
                result = _apply_operator(a, b, op)
                if result is not None:
                    _solve_recursive(remaining + [result], results)


def solve_24(numbers: Sequence[int]) -> list[str]:
    """求解24点问题。

    给定4个数字，找出所有能通过四则运算得到24的表达式。

    Args:
        numbers: 4个整数（通常为1-13）

    Returns:
        所有可能的表达式列表，无解返回空列表

    Examples:
        >>> solve_24([1, 2, 3, 4])
        ['(1+2+3)*4', ...]
        >>> solve_24([1, 1, 1, 1])
        []
    """
    if len(numbers) != 4:
        return []

    results: set[str] = set()

    # 穷举所有数字排列
    for perm in permutations(numbers):
        # 将数字转换为Expression对象
        expressions = [
            Expression(value=Fraction(n), repr=str(n), display=str(n)) for n in perm
        ]
        _solve_recursive(expressions, results)

    return sorted(results)


def has_solution(numbers: Sequence[int]) -> bool:
    """检查给定数字是否有解。

    Args:
        numbers: 4个整数

    Returns:
        是否存在至少一个解
    """
    return len(solve_24(numbers)) > 0