# import os
# from autogen import OpenAIWrapper
# from agents import initialize_agents, config_list
# from utils import *

# assistant, userproxy = initialize_agents()

# def chat_to_oai_message(chat_history):
#     """Convert chat history to OpenAI message format."""
#     messages = []
#     if LOG_LEVEL == "DEBUG":
#         print(f"chat_to_oai_message: {chat_history}")
#     for msg in chat_history:
#         messages.append(
#             {
#                 "content": msg[0].split()[0] if msg[0].startswith("exitcode") else msg[0],
#                 "role": "user",
#             }
#         )
#         messages.append({"content": msg[1], "role": "assistant"})
#     return messages

# def oai_message_to_chat(oai_messages, sender):
#     """Convert OpenAI message format to chat history."""
#     chat_history = []
#     messages = oai_messages[sender]
#     if LOG_LEVEL == "DEBUG":
#         print(f"oai_message_to_chat: {messages}")
#     for i in range(0, len(messages), 2):
#         chat_history.append(
#             [
#                 messages[i]["content"],
#                 messages[i + 1]["content"] if i + 1 < len(messages) else "",
#             ]
#         )
#     return chat_history

# def initiate_chat(config_list, user_message, chat_history):
#     if LOG_LEVEL == "DEBUG":
#         print(f"chat_history_init: {chat_history}")

#     if len(config_list[0].get("api_key", "")) < 2:
#         chat_history.append(
#             [
#                 user_message,
#             ]
#         )
#         return chat_history
#     else:
#         llm_config = {
#             "timeout": TIMEOUT,
#             "config_list": config_list,
#         }
#         assistant.llm_config.update(llm_config)
#         assistant.client = OpenAIWrapper(**assistant.llm_config)

#     if user_message.strip().lower().startswith("show file:"):
#         filename = user_message.strip().lower().replace("show file:", "").strip()
#         filepath = os.path.join("coding", filename)
#         if os.path.exists(filepath):
#             chat_history.append([user_message, (filepath,)])
#         else:
#             chat_history.append([user_message, f"File {filename} not found."])
#         return chat_history

#     assistant.reset()
#     oai_messages = chat_to_oai_message(chat_history)
#     assistant._oai_system_message_origin = assistant._oai_system_message.copy()
#     assistant._oai_system_message += oai_messages

#     try:
#         userproxy.initiate_chat(assistant, message=user_message)
#         messages = userproxy.chat_messages
#         chat_history += oai_message_to_chat(messages, assistant)
#     except Exception as e:
#         chat_history.append([user_message, str(e)])

#     assistant._oai_system_message = assistant._oai_system_message_origin.copy()
#     if LOG_LEVEL == "DEBUG":
#         print(f"chat_history: {chat_history}")
#     return chat_history


# def chatbot_reply_thread(input_text, chat_history, config_list):
#     """Chat with the agent through terminal."""
#     thread = thread_with_trace(target=initiate_chat, args=(config_list, input_text, chat_history))
#     thread.start()
#     try:
#         messages = thread.join(timeout=TIMEOUT)
#         if thread.is_alive():
#             thread.kill()
#             thread.join()
#             messages = [
#                 input_text,
#                 "Timeout Error: Please check your API keys and try again later.",
#             ]
#     except Exception as e:
#         messages = [
#             [
#                 input_text,
#                 str(e) if len(str(e)) > 0 else "Invalid Request to OpenAI, please check your API keys.",
#             ]
#         ]
#     return messages

# def chatbot_reply(input_text, chat_history, config_list):
#     """Chat with the agent through terminal."""
#     return chatbot_reply_thread(input_text, chat_history, config_list)

# # def chat_respond(message, chat_history):
# #     # Get the response from chatbot_reply
# #     updated_history = chatbot_reply(message, chat_history, config_list)
    
# #     # Ensure the chat history is properly formatted
# #     chat_history[:] = [
# #         {"role": "user", "content": msg[0]} if idx % 2 == 0 else {"role": "assistant", "content": msg[1]}
# #         for idx, msg in enumerate(updated_history)
# #         if isinstance(msg, list) and len(msg) == 2
# #     ]
    
