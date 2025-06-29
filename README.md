# Discord Bump Bot

一个简单的Discord机器人，用于监听特定频道的关键词并回复带按钮的嵌入消息。

## 功能特性

- 🔍 监听指定频道的消息
- 🎯 完全匹配关键词检测
- 🔐 角色权限验证
- 📱 嵌入消息 + 链接按钮回复
- ⚙️ JSON配置文件管理
- 🔄 热重载配置（`/reload`命令）

## 快速开始

### 1. 安装依赖
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者 fish shell用户使用: source venv/bin/activate.fish
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
```
编辑`.env`文件，填入你的配置：
- `DISCORD_TOKEN`: 机器人token
- `MONITOR_CHANNEL_IDS`: 监听的频道ID数组
- `REQUIRED_ROLE_IDS`: 必需的角色ID数组  
- `ADMIN_USER_IDS`: 管理员用户ID数组

### 3. 配置关键词
```bash
cp config-example.json config.json
```
编辑`config.json`文件，设置触发关键词和回复内容。

### 4. 运行机器人
```bash
python bot.py
```

## 配置说明

### 环境变量
所有ID都使用JSON数组格式，例如：`["123456789", "987654321"]`

### 关键词配置
`config.json`支持多个关键词配置，每个包含：
- `trigger`: 触发关键词（完全匹配）
- `response`: 回复内容
  - `embed`: 嵌入消息内容
  - `buttons`: 链接按钮数组

### 机器人权限
需要在Discord服务器中给机器人以下权限：
- Send Messages
- Read Message History  
- Use Slash Commands
- Embed Links

需要在Discord开发者门户开启：
- Message Content Intent

## 命令

- `/reload` - 重新加载配置文件（仅管理员可用）

## 文件结构

```
discord-bump-bot/
├── bot.py              # 主程序
├── config.json         # 关键词配置
├── .env.example        # 环境变量示例
├── requirements.txt    # 依赖包
└── README.md          # 说明文档
```