# AI新闻自动化飞书集成 - 配置完成

恭喜！AI新闻自动化与飞书通知的集成框架已经搭建完成。以下是完整的配置和使用指南。

## 📦 已创建的文件

### 核心脚本
1. `src/feishu_notifier.py` - 飞书Webhook发送器
2. `src/ai_news_automation_with_feishu.py` - 集成飞书的完整自动化

### 配置文件
3. `feishu_config_template.json` - 配置文件模板
4. `feishu_config.json` - **请创建此文件并填入你的Webhook地址**

### 运行脚本
5. `run_ai_news_with_feishu.bat` - Windows运行脚本
6. `run_ai_news_with_feishu.sh` - Linux/macOS运行脚本

### 文档
7. `FEISHU_SETUP_GUIDE.md` - 详细设置指南
8. `AUTOMATION_SETUP_COMPLETE.md` - 本文件

## 🚀 快速开始

### 步骤1：创建配置文件
```bash
# 复制配置文件模板
cp feishu_config_template.json feishu_config.json

# 编辑配置文件，填入你的飞书Webhook地址
# 用文本编辑器打开 feishu_config.json
# 将 "YOUR_FEISHU_WEBHOOK_URL_HERE" 替换为你的实际URL
```

### 步骤2：运行自动化
```bash
# Windows
run_ai_news_with_feishu.bat

# Linux/macOS
chmod +x run_ai_news_with_feishu.sh
./run_ai_news_with_feishu.sh
```

### 步骤3：测试配置
```bash
# 测试模式运行（不实际发送飞书）
python src/ai_news_automation_with_feishu.py --test

# 强制发送测试（即使配置中未启用）
python src/ai_news_automation_with_feishu.py --force
```

## 🔧 配置说明

### 配置文件结构 (feishu_config.json)
```json
{
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx",
    "notify_enabled": true,
    "message_format": "post",
    "notify_time": "09:05",
    "notify_on_error": true,
    "max_retries": 3,
    "timeout_seconds": 10,
    "project_name": "AI新闻自动化"
}
```

### 参数说明
- `webhook_url`: **必需** - 飞书Webhook地址
- `notify_enabled`: 是否启用飞书通知（默认true）
- `notify_on_error`: 错误时是否发送通知（默认true）
- `max_retries`: 发送失败重试次数（默认3）
- `timeout_seconds`: API请求超时时间（默认10秒）

## 📊 自动化流程

### 完整流程
1. **收集AI新闻** → 生成报告文件
2. **创建飞书消息** → 格式化报告内容
3. **发送到飞书** → 调用Webhook API
4. **记录执行结果** → 生成执行摘要

### 执行目录结构
```
.codebuddy/automations/ai/
├── 2026-03-27_ai_news.md      # 每日AI新闻报告
├── errors/                    # 错误报告目录
├── summaries/                 # 执行摘要目录
└── memory.md                 # 自动化执行历史
```

### 日志文件
- `ai_news_automation.log` - 自动化执行日志
- 控制台实时输出

## 🔍 测试与验证

### 1. 配置文件验证
```bash
# 检查配置文件是否存在且格式正确
python -c "import json; json.load(open('feishu_config.json')); print('✅ 配置文件格式正确')"
```

### 2. 飞书连接测试
```bash
# 测试Webhook连接
python -c "
import requests
import json
config = json.load(open('feishu_config.json'))
url = config['webhook_url']
response = requests.post(url, json={'msg_type': 'text', 'content': {'text': '测试连接'}}, timeout=5)
print('✅ 飞书连接正常' if response.status_code == 200 else '❌ 连接失败')
"
```

### 3. 完整流程测试
```bash
# 运行完整测试（生成报告但不发送）
python src/ai_news_automation_with_feishu.py --test
```

## ⚙️ 集成到现有自动化

### 方案A：替换现有自动化
1. 将 `src/ai_news_automation_with_feishu.py` 作为主要自动化脚本
2. 配置定时任务调用此脚本

### 方案B：仅添加飞书发送
1. 保持现有AI新闻收集逻辑不变
2. 在收集完成后调用 `src/feishu_notifier.py`

### 方案C：CodeBuddy自动化更新
修改CodeBuddy的自动化任务描述，添加飞书发送步骤：
```
关注当天AI领域重要动态，侧重AI coding与具身智能方向。筛选3-5条有价值的信息，简要说明事件内容及值得关注的原因，并且要针对每条AI信息进行优化策略。完成报告后，通过飞书Webhook发送通知。
```

## 🚨 故障排除

### 常见问题

#### Q1: Webhook URL无效
```
错误：飞书返回错误: 无效的webhook地址
解决：检查URL是否正确，重新在飞书创建Webhook机器人
```

#### Q2: 网络连接失败
```
错误：网络连接失败
解决：检查网络连接，确认可以访问飞书API
```

#### Q3: 报告文件不存在
```
错误：报告文件不存在
解决：确保AI新闻收集任务正常运行并生成报告
```

#### Q4: 消息格式错误
```
错误：消息格式不符合飞书要求
解决：检查消息内容，确保不超过飞书限制
```

### 查看日志
```bash
# 查看自动化日志
tail -f ai_news_automation.log

# 查看详细的错误信息
python src/ai_news_automation_with_feishu.py 2>&1 | tee debug.log
```

### 手动调试
```bash
# 单独测试飞书发送
python src/feishu_notifier.py --webhook "你的Webhook_URL"

# 查看生成的报告
cat .codebuddy/automations/ai/最新报告文件.md
```

## 📈 监控与优化

### 监控指标
1. **执行成功率**：检查 `summaries/` 目录中的执行摘要
2. **发送延迟**：报告生成到飞书接收的时间差
3. **错误率**：查看 `errors/` 目录中的错误报告

### 优化建议
1. **调整发送时间**：避免高峰期，设置合理的重试策略
2. **优化消息格式**：根据团队需求定制消息内容
3. **添加多平台支持**：扩展支持钉钉、企业微信等
4. **实现分级通知**：重要消息实时通知，次要消息汇总通知

### 性能优化
```python
# 在配置文件中调整
{
    "batch_size": 5,           # 分批处理
    "concurrent_sends": 1,     # 并发发送数
    "cache_enabled": true,     # 启用缓存
    "compression": false       # 消息压缩
}
```

## 🔄 维护与更新

### 定期检查
- 每月检查Webhook有效性
- 更新依赖库版本
- 检查飞书API变更

### 备份策略
```bash
# 备份配置和报告
tar -czf ai_news_backup_$(date +%Y%m%d).tar.gz \
  feishu_config.json \
  .codebuddy/automations/ai/ \
  ai_news_automation.log
```

### 版本更新
当有新功能或修复时：
1. 备份当前配置
2. 更新脚本文件
3. 测试新功能
4. 更新文档

## 🆘 获取帮助

### 文档资源
1. 飞书开放平台：https://open.feishu.cn/
2. Webhook文档：https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
3. 消息格式：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot

### 技术支持
如遇问题，请提供：
1. 错误日志内容
2. 配置文件（隐藏敏感信息）
3. 飞书返回的错误信息
4. 操作系统和Python版本

---

## ✅ 配置完成清单

- [ ] 创建 `feishu_config.json` 并填入Webhook地址
- [ ] 测试飞书连接
- [ ] 运行完整自动化测试
- [ ] 配置定时任务（可选）
- [ ] 通知团队成员接收配置
- [ ] 设置监控告警（可选）

现在你可以开始享受自动化的AI新闻推送服务了！🎉