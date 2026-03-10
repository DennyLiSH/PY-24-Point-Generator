"""24点题目生成器模块。

提供随机生成24点题目的功能，支持保证有解模式。
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .solver import has_solution

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass(frozen=True)
class Problem:
    """24点题目。"""

    numbers: tuple[int, int, int, int]

    def __str__(self) -> str:
        return f"{self.numbers[0]} {self.numbers[1]} {self.numbers[2]} {self.numbers[3]}"

    @property
    def has_solution(self) -> bool:
        """检查题目是否有解。"""
        return has_solution(self.numbers)


class ProblemGenerator:
    """24点题目生成器。"""

    def __init__(
        self,
        min_num: int = 1,
        max_num: int = 13,
        seed: int | None = None,
    ) -> None:
        """初始化生成器。

        Args:
            min_num: 最小数字（默认1）
            max_num: 最大数字（默认13，即扑克牌K）
            seed: 随机种子，用于可重复生成
        """
        self.min_num = min_num
        self.max_num = max_num
        self._rng = random.Random(seed)

    def generate(self, ensure_solvable: bool = True, max_attempts: int = 1000) -> Problem:
        """生成一道题目。

        Args:
            ensure_solvable: 是否保证题目有解
            max_attempts: 最大尝试次数（仅当ensure_solvable为True时有效）

        Returns:
            生成的题目

        Raises:
            RuntimeError: 无法在指定次数内生成有解题目
        """
        if not ensure_solvable:
            return self._generate_random()

        for _ in range(max_attempts):
            problem = self._generate_random()
            if problem.has_solution:
                return problem

        msg = f"无法在 {max_attempts} 次尝试内生成有解题目"
        raise RuntimeError(msg)

    def _generate_random(self) -> Problem:
        """生成随机题目。"""
        numbers = tuple(
            self._rng.randint(self.min_num, self.max_num) for _ in range(4)
        )
        return Problem(numbers=numbers)

    def generate_batch(
        self,
        count: int,
        ensure_solvable: bool = True,
        max_attempts: int = 1000,
    ) -> list[Problem]:
        """批量生成题目。

        Args:
            count: 题目数量
            ensure_solvable: 是否保证题目有解
            max_attempts: 每道题最大尝试次数

        Returns:
            题目列表
        """
        return [
            self.generate(ensure_solvable=ensure_solvable, max_attempts=max_attempts)
            for _ in range(count)
        ]

    def generate_all_solvable(self) -> Iterator[Problem]:
        """生成所有有解的题目组合。

        Yields:
            所有可能的有解题目
        """
        for n1 in range(self.min_num, self.max_num + 1):
            for n2 in range(self.min_num, self.max_num + 1):
                for n3 in range(self.min_num, self.max_num + 1):
                    for n4 in range(self.min_num, self.max_num + 1):
                        problem = Problem(numbers=(n1, n2, n3, n4))
                        if problem.has_solution:
                            yield problem