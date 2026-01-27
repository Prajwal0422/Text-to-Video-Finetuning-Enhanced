# 🚀 Deployment Guide

## Quick Deploy Options

### Option 1: GitHub Pages (Recommended)

#### Method A: Direct Repository Deployment

1. **Push files to your repository**
   ```bash
   git add index.html styles.css script.js .nojekyll
   git commit -m "Add project website"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source", select **main** branch
   - Select **/ (root)** folder
   - Click **Save**

3. **Access your site**
   - Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO/`
   - Wait 1-2 minutes for initial deployment

#### Method B: Docs Folder Deployment

1. **Create docs folder**
   ```bash
   mkdir docs
   mv index.html styles.css script.js .nojekyll docs/
   ```

2. **Push and configure**
   ```bash
   git add docs/
   git commit -m "Add website to docs folder"
   git push origin main
   ```

3. **Enable GitHub Pages**
   - Settings → Pages
   - Select **main** branch
   - Select **/docs** folder
   - Click **Save**

### Option 2: Netlify (Fastest)

#### Method A: Drag & Drop

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag the folder containing your files
3. Your site is live instantly!
4. Get a URL like: `https://random-name.netlify.app`

#### Method B: Git Integration

1. **Connect repository**
   - Sign in to [Netlify](https://app.netlify.com)
   - Click "New site from Git"
   - Choose GitHub and select your repository

2. **Configure build settings**
   - Build command: (leave empty)
   - Publish directory: `/` or `docs/`
   - Click "Deploy site"

3. **Custom domain (optional)**
   - Go to Domain settings
   - Add your custom domain
   - Update DNS records

### Option 3: Vercel

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Or use GitHub integration**
   - Go to [Vercel](https://vercel.com)
   - Import your GitHub repository
   - Deploy automatically

### Option 4: Local Testing

1. **Simple HTTP Server**
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   
   # Node.js (if you have npx)
   npx serve
   ```

2. **Open browser**
   - Navigate to `http://localhost:8000`

## 🔧 Pre-Deployment Checklist

### Required Updates

- [ ] Update GitHub links (search for `yourusername`)
- [ ] Update email address in footer
- [ ] Update author name in footer
- [ ] Update year in footer
- [ ] Test all navigation links
- [ ] Test on mobile device

### Optional Enhancements

- [ ] Add Google Analytics
- [ ] Add custom domain
- [ ] Add favicon
- [ ] Add Open Graph images
- [ ] Compress images (if added)
- [ ] Minify CSS/JS for production

## 📝 Custom Domain Setup

### GitHub Pages

1. **Add CNAME file**
   ```bash
   echo "yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Update DNS records**
   - Add A records pointing to GitHub IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add CNAME record: `YOUR_USERNAME.github.io`

3. **Configure in GitHub**
   - Settings → Pages
   - Enter custom domain
   - Enable "Enforce HTTPS"

### Netlify

1. **Add domain in Netlify**
   - Site settings → Domain management
   - Add custom domain

2. **Update DNS**
   - Add CNAME record: `YOUR_SITE.netlify.app`
   - Or use Netlify DNS

3. **Enable HTTPS**
   - Automatic with Let's Encrypt

## 🎨 Customization Before Deploy

### 1. Update Personal Info

**In `index.html`:**
```html
<!-- Line 28, 73, 395 -->
<a href="https://github.com/YOUR_USERNAME/YOUR_REPO">

<!-- Line 398 -->
<a href="mailto:YOUR_EMAIL@example.com">

<!-- Line 407 -->
<p>&copy; 2025 YOUR NAME. Built for research and education.</p>
```

### 2. Add Favicon

Create `favicon.ico` and add to `<head>`:
```html
<link rel="icon" type="image/x-icon" href="favicon.ico">
```

### 3. Add Meta Tags for Social Sharing

```html
<!-- Open Graph -->
<meta property="og:title" content="Text-to-Video Finetuning Framework">
<meta property="og:description" content="Advanced AI research project">
<meta property="og:image" content="https://yoursite.com/preview.jpg">
<meta property="og:url" content="https://yoursite.com">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Text-to-Video Finetuning">
<meta name="twitter:description" content="Advanced AI research project">
<meta name="twitter:image" content="https://yoursite.com/preview.jpg">
```

## 🔍 SEO Optimization

### 1. Add robots.txt

```txt
User-agent: *
Allow: /

Sitemap: https://yoursite.com/sitemap.xml
```

### 2. Add sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yoursite.com/</loc>
    <lastmod>2025-01-27</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

## 📊 Analytics Setup

### Google Analytics

Add before `</head>`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Plausible (Privacy-friendly)

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

## 🐛 Troubleshooting

### Site not loading?
- Check GitHub Pages is enabled
- Verify branch and folder settings
- Wait 2-3 minutes for deployment
- Check for typos in file names

### Styles not applying?
- Verify `styles.css` is in same folder as `index.html`
- Check browser console for errors
- Clear browser cache

### JavaScript not working?
- Verify `script.js` is in same folder
- Check browser console for errors
- Ensure JavaScript is enabled

### Mobile menu not working?
- Test on actual mobile device
- Check responsive breakpoints
- Verify JavaScript loaded

## 🚀 Performance Optimization

### 1. Minify Files

Use online tools:
- [CSS Minifier](https://cssminifier.com/)
- [JavaScript Minifier](https://javascript-minifier.com/)
- [HTML Minifier](https://www.willpeavy.com/tools/minifier/)

### 2. Enable Compression

Most hosting platforms enable gzip automatically.

### 3. Add Cache Headers

For custom servers, add to `.htaccess`:
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
</IfModule>
```

## ✅ Post-Deployment Checklist

- [ ] Test all links
- [ ] Test on mobile
- [ ] Test on different browsers
- [ ] Check loading speed
- [ ] Verify analytics working
- [ ] Test contact form (if added)
- [ ] Check console for errors
- [ ] Verify HTTPS enabled
- [ ] Test social sharing preview
- [ ] Submit to Google Search Console

## 📱 Testing Tools

- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) (Chrome DevTools)

---

**Your website is now ready to impress recruiters, researchers, and admissions committees!** 🎉
