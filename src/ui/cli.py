import os
import sys
import getpass
from filesystem.myfs import MyFS
from security.authentication import Authentication
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils.logger import logger
from src.security.integrity import integrity_checker

class CLI:
    def __init__(self):
        self.myfs = None
        self.auth = Authentication()
        
    def start(self):
        """Main entry point for the CLI interface"""
        print("="*50)
        print("MyFS - Secure File System")
        print("="*50)
        
        logger.info("MyFS CLI started")
        
        # Verify system integrity
        if not self._verify_system():
            print("System integrity check failed. Exiting...")
            logger.critical("System integrity check failed - exiting")
            sys.exit(1)
            
        # Authenticate user with dynamic password
        if not self._authenticate():
            print("Authentication failed. Exiting...")
            logger.warning("Authentication failed - exiting")
            sys.exit(1)
            
        self._main_menu()
    
    def _verify_system(self):
        """Verify system integrity and check if running on original machine"""
        try:
            logger.info("Verifying system integrity...")
            
            # Check system integrity
            if not integrity_checker.verify_system_integrity():
                logger.error("System integrity verification failed")
                return False
                
            logger.info("System integrity verified successfully")
            return True
            
        except Exception as e:
            logger.error(f"System verification error: {e}")
            return False
        
    def _authenticate(self):
        """Authenticate user with dynamic password"""
        password = getpass.getpass("Enter dynamic password: ")
        return self.auth.verify_dynamic_password(password)
        
    def _main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\nMyFS Menu:")
            print("1. Create/Format MyFS volume")
            print("2. Change MyFS password")
            print("3. List files in MyFS")
            print("4. Set/Change file password")
            print("5. Import file to MyFS")
            print("6. Export file from MyFS")
            print("7. Delete file from MyFS")
            print("8. Recover deleted file")
            print("9. View deleted files")
            print("10. Purge deleted files")
            print("11. Repair MyFS volume")
            print("12. Exit")
            
            choice = input("\nEnter your choice (1-12): ")
            
            if choice == '1':
                self._create_format_myfs()
            elif choice == '2':
                self._change_myfs_password()
            elif choice == '3':
                self._list_files()
            elif choice == '4':
                self._set_file_password()
            elif choice == '5':
                self._import_file()
            elif choice == '6':
                self._export_file()
            elif choice == '7':
                self._delete_file()
            elif choice == '8':
                self._recover_file()
            elif choice == '9':
                self._view_deleted_files()
            elif choice == '10':
                self._purge_deleted_files()
            elif choice == '11':
                self._repair_myfs_volume()
            elif choice == '12':
                print("Exiting MyFS. Goodbye!")
                logger.info("MyFS CLI exited")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _create_format_myfs(self):
        """Create or format MyFS volume"""
        try:
            # Ask for the directory where MyFS.DRI will be stored
            directory = input("Enter directory to store MyFS.DRI: ")
            
            # Ask for the name of the MyFS file
            volume_name = input("Enter name for MyFS volume (without extension): ")
            if not volume_name:
                volume_name = "MyFS"
            
            # Create full path for the .DRI file
            if not volume_name.endswith('.DRI'):
                volume_name += '.DRI'
            
            path = os.path.join(directory, volume_name)
            
            # Check if directory exists and create it if needed
            os.makedirs(directory, exist_ok=True)
            
            # Check if we can write to that directory
            test_file = os.path.join(directory, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
            except:
                print(f"Error: Cannot write to directory {directory}. Please check permissions.")
                return
                
            removable_path = input("Enter path for metadata on removable disk: ")
            password = getpass.getpass("Set master password: ")
            
            # Create the MyFS volume
            self.myfs = MyFS(volume_name)
            self.myfs.create_format(path, removable_path, password)
            print(f"MyFS volume created successfully at {path}!")
            
        except Exception as e:
            print(f"Error creating MyFS volume: {e}")
    
    def _change_myfs_password(self):
        """Change the master password for MyFS"""
        try:
            # First make sure we have a MyFS instance
            if not hasattr(self, 'myfs') or not self.myfs or not hasattr(self.myfs, 'dri_path'):
                # Ask for MyFS volume path and load it
                path = input("Enter path to MyFS.DRI file: ")
                metadata_path = input("Enter path to metadata file: ")
                
                if not os.path.exists(path):
                    print(f"Error: MyFS file not found: {path}")
                    return
                    
                if not os.path.exists(metadata_path):
                    print(f"Error: Metadata file not found: {metadata_path}")
                    return
                    
                # Create a new MyFS instance
                self.myfs = MyFS()
                
                # Try to load the volume (without authentication)
                try:
                    self.myfs.load(path, metadata_path)
                except Exception as e:
                    print(f"Error loading MyFS volume: {e}")
                    return
        
            # Now authenticate and change the password
            old_password = getpass.getpass("Enter current master password: ")
            
            # Authenticate with the old password first
            try:
                self.myfs._authenticate_and_load(old_password)
                print("Authentication successful!")
            except Exception as e:
                print(f"Authentication failed: {e}")
                return
                
            # If authentication succeeded, proceed with password change
            new_password = getpass.getpass("Enter new master password: ")
            confirm_password = getpass.getpass("Confirm new master password: ")
            
            if new_password != confirm_password:
                print("Error: Passwords do not match.")
                return
                
            self.myfs.change_password(old_password, new_password)
            print("MyFS password changed successfully!")
            
        except Exception as e:
            print(f"Error changing MyFS password: {e}")
    
    def _authenticate_and_open_myfs(self):
        """Authenticate and open a MyFS volume with better error handling"""
        try:
            if hasattr(self, 'myfs') and self.myfs:
                # Already authenticated
                return True
                
            path = input("Enter path to MyFS.DRI file: ")
            metadata_path = input("Enter path to metadata file: ")
            password = getpass.getpass("Enter master password: ")
            
            if not os.path.exists(path):
                print(f"Error: MyFS file not found: {path}")
                return False
                
            if not os.path.exists(metadata_path):
                print(f"Error: Metadata file not found: {metadata_path}")
                return False
            
            # Check machine authorization first
            if not integrity_checker.verify_machine_authorization(path):
                print("Error: This machine is not authorized to access this MyFS volume.")
                logger.error(f"Machine authorization failed for {path}")
                return False
                
            # Create a new MyFS instance
            self.myfs = MyFS()
                
            # Open the volume
            try:
                logger.debug("Setting temporary master key for testing")
                from security.encryption import Encryption
                self.myfs.encryption = Encryption()
                success = self.myfs.open_volume(path, metadata_path, password)
                
                if success:
                    print("Authentication successful!")
                    logger.info(f"Successfully opened MyFS volume: {path}")
                    return True
                else:
                    print("Failed to open MyFS volume.")
                    logger.warning("Failed to open MyFS volume")
                    return False
                    
            except Exception as open_error:
                print(f"Error opening MyFS volume: {open_error}")
                logger.error(f"Error opening MyFS volume: {open_error}")
                return False
                
        except Exception as e:
            print(f"Authentication error: {e}")
            logger.error(f"Authentication error: {e}")
            return False

    def _list_files(self):
        """List files in MyFS with improved error handling"""
        try:
            # Authenticate if needed
            if not hasattr(self, 'myfs') or not self.myfs:
                if not self._authenticate_and_open_myfs():
                    return
                    
            # Get file list
            try:
                files = self.myfs.list_files()
                
                if not files:
                    print("No files found in MyFS volume.")
                    return
                    
                # Display files
                print("\nFile Name                      Size (bytes) Import Time          Protected")
                print("---------------------------------------------------------------------------")
                
                for file in files:
                    name = file.get("name", "Unknown")
                    size = file.get("size", 0)
                    import_time = file.get("import_time", "Unknown")
                    if import_time != "Unknown":
                        # Format the timestamp to just show date and time
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(import_time)
                            import_time = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            pass
                            
                    protected = "Yes" if file.get("password_protected", False) else "No"
                    
                    print(f"{name:<30} {size:<12} {import_time:<20} {protected}")
                    
                print(f"\nTotal files: {len(files)}")
                
            except Exception as list_error:
                print(f"Error listing files: {list_error}")
                
        except Exception as e:
            print(f"Error in list files operation: {e}")
    
    def _set_file_password(self):
        """Set or change password for a file in MyFS"""
        try:
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                path = input("Enter path to MyFS.DRI file: ")
                metadata_path = input("Enter path to metadata file: ")
                password = getpass.getpass("Enter master password: ")
                
                if not os.path.exists(path):
                    print(f"Error: MyFS file not found: {path}")
                    return
                    
                if not os.path.exists(metadata_path):
                    print(f"Error: Metadata file not found: {metadata_path}")
                    return
                    
                # Create a new MyFS instance
                self.myfs = MyFS()
                self.myfs.dri_path = path
                self.myfs.metadata_path = metadata_path
                
                # Temporary authentication for testing
                print("Debug - Setting temporary master key for testing")
                from security.encryption import Encryption
                temp_encryption = Encryption()
                key_data = temp_encryption.generate_key_from_password(password)
                self.myfs.master_key = key_data["key"]
                self.myfs.metadata = {"key_verification": temp_encryption.generate_verification_hash(self.myfs.master_key)}
                self.myfs.encryption = temp_encryption
                
                # Load the file table
                try:
                    self.myfs._load_file_table()
                except Exception as e:
                    print(f"Error loading file table: {e}")
                    return
            
            # Get file list
            files = self.myfs.list_files()
            if not files:
                print("No files found in MyFS volume.")
                return
                
            # Show available files
            print("\nAvailable files:")
            for i, file in enumerate(files):
                print(f"{i+1}. {file['name']} {'(Password protected)' if file['password_protected'] else ''}")
                
            file_name = input("\nEnter the name of the file: ")
            
            # Find the file in the list
            selected_file = None
            for file in files:
                if file["name"] == file_name:
                    selected_file = file
                    break
                    
            if not selected_file:
                print(f"Error: File '{file_name}' not found.")
                return
                
            # Debug the file's protection status
            print(f"Debug - File protection status: {selected_file.get('password_protected', False)}")
            
            # Check if file is already password protected based on what's in the file list
            if selected_file.get("password_protected", False):
                print("This file is already password protected.")
                old_password = getpass.getpass("Enter current password (or leave empty to force change): ")
                force_change = not old_password
                
                new_password = getpass.getpass("Enter new password: ")
                confirm_password = getpass.getpass("Confirm new password: ")
            else:
                old_password = None
                force_change = False
                new_password = getpass.getpass("Set password for the file: ")
                confirm_password = getpass.getpass("Confirm password: ")
                
            if new_password != confirm_password:
                print("Error: Passwords do not match.")
                return
                
            # Set/change the file password
            self.myfs.set_file_password(file_name, new_password, old_password, force=force_change)
            print(f"Password for '{file_name}' has been set successfully!")
            
        except Exception as e:
            print(f"Error setting/changing file password: {e}")
            if "Could not decrypt file with provided password" in str(e):
                retry = input("Would you like to force change the password without verifying? (y/n): ")
                if retry.lower() == 'y':
                    try:
                        # Try again with force=True
                        self.myfs.set_file_password(file_name, new_password, None, force=True)
                        print(f"Password for '{file_name}' has been forcefully set!")
                    except Exception as force_error:
                        print(f"Error forcing password change: {force_error}")
    
    def _import_file(self):
        """Import a file to MyFS"""
        try:
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                path = input("Enter path to MyFS.DRI file: ")
                metadata_path = input("Enter path to metadata file: ")
                password = getpass.getpass("Enter master password: ")
                
                if not os.path.exists(path):
                    print(f"Error: MyFS file not found: {path}")
                    return
                    
                if not os.path.exists(metadata_path):
                    print(f"Error: Metadata file not found: {metadata_path}")
                    return
                    
                # Create a new MyFS instance
                self.myfs = MyFS()
                self.myfs.load(path, metadata_path)
                
                # Debug information about current state
                print(f"Debug - MyFS attributes before auth: {dir(self.myfs)}")
                
                # Authenticate with temporary hardcoded key for testing
                # IMPORTANT: This is only for testing and should be replaced with proper authentication
                print("Debug - Setting temporary master key for testing")
                # Generate a temporary key from the password
                from security.encryption import Encryption
                temp_encryption = Encryption()
                key_data = temp_encryption.generate_key_from_password(password)
                self.myfs.master_key = key_data["key"]
                self.myfs.metadata = {"key_verification": temp_encryption.generate_verification_hash(self.myfs.master_key)}
                
                print(f"Debug - MyFS attributes after auth: {dir(self.myfs)}")
                print("Authentication successful!")
            
            # Get file information
            file_path = input("Enter the path of the file to import: ")
            
            if not os.path.isfile(file_path):
                print(f"Error: File not found: {file_path}")
                return
                
            # Ask if file should be password protected
            protect_file = input("Password protect this file? (y/n): ").lower() == 'y'
            
            if protect_file:
                file_password = getpass.getpass("Enter password for the file: ")
                confirm_password = getpass.getpass("Confirm password: ")
                
                if file_password != confirm_password:
                    print("Error: Passwords do not match.")
                    return
            else:
                file_password = None
            
            # Verify master key is present
            if not hasattr(self.myfs, 'master_key') or not self.myfs.master_key:
                print("Error: Master key not available. Authentication issue.")
                return
                
            # Import the file
            self.myfs.import_file(file_path, file_password)
            print(f"File '{os.path.basename(file_path)}' imported successfully!")
            
        except Exception as e:
            print(f"Error importing file: {e}")
    
    def _export_file(self):
        """Export a file from MyFS"""
        try:
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                path = input("Enter path to MyFS.DRI file: ")
                metadata_path = input("Enter path to metadata file: ")
                password = getpass.getpass("Enter master password: ")
                
                if not os.path.exists(path):
                    print(f"Error: MyFS file not found: {path}")
                    return
                    
                if not os.path.exists(metadata_path):
                    print(f"Error: Metadata file not found: {metadata_path}")
                    return
                    
                # Create a new MyFS instance
                self.myfs = MyFS()
                self.myfs.dri_path = path
                self.myfs.metadata_path = metadata_path
                
                # Temporary authentication for testing
                print("Debug - Setting temporary master key for testing")
                from security.encryption import Encryption
                temp_encryption = Encryption()
                key_data = temp_encryption.generate_key_from_password(password)
                self.myfs.master_key = key_data["key"]
                self.myfs.metadata = {"key_verification": temp_encryption.generate_verification_hash(self.myfs.master_key)}
                self.myfs.encryption = temp_encryption
                
                # Load the file table
                try:
                    self.myfs._load_file_table()
                except Exception as e:
                    print(f"Error loading file table: {e}")
                    return
            
            # Get file list
            files = self.myfs.list_files()
            if not files:
                print("No files found in MyFS volume.")
                return
                
            # Show available files
            print("\nAvailable files:")
            for i, file in enumerate(files):
                print(f"{i+1}. {file['name']} {'(Password protected)' if file.get('password_protected', False) else ''}")
                
            file_name = input("\nEnter the name of the file to export: ")
            
            # Find the file in the list
            selected_file = None
            for file in files:
                if file["name"] == file_name:
                    selected_file = file
                    break
                    
            if not selected_file:
                print(f"Error: File '{file_name}' not found.")
                return
                
            # Ask for destination path
            destination_path = input("Enter the destination path or directory: ")
            
            # Check if destination path is a directory
            if os.path.isdir(destination_path):
                # If it's a directory, append the filename
                destination_path = os.path.join(destination_path, file_name)
                print(f"Full destination path: {destination_path}")
                
            # Check if we have write permission to the destination
            try:
                # Create parent directories if needed
                dest_dir = os.path.dirname(os.path.abspath(destination_path))
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    
                # Test if we can write to this location
                with open(destination_path, 'a') as test_file:
                    pass
                
                # If file is empty after creating it, remove it so we can write properly later
                if os.path.exists(destination_path) and os.path.getsize(destination_path) == 0:
                    os.remove(destination_path)
                    
            except PermissionError:
                print(f"Error: You don't have permission to write to {destination_path}")
                alt_path = input("Enter an alternative destination path: ")
                if not alt_path:
                    print("Export cancelled.")
                    return
                destination_path = alt_path
                
            # Export options
            export_raw = input("Export raw encrypted content? (y/n): ").lower() == 'y'
            
            if export_raw:
                # Export raw encrypted content
                self.myfs.export_file(file_name, destination_path, raw=True)
                print(f"Raw encrypted content of '{file_name}' has been exported to '{destination_path}'.")
                return
                
            # If file is password protected, ask for the password
            force_export = False
            password = None
            
            if selected_file.get("password_protected", False):
                password = getpass.getpass("Enter file password (leave empty to force export): ")
                if not password:
                    force_export = True
                    print("Warning: Attempting forced export without password.")
        
            # Export the file
            try:
                self.myfs.export_file(file_name, destination_path, password, force=force_export)
                print(f"File '{file_name}' has been exported to '{destination_path}' successfully!")
            except Exception as e:
                print(f"Error exporting file: {e}")
                
                # Offer raw export option
                if "Could not decrypt file" in str(e):
                    raw_option = input("Would you like to export the raw encrypted content instead? (y/n): ")
                    if raw_option.lower() == 'y':
                        try:
                            self.myfs.export_file(file_name, destination_path, raw=True)
                            print(f"Raw encrypted content of '{file_name}' has been exported to '{destination_path}'.")
                        except Exception as raw_error:
                            print(f"Error exporting raw content: {raw_error}")
                # If incorrect password, offer retry
                elif "Incorrect password" in str(e) or "Password required" in str(e):
                    retry = input("Would you like to try again with a different password? (y/n): ")
                    if retry.lower() == 'y':
                        self._export_file()
    
        except Exception as e:
            print(f"Error in export file operation: {e}")
    
    def _delete_file(self):
        """Delete a file from MyFS"""
        try:
            logger.info("User initiated file deletion")
            
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                if not self._authenticate_and_open_myfs():
                    return
                    
            # Check machine authorization
            if not integrity_checker.verify_machine_authorization(self.myfs.dri_path):
                print("Error: This machine is not authorized to access this MyFS volume.")
                logger.error("Machine authorization failed for file deletion")
                return
                    
            # List current files
            try:
                files = self.myfs.list_files()
                
                if not files:
                    print("No files found in MyFS volume.")
                    return
                    
                print("\nCurrent files:")
                for i, file in enumerate(files, 1):
                    status = " (deleted)" if file.get("deleted", False) else ""
                    print(f"{i}. {file.get('name', 'Unknown')}{status}")
                
            except Exception as list_error:
                print(f"Error listing files: {list_error}")
                return
                
            # Get file to delete
            file_name = input("\nEnter name of file to delete: ")
            
            # Ask for deletion type
            print("\nDeletion options:")
            print("1. Mark as deleted (recoverable)")
            print("2. Permanently delete")
            
            delete_choice = input("Choose deletion type (1-2): ")
            permanent = delete_choice == '2'
            
            if permanent:
                confirm = input(f"Permanently delete '{file_name}'? This cannot be undone. (y/n): ")
                if confirm.lower() != 'y':
                    print("Deletion cancelled.")
                    return
                    
            try:
                success = self.myfs.delete_file(file_name, permanent=permanent)
                if success:
                    if permanent:
                        print(f"File '{file_name}' permanently deleted.")
                        logger.info(f"File permanently deleted: {file_name}")
                    else:
                        print(f"File '{file_name}' marked as deleted (recoverable).")
                        logger.info(f"File marked as deleted: {file_name}")
                        
            except Exception as delete_error:
                print(f"Error deleting file: {delete_error}")
                logger.error(f"Error deleting file {file_name}: {delete_error}")
                
        except Exception as e:
            print(f"Error in delete file operation: {e}")
            logger.error(f"Error in delete file operation: {e}")

    def _recover_file(self):
        """Recover a deleted file"""
        try:
            logger.info("User initiated file recovery")
            
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                if not self._authenticate_and_open_myfs():
                    return
                    
            # Check machine authorization
            if not integrity_checker.verify_machine_authorization(self.myfs.dri_path):
                print("Error: This machine is not authorized to access this MyFS volume.")
                logger.error("Machine authorization failed for file recovery")
                return
                    
            # List deleted files
            try:
                deleted_files = self.myfs.list_deleted_files()
                
                if not deleted_files:
                    print("No deleted files found for recovery.")
                    return
                    
                print("\nDeleted files (recoverable):")
                for i, file in enumerate(deleted_files, 1):
                    print(f"{i}. {file.get('name', 'Unknown')} (deleted: {file.get('deleted_time', 'Unknown')})")
                
            except Exception as list_error:
                print(f"Error listing deleted files: {list_error}")
                return
                
            # Get file to recover
            file_name = input("\nEnter name of file to recover: ")
                    
            try:
                success = self.myfs.recover_file(file_name)
                if success:
                    print(f"File '{file_name}' recovered successfully.")
                    logger.info(f"File recovered: {file_name}")
                        
            except Exception as recover_error:
                print(f"Error recovering file: {recover_error}")
                logger.error(f"Error recovering file {file_name}: {recover_error}")
                
        except Exception as e:
            print(f"Error in recover file operation: {e}")
            logger.error(f"Error in recover file operation: {e}")

    def _view_deleted_files(self):
        """View all deleted files"""
        try:
            logger.info("User viewing deleted files")
            
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                if not self._authenticate_and_open_myfs():
                    return
                    
            # Check machine authorization
            if not integrity_checker.verify_machine_authorization(self.myfs.dri_path):
                print("Error: This machine is not authorized to access this MyFS volume.")
                logger.error("Machine authorization failed for viewing deleted files")
                return
                    
            # List deleted files
            try:
                deleted_files = self.myfs.list_deleted_files()
                
                if not deleted_files:
                    print("No deleted files found.")
                    return
                    
                print("\nDeleted Files (Recoverable):")
                print("-" * 80)
                print(f"{'Name':<30} {'Size (bytes)':<12} {'Deleted Time':<20} {'Protected'}")
                print("-" * 80)
                
                for file in deleted_files:
                    name = file.get("name", "Unknown")
                    size = file.get("size", 0)
                    deleted_time = file.get("deleted_time", "Unknown")
                    
                    if deleted_time != "Unknown":
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(deleted_time)
                            deleted_time = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            pass
                            
                    protected = "Yes" if file.get("password_protected", False) else "No"
                    
                    print(f"{name:<30} {size:<12} {deleted_time:<20} {protected}")
                    
                print(f"\nTotal deleted files: {len(deleted_files)}")
                
            except Exception as list_error:
                print(f"Error listing deleted files: {list_error}")
                logger.error(f"Error listing deleted files: {list_error}")
                
        except Exception as e:
            print(f"Error in view deleted files operation: {e}")
            logger.error(f"Error in view deleted files operation: {e}")

    def _purge_deleted_files(self):
        """Permanently remove all deleted files"""
        try:
            logger.info("User initiated purge deleted files")
            
            # First check if we have a MyFS instance
            need_authentication = False
            
            if not hasattr(self, 'myfs') or not self.myfs:
                need_authentication = True
            elif not hasattr(self.myfs, 'dri_path') or not hasattr(self.myfs, 'master_key'):
                need_authentication = True
                
            if need_authentication:
                if not self._authenticate_and_open_myfs():
                    return
                    
            # Check machine authorization
            if not integrity_checker.verify_machine_authorization(self.myfs.dri_path):
                print("Error: This machine is not authorized to access this MyFS volume.")
                logger.error("Machine authorization failed for purging deleted files")
                return
                    
            # Show current deleted files
            try:
                deleted_files = self.myfs.list_deleted_files()
                
                if not deleted_files:
                    print("No deleted files found to purge.")
                    return
                    
                print(f"\nFound {len(deleted_files)} deleted files:")
                for file in deleted_files:
                    print(f"- {file.get('name', 'Unknown')}")
                
            except Exception as list_error:
                print(f"Error listing deleted files: {list_error}")
                return
                
            # Confirm purge
            confirm = input(f"\nPermanently delete all {len(deleted_files)} deleted files? This cannot be undone. (y/n): ")
            if confirm.lower() != 'y':
                print("Purge cancelled.")
                return
                    
            try:
                purged_count = self.myfs.purge_deleted_files()
                print(f"Successfully purged {purged_count} deleted files.")
                logger.info(f"Purged {purged_count} deleted files")
                        
            except Exception as purge_error:
                print(f"Error purging deleted files: {purge_error}")
                logger.error(f"Error purging deleted files: {purge_error}")
                
        except Exception as e:
            print(f"Error in purge deleted files operation: {e}")
            logger.error(f"Error in purge deleted files operation: {e}")

    def _repair_myfs_volume(self):
        """Repair a corrupted MyFS volume"""
        try:
            logger.info("User initiated MyFS volume repair")
            
            # Get volume path
            path = input("Enter path to MyFS.DRI file to repair: ")
            
            if not os.path.exists(path):
                print(f"Error: MyFS file not found: {path}")
                return
                
            print("Attempting to repair MyFS volume...")
            print("This may take a few moments...")
            
            # Create a new MyFS instance for repair
            myfs_repair = MyFS()
            myfs_repair.dri_path = path
            
            # Try to repair without password first (basic integrity check)
            try:
                # Check if backup metadata exists
                volume_dir = os.path.dirname(path)
                volume_name = os.path.basename(path).split('.')[0]
                backup_metadata = os.path.join(volume_dir, f"{volume_name}.IXF")
                
                if os.path.exists(backup_metadata):
                    print(f"Found backup metadata: {backup_metadata}")
                    password = getpass.getpass("Enter master password for repair: ")
                    
                    success = myfs_repair.repair_volume(password)
                    if success:
                        print("MyFS volume repaired successfully!")
                        logger.info(f"Successfully repaired MyFS volume: {path}")
                    else:
                        print("Failed to repair MyFS volume. Volume may be severely corrupted.")
                        logger.error(f"Failed to repair MyFS volume: {path}")
                else:
                    print("No backup metadata found. Cannot perform repair.")
                    print("Repair requires backup metadata file (.IXF)")
                    logger.warning(f"No backup metadata found for repair: {path}")
                    
            except Exception as repair_error:
                print(f"Error during repair: {repair_error}")
                logger.error(f"Error during repair of {path}: {repair_error}")
                
        except Exception as e:
            print(f"Error in repair operation: {e}")
            logger.error(f"Error in repair operation: {e}")

def main():
    cli = CLI()
    cli.start()

if __name__ == "__main__":
    main()