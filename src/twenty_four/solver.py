"""24点游戏求解算法模块。

使用递归归约法求解给定4个数字是否能通过四则运算得到24。
采用Fraction避免浮点精度问题。
支持结合律等价去重和括号简化。
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from typing import TYPE_CHECKING

from .exceptions import InvalidOperatorError

if TYPE_CHECKING:
    from collections.abc import Sequence

TARGET = Fraction(24)
OPERATORS = ("+", "-", "*", "/")

# 运算符优先级
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


@dataclass(slots=True)
class Expression:
    """表达式节点，支持构建表达式树。

    Attributes:
        value: 数值。
        op: 运算符，基本数字为 None。
        operands: 操作数列表。原子节点存储原始整数，复合节点存储子表达式。
    """

    value: Fraction
    op: str | None
    operands: tuple[Expression | int, ...]

    def __hash__(self) -> int:
        return hash((self.op, self.operands))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expression):
            return NotImplemented
        return self.op == other.op and self.operands == other.operands

    def is_atom(self) -> bool:
        """是否为基本数字。"""
        return self.op is None

    def to_display(self, parent_op: str | None = None, is_right: bool = False) -> str:
        """生成显示形式，根据上下文简化括号。

        Args:
            parent_op: 父节点的运算符
            is_right: 是否为父节点的右操作数
        """
        if self.is_atom():
            return str(self.operands[0])

        # 获取当前运算符优先级（此时 self.op 必不为 None，因为 is_atom() 为 False）
        assert self.op is not None  # noqa: S101
        my_prec = PRECEDENCE.get(self.op, 0)
        parent_prec = PRECEDENCE.get(parent_op, 0) if parent_op else 0

        # 生成子表达式
        # 此时 self.op 不为 None，所以 operands 中的元素都是 Expression
        operands_expr = [e for e in self.operands if isinstance(e, Expression)]
        if self.op in ("+", "*"):
            # 加法和乘法：收集所有操作数，用运算符连接
            parts = [e.to_display(self.op, is_right=False) for e in operands_expr]
            result = self.op.join(parts)
        else:
            # 减法和除法：二元运算
            left = operands_expr[0].to_display(self.op, is_right=False)
            right = operands_expr[1].to_display(self.op, is_right=True)
            result = f"{left}{self.op}{right}"

        # 判断是否需要括号
        need_paren = False
        if parent_op:
            if my_prec < parent_prec:
                # 低优先级嵌套在高优先级中，需要括号
                need_paren = True
            elif my_prec == parent_prec and parent_op in ("-", "/") and is_right:
                # 同优先级：减法和除法不满足结合律，右操作数需要括号
                need_paren = True

        return f"({result})" if need_paren else result

    def _remove_trivial_one(self) -> Expression:
        """移除冗余的 1 操作，返回简化后的表达式。

        冗余操作定义：
        - 1 * expr → expr
        - expr * 1 → expr
        - expr / 1 → expr
        """
        if self.is_atom():
            return self

        # 递归处理子表达式
        new_operands = tuple(
            e._remove_trivial_one() if isinstance(e, Expression) else e
            for e in self.operands
        )

        # 检查是否可以移除当前的 1 操作
        if self.op == "*" and len(new_operands) >= 2:
            # 对于乘法，检查是否有操作数为 1
            filtered: list[Expression] = []
            has_one = False
            for op in new_operands:
                if isinstance(op, Expression) and op.is_atom() and op.operands[0] == 1:
                    has_one = True
                elif isinstance(op, Expression):
                    filtered.append(op)

            if has_one and len(filtered) >= 1:
                # 如果移除 1 后只剩一个操作数，返回该操作数
                if len(filtered) == 1:
                    return filtered[0]
                # 否则重新构建表达式
                return Expression(
                    value=self.value,
                    op=self.op,
                    operands=tuple(filtered)
                )

        if self.op == "/" and len(new_operands) == 2:
            left, right = new_operands
            # expr / 1 → expr（只有除数是 1 才是冗余）
            if isinstance(right, Expression) and right.is_atom() and right.operands[0] == 1:
                return left

        # 无法简化，返回处理后的表达式
        return Expression(value=self.value, op=self.op, operands=new_operands)

    def _has_trivial_one(self) -> bool:
        """检查表达式是否包含冗余的 1 操作。"""
        if self.is_atom():
            return False

        # 检查当前操作
        if self.op == "*":
            for op in self.operands:
                if isinstance(op, Expression) and op.is_atom() and op.operands[0] == 1:
                    return True

        if self.op == "/" and len(self.operands) == 2:
            right = self.operands[1]
            if isinstance(right, Expression) and right.is_atom() and right.operands[0] == 1:
                return True

        # 递归检查子表达式
        return any(
            e._has_trivial_one() for e in self.operands if isinstance(e, Expression)
        )


@dataclass
class Solution:
    """24点解法。

    Attributes:
        expression: 简化后的表达式。
        has_trivial_one: 是否包含冗余的 1 操作。
    """

    expression: str
    has_trivial_one: bool

    def __str__(self) -> str:
        if self.has_trivial_one:
            return f"{self.expression} (1 可参与计算)"
        return self.expression


def _make_canonical(op: str, a: Expression, b: Expression) -> Expression:
    """创建规范化表达式，处理结合律等价。"""
    if op in ("+", "*"):
        # 收集所有连续同运算的操作数
        operands: list[Expression] = []
        for expr in (a, b):
            if expr.op == op:
                # 该表达式也是同运算，展开其操作数（此时操作数必为 Expression）
                operands.extend(e for e in expr.operands if isinstance(e, Expression))
            else:
                operands.append(expr)
        # 按显示形式排序（确保等价表达式产生相同顺序）
        operands.sort(key=lambda e: e.to_display())
        return Expression(
            value=_compute_value(op, a, b), op=op, operands=tuple(operands)
        )
    else:
        # 减法和除法不满足交换律/结合律
        return Expression(value=_compute_value(op, a, b), op=op, operands=(a, b))


def _compute_value(op: str, a: Expression, b: Expression) -> Fraction:
    """计算运算结果。

    Args:
        op: 运算符。
        a: 左操作数。
        b: 右操作数。

    Returns:
        运算结果。

    Raises:
        InvalidOperatorError: 遇到未知运算符。
    """
    if op == "+":
        return a.value + b.value
    elif op == "-":
        return a.value - b.value
    elif op == "*":
        return a.value * b.value
    elif op == "/":
        return a.value / b.value
    raise InvalidOperatorError(op)


def _apply_operator(a: Expression, b: Expression, op: str) -> Expression | None:
    """应用运算符，返回新表达式。"""
    if op == "/" and b.value == 0:
        return None
    return _make_canonical(op, a, b)


def _solve_recursive(
    expressions: list[Expression],
    results: dict[str, Solution],
) -> None:
    """递归求解所有可能的表达式组合。"""
    if len(expressions) == 1:
        if expressions[0].value == TARGET:
            expr = expressions[0]
            core_expr = expr._remove_trivial_one()
            core_str = core_expr.to_display()
            has_trivial_one = expr._has_trivial_one()

            # 使用核心表达式去重
            if core_str not in results:
                results[core_str] = Solution(
                    expression=core_str,
                    has_trivial_one=has_trivial_one
                )
            elif has_trivial_one and not results[core_str].has_trivial_one:
                # 优先保留有冗余 1 的标记（因为可以提示用户）
                results[core_str] = Solution(
                    expression=core_str,
                    has_trivial_one=True
                )
        return

    # 从当前表达式中任选两个进行运算
    for i in range(len(expressions)):
        for j in range(len(expressions)):
            if i == j:
                continue

            a, b = expressions[i], expressions[j]
            remaining = [
                expressions[k] for k in range(len(expressions)) if k != i and k != j
            ]

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
    """
    if len(numbers) != 4:
        return []

    results: dict[str, Solution] = {}

    # 穷举所有数字排列
    for perm in permutations(numbers):
        # 将数字转换为 Expression 对象
        expressions = [
            Expression(value=Fraction(n), op=None, operands=(n,)) for n in perm
        ]
        _solve_recursive(expressions, results)

    return sorted(str(sol) for sol in results.values())


def has_solution(numbers: Sequence[int]) -> bool:
    """检查给定数字是否有解。"""
    return len(solve_24(numbers)) > 0
