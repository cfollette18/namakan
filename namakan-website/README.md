# Namakan Website

Static HTML/CSS site for Namakan AI Engineering.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main landing page with services, pricing, positioning |
| `services.html` | Detailed service descriptions |
| `contact.html` | Contact form |
| `hero-video.html` | Fine-tuned vs Generic AI demo (standalone) |
| `styles.css` | Shared stylesheet |

## Development

Simply open `index.html` in a browser, or serve with any static file server:

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .

# PHP
php -S localhost:8080
```

## Deployment

Deploy `namakan-website/` contents to any static host:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any web server

## Note

A Next.js version exists in `/frontend/` — this plain HTML version is the current live site.
