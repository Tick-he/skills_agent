#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息化项目验收文档编写技能 - 简化验证脚本

功能：验证文档的基本结构完整性
作者：Claude
日期：2026-01-27
"""

import os
import re
from typing import Dict, List, Tuple


class SimpleDocumentValidator:
    """简化文档验证器"""

    def __init__(self):
        self.required_sections = {
            '概要设计': ['项目概述', '总体架构设计', '系统功能架构', '技术路线'],
            '详细设计': ['模块概述', '功能设计', '接口设计', '数据结构设计'],
            '产品手册': ['产品概述', '系统功能', '用户操作指南', '常见问题解答'],
            '测试报告': ['测试概述', '测试策略', '测试用例执行情况', '测试结论'],
            '架构设计': ['架构概述', '总体架构设计', '技术架构', '应用架构'],
            '数据库设计': ['数据库设计概述', '需求分析', '概念设计', '逻辑设计'],
            '运维报告': ['运维概述', '系统架构', '监控体系', '日常运维'],
            '可研报告': ['项目概述', '项目建设必要性', '项目建设方案', '经济可行性分析'],
            '立项报告': ['项目基本信息', '项目建设必要性', '项目建设方案', '投资估算']
        }

    def validate_basic_structure(self, content: str) -> Tuple[bool, List[str]]:
        """验证基本结构"""
        errors = []

        # 检查文档信息
        if '文档信息' not in content:
            errors.append("缺少'文档信息'章节")

        # 检查修订记录
        if '修订记录' not in content:
            errors.append("缺少'修订记录'章节")

        # 检查是否有标题
        if not re.search(r'^#+\s+', content, re.MULTILINE):
            errors.append("缺少标题")

        return len(errors) == 0, errors

    def validate_required_sections(self, content: str, doc_type: str) -> Tuple[bool, List[str]]:
        """验证必需章节"""
        errors = []

        if doc_type in self.required_sections:
            for section in self.required_sections[doc_type]:
                if section not in content:
                    errors.append(f"缺少必需章节: {section}")

        return len(errors) == 0, errors

    def validate_document(self, file_path: str, doc_type: str) -> Dict:
        """验证文档"""
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'errors': [f'文件不存在: {file_path}']
            }

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 执行验证
        basic_valid, basic_errors = self.validate_basic_structure(content)
        sections_valid, sections_errors = self.validate_required_sections(content, doc_type)

        all_errors = basic_errors + sections_errors
        is_valid = basic_valid and sections_valid

        return {
            'valid': is_valid,
            'file_path': file_path,
            'doc_type': doc_type,
            'basic_valid': basic_valid,
            'sections_valid': sections_valid,
            'basic_errors': basic_errors,
            'sections_errors': sections_errors,
            'all_errors': all_errors,
            'error_count': len(all_errors)
        }


def main():
    """主函数"""
    validator = SimpleDocumentValidator()

    # 示例：验证参考文档
    reference_dir = 'references'
    if not os.path.exists(reference_dir):
        print(f"目录 {reference_dir} 不存在")
        return False

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
                for error in result['all_errors']:
                    print(f"  - {error}")
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


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)