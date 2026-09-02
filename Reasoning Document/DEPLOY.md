# 个人官网部署指南

## 一、需要打包的文件

上线只需打包以下文件，保持相对路径不变：

```
Smart-Chinese-Herbal-Medicine-Recognition-App/
├── index.html              # 主页面（含全部 CSS / JS）
└── assets/
    ├── hero-bg.jpg         # Hero 背景图
    ├── hero-video.mp4      # Hero 背景视频
    └── about-accent.jpg    # About 区装饰图
```

> 说明：`index.html` 中 CSS 与 JS 均为内嵌，除 CDN 资源外无需额外依赖。

***

## 二、部署具体步骤

### 方案 A：Nginx 服务器

1. 将 `index.html` 与 `assets/` 上传到服务器站点目录，例如 `/var/www/personal-site/`。
2. 目录结构如下：

   ```
   /var/www/personal-site/
   ├── index.html
   └── assets/
       ├── hero-bg.jpg
       ├── hero-video.mp4
       └── about-accent.jpg
   ```
3. 编辑 Nginx 配置：

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /var/www/personal-site;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location ~* \.(jpg|jpeg|png|gif|ico|css|js|mp4|webp)$ {
           expires 30d;
           add_header Cache-Control "public, immutable";
       }
   }
   ```
4. 检查配置并重启：

   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 方案 B：GitHub Pages

1. 将上述文件推送到仓库的 `gh-pages` 分支，或仓库根目录 / `docs/` 目录。
2. 进入仓库 **Settings → Pages**。
3. Source 选择部署分支与目录（如 `main` / `root`）。
4. 等待几分钟后访问 `https://<username>.github.io/<repo-name>/`。

### 方案 C：Vercel / Netlify / Cloudflare Pages

1. 将文件上传至 Git 仓库。
2. 在平台中 **Import** 该仓库。
3. Build settings：

   * Framework Preset：`Other` / `None`

   * Build command：留空

   * Output directory：`/`（根目录）
4. 点击 Deploy，等待自动完成。
5. 绑定自定义域名（可选）。

***

## 三、部署前检查清单

* [ ] 已修改默认管理员密码与锁定码（当前为演示值，务必替换）

* [ ] 已确认 `assets/` 内图片与视频能正常加载

* [ ] 已在本地浏览器完成功能验证（登录、申请、刷新、响应式）

* [ ] 已配置 HTTPS（推荐）