# #     if LOG_LEVEL == "DEBUG":
# #         print(f"return chat_history: {chat_history}")
# #     print("Original chat_history: ", chat_history)
# #     # Return an empty string for the Gradio text input to reset
# #     return ""

# def chat_respond(message, chat_history):
#     # Simulate valid bot responses
#     if "python" in message.lower():
#         return "Here is your Python function: ..."
#     elif message.strip() == "":
#         return ""  # Simulate an empty response
#     else:
#         return "I didn't understand your question. Can you rephrase it?"



import os
import re
from autogen import OpenAIWrapper
from agents import initialize_agents, config_list
from utils import *

assistant, userproxy = initialize_agents()

def sanitize_response(response):
    """Sanitize the bot response: remove code blocks and flatten multi-lines."""
    response = re.sub(r"```[a-zA-Z]*\n", "", response)  # Remove code block markers
    response = response.replace("```", "")  # Remove remaining backticks
    response = response.replace("\n", " ").strip()  # Replace newlines with spaces
    return response

def chat_to_oai_message(chat_history):
    """Convert chat history to OpenAI message format."""
    messages = []
    for msg in chat_history:
        messages.append({"content": msg[0], "role": "user"})
        messages.append({"content": msg[1], "role": "assistant"})
    return messages

def oai_message_to_chat(oai_messages, sender):
    """Convert OpenAI message format to chat history."""
    chat_history = []
    messages = oai_messages[sender]
    for i in range(0, len(messages), 2):
        chat_history.append([
            messages[i]["content"],
            messages[i + 1]["content"] if i + 1 < len(messages) else "",
        ])
    return chat_history

def initiate_chat(config_list, user_message, chat_history):
    """Chat with OpenAI agent."""
    if len(config_list[0].get("api_key", "")) < 2:
        chat_history.append([user_message, "API key is missing."])
        return chat_history

    llm_config = {"timeout": TIMEOUT, "config_list": config_list}
    assistant.llm_config.update(llm_config)
    assistant.client = OpenAIWrapper(**assistant.llm_config)

    assistant.reset()
    oai_messages = chat_to_oai_message(chat_history)
    assistant._oai_system_message_origin = assistant._oai_system_message.copy()
    assistant._oai_system_message += oai_messages

    try:
        userproxy.initiate_chat(assistant, message=user_message)
        messages = userproxy.chat_messages
        chat_history += oai_message_to_chat(messages, assistant)
    except Exception as e:
        chat_history.append([user_message, str(e)])

    assistant._oai_system_message = assistant._oai_system_message_origin.copy()
    return chat_history

def chat_respond(message, chat_history):
    """
    Process user input, handle execution outputs, and maintain consistent chat history.
    """
    try:
        print("Debug - Received message:", message)
        print("Debug - Current history:", chat_history)

        # Process the input message and update history
        updated_history = initiate_chat(config_list, message, chat_history)

        # Clean and sanitize the updated history
        clean_history = []
        for msg in updated_history:
            if isinstance(msg, list) and len(msg) == 2:  # Handle execution results
                user_input = msg[0].strip()
                bot_response = msg[1].strip()

                # Detect execution success or failure
                if "exitcode: 0" in user_input:  # Success
                    clean_history.append({"role": "user", "content": user_input})
                    clean_history.append({"role": "assistant", "content": "✅ Code executed successfully."})
                    clean_history.append({"role": "assistant", "content": bot_response})
                elif "exitcode" in user_input:  # Failure
                    clean_history.append({"role": "user", "content": user_input})
                    clean_history.append({"role": "assistant", "content": "❌ Code execution failed."})
                    clean_history.append({"role": "assistant", "content": bot_response})
                else:  # Normal user-assistant exchange
                    clean_history.append({"role": "user", "content": user_input})
                    clean_history.append({"role": "assistant", "content": bot_response})

            elif isinstance(msg, dict):  # Already clean format
                clean_history.append({"role": msg["role"], "content": msg["content"].strip()})

        print("Debug - Updated history:", clean_history)
        return clean_history

    except Exception as e:
        print("Error in chat_respond:", e)
        chat_history.append({"role": "assistant", "content": "An unexpected error occurred. Please try again."})
        return chat_history
