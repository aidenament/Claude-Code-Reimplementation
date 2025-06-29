import os
import subprocess

def run_python_file(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    
    path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file is outside the working directory
    if not path_abs.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # Check if the path exists
    if not os.path.exists(path_abs):
        return f'Error: File "{file_path}" not found'
    
    #if file dooes not end in .py, return error
    if not file_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file'
    
    #use subprocess.run with 30 seconds timeout
    #capture stdout and stderr
    #set working directory to working_directory
    try:
        result = subprocess.run(
            ['python', path_abs],
            capture_output=True,
            timeout=30,
            cwd=working_directory
        )
        
        stdout = f"STDOUT: {result.stdout.strip()}" if result.stdout else 'No STDOUT from script'
        stderr = f"STDERR: {result.stderr.strip()}" if result.stderr else 'No STDERR from script'
        if result.returncode != 0:
            return f"{stdout}\n{stderr}\n Process exited with code {result.returncode}"
        elif result.stdout or result.stderr:
            return f"{stdout}\n{stderr}"
        else:
            return 'No output produced'

    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f'Error: executing Python file: {e}'