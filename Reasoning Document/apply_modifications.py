# -*- coding: utf-8 -*-
import re

path = r'd:\Application\AllToolsSet\Herb\Smart-Chinese-Herbal-Medicine-Recognition-App\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

orig_len = len(content)

def replace(old, new, count=1):
    global content
    if old not in content:
        print('NOT FOUND:', old[:80].replace('\n','\\n'))
        return
    content = content.replace(old, new, count)
    print('REPLACED:', old[:60].replace('\n','\\n'), '->', new[:60].replace('\n','\\n'))

# 1. Update :root CSS to Apple-ish tokens
replace("""        :root {
            --dark-bg: #0b1a2e;
            --dark-secondary: #0f2440;
            --light-bg: #f8fafc;
            --primary-blue: #1a2a4a;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --text-dark: #1e293b;
            --text-light: #f8fafc;
            --text-muted: #64748b;
            --card-shadow: 0 10px 40px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
        }""", """        :root {
            --dark-bg: #000000;
            --dark-secondary: #1c1c1e;
            --light-bg: #f2f2f7;
            --primary-blue: #00275a;
            --accent-blue: #007aff;
            --accent-purple: #5e5ce6;
            --text-dark: #1d1d1f;
            --text-light: #f5f5f7;
            --text-muted: #6e6e73;
            --card-shadow: 0 10px 40px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
            --success: #34c759;
            --error: #ff3b30;
            --warning: #ff9f0a;
        }""")

# 2. Add extra CSS for empty state, lock inputs, stagger reveal
replace("""        .lock-timer { color: #ef4444; font-size: 0.9rem; margin-top: 0.5rem; }

        /* Toast */""", """        .lock-timer { color: #ef4444; font-size: 0.9rem; margin-top: 0.5rem; }

        .project-empty-state { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:3rem 1rem; color:rgba(245,245,247,0.5); text-align:center; }
        .project-empty-state p { margin:0; }

        .admin-login-card input:disabled { background:#f2f2f7; color:#8e8e93; cursor:not-allowed; opacity:0.7; }
        .admin-login-card button:disabled { opacity:0.6; cursor:not-allowed; transform:none !important; box-shadow:none; }

        /* Staggered reveal delays */
        .feature-cards .feature-card.reveal:nth-child(1) { transition-delay: 0.1s; }
        .feature-cards .feature-card.reveal:nth-child(2) { transition-delay: 0.2s; }
        .project-categories .project-col.reveal:nth-child(1) { transition-delay: 0.1s; }
        .project-categories .project-col.reveal:nth-child(2) { transition-delay: 0.2s; }
        .project-categories .project-col.reveal:nth-child(3) { transition-delay: 0.3s; }
        .portfolio-layout .portfolio-panel.reveal:nth-child(1) { transition-delay: 0.1s; }
        .portfolio-layout .portfolio-panel.reveal:nth-child(2) { transition-delay: 0.2s; }
        .about-grid .about-card.reveal:nth-child(1) { transition-delay: 0.1s; }
        .about-grid .about-card.reveal:nth-child(2) { transition-delay: 0.2s; }
        .contact-methods .contact-item.reveal:nth-child(1) { transition-delay: 0.1s; }
        .contact-methods .contact-item.reveal:nth-child(2) { transition-delay: 0.2s; }

        /* Toast */""")

