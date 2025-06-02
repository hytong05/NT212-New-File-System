import os
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

class Encryption:
    def __init__(self):
        """Initialize encryption module with default settings"""
        self.backend = default_backend()
        self.iterations = 100000  # Number of iterations for PBKDF2
        self.key_length = 32  # 256 bits for AES-256
    
    def generate_key_from_password(self, password, salt=None):
        """
        Generate a cryptographic key from a password using PBKDF2
        
        Args:
            password (str): The password to derive the key from
            salt (bytes, optional): Salt for key derivation, randomly generated if None
            
        Returns:
            dict: {"key": derived_key, "salt": salt} containing bytes objects
        """
        if salt is None:
            salt = os.urandom(16)  # Generate a random 16-byte salt
            
        # Use PBKDF2 to derive a key from the password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        
        key = kdf.derive(password.encode())
        return {"key": key, "salt": salt}  # Return as dictionary instead of tuple
    
    def encrypt_data(self, plaintext, key):
        """
        Encrypt data using AES-GCM
    
        Args:
            plaintext (bytes): Data to encrypt
            key (bytes): Encryption key
            
        Returns:
            bytes: Encrypted data with IV and tag
        """
        # Generate a random IV (Initialization Vector)
        iv = os.urandom(12)  # 96 bits / 12 bytes is recommended for GCM
        
        # Create an encryptor object
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Encrypt the data
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        # Return IV + ciphertext + tag
        # Format: [12 bytes IV][ciphertext][16 bytes tag]
        return iv + ciphertext + encryptor.tag

    def decrypt_data(self, ciphertext, key):
        """
        Decrypt data using AES-GCM
    
        Args:
            ciphertext (bytes): Encrypted data with IV and tag
            key (bytes): Decryption key
            
        Returns:
            bytes: Decrypted data
            
        Raises:
            ValueError: If decryption fails
        """
        try:
            # Extract IV, ciphertext, and tag
            iv = ciphertext[:12]  # First 12 bytes are IV
            tag = ciphertext[-16:]  # Last 16 bytes are tag
            actual_ciphertext = ciphertext[12:-16]  # Middle is the actual encrypted data
            
            # Validate IV size
            if len(iv) != 12:
                raise ValueError(f"Invalid IV size: {len(iv)} bytes. Expected 12 bytes.")
                
            # Create a decryptor object
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # Decrypt the data
            padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
            
            return padded_plaintext
            
        except Exception as e:
            print(f"Debug - Decryption error: {str(e)}")
            raise
    
    def generate_verification_hash(self, key):
        """
        Generate a verification hash for key validation without storing the key
        
        Args:
            key (bytes): The key to generate verification hash for
            
        Returns:
            str: Hexadecimal verification hash
        """
        # Use a fixed verification phrase
        verification_phrase = b"MyFS-Key-Verification"
        
        # Create an HMAC using the key
        h = hmac.HMAC(key, hashes.SHA256(), backend=self.backend)
        h.update(verification_phrase)
        
        # Return hexadecimal digest
        return h.finalize().hex()
    
    def verify_key(self, key, verification_hash):
        """
        Verify if a key matches the verification hash
        
        Args:
            key (bytes): The key to verify
            verification_hash (str): Hexadecimal verification hash
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        calculated_hash = self.generate_verification_hash(key)
        return calculated_hash == verification_hash
    
    def calculate_checksum(self, data):
        """
        Calculate checksum for data integrity verification
        
        Args:
            data (bytes): Data to calculate checksum for
            
        Returns:
            str: Hexadecimal checksum
        """
        return hashlib.sha256(data).hexdigest()