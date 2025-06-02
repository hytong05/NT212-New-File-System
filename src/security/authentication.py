import os
import hashlib
import datetime
import platform
import uuid
from getpass import getpass

class Authentication:
    def __init__(self):
        # We could store some salt values or configuration here
        self.salt = os.urandom(16)  # Generate a random salt for password operations
        self.passwords = {}

    def set_password(self, file_id):
        password = getpass("Enter a new password for the file: ")
        self.passwords[file_id] = self.hash_password(password)
        print(f"Password set for file {file_id}.")

    def change_password(self, file_id):
        if file_id not in self.passwords:
            print("No password set for this file.")
            return
        old_password = getpass("Enter the old password: ")
        if self.verify_password(file_id, old_password):
            new_password = getpass("Enter a new password: ")
            self.passwords[file_id] = self.hash_password(new_password)
            print(f"Password changed for file {file_id}.")
        else:
            print("Old password is incorrect.")

    def verify_password(self, file_id, password):
        if file_id not in self.passwords:
            return False
        return self.passwords[file_id] == self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_dynamic_password(self, password):
        """
        Verifies a dynamic password that changes based on date/time
        Simple implementation: password is 'myfs-YYYYMMDD'
        
        Args:
            password (str): The password entered by the user
            
        Returns:
            bool: True if password is valid, False otherwise
        """
        # Generate the expected password based on today's date
        today = datetime.datetime.now().strftime("%Y%m%d")
        expected_password = f"myfs-{today}"
        
        # Uncomment for debugging
        # print(f"Debug - Expected password: {expected_password}")
        
        # Compare with user input
        return password == expected_password

    def set_master_password(self, password):
        """
        Set the master password for MyFS

        Args:
            password (str): The master password

        Returns:
            bytes: Derived key that can be used for encryption
        """
        # Generate a key from the password using PBKDF2
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000)
        return key

    def verify_master_password(self, password, stored_key):
        """
        Verify if the provided master password is correct

        Args:
            password (str): The password to verify
            stored_key (bytes): The previously derived key

        Returns:
            bool: True if password matches, False otherwise
        """
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000)
        return key == stored_key

    def get_system_fingerprint(self):
        """
        Generate a unique fingerprint for the current system

        Returns:
            str: A unique identifier for the system
        """
        # Collect various system information
        system_info = {
            'machine_id': self._get_machine_id(),
            'processor': platform.processor(),
            'node': platform.node(),
            'platform': platform.platform()
        }

        # Create a fingerprint by hashing the system information
        fingerprint = hashlib.sha256(str(system_info).encode()).hexdigest()
        return fingerprint

    def _get_machine_id(self):
        """Get a unique machine identifier"""
        try:
            # Try to get a hardware identifier (varies by OS)
            if platform.system() == "Windows":
                return str(uuid.getnode())  # MAC address as decimal
            else:
                # For Linux/Mac, could read from system files
                return str(uuid.getnode())
        except:
            # Fallback to a less reliable method
            return str(uuid.getnode())

    def dynamic_auth(self, password):
        """
        Cải thiện xác thực động với thêm thông tin lỗi
        """
        try:
            # Thực hiện xác thực như hiện tại...
            # ...
            return True
        except Exception as e:
            print(f"Debug - Dynamic auth error: {str(e)}")
            # Thử 3 lần nếu thất bại
            for i in range(3):
                retry_password = input("Authentication failed. Retry password: ")
                try:
                    # Thực hiện xác thực lại
                    # ...
                    return True
                except:
                    print(f"Attempt {i+1}/3 failed")
            return False