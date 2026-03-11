"""24点游戏CLI交互模块。

提供命令行界面供用户交互式出题和查看答案。
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from .exceptions import ProblemGenerationError
from .generator import Problem, ProblemGenerator
from .solver import solve_24

if TYPE_CHECKING:
    from collections.abc import Sequence

VERSION = "1.0.0"


class TwentyFourCLI:
    """24点游戏CLI应用。"""

    def __init__(self) -> None:
        """初始化CLI应用。"""
        self.generator = ProblemGenerator()
        self.current_problem: Problem | None = None
        self.current_solutions: list[str] | None = None

    def run(self) -> None:
        """运行主循环。"""
        self._display_welcome()

        while True:
            self._display_menu()
            choice = self._get_input("请输入选项: ").strip().lower()

            if choice == "1":
                self._handle_new_problem()
            elif choice == "2":
                self._handle_show_answer()
            elif choice in ("q", "quit", "exit"):
                self._display_goodbye()
                break
            else:
                print("无效选项，请重新输入。")

    def _display_welcome(self) -> None:
        """显示欢迎信息。"""
        print("=" * 45)
        print("        24点游戏出题器 v" + VERSION)
        print("=" * 45)
        print()
        print("规则说明：")
        print("  给定4个数字（1-13），使用 +、-、*、/ 四则运算")
        print("  每个数字必须且只能使用一次，使结果等于24")
        print()

    def _display_menu(self) -> None:
        """显示菜单。"""
        print("-" * 45)
        print("              主菜单")
        print("-" * 45)
        print("  [1] 生成新题目")
        print("  [2] 显示答案")
        print("  [q] 退出程序")
        print("-" * 45)

        if self.current_problem:
            print(f"当前题目：{self.current_problem}")
            if self.current_solutions is not None:
                status = (
                    f"（有 {len(self.current_solutions)} 种解法）"
                    if self.current_solutions
                    else "（无解）"
                )
                print(f"状态：{status}")

        print()

    def _handle_new_problem(self) -> None:
        """处理生成新题目。"""
        try:
            self.current_problem = self.generator.generate(ensure_solvable=True)
            self.current_solutions = solve_24(self.current_problem.numbers)
            print(f"\n新题目：{self.current_problem}")
            print(f"此题目有解！（共 {len(self.current_solutions)} 种解法）")
        except ProblemGenerationError:
            # 如果无法生成有解题目，生成任意题目
            self.current_problem = self.generator.generate(ensure_solvable=False)
            self.current_solutions = solve_24(self.current_problem.numbers)
            print(f"\n新题目：{self.current_problem}")
            if self.current_solutions:
                print(f"此题目有解！（共 {len(self.current_solutions)} 种解法）")
            else:
                print("此题目无解！")
        print()

    def _handle_show_answer(self) -> None:
        """处理显示答案。"""
        if self.current_problem is None:
            print("\n请先生成题目！\n")
            return

        if self.current_solutions is None:
            self.current_solutions = solve_24(self.current_problem.numbers)

        print()
        if not self.current_solutions:
            print("此题目无解！")
        else:
            print(f"答案（共 {len(self.current_solutions)} 种解法）：")
            for i, solution in enumerate(self.current_solutions, 1):
                print(f"  {i}. {solution} = 24")
        print()

    def _display_goodbye(self) -> None:
        """显示告别信息。"""
        print("\n感谢使用！再见！\n")

    def _get_input(self, prompt: str) -> str:
        """获取用户输入。

        Args:
            prompt: 提示信息

        Returns:
            用户输入的字符串
        """
        try:
            return input(prompt)
        except EOFError, KeyboardInterrupt:
            print()  # 打印换行
            self._display_goodbye()
            sys.exit(0)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI入口函数。

    Args:
        argv: 命令行参数（未使用，保留用于未来扩展）

    Returns:
        退出码
    """
    cli = TwentyFourCLI()
    cli.run()
    return 0
