def import_file(file_path, myfs_instance):
    # Import a file into MyFS
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            myfs_instance.add_file(file_path, content)
            print(f"File '{file_path}' imported successfully.")
    except Exception as e:
        print(f"Error importing file: {e}")

def export_file(file_name, export_path, myfs_instance):
    # Export a file from MyFS
    try:
        content = myfs_instance.get_file(file_name)
        with open(export_path, 'wb') as file:
            file.write(content)
            print(f"File '{file_name}' exported successfully to '{export_path}'.")
    except Exception as e:
        print(f"Error exporting file: {e}")

def delete_file(file_name, myfs_instance, permanent=False):
    # Delete a file from MyFS
    try:
        if permanent:
            myfs_instance.delete_file_permanently(file_name)
            print(f"File '{file_name}' deleted permanently.")
        else:
            myfs_instance.delete_file(file_name)
            print(f"File '{file_name}' deleted (can be recovered).")
    except Exception as e:
        print(f"Error deleting file: {e}")

def list_files(myfs_instance):
    # List all files in MyFS
    try:
        files = myfs_instance.list_files()
        print("Files in MyFS:")
        for file in files:
            print(f"- {file}")
    except Exception as e:
        print(f"Error listing files: {e}")