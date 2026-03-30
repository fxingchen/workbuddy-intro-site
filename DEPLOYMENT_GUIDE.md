# WorkBuddy网站部署指南

## 📦 准备工作

### 1. 创建GitHub仓库

访问 https://github.com/new 创建新仓库：
- **仓库名称**：`workbuddy-intro`（或自定义）
- **可见性**：Public（公开）
- **初始化**：可以不勾选，或勾选"Add a README file"

### 2. 获取仓库地址

创建后，复制你的仓库地址，例如：
```
https://github.com/你的用户名/workbuddy-intro.git
```

## 🚀 方法一：使用自动部署脚本（推荐）

### Windows用户
```bash
# 双击运行
deploy.bat
```

### Linux/Mac用户
```bash
# 添加执行权限
chmod +x deploy.sh

# 运行
./deploy.sh
```

脚本会自动：
1. 配置Git远程仓库（首次运行）
2. 添加所有文件
3. 提交更改
4. 推送到GitHub

## 🚀 方法二：手动部署

### 1. 初始化Git仓库
```bash
cd "c:\Users\starry sky\CodeBuddy\Claw"
git init
```

### 2. 添加远程仓库
```bash
git remote add origin https://github.com/你的用户名/workbuddy-intro.git
```

### 3. 添加文件并提交
```bash
git add .
git commit -m "初始提交：WorkBuddy介绍网站"
```

### 4. 推送到GitHub
```bash
git branch -M main
git push -u origin main
```

## 🌐 启用GitHub Pages

### 步骤：

1. 访问你的GitHub仓库
2. 点击 `Settings` 标签
3. 在左侧菜单找到 `Pages`
4. 在 `Source` 下选择 `Deploy from a branch`
5. Branch选择 `main`，目录选择 `/ (root)`
6. 点击 `Save`

### 访问网站

等待1-2分钟后，网站将部署到：
```
https://你的用户名.github.io/workbuddy-intro/
```

## 🔧 配置自定义域名（可选）

### 1. 准备域名
在域名服务商（如阿里云、腾讯云、Namecheap）购买域名。

### 2. 配置DNS
添加以下记录：

**CNAME记录**：
```
类型：CNAME
主机记录：@
记录值：你的用户名.github.io
TTL：600
```

### 3. 在GitHub设置域名
1. 仓库 Settings → Pages
2. Custom domain 输入你的域名
3. 点击 Save
4. GitHub会验证域名所有权

### 4. 配置HTTPS
1. 在Pages设置中勾选 `Enforce HTTPS`
2. 等待证书生成（通常几分钟）

## 📊 其他部署平台

### Vercel部署

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel
```

### Netlify部署

**方式1：拖拽部署**
1. 访问 https://app.netlify.com/drop
2. 将 `workbuddy-intro.html` 拖入页面
3. 等待部署完成

**方式2：CLI部署**
```bash
# 安装Netlify CLI
npm i -g netlify-cli

# 登录
netlify login

# 部署
netlify deploy --prod
```

### Cloudflare Pages

1. 访问 https://pages.cloudflare.com
2. 连接GitHub账户
3. 选择仓库
4. 构建设置（无需配置，默认即可）
5. 点击 Save and Deploy

## 📈 性能优化

### 使用CDN加速
- GitHub Pages自带CDN
- 可选择其他CDN服务商（Cloudflare、Fastly）

### 压缩资源
```bash
# 压缩HTML（可选）
npm install -g html-minifier
html-minifier workbuddy-intro.html -o workbuddy-intro.min.html --collapse-whitespace --remove-comments
```

### 启用缓存
在GitHub Pages的CORS或缓存头配置中设置。

## 🔍 SEO优化检查

部署后，使用以下工具检查SEO：

- [Google Search Console](https://search.google.com/search-console)
- [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [SEMrush](https://www.semrush.com/siteaudit)

## 📱 测试网站功能

部署后测试以下功能：

- ✅ 响应式设计（手机、平板、桌面）
- ✅ 动画效果
- ✅ 导航滚动
- ✅ 表单提交
- ✅ 多语言切换
- ✅ 所有链接可访问

## 🐛 常见问题

### Q: GitHub Pages部署失败？
A: 检查仓库是否为Public，确保main分支存在。

### Q: 自定义域名不生效？
A: 检查DNS设置，等待最多24小时传播。

### Q: 网站加载慢？
A: 优化图片大小，使用CDN，压缩CSS/JS。

### Q: 想回滚到旧版本？
A: 使用git回滚：
```bash
git log --oneline
git reset --hard <commit-hash>
git push -f origin main
```

## 🔄 持续更新

### 添加新功能后更新网站：
```bash
# 修改文件后
git add .
git commit -m "添加新功能描述"
git push
```

GitHub Pages会自动重新部署。

## 📞 获取帮助

- GitHub文档：https://docs.github.com/pages
- WorkBuddy支持：https://workbuddycn.com/support
- 社区论坛：https://workbuddycn.com/community

---

**祝你部署顺利！** 🎉
