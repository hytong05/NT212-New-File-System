# MyFS - Secure File System

## Overview

MyFS (My File System) is a comprehensive secure file management system designed to create, manage, and protect files within encrypted virtual volumes. The system provides enterprise-grade security features including file encryption, machine authorization, integrity verification, and advanced recovery capabilities.

## 🚀 Key Features

### 🔐 **Security Features**
- **Dynamic Authentication**: Time-based dynamic passwords that change daily (format: `myfs-YYYYMMDD`)
- **Machine Authorization**: Ensures MyFS volumes only run on authorized machines using hardware fingerprinting
- **AES-256 Encryption**: Military-grade encryption for all file contents
- **Individual File Passwords**: Optional password protection for individual files
- **System Integrity Checking**: Continuous monitoring for tampering and corruption

### 📁 **File Management**
- **Secure Volume Creation**: Create encrypted `.DRI` volumes with separate metadata storage
- **File Import/Export**: Securely import files into MyFS and export them with integrity verification
- **Soft/Hard Delete**: Recoverable deletion and permanent purging capabilities
- **File Recovery**: Restore accidentally deleted files from the recycle system
- **Metadata Backup**: Automatic backup of volume metadata for disaster recovery

### 🛡️ **Advanced Security**
- **Tamper Detection**: Real-time detection of unauthorized modifications
- **Auto-Recovery**: Automatic restoration from backup when corruption is detected
- **Comprehensive Logging**: Detailed audit trails with timestamped file-based logging
- **Emergency Repair**: Volume repair functionality for corrupted MyFS volumes

## 📋 Prerequisites

- Python 3.7 or higher
- Windows, macOS, or Linux operating system
- Required Python packages (see requirements.txt)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd myfs-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python src/main.py
   ```

## 📦 Dependencies

```
cryptography==3.4.7    # Advanced encryption operations
psutil==5.9.5          # System information gathering
pycryptodome==3.10.1   # Additional cryptographic functions
pytest==6.2.4         # Testing framework
Flask==2.0.1           # Web framework (future web interface)
click==8.0.1           # Command line interface utilities
```

## 🚀 Quick Start

1. **Launch MyFS:**
   ```bash
   python src/main.py
   ```

2. **Enter dynamic authentication:**
   - Format: `myfs-YYYYMMDD`
   - Example for Dec 25, 2024: `myfs-20241225`

3. **Create your first volume:**
   - Choose option 1 from the main menu
   - Specify volume location and metadata storage path
   - Set a strong master password

4. **Start managing files:**
   - Import files with option 5
   - List files with option 3
   - Export files with option 6

## 📖 Detailed Usage Guide

### 🆕 Creating a MyFS Volume

1. Select **"Create/Format MyFS volume"** from the main menu
2. **Directory Selection**: Choose where to store your `.DRI` file
3. **Volume Naming**: Enter a name for your volume (extension added automatically)
4. **Metadata Location**: Specify path for metadata storage (preferably on removable media)
5. **Master Password**: Set a strong password for volume encryption

**Example:**
```
Enter directory to store MyFS.DRI: C:\MySecureFiles
Enter name for MyFS volume (without extension): CompanyData
Enter path for metadata on removable disk: E:\Backup\CompanyData.IXF
Set master password: [Enter strong password]
```

### 🔑 Authentication System

**Dynamic Password Format:** `myfs-YYYYMMDD`
- **Daily Change**: Password changes automatically each day
- **Example Passwords:**
  - January 1, 2024: `myfs-20240101`
  - December 31, 2024: `myfs-20241231`

**Machine Authorization:**
- First access creates a hardware fingerprint
- Subsequent access requires same machine
- Prevents unauthorized volume access from different computers

### 📂 File Operations

#### **Import Files**
1. Select option 5: **"Import file to MyFS"**
2. Enter the full path to the file you want to import
3. Choose whether to add password protection
4. If password protecting: enter and confirm file password

**Supported Features:**
- Files of any size and type
- Optional individual file encryption
- Automatic integrity verification
- Metadata preservation (size, timestamps)

#### **Export Files**
1. Select option 6: **"Export file from MyFS"**
2. Choose from the list of available files
3. Specify destination path
4. Enter file password if required
5. Choose export mode:
   - **Normal**: Decrypted file
   - **Raw**: Encrypted content (for backup)

#### **File Listing**
- **Standard View**: Shows active files with metadata
- **Include Deleted**: View both active and soft-deleted files
- **Information Displayed**:
  - File name and size
  - Import timestamp
  - Protection status
  - Deletion status

### 🗑️ Deletion and Recovery

#### **Soft Delete (Recoverable)**
1. Select option 7: **"Delete file from MyFS"**
2. Choose option 1: **"Mark as deleted (recoverable)"**
3. File is hidden but can be recovered

#### **Hard Delete (Permanent)**
1. Select option 7: **"Delete file from MyFS"**
2. Choose option 2: **"Permanently delete"**
3. Confirm deletion - **this cannot be undone**

#### **File Recovery**
1. Select option 8: **"Recover deleted file"**
2. View list of recoverable files
3. Enter the name of file to recover
4. File is restored to active status

#### **Purge All Deleted Files**
1. Select option 10: **"Purge deleted files"**
2. Review list of files to be permanently deleted
3. Confirm with 'y' - **this cannot be undone**

### 🔒 Security Operations

#### **Change Master Password**
1. Select option 2: **"Change MyFS password"**
2. Enter current master password for verification
3. Enter new password twice to confirm
4. All data re-encrypted with new password

#### **Set/Change File Passwords**
1. Select option 4: **"Set/Change file password"**
2. Choose file from list
3. For existing passwords: enter current password
4. Enter new password twice to confirm
5. Option to force change without current password

### 🛠️ Maintenance and Repair

#### **Volume Repair**
1. Select option 11: **"Repair MyFS volume"**
2. Enter path to corrupted `.DRI` file
3. System checks for backup metadata
4. Enter master password for repair
5. Automatic restoration if possible

**Repair Capabilities:**
- Metadata corruption recovery
- File table reconstruction
- Integrity verification
- Backup restoration

#### **System Integrity Verification**
- **Automatic**: Runs on every startup
- **Continuous**: Monitors for changes during operation
- **Recovery**: Automatic restoration from backups when corruption detected

## 🏗️ Architecture Overview

### **Core Components**

```
src/
├── filesystem/          # Core filesystem operations
│   ├── myfs.py         # Main MyFS class
│   ├── core/           # Core functionality
│   │   ├── volume_operations.py
│   │   ├── file_table.py
│   │   └── myfs.py
│   ├── operations/     # File and security operations
│   └── utils/          # Utility functions
├── security/           # Security subsystem
│   ├── encryption.py   # AES-256 encryption
│   ├── authentication.py  # Dynamic authentication
│   └── integrity.py    # System integrity checking
├── ui/                 # User interface
│   └── cli.py         # Command line interface
└── utils/              # Shared utilities
    ├── logger.py       # Comprehensive logging
    ├── file_operations.py
    └── system_info.py
