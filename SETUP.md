# SentinelVision Pro — Website Setup Guide

## What you have

```
sentinelvision_website/
├── index.html       ← Landing page (hero, features, pricing preview, contact)
├── pricing.html     ← Full pricing table + FAQ
├── order.html       ← License order form
├── css/style.css    ← All styles
├── js/main.js       ← Interactive features
└── SETUP.md         ← This file
```

---

## Step 1 — Set up your contact form (Web3Forms — FREE)

The order form and contact form send emails to you via Web3Forms (completely free).

1. Go to **https://web3forms.com**
2. Enter **info.sentinelvision@gmail.com** in the box
3. Click **Create Access Key**
4. Copy your access key (looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
5. Open `index.html` — find this line:
   ```html
   <input type="hidden" name="access_key" value="REPLACE_WITH_YOUR_WEB3FORMS_KEY">
   ```
   Replace `REPLACE_WITH_YOUR_WEB3FORMS_KEY` with your key.

6. Do the same in `order.html` — find the same line and replace it.

> Web3Forms is free with no submission limit. Emails arrive at info.sentinelvision@gmail.com.

---

## Step 2 — Deploy to Netlify (FREE hosting)

Netlify gives you free hosting at a URL like `sentinelvisionpro.netlify.app`.

### Option A — Drag and drop (easiest, no account needed for files)

1. Go to **https://app.netlify.com**
2. Sign up for a free account (use GitHub or email)
3. In the dashboard, scroll to the bottom — you'll see a box that says
   **"Want to deploy a new site without connecting to Git? Drag and drop your site folder here."**
4. Open File Explorer and drag the entire `sentinelvision_website` folder into that box
5. Netlify deploys it instantly and gives you a URL

### Option B — Netlify CLI (for easier re-deployments after changes)

```powershell
npm install -g netlify-cli
cd H:\sentinelvision_website
netlify deploy --prod
```

---

## Step 3 — Customise your Netlify URL

After deploying:
1. Go to **Site configuration → General → Site details**
2. Click **Change site name**
3. Enter something like `sentinelvisionpro` → your site becomes `sentinelvisionpro.netlify.app`

---

## Step 4 — Connect your domain: sentinelvision.net.za

You already own `sentinelvision.net.za`. Here's how to point it at Netlify.

### In Netlify:
1. Go to your site dashboard → **Domain management → Add a domain**
2. Type `sentinelvision.net.za` and click **Verify**
3. Click **Add domain**
4. Netlify will show you DNS records to add — note them down

### In your domain registrar (wherever you bought sentinelvision.net.za):
Add these DNS records (Netlify will give you the exact values):

| Type | Name | Value |
|---|---|---|
| A | @ | `75.2.60.5` (Netlify load balancer) |
| CNAME | www | `[your-netlify-site-name].netlify.app` |

Save the records. DNS can take up to 24 hours to propagate but is usually live within minutes.

### Free SSL (HTTPS):
Once your domain is connected, go to **Domain management → HTTPS** and click **Verify DNS configuration** then **Provision certificate**. Netlify issues a free Let's Encrypt SSL certificate automatically.

Your site will then be live at:
- `https://sentinelvision.net.za`
- `https://www.sentinelvision.net.za`

---

## Step 5 — Update your SentinelVision app

Now that your website is live, update the license renewal link in the app so expired licenses link to your website.

In `templates/license.html`, find the renewal CTA link and change:
```html
href="mailto:info.sentinelvision@gmail.com?subject=..."
```
to:
```html
href="https://sentinelvision.net.za/order.html"
```

---

## Future upgrades (when budget allows)

| Upgrade | Cost | What it adds |
|---|---|---|
| Stripe payments | Free to set up, ~3% per transaction | Customers pay online, no manual EFT chasing |
| Automated license emails | Requires a small backend | Key generated and emailed automatically on payment |

---

## What orders look like

When someone submits the order form, you get an email like:

```
From: SentinelVision Website
Subject: SentinelVision Pro — New License Order

first_name: Jane
last_name: Smith
email: jane@example.com
license_type: Full Feature Bundle — R500/month
duration: 3 months
order_summary: Full Feature Bundle — 3 months — R1,400
notes: I have 4 cameras
```

You then:
1. Send Jane your bank details by email
2. Once paid, run `python generate_license.py` in your project to create her key
3. Email her the key

---

## Contact

Website by SentinelVision Pro — info.sentinelvision@gmail.com
