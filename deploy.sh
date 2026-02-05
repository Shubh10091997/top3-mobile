#!/bin/bash
cd /c/Users/Shubham/Desktop/top3-mobile

echo "📦 Pushing changes to live site..."

# Add all changes
git add -A
echo "✅ Files staged"

# Commit with message
git commit -m "Add Google Analytics exclusion, health check, new launch phones, duplicate compare fix, and detailed phone specs"
echo "✅ Changes committed"

# Push to main branch
git push origin main
echo "✅ Pushed to live site!"

# Show status
git status
