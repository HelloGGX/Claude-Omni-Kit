# Confluence页面创建自动化技能

使用Playwright自动化在Confluence平台创建文档页面的Python技能，支持多种模板和用户交互确认。

## 功能特性

- 🚀 **自动化页面创建**: 使用Playwright自动操作Web界面
- 📝 **智能内容生成**: 支持会议纪要、项目更新、技术文档等多种模板
- ✅ **用户确认机制**: 生成内容后提供预览和编辑确认
- 🏷️  **标签管理**: 自动为页面添加相关标签
- 🔧 **灵活配置**: 支持多种浏览器和自定义配置
- 📊 **详细日志**: 完整的操作日志记录

## 安装依赖

```bash
pip install -r requirements.txt
playwright install  # 安装浏览器驱动
```

## 配置说明

1. 复制配置模板：
```bash
cp config-example.yaml config.yaml
```

2. 编辑 `config.yaml` 文件：
```yaml
confluence_url: "https://your-company.atlassian.net/wiki"
space_key: "YOUR_SPACE"
username: "your-email@company.com"
api_token: "your-api-token"
page_title: "会议纪要 - 2024-01-15"
page_template: "meeting-notes"
```

## 使用方法

### 基本使用

```bash
python main.py config.yaml
```

### 支持的模板类型

- `meeting-notes`: 会议纪要模板
- `project-update`: 项目更新报告
- `technical-doc`: 技术文档
- `custom`: 自定义模板

### 用户交互选项

执行过程中会显示内容预览，支持以下操作：
- **y/yes**: 确认使用生成的内容
- **n/no**: 取消操作
- **e/edit**: 编辑内容（支持多行输入，输入'END'结束）

## 配置参数详解

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `confluence_url` | string | ✅ | Confluence服务器地址 | `https://company.atlassian.net/wiki` |
| `space_key` | string | ✅ | 空间键 | `DEV` |
| `parent_page_id` | string | ❌ | 父页面ID | `123456` |
| `username` | string | ✅ | 用户名 | `user@company.com` |
| `api_token` | string | ✅ | API令牌 | `ATATT3xFfGF0...` |
| `page_title` | string | ✅ | 页面标题 | `会议纪要 - 2024-01-15` |
| `page_template` | string | ❌ | 模板类型 | `meeting-notes` |
| `tags` | array | ❌ | 页面标签 | `["会议", "纪要"]` |
| `browser` | string | ❌ | 浏览器类型 | `chromium` |
| `headless` | boolean | ❌ | 无头模式 | `false` |
| `timeout` | integer | ❌ | 超时时间(ms) | `30000` |

## API令牌获取

1. 访问 [Atlassian账户设置](https://id.atlassian.com/manage-profile/security/api-tokens)
2. 点击"Create API token"
3. 输入标签名称并复制生成的令牌
4. 将令牌添加到配置文件的 `api_token` 字段

## 工作流程

1. **初始化**: 启动浏览器并建立认证
2. **导航**: 打开指定的Confluence页面
3. **创建**: 点击创建按钮进入编辑模式
4. **生成**: 根据模板生成页面内容
5. **确认**: 显示预览，等待用户确认或编辑
6. **填写**: 将内容填入页面编辑器
7. **保存**: 保存并发布页面
8. **清理**: 关闭浏览器，释放资源

## 错误处理

技能包含完善的错误处理机制：

- ✅ **配置验证**: 启动时验证必需参数
- ✅ **元素等待**: 智能等待页面元素加载
- ✅ **多选择器支持**: 尝试多种可能的元素选择器
- ✅ **详细日志**: 记录每个步骤的执行状态
- ✅ **资源清理**: 确保浏览器资源正确释放

## 日志输出

```
2024-01-15 10:30:00 - INFO - 正在初始化浏览器...
2024-01-15 10:30:05 - INFO - 浏览器初始化完成
2024-01-15 10:30:05 - INFO - 正在执行登录...
2024-01-15 10:30:08 - INFO - 登录完成
2024-01-15 10:30:08 - INFO - 正在查找创建按钮...
2024-01-15 10:30:09 - INFO - 已点击创建按钮
2024-01-15 10:30:10 - INFO - 页面内容生成完成
2024-01-15 10:30:15 - INFO - 页面内容填写完成
2024-01-15 10:30:20 - INFO - 页面保存完成
```

## 故障排除

### 常见问题

**Q: 找不到创建按钮**
A: 检查用户权限，确保有页面创建权限

**Q: 登录失败**
A: 验证用户名和API令牌是否正确

**Q: 内容编辑器无法找到**
A: 确保页面完全加载，可适当增加timeout时间

**Q: 浏览器启动失败**
A: 运行 `playwright install` 安装浏览器驱动

### 调试建议

1. 首次使用时设置 `headless: false` 观察操作过程
2. 增加 `timeout` 值应对网络延迟
3. 检查浏览器控制台是否有JavaScript错误

## 扩展开发

### 添加新模板

在 `generate_page_content()` 方法的 `content_templates` 字典中添加新模板：

```python
'new-template': f"""
# {page_title}

## 模板内容
[添加您的模板内容]
""".strip()
```

### 自定义选择器

如需适配不同版本的Confluence，可在相应方法中添加新的选择器：

```python
# 示例：添加新的创建按钮选择器
create_selectors = [
    'button[aria-label="Create"]',
    'button[data-testid="create-page-button"]',
    '.your-custom-selector'  # 添加自定义选择器
]
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个技能！