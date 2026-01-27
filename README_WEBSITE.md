# Text-to-Video Finetuning - Project Website

## 🎯 Overview

This is a world-class, production-ready project webpage for showcasing your Text-to-Video Finetuning framework. Designed for recruiters, AI/ML engineers, research reviewers, and graduate admissions committees.

## 📁 Files Included

- `index.html` - Main HTML structure
- `styles.css` - Complete CSS styling with dark theme
- `script.js` - Interactive JavaScript features
- `README_WEBSITE.md` - This file

## 🚀 Quick Start

### Option 1: Local Testing

1. Open `index.html` in your browser
2. That's it! No build process required.

### Option 2: Deploy to GitHub Pages

1. Create a new repository or use your existing project repo
2. Add these files to the root or a `docs/` folder
3. Go to Settings → Pages
4. Select the branch and folder
5. Your site will be live at `https://yourusername.github.io/repo-name/`

### Option 3: Deploy to Netlify

1. Drag and drop the folder to [Netlify Drop](https://app.netlify.com/drop)
2. Or connect your GitHub repo for automatic deployments
3. Your site will be live instantly

## ✏️ Customization Guide

### 1. Update Personal Information

**In `index.html`:**

- Line 28: Update GitHub link
  ```html
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO">
  ```

- Line 73: Update GitHub link in hero section
  ```html
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO">
  ```

- Line 395: Update footer links
  ```html
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO">
  <a href="mailto:YOUR_EMAIL@example.com">
  ```

- Line 407: Update author name and year
  ```html
  <p>&copy; 2025 YOUR NAME. Built for research and education.</p>
  ```

### 2. Add Your Own Content

**Replace placeholder text:**
- Update project descriptions to match your specific implementation
- Add actual performance metrics if available
- Include real video examples or screenshots

**Add video demos:**
- Replace `.result-video-placeholder` divs with actual `<video>` tags
- Or add thumbnail images linking to video demos

### 3. Customize Colors

**In `styles.css` (lines 10-20):**

```css
--accent-primary: #6366f1;  /* Change primary color */
--accent-secondary: #8b5cf6; /* Change secondary color */
--accent-tertiary: #ec4899;  /* Change tertiary color */
```

### 4. Add Analytics (Optional)

Add Google Analytics or Plausible before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_ID');
</script>
```

## 🎨 Features Included

### Design Features
- ✅ Dark theme with gradient accents
- ✅ Smooth animations and transitions
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Modern glassmorphism effects
- ✅ Professional typography (Inter font)

### Interactive Features
- ✅ Smooth scrolling navigation
- ✅ Intersection Observer animations
- ✅ Hover effects on cards
- ✅ Copy code snippets on click
- ✅ Active navigation highlighting
- ✅ Mouse-following gradient orbs
- ✅ Mobile menu toggle

### SEO & Performance
- ✅ Semantic HTML5
- ✅ Meta tags for social sharing
- ✅ Fast loading (no heavy dependencies)
- ✅ Accessible markup
- ✅ Clean, commented code

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔧 Advanced Customization

### Add New Sections

1. Copy an existing section structure from `index.html`
2. Update the content
3. Add corresponding styles in `styles.css`
4. Update navigation links

### Change Fonts

Replace the Google Fonts link in `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT&display=swap" rel="stylesheet">
```

Update CSS variables:
```css
--font-primary: 'YOUR_FONT', sans-serif;
```

### Add Images

1. Create an `images/` folder
2. Add your images
3. Reference them in HTML:
   ```html
   <img src="images/your-image.jpg" alt="Description">
   ```

## 📊 Performance Tips

1. **Optimize images**: Use WebP format, compress images
2. **Lazy loading**: Images already set up for lazy loading
3. **Minify**: Use tools like [HTMLMinifier](https://www.willpeavy.com/tools/minifier/) for production
4. **CDN**: Consider using a CDN for faster global delivery

## 🐛 Troubleshooting

**Fonts not loading?**
- Check internet connection (Google Fonts requires internet)
- Or download fonts and host locally

**Animations not working?**
- Check browser console for JavaScript errors
- Ensure `script.js` is properly linked

**Mobile menu not working?**
- Verify JavaScript is enabled
- Check that `script.js` loaded correctly

## 📝 License

This website template is part of your Text-to-Video Finetuning project.
Feel free to customize and use it for your portfolio.

## 🤝 Credits

- Design: Custom built for AI research showcase
- Icons: Inline SVG (no external dependencies)
- Fonts: Google Fonts (Inter, JetBrains Mono)

## 📧 Support

For questions about customization, open an issue in your repository.

---

**Built with ❤️ for AI researchers and engineers**
