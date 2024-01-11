import subprocess
import sys
from termcolor import cprint
import shutil
import ast
import json

from modules.gpt import ask_gpt
from modules.paths import relative



def run_script():
    subprocess_args = (
        [sys.executable, relative("modules", "script_runner.py")]
    )

    try:
        result = subprocess.check_output(subprocess_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        print(error)
        return error.output.decode("utf-8"), error.returncode
    return ast.literal_eval(result.decode("utf-8"))


def send_script_to_gpt(input, error_message):
    with open("temp.py", "r") as f:
        file_lines = f.readlines()

    file_with_lines = []
    for i, line in enumerate(file_lines):
        file_with_lines.append(str(i + 1) + ": " + line)
    file_with_lines = "".join(file_with_lines)

    prompt = (
        "Here is the script that needs fixing:\n\n"
        f"{file_with_lines}\n\n"
        "Here is the input it was provided:\n\n"
        f"{input}\n\n"
        "Here is the error message:\n\n"
        f"{error_message}\n"
        "Please provide your suggested changes, and remember to stick to the "
        "exact format as described above."
    )

    return ask_gpt(prompt, temperature=0.5, system="syntax_corrector")


def apply_changes(file_path, changes):

    with open(file_path) as f:
        original_file_lines = f.readlines()
    changes = json.loads(changes)
    print(changes)
    if isinstance(changes, dict):
        explanations = [changes["explanation"]]
        operation_changes = [{k: changes[k] for k in changes.keys() - {'explanation'}}]
    else:
        operation_changes = [change for change in changes if "operation" in change]
        explanations = [
            change["explanation"] for change in changes if "explanation" in change
        ]

    # Sort the changes in reverse line order
    operation_changes.sort(key=lambda x: x["line"], reverse=True)

    file_lines = original_file_lines.copy()
    
    for change in operation_changes:
        operation = change["operation"]
        line = change["line"]
        content = change["content"]

        if operation == "Replace":
            file_lines[line - 1] = content + "\n"
        elif operation == "Delete":
            del file_lines[line - 1]
        elif operation == "InsertAfter":
            file_lines.insert(line, content + "\n")

    with open(file_path, "w") as f:
        f.writelines(file_lines)


def syntax_corrector(script, test_case):
    with open("temp.py", "w") as f:
        f.write(script)
    with open("temp.in", "w") as f:
        f.write(test_case["input"])

    # Make a backup of the original script
    shutil.copy("temp.py", "temp.py.bak")
    while True:
        output, returncode = run_script()
        if returncode == 0:
            break
        else:
            print("sending")
            json_response = send_script_to_gpt(
                input=test_case["input"],
                error_message=output,
            )
            apply_changes("temp.py", json_response)
    with open("temp.py", "r") as f:
        output_script = f.read()
    return output_script