# PKI X.509 Lab - GitHub Repository Setup - COMPLETE GUIDE

## ✅ What Has Been Prepared For You

Your project folder now contains the following files to streamline GitHub setup:

### Documentation Files
- **README.md** - Comprehensive project documentation with features, usage, and examples
- **SETUP_GUIDE_FA.md** - Complete setup guide in Persian/Farsi
- **MANUAL_GIT_COMMANDS.md** - All git commands if you prefer manual execution
- **.gitignore** - Configured to ignore generated certificates, keys, and Python cache

### Setup Scripts
- **setup_git.bat** - Windows Batch script (run directly in Explorer or CMD)
- **setup_git.ps1** - PowerShell script (recommended for Windows)

## 🎯 The 8 Meaningful Commits

Each commit represents a logical feature milestone:

| # | Commit Message | Description |
|---|---|---|
| 1 | Core infrastructure | Base code, directory structure, utility functions |
| 2 | Certificate Authority | CA creation with RSA-3072 and X.509 extensions |
| 3 | CSR Generation | Certificate Signing Request with SAN support |
| 4 | RA Approval Workflow | Registration Authority validation and approval process |
| 5 | CA Signing | Certificate issuance and signing functionality |
| 6 | Extended Key Usage | EKU support and advanced certificate features |
| 7 | Revocation & CRL | Certificate revocation and CRL management |
| 8 | Documentation | README and project documentation |

## 🚀 How to Execute Setup

### Option 1: PowerShell (RECOMMENDED)

```powershell
# Navigate to project folder
cd C:\Users\Nine\Downloads\git\PKI_X.509

# Set execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Run the PowerShell script
.\setup_git.ps1

# When prompted, press Y to continue
```

### Option 2: Windows Batch

```cmd
# Navigate to project folder
cd C:\Users\Nine\Downloads\git\PKI_X.509

# Run the batch script
setup_git.bat

# Or right-click setup_git.bat and select "Run as Administrator"
```

### Option 3: Manual Commands

Open PowerShell or CMD in the project folder and run all commands from MANUAL_GIT_COMMANDS.md

## ⚠️ Prerequisites

### Git Installation Required
Before running any scripts, ensure Git is installed:

```bash
# Check if Git is installed
git --version

# If not installed, download from:
# https://git-scm.com/download/win
```

### Git Global Configuration (one-time setup)

```bash
# Configure your Git identity globally
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# Or configure per-repository (after init):
git config user.name "Your Full Name"
git config user.email "your.email@example.com"
```

## 📤 Publishing to GitHub (Next Steps)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Enter repository name (e.g., "PKI_X.509" or "pki-lab")
3. Choose "Public" or "Private"
4. Do NOT initialize with README, .gitignore, or license
5. Click "Create repository"
6. Copy the repository URL (HTTPS or SSH)

### Step 2: Connect Local Repository to GitHub

In PowerShell/CMD, run:

```bash
# Navigate to your project folder
cd C:\Users\Nine\Downloads\git\PKI_X.509

# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Verify remote was added
git remote -v

# Rename branch to main (if needed)
git branch -M main

# Push all 8 commits to GitHub
git push -u origin main
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name

### Step 3: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see:
   - All 8 commits in the Commits history
   - README.md displayed on the repository homepage
   - All files properly listed
   - .gitignore properly configured

## 🔍 Verification Commands

After setup, verify everything is correct:

```bash
# View all commits with one-line summary
git log --oneline

# View detailed information for a specific commit
git log -1
git show <commit-hash>

# Check git status
git status

# View configured remotes
git remote -v
```

Expected output for `git log --oneline`:
```
abcdef8 docs: add comprehensive README and project documentation
abcdef7 feat: implement certificate revocation and CRL management
abcdef6 feat: implement Extended Key Usage and advanced certificate features
abcdef5 feat: implement certificate signing by CA
abcdef4 feat: add RA certificate request approval process
abcdef3 feat: implement CSR generation with SAN support
abcdef2 feat: add Certificate Authority (CA) creation functionality
abcdef1 feat: initial project structure with core infrastructure
```

## 💡 Key Features

✅ **8 Organized Commits** - Each represents a logical project milestone
✅ **Professional Messages** - Follows conventional commits format
✅ **Complete Documentation** - README covers all features and usage
✅ **Ignored Files** - Private keys, certificates, and generated files won't be tracked
✅ **Automated Setup** - Scripts handle everything automatically
✅ **Push-Ready** - All commits prepared locally, ready for one-command push

## 📝 Project Structure in Repository

```
PKI_X.509/
├── README.md                    ← Usage documentation
├── SETUP_GUIDE_FA.md           ← Persian setup guide
├── MANUAL_GIT_COMMANDS.md      ← Manual git commands
├── setup_git.bat               ← Windows batch script
├── setup_git.ps1               ← PowerShell script
├── .gitignore                  ← File exclusions
├── pki_lab.py                  ← Main source code
├── pki_manual.pdf              ← Original documentation
├── .git/                       ← Git repository (auto-created)
└── pki/                        ← Generated at runtime
    ├── ca/                     ← CA certificates
    ├── keys/                   ← Private keys
    ├── certs/                  ← Issued certificates
    ├── requests/               ← CSRs
    ├── crl/                    ← Certificate Revocation Lists
    └── approvals/              ← Approval records
```

## 🔐 Security Notes

- The `.gitignore` prevents accidental commit of:
  - Private keys (*.key.pem)
  - Generated certificates (*.cert.pem)
  - CA certificates and keys
  - CRL files and revocation lists
  - Approval JSON files with sensitive data

- Never commit private keys or sensitive credentials
- Use environment variables or secure vaults for production

## ❓ Frequently Asked Questions

**Q: Do I need to run the script multiple times?**
A: No, run it once. It creates all 8 commits automatically.

**Q: Can I modify the commit messages?**
A: You can edit SETUP_GUIDE_FA.md before running, but scripts have fixed messages.

**Q: What if Git is not installed?**
A: Download Git from https://git-scm.com/download/win and run the installer.

**Q: Can I run the PowerShell script on Mac/Linux?**
A: Yes, but run it via WSL or use the manual commands instead.

**Q: Do the commits get pushed automatically?**
A: No. Only local commits are created. You must run `git push -u origin main` separately.

**Q: Can I add more commits later?**
A: Yes, make changes to files and run `git commit -am "message"` as normal.

## 📞 Support

If you encounter issues:

1. Check that Git is installed: `git --version`
2. Verify your git configuration: `git config --list`
3. Check console output for specific error messages
4. Review MANUAL_GIT_COMMANDS.md for individual command steps
5. Ensure you have internet connection for pushing to GitHub

## 🎉 Summary

Your PKI X.509 project is ready for GitHub!

**What's Next:**

1. ✅ Files and documentation prepared
2. → Run setup_git.ps1 or setup_git.bat
3. → Create repository on GitHub
4. → Run `git push -u origin main`
5. → Share your professional project!

**All 8 commits will be pushed in one command!**

---

**Created**: July 2026
**Project**: PKI X.509 Certificate Management Lab
**Ready for**: Professional GitHub Repository
