#!/usr/bin/env python3
"""
Confluence页面创建自动化技能
使用Playwright自动化在Confluence平台创建文档页面
"""

import asyncio
import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import yaml


class ConfluencePageCreator:
    """Confluence页面创建自动化类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.generated_content: Dict[str, str] = {}

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # 验证必需参数
        self._validate_config()

    def _validate_config(self):
        """验证配置参数"""
        required_fields = ['confluence_url', 'space_key', 'username', 'api_token', 'page_title']
        for field in required_fields:
            if not self.config.get(field):
                raise ValueError(f"缺少必需参数: {field}")

    async def setup_browser_and_auth(self):
        """初始化浏览器和认证"""
        self.logger.info("正在初始化浏览器...")

        playwright = await async_playwright().start()

        # 选择浏览器类型
        browser_type = getattr(playwright, self.config.get('browser', 'chromium'))
        self.browser = await browser_type.launch(
            headless=self.config.get('headless', True),
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        # 创建浏览器上下文
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        self.page = await self.context.new_page()

        # 设置页面超时
        self.page.set_default_timeout(self.config.get('timeout', 30000))

        self.logger.info("浏览器初始化完成")

    async def navigate_to_parent_page(self):
        """导航到父页面"""
        confluence_url = self.config['confluence_url'].rstrip('/')
        space_key = self.config['space_key']

        if self.config.get('parent_page_id'):
            # 导航到特定父页面
            parent_page_url = f"{confluence_url}/pages/{self.config['parent_page_id']}"
            self.logger.info(f"导航到父页面: {parent_page_url}")
            await self.page.goto(parent_page_url)
        else:
            # 导航到空间主页
            space_url = f"{confluence_url}/spaces/{space_key}/overview"
            self.logger.info(f"导航到空间主页: {space_url}")
            await self.page.goto(space_url)

        # 等待页面加载
        await self.page.wait_for_load_state('networkidle')

        # 检查是否需要登录
        if await self._need_login():
            await self._login()

    async def _need_login(self) -> bool:
        """检查是否需要登录"""
        try:
            # 检查是否存在登录表单
            await self.page.wait_for_selector('#username', timeout=5000)
            return True
        except:
            return False

    async def _login(self):
        """执行登录"""
        self.logger.info("正在执行登录...")

        # 输入用户名
        await self.page.fill('#username', self.config['username'])
        await self.page.click('#login-submit')

        # 等待密码输入框
        await self.page.wait_for_selector('#password')
        await self.page.fill('#password', self.config['api_token'])
        await self.page.click('#login-submit')

        # 等待登录完成
        await self.page.wait_for_load_state('networkidle')
        self.logger.info("登录完成")

    async def click_create_button(self):
        """点击创建按钮"""
        self.logger.info("正在查找创建按钮...")

        # 查找创建按钮（可能有多种选择器）
        create_selectors = [
            'button[aria-label="Create"]',
            'button[data-testid="create-page-button"]',
            '[data-testid="create-button"]',
            'a[href*="/create"]',
            '#create-page-button'
        ]

        create_button = None
        for selector in create_selectors:
            try:
                create_button = await self.page.wait_for_selector(selector, timeout=5000)
                if create_button:
                    break
            except:
                continue

        if not create_button:
            raise Exception("无法找到创建按钮")

        await create_button.click()
        self.logger.info("已点击创建按钮")

        # 等待创建页面加载
        await self.page.wait_for_load_state('networkidle')

    async def generate_page_content(self) -> Dict[str, str]:
        """生成页面内容"""
        self.logger.info("正在生成页面内容...")

        template_type = self.config.get('page_template', 'meeting-notes')
        page_title = self.config['page_title']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 根据模板类型生成内容
        content_templates = {
            'meeting-notes': f"""
# {page_title}

## 会议信息
- **时间**: {current_time}
- **地点**: [待填写]
- **参会人员**: [待填写]
- **主持人**: [待填写]

## 会议议程
1. [议题一]
2. [议题二]
3. [议题三]

## 讨论内容
### 议题一
- 讨论要点:
- 决定事项:
- 负责人:

