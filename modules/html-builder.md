# HTML组装模块

## 职责

将分析结果组装成完整的HTML报告。

## 输出格式

单HTML文件（PC端为主），包含：
1. 报头（标题 + 数据概览）
2. **核心结论速览（3-5条，放在KPI之前）**
3. KPI卡片（6个，带趋势箭头）
4. 图表区（单维度 + 组合维度）
5. 洞察报告（8类通用方法，至少用5类，最终≥7条）
6. **根因诊断（R阶段，5-8条，独立区块）**
7. 趋势预测（F阶段）
8. **情景模拟（W阶段，交互滑块）**
9. 行动建议
10. 数据自检（放在页脚，只显示描述性信息）

## 字段识别与别名机制（写死）

**识别优先级**（从高到低）：
1. **精确匹配标准字段名**：如"销售额"、"渠道"、"地区"
2. **模糊匹配别名列表**：如"零售全产品总金额"→total，"渠道名称"→channel
3. **按字段内容推断**：数值+包含"金额/数量/率"→度量，文本+包含"类型/渠道/区域"→维度
4. **按位置兜底**：最后一列通常是度量，前三列通常是维度

**内置别名表**（不可修改）：

| 别名 | 标准字段名 | 说明 |
|------|-----------|------|
| 零售全产品总金额 / 总金额 / 总销售 / 销售总额 | total | 总销售额 |
| 属性 / 渠道 / 渠道名称 / 销售渠道 | channel | 渠道维度 |
| 办事处 / 分公司 / 区域 | office | 办事处维度 |
| 地区 / 区域名称 / 省份 | region | 地区维度 |
| 公司名称 / 公司 | company | 公司维度 |
| 店铺名称 / 店铺 / 门店 | store | 店铺维度 |
| 日期 / 时间 / 月份 / 年月 | date | 时间维度 |

**扩展规则**：
- 如果字段名不在别名表中，按"按字段内容推断"规则处理
- 如果推断失败，标记为"未识别字段"，跳过该字段
- 不修改别名表，保持skill的通用性

## 组装流程

```
1. 接收所有分析结果
   - 场景识别结果
   - 指标推断结果
   - 图表选型结果
   - 流程编排结果
   - 实际计算结果

2. 组装HTML结构
   - 头部（CSS样式）
   - 主体（各区块）
   - 尾部（JavaScript）

3. 填充数据
   - KPI数值
   - 图表配置
   - 表格数据
   - 洞察内容
   - 建议内容

4. 生成完整HTML
   - 压缩代码
   - 控制文件大小（≤500KB）

5. 输出文件
```

## HTML结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{报告标题}</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>
  <style>
    /* 样式定义 */
  </style>
</head>
<body>
  <div class="container">
    <!-- 报头 -->
    <header class="header">
      <h1>{标题}</h1>
      <p>{描述}</p>
    </header>
    
    <!-- 上传区 -->
    <section class="upload-area">
      <div class="upload-zone" id="uploadZone">
        <p>点击或拖拽上传Excel文件</p>
      </div>
    </section>
    
    <!-- 核心结论速览（3-5条，放在KPI之前） -->
    <section class="conclusion-section">
      <h3>核心结论速览</h3>
      <div id="conclusionList"></div>
    </section>
    
    <!-- KPI卡片 -->
    <section class="kpi-section" id="kpiSection">
      <!-- 动态生成 -->
    </section>
    
    <!-- 图表区：单维度 -->
    <section class="charts-section">
      <h3>单维度分析</h3>
      <div class="chart-card"><h3>渠道销售对比</h3><div class="chart-container" id="chart-channel"></div></div>
      <div class="chart-card"><h3>地区销售TOP10</h3><div class="chart-container" id="chart-region"></div></div>
      <div class="chart-card"><h3>产品销售TOP10</h3><div class="chart-container" id="chart-product"></div></div>
      <div class="chart-card"><h3>销售构成分析</h3><div class="chart-container" id="chart-compose"></div></div>
    </section>
    
    <!-- 图表区：组合维度 -->
    <section class="charts-section">
      <h3>组合维度分析</h3>
      <div class="chart-card"><h3>渠道×地区销售热力图</h3><div class="chart-container" id="chart-heatmap1"></div></div>
      <div class="chart-card"><h3>渠道×产品销售热力图</h3><div class="chart-container" id="chart-heatmap2"></div></div>
      <div class="chart-card"><h3>地区×产品销售热力图</h3><div class="chart-container" id="chart-heatmap3"></div></div>
      <div class="chart-card"><h3>渠道×地区×产品多维分析</h3><div class="chart-container" id="chart-multi"></div></div>
    </section>
    
    <!-- 数据表格 -->
    <section class="table-section">
      <table id="dataTable">
        <thead></thead>
        <tbody></tbody>
      </table>
    </section>
    
    <!-- 洞察报告（8类通用方法，至少用5类，最终≥7条） -->
    <section class="insights-section">
      <h3>深度洞察分析</h3>
      <div id="insightsList"></div>
    </section>
    
    <!-- 根因诊断（R阶段，5-8条，独立区块） -->
    <section class="rootcause-section">
      <h3>根因诊断（5-8条）</h3>
      <div id="rootcauseList"></div>
    </section>
    
    <!-- 趋势预测（F阶段） -->
    <section class="forecast-section">
      <h3>趋势预测</h3>
      <div id="forecastContent"></div>
    </section>
    
    <!-- 情景模拟（W阶段，交互滑块） -->
    <section class="whatif-section">
      <h3>情景模拟</h3>
      <div id="whatifContent"></div>
    </section>
    
    <!-- 行动建议 -->
    <section class="actions-section">
      <h3>行动建议</h3>
      <div id="actionsList"></div>
    </section>
    
    <!-- 数据自检注释 -->
    <section class="selfcheck-section">
      <h3>数据自检报告（C阶段）</h3>
      <div id="selfcheckContent"></div>
    </section>
  </div>
  
  <script>
    /* 业务逻辑 */
  </script>