# 3. Reorder project detail / apply panel and add empty state
replace("""            <div class="project-wide-panel reveal">
                <div class="project-detail-area" id="projectDetailArea">
                    <h2><i class="fas fa-info-circle"></i> 项目详情</h2>
                    <p style="color:rgba(248,250,252,0.5); text-align:center; padding:2rem 0;">请点击上方项目名称查看详情</p>
                </div>
                <div class="project-divider"></div>
                <div class="project-apply-area">
                    <div class="project-data-card" id="projectDataCard">
                        <h4><i class="fas fa-chart-line"></i> 项目数据</h4>
                        <div style="color:rgba(248,250,252,0.9); font-weight:600; margin-bottom:1rem; font-size:0.95rem;">基于轻量化 MobileNetV2 的中药材识别系统</div>
                        <div class="project-data-grid">
                            <div><div class="value" style="color:#3b82f6;">163</div><div class="label">中药材种类</div></div>
                            <div><div class="value" style="color:#8b5cf6;">98.34%</div><div class="label">测试集准确率</div></div>
                            <div><div class="value" style="color:#10b981;">~9.7MB</div><div class="label">模型体积</div></div>
                            <div><div class="value" style="color:#fbbf24;">v0.3</div><div class="label">模型版本</div></div>
                        </div>
                    </div>
                    <h3><i class="fas fa-file-alt"></i> 申请新项目</h3>
                    <p>如果你有一个项目想法，欢迎提交申请，我会与您取得联系。</p>
                    <form class="apply-form" id="projectApplyForm" style="margin-top:0; padding-top:0; border-top:none;">
                        <div class="form-group">
                            <label>项目名称 <span class="required">*</span></label>
                            <input type="text" name="projectName" required placeholder="输入项目名称">
                        </div>
                        <div class="form-group">
                            <label>项目类型</label>
                            <select name="projectType">
                                <option value="网站开发">网站开发</option>
                                <option value="小程序开发">小程序开发</option>
                                <option value="AI应用">AI应用</option>
                                <option value="其他">其他</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>项目描述</label>
                            <textarea name="projectDesc" placeholder="简述项目目标和预期成果..."></textarea>
                        </div>
                        <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> 提交申请</button>
                    </form>
                </div>
            </div>""", """            <div class="project-wide-panel reveal">
                <div class="project-apply-area">
                    <h3><i class="fas fa-file-alt"></i> 申请新项目</h3>
                    <p>如果你有一个项目想法，欢迎提交申请，我会与您取得联系。</p>
                    <form class="apply-form" id="projectApplyForm" style="margin-top:0; padding-top:0; border-top:none;">
                        <div class="form-group">
                            <label>项目名称 <span class="required">*</span></label>
                            <input type="text" name="projectName" required placeholder="输入项目名称">
                        </div>
                        <div class="form-group">
                            <label>项目类型</label>
                            <select name="projectType">
                                <option value="网站开发">网站开发</option>
                                <option value="小程序开发">小程序开发</option>
                                <option value="AI应用">AI应用</option>
                                <option value="其他">其他</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>项目描述</label>
                            <textarea name="projectDesc" placeholder="简述项目目标和预期成果..."></textarea>
                        </div>
                        <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> 提交申请</button>
                    </form>
                </div>
                <div class="project-divider"></div>
                <div class="project-detail-area" id="projectDetailArea">
                    <h2><i class="fas fa-info-circle"></i> 项目详情</h2>
                    <div class="project-empty-state" id="projectEmptyState">
                        <i class="fas fa-hand-pointer" style="margin-bottom:0.5rem; font-size:1.5rem; opacity:0.5;"></i>
                        <p>请点击上方已完成的项目查看详情</p>
                    </div>
                    <div class="project-data-card" id="projectDataCard" style="display:none;">
                        <h4><i class="fas fa-chart-line"></i> 项目数据</h4>
                        <div id="projectDataTitle" style="color:rgba(245,245,247,0.9); font-weight:600; margin-bottom:1rem; font-size:0.95rem;">基于轻量化 MobileNetV2 的中药材识别系统</div>
                        <div class="project-data-grid">
                            <div><div class="value" style="color:#007aff;">163</div><div class="label">中药材种类</div></div>
                            <div><div class="value" style="color:#5e5ce6;">98.34%</div><div class="label">测试集准确率</div></div>
                            <div><div class="value" style="color:#34c759;">~9.7MB</div><div class="label">模型体积</div></div>
                            <div><div class="value" style="color:#ff9f0a;">v0.3</div><div class="label">模型版本</div></div>
                        </div>
                        <div id="projectDetailContent" style="margin-top:1.5rem; color:rgba(245,245,247,0.8); line-height:1.8;"></div>
                    </div>
                </div>
            </div>""")

# 4. Add reveal class to project columns
replace('<div class="project-col">\n                    <h3><i class="fas fa-clock"></i> 预计进行的项目</h3>',
        '<div class="project-col reveal">\n                    <h3><i class="fas fa-clock"></i> 预计进行的项目</h3>')
replace('<div class="project-col">\n                    <h3><i class="fas fa-spinner"></i> 进行中的项目</h3>',
        '<div class="project-col reveal">\n                    <h3><i class="fas fa-spinner"></i> 进行中的项目</h3>')
replace('<div class="project-col">\n                    <h3><i class="fas fa-check-circle"></i> 已完成的项目</h3>',
        '<div class="project-col reveal">\n                    <h3><i class="fas fa-check-circle"></i> 已完成的项目</h3>')

# 5. Add reveal class to portfolio panels and work item
replace('<div class="portfolio-work-item active" data-work="chinese-herb">',
        '<div class="portfolio-work-item active reveal" data-work="chinese-herb">')
replace('<div class="portfolio-panel">\n                    <h3><i class="fas fa-folder-tree" style="color:#fbbf24;"></i> 目录树</h3>',
        '<div class="portfolio-panel reveal">\n                    <h3><i class="fas fa-folder-tree" style="color:#ff9f0a;"></i> 目录树</h3>')
replace('<div class="portfolio-panel">\n                    <h3><i class="fas fa-star" style="color:#8b5cf6;"></i> 3D 星图</h3>',
        '<div class="portfolio-panel reveal">\n                    <h3><i class="fas fa-star" style="color:#5e5ce6;"></i> 3D 星图</h3>')

# 6. Add reveal class to contact items
replace('<button class="contact-item" id="emailBtn">',
        '<button class="contact-item reveal" id="emailBtn">')
replace('<a href="https://github.com/TaoYaTou" target="_blank" class="contact-item">',
        '<a href="https://github.com/TaoYaTou" target="_blank" class="contact-item reveal">')

