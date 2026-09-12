# Auto-Renew-HidenCloud

纯到期提醒（完全不碰面板）：每天算一次剩余天数，≤3 天发 TG 群通知。
续期由人工完成。每次续期后更新 remind.yml 里的 DUE 日期。

历史：曾尝试全自动浏览器续期，但 HidenCloud 的 Cloudflare Turnstile 只放行亚太出口，
GitHub runner（美国）无论如何换出口（WARP/德国节点/各种指纹伪装）都无法登录，遂放弃自动化。
