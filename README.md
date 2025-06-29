# AI Agent Development Assistant

## Description
This project is an AI-powered development assistant designed to help users with Python development and file system operations within a secure, sandboxed environment. It leverages the Gemini AI model to understand user prompts and execute various coding and file management tasks. The agent is equipped with specific tool functions that allow it to interact with the file system, read/write files, and run Python scripts, all while maintaining strict security boundaries to prevent unauthorized access.

## Features
*   **Intelligent AI Interaction**: Utilizes the Gemini AI model to interpret natural language requests and determine appropriate actions.
*   **File System Exploration**: Capability to list files and directories to understand project structure.
*   **File Content Management**: Read and write content to files, facilitating code modification and documentation.
*   **Python Code Execution**: Run Python scripts within the sandboxed environment to test and verify code.
*   **Secure Operations**: All file system operations are constrained to the working directory, ensuring a secure and controlled environment.
*   **Interactive Mode**: Engage with the AI agent in a conversational manner for continuous development tasks.
*   **Command-Line Prompting**: Provide initial prompts directly via command-line arguments for specific tasks.

## Project Structure
The project is organized into the following key directories and files:

*   `.` (root directory):
    *   `main.py`: The main script that orchestrates the AI agent, handling conversation flow, AI model interaction, and dispatching tool calls.
    *   `README.md`: This file, providing an overview and instructions for the project.
    *   `tests.py`: Contains tests for the AI agent's capabilities, specifically focusing on `run_python_file` security.
    *   `.env`: Stores environment variables, such as the `GEMINI_API_KEY`.
    *   `requirements.txt`: Lists Python dependencies required for the project.
*   `functions/`: Contains the implementations of the tool functions available to the AI agent:
    *   `get_files_info.py`: Lists files and their metadata.
    *   `get_file_content.py`: Reads the content of specified files.
    *   `run_python.py`: Executes Python scripts.
    *   `write_file_content.py`: Writes content to files securely.
*   `calculator/`: An example Python project that the AI agent can interact with. It includes:
    *   `main.py`: The main script for the calculator application.
    *   `tests.py`: Unit tests for the calculator.
    *   `pkg/`:
        *   `calculator.py`: The core logic for evaluating arithmetic expressions.
        *   `render.py`: Utility for formatting calculator output.

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key**:
    *   Obtain a `GEMINI_API_KEY` from Google AI Studio.
    *   Create a `.env` file in the root directory of the project.
    *   Add your API key to the `.env` file:
        ```
        GEMINI_API_KEY="your_gemini_api_key_here"
        ```

## Usage

You can run the AI agent in two modes:

### Interactive Mode

To start an interactive conversation with the AI agent:

```bash
python main.py
```
Type your prompts at the `>` prompt. Type `/q` to quit the application.

### Command-Line Prompt

To provide an initial prompt directly via the command line:

```bash
python main.py "Your initial prompt here, e.g., list all python files"
```

### Verbose Mode

To see detailed output including function calls and their responses, add the `--verbose` flag:

```bash
python main.py --verbose
# or
python main.py "Your prompt" --verbose
```

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