# 7. Admin section HTML: remove desc, empty username, add lock code input
replace("""    <!-- Admin -->
    <section id="admin">
        <div class="container">
            <div class="section-header reveal">
                <h2 class="section-title" style="color:var(--text-dark);">管理<span>后台</span></h2>
                <p class="section-desc">管理员登录后查看与管理申请记录</p>
            </div>
            <div id="adminContent" class="reveal">
                <!-- Login -->
                <div class="admin-login-card" id="adminLoginCard">
                    <h3><i class="fas fa-lock" style="color:#3b82f6;"></i> 管理员登录</h3>
                    <form id="adminLoginForm">
                        <div class="form-group">
                            <label>用户名</label>
                            <input type="text" id="adminUsername" value="TAO" required>
                        </div>
                        <div class="form-group">
                            <label>密码</label>
                            <input type="password" id="adminPassword" required placeholder="请输入密码">
                        </div>
                        <div id="lockMessage" class="lock-timer" style="display:none;"></div>
                        <button type="submit" class="btn btn-primary" style="width:100%;"><i class="fas fa-sign-in-alt"></i> 登录</button>
                    </form>
                </div>""", """    <!-- Admin -->
    <section id="admin">
        <div class="container">
            <div class="section-header reveal">
                <h2 class="section-title" style="color:var(--text-dark);">管理<span>后台</span></h2>
            </div>
            <div id="adminContent" class="reveal">
                <!-- Login -->
                <div class="admin-login-card reveal" id="adminLoginCard">
                    <h3><i class="fas fa-lock" style="color:#007aff;"></i> 管理员登录</h3>
                    <form id="adminLoginForm">
                        <div class="form-group">
                            <label>用户名</label>
                            <input type="text" id="adminUsername" required placeholder="请输入用户名">
                        </div>
                        <div class="form-group">
                            <label>密码</label>
                            <input type="password" id="adminPassword" required placeholder="请输入密码">
                        </div>
                        <div class="form-group">
                            <label>锁定码</label>
                            <input type="text" id="adminLockCode" placeholder="账户锁定时输入锁定码解除">
                        </div>
                        <div id="lockMessage" class="lock-timer" style="display:none;"></div>
                        <button type="submit" class="btn btn-primary" style="width:100%;"><i class="fas fa-sign-in-alt"></i> 登录</button>
                    </form>
                </div>""")

# 8. Add AI-driven skill tag
replace("""                        <span class="skill-tag">Git</span>
                        <span class="skill-tag">VS Code</span>""",
        """                        <span class="skill-tag">Git</span>
                        <span class="skill-tag">AI驱动式开发</span>
                        <span class="skill-tag">VS Code</span>""")

# 9. Replace project click handler
replace("""        document.querySelectorAll('.project-list li[data-project]').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.project-list li').forEach(li => li.classList.remove('active'));
                item.classList.add('active');
                const projectId = item.dataset.project;
                const detail = projectData[projectId];
                const area = document.getElementById('projectDetailArea');
                if (detail) {
                    area.innerHTML = `
                        <h2>${escapeHtml(detail.title)}</h2>
                        <p>${escapeHtml(detail.desc)}</p>
                        <p><strong>技术栈：</strong>${escapeHtml(detail.tech.join(' / '))}</p>
                        <button class="btn btn-primary" id="gotoPortfolioBtn"><i class="fas fa-arrow-right"></i> 前往「作品」板块查看完整架构</button>
                    `;
                    document.getElementById('gotoPortfolioBtn').addEventListener('click', () => {
                        document.getElementById('portfolio').scrollIntoView({ behavior: 'smooth' });
                        setTimeout(() => {
                            document.querySelector('.portfolio-work-item')?.click();
                            const firstFile = document.querySelector('.tree-item[data-path="Smart-Chinese-Herbal-Medicine-Recognition-App/Backend/app.py"]');
                            if (firstFile) firstFile.click();
                        }, 500);
                    });
                }
            });
        });""", """        document.querySelectorAll('.project-list li[data-project]').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.project-list li').forEach(li => li.classList.remove('active'));
                item.classList.add('active');
                const projectId = item.dataset.project;
                const detail = projectData[projectId];
                if (!detail) return;
                document.getElementById('projectEmptyState').style.display = 'none';
                document.getElementById('projectDataCard').style.display = 'block';
                document.getElementById('projectDataTitle').textContent = detail.title;
                document.getElementById('projectDetailContent').innerHTML = `
                    <p>${escapeHtml(detail.desc)}</p>
                    <p><strong>技术栈：</strong>${escapeHtml(detail.tech.join(' / '))}</p>
                    <button class="btn btn-primary" id="gotoPortfolioBtn"><i class="fas fa-arrow-right"></i> 前往「作品」板块查看完整架构</button>
                `;
                document.getElementById('gotoPortfolioBtn').addEventListener('click', () => {
                    document.getElementById('portfolio').scrollIntoView({ behavior: 'smooth' });
                    setTimeout(() => {
                        document.querySelector('.portfolio-work-item')?.click();
                        const firstFile = document.querySelector('.tree-item[data-path="Smart-Chinese-Herbal-Medicine-Recognition-App/Backend/app.py"]');
                        if (firstFile) firstFile.click();
                    }, 500);
                });
            });
        });""")

