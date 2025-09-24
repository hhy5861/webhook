# Alertmanager → WeCom Webhook Relay

一个将 Alertmanager 告警转发到企业微信的 FastAPI webhook 服务。

## 功能特性

- 接收 Alertmanager webhook 告警
- 将告警转换为企业微信模板卡片格式
- 详细的访问日志记录
- 模块化架构设计

## 项目结构

```
webhook/
├── main.py          # 应用入口点
├── routes.py        # API 路由定义
├── services.py      # 业务逻辑（WeCom 卡片生成）
├── middleware.py    # 访问日志中间件
├── config.py        # 配置管理
├── requirements.txt # Python 依赖
└── README.md        # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置环境变量

```bash
export WECOM_WEBHOOK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
export HTTP_TIMEOUT="5"  # 可选，默认 5 秒
export AM_URL="http://your-alertmanager-url"  # 可选，用于生成链接
```

### 3. 运行服务

**方式一：直接运行**
```bash
python main.py
```

**方式二：使用 uvicorn**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API 接口

### POST /hooks/alertmanager

接收 Alertmanager webhook 并转发到企业微信。

**请求体示例：**
```json
{
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
      "generatorURL": "http://alertmanager:9093/graph"
    }
  ]
}
```

**响应示例：**
```json
{
  "ok": true,
  "sent": 1
}
```

## 日志

服务会记录详细的访问日志，包括：

- 请求方法、路径、状态码
- 客户端 IP 地址
- 处理时间
- 告警数量
- 详细的 payload 内容（用于调试）

## 企业微信卡片格式

生成的卡片包含以下信息：

- 告警名称和描述
- 严重级别
- 实例和环境信息
- 告警状态和开始时间
- 跳转到 Alertmanager 的链接

## 错误处理

- 如果 `WECOM_WEBHOOK` 环境变量未设置，返回 500 错误
- 如果企业微信 API 返回错误，返回 502 错误
- 所有错误都会记录到日志中

## 部署

### 使用 systemd 服务

创建 `/etc/systemd/system/webhook.service`：

```ini
[Unit]
Description=WebHook for Alertmanager
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/webhook
Environment=WECOM_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY
ExecStart=/path/to/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable webhook.service
sudo systemctl start webhook.service
```

查看日志：
```bash
sudo journalctl -u webhook.service -f
```

## 开发

### 添加新的告警类型

在 `services.py` 中添加新的卡片生成函数，然后在 `routes.py` 中调用。

### 自定义中间件

在 `middleware.py` 中修改 `AccessLogMiddleware` 类来添加更多功能。

## 许可证

MIT License
