# Step-by-Step Guide: Push Code to GitHub

## Prerequisites

Before starting, make sure you have:
- [ ] GitHub account created (https://github.com)
- [ ] Git installed on your computer
- [ ] Terminal/Command Prompt open in your project folder

Check Git installation:
```bash
git --version
# Should show: git version 2.x.x
```

---

## Step 1: Create a New Repository on GitHub

### Option A: Via GitHub Website (Recommended for First Time)

1. **Go to GitHub**: https://github.com
2. **Sign in** to your account
3. **Click** the `+` icon (top right) → **"New repository"**
4. **Fill in details**:
   - **Repository name**: `bank-statement-processor` (or your preferred name)
   - **Description**: `AI-powered bank statement processing system with hybrid extraction and ML classification`
   - **Visibility**: 
     - ✅ **Public** (if you want to share/showcase)
     - 🔒 **Private** (if you want to keep it confidential)
   - **DO NOT** check "Initialize with README" (we already have one)
   - **DO NOT** add .gitignore (we already have one)
   - **DO NOT** choose a license yet (optional)
5. **Click** "Create repository"
6. **Copy** the repository URL shown (looks like: `https://github.com/YOUR_USERNAME/bank-statement-processor.git`)

---

## Step 2: Initialize Git in Your Project (Run These Commands)

Open your terminal in the project folder and run:

```bash
# 1. Initialize git repository
git init

# 2. Configure your identity (if not done before)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Check what files will be committed
git status
```

**Expected output**: You should see all your project files listed in red (untracked files).

---

## Step 3: Stage and Commit Your Code

```bash
# 1. Add all files (respecting .gitignore)
git add .

# 2. Check what's staged (should be green now)
git status

# 3. Create your first commit
git commit -m "Initial commit: Bank statement processor with hybrid extraction"
```

**What this does**:
- `git add .` - Stages all files (except those in .gitignore)
- `git commit` - Creates a snapshot of your code with a message

---

## Step 4: Connect to GitHub and Push

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# 1. Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/bank-statement-processor.git

# 2. Verify remote was added
git remote -v

# 3. Rename branch to 'main' (GitHub default)
git branch -M main

# 4. Push your code to GitHub
git push -u origin main
```

**Enter credentials** when prompted:
- **Username**: Your GitHub username
- **Password**: Your GitHub Personal Access Token (NOT your GitHub password)

---

## Step 5: Get GitHub Personal Access Token (If Needed)

If you don't have a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `bank-statement-processor-access`
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

**Store token securely** - Don't share it or commit it!

---

## Step 6: Verify Upload

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/bank-statement-processor`
2. You should see all your files!
3. Check that sensitive files are NOT there:
   - ❌ No `venv/` folder
   - ❌ No `.env` files
   - ❌ No files in `uploads/` or `outputs/` (except .gitkeep)
   - ❌ No log files

---

## Quick Command Summary (Copy-Paste This)

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Initialize and commit
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: Bank statement processor with hybrid extraction"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/bank-statement-processor.git
git branch -M main
git push -u origin main
```

---

## Future Updates (After Initial Push)

When you make changes later:

```bash
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with meaningful message
git commit -m "Add: Description of what you changed"

# 4. Push to GitHub
git push
```

---

## Common Issues & Solutions

### Issue 1: "Authentication Failed"
**Solution**: Use Personal Access Token, not password
- Get token from: https://github.com/settings/tokens

### Issue 2: "remote origin already exists"
**Solution**: 
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/repo.git
```

### Issue 3: "Permission denied"
**Solution**: Check you're using the correct GitHub username and token

### Issue 4: Files showing that shouldn't be there
**Solution**: 
```bash
# Remove from git but keep locally
git rm --cached filename
git commit -m "Remove sensitive file"
git push
```

---

## Security Checklist Before Pushing

✅ Check `.gitignore` is properly configured  
✅ No API keys in code (use environment variables)  
✅ No `.env` files  
✅ No `uploads/` or `outputs/` with user data  
✅ No `venv/` or `__pycache__/`  
✅ No personal information in code or config files  

---

## Optional: Add Repository Badges

After pushing, add these to your README.md:

```markdown
# Bank Statement Processor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)
```

---

## Need Help?

If you encounter issues:
1. Check GitHub's help: https://docs.github.com
2. Read error messages carefully
3. Search on Google: "git [your error message]"
4. Ask for help with the specific error message

---

**Congratulations! 🎉** Your code is now on GitHub and can be shared, showcased, or collaborated on!
