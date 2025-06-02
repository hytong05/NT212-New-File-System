import os
import hashlib
import json
import shutil
import traceback
from datetime import datetime
from security.encryption import Encryption
from security.authentication import Authentication
from utils.system_info import SystemInfo

# Import các module mới tách ra
from .core.volume_operations import VolumeOperations
from .core.file_table import FileTableManager
from .operations.file_operations import FileOperations
from .operations.security_operations import SecurityOperations
from .utils.metadata import MetadataManager

class MyFS:
    def __init__(self, volume_name=None):
        """
        Initialize MyFS filesystem
        
        Args:
            volume_name (str, optional): Name of the MyFS volume
        """
        self.volume_name = volume_name
        self.file_table = {}
        self.encryption = Encryption()
        self.authentication = Authentication()
        self.system_info = SystemInfo()
        
        # Initialize managers
        self.volume_manager = VolumeOperations(self)
        self.file_table_manager = FileTableManager(self)
        self.file_operations = FileOperations(self)
        self.security_operations = SecurityOperations(self)
        self.metadata_manager = MetadataManager(self)
        
    # Forward methods to appropriate managers
    
    # Volume operations
    def create_format(self, path, removable_path, password):
        """Tạo hoặc format volume MyFS mới"""
        return self.volume_manager.create_format(path, removable_path, password)
        
    def open_volume(self, path, metadata_path, password):
        """Mở volume MyFS đã tồn tại"""
        return self.volume_manager.open_volume(path, metadata_path, password)
        
    def repair_volume(self, password=None):
        """Sửa chữa volume MyFS bị hư hỏng"""
        try:
            # Try emergency recovery using volume_manager
            if hasattr(self.volume_manager, 'emergency_recover'):
                return self.volume_manager.emergency_recover(self.dri_path, password)
            else:
                # Fallback to basic recovery attempt
                if password:
                    # Try to open with backup metadata if available
                    volume_dir = os.path.dirname(self.dri_path)
                    volume_name = os.path.basename(self.dri_path).split('.')[0]
                    backup_metadata = os.path.join(volume_dir, f"{volume_name}.IXF")
                    
                    if os.path.exists(backup_metadata):
                        print(f"Attempting repair with backup metadata: {backup_metadata}")
                        return self.open_volume(self.dri_path, backup_metadata, password)
                
                return False
        except Exception as e:
            print(f"Repair failed: {str(e)}")
            return False
        
    # File operations
    def list_files(self, include_deleted=False):
        """Liệt kê tất cả các file trong volume"""
        return self.file_operations.list_files(include_deleted)
        
    def list_deleted_files(self):
        """Liệt kê các file đã bị xóa (có thể phục hồi)"""
        return self.file_operations.list_deleted_files()
        
    def import_file(self, file_path, file_password=None):
        """Import file từ hệ thống file vào MyFS"""
        return self.file_operations.import_file(file_path, file_password)
        
    def export_file(self, file_name, destination_path, password=None, force=False, raw=False, recover=False):
        """Export file từ MyFS ra hệ thống file"""
        return self.file_operations.export_file(file_name, destination_path, password, force, raw, recover)
        
    def delete_file(self, file_name, permanent=False):
        """Xóa file khỏi MyFS"""
        return self.file_operations.delete_file(file_name, permanent)
        
    def recover_file(self, file_name):
        """Phục hồi file đã bị xóa"""
        return self.file_operations.recover_file(file_name)
        
    def purge_deleted_files(self):
        """Xóa vĩnh viễn tất cả các file đã bị xóa"""
        return self.file_operations.purge_deleted_files()
        
    # Security operations
    def check_password(self, password):
        """Kiểm tra xem password đã nhập vào có đúng không"""
        return self.security_operations.check_password(password)
        
    def change_password(self, old_password, new_password):
        """Thay đổi master password của volume"""
        return self.security_operations.change_password(old_password, new_password)
        
    def set_file_password(self, file_name, new_password, old_password=None, force=False):
        """Đặt/thay đổi password cho file riêng lẻ"""
        return self.security_operations.set_file_password(file_name, new_password, old_password, force)
        
    def check_integrity(self):
        """Kiểm tra tính toàn vẹn của file trong MyFS"""
        return self.security_operations.check_integrity()

    # Additional public methods can be forwarded to the respective managers
    
    def _authenticate_and_load(self, password):
        """
        Authenticate with password and load necessary data
        
        Args:
            password (str): Master password
            
        Returns:
            bool: True if authentication successful
        """
        try:
            # Kiểm tra xem đường dẫn đã được thiết lập chưa
            if not hasattr(self, 'dri_path') or not self.dri_path:
                raise ValueError("MyFS volume path not set")
                
            if not hasattr(self, 'metadata_path') or not self.metadata_path:
                raise ValueError("Metadata path not set")
            
            # Thử mở volume với mật khẩu đã cung cấp
            success = self.volume_manager.open_volume(
                self.dri_path, 
                self.metadata_path, 
                password
            )
            
            if not success:
                raise ValueError("Failed to authenticate with provided password")
                
            return True
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise

