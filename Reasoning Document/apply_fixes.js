const fs = require('fs');
const FILE = 'd:\\Application\\AllToolsSet\\Herb\\Smart-Chinese-Herbal-Medicine-Recognition-App\\index.html';
let code = fs.readFileSync(FILE, 'utf-8');

function findFunctionEnd(code, start) {
    const stack = [{ name: 'code', depth: 1 }];
    let i = start;
    while (i < code.length) {
        const state = stack[stack.length - 1];
        const ch = code[i];
        if (state.name === 'code' || state.name === 'template_expr') {
            if (ch === '{' && state.name === 'code') {
                state.depth++;
            } else if (ch === '}' && state.name === 'code') {
                state.depth--;
                if (state.depth === 0) {
                    stack.pop();
                    if (stack.length === 0) return i;
                }
            } else if (ch === '{' && state.name === 'template_expr') {
                state.depth++;
            } else if (ch === '}' && state.name === 'template_expr') {
                state.depth--;
                if (state.depth === 0) {
                    stack.pop();
                }
            } else if (ch === "'") {
                stack.push({ name: 'single' });
            } else if (ch === '"') {
                stack.push({ name: 'double' });
            } else if (ch === '`') {
                stack.push({ name: 'backtick' });
            }
        } else if (state.name === 'single') {
            if (ch === '\\') {
                i++;
            } else if (ch === "'") {
                stack.pop();
            }
        } else if (state.name === 'double') {
            if (ch === '\\') {
                i++;
            } else if (ch === '"') {
                stack.pop();
            }
        } else if (state.name === 'backtick') {
            if (ch === '\\') {
                i++;
            } else if (ch === '`') {
                stack.pop();
            } else if (code.startsWith('${', i)) {
                stack.push({ name: 'template_expr', depth: 1 });
                i++;
            }
        }
        i++;
    }
    return -1;
}

