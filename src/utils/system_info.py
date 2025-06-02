import platform
import uuid
import hashlib
import os
import socket
import subprocess
import re

class SystemInfo:
    def __init__(self):
        """Initialize SystemInfo module"""
        pass
    
    def get_system_fingerprint(self):
        """
        Generate a unique fingerprint for the current system
        
        Returns:
            str: A unique identifier for the system
        """
        # Collect system information
        system_data = {
            "machine_id": self.get_machine_id(),
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_build": platform.python_build(),
            "mac_address": self.get_mac_address()
        }
        
        # Generate fingerprint by hashing system data
        fingerprint = hashlib.sha256(str(system_data).encode()).hexdigest()
        return fingerprint
    
    def get_machine_id(self):
        """
        Get a machine ID that is relatively stable across boots
        
        Returns:
            str: Machine ID string
        """
        if platform.system() == "Windows":
            # Try to get Windows product ID
            try:
                cmd = 'wmic csproduct get UUID'
                uuid = subprocess.check_output(cmd, shell=True).decode().strip()
                # Extract just the UUID part
                uuid = re.search(r'UUID\s*(.*)', uuid).group(1).strip()
                return uuid
            except:
                # Fallback to MAC address
                return str(uuid.getnode())
        elif platform.system() == "Linux":
            # Try to read machine-id in Linux
            try:
                with open('/etc/machine-id', 'r') as f:
                    return f.read().strip()
            except:
                return str(uuid.getnode())
        elif platform.system() == "Darwin":  # macOS
            try:
                # Use system_profiler to get hardware UUID
                cmd = 'system_profiler SPHardwareDataType | grep "Hardware UUID"'
                output = subprocess.check_output(cmd, shell=True).decode()
                hw_uuid = output.split(': ')[1].strip()
                return hw_uuid
            except:
                return str(uuid.getnode())
        else:
            # Fallback for other systems
            return str(uuid.getnode())
    
    def get_mac_address(self):
        """
        Get the MAC address of the main network interface
        
        Returns:
            str: MAC address as a hex string
        """
        mac = uuid.getnode()
        return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    
    def verify_system(self, stored_fingerprint):
        """
        Verify if current system matches stored fingerprint
        
        Args:
            stored_fingerprint (str): Previously stored system fingerprint
            
        Returns:
            bool: True if system matches, False otherwise
        """
        current_fingerprint = self.get_system_fingerprint()
        return current_fingerprint == stored_fingerprint
    
    def dump_system_info(self):
        """
        Return a dictionary with detailed system information for debugging
        
        Returns:
            dict: System information
        """
        cpu_info = {}
        try:
            if platform.system() == "Windows":
                cpu_info = {
                    "processor": platform.processor(),
                    "physical_cores": os.cpu_count()
                }
            else:
                # More detailed CPU info for Linux/Mac
                cpu_info = {
                    "processor": platform.processor(),
                    "physical_cores": os.cpu_count()
                }
        except:
            cpu_info = {"processor": "Unknown"}
            
        return {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_info": cpu_info,
            "mac_address": self.get_mac_address(),
            "machine_id": self.get_machine_id(),
            "fingerprint": self.get_system_fingerprint()
        }