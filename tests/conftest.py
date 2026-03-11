"""pytest 共享 fixtures。"""

import pytest


@pytest.fixture
def sample_solvable_numbers() -> tuple[int, int, int, int]:
    """返回一个有解的测试数字组合。"""
    return (1, 2, 3, 4)


@pytest.fixture
def sample_unsolvable_numbers() -> tuple[int, int, int, int]:
    """返回一个无解的测试数字组合。"""
    return (1, 1, 1, 1)
