import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    
    path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    # Check if the file is outside the working directory
    if not path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    # if file path doesn't exist, create it
    if not os.path.exists(os.path.dirname(path_abs)):
        try:
            os.makedirs(os.path.dirname(path_abs))
        except Exception as e:
            return f"Error creating directory: {e}"

    try:
        with open(path_abs, 'w') as f:
            f.write(content)
    except Exception as e:
        return f"Error writing file: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'