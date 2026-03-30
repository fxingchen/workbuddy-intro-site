// 多语言切换完整实现
// 在 workbuddy-intro.html 的 <head> 中引入此脚本

const translations = {
    zh: {
        // 导航栏
        'nav-features': '核心功能',
        'nav-demo': '使用演示',
        'nav-comparison': '产品对比',
        'nav-faq': '常见问题',
        'nav-contact': '联系我们',
        'nav-experience': '立即体验',

        // Hero区域
        'hero-badge': '🚀 腾讯推出，更适合普通人的国产AI',
        'hero-title': '微信一句话',
        'hero-subtitle': '就能真干活！',
        'hero-desc-1': '不懂编程？没关系！不需要复杂配置，无需技术背景。',
        'hero-desc-2': '自然语言指令，解放双手，让AI替你上班。',
        'hero-download': '免费下载',
        'hero-watch': '观看演示',
        'hero-followers': '粉丝关注',
        'hero-likes': '播放点赞',
        'hero-demo-tip': '真实使用演示，仅需3秒完成任务',

        // 功能区域
        'features-title': '为什么选择 WorkBuddy？',
        'features-subtitle': '不止是聊天工具，而是你的数字同事，真正能替你干活！',
        'feature-1-title': '自然语言驱动',
        'feature-1-desc': '不需要学习命令，不需要编程。就像和人聊天一样，用日常语言告诉AI你想做什么，它就自动执行。',
        'feature-2-title': '本地执行，数据安全',
        'feature-2-desc': '所有任务在本地电脑执行，数据不出境。无需上传云端，隐私安全有保障。',
        'feature-3-title': 'OpenClaw生态兼容',
        'feature-3-desc': '完全兼容OpenClaw技能生态，支持桌面控制、文件操作、网络自动化等丰富功能。',
        'feature-4-title': '多Agent并行工作',
        'feature-4-desc': '同时启动多个AI助手，并行处理不同任务，效率提升3-5倍。就像有个专业团队。',
        'feature-5-title': '微信/飞书联动',
        'feature-5-desc': '不在电脑旁？通过微信、飞书远程控制，一句话就能让电脑干活，随时随地上线。',
        'feature-6-title': '零代码自动化',
        'feature-6-desc': '用自然语言搭建自动化工作流，重复性工作自动完成。定时任务、条件触发，解放双手。',

        // 演示区域
        'demo-title': '真实使用演示',
        'demo-subtitle': '看看WorkBuddy如何帮你完成日常任务',
        'demo-1-title': '文件智能整理',
        'demo-2-title': '数据分析报告',
        'demo-3-title': '远程办公控制',

        // 对比区域
        'comparison-title': '与其他产品对比',
        'comparison-subtitle': '为什么WorkBuddy更适合普通人使用？',

        // FAQ区域
        'faq-title': '常见问题',
        'faq-subtitle': '关于WorkBuddy的常见疑问解答',
        'faq-1-q': 'Q: WorkBuddy需要技术背景吗？',
        'faq-1-a': '完全不需要！WorkBuddy专为普通人设计，零编程、零配置、零学习成本。就像和同事聊天一样，用日常语言告诉它你想做什么就行。',
        'faq-2-q': 'Q: 数据安全吗？会上传到云端吗？',
        'faq-2-a': '非常安全！所有任务都在你的本地电脑执行，数据不会出境。WorkBuddy只是帮你操作电脑，不会保存或上传你的文件到云端。',
        'faq-3-q': 'Q: 免费吗？有什么付费计划？',
        'faq-3-a': 'WorkBuddy提供免费版本，满足日常办公需求。专业版本提供更多功能（如更多并行Agent、高级自动化、企业级支持），具体价格请查看官方定价页面。',
        'faq-4-q': 'Q: 支持哪些操作系统？',
        'faq-4-a': '目前支持Windows系统，Mac和Linux版本正在开发中。需要Node.js、Git和.NET等基础环境，首次使用时会有安装指引。',
        'faq-5-q': 'Q: 能做什么任务？',
        'faq-5-a': '几乎所有桌面操作！包括但不限于：文件整理、数据录入、报告生成、邮件发送、软件操作、定时任务、远程控制、内容创作、PPT制作、表格处理等等。',

        // 联系表单
        'contact-title': '联系我们',
        'contact-subtitle': '有问题？随时联系我们',
        'contact-name': '姓名',
        'contact-email': '邮箱',
        'contact-subject': '主题',
        'contact-message': '消息',
        'contact-send': '发送消息',
        'contact-name-placeholder': '请输入您的姓名',
        'contact-email-placeholder': '请输入您的邮箱',
        'contact-subject-placeholder': '请输入咨询主题',
        'contact-message-placeholder': '请输入您的消息...',
        'contact-success': '✅ 消息发送成功！我们会尽快回复您。',

        // CTA区域
        'cta-title': '准备好让你的AI同事帮你上班了吗？',
        'cta-subtitle': '免费下载，5分钟快速上手，从此解放双手，效率翻倍！',
        'cta-download': '🚀 免费下载',
        'cta-watch': '📺 观看B站演示视频',
        'cta-gift': '🎁 立即下载，前10000名用户送30天高级功能体验',

        // 页脚
        'footer-tagline': '腾讯出品，更懂中国人的AI助手',
        'footer-product': '产品',
        'footer-support': '支持',
        'footer-follow': '关注我们',
        'footer-features': '功能介绍',
        'footer-tutorial': '使用教程',
        'footer-api': 'API文档',
        'footer-updates': '更新日志',
        'footer-help': '帮助中心',
        'footer-video': '视频教程',
        'footer-community': '社区论坛',
        'footer-feedback': '反馈建议',
        'footer-privacy': '隐私政策',
        'footer-terms': '服务条款',
        'footer-icp': '备案信息',
        'footer-copyright': '© 2026 WorkBuddy. All rights reserved. 腾讯云出品'
    },
    en: {
        // Navigation
        'nav-features': 'Features',
        'nav-demo': 'Demo',
        'nav-comparison': 'Comparison',
        'nav-faq': 'FAQ',
        'nav-contact': 'Contact',
        'nav-experience': 'Try Now',

        // Hero
        'hero-badge': '🚀 Powered by Tencent - Made for Everyone',
        'hero-title': 'Send a Message',
        'hero-subtitle': 'Let AI Do the Work!',
        'hero-desc-1': 'No coding? No problem! No complex setup, no technical background required.',
        'hero-desc-2': 'Natural language commands to free your hands and let AI work for you.',
        'hero-download': 'Free Download',
        'hero-watch': 'Watch Demo',
        'hero-followers': 'Followers',
        'hero-likes': 'Likes',
        'hero-demo-tip': 'Real demo, completes tasks in just 3 seconds',

        // Features
        'features-title': 'Why Choose WorkBuddy?',
        'features-subtitle': 'More than a chat tool - your digital colleague that really gets work done!',
        'feature-1-title': 'Natural Language Driven',
        'feature-1-desc': 'No need to learn commands or code. Just talk to AI like you would to a person, and it will execute automatically.',
        'feature-2-title': 'Local Execution, Data Secure',
        'feature-2-desc': 'All tasks execute on your local computer, no data leaves your device. No cloud upload, privacy guaranteed.',
        'feature-3-title': 'OpenClaw Ecosystem Compatible',
        'feature-3-desc': 'Fully compatible with OpenClaw skill ecosystem, supporting desktop control, file operations, web automation and more.',
        'feature-4-title': 'Multi-Agent Parallel Work',
        'feature-4-desc': 'Launch multiple AI assistants simultaneously to process different tasks in parallel, 3-5x efficiency boost. Like having a pro team.',
        'feature-5-title': 'WeChat/Feishu Integration',
        'feature-5-desc': 'Not at your computer? Remote control via WeChat or Feishu with a single message. Work from anywhere.',
        'feature-6-title': 'Zero-Code Automation',
        'feature-6-desc': 'Build automation workflows with natural language. Repetitive tasks completed automatically. Scheduled tasks, triggers, hands-free.',

        // Demo
        'demo-title': 'Real Usage Demo',
        'demo-subtitle': 'See how WorkBuddy helps you complete daily tasks',
        'demo-1-title': 'Smart File Organization',
        'demo-2-title': 'Data Analysis Reports',
        'demo-3-title': 'Remote Work Control',

        // Comparison
        'comparison-title': 'Comparison with Other Products',
        'comparison-subtitle': 'Why is WorkBuddy more suitable for everyday users?',

        // FAQ
        'faq-title': 'FAQ',
        'faq-subtitle': 'Answers to common questions about WorkBuddy',
        'faq-1-q': 'Q: Does WorkBuddy require technical background?',
        'faq-1-a': 'Not at all! WorkBuddy is designed for everyone. Zero programming, zero configuration, zero learning curve. Just tell it what you want in plain language.',
        'faq-2-q': 'Q: Is data secure? Will it be uploaded to cloud?',
        'faq-2-a': 'Very secure! All tasks execute on your local computer, data never leaves your device. WorkBuddy just helps you operate the computer, it does not save or upload your files to the cloud.',
        'faq-3-q': 'Q: Is it free? What are the paid plans?',
        'faq-3-a': 'WorkBuddy offers a free version that meets daily office needs. The professional version provides more features (such as more parallel Agents, advanced automation, enterprise-level support). Check the official pricing page for details.',
        'faq-4-q': 'Q: Which operating systems are supported?',
        'faq-4-a': 'Currently supports Windows, Mac and Linux versions are under development. Requires Node.js, Git and .NET basic environments. Installation guides are provided on first use.',
        'faq-5-q': 'Q: What tasks can it do?',
        'faq-5-a': 'Almost all desktop operations! Including but not limited to: file organization, data entry, report generation, email sending, software operation, scheduled tasks, remote control, content creation, PPT making, spreadsheet processing, etc.',

        // Contact
        'contact-title': 'Contact Us',
        'contact-subtitle': 'Have questions? Contact us anytime',
        'contact-name': 'Name',
        'contact-email': 'Email',
        'contact-subject': 'Subject',
        'contact-message': 'Message',
        'contact-send': 'Send Message',
        'contact-name-placeholder': 'Enter your name',
        'contact-email-placeholder': 'Enter your email',
        'contact-subject-placeholder': 'Enter subject',
        'contact-message-placeholder': 'Enter your message...',
        'contact-success': '✅ Message sent successfully! We will reply as soon as possible.',

        // CTA
        'cta-title': 'Ready to Let Your AI Colleague Work for You?',
        'cta-subtitle': 'Free download, 5 minutes to get started. Free your hands, double your efficiency!',
        'cta-download': '🚀 Free Download',
        'cta-watch': '📺 Watch Demo Video',
        'cta-gift': '🎁 Download now, first 10,000 users get 30 days of premium features free',

        // Footer
        'footer-tagline': 'Powered by Tencent - AI Assistant Made for You',
        'footer-product': 'Product',
        'footer-support': 'Support',
        'footer-follow': 'Follow Us',
        'footer-features': 'Features',
        'footer-tutorial': 'Tutorial',
        'footer-api': 'API Docs',
        'footer-updates': 'Changelog',
        'footer-help': 'Help Center',
        'footer-video': 'Video Tutorial',
        'footer-community': 'Community',
        'footer-feedback': 'Feedback',
        'footer-privacy': 'Privacy Policy',
        'footer-terms': 'Terms of Service',
        'footer-icp': 'ICP',
        'footer-copyright': '© 2026 WorkBuddy. All rights reserved. Tencent Cloud'
    }
};

