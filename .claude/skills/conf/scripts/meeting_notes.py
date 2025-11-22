import yaml
import os
import sys
from playwright.sync_api import sync_playwright
from datetime import datetime


def load_config():
    """加载配置文件"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_meeting_notes_content(meeting_info):
    """生成会议纪要内容"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    template = f"""# {meeting_info.get('title', '会议纪要')}

## 会议基本信息
- **会议主题**: {meeting_info.get('title', '未指定主题')}
- **会议时间**: {meeting_info.get('date', current_date)} {meeting_info.get('time', '未指定时间')}
- **会议地点**: {meeting_info.get('location', '未指定地点')}
- **主持人**: {meeting_info.get('host', '未指定主持人')}
- **参会人员**: {meeting_info.get('attendees', '未指定参会人员')}
- **记录人**: {meeting_info.get('recorder', '未指定记录人')}

## 会议议程
{meeting_info.get('agenda', '1. 开场介绍\n2. 主要议题讨论\n3. 行动项确定\n4. 下次会议安排')}

## 主要讨论内容
{meeting_info.get('discussion', '请在此处添加主要讨论内容...')}

## 决策事项
{meeting_info.get('decisions', '请在此处添加决策事项...')}

## 行动项目
| 负责人 | 任务内容 | 截止日期 | 状态 |
|--------|----------|----------|------|
| 待定 | 待确定 | 待定 | 进行中 |

## 下次会议安排
- **时间**: {meeting_info.get('next_meeting_date', '待定')}
- **地点**: {meeting_info.get('next_meeting_location', '待定')}
- **主要议题**: {meeting_info.get('next_meeting_topics', '待定')}

## 附件
- [相关文档1](链接)
- [相关文档2](链接)

---
*纪要创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return template


def login_if_required(page, config):
    """如果需要，执行登录"""
    if not config.get('login_required', False):
        return True

    try:
        # 等待登录表单加载
        page.wait_for_selector(config['login']['username_selector'], timeout=10000)

        # 输入用户名
        page.fill(config['login']['username_selector'],
                os.environ.get('CONF_USERNAME', config['login']['username']))

        # 输入密码
        page.fill(config['login']['password_selector'],
                os.environ.get('CONF_PASSWORD', config['login']['password']))

        # 点击登录按钮
        page.click(config['login']['submit_button'])

        # 等待登录完成
        page.wait_for_load_state('networkidle')
        print("登录成功")
        return True

    except Exception as e:
        print(f"登录失败: {e}")
        return False


async def create_meeting_notes(meeting_info):
    """创建会议纪要的主函数"""
    config = load_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 导航到Confluence
            page.goto(config['target_url'])
            print(f"已导航到: {page.title()}")

            # 登录（如果需要）
            if not login_if_required(page, config):
                return False

            # 点击创建页面按钮
            page.wait_for_selector(config['create_button_selector'], timeout=10000)
            page.click(config['create_button_selector'])

            # 等待页面创建表单加载
            page.wait_for_selector(config['form_fields']['title'], timeout=10000)

            # 填写页面标题
            page_title = meeting_info.get('title', '会议纪要')
            page.fill(config['form_fields']['title'], page_title)

            # 生成会议纪要内容
            content = generate_meeting_notes_content(meeting_info)

            # 填写页面内容
            page.wait_for_selector(config['form_fields']['body'], timeout=10000)
            page.fill(config['form_fields']['body'], content)

            # 保存页面
            page.wait_for_selector(config['save_button_selector'], timeout=10000)
            page.click(config['save_button_selector'])

            # 等待保存完成
            page.wait_for_load_state('networkidle')

            current_url = page.url
            print(f"会议纪要创建成功!")
            print(f"页面链接: {current_url}")

            return True

        except Exception as e:
            print(f"创建会议纪要时出错: {e}")
            return False

        finally:
            browser.close()


def parse_meeting_input(user_input):
    """解析用户输入，提取会议信息"""
    meeting_info = {
        'title': '会议纪要',
        'date': datetime.now().strftime("%Y-%m-%d"),
        'time': '14:00',
        'location': '会议室A',
        'host': '待定',
        'attendees': '待定',
        'recorder': '待定',
        'agenda': '',
        'discussion': '',
        'decisions': ''
    }

    # 简单的关键词解析逻辑
    if '主题' in user_input or 'title' in user_input.lower():
        # 提取主题信息
        pass

    if '时间' in user_input or 'time' in user_input.lower():
        # 提取时间信息
        pass

    if '地点' in user_input or 'location' in user_input.lower():
        # 提取地点信息
        pass

    return meeting_info


async def main(user_input="创建会议纪要"):
    """主入口函数"""
    print("开始创建会议纪要...")

    # 解析用户输入
    meeting_info = parse_meeting_input(user_input)

    # 如果需要，向用户确认信息
    print("会议信息:")
    print(f"- 主题: {meeting_info['title']}")
    print(f"- 日期: {meeting_info['date']}")
    print(f"- 时间: {meeting_info['time']}")

    confirm = input("确认创建会议纪要? (y/n): ").lower().strip()
    if confirm != 'y':
        print("操作已取消")
        return False

    # 创建会议纪要
    result = await create_meeting_notes(meeting_info)
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())