---
name: agentic-eval
description: |
  评估和改进AI代理输出的模式与技术。在以下情况下使用此技能：
  - 实现自我批评和反思循环
  - 构建对生成质量至关重要的评估-优化流水线
  - 创建测试驱动的代码优化工作流
  - 设计基于评分标准或LLM作为裁判的评估系统
  - 为代理输出（代码、报告、分析）添加迭代改进
  - 测量和提升代理响应质量
---

# 代理评估模式

通过迭代评估和优化实现自我提升的模式。

## 概述

评估模式使代理能够评估和改进自身的输出，超越单次生成，进入迭代优化循环。

```
生成 → 评估 → 批判 → 优化 → 输出
    ↑                              │
    └──────────────────────────────┘
```

## 使用场景

- **对质量要求高的生成任务**：需要高准确性的代码、报告、分析
- **有明确评估标准的任务**：存在定义明确的成功度量标准
- **需要特定标准的内容**：如风格指南、合规性、格式要求

---

## 模式1：基础反思

代理通过自我批评来评估和改进自身的输出。

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    """带反思循环的生成过程"""
    output = llm(f"完成此任务:\n{task}")
    
    for i in range(max_iterations):
        # 自我批评
        critique = llm(f"""
        根据以下标准评估此输出：{criteria}
        输出内容：{output}
        请以JSON格式对每个标准进行评分：通过/失败，并附反馈。
        """)
        
        critique_data = json.loads(critique)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output
        
        # 根据批评结果优化
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"根据以下问题进行改进：{failed}\n原始输出：{output}")
    
    return output
```

**关键洞察**：使用结构化的JSON输出以便可靠解析批评结果。

---

## 模式2：评估-优化分离

将生成和评估拆分为独立组件，以明确职责划分。

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold
    
    def generate(self, task: str) -> str:
        return llm(f"完成任务：{task}")
    
    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"""
        评估任务：{task} 的输出
        输出内容：{output}
        返回JSON：{{"整体评分": 0-1, "维度": {{"准确性": ..., "清晰度": ...}}}}
        """))
    
    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"根据反馈进行改进：{feedback}\n输出内容：{output}")
    
    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            if evaluation["整体评分"] >= self.score_threshold:
                break
            output = self.optimize(output, evaluation)
        return output
```

---

## 模式3：代码特定反思

用于代码生成的测试驱动优化循环。

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"为以下需求编写Python代码：{spec}")
        tests = llm(f"为以下需求生成pytest测试用例：{spec}\n代码：{code}")
        
        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["成功"]:
                return code
            code = llm(f"修复错误：{result['错误信息']}\n代码：{code}")
        return code
```

---

## 评估策略

### 基于结果的评估
评估输出是否达到预期结果。

```python
def evaluate_outcome(task: str, output: str, expected: str) -> str:
    return llm(f"输出是否达到预期结果？任务：{task}，预期：{expected}，输出：{output}")
```

### LLM作为裁判
使用LLM对输出进行比较和排序。

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> str:
    return llm(f"根据{criteria}比较输出A和B。哪个更好？为什么？")
```

### 基于评分标准的评估
对输出进行加权维度评分。

```python
RUBRIC = {
    "准确性": {"权重": 0.4},
    "清晰度": {"权重": 0.3},
    "完整性": {"权重": 0.3}
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    scores = json.loads(llm(f"对以下维度进行1-5分评分：{list(rubric.keys())}\n输出内容：{output}"))
    return sum(scores[d] * rubric[d]["权重"] for d in rubric) / 5
```

---

## 最佳实践

| 实践 | 理由 |
|------|-----|
| **明确的评估标准** | 提前定义具体、可衡量的评估标准 |
| **设置迭代上限** | 设置最大迭代次数（3-5次）以防止无限循环 |
| **收敛性检查** | 如果输出评分在迭代间未改善则停止 |
| **记录历史轨迹** | 保留完整过程用于调试和分析 |
| **结构化输出** | 使用JSON以便可靠解析评估结果 |

---

## 快速入门检查清单

```markdown
## 评估实现检查清单

### 设置
- [ ] 定义评估标准/评分表
- [ ] 设置"足够好"的评分阈值
- [ ] 配置最大迭代次数（默认：3次）

### 实现
- [ ] 实现generate()函数
- [ ] 实现带有结构化输出的evaluate()函数
- [ ] 实现optimize()函数
- [ ] 搭建优化循环

### 安全性
- [ ] 添加收敛性检测
- [ ] 记录所有迭代过程用于调试
- [ ] 异常解析失败时优雅处理
```