```

### **Security Architecture**

1. **Multi-Layer Encryption**:
   - Volume-level encryption with master password
   - Individual file encryption with optional passwords
   - Metadata encryption for volume structure

2. **Authentication Chain**:
   - Dynamic daily passwords for system access
   - Master password for volume access
   - Individual file passwords for sensitive files
   - Machine authorization for volume binding

3. **Integrity Protection**:
   - Hash-based file verification
   - System fingerprinting
   - Automatic backup and recovery
   - Tamper detection and alerting

## 📊 File Structure Example

```
MyFS Volume Structure:
CompanyData.DRI         # Main encrypted volume
CompanyData.IXF         # Metadata file
CompanyData.DRI.machine # Machine authorization file

Volume Contents:
├── document.pdf        (Password protected)
├── spreadsheet.xlsx    (No password)
├── presentation.pptx   (Deleted - recoverable)
└── [deleted files]     (Soft deleted items)
```

## 🔍 Menu Reference

| Option | Function | Description |
|--------|----------|-------------|
| 1 | Create/Format MyFS volume | Create new encrypted volume |
| 2 | Change MyFS password | Update master password |
| 3 | List files in MyFS | View all files in volume |
| 4 | Set/Change file password | Manage individual file passwords |
| 5 | Import file to MyFS | Add files to volume |
| 6 | Export file from MyFS | Extract files from volume |
| 7 | Delete file from MyFS | Remove files (soft/hard) |
| 8 | Recover deleted file | Restore soft-deleted files |
| 9 | View deleted files | List recoverable files |
| 10 | Purge deleted files | Permanently remove all deleted files |
| 11 | Repair MyFS volume | Fix corrupted volumes |
| 12 | Exit | Close application |

## 🧪 Testing

Run the test suite to verify system functionality:

```bash
# Run all tests
pytest tests/

# Run specific test modules
pytest tests/test_filesystem.py
pytest tests/test_security.py

# Run with verbose output
pytest -v tests/
```

## 📝 Logging and Monitoring

**Log Location**: `logs/myfs_YYYYMMDD_HHMMSS.log`

**Log Levels**:
- **DEBUG**: Detailed development information
- **INFO**: General operational messages
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: System failures

**Log Content**:
- User authentication attempts
- File operations (import/export/delete)
- Security events and violations
- System integrity checks
- Error conditions and recoveries

## 🔧 Troubleshooting

### **Common Issues**

#### **Authentication Failed**
- Verify date format: `myfs-YYYYMMDD`
- Check system date/time settings
- Ensure consistent timezone

#### **Machine Authorization Failed**
- Volume created on different machine
- Hardware configuration changed significantly
- Move volume to original machine or recreate

#### **Volume Corruption**
- Use repair function (option 11)
- Ensure backup metadata exists
- Check disk integrity

#### **File Not Found**
- Verify file paths are correct
- Check file hasn't been soft-deleted
- Ensure proper permissions

### **Emergency Recovery**

If your MyFS volume becomes corrupted:

1. **Don't panic** - backups exist
2. Use **Repair MyFS volume** (option 11)
3. Ensure backup metadata file exists
4. Have master password ready
5. Allow repair process to complete

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## ⚠️ Security Notice

- Keep your master passwords secure
- Regularly backup metadata files
- Monitor logs for security events
- Update system regularly
- Report security issues responsibly

## 📞 Support

For support, issues, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section
- Review log files for error details

---

**MyFS** - Secure, Reliable, Professional File Management
