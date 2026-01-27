# ⚡ Quick Reference Card

## 🎯 3-Minute Deploy

```bash
# 1. Update personal info in index.html (lines 28, 73, 395, 398, 407)
# 2. Push to GitHub
git add index.html styles.css script.js .nojekyll
git commit -m "Add website"
git push

# 3. Enable GitHub Pages: Settings → Pages → main branch → / (root)
# Done! Live at: https://YOUR_USERNAME.github.io/YOUR_REPO/
```

## 📝 Must Update

| Location | What to Change | Example |
|----------|---------------|---------|
| Line 28 | GitHub link | `https://github.com/YOUR_USERNAME/YOUR_REPO` |
| Line 73 | GitHub link | Same as above |
| Line 395 | GitHub link | Same as above |
| Line 398 | Email | `your.email@example.com` |
| Line 407 | Name & Year | `© 2025 Your Name` |

## 🎨 Color Customization

In `styles.css` (lines 10-20):
```css
--accent-primary: #6366f1;   /* Main color */
--accent-secondary: #8b5cf6; /* Secondary */
--accent-tertiary: #ec4899;  /* Accent */
```

## 🔧 Common Tasks

### Add Favicon
```html
<!-- In <head> -->
<link rel="icon" href="favicon.ico">
```

### Add Analytics
```html
<!-- Before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ID"></script>
```

### Test Locally
```bash
python -m http.server 8000
# Visit: http://localhost:8000
```

## 📱 File Structure

```
your-repo/
├── index.html          # Main page
├── styles.css          # All styles
├── script.js           # Interactions
├── .nojekyll          # GitHub Pages config
├── README_WEBSITE.md  # Full guide
└── DEPLOYMENT_GUIDE.md # Deploy help
```

## 🚀 Deploy Options

| Platform | Speed | Command |
|----------|-------|---------|
| GitHub Pages | 2 min | Settings → Pages |
| Netlify | 30 sec | Drag & drop |
| Vercel | 1 min | `vercel` |

## 🎯 Key Sections

1. **Hero** - First impression
2. **About** - Problem/solution
3. **Architecture** - System design
4. **Features** - Capabilities (6 cards)
5. **Tech Stack** - Technologies
6. **Results** - Metrics
7. **Workflow** - How to use
8. **Acknowledgements** - Credits

## 💡 Pro Tips

- ✅ Test on mobile before deploy
- ✅ Add real performance metrics
- ✅ Include video demos if possible
- ✅ Link from GitHub README
- ✅ Share on LinkedIn

## 🐛 Quick Fixes

**Styles not loading?**
→ Check file names match exactly

**JavaScript not working?**
→ Check browser console (F12)

**Mobile menu broken?**
→ Verify script.js loaded

**Site not deploying?**
→ Wait 2-3 minutes, check Settings

## 📊 Performance

- Load time: < 2 seconds
- Total size: ~65 KB
- No dependencies
- Mobile optimized

## 🎓 Perfect For

- ✅ Job applications
- ✅ Portfolio showcase
- ✅ Research presentations
- ✅ Graduate admissions
- ✅ Conference demos

## 📞 Support

- Read: `README_WEBSITE.md`
- Deploy: `DEPLOYMENT_GUIDE.md`
- Features: `WEBSITE_FEATURES.md`

---

**Deploy in 3 minutes. Impress for years.** ⚡
