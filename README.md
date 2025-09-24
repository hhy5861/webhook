# Alertmanager → WeCom Webhook Relay

一个将 Alertmanager 告警转发到企业微信群机器人的 FastAPI 服务。

## 🚀 功能特性

- 📨 接收 Alertmanager webhook 告警
- 🎨 生成企业微信模板卡片格式
- 📊 详细的访问日志记录
- 🔧 模块化架构设计
- ⚡ 高性能异步处理

## 📋 项目结构

```
webhook/
├── main.py          # 应用入口点
├── routes.py        # API 路由定义
├── services.py      # 业务逻辑（卡片生成）
├── middleware.py    # 访问日志中间件
├── config.py        # 配置管理
├── requirements.txt # 依赖包
├── .gitignore       # Git 忽略文件
└── README.md        # 项目说明
```

## 🛠️ 安装部署

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd webhook
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 必需配置
export WECOM_WEBHOOK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# 可选配置
export HTTP_TIMEOUT="5"           # HTTP 请求超时时间（秒）
export AM_URL="http://alertmanager:9093"  # Alertmanager 地址
```

### 5. 启动服务
```bash
# 方式一：直接运行
python main.py

# 方式二：使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# 方式三：生产环境（多进程）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔧 配置说明

### 环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `WECOM_WEBHOOK` | ✅ | - | 企业微信群机器人 webhook URL |
| `HTTP_TIMEOUT` | ❌ | `5` | HTTP 请求超时时间（秒） |
| `AM_URL` | ❌ | - | Alertmanager 访问地址 |

### 企业微信群机器人配置

1. 在企业微信群中添加群机器人
2. 获取 webhook URL
3. 设置环境变量 `WECOM_WEBHOOK`

## 📡 API 接口

### POST `/hooks/alertmanager`

接收 Alertmanager webhook 并转发到企业微信。

**请求示例：**
```bash
curl -X POST "http://localhost:8000/hooks/alertmanager" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver": "webhook",
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "HighCPU",
          "instance": "server1:9100",
          "severity": "warning"
        },
        "annotations": {
          "summary": "High CPU usage detected",
          "description": "CPU usage is above 80%"
        },
        "startsAt": "2024-01-15T10:30:00Z",
        "generatorURL": "http://prometheus:9090/graph"
      }
    ]
  }'
```

**响应示例：**
```json
{
  "ok": true,
  "sent": 1
}
```

## 📊 日志记录

服务会自动记录详细的访问日志：

```
2024-01-15 10:30:45,123 - __main__ - INFO - POST /hooks/alertmanager - Status: 200 - Client: 192.168.1.100 - Time: 0.234s - Payload: 3 alerts
2024-01-15 10:30:45,125 - __main__ - INFO - Alertmanager payload: {
  "receiver": "webhook",
  "status": "firing",
  "alerts": [...]
}
```

## 🎨 企业微信卡片格式

生成的卡片包含以下信息：
- 📋 告警名称和描述
- 🚨 严重级别（critical/warning/info）
- 🖥️ 实例和环境信息
- ⏰ 告警状态和开始时间
- 🔗 跳转到 Alertmanager 的链接

## 🐳 Docker 部署

### 创建 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建和运行
```bash
docker build -t webhook-relay .
docker run -d -p 8000:8000 \
  -e WECOM_WEBHOOK="your_webhook_url" \
  webhook-relay
```

## 🔍 故障排查

### 常见问题

1. **企业微信发送失败**
   - 检查 `WECOM_WEBHOOK` 是否正确
   - 确认群机器人未被禁用

2. **服务启动失败**
   - 检查端口 8000 是否被占用
   - 确认所有依赖已正确安装

3. **告警未收到**
   - 检查 Alertmanager webhook 配置
   - 查看服务日志确认请求是否到达

### 日志级别

可以通过环境变量调整日志级别：
```bash
export LOG_LEVEL="DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 支持

如有问题，请提交 Issue 或联系维护者。
