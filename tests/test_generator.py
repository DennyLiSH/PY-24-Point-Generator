"""24点题目生成器测试。"""

import pytest

from twenty_four.generator import Problem, ProblemGenerator


class TestProblem:
    """Problem 类测试。"""

    def test_str_representation(self) -> None:
        """测试字符串表示。"""
        problem = Problem(numbers=(1, 2, 3, 4))
        assert str(problem) == "1 2 3 4"

    def test_has_solution_true(self) -> None:
        """测试有解题目。"""
        problem = Problem(numbers=(1, 2, 3, 4))
        assert problem.has_solution is True

    def test_has_solution_false(self) -> None:
        """测试无解题目。"""
        problem = Problem(numbers=(1, 1, 1, 1))
        assert problem.has_solution is False

    def test_frozen(self) -> None:
        """测试不可变。"""
        problem = Problem(numbers=(1, 2, 3, 4))
        with pytest.raises(AttributeError):
            problem.numbers = (5, 6, 7, 8)  # type: ignore[misc]


class TestProblemGenerator:
    """ProblemGenerator 类测试。"""

    def test_generate_solvable(self) -> None:
        """测试生成有解题目。"""
        generator = ProblemGenerator(seed=42)
        problem = generator.generate(ensure_solvable=True)
        assert problem.has_solution is True

    def test_generate_unsolvable_allowed(self) -> None:
        """测试允许生成无解题目。"""
        generator = ProblemGenerator(seed=1)
        # 使用特定种子，可能生成无解题目
        problem = generator.generate(ensure_solvable=False)
        # 只检查能正常生成
        assert len(problem.numbers) == 4

    def test_generate_with_seed_reproducible(self) -> None:
        """测试使用种子可重复生成。"""
        gen1 = ProblemGenerator(seed=42)
        gen2 = ProblemGenerator(seed=42)

        problem1 = gen1.generate(ensure_solvable=False)
        problem2 = gen2.generate(ensure_solvable=False)

        assert problem1.numbers == problem2.numbers

    def test_generate_batch(self) -> None:
        """测试批量生成。"""
        generator = ProblemGenerator(seed=42)
        problems = generator.generate_batch(5, ensure_solvable=True)

        assert len(problems) == 5
        for problem in problems:
            assert problem.has_solution is True

    def test_custom_range(self) -> None:
        """测试自定义数字范围。"""
        generator = ProblemGenerator(min_num=5, max_num=10, seed=42)
        problem = generator.generate(ensure_solvable=False)

        for num in problem.numbers:
            assert 5 <= num <= 10

    def test_generate_all_solvable(self) -> None:
        """测试生成所有有解题目。"""
        generator = ProblemGenerator(min_num=1, max_num=3)
        # 生成所有组合，检查是否都有解
        all_solvable = list(generator.generate_all_solvable())
        for problem in all_solvable:
            assert problem.has_solution is True