# 用户配置

## 说明

configs/目录是可选的，用于高级用户自定义skill行为。

**普通用户无需配置**，上传Excel就能用。

## 目录结构

```
configs/
├── frameworks/           # 用户的提示词框架（可选）
│   └── example.md        # 示例框架
└── custom-rules/         # 用户的特殊规则（可选）
    └── example.yaml      # 示例规则
```

## 配置类型

### 1. 框架文件（frameworks/）

自定义分析流程框架。

**用途**：当你有自己的分析框架时，可以上传覆盖默认行为。

**文件格式**：Markdown或文本文件

**示例**：
```markdown
# 我的分析框架

## P阶段：需求拆解
- 确定核心问题
- 定义KPI

## D阶段：数据执行
- 加载数据
- 计算KPI
- 生成图表
...
```

### 2. 特殊规则（custom-rules/）

自定义KPI公式、阈值等。

**用途**：当AI推断的KPI不准确时，可以提供自定义规则。

**文件格式**：YAML或JSON

**示例**：
```yaml
# 我的KPI规则
kpis:
  - name: 赔付率
    formula: "(已决+未决+费用-追偿)/保费"
    description: 赔付比例
  
  - name: 费用率
    formula: "费用/保费"
    description: 费用比例

# 我的阈值规则
thresholds:
  - metric: 赔付率
    warning: 70
    critical: 85
```

## 使用方式

用户上传Excel时，可以同时提供配置文件：
- 指定使用哪个框架
- 指定KPI公式
- 指定特殊规则

如不提供，skill使用默认行为（AI自动推断）。

## 配置优先级

```
用户配置 > AI推断 > 默认行为
```

- 用户提供了配置 → 使用用户配置
- 用户未提供配置 → AI自动推断
- AI推断失败 → 使用默认行为
