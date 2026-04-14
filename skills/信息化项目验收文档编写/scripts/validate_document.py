#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息化项目验收文档编写技能 - 文档验证脚本

功能：验证文档的完整性和规范性
作者：Claude
日期：2026-01-27
"""

import os
import re
import json
from typing import Dict, List, Tuple


class DocumentValidator:
    """文档验证器"""

    def __init__(self):
        self.required_sections = {
            '概要设计': [
                '项目概述', '总体架构设计', '系统功能架构', '技术路线',
                '关键设计', '部署架构', '接口设计', '数据架构', '实施计划'
            ],
            '详细设计': [
                '模块概述', '功能设计', '接口设计', '数据结构设计',
                '算法与逻辑设计', '异常处理', '性能设计', '安全设计'
            ],
            '产品手册': [
                '产品概述', '系统功能', '用户操作指南', '系统管理',
                '常见问题解答', '系统维护', '技术支持'
            ],
            '测试报告': [
                '测试概述', '测试策略', '测试用例执行情况', '缺陷分析',
                '测试问题汇总', '测试结论', '测试建议'
            ],
            '架构设计': [
                '架构概述', '总体架构设计', '技术架构', '应用架构',
                '数据架构', '部署架构', '安全架构', '性能架构'
            ],
            '数据库设计': [
                '数据库设计概述', '需求分析', '概念设计', '逻辑设计',
                '物理设计', '安全设计', '备份恢复策略', '性能监控'
            ],
            '运维报告': [
                '运维概述', '系统架构', '监控体系', '日常运维',
                '故障管理', '性能优化', '安全管理', '备份恢复'
            ],
            '可研报告': [
                '项目概述', '项目建设必要性', '项目建设方案', '项目实施情况',
                '系统运行情况', '技术可行性分析', '经济可行性分析', '社会可行性分析'
            ],
            '立项报告': [
                '项目基本信息', '项目建设必要性', '项目建设方案', '项目实施情况',
                '系统运行情况', '投资估算', '经济效益分析', '社会效益分析'
            ]
        }

        self.required_fields = {
            '文档信息': ['文档编号', '文档名称', '编制单位', '编制日期', '文档版本'],
            '修订记录': ['版本号', '修订日期', '修订内容', '修订人'],
            '项目概述': ['项目背景', '建设目标', '建设范围']
        }

    def validate_document_structure(self, content: str, doc_type: str) -> Tuple[bool, List[str]]:
        """
        验证文档结构完整性

        Args:
            content: 文档内容
            doc_type: 文档类型

        Returns:
            (是否通过, 错误列表)
        """
        errors = []

        # 检查文档信息
        if '文档信息' not in content:
            errors.append("缺少'文档信息'章节")

        # 检查修订记录
        if '修订记录' not in content:
            errors.append("缺少'修订记录'章节")

        # 检查必需章节
        if doc_type in self.required_sections:
            for section in self.required_sections[doc_type]:
                if section not in content:
                    errors.append(f"缺少必需章节: {section}")

        # 检查关键字段
        for section, fields in self.required_fields.items():
            if section in content:
                for field in fields:
                    if field not in content:
                        errors.append(f"在{section}中缺少字段: {field}")

        return len(errors) == 0, errors

    def validate_document_format(self, content: str) -> Tuple[bool, List[str]]:
        """
        验证文档格式规范性

        Args:
            content: 文档内容

        Returns:
            (是否通过, 错误列表)
        """
        errors = []

        # 检查标题层级
        lines = content.split('\n')
        title_levels = []
        for line in lines:
            if line.startswith('# ') and not line.startswith('```'):
                title_levels.append(1)
            elif line.startswith('## ') and not line.startswith('```'):
                title_levels.append(2)
            elif line.startswith('### ') and not line.startswith('```'):
                title_levels.append(3)
            elif line.startswith('#### ') and not line.startswith('```'):
                title_levels.append(4)

        # 检查标题层级是否连续（允许跳级，但不能跳太多）
        for i in range(1, len(title_levels)):
            if title_levels[i] > title_levels[i-1] + 2:  # 允许跳1级
                errors.append(f"标题层级跳跃过大: 从{title_levels[i-1]}级跳到{title_levels[i]}级")

        # 检查表格格式 - 简化检查，只检查基本格式
        table_pattern = r'\|.*\|'
        tables = re.findall(table_pattern, content)
        if tables:
            # 检查表格行是否都有表头分隔线
            table_lines = [line for line in lines if line.strip().startswith('|')]
            if table_lines:
                # 检查是否有表头分隔线（包含---的行）
                has_separator = any('---' in line for line in table_lines)
                if not has_separator and len(table_lines) > 1:
                    errors.append("表格缺少表头分隔线")

        # 检查代码块格式
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        for block in code_blocks:
            if block.count('```') != 2:
                errors.append("代码块格式错误")

        return len(errors) == 0, errors

    def validate_content_completeness(self, content: str, doc_type: str) -> Tuple[bool, List[str]]:
        """
        验证内容完整性

        Args:
            content: 文档内容
            doc_type: 文档类型

        Returns:
            (是否通过, 错误列表)
        """
        errors = []

        # 检查是否有TODO标记（允许在示例中）
        if 'TODO' in content and '示例' not in content:
            errors.append("文档中包含未完成的TODO标记")

        # 检查是否有明显的占位符（但允许示例中的占位符）
        placeholders = ['[待填写]', '[待完善]', '[待补充]']
        for placeholder in placeholders:
            if placeholder in content:
                errors.append(f"文档中包含占位符: {placeholder}")

        # 检查是否有空章节（但允许有示例内容的章节）
        lines = content.split('\n')
        empty_sections = []
        for i, line in enumerate(lines):
            if line.startswith('#') and not line.startswith('```'):
                # 检查下一非空行是否是示例或说明
                next_content = ''
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        next_content = next_line
                        break

                # 如果下一内容是示例或说明，不算空章节
                if next_content and ('示例' in next_content or '说明' in next_content or '描述' in next_content):
                    continue

                # 检查是否真的是空章节（只有占位符）
                if next_content and ('[' in next_content and ']' in next_content):
                    empty_sections.append(line.strip())

        if empty_sections:
            errors.append(f"存在内容不完整的章节: {', '.join(empty_sections[:3])}")  # 只显示前3个

        return len(errors) == 0, errors

    def validate_document(self, file_path: str, doc_type: str) -> Dict:
        """
        验证文档

        Args:
            file_path: 文件路径
            doc_type: 文档类型

        Returns:
            验证结果字典
        """
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'errors': [f'文件不存在: {file_path}']
            }

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 执行各项验证
        structure_valid, structure_errors = self.validate_document_structure(content, doc_type)
        format_valid, format_errors = self.validate_document_format(content)
        content_valid, content_errors = self.validate_content_completeness(content, doc_type)

        # 汇总结果
        all_errors = structure_errors + format_errors + content_errors
        is_valid = structure_valid and format_valid and content_valid

        return {
            'valid': is_valid,
            'file_path': file_path,
            'doc_type': doc_type,
            'structure_valid': structure_valid,
            'format_valid': format_valid,
            'content_valid': content_valid,
            'structure_errors': structure_errors,
            'format_errors': format_errors,
            'content_errors': content_errors,
            'all_errors': all_errors,
            'error_count': len(all_errors)
        }


def main():
    """主函数"""
    validator = DocumentValidator()

    # 示例：验证参考文档
    reference_dir = 'references'
    if os.path.exists(reference_dir):
        print("开始验证参考文档...")
        print("=" * 50)

        # 定义文档类型映射
        doc_type_map = {
            '概要设计模板.md': '概要设计',
            '详细设计模板.md': '详细设计',
            '产品手册模板.md': '产品手册',
            '测试报告模板.md': '测试报告',
            '架构设计模板.md': '架构设计',
            '数据库设计模板.md': '数据库设计',
            '运维报告模板.md': '运维报告',
            '可研报告模板.md': '可研报告',
            '立项报告模板.md': '立项报告'
        }

        results = []
        for filename, doc_type in doc_type_map.items():
            file_path = os.path.join(reference_dir, filename)
            if os.path.exists(file_path):
                result = validator.validate_document(file_path, doc_type)
                results.append(result)

                # 输出验证结果
                status = "✅ 通过" if result['valid'] else "❌ 不通过"
                print(f"{filename} ({doc_type}): {status}")

                if not result['valid']:
                    print(f"  错误数量: {result['error_count']}")
                    for error in result['all_errors'][:5]:  # 只显示前5个错误
                        print(f"  - {error}")
                    if len(result['all_errors']) > 5:
                        print(f"  ... 还有 {len(result['all_errors']) - 5} 个错误")
                print()

        # 统计结果
        total = len(results)
        passed = sum(1 for r in results if r['valid'])
        failed = total - passed

        print("=" * 50)
        print(f"验证完成: 总计 {total} 个文档, 通过 {passed} 个, 失败 {failed} 个")

        if failed > 0:
            print("\n失败的文档:")
            for result in results:
                if not result['valid']:
                    print(f"  - {result['file_path']}")

        return failed == 0
    else:
        print(f"目录 {reference_dir} 不存在")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)