import os

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    
    path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file is outside the working directory
    if not path_abs.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file exists
    if not os.path.isfile(path_abs):
        return f'Error: "{file_path}" is not a file'
    
    MAX_CHARS = 10000
    try:
        with open(path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"
    if len(file_content_string) == 10000:
        file_content_string += f"[...File \"{file_path}\" truncated at 10000 characters]"
    return file_content_string