### 议题二
- 讨论要点:
- 决定事项:
- 负责人:

## 行动项
| 事项 | 负责人 | 截止时间 | 状态 |
|------|--------|----------|------|
| [行动项1] | [姓名] | [日期] | 待处理 |
| [行动项2] | [姓名] | [日期] | 待处理 |

## 下次会议
- **时间**: [待确定]
- **议题**: [待确定]

---
*文档由自动化工具生成于 {current_time}*
            """.strip(),

            'project-update': f"""
# {page_title}

## 项目概览
- **项目名称**: {page_title}
- **更新时间**: {current_time}
- **报告人**: [待填写]

## 本期进展
### 完成的工作
- [完成项1]
- [完成项2]

### 遇到的问题
- [问题描述]
- [解决方案]

## 下期计划
- [计划项1]
- [计划项2]

## 资源需求
- 人力资源: [需求说明]
- 技术资源: [需求说明]

---
*项目更新报告 - {current_time}*
            """.strip(),

            'technical-doc': f"""
# {page_title}

## 概述
本文档描述了{page_title}的技术实现细节。

## 背景
[项目背景和需求说明]

## 技术架构
### 系统架构
```mermaid
graph TD
    A[用户接口] --> B[业务逻辑]
    B --> C[数据层]
```

### 关键组件
- **组件1**: [功能说明]
- **组件2**: [功能说明]

## 实现细节
### 核心算法
[算法描述和实现]

### 数据结构
[数据结构定义]

## API文档
### 接口列表
- `GET /api/endpoint1`: [接口说明]
- `POST /api/endpoint2`: [接口说明]

### 请求示例
```json
{{
  "param1": "value1",
  "param2": "value2"
}}
```

## 部署说明
### 环境要求
- Python 3.8+
- [其他依赖]

### 部署步骤
1. [步骤1]
2. [步骤2]

## 测试
### 测试用例
- [测试用例1]
- [测试用例2]

---
*技术文档 - 创建于 {current_time}*
            """.strip(),

            'custom': f"""
# {page_title}

## 内容区域
[请在此处添加您的内容]

