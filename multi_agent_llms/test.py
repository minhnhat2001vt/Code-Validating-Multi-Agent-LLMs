import gradio as gr

# A simple response function for testing
def chat_respond(message, chat_history):
    print(f"Received message: {message}")
    print(f"Chat history before update: {chat_history}")

    # Mock response logic
    mock_response = {"role": "assistant", "content": "This is a mock response."}
    
    # Debug print to ensure proper format
    print(f"Returning response: {mock_response}")
    
    # Return the last assistant message as a list
    return [mock_response]

# Build the Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], type="messages", elem_id="chatbot", height=600)  # Chatbot UI
    textbox = gr.Textbox(placeholder="Enter your message here...", label="Your Message")  # Text input
    submit = gr.Button("Submit")  # Submit button

    # Function to handle the user input and return a response
    def update_chat(message, history):
        print(f"Textbox input: {message}")
        response = chat_respond(message, history)
        print(f"Response sent to Gradio: {response}")
        return response, ""  # Clear the textbox

    # Link the components
    textbox.submit(update_chat, inputs=[textbox, chatbot], outputs=[chatbot, textbox])  # Submit on Enter
    submit.click(update_chat, inputs=[textbox, chatbot], outputs=[chatbot, textbox])  # Submit on Button Click

# Launch the app
if __name__ == "__main__":
    demo.launch(debug=True)  # Enable debug mode
