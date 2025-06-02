# MyFS - Secure File System

## Overview

MyFS (My File System) is a comprehensive secure file management system designed to create, manage, and protect files within encrypted virtual volumes. The system provides enterprise-grade security features including dynamic authentication, machine authorization, AES-256 encryption, and advanced recovery capabilities.

> **📖 Documentation**: For complete documentation, see:
> - [English Documentation](README_EN.md) - Comprehensive English guide
> - [Vietnamese Documentation](README_VI.md) - Hướng dẫn tiếng Việt đầy đủ

## 🚀 Key Features

### Security & Authentication
- **Dynamic Daily Passwords**: Time-based authentication (format: `myfs-YYYYMMDD`)
- **Machine Authorization**: Hardware fingerprinting ensures volumes only run on authorized machines
- **AES-256 Encryption**: Military-grade encryption for all file contents
- **Individual File Passwords**: Optional password protection for sensitive files
- **System Integrity Checking**: Real-time tamper detection and auto-recovery

### File Management
- **Secure Volume Creation**: Create encrypted `.DRI` volumes with separate metadata storage
- **Import/Export Operations**: Secure file transfer with integrity verification
- **Advanced Deletion**: Soft delete (recoverable) and hard delete (permanent) options
- **File Recovery System**: Restore accidentally deleted files
- **Comprehensive Logging**: Detailed audit trails with timestamped file-based logging

### Advanced Features
- **Volume Repair**: Automatic repair of corrupted MyFS volumes
- **Backup & Recovery**: Metadata backup and emergency restoration
- **Multi-layer Security**: Volume, file, and system-level protection
- **Professional Logging**: Comprehensive monitoring and audit capabilities

## 📋 Complete Feature List

| Feature | Description | Status |
|---------|-------------|--------|
| Volume Creation | Create encrypted MyFS volumes | ✅ Complete |
| Dynamic Authentication | Daily changing passwords | ✅ Complete |
| Machine Authorization | Hardware-based access control | ✅ Complete |
| File Import/Export | Secure file operations | ✅ Complete |
| Individual File Passwords | Per-file encryption | ✅ Complete |
| Soft Delete | Recoverable file deletion | ✅ Complete |
| Hard Delete | Permanent file removal | ✅ Complete |
| File Recovery | Restore deleted files | ✅ Complete |
| Volume Repair | Fix corrupted volumes | ✅ Complete |
| System Integrity | Tamper detection | ✅ Complete |
| Comprehensive Logging | Audit trails | ✅ Complete |
| Emergency Recovery | Disaster recovery | ✅ Complete |

## 🔧 Quick Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd myfs-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run MyFS:**
   ```bash
   python src/main.py
   ```

## 🚀 Quick Start

1. **Authentication**: Enter today's password in format `myfs-YYYYMMDD`
   - Example for Dec 25, 2024: `myfs-20241225`

2. **Create Volume**: Use option 1 to create your first encrypted volume

3. **Manage Files**: Import (option 5), list (option 3), export (option 6)

## 📖 Menu Overview

```
MyFS Menu:
1. Create/Format MyFS volume      7. Delete file from MyFS
2. Change MyFS password           8. Recover deleted file
3. List files in MyFS            9. View deleted files
4. Set/Change file password      10. Purge deleted files
5. Import file to MyFS           11. Repair MyFS volume
6. Export file from MyFS         12. Exit
```

## 🏗️ Architecture

MyFS uses a modular architecture with the following components:

- **Filesystem Core**: Volume operations, file table management
- **Security System**: Encryption, authentication, integrity checking
- **User Interface**: Command-line interface with comprehensive options
- **Utilities**: Logging, system information, file operations

## 📦 Dependencies

```
cryptography==3.4.7     # Advanced encryption
psutil==5.9.5           # System information
pycryptodome==3.10.1    # Additional crypto functions
pytest==6.2.4          # Testing framework
Flask==2.0.1            # Web framework (future use)
click==8.0.1            # CLI utilities
```

## 🧪 Testing

Run the complete test suite:

```bash
# All tests
pytest tests/

# Specific modules
pytest tests/test_filesystem.py
pytest tests/test_security.py

# Verbose output
pytest -v tests/
```

## 📝 Logging

MyFS provides comprehensive logging:
- **Location**: `logs/myfs_YYYYMMDD_HHMMSS.log`
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Content**: Authentication, file operations, security events, errors

## 🔐 Security Features

- **Multi-layer Encryption**: Volume + file + metadata encryption
- **Access Control**: Dynamic passwords + machine authorization + file passwords
- **Integrity Protection**: Hash verification + tamper detection + auto-recovery
- **Audit Trail**: Comprehensive logging of all operations

## 🛠️ Advanced Usage

### File Operations
- **Import**: Secure addition of files with optional individual passwords
- **Export**: Extract files with integrity verification (normal or raw mode)
- **Delete**: Soft delete (recoverable) or hard delete (permanent)
- **Recovery**: Restore soft-deleted files from internal recycle system

### Security Operations
- **Password Management**: Change master password or individual file passwords
- **Machine Binding**: Automatic hardware fingerprinting and authorization
- **Integrity Checking**: Continuous monitoring with automatic recovery
- **Emergency Repair**: Volume repair using backup metadata

## 🔧 Troubleshooting

### Common Issues
- **Authentication Failed**: Check date format (`myfs-YYYYMMDD`)
- **Machine Authorization Failed**: Volume created on different machine
- **Volume Corruption**: Use repair function (option 11)
- **File Not Found**: Check if file was soft-deleted

### Emergency Recovery
1. Use "Repair MyFS volume" (option 11)
2. Ensure backup metadata exists (.IXF file)
3. Provide master password
4. Allow repair process to complete

---

**MyFS** - Enterprise-grade secure file management with comprehensive protection and recovery capabilities.
