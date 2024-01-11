import json

from modules.syntax import syntax_corrector
from modules.gpt import ask_gpt



def run_pipeline(message):
    print("summary")
    json_summary, explanation = summarize_and_explain(message)
    print('*******************************************')
    print(json_summary)
    print('*******************************************')
    print("code")
    python_script = generate_code(json_summary)
    print('*******************************************')
    print(python_script)
    print('*******************************************')
    print("testcase")
    sample_testcases = ask_gpt(json_summary, system="sample_testcases_prompt")
    sample_testcases = json.loads(sample_testcases)
    print('*******************************************')
    print(sample_testcases)
    print('*******************************************')
    print("corrector")
    corrected_python_script = syntax_corrector(python_script, sample_testcases["testcase_1"])
    print('*******************************************')
    print(corrected_python_script)
    print('*******************************************')
    responses = [corrected_python_script , explanation]
    return responses


def summarize_and_explain(message):
    json_summary = ask_gpt(message, system="summarize_prompt")
    explanation = ask_gpt(message, system="explanation_prompt")
    return json_summary, explanation


def generate_code(json_summary):
    raw_code_response = ask_gpt(json_summary, system="code_generation_prompt", temperature=0.4)
    try:
        raw_code_response = json.loads(raw_code_response)
    except Exception as e:
        return -1
    if type(raw_code_response["code"]) == list:
        temp = ''
        for item in raw_code_response["code"]:
                temp += item + '\n'
        raw_code_response["code"] = temp
    return raw_code_response["code"]



