# Fix Streamlit Cloud Deployment Error

## Problem
```
ModuleNotFoundError: No module named 'httpx'
```

## Root Cause
The `requirements.txt` file was updated locally but not pushed to GitHub, or Streamlit Cloud hasn't redeployed with the new dependencies.

## Solution

### Step 1: Initialize Git Repository (if not already done)
```bash
cd D:\Optimum\UOB_QA_Complete

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Add httpx dependency and fix deployment"
```

### Step 2: Push to GitHub
```bash
# Add your GitHub repository as remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/UOBSurvey.git

# Push to GitHub
git push -u origin main
```

Or if already initialized:
```bash
cd D:\Optimum\UOB_QA_Complete
git add requirements.txt
git commit -m "Add httpx dependency"
git push origin main
```

### Step 3: Redeploy on Streamlit Cloud

#### Option A: Automatic (recommended)
Streamlit Cloud will automatically detect the GitHub push and redeploy. Wait 2-3 minutes.

#### Option B: Manual Reboot
1. Go to your app on Streamlit Cloud
2. Click the "⋮" menu (three dots) in the top right
3. Click "Reboot app"
4. Wait for the app to restart

### Step 4: Verify Fix
1. Check the app logs in Streamlit Cloud
2. The error should be gone
3. You should see "Successfully installed httpx-..." in the logs

## Verification Checklist

- [ ] requirements.txt contains `httpx>=0.24.0`
- [ ] requirements.txt is committed to Git
- [ ] requirements.txt is pushed to GitHub
- [ ] Streamlit Cloud has redeployed (check logs)
- [ ] App is running without errors

## Current Requirements.txt Status
Your requirements.txt DOES include httpx:
```
httpx>=0.24.0
```

So you just need to:
1. Push it to GitHub
2. Let Streamlit Cloud redeploy

## Quick Commands
```bash
# Quick push
cd D:\Optimum\UOB_QA_Complete
git add requirements.txt
git commit -m "Add httpx dependency for OpenAI client"
git push

# Then wait 2-3 minutes for Streamlit Cloud to redeploy
```

## Alternative: Skip httpx (Not Recommended)
If you want a quick workaround without httpx, you can modify the code, but this will disable the proxy workaround for OpenAI. Not recommended.

## Still Having Issues?

### Check Streamlit Cloud Logs
1. Go to your app
2. Click "Manage app" (bottom right)
3. Click "Logs"
4. Look for installation errors

### Common Issues
- **GitHub sync delay**: Wait 5 minutes after pushing
- **Build cache**: Do a manual reboot from Streamlit Cloud settings
- **Wrong branch**: Ensure Streamlit Cloud is watching the correct branch
- **File location**: Ensure requirements.txt is in the root directory of your repo

