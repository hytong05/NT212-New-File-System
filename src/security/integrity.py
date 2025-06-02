import hashlib
import os
import json
import platform
import uuid
import psutil
from datetime import datetime
from ..utils.logger import logger

class SystemIntegrity:
    def __init__(self):
        self.integrity_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'system_integrity.json'
        )
        self.backup_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'backup'
        )
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def get_file_hash(self, file_path):
        """Calculate SHA256 hash of a file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def get_system_fingerprint(self):
        """Get unique system fingerprint"""
        try:
            # Get system information
            system_info = {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'node': platform.node(),
                'mac_address': ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                       for elements in range(0, 2*6, 2)][::-1])
            }
            
            # Get disk serial number if available
            try:
                partitions = psutil.disk_partitions()
                if partitions:
                    # Use the first partition's device
                    disk_usage = psutil.disk_usage(partitions[0].mountpoint)
                    system_info['disk_total'] = disk_usage.total
            except:
                pass
            
            # Create fingerprint hash
            fingerprint_str = json.dumps(system_info, sort_keys=True)
            return hashlib.sha256(fingerprint_str.encode()).hexdigest()
            
        except Exception as e:
            logger.error(f"Error generating system fingerprint: {e}")
            return None
    
    def create_integrity_baseline(self):
        """Create baseline integrity information"""
        try:
            logger.info("Creating system integrity baseline...")
            
            # Get current system fingerprint
            system_fingerprint = self.get_system_fingerprint()
            
            # Calculate hashes for critical files
            src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src')
            critical_files = []
            
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, src_dir)
                        file_hash = self.get_file_hash(file_path)
                        if file_hash:
                            critical_files.append({
                                'path': rel_path,
                                'hash': file_hash,
                                'size': os.path.getsize(file_path),
                                'modified': os.path.getmtime(file_path)
                            })
            
            # Create integrity data
            integrity_data = {
                'created_at': datetime.now().isoformat(),
                'system_fingerprint': system_fingerprint,
                'critical_files': critical_files,
                'version': '1.0'
            }
            
            # Save to file
            with open(self.integrity_file, 'w', encoding='utf-8') as f:
                json.dump(integrity_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Integrity baseline created with {len(critical_files)} files")
            return True
            
        except Exception as e:
            logger.error(f"Error creating integrity baseline: {e}")
            return False
    
    def verify_system_integrity(self):
        """Verify system integrity against baseline"""
        try:
            if not os.path.exists(self.integrity_file):
                logger.warning("No integrity baseline found. Creating new baseline...")
                return self.create_integrity_baseline()
            
            # Load baseline
            with open(self.integrity_file, 'r', encoding='utf-8') as f:
                baseline = json.load(f)
            
            logger.info("Verifying system integrity...")
            
            # Check system fingerprint
            current_fingerprint = self.get_system_fingerprint()
            if current_fingerprint != baseline.get('system_fingerprint'):
                logger.warning("System fingerprint mismatch detected!")
                return False
            
            # Check file integrity
            src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src')
            violations = []
            
            for file_info in baseline.get('critical_files', []):
                file_path = os.path.join(src_dir, file_info['path'])
                
                if not os.path.exists(file_path):
                    violations.append(f"Missing file: {file_info['path']}")
                    continue
                
                current_hash = self.get_file_hash(file_path)
                if current_hash != file_info['hash']:
                    violations.append(f"Modified file: {file_info['path']}")
                    continue
                
                current_size = os.path.getsize(file_path)
                if current_size != file_info['size']:
                    violations.append(f"Size changed: {file_info['path']}")
            
            if violations:
                logger.error(f"Integrity violations detected: {violations}")
                return False
            
            logger.info("System integrity verified successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying system integrity: {e}")
            return False
    
    def restore_from_backup(self):
        """Attempt to restore files from backup"""
        try:
            logger.info("Attempting to restore from backup...")
            
            # This would contain backup restoration logic
            # For now, we'll log the attempt
            logger.warning("Backup restoration not implemented yet")
            return False
            
        except Exception as e:
            logger.error(f"Error during backup restoration: {e}")
            return False
    
    def verify_machine_authorization(self, myfs_path):
        """Verify if current machine is authorized to access MyFS"""
        try:
            logger.info(f"Verifying machine authorization for {myfs_path}")
            
            # Check if there's a machine fingerprint stored with the MyFS
            machine_file = f"{myfs_path}.machine"
            current_fingerprint = self.get_system_fingerprint()
            
            if not os.path.exists(machine_file):
                # First time - create machine fingerprint
                with open(machine_file, 'w') as f:
                    f.write(current_fingerprint)
                logger.info("Machine fingerprint created for first-time access")
                return True
            
            # Check existing fingerprint
            with open(machine_file, 'r') as f:
                stored_fingerprint = f.read().strip()
            
            if current_fingerprint == stored_fingerprint:
                logger.info("Machine authorization verified")
                return True
            else:
                logger.error("Machine authorization failed - unauthorized access attempt")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying machine authorization: {e}")
            return False

# Global integrity checker
integrity_checker = SystemIntegrity()

def check_data_integrity(file_path):
    # Implement logic to check the integrity of the file
    return integrity_checker.get_file_hash(file_path)

def recover_file(file_path):
    # Implement logic to recover a file if it has been corrupted or deleted
    return integrity_checker.restore_from_backup()

def log_integrity_check(file_path, status):
    # Implement logic to log the results of the integrity check
    logger.info(f"Integrity check for {file_path}: {status}")

def verify_file(file_path):
    # Implement logic to verify the file's authenticity and integrity
    return integrity_checker.verify_system_integrity()