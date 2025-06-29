import os

def get_files_info(working_directory, directory=None):
    
    working_dir_abs = os.path.abspath(working_directory)
    
    if directory is not None:
        directory_abs = os.path.abspath(os.path.join(working_directory, directory))
        
        # Check if the directory is outside the working directory
        if not directory_abs.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the directory exists
        if not os.path.isdir(directory_abs):
            return f'Error: "{directory}" is not a directory'
        
        target_dir = directory_abs
    else:
        target_dir = working_dir_abs
    
    string_of_contents = ''
    contents = os.listdir(target_dir)
    for item in contents:
        info = f"- {item}: "
        item_path = os.path.join(target_dir, item)
        try:
            size = f"file_size={os.path.getsize(item_path)} bytes"
        except Exception as e:
            size = f"Error getting file size: {e}" 
        try:
            is_dir = f"is_dir={os.path.isdir(item_path)}"
        except Exception as e:
            is_dir = f"Error checking if directory: {e}"
        info += f"{size}, {is_dir}\n"
        string_of_contents += info
    return string_of_contents