# 10. Add pathTypeMap population in buildTree
replace("""        const fileTreeEl = document.getElementById('fileTree');
        const treeItemMap = new Map();
        function buildTree(node, parentPath, container, level) {
            const fullPath = parentPath ? parentPath + '/' + node.name : node.name;
            const item = document.createElement('div');""",
        """        const fileTreeEl = document.getElementById('fileTree');
        const treeItemMap = new Map();
        const pathTypeMap = new Map();
        function buildTree(node, parentPath, container, level) {
            const fullPath = parentPath ? parentPath + '/' + node.name : node.name;
            pathTypeMap.set(fullPath, node.type);
            const item = document.createElement('div');""")

# 11. Replace selectFile function and add fileInfo/descriptions
old_select = """        // ===================== Detail panel =====================
        function selectFile(path) {
            const cleanPath = path.replace(/^Smart-Chinese-Herbal-Medicine-Recognition-App\\//, '');
            document.querySelectorAll('.tree-item').forEach(i => i.classList.remove('active'));
            const treeItem = treeItemMap.get(path);
            if (treeItem) treeItem.classList.add('active');

            const snippet = fileSnippets[cleanPath];
            const titleEl = document.getElementById('detailTitle');
            const descEl = document.getElementById('detailDesc');
            const codeEl = document.getElementById('detailCode');
            const wrapper = document.getElementById('detailCodeWrapper');

            titleEl.textContent = escapeHtml(cleanPath || path);
            if (snippet) {
                descEl.textContent = snippet.desc;
                codeEl.className = 'language-' + snippet.language;
                codeEl.textContent = snippet.code;
                wrapper.style.display = 'block';
            } else {
                descEl.textContent = '该文件为项目资源或配置文件，详细内容请前往 GitHub 仓库查看。';
                codeEl.textContent = '';
                wrapper.style.display = 'none';
            }
            if (window.Prism) Prism.highlightElement(codeEl);

            // Highlight star node
            highlightStarNode(path);
        }"""
