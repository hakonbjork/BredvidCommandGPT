import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = "https://test8322.openai.azure.com/"
OPENAI_API_VERSION = "2023-03-15-preview"

CHAT_ENGINE_ID = "CommandGPT4"
CMD_EXEC_MAX_OUTPUT_LENGTH = 3000
NUM_OF_MESSAGES = 5
DEBUG = True

# Define the regular expression pattern. Search for ${{COMMAND:ARGUMENT}}
CMD_REGEX_PATTERN = r"\$\{\{(.+?):((.|\n|\r\n)+?)\}\}"


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def debug_print(message):
    if DEBUG:
        print(f"{BCOLORS.OKCYAN}{message}{BCOLORS.ENDC}")


def warning_print(message):
    print(f"{BCOLORS.WARNING}{message}{BCOLORS.ENDC}")


def error_print(message):
    print(f"{BCOLORS.FAIL}{message}{BCOLORS.ENDC}")


def chat_print(message):
    print(f"{BCOLORS.OKBLUE}{message}{BCOLORS.ENDC}")


def chat(system_message, content_array):
    try:
        response = openai.ChatCompletion.create(
            engine=CHAT_ENGINE_ID,
            messages=[system_message] + content_array[-NUM_OF_MESSAGES:],
            temperature=1,
            max_tokens=2000,
            top_p=0.95,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_print(f"OpenAI API failed with error: {e}")
        return "OpenAI API failed with error."

def main():
    with open("system_content.txt") as file:
        system_content = (
            file.read()
            .replace("\r", "")
            .replace("\n", "")
            .replace("\t", "")
            .replace("  ", " ")
        )

    system_message = {"role": "system", "content": system_content}

    content_array = []

    print(f"\t\t\n\n{BCOLORS.UNDERLINE}Welcome to CommandGPT!{BCOLORS.ENDC}\n\n")

    while True:
        user_input = input("Talk to CommandGPT: ")

        content_array += [{"role": "user", "content": user_input}]

        assistant_content = chat(system_message, content_array)

        content_array += [{"role": "assistant", "content": assistant_content}]

        chat_print(content_array[-1]["content"] + "\n")


if __name__ == "__main__":
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    openai.api_type = OPENAI_API_TYPE
    openai.api_base = OPENAI_API_BASE
    openai.api_version = OPENAI_API_VERSION
    openai.api_key = OPENAI_API_KEY

    main()