</body>
</html>
```

## 布局规范（写死 · PC端为主）

### 整体布局
```yaml
页面宽度: 1200px居中，最大1440px
背景色: #f8fafc
卡片背景: #ffffff
卡片圆角: 12px
卡片阴影: 0 2px 8px rgba(0,0,0,0.06)
卡片间距: 24px
```

### 模块布局
```yaml
报头: 全宽渐变背景，白色文字
核心结论速览: 白色卡片，左侧蓝色边框
KPI卡片: 6个横排，响应式网格
单维度分析: 2列网格（图表卡片）
组合维度分析: 2列网格（热力图卡片）
洞察报告: 白色卡片，左侧黄色边框
根因诊断: 白色卡片，左侧红色边框，独立区块，5-8条
趋势预测: 白色卡片，左侧绿色边框
情景模拟: 白色卡片，左侧紫色边框，交互滑块
行动建议: 白色卡片，左侧橙色边框
数据自检: 放在页脚，只显示描述性信息
```

### 颜色规范
```yaml
主色: #2563eb（蓝色）- 标题、KPI、链接
辅色1: #10b981（绿色）- 正向指标、通过
辅色2: #f59e0b（黄色）- 警告、洞察
辅色3: #ef4444（红色）- 异常、根因
文字主色: #1f2937
文字次色: #6b7280
背景色: #f8fafc
```

### 字体规范
```yaml
页面标题: 28px，白色，加粗
模块标题: 18px，#1f2937，加粗，左侧4px色条
KPI数值: 28px，#2563eb，加粗
KPI标签: 13px，#6b7280
正文: 14px，#374151
标签/注释: 12-13px，#6b7280
```

## 动态生成规则

### KPI卡片
```
遍历KPI列表
  → 生成卡片HTML
  → 填充数值和标签
  → 添加变化标识（如有）
```

### 图表
```
遍历图表列表
  → 生成容器HTML
  → 调用ECharts渲染
  → 配置tooltip和animation
```

### 数据表格
```
识别字段列表
  → 生成表头
  → 填充数据行（最多100行）
  → 添加排序功能（可选）
```

### 洞察报告（8类通用方法，至少用5类，最终≥7条）

**8类通用方法**：

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

**规则（写死）**：
- 至少用5类方法
- 每类至少1条
- 最终≥7条洞察

**每条洞察输出格式**：
```
🔍 洞察 #N：[方法标签]
- 现象：……
- 数字证据：……
- 方法：……
- 置信度：……（基于N行数据）
- 建议：……【紧急/重要/长期】
```

**遍历逻辑**：
```
遍历洞察列表
  → 生成洞察卡片
  → 填充现象、数字证据、方法、置信度、建议
  → 标注优先级颜色