new_select = """        // ===================== File descriptions =====================
        const folderInfo = {
            'Smart-Chinese-Herbal-Medicine-Recognition-App': '项目根目录，包含后端服务、小程序前端、文档与配置文件。',
            'Backend': '后端服务目录，包含 Flask API、训练脚本、模型文件与部署配置。',
            'Backend/.vscode': 'VS Code 编辑器配置目录。',
            'Frontend': '微信小程序前端目录，包含页面、样式、配置与云托管相关文件。',
            'Frontend/.cloudbase': '腾讯云开发配置目录。',
            'Frontend/.cloudbase/container': '云托管容器配置目录。',
            'Frontend/pages': '小程序页面目录。',
            'Frontend/pages/index': '小程序首页目录。',
            'Frontend/pages/history': '历史记录页面目录。',
            'Frontend/pages/history-detail': '历史详情页面目录。',
            'Frontend/pages/settings': '设置页面目录。',
            'Frontend/pages/contact': '联系我们页面目录。'
        };
        const fileInfo = {
            'README.md': '项目说明文档，介绍项目背景、功能与使用方法。',
            'LICENSE': '开源许可证文件。',
            '.gitattributes': 'Git 属性配置文件。',
            '.gitignore': 'Git 忽略规则文件。',
            'Database connection.txt': '数据库连接说明文件。',
            'project_structure.txt': '项目结构说明文件。',
            'Backend/requirements.txt': '后端依赖包列表。',
            'Backend/label.txt': '中药材类别标签文件。',
            'Backend/Dockerfile': '容器镜像构建配置。',
            'Backend/model.onnx': '导出后的 ONNX 模型文件，用于后端推理。',
            'Backend/confusion_matrix.png': '模型混淆矩阵可视化图。',
            'Backend/top20_accuracy.png': 'Top20 类别准确率可视化图。',
            'Backend/training_curve.png': '训练曲线可视化图。',
            'Backend/v0.3_epoch26_20260807_072722_acc98.34.pth': '训练得到的 PyTorch 模型权重文件。',
            'Backend/.msc': '模型训练相关辅助文件。',
            'Backend/.mv': '模型训练相关辅助文件。',
            'Backend/.vscode/settings.json': 'VS Code 编辑器配置文件。',
            'Backend/Python包版本.py': '记录项目使用的 Python 包版本。',
            'Frontend/app.js': '小程序全局逻辑入口文件。',
            'Frontend/app.wxss': '小程序全局样式文件。',
            'Frontend/.eslintrc.js': 'ESLint 代码规范配置。',
            'Frontend/.gitattributes': 'Git 属性配置文件。',
            'Frontend/project.config.json': '微信小程序项目配置文件。',
            'Frontend/project.private.config.json': '微信开发者工具私有配置文件。',
            'Frontend/sitemap.json': '小程序搜索索引配置。',
            'Frontend/.cloudbase/container/debug.json': '云托管容器调试配置。',
            'Frontend/pages/index/index.json': '首页页面配置。',
            'Frontend/pages/index/index.wxss': '首页页面样式。',
            'Frontend/pages/history/history.js': '历史记录页面逻辑。',
            'Frontend/pages/history/history.json': '历史记录页面配置。',
            'Frontend/pages/history/history.wxml': '历史记录页面结构。',
            'Frontend/pages/history/history.wxss': '历史记录页面样式。',
            'Frontend/pages/history-detail/history-detail.js': '历史详情页面逻辑。',
            'Frontend/pages/history-detail/history-detail.json': '历史详情页面配置。',
            'Frontend/pages/history-detail/history-detail.wxml': '历史详情页面结构。',
            'Frontend/pages/history-detail/history-detail.wxss': '历史详情页面样式。',
            'Frontend/pages/settings/settings.js': '设置页面逻辑。',
            'Frontend/pages/settings/settings.json': '设置页面配置。',
            'Frontend/pages/settings/settings.wxml': '设置页面结构。',
            'Frontend/pages/settings/settings.wxss': '设置页面样式。',
            'Frontend/pages/contact/contact.js': '联系我们页面逻辑。',
            'Frontend/pages/contact/contact.json': '联系我们页面配置。',
            'Frontend/pages/contact/contact.wxml': '联系我们页面结构。',
            'Frontend/pages/contact/contact.wxss': '联系我们页面样式。'
        };
        function describePath(cleanPath, type) {
            if (type === 'folder') {
                if (folderInfo[cleanPath]) return folderInfo[cleanPath];
                const name = cleanPath.split('/').pop();
                return `文件夹「${name}」，用于组织项目中的相关文件与资源。`;
            }
            if (fileInfo[cleanPath]) return fileInfo[cleanPath];
            const name = cleanPath.split('/').pop();
            const ext = name.split('.').pop().toLowerCase();
            const codeExts = { 'py': 'Python 代码文件', 'js': 'JavaScript 代码文件', 'json': 'JSON 配置文件', 'wxml': '小程序页面结构文件', 'wxss': '小程序页面样式文件', 'txt': '文本说明文件', 'md': 'Markdown 说明文档' };
            if (codeExts[ext]) return `${codeExts[ext]}「${name}」。`;
            return `文件「${name}」，属于项目资源或配置文件。`;
        }

        // ===================== Detail panel =====================
        function selectFile(path) {
            const cleanPath = path.replace(/^Smart-Chinese-Herbal-Medicine-Recognition-App\\//, '');
            document.querySelectorAll('.tree-item').forEach(i => i.classList.remove('active'));
            const treeItem = treeItemMap.get(path);
            if (treeItem) treeItem.classList.add('active');

            const type = pathTypeMap.get(path) || 'file';
            const snippet = fileSnippets[cleanPath];
            const titleEl = document.getElementById('detailTitle');
            const descEl = document.getElementById('detailDesc');
            const codeEl = document.getElementById('detailCode');
            const wrapper = document.getElementById('detailCodeWrapper');

            titleEl.textContent = escapeHtml(cleanPath || path);
            if (type === 'folder') {
                descEl.textContent = describePath(cleanPath, type);
                codeEl.textContent = '';
                wrapper.style.display = 'none';
            } else if (snippet) {
                descEl.textContent = describePath(cleanPath, type) + ' 详细内容请前往 GitHub 仓库查看。';
                codeEl.className = 'language-' + snippet.language;
                codeEl.textContent = snippet.code;
                wrapper.style.display = 'block';
            } else {
                descEl.textContent = describePath(cleanPath, type) + ' 详细内容请前往 GitHub 仓库查看。';
                codeEl.textContent = '';
                wrapper.style.display = 'none';
            }
            if (window.Prism) Prism.highlightElement(codeEl);

            // Highlight star node
            highlightStarNode(path);
        }"""
replace(old_select, new_select)

# 12. 3D star map layout: thinner folder and deterministic radial placement
old_3d = """            function createFolderGeometry() {
                const group = new THREE.Group();
                const bodyGeo = new THREE.BoxGeometry(0.7, 0.5, 0.55);
                const tabGeo = new THREE.BoxGeometry(0.35, 0.12, 0.55);
                const bodyMat = new THREE.MeshPhongMaterial({ color: 0xfbbf24, emissive: 0x92400e, emissiveIntensity: 0.2 });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = -0.05;
                const tab = new THREE.Mesh(tabGeo, bodyMat);
                tab.position.set(-0.12, 0.26, 0);
                group.add(body);
                group.add(tab);
                return group;
            }

            function createGearGeometry() {"""
