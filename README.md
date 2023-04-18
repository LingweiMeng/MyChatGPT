# MyChatGPT
A causual homemade ChatGPT python script that can run using terminal (as long as you have an API).

Just run the code and type something.

## How To Use:
### 1. Prepare an API

Azure API: https://azure.microsoft.com/en-us/products/cognitive-services/openai-service

OpenAI API: https://platform.openai.com/account/api-keys

### 2. Input you API Key

Replace the `INPUT_YOUR_API_KEY` in `mychatgpt.py` with you API Key;

If you are using Azure API, replace `INPUT_YOUR_ENDPOINT_URL` and `INPUT_YOUR_MODEL_NAME` with yours.

### 3. (optional) Edit your `.bashrc` or `.zshrc`

Edit your `.bashrc` or `.zshrc`, add this line to the bottom:

`alias mychatgpt='python3 /PATH_TO_MYCHATGPT/mychatgpt.py'`

Remember to replace `PATH_TO_MYCHATGPT` to the real path.

### 4. Run

Open terminal, and run:

`python3 /PATH_TO_MYCHATGPT/mychatgpt.py`

Remember to replace `PATH_TO_MYCHATGPT` to the real path.

If you performed step 3, just run `mychatgpt`

### 5. Some command:

Input "help", you will see:

```
----------------------------------------
HELP:
exit: exit the conversation.
clear: clear the conversation history.
history: show the conversation history.
back: back to the previous conversation.
load [file_name]: load the conversation history from a file.
save [file_name]: save the conversation history to a file.
help: show the help message.
----------------------------------------
```