function replaceFunction(code, name, newText, asyncFn) {
    const prefix = asyncFn ? 'async\\s+' : '';
    const pattern = new RegExp(prefix + 'function\\s+' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*\\([^)]*\\)\\s*\\{');
    const m = code.match(pattern);
    if (!m) throw new Error('Function ' + name + ' not found');
    const start = m.index;
    const braceStart = m.index + m[0].length - 1;
    const end = findFunctionEnd(code, braceStart);
    if (end < 0) throw new Error('Could not find end of function ' + name);
    return code.slice(0, start) + newText + code.slice(end + 1);
}

function addAfterMarker(code, marker, text) {
    const idx = code.indexOf(marker);
    if (idx < 0) throw new Error('Marker not found: ' + marker);
    return code.slice(0, idx + marker.length) + text + code.slice(idx + marker.length);
}

// CSS & HTML
code = code.replace(
    `<div class="user-menu" id="navUserMenu" style="display:none;">
                        <a href="#" id="navProfileBtn"><i class="fas fa-user"></i> 个人信息</a>
                        <a href="#" id="navLogoutBtn"><i class="fas fa-sign-out-alt"></i> 退出登录</a>
                    </div>`,
    `<div class="user-menu" id="navUserMenu" style="display:none;">
                        <a href="#" id="navProfileBtn"><i class="fas fa-user"></i> 个人信息</a>
                        <a href="#" id="navMailNotifyBtn"><i class="fas fa-envelope"></i> 邮件通知 <span class="nav-badge" id="navMailBadge" style="display:none;">0</span></a>
                        <a href="#" id="navLogoutBtn"><i class="fas fa-sign-out-alt"></i> 退出登录</a>
                    </div>`
);

code = code.replace('<ul class="profile-list" id="existingFeaturesList" style="margin-top:1rem;">', '<ul class="profile-list scrollable-list" id="existingFeaturesList" style="margin-top:1rem;">');
code = code.replace('<ul class="project-list" id="plannedProjectsList">', '<ul class="project-list scrollable-list" id="plannedProjectsList">');
code = code.replace('<ul class="project-list" id="ongoingProjectsList">', '<ul class="project-list scrollable-list" id="ongoingProjectsList">');
code = code.replace('<ul class="project-list" id="completedProjectsList">', '<ul class="project-list scrollable-list" id="completedProjectsList">');

code = code.replace(
    `                    <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width:100%;"><i class="fas fa-paper-plane"></i> 提交申请</button>`,
    `                    <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <div class="form-group">
                            <label>新参与人员</label>
                            <input type="text" name="participants" placeholder="多个用户名用逗号分隔，非必填">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width:100%;"><i class="fas fa-paper-plane"></i> 提交申请</button>`
);

code = code.replace(
    `                        <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> 提交申请</button>`,
    `                        <div class="form-group">
                            <label>联系方式 <span class="required">*</span></label>
                            <input type="text" name="contact" required placeholder="手机号/邮箱/微信号">
                        </div>
                        <div class="form-group">
                            <label>新参与人员</label>
                            <input type="text" name="participants" placeholder="多个用户名用逗号分隔，非必填">
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> 提交申请</button>`
);

code = code.replace(
    `                    <div class="form-group">
                        <label>展示文件提交</label>
                        <input type="file" name="submitFile" accept="image/*,.zip">
                        <div class="form-hint">支持图片和 ZIP 压缩包，大小不超过 50GB</div>
                    </div>`,
    `                    <div class="form-group">
                        <label>新参与人员</label>
                        <input type="text" name="participants" placeholder="多个用户名用逗号分隔，非必填">
                    </div>
                    <div class="form-group">
                        <label>展示文件提交</label>
                        <input type="file" name="submitFile" accept="image/*,.zip">
                        <div class="form-hint">支持图片和 ZIP 压缩包，大小不超过 50GB</div>
                    </div>`
);

code = code.replace(
    '<!-- Showcase Apply Modal -->',
    `<!-- Mail Notifications Modal -->
    <div class="modal-overlay" id="mailNotifyModal">
        <div class="modal" style="max-width: 520px;">
            <h3><i class="fas fa-envelope"></i> 邮件通知</h3>
            <div class="mail-notify-list" id="mailNotifyList">
                <div class="empty-state" style="padding:2rem;">暂无通知</div>
            </div>
            <div class="modal-actions">
                <button class="btn btn-secondary btn-sm" id="mailNotifyClose">关闭</button>
            </div>
        </div>
    </div>

    <!-- Showcase Apply Modal -->`
);

const cssAddition = `
        .nav-badge { display:none; margin-left:auto; min-width:18px; height:18px; padding:0 5px; border-radius:9px; background:#ff3b30; color:#fff; font-size:0.7rem; font-weight:700; align-items:center; justify-content:center; }
        .user-menu a { position:relative; align-items:center; }
        .mail-notify-list { max-height:60vh; overflow-y:auto; }
        .mail-notify-item { padding:1rem; border-bottom:1px solid #f2f2f7; }
        .mail-notify-item:last-child { border-bottom:none; }
        .mail-notify-unread { background:rgba(0,122,255,0.06); }
        .mail-notify-title { font-weight:600; color:#1c1c1e; margin-bottom:0.25rem; display:flex; align-items:center; gap:0.5rem; }
        .mail-notify-time { font-size:0.75rem; color:#8e8e93; margin-bottom:0.5rem; }
        .mail-notify-message { color:#3a3a3c; font-size:0.9rem; line-height:1.6; }
        .scrollable-list { max-height:14rem; overflow-y:auto; padding-right:0.25rem; }
        .admin-table-scroll { max-height:28rem; overflow-y:auto; border:1px solid #e5e5ea; border-radius:var(--radius-sm); margin-bottom:1rem; }
        .profile-section { border:1px solid rgba(255,255,255,0.08); border-radius:var(--radius-md); padding:1.5rem; margin-bottom:1.5rem; }
`;
code = code.replace('</style>', cssAddition + '\n    </style>');

// notification helpers
const notificationHelpers = `

        function getNotifications() { return safeJsonParse(localStorage.getItem('mailNotifications'), {}); }
        function setNotifications(map) { localStorage.setItem('mailNotifications', JSON.stringify(map)); }
        function addNotification(username, notification) {
            if (!username) return;
            const map = getNotifications();
            const list = map[username] || [];
            list.push({
                id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                title: notification.title || '通知',
                message: notification.message || '',
                type: notification.type || 'info',
                read: false,
                createdAt: new Date().toISOString()
            });
            if (list.length > 5) list.splice(0, list.length - 5);
            map[username] = list;
            setNotifications(map);
            renderNavNotifications();
        }
        function markNotificationsRead(username) {
            if (!username) return;
            const map = getNotifications();
            const list = map[username] || [];
            let changed = false;
            list.forEach(n => { if (!n.read) { n.read = true; changed = true; } });
            if (changed) {
                setNotifications(map);
                const user = findUser(username);
                if (user && user.dismissed && list.some(n => n.type === 'dismiss')) {
                    user.dismissNoticeAcked = true;
                    const users = getUsers();
                    const idx = users.findIndex(u => u.username === username);
                    if (idx >= 0) { users[idx] = user; setUsers(users); }
                }
            }
            renderNavNotifications();
        }
        function getUnreadCount(username) {
            if (!username) return 0;
            return (getNotifications()[username] || []).filter(n => !n.read).length;
        }
        function renderNavNotifications() {
            const session = getCurrentSession();
            const badge = document.getElementById('navMailBadge');
            if (!badge) return;
            if (!session) { badge.style.display = 'none'; return; }
            const count = getUnreadCount(session.username);
            if (count > 0) { badge.textContent = count > 99 ? '99+' : String(count); badge.style.display = 'inline-flex'; }
            else { badge.style.display = 'none'; }
        }
        function openMailNotificationsModal() {
            const session = getCurrentSession();
            if (!session) return;
            markNotificationsRead(session.username);
            const listEl = document.getElementById('mailNotifyList');
            const map = getNotifications();
            const list = (map[session.username] || []).slice().reverse();
            if (!list.length) {
                listEl.innerHTML = '<div class="empty-state" style="padding:2rem;">暂无通知</div>';
            } else {
                listEl.innerHTML = list.map(n => {
                    const unreadClass = n.read ? '' : ' mail-notify-unread';
                    return \`<div class="mail-notify-item\${unreadClass}" data-id="\${escapeHtml(n.id)}">
                        <div class="mail-notify-title">\${escapeHtml(n.title)}\${n.read ? '' : ' <span class="badge badge-pending">未读</span>'}</div>
                        <div class="mail-notify-time">\${new Date(n.createdAt).toLocaleString()}</div>
                        <div class="mail-notify-message">\${escapeHtml(n.message)}</div>
                    </div>\`;
                }).join('');
            }
            document.getElementById('mailNotifyModal').classList.add('show');
            bringModalToFront(document.getElementById('mailNotifyModal'));
            renderNavNotifications();
        }
        function closeMailNotificationsModal() { document.getElementById('mailNotifyModal').classList.remove('show'); }
`;
code = addAfterMarker(code, "function setApplications(apps) { localStorage.setItem('applications', JSON.stringify(apps)); }", notificationHelpers);

// Replace functions
code = replaceFunction(code, 'saveApplication', `function saveApplication(type, name, category, description, contact, host = '访客', extraParticipants = []) {
            const apps = getApplications();
            const participants = [host];
            extraParticipants.forEach(p => { const t = (p || '').trim(); if (t && !participants.includes(t)) participants.push(t); });
            apps.push({
                id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                type,
                name: sanitizeInput(name),
                category: sanitizeInput(category),
                description: sanitizeInput(description),
                contact: sanitizeInput(contact),
                host,
                participants,
                timestamp: new Date().toISOString(),
                status: '待处理'
            });
            setApplications(apps);
            showToast('申请已提交，我会尽快查看并回复你');
        }`);

code = replaceFunction(code, 'renderProjectLists', `function renderProjectLists() {
            const apps = getApplications();
            const planned = apps.filter(a => a.type === '项目' && a.status === '待处理');
            const ongoing = apps.filter(a => a.type === '项目' && a.status === '处理中');
            const completed = apps.filter(a => a.type === '项目' && a.status === '已发布');
            const staticCompleted = [{ id: 'chinese-herb', name: '基于轻量化MobileNetV2的中药材识别系统（毕设）', host: 'TAO', description: '' }];
            const participantsLine = item => (item.participants && item.participants.length > 1) ? \`<div style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem;">参与人员：\${escapeHtml(item.participants.join('、'))}</div>\` : '';
            const render = (list, elId, clickable) => {
                const el = document.getElementById(elId);
                if (!el) return;
                if (!list.length) { el.innerHTML = '<li class="placeholder">暂无项目</li>'; return; }
                el.innerHTML = list.map(item => {
                    const host = item.host || '访客';
                    const clickAttr = clickable ? \` data-project="\${escapeHtml(item.id)}"\` : '';
                    return \`<li\${clickAttr}>
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;"><span>\${escapeHtml(item.name)}</span><span class="host-label">主持人：\${escapeHtml(host)}</span></div>
                        \${item.description ? \`<div style="color:var(--text-muted);font-size:0.9rem;margin-top:0.35rem;line-height:1.5;">\${escapeHtml(item.description)}</div>\` : ''}
                        \${participantsLine(item)}
                    </li>\`;
                }).join('');
            };
            render(planned, 'plannedProjectsList', false);
            render(ongoing, 'ongoingProjectsList', false);
            render([...staticCompleted, ...completed], 'completedProjectsList', true);

            document.querySelectorAll('#completedProjectsList li[data-project]').forEach(item => {
                item.addEventListener('click', () => {
                    document.querySelectorAll('.project-list li').forEach(li => li.classList.remove('active'));
                    item.classList.add('active');
                    showProjectDetail(item.dataset.project);
                });
            });
        }`);

code = replaceFunction(code, 'renderFeatureList', `function renderFeatureList() {
            const apps = getApplications();
            const features = apps.filter(a => a.type === '功能' && a.status === '已发布');
            const el = document.getElementById('existingFeaturesList');
            if (!el) return;
            if (!features.length) { el.innerHTML = '<li class="empty">暂无已发布功能</li>'; return; }
            const participantsLine = a => (a.participants && a.participants.length > 1) ? \`<div style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem;">参与人员：\${escapeHtml(a.participants.join('、'))}</div>\` : '';
            el.innerHTML = features.map(f => \`<li>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;"><span>\${escapeHtml(f.name)}</span><span class="host-label">主持人：\${escapeHtml(f.host || '访客')}</span></div>
                \${f.description ? \`<div style="color:var(--text-muted);font-size:0.9rem;margin-top:0.35rem;line-height:1.5;">\${escapeHtml(f.description)}</div>\` : ''}
                \${participantsLine(f)}
                <div style="margin-top:0.5rem;"><button class="btn btn-danger btn-sm report-project-btn" data-id="\${escapeHtml(f.id)}">举报</button></div>
            </li>\`).join('');
            el.querySelectorAll('.report-project-btn').forEach(btn => btn.addEventListener('click', e => {
                e.stopPropagation();
                handleReportProject(btn.dataset.id);
            }));
        }`);

code = replaceFunction(code, 'showProjectDetail', `function showProjectDetail(projectId) {
            const apps = getApplications();
            const app = apps.find(a => a.id === projectId);
            const staticDetail = projectData[projectId];
            if (!staticDetail && !app) return;

            document.getElementById('projectEmptyState').style.display = 'none';
            document.getElementById('projectDataCard').style.display = 'block';

            const dataGrid = document.getElementById('projectDataGrid');
            if (staticDetail) {
                dataGrid.style.display = 'grid';
                document.getElementById('projectDataTitle').textContent = staticDetail.title;
                document.getElementById('projectDetailContent').innerHTML = \`
                    <p>\${escapeHtml(staticDetail.desc)}</p>
                    <p><strong>技术栈：</strong>\${escapeHtml(staticDetail.tech.join(' / '))}</p>
                    <button class="btn btn-primary" id="gotoPortfolioBtn"><i class="fas fa-arrow-right"></i> 前往「作品」板块查看完整架构</button>
                \`;
                document.getElementById('gotoPortfolioBtn').addEventListener('click', () => {
                    document.getElementById('portfolio').scrollIntoView({ behavior: 'smooth' });
                    setTimeout(() => {
                        loadProject('chinese-herb');
                    }, 500);
                });
            } else {
                dataGrid.style.display = 'none';
                document.getElementById('projectDataTitle').textContent = app.name;
                let detailHtml = \`<p>\${escapeHtml(app.description)}</p>\`;
                if (app.status !== '已发布') {
                    detailHtml += \`<p><strong>用途：</strong>\${escapeHtml(app.purpose || '未填写')}</p><p><strong>分类：</strong>\${escapeHtml(app.category)}</p>\`;
                }
                if (app.status === '已发布') {
                    detailHtml += \`<div style="margin:1rem 0;"><button class="btn btn-primary" id="gotoPortfolioBtn"><i class="fas fa-arrow-right"></i> 前往作品查看</button></div>\`;
                    if (!app.reportStatus) {
                        detailHtml += \`<div style="margin:1rem 0;"><button class="btn btn-danger btn-sm report-project-btn" data-id="\${escapeHtml(app.id)}">举报</button></div>\`;
                    } else {
                        detailHtml += \`<div style="margin:1rem 0; color:#8e8e93; font-size:0.85rem;">该项目已被举报</div>\`;
                    }
                }
                document.getElementById('projectDetailContent').innerHTML = detailHtml;
                const gotoBtn = document.getElementById('gotoPortfolioBtn');
                if (gotoBtn) {
                    gotoBtn.addEventListener('click', () => {
                        document.getElementById('portfolio').scrollIntoView({ behavior: 'smooth' });
                        setTimeout(() => {
                            const showcase = getApplications().find(a => a.id === app.id && a.showcaseStatus === 'approved');
                            if (showcase) loadProject(app.id);
                            else showToast('该项目尚未申请作品展示', 'error');
                        }, 500);
                    });
                }
                const reportBtn = document.querySelector('#projectDetailContent .report-project-btn');
                if (reportBtn) reportBtn.addEventListener('click', () => handleReportProject(app.id));
            }

            const card = document.getElementById('participantCard');
            card.style.display = 'block';
            document.getElementById('participantHost').textContent = app ? (app.host || '访客') : 'TAO';
            document.getElementById('participantList').textContent = app ? (app.participants || [app.host || '访客']).join('、') : 'TAO';
        }`);

code = replaceFunction(code, 'loadProject', `function loadProject(projectId) {
            const staticProject = projects.find(p => p.id === projectId);
            const showcaseApp = !staticProject ? getApplications().find(a => a.id === projectId && a.type === '项目' && a.status === '已发布' && a.showcaseStatus === 'approved') : null;
            if (!staticProject && !showcaseApp) return;
            currentProjectId = projectId;
            renderProjectList();
            const detailPanel = document.getElementById('detailPanel');
            if (staticProject) {
                document.getElementById('portfolioEmptyState').style.display = 'none';
                document.getElementById('showcaseLayout').style.display = 'none';
                document.getElementById('portfolioLayout').style.display = 'grid';
                detailPanel.style.display = 'block';
                renderFileTree(staticProject);
                if (!starRenderer) { initStarMap(); }
                clearStarMap();
                renderStarMap(staticProject.data);
                resetDetailPanel(staticProject);
                setTimeout(() => selectFile(staticProject.firstFile), 100);
            } else {
                document.getElementById('portfolioEmptyState').style.display = 'none';
                document.getElementById('portfolioLayout').style.display = 'none';
                detailPanel.style.display = 'none';
                document.getElementById('showcaseLayout').style.display = 'grid';
                const role = (() => { const s = getCurrentSession(); return s ? findUser(s.username)?.role : null; })();
                document.getElementById('showcaseDetailTitle').textContent = showcaseApp.name;
                document.getElementById('showcaseDetailDesc').textContent = showcaseApp.description;
                const hostHtml = \`<strong>主持人：</strong>\${escapeHtml(showcaseApp.host || '未知')}\` + (showcaseApp.participants?.length ? \` &nbsp;|&nbsp; <strong>参与人员：</strong>\${escapeHtml(showcaseApp.participants.join(', '))}\` : '');
                document.getElementById('showcaseDetailHost').innerHTML = hostHtml;
                const dl = document.getElementById('showcaseDetailDownload');
                let dlHtml = '';
                if (showcaseApp.host === '已注销用户') {
                    dlHtml += \`<span style="color:#8e8e93; margin-right:0.5rem;">该用户已注销，下载源已被撤回</span>\`;
                } else if (showcaseApp.sourceFileName && (role === '站长' || role === '管理员')) {
                    dlHtml += \`<a href="\${showcaseApp.sourceFileData}" download="\${escapeHtml(showcaseApp.sourceFileName)}" class="btn btn-primary"><i class="fas fa-download"></i> 下载源文件</a>\`;
                }
                dlHtml += \`<button class="btn btn-danger btn-sm report-project-btn" data-id="\${escapeHtml(showcaseApp.id)}" style="margin-left:0.5rem;">举报</button>\`;
                dl.innerHTML = dlHtml;
                dl.querySelector('.report-project-btn')?.addEventListener('click', () => handleReportProject(showcaseApp.id));
            }
        }`);

code = replaceFunction(code, 'renderProfile', `function renderProfile() {
            const session = getCurrentSession();
            if (!session) return;
            const user = findUser(session.username);
            if (!user) { logout(); return; }
            document.getElementById('profileUsername').textContent = user.username;
            document.getElementById('profileRole').textContent = getRoleLabel(user.role);
            document.getElementById('profileContact').textContent = user.contact || '未填写';

            // 辞退提示与管理员申请入口
            const dismissRow = document.getElementById('profileDismissNoticeRow');
            const dismissValue = dismissRow.querySelector('.value');
            const adminApplySection = document.getElementById('profileAdminApplySection');
            const adminApplyBtn = document.getElementById('profileApplyAdminBtn');
            const cooldownNotice = document.getElementById('profileAdminCooldownNotice');
            const now = Date.now();
            const banUntil = user.idBanUntil || 0;
            const remainingDays = banUntil > now ? Math.ceil((banUntil - now) / (24 * 60 * 60 * 1000)) : 0;
            if (user.dismissed && remainingDays > 0) {
                dismissRow.style.display = 'flex';
                dismissValue.textContent = \`您已被辞退，权限降级，再次申请管理员冷却期为\${remainingDays}天\`;
                adminApplySection.style.display = 'block';
                adminApplyBtn.disabled = true;
                adminApplyBtn.title = '冷却期内无法申请';
                cooldownNotice.style.display = 'block';
                cooldownNotice.textContent = \`冷却期剩余 \${remainingDays} 天\`;
            } else {
                dismissRow.style.display = 'none';
                if (user.role === '用户') {
                    adminApplySection.style.display = 'block';
                    adminApplyBtn.disabled = false;
                    adminApplyBtn.title = '';
                    cooldownNotice.style.display = 'none';
                    const regs = getRegistrations();
                    const hasPending = regs.some(r => r.username === user.username && r.status === '待处理');
                    const hasApproved = regs.some(r => r.username === user.username && r.status === '已批准');
                    if (hasPending) {
                        adminApplyBtn.disabled = true;
                        cooldownNotice.style.display = 'block';
                        cooldownNotice.textContent = '您已有一条待处理的管理员申请';
                    } else if (hasApproved) {
                        adminApplyBtn.disabled = true;
                        cooldownNotice.style.display = 'block';
                        cooldownNotice.textContent = '您已经是管理员';
                    }
                } else {
                    adminApplySection.style.display = 'none';
                }
            }

            const apps = getApplications();
            let myProjects = apps.filter(a => a.type === '项目' && (a.host === user.username || (a.participants || []).includes(user.username)));
            const myFeatures = apps.filter(a => a.type === '功能' && (a.host === user.username || (a.participants || []).includes(user.username)));
            if (user.username === DEFAULT_TAO_USERNAME) {
                myProjects.unshift({ id: 'chinese-herb', name: '基于轻量化MobileNetV2的中药材识别系统（毕设）', host: DEFAULT_TAO_USERNAME, description: '', status: '已发布', type: '项目', notWithdrawable: true });
            }
            const statusBadgeClass = s => {
                if (s === '待处理' || s === '处理中') return 'badge-pending';
                if (s === '已发布') return 'badge-approved';
                return 'badge-rejected';
            };
            const participantsLine = a => (a.participants && a.participants.length > 1) ? \`<div style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem;">参与人员：\${escapeHtml(a.participants.join('、'))}</div>\` : '';
            const projectsEl = document.getElementById('profileProjectsList');
            if (!myProjects.length) {
                projectsEl.innerHTML = '<li class="empty">暂无</li>';
            } else {
                projectsEl.innerHTML = myProjects.map(a => {
                    const isHost = a.host === user.username;
                    let actions = '';
                    if (isHost && !a.notWithdrawable && ['待处理', '处理中', '已发布'].includes(a.status)) {
                        actions += \`<button class="btn btn-danger btn-sm withdraw-project-btn" data-id="\${escapeHtml(a.id)}" style="margin-left:0.5rem;">撤回</button>\`;
                        if (a.status === '已发布') {
                            if (!a.showcaseStatus) {
                                actions += \`<button class="btn btn-primary btn-sm apply-showcase-btn" data-id="\${escapeHtml(a.id)}" style="margin-left:0.5rem;">申请作品展示</button>\`;
                            } else if (a.showcaseStatus === 'pending') {
                                actions += \`<span style="margin-left:0.5rem;color:#ff9f0a;font-size:0.85rem;">作品展示申请中</span>\`;
                            } else if (a.showcaseStatus === 'approved') {
                                actions += \`<span style="margin-left:0.5rem;color:#34c759;font-size:0.85rem;">作品展示已通过</span>\`;
                            } else if (a.showcaseStatus === 'rejected') {
                                actions += \`<span style="margin-left:0.5rem;color:#ff3b30;font-size:0.85rem;">作品展示申请已退回\${a.showcaseRejectReason ? '：' + escapeHtml(a.showcaseRejectReason) : ''}</span>\`;
                                actions += \`<button class="btn btn-primary btn-sm apply-showcase-btn" data-id="\${escapeHtml(a.id)}" style="margin-left:0.5rem;">重新申请</button>\`;
                            }
                        }
                    }
                    const reasonHtml = (a.status === '已退回' && a.rejectReason) ? \`<div style="color:#ff3b30;font-size:0.85rem;margin-top:0.25rem;">退回理由：\${escapeHtml(a.rejectReason)}</div>\` : '';
                    return \`<li>
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;flex-wrap:wrap;">
                            <span>\${escapeHtml(a.name)} <span class="badge \${statusBadgeClass(a.status)}">\${escapeHtml(a.status)}</span>\${actions}</span>
                            <span class="host-label">主持人：\${escapeHtml(a.host || '我')}</span>
                        </div>
                        \${a.description ? \`<div style="color:var(--text-muted);font-size:0.9rem;margin-top:0.35rem;line-height:1.5;">\${escapeHtml(a.description)}</div>\` : ''}
                        \${participantsLine(a)}
                        \${reasonHtml}
                    </li>\`;
                }).join('');
                projectsEl.querySelectorAll('.withdraw-project-btn').forEach(btn => btn.addEventListener('click', handleWithdrawProject));
                projectsEl.querySelectorAll('.apply-showcase-btn').forEach(btn => btn.addEventListener('click', () => openShowcaseApplyModal(btn.dataset.id)));
            }
            const featuresEl = document.getElementById('profileFeaturesList');
            featuresEl.innerHTML = myFeatures.length ? myFeatures.map(a => \`<li>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;"><span>\${escapeHtml(a.name)} <span class="badge \${statusBadgeClass(a.status)}">\${escapeHtml(a.status)}</span></span><span class="host-label">主持人：\${escapeHtml(a.host || '我')}</span></div>
                \${a.description ? \`<div style="color:var(--text-muted);font-size:0.9rem;margin-top:0.35rem;line-height:1.5;">\${escapeHtml(a.description)}</div>\` : ''}
                \${participantsLine(a)}
                \${a.status === '已退回' && a.rejectReason ? \`<div style="color:#ff3b30;font-size:0.85rem;margin-top:0.25rem;">退回理由：\${escapeHtml(a.rejectReason)}</div>\` : ''}
            </li>\`).join('') : '<li class="empty">暂无</li>';

            renderProfileViolations(user);
        }`);

code = replaceFunction(code, 'renderProfileViolations', `function renderProfileViolations(user) {
            const apps = getApplications();
            let violations = apps.filter(a => a.reportStatus && (a.host === user.username || (a.participants || []).includes(user.username)));
            const section = document.getElementById('profileViolationsSection');
            const list = document.getElementById('profileViolationsList');
            section.style.display = 'block';
            if (!violations.length) {
                list.innerHTML = '<li class="empty">暂无违规记录</li>';
                return;
            }
            violations = violations.slice().sort((a, b) => new Date(b.reportedAt || b.timestamp) - new Date(a.reportedAt || a.timestamp)).slice(0, 5);
            list.innerHTML = violations.map(a => {
                let adminReason = '';
                if (a.reportStatus === 'confirmed' && a.reportSupplementReason) {
                    adminReason = \`确认者补充理由：\${escapeHtml(a.reportSupplementReason)}\`;
                } else if (a.reportStatus === 'rejected' && a.reportRejectReason) {
                    adminReason = \`驳回理由：\${escapeHtml(a.reportRejectReason)}\`;
                }
                return \`<li>
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;">
                        <span>\${escapeHtml(a.name)} <span class="badge badge-rejected">\${escapeHtml(a.status)}</span></span>
                        <span class="host-label">主持人：\${escapeHtml(a.host || '未知')}</span>
                    </div>
                    <div style="color:#ff3b30;font-size:0.85rem;margin-top:0.25rem;">举报人理由：\${escapeHtml(a.reportReason || '无')}</div>
                    \${adminReason ? \`<div style="color:#ff9f0a;font-size:0.85rem;margin-top:0.25rem;">\${adminReason}</div>\` : ''}
                </li>\`;
            }).join('');
        }`);

code = replaceFunction(code, 'finalizeLogin', `async function finalizeLogin(user) {
            clearLockout(user.username);
            setCurrentSession({ username: user.username, role: user.role, loginAt: new Date().toISOString() });
            addAdminLog({ type: 'login', username: user.username, role: user.role, success: true, reason: '登录成功' });
            renderNavUser();
            closeAuthModal();
            resetAdminLoginUI();
            renderProjectLists();
            renderFeatureList();
            renderAdminDashboard();
            showToast('登录成功');
            resetSessionTimer();
            if (user.dismissed && user.dismissReason && !user.dismissNoticeAcked) {
                const map = getNotifications();
                const list = map[user.username] || [];
                if (!list.some(n => n.type === 'dismiss')) {
                    addNotification(user.username, { title: '权限降级通知', message: \`您已被辞退，权限降级，辞退理由为：\${escapeHtml(user.dismissReason)}\`, type: 'dismiss' });
                }
            }
            renderNavNotifications();
            const unread = getUnreadCount(user.username);
            if (unread > 0) {
                setTimeout(() => openMailNotificationsModal(), 300);
            }
        }`);

code = replaceFunction(code, 'renderNavUser', `function renderNavUser() {
            const session = getCurrentSession();
            if (!session) {
                navUserBtn.className = 'btn btn-primary btn-sm';
                navUserBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> 登录';
                navUserBtn.onclick = () => openAuthModal('login');
                navUserMenu.style.display = 'none';
                return;
            }
            const user = findUser(session.username);
            if (!user) { logout(); return; }
            navUserBtn.className = 'nav-user-btn';
            navUserBtn.innerHTML = \`\${escapeHtml(user.username)} <span class="role-badge \${getRoleBadgeClass(user.role)}">\${getRoleLabel(user.role)}</span>\`;
            navUserBtn.onclick = () => { navUserMenu.style.display = navUserMenu.style.display === 'block' ? 'none' : 'block'; };
            navUserMenu.style.display = 'none';
            renderNavNotifications();
        }`);

code = replaceFunction(code, 'handleApproveRegistration', `async function handleApproveRegistration(id, approve) {
            const regs = getRegistrations();
            const idx = regs.findIndex(r => r.id === id);
            if (idx < 0) return;
            const reg = regs[idx];
            const session = getCurrentSession();
            const currentUsername = session ? session.username : '';
            if (reg.username === currentUsername) { showToast('不能处理自己的管理员申请', 'error'); return; }
            reg.status = approve ? '已批准' : '已拒绝';
            setRegistrations(regs);
            if (approve) {
                const users = getUsers();
                const userIdx = users.findIndex(u => u.username === reg.username);
                if (userIdx >= 0) {
                    users[userIdx].role = '管理员';
                    if (reg.contact && !users[userIdx].contact) users[userIdx].contact = reg.contact;
                } else {
                    users.push({ username: reg.username, passwordHash: reg.passwordHash, salt: reg.salt, role: '管理员', contact: reg.contact, createdAt: new Date().toISOString(), forceChangePassword: false });
                }
                setUsers(users);
            }
            addAdminLog({ type: 'registration_review', username: reg.username, approved: approve, operator: currentUsername });
            showToast(approve ? '已批准该管理员申请' : '已拒绝该管理员申请');
            renderRegistrations();
            renderUserList();
        }`);

code = replaceFunction(code, 'renderRegistrations', `function renderRegistrations() {
            const el = document.getElementById('panel-registrations');
            const regs = getRegistrations();
            const session = getCurrentSession();
            const currentUsername = session ? session.username : '';
            if (!regs.length) { el.innerHTML = '<div class="empty-state">暂无管理员申请</div>'; return; }
            let html = '<div class="admin-table-scroll"><table class="admin-table"><thead><tr><th>申请人</th><th>联系方式（脱敏）</th><th>申请角色</th><th>状态</th><th>申请时间</th><th>操作</th></tr></thead><tbody>';
            regs.forEach(reg => {
                const isSelf = reg.username === currentUsername;
                let actionCell = '';
                if (reg.status === '待处理') {
                    if (isSelf) {
                        actionCell = '<span style="color:#8e8e93;font-size:0.85rem;">不能处理自己的申请</span>';
                    } else {
                        actionCell = \`<button class="btn btn-primary btn-sm approve-reg" data-id="\${escapeHtml(reg.id)}">批准</button> <button class="btn btn-danger btn-sm reject-reg" data-id="\${escapeHtml(reg.id)}">拒绝</button>\`;
                    }
                }
                html += \`<tr>
                    <td>\${escapeHtml(reg.username)}</td>
                    <td>\${maskContact(reg.contact)}</td>
                    <td>\${escapeHtml(reg.role)}</td>
                    <td><span class="badge \${reg.status === '待处理' ? 'badge-pending' : reg.status === '已批准' ? 'badge-approved' : 'badge-rejected'}">\${escapeHtml(reg.status)}</span></td>
                    <td>\${new Date(reg.createdAt).toLocaleString()}</td>
                    <td>\${actionCell}</td>
                </tr>\`;
            });
            html += '</tbody></table></div>';
            el.innerHTML = html;
            el.querySelectorAll('.approve-reg').forEach(btn => btn.addEventListener('click', () => handleApproveRegistration(btn.dataset.id, true)));
            el.querySelectorAll('.reject-reg').forEach(btn => btn.addEventListener('click', () => handleApproveRegistration(btn.dataset.id, false)));
        }`);

code = replaceFunction(code, 'handleDismissAdmin', `async function handleDismissAdmin(e) {
            const username = e.target.dataset.username;
            if (username === DEFAULT_TAO_USERNAME) { showToast('不能辞退 TAO 账号', 'error'); return; }
            const reason = await showModal('辞退管理员', \`确定要辞退管理员 \${escapeHtml(username)} 吗？请填写理由。\`, { input: true, confirmText: '确认辞退' });
            if (reason === null || reason === undefined) return;
            const r = reason.trim();
            if (!r) { showToast('理由不能为空', 'error'); return; }
            let users = getUsers();
            const idx = users.findIndex(u => u.username === username);
            if (idx < 0) { showToast('用户不存在', 'error'); return; }
            const target = users[idx];
            target.role = '用户';
            target.dismissed = true;
            target.dismissReason = r;
            target.dismissNoticeAcked = false;
            target.idBanUntil = Date.now() + 15 * 24 * 60 * 60 * 1000;
            setUsers(users);
            addNotification(username, { title: '权限降级通知', message: \`您已被辞退，权限降级，辞退理由为：\${r}\`, type: 'dismiss' });
            addAdminLog({ type: 'dismiss_admin', username, operator: getCurrentSession().username, reason: r });
            showToast('管理员已辞退');
            renderUserList();
            renderApplicationsManagement('站长');
        }`);

code = replaceFunction(code, 'renderUserList', `function renderUserList() {
            const el = document.getElementById('panel-users');
            const users = getUsers();
            const session = getCurrentSession();
            const currentUser = session ? findUser(session.username) : null;
            const isRoot = currentUser && currentUser.role === '站长';
            if (!users.length) { el.innerHTML = '<div class="empty-state">暂无用户</div>'; return; }
            let html = \`<div class="admin-table-scroll"><table class="admin-table"><thead><tr><th>用户名</th><th>联系方式（脱敏）</th><th>权限等级</th><th>注册时间</th>\${isRoot ? '<th>操作</th>' : ''}</tr></thead><tbody>\`;
            users.forEach(u => {
                const contactDisplay = u.contact ? maskContact(u.contact) : '<span style="color:#ff9f0a;">请到个人信息页面补全个人信息</span>';
                let actionCell = '-';
                if (isRoot && u.username !== DEFAULT_TAO_USERNAME && u.role === '管理员') {
                    actionCell = \`<button class="btn btn-danger btn-sm dismiss-admin-btn" data-username="\${escapeHtml(u.username)}" style="background:#ff3b30; color:#fff; border-color:#ff3b30;">辞退</button>\`;
                }
                html += \`<tr>
                    <td>\${escapeHtml(u.username)}</td>
                    <td>\${contactDisplay}</td>
                    <td><span class="badge \${getRoleBadgeClass(u.role)}">\${getRoleLabel(u.role)}</span></td>
                    <td>\${new Date(u.createdAt).toLocaleString()}</td>
                    \${isRoot ? \`<td>\${actionCell}</td>\` : ''}
                </tr>\`;
            });
            html += '</tbody></table></div>';
            el.innerHTML = html;
            if (isRoot) {
                el.querySelectorAll('.dismiss-admin-btn').forEach(btn => btn.addEventListener('click', handleDismissAdmin));
            }
        }`);

code = replaceFunction(code, 'renderApplicationsManagement', `function renderApplicationsManagement(role) {
            const el = document.getElementById('panel-applications');
            const apps = getApplications();
            apps.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            if (!apps.length) { el.innerHTML = '<div class="empty-state">暂无申请记录</div>'; return; }
            const session = getCurrentSession();
            const currentUser = session ? findUser(session.username) : null;
            const currentUsername = currentUser ? currentUser.username : '';
            const isRoot = currentUser && currentUser.role === '站长';
            let html = '<div class="admin-table-scroll"><table class="admin-table"><thead><tr><th>类型</th><th>名称</th><th>分类</th><th>主持人</th><th>联系方式</th><th>文件</th><th>提交时间</th><th>状态</th></tr></thead><tbody>';
            apps.forEach(app => {
                const fileCell = renderFileCell(app, role);
                const isSelf = currentUsername && (app.host === currentUsername || (app.participants || []).includes(currentUsername));
                let statusCell;
                if (app.showcaseStatus === 'approved') {
                    statusCell = \`<span class="badge badge-approved">已展示</span>\`;
                    if (app.reportStatus === 'pending') statusCell += \` <span class="badge badge-pending" style="margin-left:0.25rem;">举报审核中</span>\`;
                    else if (app.reportStatus === 'confirmed') statusCell += \` <span class="badge badge-rejected" style="margin-left:0.25rem;">违规已确认</span>\`;
                    else if (app.reportStatus === 'rejected') statusCell += \` <span class="badge badge-approved" style="margin-left:0.25rem;">举报已驳回</span>\`;
                } else {
                    const nextStatuses = !isSelf && canManageStatus(role, app.status) ? getAllowedNextStatuses(app.status) : [];
                    statusCell = nextStatuses.length > 1 ? \`<select data-id="\${escapeHtml(app.id)}" class="status-select">\${nextStatuses.map(s => \`<option value="\${s}" \${app.status === s ? 'selected' : ''}>\${s}</option>\`).join('')}</select>\` : \`<span class="badge \${getStatusBadgeClass(app.status)}">\${escapeHtml(app.status)}</span>\`;
                }
                const showcaseActions = [];
                if (!isSelf && role === '站长' && app.status === '已发布') {
                    if (app.showcaseStatus === 'pending') {
                        showcaseActions.push(\`<button class="btn btn-primary btn-sm approve-showcase-btn" data-id="\${escapeHtml(app.id)}" style="margin-left:0.5rem;">批准作品展示</button>\`);
                        showcaseActions.push(\`<button class="btn btn-danger btn-sm reject-showcase-btn" data-id="\${escapeHtml(app.id)}" style="margin-left:0.5rem;">退回作品展示</button>\`);
                    } else if (app.showcaseStatus === 'approved') {
                        showcaseActions.push('<span style="margin-left:0.5rem;color:#34c759;font-size:0.85rem;">作品展示已批准</span>');
                    } else if (app.showcaseStatus === 'rejected') {
                        showcaseActions.push(\`<span style="margin-left:0.5rem;color:#ff3b30;font-size:0.85rem;">作品展示已退回\${app.showcaseRejectReason ? '：' + escapeHtml(app.showcaseRejectReason) : ''}</span>\`);
                    }
                }
                if (isRoot) {
                    showcaseActions.push(\`<button class="btn btn-danger btn-sm delete-app-btn" data-id="\${escapeHtml(app.id)}" style="margin-left:0.5rem;">删除</button>\`);
                }
                html += \`<tr>
                    <td>\${escapeHtml(app.type)}</td>
                    <td>\${escapeHtml(app.name)}</td>
                    <td>\${escapeHtml(app.category)}</td>
                    <td>\${escapeHtml(app.host || '访客')}</td>
                    <td>\${escapeHtml(app.contact)}</td>
                    <td>\${fileCell}</td>
                    <td>\${new Date(app.timestamp).toLocaleString()}</td>
                    <td>\${statusCell}\${showcaseActions.join('')}</td>
                </tr>\`;
                html += \`<tr><td colspan="8" style="background:#f9f9fb; color:var(--text-muted); font-size:0.9rem; padding:0.75rem 1rem; border-top:none;"><strong>描述：</strong>\${escapeHtml(app.description)}</td></tr>\`;
            });
            html += '</tbody></table></div>';
            el.innerHTML = html;
            if (role === '站长' || role === '管理员') {
                el.querySelectorAll('.status-select').forEach(sel => sel.addEventListener('change', async e => {
                    const id = e.target.dataset.id;
                    const newStatus = e.target.value;
                    const allApps = getApplications();
                    const app = allApps.find(a => a.id === id);
                    if (!app) return;
                    const session = getCurrentSession();
                    const currentUsername = session ? session.username : '';
                    if (currentUsername && (app.host === currentUsername || (app.participants || []).includes(currentUsername))) {
                        showToast('不能处理自己的项目/功能', 'error');
                        renderApplicationsManagement(role);
                        return;
                    }
                    if (!canManageStatus(role, app.status)) {
                        showToast('无权修改该项目状态', 'error');
                        renderApplicationsManagement(role);
                        return;
                    }
                    let rejectReason = '';
                    if (newStatus === '已退回') {
                        const reason = await showModal('退回理由', '请填写退回理由', { input: true, confirmText: '确认' });
                        if (reason === null || reason === undefined) {
                            app.status = '待处理';
                            app.rejectReason = '';
                            setApplications(allApps);
                            renderApplicationsManagement(role);
                            return;
                        }
                        rejectReason = reason.trim();
                        if (!rejectReason) {
                            showToast('退回理由不能为空', 'error');
                            app.status = '待处理';
                            app.rejectReason = '';
                            setApplications(allApps);
                            renderApplicationsManagement(role);
                            return;
                        }
                    }
                    const oldStatus = app.status;
                    app.status = newStatus;
                    app.rejectReason = rejectReason || '';
                    setApplications(allApps);
                    addAdminLog({ type: 'status_change', applicationId: id, applicationName: app.name, operator: currentUsername, oldStatus, newStatus, reason: rejectReason });
                    showToast('状态已更新');
                    resetSessionTimer();
                    renderProjectLists();
                    renderFeatureList();
                    renderApplicationsManagement(role);
                }));
            }
            el.querySelectorAll('.approve-showcase-btn').forEach(btn => btn.addEventListener('click', () => handleShowcaseReview(btn.dataset.id, true)));
            el.querySelectorAll('.reject-showcase-btn').forEach(btn => btn.addEventListener('click', () => handleShowcaseReview(btn.dataset.id, false)));
            el.querySelectorAll('.delete-app-btn').forEach(btn => btn.addEventListener('click', () => handleDeleteApplication(btn.dataset.id)));
        }`);

code = replaceFunction(code, 'renderViolations', `function renderViolations() {
            const el = document.getElementById('panel-violations');
            const session = getCurrentSession();
            const currentUser = session ? findUser(session.username) : null;
            const currentUsername = currentUser ? currentUser.username : '';
            const apps = getApplications().filter(a => a.reportStatus);
            apps.sort((a, b) => new Date(b.reportedAt || b.timestamp) - new Date(a.reportedAt || a.timestamp));
            if (!apps.length) { el.innerHTML = '<div class="empty-state">暂无违规处理记录</div>'; return; }
            let html = '<div class="admin-table-scroll"><table class="admin-table"><thead><tr><th>项目/功能</th><th>主持人</th><th>举报人</th><th>举报理由</th><th>状态</th><th>操作</th></tr></thead><tbody>';
            apps.forEach(app => {
                let statusLabel = '待处理';
                let statusClass = 'badge-pending';
                if (app.reportStatus === 'confirmed') { statusLabel = '已确认'; statusClass = 'badge-rejected'; }
                else if (app.reportStatus === 'rejected') { statusLabel = '已驳回'; statusClass = 'badge-approved'; }
                const isSelf = currentUsername && (app.host === currentUsername || (app.participants || []).includes(currentUsername) || app.reportReporter === currentUsername);
                let actions = '';
                if (app.reportStatus === 'pending') {
                    if (isSelf) {
                        actions = '<span style="color:#8e8e93;font-size:0.85rem;">不能处理自己的举报请求</span>';
                    } else {
                        actions = \`<button class="btn btn-danger btn-sm confirm-violation-btn" data-id="\${escapeHtml(app.id)}" style="margin-right:0.5rem;">确认</button><button class="btn btn-secondary btn-sm reject-violation-btn" data-id="\${escapeHtml(app.id)}">驳回</button>\`;
                    }
                } else {
                    const extra = app.reportStatus === 'confirmed' && app.reportSupplementReason ? \`补充：\${escapeHtml(app.reportSupplementReason)}\` : (app.reportStatus === 'rejected' && app.reportRejectReason ? \`驳回：\${escapeHtml(app.reportRejectReason)}\` : '-');
                    actions = \`<span style="color:var(--text-muted);font-size:0.85rem;">\${extra}</span>\`;
                }
                html += \`<tr>
                    <td>\${escapeHtml(app.name)}</td>
                    <td>\${escapeHtml(app.host || '未知')}</td>
                    <td>\${escapeHtml(app.reportReporter || '访客')}</td>
                    <td>\${escapeHtml(app.reportReason || '-')}</td>
                    <td><span class="badge \${statusClass}">\${statusLabel}</span></td>
                    <td>\${actions}</td>
                </tr>\`;
            });
            html += '</tbody></table></div>';
            el.innerHTML = html;
            el.querySelectorAll('.confirm-violation-btn').forEach(btn => btn.addEventListener('click', () => handleViolationReview(btn.dataset.id, true)));
            el.querySelectorAll('.reject-violation-btn').forEach(btn => btn.addEventListener('click', () => handleViolationReview(btn.dataset.id, false)));
        }`);

code = replaceFunction(code, 'handleViolationReview', `async function handleViolationReview(id, confirm) {
            const allApps = getApplications();
            const app = allApps.find(a => a.id === id);
            if (!app || app.reportStatus !== 'pending') return;
            const session = getCurrentSession();
            const currentUsername = session ? session.username : '';
            if (currentUsername && (app.host === currentUsername || (app.participants || []).includes(currentUsername) || app.reportReporter === currentUsername)) {
                showToast('不能处理自己的举报请求', 'error'); return;
            }
            if (confirm) {
                const reason = await showModal('确认违规', '请填写补充理由（非必填）', { input: true, confirmText: '确认违规' });
                if (reason === null || reason === undefined) return;
                app.reportStatus = 'confirmed';
                app.reportSupplementReason = reason.trim();
                app.status = '已退回';
                addAdminLog({ type: 'violation_confirm', applicationId: id, applicationName: app.name, operator: currentUsername, reason: app.reportSupplementReason });
            } else {
                const reason = await showModal('驳回违规举报', '请填写驳回理由', { input: true, confirmText: '确认驳回' });
                if (reason === null || reason === undefined) return;
                const r = reason.trim();
                if (!r) { showToast('驳回理由不能为空', 'error'); return; }
                app.reportStatus = 'rejected';
                app.reportRejectReason = r;
                addAdminLog({ type: 'violation_reject', applicationId: id, applicationName: app.name, operator: currentUsername, reason: r });
                if (app.reportReporter && app.reportReporter !== '访客') {
                    addNotification(app.reportReporter, { title: '举报驳回通知', message: \`您举报的《\${app.name}》已被驳回，理由为：\${r}\`, type: 'report_rejected' });
                }
            }
            setApplications(allApps);
            showToast(confirm ? '已确认违规并退回项目' : '已驳回违规举报');
            renderViolations();
            renderApplicationsManagement(getCurrentSession() ? findUser(getCurrentSession().username)?.role : '');
            renderProjectLists();
            renderFeatureList();
            renderProfile();
        }`);

code = replaceFunction(code, 'handleShowcaseReview', `async function handleShowcaseReview(id, approve) {
            const allApps = getApplications();
            const app = allApps.find(a => a.id === id);
            if (!app) return;
            const session = getCurrentSession();
            const currentUsername = session ? session.username : '';
            if (currentUsername && (app.host === currentUsername || (app.participants || []).includes(currentUsername))) {
                showToast('不能处理自己的作品展示申请', 'error'); return;
            }
            if (approve) {
                app.showcaseStatus = 'approved';
                app.showcaseRejectReason = '';
            } else {
                const reason = await showModal('退回作品展示申请', '请填写退回理由', { input: true, confirmText: '确认' });
                if (reason === null || reason === undefined) return;
                const r = reason.trim();
                if (!r) { showToast('退回理由不能为空', 'error'); return; }
                app.showcaseStatus = 'rejected';
                app.showcaseRejectReason = r;
            }
            setApplications(allApps);
            addAdminLog({ type: 'showcase_review', applicationId: id, applicationName: app.name, operator: currentUsername, approved: approve });
            showToast(approve ? '已批准作品展示申请' : '已退回作品展示申请');
            renderApplicationsManagement('站长');
            renderProfile();
            renderProjectList();
        }`);

code = addAfterMarker(code, "renderProjectList();\n        }", `

        async function handleDeleteApplication(id) {
            const apps = getApplications();
            const app = apps.find(a => a.id === id);
            if (!app) return;
            const ok = await showModal('删除项目/功能', \`确定要删除《\${app.name}》吗？删除后不可恢复，相关数据将被清除。\`, { confirmText: '确认删除' });
            if (!ok) return;
            const newApps = apps.filter(a => a.id !== id);
            setApplications(newApps);
            if (app.host && app.host !== '访客' && app.host !== '已注销用户') {
                addNotification(app.host, { title: '项目/功能删除通知', message: \`您提交的项目/功能《\${app.name}》已被站长删除\`, type: 'delete_app' });
            }
            addAdminLog({ type: 'delete_app', applicationId: id, applicationName: app.name, operator: (getCurrentSession() || {}).username, reason: '站长删除' });
            showToast('已删除项目/功能');
            renderApplicationsManagement('站长');
            renderProjectLists();
            renderFeatureList();
            renderProfile();
            renderViolations();
        }`);

code = replaceFunction(code, 'renderLogs', `function renderLogs() {
            const el = document.getElementById('panel-logs');
            const logs = getAdminLogs().slice().reverse();
            let html = '<div style="display:flex; justify-content:flex-end; margin-bottom:1rem;"><button class="btn btn-danger btn-sm" id="clearLogsBtn" style="background:#ff3b30; color:#fff; border-color:#ff3b30; box-shadow:0 4px 12px rgba(255,59,48,0.35);"><i class="fas fa-trash-alt"></i> 清空日志</button></div>';
            if (!logs.length) { el.innerHTML = html + '<div class="empty-state">暂无操作日志</div>'; return; }
            html += '<div class="admin-table-scroll"><table class="admin-table"><thead><tr><th>时间</th><th>类型</th><th>用户</th><th>详情</th></tr></thead><tbody>';
            logs.forEach(log => {
                let detail = '';
                if (log.type === 'login') detail = (log.success ? '登录成功' : '登录失败') + (log.reason ? \` - \${log.reason}\` : '');
                else if (log.type === 'logout') detail = '退出登录';
                else if (log.type === 'register') detail = \`注册为 \${log.role}\` + (log.status ? \` (\${log.status})\` : '');
                else if (log.type === 'registration_review') detail = (log.approved ? '批准' : '拒绝') + \` \${log.username} 的管理员申请\`;
                else if (log.type === 'status_change') detail = \`\${log.applicationName}: \${log.oldStatus} → \${log.newStatus}\` + (log.reason ? \`（理由：\${log.reason}）\` : '');
                else if (log.type === 'password_reset') detail = '重置密码';
                else if (log.type === 'profile_submit') detail = \`提交\${log.itemType} \${log.itemName}\`;
                else if (log.type === 'withdraw') detail = \`撤回项目 \${log.applicationName}\`;
                else if (log.type === 'showcase_apply') detail = \`申请作品展示 \${log.applicationName}\`;
                else if (log.type === 'showcase_review') detail = \`作品展示申请\${log.approved ? '批准' : '退回'} \${log.applicationName}\`;
                else if (log.type === 'delete_user') detail = \`辞退/注销用户 \${log.username}\` + (log.reason ? \`（理由：\${log.reason}）\` : '');
                else if (log.type === 'dismiss_admin') detail = \`辞退管理员 \${log.username}\` + (log.reason ? \`（理由：\${log.reason}）\` : '');
                else if (log.type === 'violation_report') detail = \`举报 \${log.applicationName}（举报人：\${log.reporter || '访客'}）\` + (log.reason ? \`：\${log.reason}\` : '');
                else if (log.type === 'violation_confirm') detail = \`确认违规 \${log.applicationName}\` + (log.reason ? \`（补充：\${log.reason}）\` : '');
                else if (log.type === 'violation_reject') detail = \`驳回违规 \${log.applicationName}\` + (log.reason ? \`（理由：\${log.reason}）\` : '');
                else if (log.type === 'delete_app') detail = \`删除项目/功能 \${log.applicationName}\` + (log.reason ? \`（\${log.reason}）\` : '');
                else detail = JSON.stringify(log);
                html += \`<tr><td>\${new Date(log.timestamp).toLocaleString()}</td><td>\${escapeHtml(log.type)}</td><td>\${escapeHtml(log.username || log.operator || '-')}</td><td>\${escapeHtml(detail)}</td></tr>\`;
            });
            html += '</tbody></table></div>';
            el.innerHTML = html;
            document.getElementById('clearLogsBtn').addEventListener('click', handleClearLogs);
        }`);

// form handlers
code = code.replace(
    "saveApplication('功能', fd.get('featureName'), fd.get('featureType'), fd.get('featureDesc'), contact, session ? session.username : '访客');",
    "const featureParticipants = (fd.get('participants') || '').split(/[,，]/).map(s => s.trim()).filter(Boolean);\n            saveApplication('功能', fd.get('featureName'), fd.get('featureType'), fd.get('featureDesc'), contact, session ? session.username : '访客', featureParticipants);"
);
code = code.replace(
    "saveApplication('项目', fd.get('projectName'), fd.get('projectType'), fd.get('projectDesc'), contact, session ? session.username : '访客');",
    "const projectParticipants = (fd.get('participants') || '').split(/[,，]/).map(s => s.trim()).filter(Boolean);\n            saveApplication('项目', fd.get('projectName'), fd.get('projectType'), fd.get('projectDesc'), contact, session ? session.username : '访客', projectParticipants);"
);

const oldProfileSubmit = `            if (existing && existing.status !== '已退回') {
                if (file) {
                    existing.fileName = fileName;
                    existing.fileType = fileType;
                    existing.fileSize = fileSize;
                    existing.fileData = fileData;
                    existing.timestamp = new Date().toISOString();
                    setApplications(apps);
                    addAdminLog({ type: 'profile_submit', username: session.username, itemType: type, itemName: name, success: true, note: '追加改动' });
                    showToast('已在原申请上更新文件改动');
                } else {
                    showToast('已存在相同/相似申请，请等待处理或退回后重新申请', 'error');
                    return;
                }
            } else {
                apps.push({
                    id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                    type,
                    name: sanitizeInput(name),
                    category: type === '项目' ? '已有项目' : '已有功能',
                    description: sanitizeInput(desc),
                    purpose: sanitizeInput(purpose),
                    contact: user.contact || '',
                    host: session.username,
                    participants: [session.username],
                    fileName,
                    fileType,
                    fileSize,
                    fileData,
                    timestamp: new Date().toISOString(),
                    status: '待处理'
                });
                setApplications(apps);
                addAdminLog({ type: 'profile_submit', username: session.username, itemType: type, itemName: name, success: true });
                showToast('提交成功');
            }`;
const newProfileSubmit = `            const newParticipants = (fd.get('participants') || '').split(/[,，]/).map(s => s.trim()).filter(Boolean);
            if (existing && existing.status !== '已退回') {
                if (file) {
                    existing.fileName = fileName;
                    existing.fileType = fileType;
                    existing.fileSize = fileSize;
                    existing.fileData = fileData;
                    existing.timestamp = new Date().toISOString();
                    newParticipants.forEach(p => { if (!existing.participants.includes(p)) existing.participants.push(p); });
                    setApplications(apps);
                    addAdminLog({ type: 'profile_submit', username: session.username, itemType: type, itemName: name, success: true, note: '追加改动' });
                    showToast('已在原申请上更新文件改动');
                } else {
                    showToast('已存在相同/相似申请，请等待处理或退回后重新申请', 'error');
                    return;
                }
            } else {
                const participants = [session.username];
                newParticipants.forEach(p => { if (!participants.includes(p)) participants.push(p); });
                apps.push({
                    id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                    type,
                    name: sanitizeInput(name),
                    category: type === '项目' ? '已有项目' : '已有功能',
                    description: sanitizeInput(desc),
                    purpose: sanitizeInput(purpose),
                    contact: user.contact || '',
                    host: session.username,
                    participants,
                    fileName,
                    fileType,
                    fileSize,
                    fileData,
                    timestamp: new Date().toISOString(),
                    status: '待处理'
                });
                setApplications(apps);
                addAdminLog({ type: 'profile_submit', username: session.username, itemType: type, itemName: name, success: true });
                showToast('提交成功');
            }`;
if (!code.includes(oldProfileSubmit)) throw new Error('Profile submit block not found');
code = code.replace(oldProfileSubmit, newProfileSubmit);

// mail modal event listeners
code = code.replace(
    "document.getElementById('navProfileBtn').addEventListener('click', e => { e.preventDefault(); openProfileModal(); });",
    `document.getElementById('navProfileBtn').addEventListener('click', e => { e.preventDefault(); openProfileModal(); });
        document.getElementById('navMailNotifyBtn').addEventListener('click', e => { e.preventDefault(); openMailNotificationsModal(); });
        document.getElementById('mailNotifyClose').addEventListener('click', closeMailNotificationsModal);
        document.getElementById('mailNotifyModal').addEventListener('click', e => { if (e.target === document.getElementById('mailNotifyModal')) closeMailNotificationsModal(); });`
);

fs.writeFileSync(FILE, code, 'utf-8');
console.log('Done.');
