# 项目改进建议

基于当前代码审查，以下是十个可以改进的地方：

## 1. `has_solution` 函数性能优化

**问题**：`has_solution` 调用 `solve_24` 并检查返回列表长度，但实际上只需要确认是否存在一个解即可。

**位置**：[solver.py:145-154](src/twenty_four/solver.py#L145-L154)

```python
# 当前实现
def has_solution(numbers: Sequence[int]) -> bool:
    return len(solve_24(numbers)) > 0

# 建议：添加提前终止的版本
def has_solution(numbers: Sequence[int]) -> bool:
    """检查是否有解，找到第一个解即返回，无需穷举所有解。"""
    # 实现一个在找到第一个解时就返回的版本
```

**影响**：性能提升约 50%-90%（取决于题目）。

---

## 2. CLI 缺少命令行参数支持

**问题**：`main` 函数有 `argv` 参数但未使用，无法通过命令行直接求解或查看版本。

**位置**：[cli.py:133-144](src/twenty_four/cli.py#L133-L144)

**建议添加**：
- `--version` / `-v`：显示版本号
- `--solve 1,2,3,4`：直接求解指定数字
- `--generate`：生成一道题目并退出

```python
# 示例
def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="24点游戏出题器")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--solve", type=str, help="求解指定数字，如 '1,2,3,4'")
    # ...
```

---

## 3. 缺少 CLI 交互测试

**问题**：测试文件仅覆盖 `solver` 和 `generator` 模块，缺少 `cli.py` 的测试。

**位置**：`tests/` 目录

**建议**：添加 `tests/test_cli.py`，测试：
- 菜单选项处理
- 输入验证
- 边界情况（如 EOF、KeyboardInterrupt）

---

## 4. 代码重复：题目状态打印逻辑

**问题**：`_handle_new_problem` 中有重复的题目状态打印逻辑。

**位置**：[cli.py:76-92](src/twenty_four/cli.py#L76-L92)

```python
# 当前：重复的打印逻辑
print(f"\n新题目：{self.current_problem}")
print(f"此题目有解！（共 {len(self.current_solutions)} 种解法）")
# ... 和
print(f"\n新题目：{self.current_problem}")
if self.current_solutions:
    print(f"此题目有解！（共 {len(self.current_solutions)} 种解法）")
```

**建议**：提取为 `_display_problem_status()` 方法。

---

## 5. 缺少配置文件支持

**问题**：数字范围等配置硬编码在代码中，用户无法自定义。

**建议**：
- 添加 `pyproject.toml` 中的 `[tool.twenty-four]` 配置节
- 或支持 `.twentyfourrc` 配置文件
- 可配置项：数字范围、默认题目数量、界面语言等

---

## 6. 预计算解的存在性缓存

**问题**：每次调用 `has_solution` 都会重新计算，对于常见数字组合可以缓存结果。

**位置**：[solver.py](src/twenty_four/solver.py)

**建议**：
```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def has_solution_cached(numbers: tuple[int, int, int, int]) -> bool:
    # 预计算或缓存结果
```

**影响**：重复调用时性能提升显著。

---

## 7. 缺少 CI/CD 配置

**问题**：项目没有 GitHub Actions 或其他 CI 配置。

**建议**：添加 `.github/workflows/ci.yml`：
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --all-extras
      - run: uv run pytest
      - run: uv run mypy src
      - run: uv run ruff check src tests
```

---

## 8. 缺少文档字符串示例验证

**问题**：`solver.py` 中的 docstring 包含示例但未启用 doctest。

**位置**：[solver.py:123-127](src/twenty_four/solver.py#L123-L127)

```python
    Examples:
        >>> solve_24([1, 2, 3, 4])
        ['(1+2+3)*4', ...]  # 这个示例不精确
```

**建议**：
- 启用 doctest 或
- 使用 pytest 的 doctest 插件
- 或将示例改为更精确的形式

---

## 9. `generate_all_solvable` 性能问题

**问题**：该方法遍历所有可能的组合（如 1-13 范围有 13^4 = 28,561 种），且每次都调用 `has_solution`。

**位置**：[generator.py:105-117](src/twenty_four/generator.py#L105-L117)

**建议**：
- 添加进度回调参数
- 或预计算并序列化结果
- 或使用多进程加速

---

## 10. 缺少国际化（i18n）支持

**问题**：所有 UI 文本硬编码为中文，无法切换语言。

**位置**：[cli.py](src/twenty_four/cli.py)

**建议**：
```python
# 使用 gettext 或简单的字典映射
MESSAGES = {
    "zh": {"welcome": "24点游戏出题器", ...},
    "en": {"welcome": "24-Point Game", ...},
}
```

---

## 优先级建议

| 优先级 | 改进项 | 理由 |
|--------|--------|------|
| 高 | #1 性能优化 | 直接影响用户体验 |
| 高 | #7 CI/CD | 保证代码质量 |
| 中 | #2 命令行参数 | 提升易用性 |
| 中 | #3 CLI 测试 | 提高测试覆盖率 |
| 中 | #6 缓存 | 性能优化 |
| 低 | #4 代码重复 | 代码质量 |
| 低 | #5 配置文件 | 可扩展性 |
| 低 | #8 doctest | 文档质量 |
| 低 | #9 性能问题 | 边缘场景 |
| 低 | #10 国际化 | 可扩展性 |