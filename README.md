# WorkBuddy 介绍网站

现代化的WorkBuddy产品介绍网站，包含丰富的动画效果、交互功能和多语言支持。

## ✨ 特性

### 🎨 动画效果
- 粒子背景动画
- 滑入/淡入效果
- 数字计数动画
- 渐变文字动画
- 3D卡片悬停效果
- 波纹按钮效果
- 打字机效果
- 进度条动画

### 🖱️ 交互功能
- 平滑滚动导航
- 响应式导航栏
- 移动端汉堡菜单
- FAQ手风琴展开
- 联系表单验证
- Toast通知提示
- 悬停动画反馈
- 滚动视差效果

### 🔍 SEO优化
- 完整的meta标签
- Open Graph标签
- Twitter Card标签
- 结构化数据（JSON-LD）
- 规范化URL
- 语义化HTML标签

### 🌐 多语言支持
- 中文/英文切换
- 本地存储语言偏好
- 完整的翻译字典
- 自动加载用户语言

### 📱 响应式设计
- 移动端优化
- 平板适配
- 桌面端完整展示
- Touch友好交互

## 🚀 快速开始

### 本地预览

1. 直接在浏览器中打开 `workbuddy-intro.html`
2. 或使用Live Server（推荐）：
   ```bash
   # 使用Node.js Live Server
   npx live-server
   ```

### 部署到GitHub Pages

1. 创建GitHub仓库
2. 推送代码：
   ```bash
   git init
   git add workbuddy-intro.html
   git commit -m "初始提交"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/workbuddy-intro.git
   git push -u origin main
   ```

3. 启用GitHub Pages：
   - 进入仓库 Settings > Pages
   - Source选择 `Deploy from a branch`
   - Branch选择 `main`，目录选择 `/ (root)`
   - 点击Save

4. 访问：`https://YOUR_USERNAME.github.io/workbuddy-intro/`

### 部署到Vercel

```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel
```

### 部署到Netlify

1. 拖拽文件夹到Netlify
2. 或使用CLI：
   ```bash
   npm i -g netlify-cli
   netlify deploy --prod
   ```

## 📁 项目结构

```
.
├── workbuddy-intro.html    # 主网站文件
└── README.md               # 项目说明
```

## 🎯 功能模块

### 1. 导航栏
- 固定顶部
- 毛玻璃效果
- 滚动自动隐藏/显示
- 移动端汉堡菜单
- 平滑滚动

### 2. Hero区域
- 渐变背景
- 粒子动画
- 数字计数
- 打字机效果
- CTA按钮

### 3. 核心功能
- 6大功能卡片
- 3D悬停效果
- 滚动触发动画
- 图标旋转动画

### 4. 使用演示
- 真实场景展示
- 进度条动画
- 实时状态显示

### 5. 产品对比
- 对比表格
- 清晰的差异展示

### 6. 常见问题
- 手风琴展开
- 图标旋转动画
- 平滑过渡

### 7. 联系表单
- 表单验证
- 提交动画
- 成功提示
- Toast通知

### 8. 页脚
- 导航链接
- 社交媒体
- 版权信息

## 🛠️ 技术栈

- **HTML5** - 语义化标签
- **CSS3** - 动画、Flexbox、Grid
- **Tailwind CSS** - 实用类样式（CDN）
- **JavaScript** - 交互逻辑
- **Intersection Observer API** - 滚动动画
- **LocalStorage** - 语言偏好存储

## 🎨 自定义

### 修改颜色主题

搜索并替换颜色变量：
```css
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 添加新语言

在 `translations` 对象中添加新语言：
```javascript
const translations = {
    zh: { ... },
    en: { ... },
    ja: { /* 添加日语翻译 */ }
};
```

### 修改动画速度

调整动画时长：
```css
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

.feature-card {
    transition: opacity 0.6s, transform 0.6s; /* 调整速度 */
}
```

## 📊 性能优化

- CDN加载Tailwind CSS
- 懒加载图片（如需要）
- Debounce滚动事件
- Intersection Observer优化
- CSS动画优先于JS动画

## 🔧 浏览器兼容性

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- 移动端浏览器（iOS Safari, Chrome Mobile）

## 📝 待办事项

- [ ] 添加图片懒加载
- [ ] 添加更多语言（日语、韩语等）
- [ ] 集成Google Analytics
- [ ] 添加暗色模式切换
- [ ] 添加PWA支持
- [ ] 优化首屏加载速度
- [ ] 添加更多动画效果

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- WorkBuddy官网：https://workbuddycn.com
- B站：https://space.bilibili.com/1619549806
- 邮箱：contact@workbuddycn.com

---

**Powered by 腾讯云** © 2026 WorkBuddy
