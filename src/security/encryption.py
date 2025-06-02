import os
import hashlib
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from utils.logger import logger

class Encryption:
    """Class for handling encryption and decryption in MyFS"""
    
    def __init__(self):
        """Initialize the encryption module"""
        pass
        
    def generate_key_from_password(self, password, salt=None):
        """
        Generate a key from a password using PBKDF2 with consistent parameters
        
        Args:
            password (str): The password to derive the key from
            salt (bytes, optional): Salt for key derivation
            
        Returns:
            dict: Dictionary with key and salt
        """
        # Always use a consistent approach for salt handling
        if salt is None:
            salt = os.urandom(16)
        elif isinstance(salt, str):
            # Convert hex string to bytes if needed
            try:
                salt = bytes.fromhex(salt)
            except ValueError:
                salt = salt.encode('utf-8')
        
        logger.debug(f"Using salt: {salt.hex()}")
        
        # Always use the same parameters for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=100000,  # This value must be consistent
            backend=default_backend()
        )
        
        # Derive the key using UTF-8 encoded password
        key = kdf.derive(password.encode('utf-8'))
        
        # Store both the binary key and a hex version for debug purposes
        return {
            "key": key,
            "key_hex": key.hex(),  # For debugging
            "salt": salt,
            "salt_hex": salt.hex()  # For debugging
        }
        
    def generate_verification_hash(self, key):
        """
        Generate a verification hash for a key
        
        Args:
            key (bytes): The key to generate a hash for
            
        Returns:
            str: Base64-encoded hash for verification
        """
        # Create a hash of the key for verification
        digest = hashlib.sha256(key).digest()
        return base64.b64encode(digest).decode('utf-8')
        
    def verify_key(self, key, verification_hash):
        """
        Verify a key against a verification hash
        
        Args:
            key (bytes): The key to verify
            verification_hash (str): Base64-encoded verification hash
            
        Returns:
            bool: True if verified, False otherwise
        """
        # Hash the key and compare with stored hash
        digest = hashlib.sha256(key).digest()
        calculated_hash = base64.b64encode(digest).decode('utf-8')
        
        return calculated_hash == verification_hash
    
    def calculate_checksum(self, data):
        """
        Calculate a SHA-256 checksum for data integrity verification
        
        Args:
            data (bytes): The data to calculate checksum for
            
        Returns:
            str: Hex-encoded checksum
        """
        return hashlib.sha256(data).hexdigest()
        
    def encrypt_data(self, plaintext, key):
        """
        Encrypt data using AES-GCM with a consistent format
        
        Args:
            plaintext (bytes): Data to encrypt
            key (bytes): Encryption key
            
        Returns:
            bytes: Encrypted data with format information
        """
        # Generate a random 96-bit IV (12 bytes) as recommended for GCM
        iv = os.urandom(12)
        
        # Create cipher object
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        
        # Create encryptor
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        # Get authentication tag
        tag = encryptor.tag
        
        # Create a data structure with all components
        # This ensures a consistent format that can be decoded later
        encrypted_package = {
            "iv": base64.b64encode(iv).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8'),
            "format": "aes-256-gcm"
        }
        
        # Convert to JSON and encode
        return json.dumps(encrypted_package).encode('utf-8')
        
    def decrypt_data(self, encrypted_data, key):
        """
        Decrypt data that was encrypted with encrypt_data
        
        Args:
            encrypted_data (bytes): The encrypted data package
            key (bytes): Decryption key
            
        Returns:
            bytes: Decrypted plaintext
            
        Raises:
            ValueError: If decryption fails
        """
        try:
            # Parse the encrypted package
            encrypted_package = json.loads(encrypted_data.decode('utf-8'))
            
            # Check format
            if encrypted_package.get("format") != "aes-256-gcm":
                # Try legacy format (from older versions)
                return self._decrypt_legacy_format(encrypted_data, key)
            
            # Extract components
            iv = base64.b64decode(encrypted_package["iv"])
            ciphertext = base64.b64decode(encrypted_package["ciphertext"])
            tag = base64.b64decode(encrypted_package["tag"])
            
            # Create cipher object
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            
            # Create decryptor
            decryptor = cipher.decryptor()
            
            # Decrypt
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext
            
        except json.JSONDecodeError:
            # Not in JSON format, try legacy format
            return self._decrypt_legacy_format(encrypted_data, key)
            
        except Exception as e:
            logger.debug(f"Decryption error: {type(e).__name__} - {str(e)}")
            logger.debug(f"Key length: {len(key)} bytes")
            logger.debug(f"Key hex: {key.hex()[:32]}...")
            if 'encrypted_package' in locals():
                logger.debug(f"IV length: {len(base64.b64decode(encrypted_package['iv']))} bytes")
                logger.debug(f"Ciphertext length: {len(base64.b64decode(encrypted_package['ciphertext']))} bytes")
                logger.debug(f"Tag length: {len(base64.b64decode(encrypted_package['tag']))} bytes")
            raise
            
    def _decrypt_legacy_format(self, encrypted_data, key):
        """
        Decrypt data from legacy format (directly concatenated IV+ciphertext+tag)
        
        Args:
            encrypted_data (bytes): Legacy format encrypted data
            key (bytes): Decryption key
            
        Returns:
            bytes: Decrypted plaintext
        """
        try:
            # Legacy format: [12 bytes IV][ciphertext][16 bytes tag]
            iv = encrypted_data[:12]
            tag = encrypted_data[-16:]
            ciphertext = encrypted_data[12:-16]
            
            # Validate IV size
            if len(iv) != 12:
                raise ValueError(f"Invalid IV size in legacy format: {len(iv)} bytes")
                
            # Create cipher object
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            
            # Create decryptor
            decryptor = cipher.decryptor()
            
            # Decrypt
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext
            
        except Exception as e:
            print(f"Debug - Legacy decryption error: {str(e)}")
            raise