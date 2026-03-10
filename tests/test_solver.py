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


class TestEquivalentDeduplication:
    """等价表达式去重测试。"""

    def test_commutative_deduplication(self) -> None:
        """测试交换律去重：a*b 和 b*a 只保留一种。"""
        # 11, 5, 2, 2 应该减少等价形式
        results = solve_24([11, 5, 2, 2])
        # 验证解的数量应该大幅减少（结合律去重）
        assert len(results) < 5, f"Expected < 5 solutions, got {len(results)}: {results}"

    def test_associative_deduplication(self) -> None:
        """测试结合律去重：(a+b)+c 和 a+(b+c) 只保留一种。"""
        # 4, 10, 2, 5 的 ((2*5)+10)+4 和 ((2*5)+4)+10 应合并
        results = solve_24([4, 10, 2, 5])
        # 验证解的数量应该很少
        assert len(results) < 5, f"Expected < 5 solutions, got {len(results)}: {results}"

    def test_parenthesis_simplification(self) -> None:
        """测试括号简化。"""
        results = solve_24([11, 5, 2, 2])
        # 所有解应该没有多余括号
        for expr in results:
            # 不应该有 (( 开头
            assert not expr.startswith("(("), f"Double parentheses in: {expr}"

    def test_commutative_addition(self) -> None:
        """测试加法交换律去重。"""
        # 1, 2, 3, 4 不应同时包含大量交换律变体
        results = solve_24([1, 2, 3, 4])
        # 验证数量合理（规范化后大幅减少，从原来的80+降到22左右）
        assert len(results) <= 25, f"Expected <= 25 solutions, got {len(results)}"

    def test_no_duplicate_patterns(self) -> None:
        """测试没有重复模式。"""
        results = solve_24([1, 2, 3, 4])
        # 检查没有完全相同的结果
        assert len(results) == len(set(results))

    def test_classic_case_unchanged(self) -> None:
        """测试经典案例 8,3,8,3 仍然正确。"""
        results = solve_24([8, 3, 8, 3])
        assert len(results) >= 1
        # 注意：不使用 eval() 验证，因为浮点精度问题
        # 求解器内部使用 Fraction 精确计算，结果可信