let currentLanguage = 'zh';

function setLanguage(lang) {
    currentLanguage = lang;
    const t = translations[lang];

    // Update HTML lang attribute
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';

    // Update current lang indicator
    const langIndicator = document.getElementById('current-lang');
    if (langIndicator) {
        langIndicator.textContent = lang === 'zh' ? '中文' : 'English';
    }

    // Update all translatable elements
    Object.keys(t).forEach(key => {
        const element = document.querySelector(`[data-i18n="${key}"]`);
        if (element) {
            // Handle elements with multiple text nodes
            if (key.includes('-desc-1') || key.includes('-desc-2')) {
                const parent = element.closest('.text-xl') || element.closest('.lead');
                if (parent) {
                    const parts = key.split('-desc-');
                    if (parts.length === 2) {
                        const baseKey = parts[0] + '-desc';
                        const index = parseInt(parts[1]) - 1;
                        const childNodes = parent.querySelectorAll('[data-i18n^="' + baseKey + '-"]');
                        if (childNodes[index]) {
                            childNodes[index].textContent = t[key];
                        }
                    }
                    return;
                }
            }
            element.textContent = t[key];
        }
    });

    // Update placeholder attributes
    ['name', 'email', 'subject', 'message'].forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            input.placeholder = t[`contact-${field}-placeholder`];
        }
    });

    // Store language preference
    localStorage.setItem('preferredLanguage', lang);
}

// Load saved language preference on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang && savedLang !== 'zh') {
        setLanguage(savedLang);
    }
});
