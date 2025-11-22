#!/usr/bin/env python3
"""
Confluence页面创建器测试脚本
用于测试技能的各个组件功能
"""

import asyncio
import os
import tempfile
import yaml
from main import ConfluencePageCreator


async def test_content_generation():
    """测试内容生成功能"""
    print("🧪 测试内容生成功能...")

    config = {
        'page_title': '测试会议纪要',
        'page_template': 'meeting-notes',
        'tags': ['测试']
    }

    creator = ConfluencePageCreator(config)
    content = await creator.generate_page_content()

    print("✅ 内容生成测试通过")
    print(f"   标题: {content['title']}")
    print(f"   内容长度: {len(content['content'])} 字符")
    print(f"   标签: {content['tags']}")
    return True


async def test_config_validation():
    """测试配置验证功能"""
    print("🧪 测试配置验证功能...")

    # 测试缺少必需参数
    try:
        config = {'page_title': 'test'}
        ConfluencePageCreator(config)
        print("❌ 配置验证测试失败：应该抛出异常")
        return False
    except ValueError as e:
        print(f"✅ 配置验证测试通过：正确捕获异常 - {e}")
        return True
    except Exception as e:
        print(f"❌ 配置验证测试失败：意外异常 - {e}")
        return False


async def test_template_types():
    """测试所有模板类型"""
    print("🧪 测试所有模板类型...")

    templates = ['meeting-notes', 'project-update', 'technical-doc', 'custom']

    for template in templates:
        try:
            config = {
                'confluence_url': 'https://test.atlassian.net/wiki',
                'space_key': 'TEST',
                'username': 'test@test.com',
                'api_token': 'test-token',
                'page_title': f'测试{template}模板',
                'page_template': template
            }

            creator = ConfluencePageCreator(config)
            content = await creator.generate_page_content()

            print(f"   ✅ {template} 模板测试通过")

        except Exception as e:
            print(f"   ❌ {template} 模板测试失败：{e}")
            return False

    return True


def test_config_file_loading():
    """测试配置文件加载"""
    print("🧪 测试配置文件加载...")

    # 创建临时配置文件
    test_config = {
        'confluence_url': 'https://test.atlassian.net/wiki',
        'space_key': 'TEST',
        'username': 'test@test.com',
        'api_token': 'test-token',
        'page_title': '测试页面',
        'page_template': 'meeting-notes'
    }

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            temp_file = f.name

        # 加载配置文件
        with open(temp_file, 'r', encoding='utf-8') as f:
            loaded_config = yaml.safe_load(f)

        # 验证配置
        creator = ConfluencePageCreator(loaded_config)

        # 清理临时文件
        os.unlink(temp_file)

        print("✅ 配置文件加载测试通过")
        return True

    except Exception as e:
        print(f"❌ 配置文件加载测试失败：{e}")
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file)
            except:
                pass
        return False


def test_yaml_parsing():
    """测试YAML解析功能"""
    print("🧪 测试YAML解析功能...")

    test_yaml_content = """
confluence_url: "https://test.atlassian.net/wiki"
space_key: "TEST"
username: "test@test.com"
api_token: "test-token"
page_title: "测试页面"
page_template: "meeting-notes"
tags:
  - "测试"
  - "自动化"
headless: false
timeout: 25000
"""

    try:
        config = yaml.safe_load(test_yaml_content)

        # 验证解析结果
        assert config['confluence_url'] == "https://test.atlassian.net/wiki"
        assert config['space_key'] == "TEST"
        assert isinstance(config['tags'], list)
        assert len(config['tags']) == 2

        print("✅ YAML解析测试通过")
        return True

    except Exception as e:
        print(f"❌ YAML解析测试失败：{e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行Confluence页面创建器测试套件")
    print("=" * 60)

    tests = [
        test_config_validation,
        test_config_file_loading,
        test_yaml_parsing,
        test_content_generation,
        test_template_types,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()

            if result:
                passed += 1

        except Exception as e:
            print(f"❌ 测试异常：{e}")

        print()  # 空行分隔

    print("=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！技能功能正常")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关功能")
        return False


async def main():
    """主函数"""
    success = await run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)