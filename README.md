# Data Analysis Insight

通用数据分析洞察框架 - 用户上传Excel，AI自动识别场景、推断指标、生成看板。

## 核心特性

### 三种输出模式

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| **PDCA** | 简单分析 | 基础PDC+A流程，适合单表或简单多表 |
| **PDCAWFR** | 深度分析 | 完整PDC+WFR+A流程，适合复杂场景 |
| **Tool** | 离线工具 | 交互式HTML工具，支持上传Excel实时分析 |

### WFR智能判断

AI根据数据特征自动决定是否执行WFR：
- **F（Forecast）**：有≥2期数据 + 有时间维度 → 执行
- **R（Root Cause）**：C阶段有异常 / 维度≥2 → 执行（输出5-8条根因）
- **W（What-if）**：C阶段有异常 + 维度≥3 → 执行（交互滑块）

### 8类离线规则（Tool模式）

| 标签 | 方法 | 公式 |
|------|------|------|
| A. 极值 | 找最高/最低的维度 | max/min(groupBy(field).指标) |
| B. 集中度 | 帕累托分析 | top1 / total |
| C. 趋势 | 时间维度环比 | (cur - prev) / prev |
| D. 异常 | 超过阈值项 | 指标 > threshold |
| E. 关联 | 多维交叉 | groupBy([d1, d2]) |
| F. 偏离 | 实际/目标偏离度 | actual/target - 1 |
| G. 对比 | 同维度差异 | max ÷ min |
| H. 行动建议 | 基于洞察的下一步 | 诊断 + 优先级 |

## 安装

### 前置条件

- Python 3.x
- pandas
- openpyxl

### 安装步骤

```bash
# 安装Python依赖
pip install pandas openpyxl

# 将skill目录复制到OpenCode skills目录
cp -r data-analysis-insight ~/.agents/skills/
```

## 使用方法

### 1. 上传Excel分析

在OpenCode中直接上传Excel文件，AI会自动：

1. **识别数据场景**：分析字段特征、数据结构、行业特征
2. **推断KPI指标**：根据场景自动推断应该计算哪些KPI
3. **选择图表类型**：根据数据特征自动选择最佳图表
4. **执行分析流程**：根据场景复杂度选择PDCA/PDCAWFR/Tool
5. **生成HTML报告**：输出完整的交互式HTML看板

### 2. 示例对话

```
用户：上传[文件名].xlsx，帮我分析一下
AI：[自动执行数据分析，生成HTML报告]
```

```
用户：上传[文件名].xlsx，生成看板工具
AI：[生成Tool模式的交互式HTML工具]
```

## 目录结构

```
data-analysis-insight/
├── SKILL.md                          # 主文件
├── LICENSE                           # MIT License
├── modules/                          # 核心模块
│   ├── scene-recognizer.md           # 场景识别
│   ├── metric-inferencer.md          # 指标推断
│   ├── chart-selector.md             # 图表选型
│   ├── flow-orchestrator.md          # 流程编排
│   ├── html-builder.md               # HTML组装
│   └── data-storytelling.md          # 数据故事结构
├── scripts/                          # 工具脚本
│   └── parse_excel.py                # Python pandas Excel解析
├── configs/                          # 用户配置（可选）
│   └── README.md
├── references/                       # 参考文档
│   ├── README.md
│   ├── reference-materials.md        # 参考材料
│   └── case-studies.md               # 成功案例库
└── docs/                             # 使用文档
    ├── USAGE.md                      # 使用说明
    ├── troubleshooting.md            # 故障排除
    └── success-criteria.md           # 成功标准
```

## 技术栈

- **ECharts CDN**：图表渲染
- **SheetJS CDN**：Excel解析
- **Python pandas**：数据解析（固定工具）
- **纯JavaScript**：业务逻辑

## 设计原则

1. **通用性**：不限定具体行业，支持多种数据结构
2. **智能化**：AI自动识别场景、推断指标、选择图表
3. **可扩展**：支持用户自定义配置和特殊图表
4. **健壮性**：完善的错误处理和降级显示

## 贡献

欢迎贡献代码、报告问题或提出建议。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
