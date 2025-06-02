import os
import json
from datetime import datetime

class MetadataManager:
    def __init__(self, myfs):
        """
        Initialize metadata manager
        
        Args:
            myfs: MyFS instance
        """
        self.myfs = myfs
        
    def update(self):
        """
        Update the metadata file
    
        Returns:
        bool: True if updated successfully
        """
        try:
            # Make sure we have metadata to update
            if not hasattr(self.myfs, 'metadata') or not self.myfs.metadata:
                if not hasattr(self.myfs, 'master_key'):
                    print(f"Debug - Cannot update metadata: no master key")
                    return False
                    
                # Initialize basic metadata
                self.myfs.metadata = {
                    "version": "2.0",
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                    "file_keys": {}
                }
                
                # Add salt if available
                if hasattr(self.myfs, 'master_salt'):
                    self.myfs.metadata["salt"] = self.myfs.master_salt.hex()
                    
                # Add key verification
                self.myfs.metadata["key_verification"] = self.myfs.encryption.generate_verification_hash(self.myfs.master_key)
            else:
                # Update the timestamp
                self.myfs.metadata["updated"] = datetime.now().isoformat()
            
            # Ensure metadata has all required fields
            if "version" not in self.myfs.metadata:
                self.myfs.metadata["version"] = "2.0"
                
            if "created" not in self.myfs.metadata:
                self.myfs.metadata["created"] = datetime.now().isoformat()
                
            if "file_keys" not in self.myfs.metadata:
                self.myfs.metadata["file_keys"] = {}
                
            if "key_verification" not in self.myfs.metadata:
                self.myfs.metadata["key_verification"] = self.myfs.encryption.generate_verification_hash(self.myfs.master_key)
                
            # Make sure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.myfs.metadata_path)), exist_ok=True)
            
            # Encrypt the metadata
            encrypted_metadata = self.myfs.encryption.encrypt_data(json.dumps(self.myfs.metadata).encode(), self.myfs.master_key)
            
            # Write to metadata file
            with open(self.myfs.metadata_path, 'wb') as f:
                f.write(encrypted_metadata)
                
            print(f"Debug - Metadata updated successfully")
            return True
            
        except Exception as e:
            print(f"Debug - Error updating metadata: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Failed to update metadata: {str(e)}")
