# 📱 飞书Webhook地址获取详细指南

## 🎯 获取飞书Webhook地址 - 完整步骤

### 第一步：打开飞书并进入群组
1. **打开飞书App** 或 **飞书网页版** (feishu.cn)
2. **进入你要接收AI新闻的群组**
   - 可以是现有群组，也可以新建一个群组
   - 建议命名为 "AI新闻播报" 或类似名称

### 第二步：进入群设置添加机器人
**桌面端操作：**
```
群聊窗口 → 右上角「...」更多 → 设置 → 群机器人 → 添加机器人
```

**移动端操作：**
```
群聊窗口 → 右上角「...」 → 群设置 → 群机器人 → 添加机器人
```

### 第三步：选择Webhook机器人
在机器人列表中：
1. 找到 **「Webhook」** 机器人
2. 点击 **「添加」** 按钮
3. 为机器人命名（建议：`AI新闻助手`）
4. 点击 **「确认」** 或 **「完成」**

### 第四步：复制Webhook URL
添加成功后，你会看到：
```
Webhook 地址：
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**重要**：立即复制这个URL，它只会显示一次！

### 第五步：验证Webhook有效性（可选）
复制URL后，可以立即测试：
1. 使用浏览器访问这个URL（会显示Webhook信息）
2. 或使用工具发送测试消息

## 📋 Webhook地址格式说明

### 标准格式
```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 组成部分
1. **协议**：`https://`
2. **域名**：`open.feishu.cn`
3. **路径**：`/open-apis/bot/v2/hook/`
4. **令牌**：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (你的唯一标识)

### 注意要点
✅ **必须以https开头**  
✅ **包含hook字样**  
✅ **最后是唯一令牌字符串**  
✅ **长度约70-80字符**  
❌ **不要泄露给他人**（可以给我，但不要公开）

## 🔧 获取地址后的操作

### 方案A：直接提供给我（推荐）
将复制的Webhook地址**完整粘贴**给我，我帮你：
1. 配置到 `feishu_config.json`
2. 测试发送验证
3. 执行今日AI新闻补发

### 方案B：自行配置
1. 编辑 `feishu_config.json` 文件
2. 将地址填入 `"webhook_url": "你的地址"`
3. 运行测试命令

### 示例配置文件
```json
{
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的实际令牌",
    "notify_enabled": true,
    "message_format": "post",
    "notify_time": "立即",
    "notify_on_error": true,
    "max_retries": 3,
    "timeout_seconds": 10,
    "project_name": "AI新闻自动化"
}
```

## 🎯 常见问题解答

### Q1: 找不到群机器人选项？
- 确认你是**群管理员**或**有相应权限**
- 某些企业版飞书可能需要管理员开启机器人功能
- 尝试使用网页版飞书：https://www.feishu.cn

### Q2: Webhook地址丢失了怎么办？
重新添加Webhook机器人会生成**新的地址**，旧的会失效。

### Q3: 可以多个群组接收吗？
可以！为每个群组创建独立的Webhook机器人，获取不同的地址。

### Q4: Webhook地址安全吗？
- **相对安全**：只能发送消息到指定群组
- **建议**：不要公开分享，使用后可以随时删除机器人
- **权限**：Webhook机器人只有发送消息权限，无法读取群消息

### Q5: 如何测试Webhook是否有效？
使用这个快速测试命令（将URL替换为你的）：
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"msg_type":"text","content":{"text":"测试消息"}}' \
"你的Webhook地址"
```

## 📝 获取地址的图文指引

### 步骤图示（文字描述）
```
1. [飞书主界面] → 选择群组
2. [群聊窗口] → 右上角「···」→ 设置
3. [群设置] → 群机器人 → 添加机器人
4. [机器人列表] → 找到「Webhook」→ 添加
5. [机器人配置] → 命名 → 确认
6. [成功页面] → 复制Webhook地址
```

### 关键位置提示
- **群机器人**通常在群设置的**高级功能**或**管理工具**中
- **Webhook机器人**在自定义机器人分类中
- 添加后**立即复制地址**，页面关闭后无法再次查看

## 🚀 立即操作建议

### 时间预估
- **熟悉操作**：3-5分钟
- **实际获取**：2-3分钟
- **测试验证**：1-2分钟
- **总计**：6-10分钟

### 最佳实践
1. **新建专门群组**：用于接收AI新闻，便于管理
2. **立即测试**：获取地址后立即发送测试消息
3. **备份地址**：保存到安全位置（如笔记应用）
4. **权限检查**：确保有添加机器人的权限

### 备用方案
如果无法获取Webhook地址：
1. **联系飞书管理员**：请求开启机器人权限
2. **使用其他群组**：使用已有机器人权限的群组
3. **测试模式**：先使用本地测试，稍后再配置飞书

## 🔍 验证Webhook是否成功

### 成功标志
1. **添加机器人成功**：群组中出现Webhook机器人
2. **获得有效URL**：格式正确的Webhook地址
3. **发送测试消息**：能接收到测试消息

### 测试方法
```python
# 使用Python测试（替换YOUR_WEBHOOK_URL）
import requests
import json

webhook_url = "你的Webhook地址"
test_message = {
    "msg_type": "text",
    "content": {
        "text": "🔧 AI新闻Webhook测试\n\n这是一条测试消息，用于验证Webhook配置是否正确。"
    }
}

response = requests.post(webhook_url, json=test_message)
if response.status_code == 200:
    print("✅ Webhook测试成功！")
else:
    print("❌ Webhook测试失败")
```

## 📞 技术支持

### 如遇问题
1. **截图或描述**：遇到的具体问题和界面
2. **飞书版本**：桌面版/移动版/网页版
3. **错误信息**：具体的错误提示
4. **权限状态**：是否是群管理员

### 快速帮助
我可以：
- 指导你找到具体的菜单位置
- 解决权限相关问题
- 验证获取的Webhook地址格式
- 测试地址是否有效

---

## 🏁 最终操作

**现在请按以下步骤操作：**

1. **打开飞书** → 进入目标群组
2. **群设置** → 群机器人 → 添加机器人
3. **选择Webhook** → 添加 → 命名 → 确认
4. **立即复制**显示的全部Webhook地址
5. **将地址提供给我**或自行配置

**一旦获得地址，我立即为你补发今日AI新闻！**