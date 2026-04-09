# 小红书自动维护工具

每天定时从本地图片库读取 5-6 张图片，通过 AI 生成配文，自动发布到小红书。

## 功能特性

- 定时自动发布（每天早上 8:00）
- 随机从图片库选取 5-6 张图片
- AI 生成小红书风格配文（标题 + 正文 + 标签）
- Selenium 浏览器自动化发布

## 环境要求

- Python 3.10+
- Google Chrome 浏览器
- ChromeDriver（与 Chrome 版本匹配）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.py`：

```python
# 图片库目录
IMAGE_DIR = r"C:\Users\<用户名>\Images"  # 修改为你的图片目录

# 通义千问 API 配置
QWEN_API_KEY = "your-api-key-here"

# 定时发布时间（每天）
SCHEDULE_HOUR = 8
SCHEDULE_MINUTE = 0
```

### 获取通义千问 API Key

1. 访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 在控制台获取 API Key

### ChromeDriver 安装

1. 确认 Chrome 版本：`chrome://version`
2. 下载对应版本：https://chromedriver.chromium.org/downloads
3. 将 chromedriver 放到项目目录或系统 PATH 中

## 使用

### 首次运行（登录）

```bash
python main.py --login
```

首次运行会打开浏览器窗口，需要扫码登录小红书。登录成功后 Cookie 会自动保存。

### 启动定时任务

```bash
python main.py
```

程序将每天早上 8:00 自动执行发布任务。

### 手动发布测试

```bash
python main.py --publish-now
```

## 项目结构

```
.
├── config.py           # 配置文件
├── image_picker.py     # 图片采集模块
├── ai_writer.py        # AI 生成配文
├── xhs_publisher.py    # 小红书发布模块
├── scheduler.py        # 定时调度
├── main.py             # 主入口
├── requirements.txt    # 依赖
├── cookies.json        # 登录 Cookie（自动生成）
└── xhs.log            # 运行日志
```

## 依赖

```
selenium
apscheduler
openai
pillow
requests
```

## 注意事项

1. 首次使用需扫码登录，建议先手动发布测试
2. 发布间隔不要太频繁，避免账号风险
3. 确保图片格式正确（jpg/png，单张不超过 10MB）
4. AI 生成的配文建议人工审核后再正式使用

## 常见问题

### 登录失败
- 确保 ChromeDriver 版本与 Chrome 匹配
- 检查网络连接

### 发布失败
- 检查是否已成功登录
- 查看日志输出具体错误信息

### API 调用失败
- 确认 API Key 正确
- 检查 API 配额是否用尽

## License

MIT