new_3d = """            function createFolderGeometry() {
                const group = new THREE.Group();
                const bodyGeo = new THREE.BoxGeometry(0.7, 0.5, 0.12);
                const tabGeo = new THREE.BoxGeometry(0.35, 0.12, 0.12);
                const bodyMat = new THREE.MeshPhongMaterial({ color: 0xff9f0a, emissive: 0x92400e, emissiveIntensity: 0.2 });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = -0.05;
                const tab = new THREE.Mesh(tabGeo, bodyMat);
                tab.position.set(-0.12, 0.26, 0);
                group.add(body);
                group.add(tab);
                return group;
            }

            function createGearGeometry() {"""
replace(old_3d, new_3d)

old_createNode = """            function createNode(node, parentPath, parentMesh, depth) {
                const path = parentPath ? parentPath + '/' + node.name : node.name;
                const angle = Math.random() * Math.PI * 2;
                const radius = 3 + depth * 2.5;
                const x = Math.cos(angle) * radius + (parentMesh ? parentMesh.position.x : 0);
                const y = (Math.random() - 0.5) * 6 + (parentMesh ? parentMesh.position.y : 0);
                const z = Math.sin(angle) * radius + (parentMesh ? parentMesh.position.z : 0);"""
new_createNode = """            function createNode(node, parentPath, parentMesh, depth, childIndex, siblingCount) {
                const path = parentPath ? parentPath + '/' + node.name : node.name;
                let x, y, z;
                if (!parentMesh) {
                    x = 0; y = 0; z = 0;
                } else {
                    const count = Math.max(siblingCount || 1, 1);
                    const idx = childIndex || 0;
                    const baseAngle = (idx / count) * Math.PI * 2 + depth * 0.8;
                    const radius = 2.0 + depth * 1.8;
                    const elevation = Math.sin(baseAngle * 3 + depth) * (1.2 / depth);
                    x = parentMesh.position.x + Math.cos(baseAngle) * radius;
                    y = parentMesh.position.y + elevation;
                    z = parentMesh.position.z + Math.sin(baseAngle) * radius;
                }"""
replace(old_createNode, new_createNode)

# Update recursive call and initial call
replace("""                if (node.children) {
                    node.children.forEach(child => createNode(child, path, mesh, depth + 1));
                }
            }
            createNode(fileTreeData, '', null, 0);""",
        """                if (node.children) {
                    const count = node.children.length;
                    node.children.forEach((child, i) => createNode(child, path, mesh, depth + 1, i, count));
                }
            }
            createNode(fileTreeData, '', null, 0, 0, 1);""")

