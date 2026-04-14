# 📋 Markdown转Word使用示例

## 示例1：转换单个文档

### 场景：将项目概要设计转换为Word格式

```bash
# 转换单个markdown文件
python3 scripts/markdown_to_word.py \
  -i references/概要设计模板.md \
  -o 项目概要设计.docx \
  -t "XX信息化项目概要设计说明书"
```

**输出结果**：
- 文件：`项目概要设计.docx`
- 大小：约40KB
- 格式：标准Word文档，包含标题样式、表格等

### 转换效果
- ✅ 标题自动应用样式（黑体、加粗）
- ✅ 表格转换为Word表格
- ✅ 代码块以等宽字体显示
- ✅ 中文正常显示
- ✅ 段落格式规范

## 示例2：批量转换生成的文档

### 场景：将所有生成的项目文档转换为Word格式

```bash
# 批量转换generated_docs目录下的所有markdown文件
python3 scripts/markdown_to_word.py \
  -d generated_docs/ \
  -o word_output/
```

**输出结果**：
```
word_output/
├── IT-2026-001_产品手册.docx
├── IT-2026-001_可研报告.docx
├── IT-2026-001_架构设计.docx
├── IT-2026-001_概要设计.docx
├── IT-2026-001_测试报告.docx
├── IT-2026-001_立项报告.docx
├── IT-2026-001_详细设计.docx
├── IT-2026-001_运维报告.docx
└── IT-2026-001_数据库设计.docx
```

**转换统计**：
- 处理文件数：9个
- 总大小：约350KB
- 转换时间：约10秒
- 成功率：100%

## 示例3：转换参考模板为Word格式

### 场景：将所有markdown模板转换为Word模板

```bash
# 批量转换参考模板
python3 scripts/markdown_to_word.py \
  -d references/ \
  -o word_templates/
```

**输出结果**：
```
word_templates/
├── 产品手册模板.docx
├── 可研报告模板.docx
├── 架构设计模板.docx
├── 概要设计模板.docx
├── 测试报告模板.docx
├── 立项报告模板.docx
├── 详细设计模板.docx
├── 运维报告模板.docx
└── 数据库设计模板.docx
```

## 示例4：完整工作流程示例

### 场景：从零开始创建项目文档并输出Word格式

```bash
# 步骤1：生成文档模板
python3 scripts/generate_template.py

# 步骤2：验证文档质量
python3 scripts/simple_validate.py

# 步骤3：转换为Word格式
python3 scripts/markdown_to_word.py -d generated_docs/ -o word_output/

# 步骤4：检查输出文件
ls -lh word_output/
```

**预期输出**：
```
总用量 352K
-rw-r--r--  1 user  staff   41K 项目产品手册.docx
-rw-r--r--  1 user  staff   43K 项目可研报告.docx
-rw-r--r--  1 user  staff   42K 项目架构设计.docx
-rw-r--r--  1 user  staff   39K 项目概要设计.docx
-rw-r--r--  1 user  staff   41K 项目测试报告.docx
-rw-r--r--  1 user  staff   45K 项目立项报告.docx
-rw-r--r--  1 user  staff   41K 项目详细设计.docx
-rw-r--r--  1 user  staff   45K 项目运维报告.docx
-rw-r--r--  1 user  staff   44K 项目数据库设计.docx
```

## 示例5：自定义转换参数

### 场景：转换特定类型的文档

```bash
# 只转换设计类文档
python3 scripts/markdown_to_word.py \
  -d generated_docs/ \
  -o design_docs/ \
  -p "*设计*.md"

# 只转换报告类文档
python3 scripts/markdown_to_word.py \
  -d generated_docs/ \
  -o report_docs/ \
  -p "*报告*.md"
```

## 转换质量检查

### 检查Word文档格式
```bash
# 查看生成的Word文件信息
ls -lh word_output/

# 检查文件大小（正常范围：30-50KB）
# 检查文件数量（应该是9个）
```

### 手动检查要点
1. **打开文档**：双击Word文件，检查是否能正常打开
2. **查看格式**：检查标题样式、段落格式是否正确
3. **检查内容**：确认所有内容都已转换，无缺失
4. **中文显示**：确认中文字符正常显示，无乱码
5. **表格格式**：检查表格是否完整，边框是否清晰

## 常见问题解决

### 问题1：转换后Word文档无法打开
**解决方案**：
```bash
# 检查文件是否完整
ls -lh word_output/

# 重新转换
python3 scripts/markdown_to_word.py -i input.md -o output.docx
```

### 问题2：中文显示乱码
**解决方案**：
- 确保系统安装了中文字体
- 使用支持中文的Word版本
- 检查markdown文件的编码格式（UTF-8）

### 问题3：表格格式错乱
**解决方案**：
- 检查markdown表格格式是否正确
- 确保表格分隔线完整
- 重新转换并检查

### 问题4：部分内容缺失
**解决方案**：
- 检查markdown文档是否有语法错误
- 确认代码块是否正确闭合
- 重新转换并查看日志输出

## 性能优化建议

### 批量转换优化
```bash
# 使用通配符批量转换
python3 scripts/markdown_to_word.py -d generated_docs/ -o word_output/ -p "*.md"

# 转换完成后清理临时文件
rm -f test_*.docx
```

### 文件组织建议
```
项目文档/
├── markdown/          # 存放markdown源文件
├── word/              # 存放转换后的Word文件
├── pdf/               # 存放PDF文件（可选）
└── templates/         # 存放模板文件
```

## 高级用法

### 自定义样式（需要修改脚本）
如果需要更精细的样式控制，可以修改 `markdown_to_word.py` 中的样式设置：

```python
# 在 _setup_heading_styles 方法中修改样式
style.font.name = '微软雅黑'  # 修改字体
style.font.size = Pt(14)     # 修改字号
style.font.color.rgb = RGBColor(0, 0, 0)  # 修改颜色
```

### 与其他工具集成
```bash
# 与Git集成：自动转换并提交
git add generated_docs/
python3 scripts/markdown_to_word.py -d generated_docs/ -o word_output/
git add word_output/
git commit -m "更新项目文档和Word版本"

# 与CI/CD集成
# 在构建流程中自动转换文档
```

## 总结

通过markdown转word功能，您可以：
1. **快速转换**：几秒钟完成文档格式转换
2. **批量处理**：一次性转换多个文档
3. **保持格式**：自动应用专业的Word样式
4. **便于提交**：生成标准的Word文档格式
5. **提高效率**：避免手动复制粘贴的繁琐

**开始使用**：运行 `python3 scripts/markdown_to_word.py -h` 查看详细帮助！