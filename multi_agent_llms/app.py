import gradio as gr
from gradio import ChatInterface
from chat import chat_respond

LOG_LEVEL = "INFO"

# Example queries for users to choose from
example_queries = [
    "write a python function to count the sum of two numbers?",
    "Write a python function to count prime numbers appearing in the range from 0 to n, with n entered by the user.",
    "write a simple page, run on local with the word 'Hello' ",
    "Plot a chart of the last year's stock prices of Nvidia and Intel and save to stock_price.png.",
    "show file: stock_price.png",
]

# A wrapper to ensure the chat works with debugging
def debug_chat_respond(message, chat_history):
    try:
        print("Debug - Received message:", message)
        print("Debug - Current history:", chat_history)

        # Call chat_respond and validate the chat history
        updated_chat_history = chat_respond(message, chat_history)
        validated_history = []
        for msg in updated_chat_history:
            if "role" in msg and "content" in msg and isinstance(msg["content"], str):
                validated_history.append(msg)
            else:
                print("Invalid message format:", msg)

        print("Debug - Updated history:", validated_history)
        return validated_history

    except Exception as e:
        print("Error in debug_chat_respond:", e)
        chat_history.append({"role": "assistant", "content": "An unexpected error occurred. Please try again."})
        return chat_history

# Gradio app setup
with gr.Blocks() as demo:
    gr.Markdown("""
        # Microsoft AutoGen
        ## Multi-agent Conversation
    """)

    # Chatbot UI component
    chatbot = gr.Chatbot(
        value=[], 
        type="messages", 
        elem_id="chatbot",
        height=500
    )

    # Textbox for user input
    txt_input = gr.Textbox(
        show_label=False,
        placeholder="Enter your message...",
        container=False,
    )

    # Submit user message to chat
    txt_input.submit(debug_chat_respond, inputs=[txt_input, chatbot], outputs=chatbot)

    # Add the examples
    gr.Examples(
        examples=example_queries,
        inputs=txt_input,
        label="Example Queries",
        examples_per_page=2,  # Adjust the number of visible examples per page
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7868)
