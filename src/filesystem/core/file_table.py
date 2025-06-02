import os
import json
from datetime import datetime

class FileTableManager:
    def __init__(self, myfs):
        """Initialize file table manager
        
        Args:
            myfs: MyFS instance
        """
        self.myfs = myfs
    
    def load_with_verification(self):
        """
        Load file table with extended verification and diagnostics
        
        Returns:
            bool: Success status
        """
        try:
            if not os.path.exists(self.myfs.dri_path):
                raise ValueError(f"MyFS file not found: {self.myfs.dri_path}")
                
            with open(self.myfs.dri_path, 'rb') as f:
                # Dump first 32 bytes for diagnostic purposes
                f.seek(0)
                header_bytes = f.read(32)
                print(f"Debug - First 32 bytes: {header_bytes.hex()}")
                f.seek(0)
                
                # Get file size for validation
                f.seek(0, os.SEEK_END)
                total_file_size = f.tell()
                f.seek(0)
                
                print(f"Debug - Total file size: {total_file_size} bytes")
                
                # Read header size
                header_size_bytes = f.read(4)
                if not header_size_bytes or len(header_size_bytes) < 4:
                    raise ValueError("Invalid MyFS file: could not read header size")
                    
                header_size = int.from_bytes(header_size_bytes, byteorder='big')
                print(f"Debug - Header size: {header_size} bytes")
                
                # Validate header size
                if header_size <= 0 or header_size > 100000:  # Reasonable header size limit
                    raise ValueError(f"Invalid header size: {header_size}")
                    
                # Read and verify header content
                header_content = f.read(header_size)
                try:
                    decrypted_header = self.myfs.encryption.decrypt_data(header_content, self.myfs.master_key)
                    header = json.loads(decrypted_header.decode())
                    if header.get("signature") != "MyFS":
                        raise ValueError(f"Invalid header signature: {header.get('signature')}")
                    print(f"Debug - Valid header found: version {header.get('version', 'unknown')}")
                except Exception as header_error:
                    print(f"Debug - Header decryption failed: {str(header_error)}")
                    raise ValueError("Failed to decrypt header - incorrect password or corrupted file")
                    
                # Read file table size
                file_table_size_bytes = f.read(4)
                if not file_table_size_bytes or len(file_table_size_bytes) < 4:
                    raise ValueError("Invalid MyFS file: could not read file table size")
                    
                file_table_size = int.from_bytes(file_table_size_bytes, byteorder='big')
                print(f"Debug - File table size: {file_table_size} bytes")
                
                # Validate file table size
                if file_table_size <= 0 or file_table_size > 10000000:  # 10MB limit for file table
                    raise ValueError(f"Invalid file table size: {file_table_size}")
                    
                # Check if file table fits in remaining file
                remaining_size = total_file_size - f.tell()
                if file_table_size > remaining_size:
                    raise ValueError(f"File table size ({file_table_size}) exceeds remaining file size ({remaining_size})")
                    
                # Read encrypted file table
                encrypted_file_table = f.read(file_table_size)
                if len(encrypted_file_table) < file_table_size:
                    raise ValueError(f"Expected {file_table_size} bytes for file table but got {len(encrypted_file_table)}")
                    
            # Try to decrypt the file table
            try:
                print(f"Debug - Decrypting file table ({file_table_size} bytes)")
                print(f"Debug - File table starts with: {encrypted_file_table[:32].hex()}")
                decrypted_file_table = self.myfs.encryption.decrypt_data(encrypted_file_table, self.myfs.master_key)
                
                # Parse as JSON
                file_table = json.loads(decrypted_file_table.decode())
                
                # Validate structure
                if not isinstance(file_table, dict):
                    raise ValueError("Invalid file table format: not a dictionary")
                    
                if "files" not in file_table:
                    file_table["files"] = []
                    
                if "deleted_files" not in file_table:
                    file_table["deleted_files"] = []
                    
                print(f"Debug - File table loaded successfully with {len(file_table.get('files', []))} files")
                
                # Store the file table
                self.myfs.file_table = file_table
                return True
                
            except Exception as e:
                print(f"Debug - Error decrypting file table: {str(e)}")
                return False
                
        except Exception as e:
            print(f"Debug - Error loading file table: {str(e)}")
            return False
            
    def update_safely(self):
        """
        Update file table with proper JSON serialization
        """
        try:
            # Make sure we have a file table to update
            if not hasattr(self.myfs, 'file_table') or not self.myfs.file_table:
                self.myfs.file_table = {
                    "version": "2.0",
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                    "files": [], 
                    "deleted_files": []
                }
                
            # Update timestamp
            self.myfs.file_table["updated"] = datetime.now().isoformat()
            
            # Tạo bản sao để chuyển đổi các dữ liệu bytes thành hex string
            serializable_file_table = self._make_json_serializable(self.myfs.file_table)
            
            # Mã hóa và lưu file_table
            encrypted_file_table = self.myfs.encryption.encrypt_data(
                json.dumps(serializable_file_table).encode(), 
                self.myfs.master_key
            )
            print(f"Debug - Encrypted file table: {len(encrypted_file_table)} bytes")
            print(f"Debug - File table starts with: {encrypted_file_table[:32].hex()}")
            
            # Create temporary file for safe writing
            temp_file = self.myfs.dri_path + ".temp"
            
            # Read the current MyFS file
            try:
                with open(self.myfs.dri_path, 'rb') as f:
                    # Read header size
                    header_size_bytes = f.read(4)
                    if not header_size_bytes or len(header_size_bytes) < 4:
                        raise ValueError("Invalid MyFS file: could not read header size")
                        
                    header_size = int.from_bytes(header_size_bytes, byteorder='big')
                    
                    # Read header
                    encrypted_header = f.read(header_size)
                    
                    # Skip old file table
                    old_file_table_size_bytes = f.read(4)
                    if not old_file_table_size_bytes or len(old_file_table_size_bytes) < 4:
                        raise ValueError("Invalid MyFS file: could not read file table size")
                        
                    old_file_table_size = int.from_bytes(old_file_table_size_bytes, byteorder='big')
                    f.seek(old_file_table_size, os.SEEK_CUR)
                    
                    # Read remaining content (file data)
                    remaining_content = f.read()
                    
                # Write updated content to temporary file
                with open(temp_file, 'wb') as f:
                    # Write header size and header
                    f.write(header_size_bytes)
                    f.write(encrypted_header)
                    
                    # Write new file table size and table
                    f.write(len(encrypted_file_table).to_bytes(4, byteorder='big'))
                    f.write(encrypted_file_table)
                    
                    # Write remaining content
                    f.write(remaining_content)
                    
                # Replace the original file with the temporary file
                if os.path.exists(self.myfs.dri_path):
                    os.replace(temp_file, self.myfs.dri_path)
                else:
                    os.rename(temp_file, self.myfs.dri_path)
                    
            except Exception as read_error:
                # If read fails, try writing a new file with just header and file table
                try:
                    # Create header
                    header = {
                        "signature": "MyFS",
                        "version": "2.0",
                        "created": datetime.now().isoformat(),
                        "recovered": True
                    }
                    
                    # Encrypt header
                    encrypted_header = self.myfs.encryption.encrypt_data(json.dumps(header).encode(), self.myfs.master_key)
                    
                    # Write to temporary file
                    with open(temp_file, 'wb') as f:
                        # Write header size and header
                        f.write(len(encrypted_header).to_bytes(4, byteorder='big'))
                        f.write(encrypted_header)
                        
                        # Write file table size and table
                        f.write(len(encrypted_file_table).to_bytes(4, byteorder='big'))
                        f.write(encrypted_file_table)
                    
                    # Replace original file
                    if os.path.exists(self.myfs.dri_path):
                        os.replace(temp_file, self.myfs.dri_path)
                    else:
                        os.rename(temp_file, self.myfs.dri_path)
                        
                except Exception as write_error:
                    print(f"Debug - Error creating new file structure: {str(write_error)}")
                    raise ValueError(f"Failed to update file table: {str(write_error)}")
            
            # Update file positions
            self.update_file_positions()
            
            print(f"Debug - File table updated successfully with {len(self.myfs.file_table.get('files', []))} files")
            return True
            
        except Exception as e:
            print(f"Debug - Error updating file table: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Failed to update file table: {str(e)}")
    
    def update_file_positions(self):
        """
        Update file position information after file table changes
        
        This ensures files can still be found even if the file table size changes
        """
        try:
            # Calculate the file table section size
            with open(self.myfs.dri_path, 'rb') as f:
                # Skip header size and header
                header_size_bytes = f.read(4)
                header_size = int.from_bytes(header_size_bytes, byteorder='big')
                f.seek(header_size, os.SEEK_CUR)
                
                # Read file table size
                file_table_size_bytes = f.read(4)
                file_table_size = int.from_bytes(file_table_size_bytes, byteorder='big')
                
                # Calculate the offset where actual file data begins
                data_start = 4 + header_size + 4 + file_table_size
                
                # No need to update if we don't have any files
                if not hasattr(self.myfs, 'file_table') or not self.myfs.file_table or not self.myfs.file_table.get('files'):
                    return
                    
                # Check if positions need updating
                positions_updated = False
                for file_info in self.myfs.file_table['files']:
                    if file_info.get('position', 0) < data_start:
                        # This file position needs updating
                        print(f"Debug - Updating file position for {file_info['name']}: {file_info['position']} -> {data_start}")
                        file_info['position'] = data_start
                        data_start += file_info.get('encrypted_size', 0)
                        positions_updated = True
                    else:
                        # Skip this file
                        data_start = file_info['position'] + file_info.get('encrypted_size', 0)
                        
                # If positions were updated, we need to re-save the file table, but without calling this method again
                if positions_updated:
                    print(f"Debug - Re-saving file table with updated positions")
                    # Encrypt the file table
                    encrypted_file_table = self.myfs.encryption.encrypt_data(json.dumps(self.myfs.file_table).encode(), self.myfs.master_key)
                    
                    # Update just the file table section
                    with open(self.myfs.dri_path, 'r+b') as f:
                        # Skip header size and header
                        f.seek(4 + header_size)
                        
                        # Write new file table size and content
                        f.write(len(encrypted_file_table).to_bytes(4, byteorder='big'))
                        f.write(encrypted_file_table)
                        
                        # Don't modify any other content
        except Exception as e:
            print(f"Debug - Error updating file positions: {str(e)}")
            # This is non-critical, so don't propagate the exception
    
    def _make_json_serializable(self, obj):
        """
        Đệ quy chuyển đổi các đối tượng bytes thành chuỗi hex
        """
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, bytes):
            return obj.hex()
        else:
            return obj
