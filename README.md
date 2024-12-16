# Code-Validating-Multi-Agent-LLMs

This project demonstrates the integration of Large Language Models (LLMs) with a multi-agent system to collaboratively generate and validate code. By leveraging the [AutoGen](https://github.com/microsoft/autogen) framework, this system showcases how agents can interact to fulfill user requests in real-time, ensuring accurate and functional code output.

## Overview
The system employs two primary agents:

- **AssistantAgent**: An LLM tasked with generating code based on user input and performing code reviews when needed.
- **UserProxyAgent**: Acts as a user proxy by executing the generated code to verify its correctness.

The agents communicate through a dialogue system, exchanging information to collaboratively solve tasks, ensuring high-quality results.

## Features
- **Code Generation**: Generates Python code for specific functionalities based on user input.
- **Code Validation**: Automatically tests the generated code to ensure correctness and functionality.
- **Interactive Interface**: Provides a user-friendly interface built with [Gradio](https://gradio.app/) for real-time interaction with the agents.
- **Secure Execution**: Implements safeguards (e.g., optional Docker support) for secure code execution.
- **Local Storage**: Saves the generated and validated code inside a local folder named `coding` for future reference.

## Project Pipeline
1. **User Request**: The user submits a request to generate code for a specific task.
2. **Agent Interaction**: 
   - **AssistantAgent** generates the code.
   - **UserProxyAgent** executes the code and validates its correctness.
3. **Output Delivery**: The system provides the generated code, execution results, and conversation history.
4. **Code Storage**: The generated and validated code is saved in the `coding` folder on the local system.

## File Structure
```
multiagent_llms/
├── agent.py           # Defines the agents and their configurations
├── app.py             # Runs the Gradio interface
├── chat.py            # Manages the dialogue between agents
├── utils.py           # Utility functions for threading and other operations
├── OAI_CONFIG_LIST.json  # Configuration file for LLM API keys
├── requirements.txt   # Lists the required dependencies
├── coding/            # Folder to store generated and validated code
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-agent-llms.git
   cd multi-agent-llms
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `OAI_CONFIG_LIST.json` file with your LLM API keys:
   ```json
   [
       {
           "model": "gpt-3.5-turbo",
           "api_key": "YOUR_API_KEY"
       }
   ]
   ```

4. (Optional) Configure Docker for secure code execution if needed.

## Usage
Run the application:
```bash
python app.py
```
Access the interactive interface at `http://localhost:7868` to submit requests and view results.

## Examples
### Example Request
```
Write a Python function to calculate the factorial of a number.
```
### Example Output
Generated Code:
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```
Execution Result:
```
Input: 5
Output: 120
```
The generated code is saved in the `coding` folder for future use.

## Demo Video

<video width="100%" controls>
  <source src="demo/Demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request to improve the project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