```

### 维度分析数量要求（智能决定）

**规则（写死）**：
- **单维度分析：必须覆盖≥80%的核心维度**
  - 核心维度：从业务角度最重要的维度（如渠道、地区、产品、时间等）
  - 判断标准：该维度是否能回答关键业务问题
  - 示例：数据有5个核心维度 → 单维度分析至少覆盖4个
- **组合维度分析**：根据维度数量动态决定
  - 3个维度以下：≥2个组合维度
  - 3个维度以上：≥3个组合维度
- **不设硬性数量限制，以"有分析价值"为准**
- **AI智能判断**：根据数据特征和业务价值，选择最有意义的维度组合

**维度选择逻辑**：
```
1. 识别所有可用维度（从数据字段中提取）
2. 按业务价值排序（核心维度 > 辅助维度）
3. 生成单维度分析（覆盖≥80%核心维度）
4. 生成组合维度分析（选择有业务价值的交叉）
   - 优先选择：渠道×地区、渠道×产品、地区×产品
   - 可选：时间×渠道、时间×地区、时间×产品
   - 高级：渠道×地区×产品（3维交叉）
5. 过滤无意义的组合（如两个数值字段交叉）
```
- **优先级**：核心业务维度 > 辅助维度 > 边缘维度

**示例**：
- 数据有4个维度（渠道、地区、产品、时间）→ 单维度4个 + 组合维度≥3个 = 总计≥7个
- 数据有3个维度（渠道、地区、产品）→ 单维度3个 + 组合维度≥2个 = 总计≥5个

### 组合维度图表

**热力图设计规则（写死）**：
- **横坐标（X轴）**：放维度数量多的（如产品有15个）
- **纵坐标（Y轴）**：放维度数量少的（如渠道有4个）
- **超出页面**：支持横向滚动，不换行
- **单元格**：显示具体数值，颜色深浅表示大小

```
渠道×产品热力图
  → 横坐标：产品（维度数量多）
  → 纵坐标：渠道（维度数量少）
  → 支持横向滚动
  → 颜色深浅表示销量
  → 标注具体数值

渠道×地区热力图
  → 横坐标：地区（维度数量多）
  → 纵坐标：渠道（维度数量少）
  → 支持横向滚动

地区×产品热力图
  → 横坐标：产品（维度数量多）
  → 纵坐标：地区（维度数量少）
  → 支持横向滚动

渠道×地区×产品多维分析
  → 树形图展示
  → 多维度交叉对比
```

### WFR深度分析

#### What-if情景模拟
```
→ 设定目标变量（如：提升销售额）
→ 设定自变量（如：渠道拓展、产品优化）
→ 模拟不同场景的结果
→ 输出：场景A/B/C的预测结果
```

#### Forecast趋势预测（写死输出格式）
```
→ 选择预测方法（移动平均/指数平滑/线性回归/季节性分解）
→ 必须说明为什么选这个方法
→ 执行预测
→ 输出必须包含：
   - 预测方法名称
   - 选择该方法的理由
   - 预测值 + 置信区间
   - 置信度（高/中/低）及原因
   - 数据局限性说明（至少2条）
   - 假设条件
```

#### Root Cause根因诊断（写死输出格式）

**输出条数（写死）**：
- **每次R分析输出5-8条根因**
- 每条针对一个异常值或一个KPI
- 每条必须包含：方法选择依据、判断标准、量化数据、反例检验、边界条件、置信度

**每条根因输出格式**：
```
→ 选择诊断方法（5 Whys/鱼骨图/帕累托/下钻归因/价值树/时间序列归因/组合维度归因）
→ 必须说明为什么选这个方法
→ 分析根本原因
→ 输出必须包含：
   - 根因方法名称
   - 选择该方法的理由
   - 判断标准（具体数字，如"< 8%为异常"）
   - 量化数据支撑（基于N行数据，计算过程）
   - 反例检验（什么情况下结论不成立）
   - 边界条件（结论适用范围）
   - 置信度（高/中/低）
```

**R分析与8类洞察的关系（写死）**：
- R分析是8类洞察的**升级版**
- 8类洞察（Tool模式）：用固定规则驱动，适合离线HTML工具
- R分析（PDCAWFR模式）：用AI深度分析，适合在线报告
- R分析可以选择8类中的方法（如帕累托、下钻归因），但会更深入（包含反例检验、边界条件等）

### 数据自检报告
```
总量校验
  → 各分类加总 vs KPI总计
  → 差异分析