# 13. Admin JS rewrite
old_admin = """        // ===================== Admin =====================
        const DEFAULT_USERNAME = 'TAO';
        const DEFAULT_PASSWORD = 'Admin@2026#Secure';
        const LOCKOUT_LIMIT = 5;
        const LOCKOUT_DURATION = 15 * 60 * 1000;
        const SESSION_TIMEOUT = 30 * 60 * 1000;

        function getAdminUser() {
            return JSON.parse(localStorage.getItem('adminUser') || 'null');
        }
        function setAdminUser(user) {
            localStorage.setItem('adminUser', JSON.stringify(user));
        }
        function getAdminLogs() {
            return JSON.parse(localStorage.getItem('adminLogs') || '[]');
        }
        function addAdminLog(log) {
            const logs = getAdminLogs();
            logs.push({ timestamp: new Date().toISOString(), ...log });
            localStorage.setItem('adminLogs', JSON.stringify(logs));
        }
        function getLockStatus() {
            return JSON.parse(localStorage.getItem('adminLock') || 'null');
        }
        function setLockStatus(status) {
            localStorage.setItem('adminLock', JSON.stringify(status));
        }

        async function ensureDefaultAdmin() {
            const user = getAdminUser();
            if (!user) {
                setAdminUser({
                    username: DEFAULT_USERNAME,
                    passwordHash: await sha256(DEFAULT_PASSWORD),
                    forceChangePassword: true
                });
            }
        }

        function updateLockDisplay() {
            const lock = getLockStatus();
            const msg = document.getElementById('lockMessage');
            if (lock && new Date().getTime() - lock.lockedAt < LOCKOUT_DURATION) {
                const remaining = Math.ceil((LOCKOUT_DURATION - (new Date().getTime() - lock.lockedAt)) / 1000);
                msg.textContent = `账户已锁定，请 ${Math.floor(remaining/60)} 分 ${remaining%60} 秒后重试`;
                msg.style.display = 'block';
                return true;
            } else {
                msg.style.display = 'none';
                if (lock) setLockStatus(null);
                return false;
            }
        }

        let sessionTimer = null;
        function resetSessionTimer() {
            if (sessionTimer) clearTimeout(sessionTimer);
            sessionTimer = setTimeout(() => {
                showToast('登录超时，已自动退出', 'error');
                adminLogout();
            }, SESSION_TIMEOUT);
        }
        function adminLogout() {
            localStorage.removeItem('adminSession');
            if (sessionTimer) clearTimeout(sessionTimer);
            document.getElementById('adminLoginCard').style.display = 'block';
            document.getElementById('adminDashboard').style.display = 'none';
            document.getElementById('adminPassword').value = '';
            updateLockDisplay();
        }
        function adminLogin() {
            document.getElementById('adminLoginCard').style.display = 'none';
            document.getElementById('adminDashboard').style.display = 'block';
            localStorage.setItem('adminSession', JSON.stringify({ loginAt: new Date().toISOString() }));
            resetSessionTimer();
            renderApplicationsTable();
        }

        document.getElementById('adminLoginForm').addEventListener('submit', async e => {
            e.preventDefault();
            if (updateLockDisplay()) return;
            await ensureDefaultAdmin();
            const username = document.getElementById('adminUsername').value.trim();
            const password = document.getElementById('adminPassword').value;
            const user = getAdminUser();
            const inputHash = await sha256(password);

            if (username !== user.username) {
                recordLoginAttempt(username, false, '账号不存在');
                showToast('账号不存在', 'error');
                return;
            }
            if (inputHash !== user.passwordHash) {
                recordLoginAttempt(username, false, '密码错误');
                const lock = getLockStatus() || { failedCount: 0, lockedAt: null, username };
                lock.failedCount = (lock.failedCount || 0) + 1;
                if (lock.failedCount >= LOCKOUT_LIMIT) {
                    lock.lockedAt = new Date().getTime();
                    setLockStatus(lock);
                    updateLockDisplay();
                    showToast('连续失败 5 次，账户已锁定 15 分钟', 'error');
                } else {
                    showToast(`密码错误（还剩 ${LOCKOUT_LIMIT - lock.failedCount} 次机会）`, 'error');
                    setLockStatus(lock);
                }
                return;
            }

            // Success
            setLockStatus(null);
            recordLoginAttempt(username, true, '登录成功');
            showToast('登录成功');

            if (user.forceChangePassword) {
                const newPw = await showModal('首次登录', '为了账户安全，请修改默认密码', { input: true, confirmText: '修改' });
                if (newPw && isStrongPassword(newPw)) {
                    setAdminUser({ username, passwordHash: await sha256(newPw), forceChangePassword: false });
                    showToast('密码修改成功');
                    adminLogin();
                } else if (newPw) {
                    showToast('密码强度不足，请重新登录后修改', 'error');
                }
            } else {
                adminLogin();
            }
        });

        function recordLoginAttempt(username, success, reason) {
            addAdminLog({ type: 'login', username, success, reason, source: 'local' });
        }"""
