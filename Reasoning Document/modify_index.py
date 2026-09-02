# -*- coding: utf-8 -*-
import re

FILE = r'd:\Application\AllToolsSet\Herb\Smart-Chinese-Herbal-Medicine-Recognition-App\index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace saveApplication function
old_save = r'''        // ===================== Application forms =====================
        function saveApplication(type, name, category, description, contact) {
            const apps = safeJsonParse(localStorage.getItem('applications'), []);
            apps.push({
                id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                type,
                name: sanitizeInput(name),
                category: sanitizeInput(category),
                description: sanitizeInput(description),
                contact: sanitizeInput(contact),
                timestamp: new Date().toISOString(),
                status: '待处理'
            });
            localStorage.setItem('applications', JSON.stringify(apps));
            showToast('申请已提交，我会尽快查看并回复你');
        }'''

new_save = r'''        // ===================== Application forms =====================
        function saveApplication(type, name, category, description, contact, host = '访客') {
            const apps = getApplications();
            apps.push({
                id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
                type,
                name: sanitizeInput(name),
                category: sanitizeInput(category),
                description: sanitizeInput(description),
                contact: sanitizeInput(contact),
                host,
                participants: [host],
                timestamp: new Date().toISOString(),
                status: '待处理'
            });
            setApplications(apps);
            showToast('申请已提交，我会尽快查看并回复你');
        }'''

if old_save not in content:
    raise ValueError('saveApplication block not found')
content = content.replace(old_save, new_save)

# 2. Replace public form handlers
old_handlers = r'''        document.getElementById('featureApplyForm').addEventListener('submit', e => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const contact = fd.get('contact');
            if (!validateContact(contact)) { showToast('请填写有效的联系方式', 'error'); return; }
            saveApplication('功能', fd.get('featureName'), fd.get('featureType'), fd.get('featureDesc'), contact);
            e.target.reset();
        });
        document.getElementById('projectApplyForm').addEventListener('submit', e => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const contact = fd.get('contact');
            if (!validateContact(contact)) { showToast('请填写有效的联系方式', 'error'); return; }
            saveApplication('项目', fd.get('projectName'), fd.get('projectType'), fd.get('projectDesc'), contact);
            e.target.reset();
        });'''

new_handlers = r'''        document.getElementById('featureApplyForm').addEventListener('submit', e => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const contact = fd.get('contact');
            if (!validateContact(contact)) { showToast('请填写有效的联系方式', 'error'); return; }
            const session = getCurrentSession();
            saveApplication('功能', fd.get('featureName'), fd.get('featureType'), fd.get('featureDesc'), contact, session ? session.username : '访客');
            e.target.reset();
        });
        document.getElementById('projectApplyForm').addEventListener('submit', e => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const contact = fd.get('contact');
            if (!validateContact(contact)) { showToast('请填写有效的联系方式', 'error'); return; }
            const session = getCurrentSession();
            saveApplication('项目', fd.get('projectName'), fd.get('projectType'), fd.get('projectDesc'), contact, session ? session.username : '访客');
            e.target.reset();
        });'''

if old_handlers not in content:
    raise ValueError('form handlers block not found')
content = content.replace(old_handlers, new_handlers)

# 3. Replace Admin section
start_marker = r'''        // ===================== Admin ====================='''
end_marker = r'''        // ===================== Initialize ====================='''

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
    raise ValueError('Admin section markers not found')

