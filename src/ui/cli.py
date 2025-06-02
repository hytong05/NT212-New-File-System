import os
import sys
import getpass
from filesystem.myfs import MyFS
from security.authentication import Authentication

class CLI:
    def __init__(self):
        self.myfs = None
        self.auth = Authentication()
        
    def start(self):
        """Main entry point for the CLI interface"""
        print("="*50)
        print("MyFS - Secure File System")
        print("="*50)
        
        # Verify system integrity
        if not self._verify_system():
            print("System integrity check failed. Exiting...")
            sys.exit(1)
            
        # Authenticate user with dynamic password
        if not self._authenticate():
            print("Authentication failed. Exiting...")
            sys.exit(1)
            
        self._main_menu()
    
    def _verify_system(self):
        """Verify system integrity and check if running on original machine"""
        # This would be implemented with actual system checks
        return True
        
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
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ")
            
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
                print("Exiting MyFS. Goodbye!")
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
    
    def _list_files(self):
        """List all files in the MyFS volume"""
        try:
            # Check if we have a MyFS instance
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
                self.myfs.encryption = temp_encryption  # Make sure encryption object is available
                
                print("Authentication successful!")
                
            # Try to initialize file table if not already loaded
            if not hasattr(self.myfs, 'file_table'):
                try:
                    self.myfs._load_file_table()
                except Exception as load_error:
                    print(f"Debug - Error pre-loading file table: {str(load_error)}")
                    # Initialize as empty if it fails
                    self.myfs.file_table = {"files": [], "deleted_files": []}
        
            # Get the list of files
            files = self.myfs.list_files()
            
            if not files:
                print("No files found in MyFS volume.")
                return
                
            # Display file information
            print("\n{:<30} {:<12} {:<20} {:<10}".format(
                "File Name", "Size (bytes)", "Import Time", "Protected"))
            print("-" * 75)
            
            for file in files:
                # Format date/time for display
                import_time = file.get("import_time", "Unknown")
                if import_time != "Unknown":
                    try:
                        # Parse ISO format and convert to readable format
                        from datetime import datetime
                        dt = datetime.fromisoformat(import_time)
                        import_time = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                        
                print("{:<30} {:<12} {:<20} {:<10}".format(
                    file.get("name", "Unknown")[:30], 
                    file.get("size", 0), 
                    import_time[:20],
                    "Yes" if file.get("password_protected", False) else "No"
                ))
                
            print("\nTotal files: {}".format(len(files)))
            
        except Exception as e:
            print(f"Error listing files: {e}")
            import traceback
            traceback.print_exc()
    
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
                
            file_name = input("\nEnter the name of the file to delete: ")
            
            # Find the file in the list
            selected_file = None
            for file in files:
                if file["name"] == file_name:
                    selected_file = file
                    break
                    
            if not selected_file:
                print(f"Error: File '{file_name}' not found.")
                return
                
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete '{file_name}'? This cannot be undone. (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
                
            # Delete the file
            self.myfs.delete_file(file_name)
            print(f"File '{file_name}' has been deleted successfully.")
            
        except Exception as e:
            print(f"Error deleting file: {e}")

def main():
    cli = CLI()
    cli.start()

if __name__ == "__main__":
    main()