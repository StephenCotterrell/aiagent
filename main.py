import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("The GEMINI_API_KEY could not be loaded.")

client = genai.Client(api_key=api_key)


def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ],
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    loop_count = 0

    while True:
        loop_count += 1
        if loop_count > 10:
            raise RuntimeError("Max tool-call iterations reached.")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if response.function_calls is None and response.text is not None:
                print(f"Final response: {response.text}")
                if args.verbose:
                    print(f"User prompt: {args.user_prompt}")
                    print(
                        f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                    )
                    print(
                        f"Response tokens: {response.usage_metadata.candidates_token_count}"
                    )
                return

            if response.candidates:
                for candidate in response.candidates:
                    content = candidate.content
                    if content:
                        messages.append(content)

            if response.usage_metadata is None:
                raise RuntimeError(
                    "Response did not contain usage metadata, failed API request."
                )

            function_calls = response.function_calls

            if function_calls:
                results_list = []
                for function_call_part in function_calls:
                    function_call_result = call_function(
                        function_call_part, verbose=args.verbose
                    )
                    parts = function_call_result.parts
                    if not parts:
                        raise Exception("Fatal error: Function call returned no parts.")
                    parts0 = parts[0]
                    fnr = parts0.function_response
                    if fnr is None or fnr.response is None:
                        raise Exception("Fatal error: Unable to call function")
                    results_list.append(parts0)
                    if args.verbose:
                        print(f"-> {fnr.response}")
                messages.append(
                    types.Content(
                        role="user", parts=[types.Part(text=str(results_list))]
                    )
                )

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