new_admin = r'''        // ===================== User System =====================
        // 安全提示：本用户系统为前端演示级实现，所有凭证与数据均存储在浏览器本地。
        // 上线前请务必修改默认密码与解锁码，并在生产环境中使用服务端认证替代本地逻辑。
        const DEFAULT_TAO_USERNAME = 'TAO';
        const DEFAULT_TAO_PASSWORD = 'Admin@2026#Secure';
        const TAO_ROOT_CODE = 'TAO_ROOT_2026';
        const ADMIN_LOCK_CODE = 'Admin-N9567ueHS-TAO-KKAp25RASD2Q34';
        const LOCKOUT_LIMIT = 5;
        const LOCKOUT_DURATION = 15 * 60 * 1000;
        const SESSION_TIMEOUT = 30 * 60 * 1000;
        const MAX_TEMPORARY_LOCKS = 2;
        const MAX_FILE_SIZE_GB = 50;

        function generateSalt() {
            const arr = new Uint8Array(16);
            if (window.crypto) crypto.getRandomValues(arr);
            return Array.from(arr, b => b.toString(16).padStart(2, '0')).join('');
        }
        async function hashPassword(password, salt) {
            return sha256(password + '|' + salt);
        }

        // Storage helpers
        function getUsers() { return safeJsonParse(localStorage.getItem('users'), []); }
        function setUsers(users) { localStorage.setItem('users', JSON.stringify(users)); }
        function getRegistrations() { return safeJsonParse(localStorage.getItem('registrations'), []); }
        function setRegistrations(regs) { localStorage.setItem('registrations', JSON.stringify(regs)); }
        function getApplications() { return safeJsonParse(localStorage.getItem('applications'), []); }
        function setApplications(apps) { localStorage.setItem('applications', JSON.stringify(apps)); }
        function getAdminLogs() { return safeJsonParse(localStorage.getItem('adminLogs'), []); }
        function addAdminLog(log) {
            const logs = getAdminLogs();
            logs.push({ timestamp: new Date().toISOString(), ...log });
            localStorage.setItem('adminLogs', JSON.stringify(logs));
        }
        function getLockedUsers() { return safeJsonParse(localStorage.getItem('lockedUsers'), {}); }
        function setLockedUsers(locks) { localStorage.setItem('lockedUsers', JSON.stringify(locks)); }
        function getCurrentSession() { return safeJsonParse(localStorage.getItem('currentSession'), null); }
        function setCurrentSession(session) { localStorage.setItem('currentSession', JSON.stringify(session)); }
        function clearCurrentSession() { localStorage.removeItem('currentSession'); }

        async function ensureDefaultTAO() {
            const users = getUsers();
            if (!users.find(u => u.username === DEFAULT_TAO_USERNAME)) {
                const salt = generateSalt();
                users.push({
                    username: DEFAULT_TAO_USERNAME,
                    passwordHash: await hashPassword(DEFAULT_TAO_PASSWORD, salt),
                    salt,
                    role: '站长',
                    contact: '2723494508@qq.com',
                    createdAt: new Date().toISOString(),
                    forceChangePassword: true
                });
                setUsers(users);
            }
        }

        function findUser(username) {
            return getUsers().find(u => u.username === username);
        }
        function getRoleLabel(role) {
            if (role === '站长') return '站长';
            if (role === '管理员') return '管理员';
            return '用户';
        }
        function getRoleBadgeClass(role) {
            if (role === '站长') return 'badge-role-root';
            if (role === '管理员') return 'badge-role-admin';
            return 'badge-role-user';
        }

        // Lockout
        function getLockStatus(username) {
            const locks = getLockedUsers();
            return locks[username] || { failedCount: 0, lockedAt: null, permanent: false, lockHistoryCount: 0 };
        }
        function setLockStatus(username, status) {
            const locks = getLockedUsers();
            locks[username] = status;
            setLockedUsers(locks);
        }
        function isLocked(username) {
            const lock = getLockStatus(username);
            if (lock.permanent) return true;
            if (!lock.lockedAt) return false;
            return new Date().getTime() - lock.lockedAt < LOCKOUT_DURATION;
        }
        function recordFailedAttempt(username) {
            let lock = getLockStatus(username);
            lock.failedCount = (lock.failedCount || 0) + 1;
            if (lock.failedCount >= LOCKOUT_LIMIT) {
                lock.lockHistoryCount = (lock.lockHistoryCount || 0) + 1;
                lock.permanent = lock.lockHistoryCount > MAX_TEMPORARY_LOCKS;
                lock.lockedAt = new Date().getTime();
            }
            setLockStatus(username, lock);
            return lock;
        }
        function tryUnlockWithCode(username, code) {
            if (code === ADMIN_LOCK_CODE) {
                const lock = getLockStatus(username);
                const historyCount = lock.lockHistoryCount || 0;
                setLockStatus(username, { failedCount: 0, lockedAt: null, permanent: false, lockHistoryCount: historyCount });
                return true;
            }
            return false;
        }
        function clearLockout(username) {
            const lock = getLockStatus(username);
            const historyCount = lock.lockHistoryCount || 0;
            setLockStatus(username, { failedCount: 0, lockedAt: null, permanent: false, lockHistoryCount: historyCount });
        }

        // Auth modal lock display
        let authLockTimer = null;
        function updateAuthLockDisplay() {
            const username = document.getElementById('authUsername').value.trim();
            const msg = document.getElementById('authLockMessage');
            const lockCodeInput = document.getElementById('authLockCode');
            const loginBtn = document.getElementById('authLoginSubmit');
            if (!username) { msg.style.display = 'none'; lockCodeInput.disabled = true; loginBtn.disabled = false; return false; }
            const locked = isLocked(username);
            if (locked) {
                msg.style.display = 'block';
                lockCodeInput.disabled = false;
                loginBtn.innerHTML = '<i class="fas fa-unlock-alt"></i> 解除锁定';
                loginBtn.classList.remove('btn-primary');
                loginBtn.classList.add('btn-secondary');
                startAuthLockCountdown(username);
            } else {
                msg.style.display = 'none';
                lockCodeInput.disabled = true;
                loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> 登录';
                loginBtn.classList.add('btn-primary');
                loginBtn.classList.remove('btn-secondary');
                stopAuthLockCountdown();
            }
            return locked;
        }
        function startAuthLockCountdown(username) {
            stopAuthLockCountdown();
            const msg = document.getElementById('authLockMessage');
            const tick = () => {
                const lock = getLockStatus(username);
                if (!lock || !lock.lockedAt || lock.permanent) {
                    if (lock && lock.permanent) msg.textContent = '账户已永久锁定，请输入锁定码解除';
                    return;
                }
                const elapsed = new Date().getTime() - lock.lockedAt;
                if (elapsed >= LOCKOUT_DURATION) {
                    stopAuthLockCountdown();
                    setLockStatus(username, { ...lock, failedCount: 0, lockedAt: null, permanent: false });
                    updateAuthLockDisplay();
                    return;
                }
                const remaining = Math.ceil((LOCKOUT_DURATION - elapsed) / 1000);
                msg.textContent = `账户已锁定，请 ${Math.floor(remaining / 60)} 分 ${remaining % 60} 秒后重试，或输入锁定码解除`;
            };
            tick();
            authLockTimer = setInterval(tick, 1000);
        }
        function stopAuthLockCountdown() { if (authLockTimer) { clearInterval(authLockTimer); authLockTimer = null; } }

        // Admin section lock display
        let adminLockTimer = null;
        function updateAdminLockDisplay() {
            const username = document.getElementById('adminUsername').value.trim();
            const msg = document.getElementById('lockMessage');
            const lockCodeInput = document.getElementById('adminLockCode');
            const usernameInput = document.getElementById('adminUsername');
            const passwordInput = document.getElementById('adminPassword');
            const submitBtn = document.querySelector('#adminLoginForm button[type="submit"]');
            if (!username) { msg.style.display = 'none'; lockCodeInput.disabled = true; return false; }
            const locked = isLocked(username);
            if (locked) {
                msg.style.display = 'block';
                lockCodeInput.disabled = false;
                usernameInput.disabled = true;
                passwordInput.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-unlock-alt"></i> 解除锁定';
                submitBtn.classList.remove('btn-primary');
                submitBtn.classList.add('btn-secondary');
                startAdminLockCountdown(username);
            } else {
                msg.style.display = 'none';
                lockCodeInput.disabled = true;
                usernameInput.disabled = false;
                passwordInput.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> 登录';
                submitBtn.classList.add('btn-primary');
                submitBtn.classList.remove('btn-secondary');
                stopAdminLockCountdown();
            }
            return locked;
        }
        function startAdminLockCountdown(username) {
            stopAdminLockCountdown();
            const msg = document.getElementById('lockMessage');
            const tick = () => {
                const lock = getLockStatus(username);
                if (!lock || !lock.lockedAt || lock.permanent) {
                    if (lock && lock.permanent) msg.textContent = '账户已永久锁定，请输入锁定码解除';
                    return;
                }
                const elapsed = new Date().getTime() - lock.lockedAt;
                if (elapsed >= LOCKOUT_DURATION) {
                    stopAdminLockCountdown();
                    setLockStatus(username, { ...lock, failedCount: 0, lockedAt: null, permanent: false });
                    updateAdminLockDisplay();
                    return;
                }
                const remaining = Math.ceil((LOCKOUT_DURATION - elapsed) / 1000);
                msg.textContent = `账户已锁定，请 ${Math.floor(remaining / 60)} 分 ${remaining % 60} 秒后重试，或输入锁定码解除`;
            };
            tick();
            adminLockTimer = setInterval(tick, 1000);
        }
        function stopAdminLockCountdown() { if (adminLockTimer) { clearInterval(adminLockTimer); adminLockTimer = null; } }

        // Session
        let sessionTimer = null;
        function resetSessionTimer() {
            if (sessionTimer) clearTimeout(sessionTimer);
            sessionTimer = setTimeout(() => {
                showToast('登录超时，已自动退出', 'error');
                logout();
            }, SESSION_TIMEOUT);
        }
        function clearSessionTimer() { if (sessionTimer) clearTimeout(sessionTimer); }

        // Login / logout core
        async function performLogin(username, password) {
            await ensureDefaultTAO();
            const user = findUser(username);
            if (!user) return { success: false, reason: '账号不存在' };
            const inputHash = await hashPassword(password, user.salt);
            if (inputHash !== user.passwordHash) return { success: false, reason: '密码错误' };
            return { success: true, user };
        }

        async function handleFirstLoginPasswordChange(user) {
            const newPw = await showModal('首次登录', '为了账户安全，请修改默认密码', { input: true, confirmText: '修改' });
            if (newPw && isStrongPassword(newPw)) {
                user.passwordHash = await hashPassword(newPw, user.salt);
                user.forceChangePassword = false;
                const users = getUsers();
                const idx = users.findIndex(u => u.username === user.username);
                if (idx >= 0) users[idx] = user;
                setUsers(users);
                showToast('密码修改成功');
                return true;
            } else if (newPw) {
                showToast('密码强度不足，请重新登录后修改', 'error');
                return false;
            }
            return true;
        }

        function finalizeLogin(user) {
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
        }

        function logout() {
            const session = getCurrentSession();
            if (session) addAdminLog({ type: 'logout', username: session.username, success: true, reason: '退出登录' });
            clearCurrentSession();
            clearSessionTimer();
            renderNavUser();
            renderAdminDashboard();
            showToast('已退出登录');
        }

        function resetAdminLoginUI() {
            document.getElementById('adminLoginCard').style.display = 'block';
            document.getElementById('adminDashboard').style.display = 'none';
            document.getElementById('adminPassword').value = '';
            document.getElementById('adminLockCode').value = '';
            updateAdminLockDisplay();
        }

        // Auth modal
        const authModal = document.getElementById('authModal');
        const authLoginPanel = document.getElementById('authLoginPanel');
        const authRegisterPanel = document.getElementById('authRegisterPanel');

        function openAuthModal(tab = 'login') {
            switchAuthTab(tab);
            authModal.classList.add('show');
            if (tab === 'login') document.getElementById('authUsername').focus();
        }
        function closeAuthModal() { authModal.classList.remove('show'); }
        function switchAuthTab(tab) {
            document.querySelectorAll('.auth-tab').forEach(t => t.classList.toggle('active', t.dataset.authTab === tab));
            authLoginPanel.style.display = tab === 'login' ? 'block' : 'none';
            authRegisterPanel.style.display = tab === 'register' ? 'block' : 'none';
            if (tab === 'register') updateRegisterUnlock();
        }

        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.addEventListener('click', () => switchAuthTab(tab.dataset.authTab));
        });
        document.getElementById('authCancel').addEventListener('click', closeAuthModal);
        authModal.addEventListener('click', e => { if (e.target === authModal) closeAuthModal(); });

        document.getElementById('navLoginBtn').addEventListener('click', () => openAuthModal('login'));
        document.getElementById('navLogoutBtn').addEventListener('click', e => { e.preventDefault(); logout(); });
        document.getElementById('navProfileBtn').addEventListener('click', e => { e.preventDefault(); openProfileModal(); });

        const navUserBtn = document.getElementById('navLoginBtn');
        const navUserMenu = document.getElementById('navUserMenu');
        function renderNavUser() {
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
            navUserBtn.innerHTML = `${escapeHtml(user.username)} <span class="role-badge ${getRoleBadgeClass(user.role)}">${getRoleLabel(user.role)}</span>`;
            navUserBtn.onclick = () => { navUserMenu.style.display = navUserMenu.style.display === 'block' ? 'none' : 'block'; };
            navUserMenu.style.display = 'none';
        }
        document.addEventListener('click', e => {
            if (!document.getElementById('navUserItem').contains(e.target)) navUserMenu.style.display = 'none';
        });

        // Auth login
        document.getElementById('authLoginSubmit').addEventListener('click', async () => {
            const username = document.getElementById('authUsername').value.trim();
            const password = document.getElementById('authPassword').value;
            const lockCode = document.getElementById('authLockCode').value.trim();
            if (!username || !password) { showToast('请填写用户名和密码', 'error'); return; }
            if (isLocked(username) && lockCode) {
                if (tryUnlockWithCode(username, lockCode)) { showToast('锁定已解除，请重新登录'); document.getElementById('authLockCode').value = ''; updateAuthLockDisplay(); return; }
                else { showToast('锁定码错误', 'error'); return; }
            }
            if (isLocked(username)) { showToast('账户已锁定，请输入锁定码解除', 'error'); return; }
            const result = await performLogin(username, password);
            if (!result.success) {
                const lock = recordFailedAttempt(username);
                updateAuthLockDisplay();
                if (lock.permanent) showToast(`累计锁定 ${lock.lockHistoryCount} 次，账户已永久锁定，仅能通过锁定码解除`, 'error');
                else if (isLocked(username)) showToast(`连续失败 ${LOCKOUT_LIMIT} 次，账户已锁定 15 分钟`, 'error');
                else showToast(`${result.reason}，剩余 ${Math.max(0, LOCKOUT_LIMIT - lock.failedCount)} 次机会`, 'error');
                return;
            }
            const user = result.user;
            if (user.forceChangePassword) {
                const ok = await handleFirstLoginPasswordChange(user);
                if (!ok) return;
            }
            finalizeLogin(user);
        });
        document.getElementById('authUsername').addEventListener('input', updateAuthLockDisplay);
        document.getElementById('authLockCode').addEventListener('input', e => {
            const username = document.getElementById('authUsername').value.trim();
            if (username && isLocked(username) && e.target.value.trim() === ADMIN_LOCK_CODE) {
                tryUnlockWithCode(username, e.target.value.trim());
                updateAuthLockDisplay();
                showToast('锁定已解除，请重新登录');
            }
        });

        // Admin section login
        document.getElementById('adminLoginForm').addEventListener('submit', async e => {
            e.preventDefault();
            const username = document.getElementById('adminUsername').value.trim();
            const password = document.getElementById('adminPassword').value;
            const lockCode = document.getElementById('adminLockCode').value.trim();
            if (!username || !password) { showToast('请填写用户名和密码', 'error'); return; }
            if (isLocked(username) && lockCode) {
                if (tryUnlockWithCode(username, lockCode)) { showToast('锁定已解除，请重新登录'); document.getElementById('adminLockCode').value = ''; updateAdminLockDisplay(); return; }
                else { showToast('锁定码错误', 'error'); return; }
            }
            if (isLocked(username)) { showToast('账户已锁定，请输入锁定码解除', 'error'); return; }
            const result = await performLogin(username, password);
            if (!result.success) {
                const lock = recordFailedAttempt(username);
                updateAdminLockDisplay();
                if (lock.permanent) showToast(`累计锁定 ${lock.lockHistoryCount} 次，账户已永久锁定，仅能通过锁定码解除`, 'error');
                else if (isLocked(username)) showToast(`连续失败 ${LOCKOUT_LIMIT} 次，账户已锁定 15 分钟`, 'error');
                else showToast(`${result.reason}，剩余 ${Math.max(0, LOCKOUT_LIMIT - lock.failedCount)} 次机会`, 'error');
                return;
            }
            const user = result.user;
            if (user.forceChangePassword) {
                const ok = await handleFirstLoginPasswordChange(user);
                if (!ok) return;
            }
            finalizeLogin(user);
        });
        document.getElementById('adminUsername').addEventListener('input', updateAdminLockDisplay);
        document.getElementById('adminLockCode').addEventListener('input', e => {
            const username = document.getElementById('adminUsername').value.trim();
            if (username && isLocked(username) && e.target.value.trim() === ADMIN_LOCK_CODE) {
                tryUnlockWithCode(username, e.target.value.trim());
                updateAdminLockDisplay();
                showToast('锁定已解除，请重新登录');
            }
        });
        document.getElementById('adminLogoutBtn').addEventListener('click', logout);

        // Registration
        function updateRegisterUnlock() {
            const username = document.querySelector('#registerForm input[name="registerUsername"]').value.trim();
            const group = document.getElementById('registerUnlockGroup');
            const input = group.querySelector('input');
            const role = document.querySelector('#registerForm input[name="registerRole"]:checked').value;
            if (username === DEFAULT_TAO_USERNAME || role === '站长') {
                group.style.display = 'block';
                input.required = true;
                input.disabled = false;
            } else {
                group.style.display = 'none';
                input.required = false;
                input.disabled = true;
                input.value = '';
            }
        }
        document.querySelector('#registerForm input[name="registerUsername"]').addEventListener('input', updateRegisterUnlock);
        document.querySelectorAll('#registerForm input[name="registerRole"]').forEach(r => r.addEventListener('change', updateRegisterUnlock));

        document.getElementById('registerForm').addEventListener('submit', async e => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const role = fd.get('registerRole');
            const username = fd.get('registerUsername').trim();
            const password = fd.get('registerPassword');
            const contact = fd.get('registerContact').trim();
            const unlockCode = fd.get('registerUnlockCode').trim();

            if (!username) { showToast('请填写用户名', 'error'); return; }
            if (username === DEFAULT_TAO_USERNAME && role !== '站长') { showToast('TAO 只能注册为站长', 'error'); return; }
            if (!isStrongPassword(password)) { showToast('密码强度不足，至少8位且包含大小写字母、数字和特殊字符', 'error'); return; }
            if (!validateContact(contact)) { showToast('请填写有效的联系方式', 'error'); return; }
            if (findUser(username)) { showToast('用户名已存在', 'error'); return; }

            const salt = generateSalt();
            const passwordHash = await hashPassword(password, salt);

            if (role === '站长') {
                if (username !== DEFAULT_TAO_USERNAME) { showToast('只有 TAO 可以注册为站长', 'error'); return; }
                if (unlockCode !== TAO_ROOT_CODE) { showToast('解锁码错误', 'error'); return; }
                const users = getUsers();
                users.push({ username, passwordHash, salt, role: '站长', contact, createdAt: new Date().toISOString(), forceChangePassword: false });
                setUsers(users);
                addAdminLog({ type: 'register', username, role: '站长', success: true });
                showToast('站长注册成功');
                e.target.reset();
                closeAuthModal();
                return;
            }

            if (role === '管理员') {
                const regs = getRegistrations();
                regs.push({ id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5), username, passwordHash, salt, role: '管理员', contact, status: '待处理', createdAt: new Date().toISOString() });
                setRegistrations(regs);
                addAdminLog({ type: 'register', username, role: '管理员', success: true, status: '待处理' });
                showToast('管理员申请已提交，等待 TAO 审批');
                e.target.reset();
                closeAuthModal();
                return;
            }

            const users = getUsers();
            users.push({ username, passwordHash, salt, role: '用户', contact, createdAt: new Date().toISOString(), forceChangePassword: false });
            setUsers(users);
            addAdminLog({ type: 'register', username, role: '用户', success: true });
            showToast('注册成功');
            e.target.reset();
            closeAuthModal();
        });

        // Forgot password
        const forgotPasswordModal = document.getElementById('forgotPasswordModal');
        const forgotUsername = document.getElementById('forgotUsername');
        const forgotNewPassword = document.getElementById('forgotNewPassword');
        const forgotUnlockCode = document.getElementById('forgotUnlockCode');
        const forgotSubmit = document.getElementById('forgotSubmit');

        function showForgotPasswordModal() {
            forgotUsername.value = '';
            forgotNewPassword.value = '';
            forgotUnlockCode.value = '';
            forgotUnlockCode.disabled = true;
            forgotSubmit.disabled = true;
            forgotPasswordModal.classList.add('show');
            updateForgotSubmitState();
        }
        function hideForgotPasswordModal() { forgotPasswordModal.classList.remove('show'); }
        function updateForgotSubmitState() {
            const username = forgotUsername.value.trim();
            const isTAO = username === DEFAULT_TAO_USERNAME;
            forgotUnlockCode.disabled = !isTAO;
            if (!isTAO) forgotUnlockCode.value = '';
            const code = forgotUnlockCode.value.trim();
            const newPw = forgotNewPassword.value;
            const codeOk = !isTAO || code === TAO_ROOT_CODE;
            const pwOk = newPw && isStrongPassword(newPw);
            forgotSubmit.disabled = !(codeOk && pwOk);
        }

        forgotUsername.addEventListener('input', updateForgotSubmitState);
        forgotNewPassword.addEventListener('input', updateForgotSubmitState);
        forgotUnlockCode.addEventListener('input', updateForgotSubmitState);
        document.getElementById('forgotCancel').addEventListener('click', hideForgotPasswordModal);
        forgotPasswordModal.addEventListener('click', e => { if (e.target === forgotPasswordModal) hideForgotPasswordModal(); });
        document.getElementById('forgotPasswordBtn').addEventListener('click', showForgotPasswordModal);
        document.getElementById('authForgotBtn').addEventListener('click', showForgotPasswordModal);
        document.getElementById('profileForgotBtn').addEventListener('click', showForgotPasswordModal);

        forgotSubmit.addEventListener('click', async () => {
            const username = forgotUsername.value.trim();
            const newPw = forgotNewPassword.value;
            const code = forgotUnlockCode.value.trim();
            if (!username) { showToast('请输入用户名', 'error'); return; }
            if (!isStrongPassword(newPw)) { showToast('新密码强度不足', 'error'); return; }
            if (username === DEFAULT_TAO_USERNAME && code !== TAO_ROOT_CODE) { showToast('解锁码错误', 'error'); return; }
            await ensureDefaultTAO();
            const users = getUsers();
            const idx = users.findIndex(u => u.username === username);
            if (idx < 0) { showToast('用户不存在', 'error'); return; }
            users[idx].passwordHash = await hashPassword(newPw, users[idx].salt);
            users[idx].forceChangePassword = false;
            setUsers(users);
            clearLockout(username);
            addAdminLog({ type: 'password_reset', username, success: true });
            hideForgotPasswordModal();
            showToast('密码重置成功，请使用新密码登录');
        });

        // Profile modal
        const profileModal = document.getElementById('profileModal');
        function openProfileModal() {
            const session = getCurrentSession();
            if (!session) { showToast('请先登录', 'error'); return; }
            renderProfile();
            profileModal.classList.add('show');
        }
        function closeProfileModal() { profileModal.classList.remove('show'); }
        document.getElementById('profileCloseBtn').addEventListener('click', closeProfileModal);
        profileModal.addEventListener('click', e => { if (e.target === profileModal) closeProfileModal(); });

        function renderProfile() {
            const session = getCurrentSession();
            if (!session) return;
            const user = findUser(session.username);
            if (!user) { logout(); return; }
            document.getElementById('profileUsername').textContent = user.username;
            document.getElementById('profileRole').textContent = getRoleLabel(user.role);
            document.getElementById('profileContact').textContent = user.contact || '未填写';

            const apps = getApplications();
            const myProjects = apps.filter(a => a.type === '项目' && (a.host === user.username || (a.participants || []).includes(user.username)));
            const myFeatures = apps.filter(a => a.type === '功能' && (a.host === user.username || (a.participants || []).includes(user.username)));
            const renderList = (list, el) => {
                el.innerHTML = list.length ? list.map(a => `<li>${escapeHtml(a.name)} <span class="host-label"><i class="fas fa-user"></i> 主持人：${escapeHtml(a.host || '我')}</span></li>`).join('') : '<li class="empty">暂无</li>';
            };
            renderList(myProjects, document.getElementById('profileProjectsList'));
            renderList(myFeatures, document.getElementById('profileFeaturesList'));
        }

        document.getElementById('profileSubmitForm').addEventListener('submit', async e => {
            e.preventDefault();
            const session = getCurrentSession();
            if (!session) { showToast('请先登录', 'error'); return; }
            const user = findUser(session.username);
            if (!user) { logout(); return; }
            const fd = new FormData(e.target);
            const type = fd.get('submitType');
            const name = fd.get('submitName').trim();
            const desc = fd.get('submitDesc').trim();
            const purpose = fd.get('submitPurpose').trim();
            const fileInput = e.target.querySelector('input[name="submitFile"]');
            const file = fileInput.files[0];

            if (!name || !desc || !purpose) { showToast('请填写完整信息', 'error'); return; }
            if (file && file.size > MAX_FILE_SIZE_GB * 1024 * 1024 * 1024) { showToast(`文件大小不能超过 ${MAX_FILE_SIZE_GB}GB`, 'error'); return; }

            let fileData = null, fileName = null, fileType = null, fileSize = 0;
            if (file) {
                try {
                    fileData = await new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onload = ev => resolve(ev.target.result);
                        reader.onerror = reject;
                        reader.readAsDataURL(file);
                    });
                    fileName = file.name;
                    fileType = file.type;
                    fileSize = file.size;
                } catch (err) { showToast('文件读取失败', 'error'); return; }
            }

            const apps = getApplications();
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
                status: '已发布'
            });
            setApplications(apps);
            addAdminLog({ type: 'profile_submit', username: session.username, itemType: type, itemName: name, success: true });
            showToast('提交成功');
            e.target.reset();
            renderProfile();
            renderProjectLists();
            renderFeatureList();
        });

        // Project / feature list rendering with hosts
        function renderProjectLists() {
            const apps = getApplications();
            const planned = apps.filter(a => a.type === '项目' && a.status === '待处理');
            const ongoing = apps.filter(a => a.type === '项目' && a.status === '已接受');
            const completed = apps.filter(a => a.type === '项目' && (a.status === '已发布' || a.status === '已完成'));
            const staticCompleted = [{ id: 'chinese-herb', name: '基于轻量化MobileNetV2的中药材识别系统（毕设）', host: 'TAO' }];
            const render = (list, elId, clickable) => {
                const el = document.getElementById(elId);
                if (!el) return;
                if (!list.length) { el.innerHTML = '<li class="placeholder">暂无项目</li>'; return; }
                el.innerHTML = list.map(item => {
                    const host = item.host || '访客';
                    const clickAttr = clickable ? ` data-project="${escapeHtml(item.id)}"` : '';
                    return `<li${clickAttr}><span>${escapeHtml(item.name)}</span><span class="host-label"><i class="fas fa-user"></i> 主持人：${escapeHtml(host)}</span></li>`;
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
        }

        function renderFeatureList() {
            const apps = getApplications();
            const features = apps.filter(a => a.type === '功能' && (a.status === '已发布' || a.status === '已接受'));
            const el = document.getElementById('existingFeaturesList');
            if (!el) return;
            if (!features.length) { el.innerHTML = '<li class="empty">暂无已发布功能</li>'; return; }
            el.innerHTML = features.map(f => `<li>${escapeHtml(f.name)} <span class="host-label"><i class="fas fa-user"></i> 主持人：${escapeHtml(f.host || '访客')}</span></li>`).join('');
        }

        function showProjectDetail(projectId) {
            const apps = getApplications();
            const app = apps.find(a => a.id === projectId);
            const staticDetail = projectData[projectId];
            if (!staticDetail && !app) return;

            document.getElementById('projectEmptyState').style.display = 'none';
            document.getElementById('projectDataCard').style.display = 'block';

            if (staticDetail) {
                document.getElementById('projectDataTitle').textContent = staticDetail.title;
                document.getElementById('projectDetailContent').innerHTML = `
                    <p>${escapeHtml(staticDetail.desc)}</p>
                    <p><strong>技术栈：</strong>${escapeHtml(staticDetail.tech.join(' / '))}</p>
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
            } else {
                document.getElementById('projectDataTitle').textContent = app.name;
                document.getElementById('projectDetailContent').innerHTML = `
                    <p>${escapeHtml(app.description)}</p>
                    <p><strong>用途：</strong>${escapeHtml(app.purpose || '未填写')}</p>
                    <p><strong>分类：</strong>${escapeHtml(app.category)}</p>
                `;
            }

            const card = document.getElementById('participantCard');
            card.style.display = 'block';
            document.getElementById('participantHost').textContent = app ? (app.host || '访客') : 'TAO';
            document.getElementById('participantList').textContent = app ? (app.participants || [app.host || '访客']).join('、') : 'TAO';
        }

        // Admin dashboard
        function renderAdminDashboard() {
            const session = getCurrentSession();
            if (!session) { resetAdminLoginUI(); return; }
            const user = findUser(session.username);
            if (!user) { logout(); return; }
            document.getElementById('adminLoginCard').style.display = 'none';
            document.getElementById('adminDashboard').style.display = 'block';
            const badge = document.getElementById('adminRoleBadge');
            badge.textContent = getRoleLabel(user.role);
            badge.className = 'badge ' + getRoleBadgeClass(user.role);
            renderAdminTabs(user.role);
            renderAdminTabPanels(user.role);
            resetSessionTimer();
        }

        function renderAdminTabs(role) {
            const tabs = document.getElementById('adminTabs');
            let items = [];
            if (role === '站长') {
                items = [
                    { id: 'registrations', label: '管理员申请' },
                    { id: 'users', label: '用户列表' },
                    { id: 'applications', label: '项目/功能管理' },
                    { id: 'logs', label: '操作日志' }
                ];
            } else if (role === '管理员') {
                items = [{ id: 'applications', label: '项目/功能管理' }];
            } else {
                items = [{ id: 'applications', label: '项目/功能列表' }];
            }
            tabs.innerHTML = items.map((item, idx) => `<button class="admin-tab ${idx === 0 ? 'active' : ''}" data-tab="${item.id}">${item.label}</button>`).join('');
            tabs.querySelectorAll('.admin-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    tabs.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    document.querySelectorAll('.admin-tab-panel').forEach(p => p.classList.remove('active'));
                    document.getElementById('panel-' + tab.dataset.tab).classList.add('active');
                });
            });
        }

        function renderAdminTabPanels(role) {
            const panels = document.getElementById('adminTabPanels');
            let html = '';
            if (role === '站长') {
                html += '<div class="admin-tab-panel active" id="panel-registrations"></div>';
                html += '<div class="admin-tab-panel" id="panel-users"></div>';
            }
            html += '<div class="admin-tab-panel ' + (role !== '站长' ? 'active' : '') + '" id="panel-applications"></div>';
            if (role === '站长') html += '<div class="admin-tab-panel" id="panel-logs"></div>';
            panels.innerHTML = html;
            if (role === '站长') { renderRegistrations(); renderUserList(); renderLogs(); }
            renderApplicationsManagement(role);
        }

        function maskContact(contact) {
            const c = String(contact || '');
            if (!c) return '<span style="color:#8e8e93;">未填写</span>';
            if (/^1[3-9]\d{9}$/.test(c)) return c.slice(0, 3) + '****' + c.slice(-4);
            if (c.includes('@')) {
                const [name, domain] = c.split('@');
                return name.slice(0, 1) + '***@' + domain;
            }
            if (c.length > 4) return c.slice(0, 2) + '***' + c.slice(-2);
            return c.slice(0, 1) + '***';
        }

        function renderRegistrations() {
            const el = document.getElementById('panel-registrations');
            const regs = getRegistrations();
            if (!regs.length) { el.innerHTML = '<div class="empty-state">暂无管理员申请</div>'; return; }
            let html = '<table class="admin-table"><thead><tr><th>申请人</th><th>联系方式（脱敏）</th><th>申请角色</th><th>状态</th><th>申请时间</th><th>操作</th></tr></thead><tbody>';
            regs.forEach(reg => {
                html += `<tr>
                    <td>${escapeHtml(reg.username)}</td>
                    <td>${maskContact(reg.contact)}</td>
                    <td>${escapeHtml(reg.role)}</td>
                    <td><span class="badge ${reg.status === '待处理' ? 'badge-pending' : reg.status === '已批准' ? 'badge-approved' : 'badge-rejected'}">${escapeHtml(reg.status)}</span></td>
                    <td>${new Date(reg.createdAt).toLocaleString()}</td>
                    <td>
                        ${reg.status === '待处理' ? `<button class="btn btn-primary btn-sm approve-reg" data-id="${reg.id}">批准</button> <button class="btn btn-danger btn-sm reject-reg" data-id="${reg.id}">拒绝</button>` : ''}
                    </td>
                </tr>`;
            });
            html += '</tbody></table>';
            el.innerHTML = html;
            el.querySelectorAll('.approve-reg').forEach(btn => btn.addEventListener('click', () => handleApproveRegistration(btn.dataset.id, true)));
            el.querySelectorAll('.reject-reg').forEach(btn => btn.addEventListener('click', () => handleApproveRegistration(btn.dataset.id, false)));
        }

        async function handleApproveRegistration(id, approve) {
            const regs = getRegistrations();
            const idx = regs.findIndex(r => r.id === id);
            if (idx < 0) return;
            const reg = regs[idx];
            reg.status = approve ? '已批准' : '已拒绝';
            setRegistrations(regs);
            if (approve) {
                const users = getUsers();
                users.push({ username: reg.username, passwordHash: reg.passwordHash, salt: reg.salt, role: '管理员', contact: reg.contact, createdAt: new Date().toISOString(), forceChangePassword: false });
                setUsers(users);
            }
            addAdminLog({ type: 'registration_review', username: reg.username, approved: approve, operator: getCurrentSession().username });
            showToast(approve ? '已批准该管理员申请' : '已拒绝该管理员申请');
            renderRegistrations();
            renderUserList();
        }

        function renderUserList() {
            const el = document.getElementById('panel-users');
            const users = getUsers();
            if (!users.length) { el.innerHTML = '<div class="empty-state">暂无用户</div>'; return; }
            let html = '<table class="admin-table"><thead><tr><th>用户名</th><th>联系方式（脱敏）</th><th>权限等级</th><th>注册时间</th></tr></thead><tbody>';
            users.forEach(u => {
                const contactDisplay = u.contact ? maskContact(u.contact) : '<span style="color:#ff9f0a;">请到个人信息页面补全个人信息</span>';
                html += `<tr>
                    <td>${escapeHtml(u.username)}</td>
                    <td>${contactDisplay}</td>
                    <td><span class="badge ${getRoleBadgeClass(u.role)}">${getRoleLabel(u.role)}</span></td>
                    <td>${new Date(u.createdAt).toLocaleString()}</td>
                </tr>`;
            });
            html += '</tbody></table>';
            el.innerHTML = html;
        }

        function renderApplicationsManagement(role) {
            const el = document.getElementById('panel-applications');
            const apps = getApplications();
            apps.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            if (!apps.length) { el.innerHTML = '<div class="empty-state">暂无申请记录</div>'; return; }
            let html = '<table class="admin-table"><thead><tr><th>类型</th><th>名称</th><th>分类</th><th>主持人</th><th>描述</th><th>联系方式</th><th>文件</th><th>提交时间</th><th>状态</th></tr></thead><tbody>';
            apps.forEach(app => {
                const fileCell = app.fileName ? `<a href="${app.fileData}" download="${escapeHtml(app.fileName)}" class="file-download-link"><i class="fas fa-download"></i> ${escapeHtml(app.fileName)}</a>` : '-';
                const statusCell = (role === '站长' || role === '管理员') ? `<select data-id="${escapeHtml(app.id)}" class="status-select">
                    <option value="待处理" ${app.status === '待处理' ? 'selected' : ''}>待处理</option>
                    <option value="已接受" ${app.status === '已接受' ? 'selected' : ''}>已接受</option>
                    <option value="已拒绝" ${app.status === '已拒绝' ? 'selected' : ''}>已拒绝</option>
                    <option value="已发布" ${app.status === '已发布' ? 'selected' : ''}>已发布</option>
                    <option value="已完成" ${app.status === '已完成' ? 'selected' : ''}>已完成</option>
                </select>` : `<span class="badge ${app.status === '待处理' ? 'badge-pending' : app.status === '已接受' || app.status === '已发布' || app.status === '已完成' ? 'badge-approved' : 'badge-rejected'}">${escapeHtml(app.status)}</span>`;
                html += `<tr>
                    <td>${escapeHtml(app.type)}</td>
                    <td>${escapeHtml(app.name)}</td>
                    <td>${escapeHtml(app.category)}</td>
                    <td>${escapeHtml(app.host || '访客')}</td>
                    <td>${escapeHtml(app.description)}</td>
                    <td>${escapeHtml(app.contact)}</td>
                    <td>${fileCell}</td>
                    <td>${new Date(app.timestamp).toLocaleString()}</td>
                    <td>${statusCell}</td>
                </tr>`;
            });
            html += '</tbody></table>';
            el.innerHTML = html;
            if (role === '站长' || role === '管理员') {
                el.querySelectorAll('.status-select').forEach(sel => sel.addEventListener('change', e => {
                    const id = e.target.dataset.id;
                    const newStatus = e.target.value;
                    const allApps = getApplications();
                    const app = allApps.find(a => a.id === id);
                    if (app) {
                        const oldStatus = app.status;
                        app.status = newStatus;
                        setApplications(allApps);
                        addAdminLog({ type: 'status_change', applicationId: id, applicationName: app.name, operator: getCurrentSession().username, oldStatus, newStatus });
                        showToast('状态已更新');
                        resetSessionTimer();
                        renderProjectLists();
                        renderFeatureList();
                    }
                }));
            }
        }

        function renderLogs() {
            const el = document.getElementById('panel-logs');
            const logs = getAdminLogs().slice().reverse();
            if (!logs.length) { el.innerHTML = '<div class="empty-state">暂无操作日志</div>'; return; }
            let html = '<table class="admin-table"><thead><tr><th>时间</th><th>类型</th><th>用户</th><th>详情</th></tr></thead><tbody>';
            logs.forEach(log => {
                let detail = '';
                if (log.type === 'login') detail = (log.success ? '登录成功' : '登录失败') + (log.reason ? ` - ${log.reason}` : '');
                else if (log.type === 'logout') detail = '退出登录';
                else if (log.type === 'register') detail = `注册为 ${log.role}` + (log.status ? ` (${log.status})` : '');
                else if (log.type === 'registration_review') detail = (log.approved ? '批准' : '拒绝') + ` ${log.username} 的管理员申请`;
                else if (log.type === 'status_change') detail = `${log.applicationName}: ${log.oldStatus} → ${log.newStatus}`;
                else if (log.type === 'password_reset') detail = '重置密码';
                else if (log.type === 'profile_submit') detail = `提交${log.itemType} ${log.itemName}`;
                else detail = JSON.stringify(log);
                html += `<tr><td>${new Date(log.timestamp).toLocaleString()}</td><td>${escapeHtml(log.type)}</td><td>${escapeHtml(log.username || log.operator || '-')}</td><td>${escapeHtml(detail)}</td></tr>`;
            });
            html += '</tbody></table>';
            el.innerHTML = html;
        }

        document.getElementById('adminRefreshBtn').addEventListener('click', () => {
            renderAdminDashboard();
            renderProjectLists();
            renderFeatureList();
            showToast('数据已刷新');
        });

        // Initialize user system
        (async function initUserSystem() {
            await ensureDefaultTAO();
            renderNavUser();
            renderProjectLists();
            renderFeatureList();
            const session = getCurrentSession();
            if (session) {
                const user = findUser(session.username);
                if (user && new Date().getTime() - new Date(session.loginAt).getTime() < SESSION_TIMEOUT) {
                    renderAdminDashboard();
                } else {
                    clearCurrentSession();
                    resetAdminLoginUI();
                }
            } else {
                resetAdminLoginUI();
            }
        })();

        ['click', 'keydown', 'mousemove'].forEach(evt => {
            document.addEventListener(evt, () => {
                if (getCurrentSession() && document.getElementById('adminDashboard').style.display !== 'none') resetSessionTimer();
            });
        });

        // ===================== Initialize ====================='''

content = content[:start_idx] + new_admin + content[end_idx:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print('index.html updated successfully')
