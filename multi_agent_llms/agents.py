import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.code_utils import extract_code
import json

TIMEOUT = 60



# Define the path to your JSON configuration file
config_file_path = "./OAI_CONFIG_LIST.json"

# Load the configuration from the JSON file
with open(config_file_path, "r") as file:
    config_list = json.load(file)

# Extract the API key (assuming the first entry contains the key)
API_Key = config_list[0].get("api_key")

# Explicitly set the LLM configurations
llm_configs = {
    "config_list": [
        {
            "timeout": TIMEOUT,
            "model": "gpt-3.5-turbo",
            "temperature": 0.9,
            "api_key": API_Key,
        }
    ]
}

# Debug print to ensure the configuration is correct
print(llm_configs)


def initialize_agents():
    assistant= AssistantAgent(
        name="assistant",
        max_consecutive_auto_reply=5,
        llm_config=llm_configs,
    )

    userproxy = UserProxyAgent(
        name="userproxy",
        human_input_mode="NEVER",
        is_termination_msg=_is_termination_msg,
        max_consecutive_auto_reply=5,
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
    )

    return assistant, userproxy

def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")

        if message is None:
            return False
    cb = extract_code(message)
    contain_code = False

    for c in cb:
        if c[0] == "python":
            contain_code = True
            break

    return not contain_code