公式校验
  → 分子分母验证
  → 单位一致性

极端值校验
  → 异常值识别
  → 影响评估
```

### 行动建议
```
遍历建议列表
  → 生成建议卡片
  → 填充建议内容
  → 标注优先级（紧急/重要/长期）
  → 量化预期效果
```

## 交互功能

### 交互动画要求（写死）

```css
/* 上传按钮 hover 变深 */
.upload-btn { transition: background-color 0.2s ease; }
.upload-btn:hover { background-color: #1d4ed8; }

/* 拖拽区域 hover 时虚线变实线 + 蓝色 */
.upload-zone { border: 2px dashed #9ca3af; transition: all 0.2s ease; }
.upload-zone:hover { border-color: #2563eb; border-style: solid; }

/* 图表加载 fadeIn 动画 */
.chart-card { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* 图表尺寸限制（防止图表过大） */
.chart-container { max-width: 100%; overflow: hidden; }
.chart-container > div { max-width: 100% !important; }
.heatmap-scroll { overflow-x: auto; }

/* KPI 数字滚动动画（从0滚动到目标值） */
.kpi-number { transition: all 0.5s ease; }
```

### 上传功能
```javascript
// 拖拽上传
uploadZone.addEventListener('drop', handleDrop);

// 点击上传
uploadZone.addEventListener('click', () => fileInput.click());

// 文件处理
function handleFile(file) {
  // 解析Excel
  // 执行分析
  // 更新页面
}
```

### 图表交互
```javascript
// tooltip
tooltip: { trigger: 'axis' }

// 动画
animation: true

// 响应式
window.addEventListener('resize', () => chart.resize());
```

### 下载功能
```javascript
// 下载HTML
function downloadHTML() {
  const html = document.documentElement.outerHTML;
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = '分析报告.html';
  a.click();
}

// 下载Excel
function downloadExcel() {
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(data);
  XLSX.utils.book_append_sheet(wb, ws, "分析结果");
  XLSX.writeFile(wb, "分析报告.xlsx");
}
```

## 文件大小控制

- 最大文件: 500KB
- 建议文件: 200-300KB
- 图片: 不内嵌，使用CDN
- 字体: 不内嵌，使用系统字体

## Tool模式代码健壮性要求（写死）

由于Tool模式生成的是离线HTML工具，代码质量直接影响用户体验。必须满足以下要求：

### 1. Sheet名识别（4层兜底）
- 精确匹配规定英文名
- 中英文别名匹配
- 按字段内容推断
- 按位置兜底
- 全部失败 → 提示"无法识别表"

### 2. 字段识别
- 支持中文别名（如"金额"对应"amount"）
- 识别不到字段 → 填空值或0，整页不崩

### 3. 数据类型处理
- 数值字段必须是数字（空值或文字转成0）
- 字符串字段保持原样

### 4. 公式正确性
- 分母为0时显示为空，不能算出无穷大
- 比率类指标：除法分母为0时显示"-"或"0"

### 5. 错误处理
- 上传/解析/渲染任何环节出错 → 显示红色错误提示
- 出错不能让整个页面变白屏

### 6. 降级显示
- 图表数据为空 → 显示"暂无数据"
- KPI没数据 → 显示0，不显示NaN
- 字段缺失 → 跳过该图表，提示业务人员

### 7. Tool模式自检逻辑（写死）

**Tool模式必须在HTML中实现以下自检逻辑**：

```
C阶段自检（基于解析后的数据执行）：
1. 总量校验：各分类加总 vs KPI总计
   → 差异 > 10% → 标记为"数据口径不一致"
2. 公式校验：分子分母验证、单位一致性
   → 发现倒置 → 标记为"公式错误"
3. 极端值校验：异常值识别、影响评估
   → 发现异常 → 标记为"存在异常值"
```

**自检结果展示**：
- 通过 → 显示"✅ 已通过数据自检"
- 警告 → 显示"⚠️ 数据口径不一致（差异X%）"
- 错误 → 显示"❌ 公式错误，请检查数据"

**自检区块位置**：放在页脚，只显示描述性信息

## 错误处理

- HTML生成失败 → 显示错误提示
- 文件过大 → 压缩代码
- 样式冲突 → 使用命名空间