---
*文档创建于 {current_time}*
            """.strip()
        }

        content = content_templates.get(template_type, content_templates['custom'])

        # 生成标签
        tags = self.config.get('tags', [])
        if template_type not in tags:
            tags.append(template_type)

        self.generated_content = {
            'title': page_title,
            'content': content,
            'tags': tags
        }

        self.logger.info("页面内容生成完成")
        return self.generated_content

    async def user_confirmation_step(self) -> bool:
        """用户确认和审核步骤"""
        print("\n" + "="*60)
        print("📋 生成的内容预览")
        print("="*60)
        print(f"\n📝 标题: {self.generated_content['title']}")
        print(f"\n🏷️  标签: {', '.join(self.generated_content['tags'])}")
        print(f"\n📄 内容预览:")
        print("-" * 40)

        # 显示内容前几行作为预览
        content_lines = self.generated_content['content'].split('\n')
        for i, line in enumerate(content_lines[:20]):
            print(f"{i+1:2d}: {line}")

        if len(content_lines) > 20:
            print(f"... (还有 {len(content_lines) - 20} 行)")

        print("-" * 40)

        # 用户确认
        while True:
            print("\n" + "="*60)
            response = input("❓ 是否确认使用此内容？(y/n/e): ").strip().lower()

            if response == 'y' or response == 'yes':
                print("✅ 用户确认，继续执行...")
                return True
            elif response == 'n' or response == 'no':
                print("❌ 用户取消，停止执行...")
                return False
            elif response == 'e' or response == 'edit':
                print("📝 编辑模式:")
                new_content = input("请输入新的内容 (支持多行，输入 'END' 结束):\n")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)

                if lines:
                    self.generated_content['content'] = '\n'.join(lines)
                    print("✅ 内容已更新，重新预览:")
                    continue  # 重新显示预览
                else:
                    print("⚠️  未输入有效内容，保持原内容")
                    continue
            else:
                print("⚠️  无效输入，请输入 y(确认)、n(取消) 或 e(编辑)")

    async def fill_page_content(self):
        """填写页面内容"""
        self.logger.info("正在填写页面内容...")

        # 等待标题输入框加载
        title_selectors = [
            'input[aria-label="Title"]',
            'input[data-testid="title-input"]',
            'input[name="title"]',
            '#title-field'
        ]

        title_input = None
        for selector in title_selectors:
            try:
                title_input = await self.page.wait_for_selector(selector, timeout=5000)
                if title_input:
                    break
            except:
                continue

        if not title_input:
            raise Exception("无法找到标题输入框")

        # 输入标题
        await title_input.fill(self.generated_content['title'])

        # 等待内容编辑器加载
        await asyncio.sleep(2)

        # 查找内容编辑器（Confluence使用富文本编辑器）
        content_selectors = [
            'div[contenteditable="true"]',
            '.ProseMirror',
            '[data-testid="editor-content"]',
            '.editor-content'
        ]

        content_editor = None
        for selector in content_selectors:
            try:
                content_editor = await self.page.wait_for_selector(selector, timeout=5000)
                if content_editor:
                    break
            except:
                continue

        if not content_editor:
            raise Exception("无法找到内容编辑器")

        # 清空现有内容并输入新内容
        await content_editor.click()
        await self.page.keyboard.press('Control+a')
        await self.page.keyboard.type(self.generated_content['content'])

        self.logger.info("页面内容填写完成")

    async def save_and_publish(self):
        """保存并发布页面"""
        self.logger.info("正在保存页面...")

        # 查找保存/发布按钮
        save_selectors = [
            'button[aria-label="Publish"]',
            'button[data-testid="publish-button"]',
            'button[type="submit"]',
            '#publish-button',
            '.publish-button'
        ]

        save_button = None
        for selector in save_selectors:
            try:
                save_button = await self.page.wait_for_selector(selector, timeout=5000)
                if save_button:
                    break
            except:
                continue

        if not save_button:
            raise Exception("无法找到发布按钮")

        await save_button.click()

        # 等待保存完成
        await self.page.wait_for_load_state('networkidle')

        self.logger.info("页面保存完成")

    async def cleanup_resources(self):
        """清理资源"""
        self.logger.info("正在清理资源...")

        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

        self.logger.info("资源清理完成")

    async def execute(self) -> Dict[str, Any]:
        """执行完整的页面创建流程"""
        result = {
            'success': False,
            'page_url': '',
            'page_id': '',
            'message': ''
        }

        try:
            # 执行工作流程
            await self.setup_browser_and_auth()
            await self.navigate_to_parent_page()
            await self.click_create_button()

            # 生成内容并获取用户确认
            await self.generate_page_content()
            confirmed = await self.user_confirmation_step()

            if not confirmed:
                result['message'] = '用户取消操作'
                return result

            await self.fill_page_content()
            await self.save_and_publish()

            # 获取页面URL和ID
            current_url = self.page.url
            result['page_url'] = current_url

            # 从URL中提取页面ID
            if '/pages/' in current_url:
                result['page_id'] = current_url.split('/pages/')[-1].split('/')[0]

            result['success'] = True
            result['message'] = '页面创建成功'

        except Exception as e:
            self.logger.error(f"执行过程中发生错误: {str(e)}")
            result['message'] = f'执行失败: {str(e)}'

        finally:
            await self.cleanup_resources()

        return result


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python main.py <config_file.yaml>")
        sys.exit(1)

    config_file = sys.argv[1]

    if not os.path.exists(config_file):
        print(f"配置文件不存在: {config_file}")
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        sys.exit(1)

    # 创建并执行技能
    creator = ConfluencePageCreator(config)
    result = await creator.execute()

    print("\n" + "="*60)
    print("🎉 执行结果")
    print("="*60)
    print(f"✅ 成功: {result['success']}")
    print(f"📝 消息: {result['message']}")

    if result['success']:
        print(f"🔗 页面URL: {result['page_url']}")
        if result['page_id']:
            print(f"🆔 页面ID: {result['page_id']}")

    print("="*60)

    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)