new_admin = """        // ===================== Admin =====================
        const DEFAULT_USERNAME = 'TAO';
        const DEFAULT_PASSWORD = 'Admin@2026#Secure';
        const LOCKOUT_LIMIT = 5;
        const LOCKOUT_DURATION = 15 * 60 * 1000;
        const SESSION_TIMEOUT = 30 * 60 * 1000;
        const UNLOCK_CODE = 'Admin-N9567ueHS-TAO-KKAp25RASD2Q34';

        function getAdminUser() {
            return JSON.parse(localStorage.getItem('adminUser') || 'null');
        }
        function setAdminUser(user) {
            localStorage.setItem('adminUser', JSON.stringify(user));
        }
        function getAdminLogs() {
            return JSON.parse(localStorage.getItem('adminLogs') || '[]');
        }
        function addAdminLog(log) {
            const logs = getAdminLogs();
            logs.push({ timestamp: new Date().toISOString(), ...log });
            localStorage.setItem('adminLogs', JSON.stringify(logs));
        }
        function getLockStatus() {
            return JSON.parse(localStorage.getItem('adminLock') || 'null');
        }
        function setLockStatus(status) {
            localStorage.setItem('adminLock', JSON.stringify(status));
        }

        async function ensureDefaultAdmin() {
            const user = getAdminUser();
            if (!user) {
                setAdminUser({
                    username: DEFAULT_USERNAME,
                    passwordHash: await sha256(DEFAULT_PASSWORD),
                    forceChangePassword: true
                });
            }
        }

        function setAdminInputsDisabled(disabled) {
            document.getElementById('adminUsername').disabled = disabled;
            document.getElementById('adminPassword').disabled = disabled;
            document.querySelector('#adminLoginForm button[type="submit"]').disabled = disabled;
        }

        function updateLockDisplay() {
            const lock = getLockStatus();
            const msg = document.getElementById('lockMessage');
            if (lock && lock.lockedAt && new Date().getTime() - lock.lockedAt < LOCKOUT_DURATION) {
                const remaining = Math.ceil((LOCKOUT_DURATION - (new Date().getTime() - lock.lockedAt)) / 1000);
                msg.textContent = `账户已锁定，请 ${Math.floor(remaining/60)} 分 ${remaining%60} 秒后重试，或在锁定码输入框输入解锁码`;
                msg.style.display = 'block';
                setAdminInputsDisabled(true);
                return true;
            } else {
                msg.style.display = 'none';
                setAdminInputsDisabled(false);
                if (lock) setLockStatus(null);
                return false;
            }
        }

        function incrementFailedLock(username) {
            const lock = getLockStatus() || { failedCount: 0, lockedAt: null, username: '' };
            lock.failedCount = (lock.failedCount || 0) + 1;
            lock.username = username;
            if (lock.failedCount >= LOCKOUT_LIMIT) {
                lock.lockedAt = new Date().getTime();
                setLockStatus(lock);
                updateLockDisplay();
                showToast(`连续失败 ${LOCKOUT_LIMIT} 次，账户已锁定 15 分钟`, 'error');
            } else {
                setLockStatus(lock);
                showToast(`密码错误（还剩 ${LOCKOUT_LIMIT - lock.failedCount} 次机会）`, 'error');
            }
        }

        document.getElementById('adminLockCode').addEventListener('input', e => {
            if (e.target.value === UNLOCK_CODE && getLockStatus() && getLockStatus().lockedAt) {
                setLockStatus(null);
                updateLockDisplay();
                showToast('锁定已解除');
                e.target.value = '';
            }
        });

        let sessionTimer = null;
        function resetSessionTimer() {
            if (sessionTimer) clearTimeout(sessionTimer);
            sessionTimer = setTimeout(() => {
                showToast('登录超时，已自动退出', 'error');
                adminLogout();
            }, SESSION_TIMEOUT);
        }
        function adminLogout() {
            localStorage.removeItem('adminSession');
            if (sessionTimer) clearTimeout(sessionTimer);
            document.getElementById('adminLoginCard').style.display = 'block';
            document.getElementById('adminDashboard').style.display = 'none';
            document.getElementById('adminPassword').value = '';
            document.getElementById('adminLockCode').value = '';
            updateLockDisplay();
        }
        function adminLogin() {
            document.getElementById('adminLoginCard').style.display = 'none';
            document.getElementById('adminDashboard').style.display = 'block';
            localStorage.setItem('adminSession', JSON.stringify({ loginAt: new Date().toISOString() }));
            resetSessionTimer();
            renderApplicationsTable();
        }

        document.getElementById('adminLoginForm').addEventListener('submit', async e => {
            e.preventDefault();
            if (updateLockDisplay()) return;
            await ensureDefaultAdmin();
            const username = document.getElementById('adminUsername').value.trim();
            const password = document.getElementById('adminPassword').value;
            const user = getAdminUser();
            const inputHash = await sha256(password);

            if (username !== user.username) {
                recordLoginAttempt(username, false, '账号不存在');
                incrementFailedLock(username);
                return;
            }
            if (inputHash !== user.passwordHash) {
                recordLoginAttempt(username, false, '密码错误');
                incrementFailedLock(username);
                return;
            }

            // Success
            setLockStatus(null);
            recordLoginAttempt(username, true, '登录成功');
            showToast('登录成功');

            if (user.forceChangePassword) {
                const newPw = await showModal('首次登录', '为了账户安全，请修改默认密码', { input: true, confirmText: '修改' });
                if (newPw && isStrongPassword(newPw)) {
                    setAdminUser({ username, passwordHash: await sha256(newPw), forceChangePassword: false });
                    showToast('密码修改成功');
                    adminLogin();
                } else if (newPw) {
                    showToast('密码强度不足，请重新登录后修改', 'error');
                }
            } else {
                adminLogin();
            }
        });

        function recordLoginAttempt(username, success, reason) {
            addAdminLog({ type: 'login', username, success, reason, source: 'local' });
        }"""
replace(old_admin, new_admin)

# 14. Global color replacements
replacements = [
    ('#3b82f6', '#007aff'),
    ('0x3b82f6', '0x007aff'),
    ('#8b5cf6', '#5e5ce6'),
    ('0x8b5cf6', '0x5e5ce6'),
    ('#10b981', '#34c759'),
    ('#ef4444', '#ff3b30'),
    ('#dc2626', '#ff3b30'),
    ('#fbbf24', '#ff9f0a'),
    ('#0b1a2e', '#000000'),
    ('0x0b1a2e', '0x000000'),
    ('#0f2440', '#1c1c1e'),
    ('#1a2a4a', '#00275a'),
    ('0x1a2a4a', '0x00275a'),
    ('#1e293b', '#1d1d1f'),
    ('#64748b', '#6e6e73'),
    ('#f8fafc', '#f5f5f7'),
    ('248, 250, 252', '245, 245, 247'),
    ('248,250,252', '245,245,247'),
    ('11, 26, 46', '0, 0, 0'),
    ('11,26,46', '0,0,0'),
    ('#f1f5f9', '#f2f2f7'),
    ('#94a3b8', '#8e8e93'),
    ('#e2e8f0', '#e5e5ea'),
]
for old, new in replacements:
    content = content.replace(old, new)
    print('GLOBAL:', old, '->', new)

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done. Original', orig_len, '-> New', len(content))
