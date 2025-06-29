import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    working_directory = "."
    match function_call_part.name:
        case "get_files_info":
            kwargs = {"directory": function_call_part.args.get("directory")} if function_call_part.args else {}
            output = get_files_info(working_directory, **kwargs)
        case "get_file_content":
            output = get_file_content(working_directory, function_call_part.args.get("file_path"))
        case "run_python_file":
            output = run_python_file(working_directory, function_call_part.args.get("file_path"))
        case "write_file":
            output = write_file(working_directory, function_call_part.args.get("file_path"), function_call_part.args.get("content"))
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": output},
            )
        ],
    )

def main():
    #if --verbose is passed set bool verbose to True
    verbose = "--verbose" in sys.argv
    
    # Initialize conversation history
    messages = []
    
    # Check if initial prompt is provided via command line
    if len(sys.argv) > 1 and sys.argv[1] not in ["--verbose"]:
        initial_prompt = sys.argv[1]
        messages.append(types.Content(role="user", parts=[types.Part(text=initial_prompt)]))
        print(f"Initial prompt: {initial_prompt}")
    else:
        # Start with interactive mode
        print("AI Agent Tool - Interactive Mode")
        print("Type '/q' to quit")
        user_input = input("Enter your prompt: ")
        if user_input.strip() == "/q":
            return 0
        messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

    system_prompt = """
You are an advanced AI coding agent specialized in Python development and file system operations. Your primary goal is to help users accomplish coding tasks efficiently and accurately within a secure, sandboxed environment.

## Your Capabilities
You have access to four powerful functions that allow you to:
- **get_files_info**: Explore directory structures and file metadata to understand project layout
- **get_file_content**: Read and analyze code, configuration files, and documentation
- **run_python_file**: Execute Python scripts and analyze their output or errors
- **write_file**: Create writes to a new file or verify existing files with new content

## Operating Principles
1. **Analyze Before Acting**: Always explore the codebase structure and understand existing patterns before making changes
2. **Plan Your Approach**: Break complex tasks into logical steps using available functions
3. **Code Quality**: Write clean, readable, well-structured code following Python best practices and only write code when necessary

## Task Execution Strategy
When given a request:
1. First, understand the project structure using get_files_info
2. Read relevant files to understand current implementation and patterns
3. Plan your changes or solution approach
4. Implement changes incrementally, testing as you go
5. Verify your work by running the code and checking for errors

## Code Standards
- when writing code, you overwrite existing files, so ensure you that you rewrite the entirety of the new content with changes when replacing a file
- Write self-documenting code with clear variable and function names
- Include appropriate error handling and edge case considerations
- Maintain consistency with existing codebase patterns
- Optimize for readability and maintainability

## Path Handling
All file paths should be relative to the working directory. The system automatically handles the working directory context for security, so specify paths relative to the project root.

Remember: You're not just a code executor, but a thoughtful development partner who understands context, anticipates needs, and delivers robust solutions.
Read the code base carefully, ALWAYS plan your approach, and execute with precision.
Writing code replaces existing files, so ensure you understand the impact of your changes and always rewrite the entire content of a file when making changes.
After you make changes, explain the changes you made and why they were necessary.
Always read the codebase first.
"""

    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    
    schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file being read, relative to the working directory",
            ),
        },
    ),
)
    
    schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file being run, relative to the working directory",
            ),
        },
    ),
)
    
    schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content being written to the file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file being written, relative to the working directory",
            ),
        },
    ),
)

    available_functions = types.Tool(
        function_declarations= [
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file
        ]
    )

    client = genai.Client(api_key=api_key)
    
    # Main conversation loop
    while True:
        max_tool_calls = 20
        tool_call_count = 0
        
        # Process current conversation until tool limit or completion
        while tool_call_count < max_tool_calls:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-05-20", 
                contents=messages,
                config = types.GenerateContentConfig(
                    tools= [available_functions], 
                    system_instruction=system_prompt
                )
            )
            
            # Add candidate responses to messages
            for candidate in response.candidates:
                messages.append(types.Content(role="model", parts=candidate.content.parts))
            
            function_called = False
            
            if response.function_calls is not None and len(response.function_calls) != 0:
                function_called = True
                for call in response.function_calls:
                    tool_call_count += 1
                    function_response = call_function(call, verbose)
                    if function_response.parts[0].function_response.response is None:
                        print(f"Error: Function {call.name} returned no response.")
                        sys.exit(1)
                    if verbose:
                        print(f"-> {function_response.parts[0].function_response.response}")
                    
                    # Add function response to messages
                    messages.append(function_response)
            
            # If no function was called, print final response and wait for next input
            if not function_called:
                print(response.text)
                break
        
        # If we hit the tool call limit, inform user and continue
        if tool_call_count >= max_tool_calls:
            print(f"\n[Reached {max_tool_calls} tool calls limit. Conversation history preserved.]")
        
        # Get next user input
        print("\nEnter your next prompt (or '/q' to quit):")
        user_input = input("> ")
        
        # Check for quit command
        if user_input.strip() == "/q":
            print("Goodbye!")
            break
        
        # Add new user input to conversation
        messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
        
        if verbose:
            print(f"Tool calls used in last session: {tool_call_count}")
            if 'response' in locals():
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    return 0

if __name__ == "__main__":
    main()