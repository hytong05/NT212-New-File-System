# GitHub Repository Guidelines for MyFS

## 📁 Essential Files for Repository

### Core Application Structure
```
MyFS/
├── .gitignore                    # Git ignore rules
├── README.md                     # Main project overview
├── README_EN.md                  # Detailed English docs
├── README_VI.md                  # Detailed Vietnamese docs
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
│
└── src/
    ├── __init__.py
    ├── main.py                   # Application entry point
    │
    ├── filesystem/
    │   ├── __init__.py
    │   ├── myfs.py              # Main MyFS class
    │   ├── metadata.py          # Metadata management
    │   │
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── file_table.py    # File table operations
    │   │   └── volume_operations.py  # Volume operations
    │   │
    │   ├── operations/
    │   │   ├── __init__.py
    │   │   ├── file_operations.py    # File operations
    │   │   └── security_operations.py # Security operations
    │   │
    │   └── utils/
    │       └── __init__.py
    │
    ├── security/
    │   ├── __init__.py
    │   ├── authentication.py    # User authentication
    │   ├── encryption.py        # File encryption
    │   └── integrity.py         # Data integrity
    │
    ├── ui/
    │   ├── __init__.py
    │   └── cli.py              # Command-line interface
    │
    └── utils/
        ├── __init__.py
        ├── logger.py           # Logging system
        ├── system_info.py      # System information
        └── file_operations.py  # File utilities
```

## 🚫 Files NOT to Include

### Temporary/Development Files
- `backup/` - Backup directory
- `old_files_backup/` - Old file backups
- `*.backup` - Backup files
- `*_fixed.py` - Fixed versions (keep original)
- `replace_debug_prints.py` - Development tool
- `test_file_listing_fix.py` - Test script
- `emergency_recovery.py` - Emergency tool
- `FIX_SUMMARY.md` - Development notes

### Runtime/Generated Files
- `__pycache__/` - Python cache
- `*.pyc`, `*.pyo` - Compiled Python
- `logs/` - Log files
- `system_integrity.json` - Runtime data
- `*.myfs`, `*.vol` - MyFS volumes

### IDE/OS Files
- `.vscode/`, `.idea/` - IDE settings
- `.DS_Store`, `Thumbs.db` - OS files

## 🛠️ Repository Preparation Steps

### 1. Clean Repository
```bash
# Run the cleanup script
python prepare_repository.py

# Or manually remove files
rm -rf __pycache__ backup old_files_backup logs
rm replace_debug_prints.py test_file_listing_fix.py
rm emergency_recovery.py FIX_SUMMARY.md
```

### 2. Verify Structure
```bash
# Check essential files are present
ls -la src/
ls -la src/filesystem/
ls -la src/security/
ls -la README*.md
```

### 3. Initialize Git (if new repo)
```bash
git init
git add .gitignore
git add README.md README_EN.md README_VI.md
git add requirements.txt setup.py
git add src/
git commit -m "Initial commit: MyFS secure file system"
```

### 4. Add Remote and Push
```bash
# Add your GitHub repository
git remote add origin https://github.com/yourusername/myfs.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 📋 Quality Checklist

### Before Pushing
- [ ] All debug prints replaced with logger calls
- [ ] No backup files included
- [ ] No __pycache__ directories
- [ ] README files are complete
- [ ] requirements.txt is updated
- [ ] All essential files present
- [ ] .gitignore is configured

### Code Quality
- [ ] No syntax errors
- [ ] Proper error handling
- [ ] Consistent coding style
- [ ] Comments in Vietnamese/English
- [ ] Security methods implemented

### Documentation
- [ ] Installation instructions
- [ ] Usage examples
- [ ] Feature descriptions
- [ ] Troubleshooting guide
- [ ] API documentation

## 🎯 Repository Best Practices

### Branch Strategy
- `main` - Stable release branch
- `develop` - Development branch  
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches

### Commit Messages
```
feat: add file password change functionality
fix: resolve volume operations syntax errors
docs: update README with security features
refactor: replace debug prints with logger calls
```

### Tags/Releases
```bash
# Tag stable versions
git tag -a v1.0.0 -m "MyFS v1.0.0 - Initial release"
git push origin v1.0.0
```

## 📊 File Size Recommendations

### Keep Small
- Individual files < 1MB
- Total repository < 100MB
- Documentation files < 500KB

### Exclude Large Files
- Test data files
- Sample MyFS volumes
- Binary dependencies
- Large log files

## 🔒 Security Considerations

### Sensitive Information
- No hardcoded passwords
- No API keys or secrets
- No personal file paths
- No system-specific configurations

### Code Security
- Input validation
- Error handling
- Secure defaults
- No debug information in production

## 📝 License Considerations

Add appropriate license file:
- MIT License (recommended for open source)
- Apache 2.0 License
- GPL v3 (if using GPL dependencies)
- Custom license for academic projects

## 🚀 Deployment Notes

### For Academic Submission
- Include Vietnamese documentation
- Add project report if required
- Include demo screenshots
- Document test cases

### For Open Source
- Complete English documentation
- Contributing guidelines
- Issue templates
- CI/CD configuration
