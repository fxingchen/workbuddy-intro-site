# 飞书通知集成设置指南

## 一、创建飞书Webhook机器人

### 步骤1：获取Webhook地址
1. 打开飞书，进入需要接收通知的群组
2. 点击群组右上角的`设置`图标
3. 选择`群机器人` → `添加机器人`
4. 找到`Webhook`机器人，点击`添加`
5. 为机器人命名（如"AI新闻助手"）
6. 复制生成的Webhook URL（格式如：`https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx`）

### 步骤2：配置通知内容
1. 机器人支持的消息类型：
   - 文本消息
   - 富文本消息
   - 卡片消息
   - 文件消息
2. 建议保持默认权限设置

## 二、配置AI新闻自动化

### 步骤1：创建配置文件
1. 复制 `feishu_config_template.json` 为 `feishu_config.json`
2. 用你的Webhook URL替换 `YOUR_FEISHU_WEBHOOK_URL_HERE`

```bash
cp feishu_config_template.json feishu_config.json
```

### 步骤2：编辑配置文件
```json
{
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的实际webhook令牌",
    "notify_enabled": true,
    "message_format": "post",
    "notify_time": "09:05",
    "notify_on_error": true,
    "max_retries": 3,
    "timeout_seconds": 10
}
```

## 三、测试飞书通知

### 手动测试
```bash
# 使用最新报告测试
python src/feishu_notifier.py

# 指定报告文件测试
python src/feishu_notifier.py --report .codebuddy/automations/ai/2026-03-27_ai_news.md

# 直接指定Webhook URL测试
python src/feishu_notifier.py --webhook "你的Webhook_URL"
```

### 预期结果
成功发送后，飞书群组将收到类似消息：
```
📊 AI新闻推送 - 2026年03月27日

🌟 AI新闻推送 - 2026年3月27日

🔍 今日核心洞察：
### 一、全球首届具身智能开发者大会今日深圳启幕
**事件内容**：全球首届具身智能开发者大会（EAIDC 2026）今日在深圳正式开幕...

📁 完整报告已生成：.codebuddy/automations/ai/2026-03-27_ai_news.md

⏰ 发送时间：2026-03-27 09:05:00
```

## 四、自动化集成方案

### 方案A：直接修改现有自动化（推荐）
创建集成脚本 `src/ai_news_with_feishu.py`：

```python
#!/usr/bin/env python3
# 1. 执行AI新闻搜集
# 2. 生成报告
# 3. 发送到飞书
```

### 方案B：定时任务调用
使用系统的定时任务（cron/计划任务）：
```
# 每天9:05执行
5 9 * * * cd /path/to/project && python src/feishu_notifier.py
```

### 方案C：CodeBuddy自动化扩展
修改现有AI新闻自动化的任务描述，添加飞书发送步骤。

## 五、故障排除

### 常见问题1：Webhook无效
- 检查URL是否正确复制
- 确认机器人是否已添加到群组
- 尝试重新创建Webhook机器人

### 常见问题2：消息发送失败
- 检查网络连接
- 确认飞书API服务状态
- 查看脚本日志输出

### 常见问题3：消息格式问题
- 检查报告文件编码（应为UTF-8）
- 确保报告文件路径正确
- 验证消息内容长度（飞书有限制）

## 六、高级配置

### 自定义消息模板
修改 `src/feishu_notifier.py` 中的 `create_ai_news_message` 函数来自定义消息格式。

### 多群组通知
创建多个配置文件，分别对应不同的飞书群组：
```bash
feishu_config_dev.json    # 开发群组
feishu_config_team.json   # 团队群组
feishu_config_leader.json # 领导群组
```

### 错误通知
启用 `notify_on_error` 后，当AI新闻搜集失败时会发送错误通知。

## 七、安全注意事项

1. **保护Webhook URL**：不要将配置文件提交到公开仓库
2. **限制机器人权限**：仅授予必要的权限
3. **定期更新配置**：定期检查Webhook有效性
4. **监控发送状态**：设置发送失败告警

## 八、后续优化建议

1. **添加发送统计**：记录每次发送的时间、状态和接收人
2. **支持多种消息格式**：除了富文本，支持卡片、文件等多种格式
3. **实现失败重试机制**：网络异常时自动重试
4. **添加发送确认**：要求接收人确认收到消息
5. **集成其他平台**：扩展支持钉钉、企业微信等平台

---

如有问题，请查看脚本日志或联系系统管理员。