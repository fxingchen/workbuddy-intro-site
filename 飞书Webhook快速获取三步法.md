# 🚀 飞书Webhook快速获取三步法

## 第一步：进入群组并打开设置
1. **打开飞书**（App或网页版）
2. **进入**要接收AI新闻的群组
3. 点击群聊右上角 **「···」** 更多按钮
4. 选择 **「设置」**

## 第二步：添加Webhook机器人
1. 在设置中找到 **「群机器人」**
2. 点击 **「添加机器人」**
3. 在机器人列表中找到 **「Webhook」**
4. 点击 **「添加」**
5. 为机器人命名（如：`AI新闻助手`）
6. 点击 **「确认」**

## 第三步：复制Webhook地址
1. 添加成功后 **立即复制** 显示的Webhook地址
2. **地址格式**：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
3. **重要**：这个地址只显示一次，请立即复制！

## 📋 提供地址的方式

### 方式一：直接粘贴给我
将复制的完整Webhook地址**直接粘贴**在聊天窗口中给我。

### 方式二：自行配置
1. 用文本编辑器打开 `feishu_config.json`
2. 找到 `"webhook_url": ""` 这一行
3. 在引号内粘贴你的地址：
   ```json
   "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的实际令牌"
   ```

### 方式三：使用配置工具
运行：`python setup_feishu_config.py`，按提示输入地址。

## ⚠️ 重要注意事项

1. **权限检查**：需要是**群管理员**才能添加机器人
2. **立即复制**：Webhook地址只显示一次，务必立即复制
3. **地址格式**：必须是`https://`开头，包含`hook/`字样
4. **安全提醒**：Webhook地址**不要公开分享**

## 🔍 找不到选项怎么办？

### 常见问题解决
- **找不到「群机器人」**：可能需要群管理员权限
- **没有Webhook选项**：尝试使用**网页版飞书** https://www.feishu.cn
- **权限不足**：联系群主或管理员开通权限
- **企业版限制**：部分企业版需要管理员开启机器人功能

### 备用方案
如果无法获取Webhook地址：
1. 先查看本地AI新闻报告：`.codebuddy/automations/ai/2026-03-27_ai_news.md`
2. 稍后再配置飞书推送
3. 或使用其他通知方式

## 🎯 获取后立即测试

### 快速测试命令（替换你的地址）
```bash
# Windows PowerShell
curl -X POST -H "Content-Type: application/json" -d '{\"msg_type\":\"text\",\"content\":{\"text\":\"测试消息\"}}' "你的Webhook地址"

# 或使用Python测试
python -c "
import requests
url = '你的Webhook地址'
data = {'msg_type':'text','content':{'text':'AI新闻Webhook测试'}}
r = requests.post(url, json=data)
print('成功' if r.status_code == 200 else '失败')
"
```

## 📞 获取帮助

### 需要我协助的情况
- 找不到具体的菜单位置
- 遇到权限错误
- 不确定获取的地址是否正确
- 需要验证地址有效性

### 提供信息帮助诊断
- 截图或详细描述遇到的问题
- 飞书版本（桌面/移动/网页）
- 具体的错误提示
- 当前的操作步骤

---

## 🏁 现在就开始！

**建议操作顺序：**
1. ✅ **立即获取**：按三步法获取Webhook地址
2. ✅ **测试验证**：发送测试消息确认有效
3. ✅ **提供地址**：将地址给我配置
4. ✅ **补发新闻**：立即补发今日AI新闻

**预计时间**：3-5分钟即可完成获取！

**一句话总结**：打开飞书 → 群设置 → 添加Webhook机器人 → 复制地址 → 提供给我 → 立即补发AI新闻！