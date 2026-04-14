#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息化项目验收文档编写技能 - 模板生成脚本

功能：根据项目信息生成文档模板
作者：Claude
日期：2026-01-27
"""

import os
import re
from datetime import datetime
from typing import Dict, List


class TemplateGenerator:
    """模板生成器"""

    def __init__(self):
        self.template_dir = 'references'
        self.output_dir = 'generated_docs'

    def create_output_dir(self):
        """创建输出目录"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建输出目录: {self.output_dir}")

    def generate_project_info(self, project_info: Dict) -> str:
        """生成项目信息部分"""
        doc_name = project_info.get('doc_name', '[文档名称]')
        info_lines = [
            "## 文档信息",
            f"- **文档编号**: {project_info.get('project_code', '[项目编号]')}-{project_info.get('doc_type', '[文档类型]')}-[版本号]",
            f"- **文档名称**: {project_info.get('project_name', '[项目名称]')} {doc_name}",
            f"- **编制单位**: {project_info.get('company', '[编制单位]')}",
            f"- **编制日期**: {datetime.now().strftime('%Y-%m-%d')}",
            f"- **审核日期**: [YYYY-MM-DD]",
            f"- **批准日期**: [YYYY-MM-DD]",
            f"- **文档版本**: V1.0"
        ]
        return '\n'.join(info_lines)

    def generate_revision_record(self) -> str:
        """生成修订记录"""
        return """## 修订记录
| 版本号 | 修订日期 | 修订内容 | 修订人 | 审核人 | 批准人 |
|--------|----------|----------|--------|--------|--------|
| V1.0   | YYYY-MM-DD | 初稿创建 | [姓名] | [姓名] | [姓名] |"""

    def load_template(self, template_name: str) -> str:
        """加载模板文件"""
        template_path = os.path.join(self.template_dir, f"{template_name}.md")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除文档信息和修订记录部分（将重新生成）
        content = re.sub(r'## 文档信息\n.*?\n\n', '', content, flags=re.DOTALL)
        content = re.sub(r'## 修订记录\n.*?\n\n', '', content, flags=re.DOTALL)

        return content

    def replace_placeholders(self, content: str, project_info: Dict) -> str:
        """替换占位符"""
        replacements = {
            '[项目名称]': project_info.get('project_name', '[项目名称]'),
            '[项目编号]': project_info.get('project_code', '[项目编号]'),
            '[承建单位]': project_info.get('company', '[承建单位]'),
            '[编制单位]': project_info.get('company', '[编制单位]'),
            '[YYYY-MM-DD]': datetime.now().strftime('%Y-%m-%d'),
            '[版本号]': 'V1.0'
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        return content

    def generate_document(self, doc_type: str, project_info: Dict) -> str:
        """生成文档"""
        # 模板名称映射
        template_map = {
            '概要设计': '概要设计模板',
            '详细设计': '详细设计模板',
            '产品手册': '产品手册模板',
            '测试报告': '测试报告模板',
            '架构设计': '架构设计模板',
            '数据库设计': '数据库设计模板',
            '运维报告': '运维报告模板',
            '可研报告': '可研报告模板',
            '立项报告': '立项报告模板'
        }

        if doc_type not in template_map:
            raise ValueError(f"不支持的文档类型: {doc_type}")

        template_name = template_map[doc_type]

        # 加载模板
        try:
            content = self.load_template(template_name)
        except FileNotFoundError as e:
            return f"错误: {str(e)}"

        # 生成文档信息
        project_info['doc_type'] = doc_type
        project_info['doc_name'] = doc_type
        doc_info = self.generate_project_info(project_info)

        # 生成修订记录
        revision_record = self.generate_revision_record()

        # 组合文档
        document = f"{doc_info}\n\n{revision_record}\n\n{content}"

        # 替换占位符
        document = self.replace_placeholders(document, project_info)

        return document

    def save_document(self, content: str, filename: str):
        """保存文档"""
        self.create_output_dir()
        file_path = os.path.join(self.output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"文档已保存: {file_path}")

    def batch_generate(self, project_info: Dict, doc_types: List[str]):
        """批量生成文档"""
        print(f"开始批量生成文档，项目: {project_info.get('project_name', '未知项目')}")
        print("=" * 60)

        for doc_type in doc_types:
            try:
                print(f"生成 {doc_type}...")
                content = self.generate_document(doc_type, project_info)

                # 生成文件名
                filename = f"{project_info.get('project_code', 'project')}_{doc_type}.md"
                self.save_document(content, filename)

                print(f"  ✅ 成功生成 {doc_type}")
            except Exception as e:
                print(f"  ❌ 生成 {doc_type} 失败: {str(e)}")

        print("=" * 60)
        print(f"批量生成完成，文档保存在: {self.output_dir}")


def main():
    """主函数"""
    # 示例项目信息
    project_info = {
        'project_name': 'XX信息化项目',
        'project_code': 'IT-2026-001',
        'company': 'XX科技有限公司'
    }

    # 要生成的文档类型
    doc_types = [
        '概要设计',
        '详细设计',
        '产品手册',
        '测试报告',
        '架构设计',
        '数据库设计',
        '运维报告',
        '可研报告',
        '立项报告'
    ]

    # 创建生成器
    generator = TemplateGenerator()

    # 执行批量生成
    generator.batch_generate(project_info, doc_types)

    print("\n使用说明:")
    print("1. 生成的文档保存在 'generated_docs' 目录下")
    print("2. 请根据实际项目情况修改文档内容")
    print("3. 建议逐个文档进行完善和审核")


if __name__ == '__main__':
    main()