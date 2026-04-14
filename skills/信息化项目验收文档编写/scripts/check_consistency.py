#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息化项目验收文档编写技能 - 一致性检查脚本

功能：检查多个文档之间的一致性
作者：Claude
日期：2026-01-27
"""

import os
import re
from typing import Dict, List, Set


class ConsistencyChecker:
    """一致性检查器"""

    def __init__(self):
        self.common_terms = {
            '项目名称': r'项目名称[:：]\s*(.+)',
            '项目编号': r'项目编号[:：]\s*(.+)',
            '编制单位': r'编制单位[:：]\s*(.+)',
            '文档版本': r'文档版本[:：]\s*(.+)'
        }

    def extract_metadata(self, content: str) -> Dict[str, str]:
        """提取文档元数据"""
        metadata = {}

        # 提取文档信息
        doc_info_match = re.search(r'## 文档信息\n(.*?)##', content, re.DOTALL)
        if doc_info_match:
            doc_info = doc_info_match.group(1)
            for term, pattern in self.common_terms.items():
                match = re.search(pattern, doc_info)
                if match:
                    metadata[term] = match.group(1).strip()

        return metadata

    def extract_sections(self, content: str) -> Set[str]:
        """提取文档章节"""
        sections = set()
        lines = content.split('\n')

        for line in lines:
            # 匹配标题（#、##、###）
            if line.startswith('#') and not line.startswith('```'):
                # 移除#符号和空格
                title = re.sub(r'^#+\s*', '', line).strip()
                if title:
                    sections.add(title)

        return sections

    def check_metadata_consistency(self, docs_metadata: Dict[str, Dict]) -> List[str]:
        """检查元数据一致性"""
        errors = []

        if not docs_metadata:
            return errors

        # 获取第一个文档的元数据作为基准
        first_doc = next(iter(docs_metadata.values()))
        reference_name = first_doc.get('项目名称', '')
        reference_code = first_doc.get('项目编号', '')
        reference_company = first_doc.get('编制单位', '')

        for doc_name, metadata in docs_metadata.items():
            # 检查项目名称一致性
            if '项目名称' in metadata:
                if metadata['项目名称'] != reference_name:
                    errors.append(f"{doc_name}: 项目名称不一致 - '{metadata['项目名称']}' vs '{reference_name}'")

            # 检查项目编号一致性
            if '项目编号' in metadata:
                if metadata['项目编号'] != reference_code:
                    errors.append(f"{doc_name}: 项目编号不一致 - '{metadata['项目编号']}' vs '{reference_code}'")

            # 检查编制单位一致性
            if '编制单位' in metadata:
                if metadata['编制单位'] != reference_company:
                    errors.append(f"{doc_name}: 编制单位不一致 - '{metadata['编制单位']}' vs '{reference_company}'")

        return errors

    def check_section_consistency(self, docs_sections: Dict[str, Set[str]]) -> List[str]:
        """检查章节一致性"""
        errors = []

        if not docs_sections:
            return errors

        # 找出所有文档都有的章节
        all_sections = set.intersection(*docs_sections.values())

        # 找出部分文档有的章节
        for doc_name, sections in docs_sections.items():
            other_docs = [d for d in docs_sections.keys() if d != doc_name]
            if other_docs:
                # 检查是否有其他文档没有的章节
                other_sections = set.union(*[docs_sections[d] for d in other_docs])
                unique_sections = sections - other_sections
                if unique_sections:
                    errors.append(f"{doc_name}: 有其他文档没有的章节: {', '.join(list(unique_sections)[:3])}")

        return errors

    def check_common_sections(self, docs_sections: Dict[str, Set[str]]) -> List[str]:
        """检查必需章节"""
        errors = []

        # 定义各类文档的必需章节
        required_sections = {
            '概要设计': {'项目概述', '总体架构设计', '系统功能架构', '技术路线'},
            '详细设计': {'模块概述', '功能设计', '接口设计', '数据结构设计'},
            '产品手册': {'产品概述', '系统功能', '用户操作指南', '常见问题解答'},
            '测试报告': {'测试概述', '测试策略', '测试用例执行情况', '测试结论'},
            '架构设计': {'架构概述', '总体架构设计', '技术架构', '应用架构'},
            '数据库设计': {'数据库设计概述', '需求分析', '概念设计', '逻辑设计'},
            '运维报告': {'运维概述', '系统架构', '监控体系', '日常运维'},
            '可研报告': {'项目概述', '项目建设必要性', '项目建设方案', '经济可行性分析'},
            '立项报告': {'项目基本信息', '项目建设必要性', '项目建设方案', '投资估算'}
        }

        for doc_name, sections in docs_sections.items():
            # 从文件名推断文档类型
            doc_type = None
            for type_name in required_sections.keys():
                if type_name in doc_name:
                    doc_type = type_name
                    break

            if doc_type and doc_type in required_sections:
                missing = required_sections[doc_type] - sections
                if missing:
                    errors.append(f"{doc_name} ({doc_type}): 缺少必需章节: {', '.join(list(missing)[:3])}")

        return errors

    def check_file_naming(self, file_list: List[str]) -> List[str]:
        """检查文件命名规范"""
        errors = []

        # 定义期望的命名模式
        expected_patterns = [
            r'.*概要设计.*\.md$',
            r'.*详细设计.*\.md$',
            r'.*产品手册.*\.md$',
            r'.*测试报告.*\.md$',
            r'.*架构设计.*\.md$',
            r'.*数据库设计.*\.md$',
            r'.*运维报告.*\.md$',
            r'.*可研报告.*\.md$',
            r'.*立项报告.*\.md$'
        ]

        for filename in file_list:
            if not any(re.match(pattern, filename) for pattern in expected_patterns):
                errors.append(f"文件命名不规范: {filename}")

        return errors

    def check_document_links(self, docs_metadata: Dict[str, Dict]) -> List[str]:
        """检查文档间的引用关系"""
        errors = []

        # 检查是否有文档相互引用
        for doc_name, metadata in docs_metadata.items():
            # 这里可以添加更复杂的引用检查逻辑
            # 例如检查"相关文档"部分是否引用了其他文档
            pass

        return errors

    def analyze_document_structure(self, docs_sections: Dict[str, Set[str]]) -> Dict:
        """分析文档结构"""
        analysis = {
            'total_docs': len(docs_sections),
            'common_sections': {},
            'unique_sections': {},
            'structure_patterns': {}
        }

        if not docs_sections:
            return analysis

        # 找出共同章节
        all_sections = set.intersection(*docs_sections.values())
        analysis['common_sections'] = {s: len(docs_sections) for s in all_sections}

        # 找出各文档独有的章节
        for doc_name, sections in docs_sections.items():
            other_docs = [d for d in docs_sections.keys() if d != doc_name]
            if other_docs:
                other_sections = set.union(*[docs_sections[d] for d in other_docs])
                unique = sections - other_sections
                if unique:
                    analysis['unique_sections'][doc_name] = list(unique)

        return analysis

    def check_directory_structure(self, base_dir: str) -> List[str]:
        """检查目录结构"""
        errors = []

        expected_dirs = ['references', 'scripts', 'assets']
        for dir_name in expected_dirs:
            dir_path = os.path.join(base_dir, dir_name)
            if not os.path.exists(dir_path):
                errors.append(f"缺少目录: {dir_name}")

        # 检查是否有必需的文件
        required_files = ['SKILL.md']
        for filename in required_files:
            file_path = os.path.join(base_dir, filename)
            if not os.path.exists(file_path):
                errors.append(f"缺少文件: {filename}")

        return errors

    def run_comprehensive_check(self, base_dir: str) -> Dict:
        """运行全面检查"""
        results = {
            'directory_check': {'valid': True, 'errors': []},
            'file_naming': {'valid': True, 'errors': []},
            'metadata_consistency': {'valid': True, 'errors': []},
            'section_consistency': {'valid': True, 'errors': []},
            'common_sections': {'valid': True, 'errors': []},
            'overall_valid': True,
            'analysis': {}
        }

        print("开始全面一致性检查...")
        print("=" * 60)

        # 1. 检查目录结构
        print("1. 检查目录结构...")
        dir_errors = self.check_directory_structure(base_dir)
        if dir_errors:
            results['directory_check']['valid'] = False
            results['directory_check']['errors'] = dir_errors
            results['overall_valid'] = False
            for error in dir_errors:
                print(f"   ❌ {error}")
        else:
            print("   ✅ 目录结构正常")

        # 2. 检查参考文档
        references_dir = os.path.join(base_dir, 'references')
        if os.path.exists(references_dir):
            print("2. 检查参考文档...")

            # 获取所有markdown文件
            md_files = [f for f in os.listdir(references_dir) if f.endswith('.md')]

            # 检查文件命名
            naming_errors = self.check_file_naming(md_files)
            if naming_errors:
                results['file_naming']['valid'] = False
                results['file_naming']['errors'] = naming_errors
                results['overall_valid'] = False
                for error in naming_errors:
                    print(f"   ❌ {error}")
            else:
                print("   ✅ 文件命名规范")

            # 读取文档内容并分析
            docs_metadata = {}
            docs_sections = {}

            for filename in md_files:
                file_path = os.path.join(references_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 提取元数据
                metadata = self.extract_metadata(content)
                if metadata:
                    docs_metadata[filename] = metadata

                # 提取章节
                sections = self.extract_sections(content)
                if sections:
                    docs_sections[filename] = sections

            # 3. 检查元数据一致性
            print("3. 检查元数据一致性...")
            metadata_errors = self.check_metadata_consistency(docs_metadata)
            if metadata_errors:
                results['metadata_consistency']['valid'] = False
                results['metadata_consistency']['errors'] = metadata_errors
                results['overall_valid'] = False
                for error in metadata_errors[:5]:  # 只显示前5个
                    print(f"   ❌ {error}")
                if len(metadata_errors) > 5:
                    print(f"   ... 还有 {len(metadata_errors) - 5} 个错误")
            else:
                print("   ✅ 元数据一致")

            # 4. 检查章节一致性
            print("4. 检查章节一致性...")
            section_errors = self.check_section_consistency(docs_sections)
            if section_errors:
                results['section_consistency']['valid'] = False
                results['section_consistency']['errors'] = section_errors
                results['overall_valid'] = False
                for error in section_errors[:5]:
                    print(f"   ❌ {error}")
                if len(section_errors) > 5:
                    print(f"   ... 还有 {len(section_errors) - 5} 个错误")
            else:
                print("   ✅ 章节结构一致")

            # 5. 检查必需章节
            print("5. 检查必需章节...")
            common_errors = self.check_common_sections(docs_sections)
            if common_errors:
                results['common_sections']['valid'] = False
                results['common_sections']['errors'] = common_errors
                results['overall_valid'] = False
                for error in common_errors:
                    print(f"   ❌ {error}")
            else:
                print("   ✅ 必需章节完整")

            # 6. 分析文档结构
            print("6. 分析文档结构...")
            analysis = self.analyze_document_structure(docs_sections)
            results['analysis'] = analysis

            print(f"   📊 分析完成: 共 {analysis['total_docs']} 个文档")
            if analysis['common_sections']:
                print(f"   📊 共同章节: {len(analysis['common_sections'])} 个")
            if analysis['unique_sections']:
                print(f"   📊 独有章节: {len(analysis['unique_sections'])} 个文档有独有章节")

        print("=" * 60)

        # 总体结论
        if results['overall_valid']:
            print("✅ 全面检查通过，文档结构良好")
        else:
            print("❌ 全面检查未通过，请查看上述错误信息")

        return results


def main():
    """主函数"""
    checker = ConsistencyChecker()
    base_dir = '.'  # 当前目录

    # 运行全面检查
    results = checker.run_comprehensive_check(base_dir)

    # 输出详细结果
    print("\n详细检查结果:")
    print("-" * 40)

    for check_name, check_result in results.items():
        if isinstance(check_result, dict) and 'valid' in check_result:
            status = "✅ 通过" if check_result['valid'] else "❌ 未通过"
            print(f"{check_name}: {status}")
            if not check_result['valid'] and 'errors' in check_result:
                for error in check_result['errors']:
                    print(f"  - {error}")

    # 输出分析结果
    if results.get('analysis'):
        analysis = results['analysis']
        print(f"\n文档结构分析:")
        print(f"  总文档数: {analysis['total_docs']}")
        print(f"  共同章节数: {len(analysis.get('common_sections', {}))}")
        print(f"  有独有章节的文档数: {len(analysis.get('unique_sections', {}))}")


if __name__ == '__main__':
    main()