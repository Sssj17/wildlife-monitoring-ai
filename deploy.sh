#!/bin/bash

echo "========================================="
echo "Wildlife Monitoring AI - Quick Deployer"
echo "========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "[1/5] Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Wildlife Monitoring AI System"
    echo "✓ Git repository initialized"
else
    echo "[1/5] Git repository already exists"
fi

echo ""
echo "[2/5] Deployment Platform Selection"
echo "Choose your deployment platform:"
echo "  1) Render (Recommended - Free tier)"
echo "  2) Heroku (Paid, starts at $5/month)"
echo "  3) PythonAnywhere (Free tier available)"
echo "  4) Manual deployment (show instructions)"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "=== Render Deployment ==="
        echo "1. Create account at render.com"
        echo "2. Push code to GitHub:"
        echo "   - Create new repo on GitHub"
        read -p "   - Enter GitHub repo URL: " repo_url
        git remote add origin "$repo_url"
        git branch -M main
        git push -u origin main
        echo ""
        echo "3. On Render:"
        echo "   - Click 'New +' → 'Web Service'"
        echo "   - Connect your GitHub repo"
        echo "   - Render will auto-detect configuration from render.yaml"
        echo "   - Click 'Create Web Service'"
        echo ""
        echo "✓ Code pushed! Now complete setup on Render dashboard"
        ;;
    2)
        echo ""
        echo "=== Heroku Deployment ==="
        echo "Installing Heroku CLI..."
        echo "Please visit: https://devcenter.heroku.com/articles/heroku-cli"
        echo ""
        read -p "Press Enter after installing Heroku CLI..."
        heroku login
        heroku create wildlife-monitoring-ai
        heroku addons:create heroku-postgresql:mini
        heroku config:set FLASK_ENV=production
        heroku config:set SECRET_KEY=$(openssl rand -hex 32)
        git push heroku main
        heroku open
        echo "✓ Deployed to Heroku!"
        ;;
    3)
        echo ""
        echo "=== PythonAnywhere Deployment ==="
        echo "1. Create account at pythonanywhere.com"
        echo "2. Upload code via Files tab or Git"
        echo "3. Create virtual environment and install requirements"
        echo "4. Configure Web app with WSGI file"
        echo ""
        echo "See DEPLOYMENT.md for detailed instructions"
        ;;
    4)
        echo ""
        echo "=== Manual Deployment Instructions ==="
        echo "See DEPLOYMENT.md for complete guide"
        echo ""
        echo "Quick checklist:"
        echo "- Push code to GitHub"
        echo "- Set environment variables"
        echo "- Configure database (PostgreSQL recommended)"
        echo "- Deploy to your chosen platform"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Deployment initiated! 🚀"
echo "========================================="
