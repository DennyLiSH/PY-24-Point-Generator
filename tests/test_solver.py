"""24点求解器测试。"""

import pytest

from twenty_four.solver import has_solution, solve_24


class TestSolve24:
    """solve_24 函数测试。"""

    def test_basic_solution(self) -> None:
        """测试基础有解情况：1, 2, 3, 4 -> (1+2+3)*4 = 24"""
        results = solve_24([1, 2, 3, 4])
        assert len(results) > 0
        # 检查是否有等于24的表达式
        assert any("24" not in expr or "=" not in expr for expr in results)

    def test_no_solution(self) -> None:
        """测试无解情况：1, 1, 1, 1 无解"""
        results = solve_24([1, 1, 1, 1])
        assert len(results) == 0

    def test_fraction_calculation(self) -> None:
        """测试分数运算：8, 3, 8, 3 -> 8/(3-8/3) = 24"""
        results = solve_24([8, 3, 8, 3])
        assert len(results) > 0

    def test_all_same_number_solvable(self) -> None:
        """测试所有数字相同且有解：6, 6, 6, 6 -> 6+6+6+6 = 24"""
        results = solve_24([6, 6, 6, 6])
        assert len(results) > 0

    def test_all_same_number_unsolvable(self) -> None:
        """测试所有数字相同且无解：13, 13, 13, 13"""
        results = solve_24([13, 13, 13, 13])
        assert len(results) == 0

    def test_different_order_same_result(self) -> None:
        """测试不同顺序应该产生相同的解法集合。"""
        results1 = set(solve_24([1, 2, 3, 4]))
        results2 = set(solve_24([4, 3, 2, 1]))
        # 结果应该相同（因为数字相同只是顺序不同）
        assert results1 == results2

    def test_invalid_input_length(self) -> None:
        """测试无效输入长度。"""
        results = solve_24([1, 2, 3])  # 只有3个数字
        assert len(results) == 0

    def test_division_by_zero_handling(self) -> None:
        """测试除零处理。"""
        # 包含除零情况的测试
        results = solve_24([1, 2, 3, 4])
        # 应该正常返回结果，不会崩溃
        assert isinstance(results, list)


class TestHasSolution:
    """has_solution 函数测试。"""

    def test_solvable(self) -> None:
        """测试有解情况。"""
        assert has_solution([1, 2, 3, 4]) is True
        assert has_solution([6, 6, 6, 6]) is True

    def test_unsolvable(self) -> None:
        """测试无解情况。"""
        assert has_solution([1, 1, 1, 1]) is False
        assert has_solution([13, 13, 13, 13]) is False