# MyChatGPT

A casual and simple homemade ChatGPT Python script that can run using terminal (as long as you have an API).

Just run the code and type something.

**(NOTE: Your input must end with a '#', such as 'How are you? #')**

## How To Use:

### 1. Install `openai`, and download the script

For Linux:
`pip install openai readline`

For MacOS:
`pip install openai; brew install readline`

For Windows:
`pip install openai pyreadline3`

Then, download or copy `mychatgpt.py` in this repository.

### 2. Prepare an API

Azure API: https://azure.microsoft.com/en-us/products/cognitive-services/openai-service

OpenAI API: https://platform.openai.com/account/api-keys

### 3. Input your API Key

Replace the `INPUT_YOUR_API_KEY` in `mychatgpt.py` with your API Key;

If you use Azure API, replace `INPUT_YOUR_ENDPOINT_URL` and `INPUT_YOUR_MODEL_NAME` with yours.

### 4. (Optional) Edit your `.bashrc` or `.zshrc`

Edit your `.bashrc` or `.zshrc` to add this line to the bottom:

`alias mychatgpt='python3 /PATH_TO_MYCHATGPT/mychatgpt.py'`

Remember to replace `PATH_TO_MYCHATGPT` with the real path.

### 5. Run

Open terminal, and run:

```
python3 /PATH_TO_MYCHATGPT/mychatgpt.py
```

Remember to replace `PATH_TO_MYCHATGPT` with the real path.

If you performed step 4, just run `mychatgpt`.

Then use it. 
**(NOTE: Your input must end with a '#', such as 'How are you? #')**

#### Run with commands

Run with additional prompts:
```
mychatgpt --prompt YOUR_PROMPT
```

Run with setting the temperature to 1.1 (the higher the value, the random the text, default 1.0):
```
mychatgpt --temperature 1.1
```

Run and save conversation history on the fly:
```
mychatgpt --save SAVE_PATH
```

Load conversation history and run:
```
mychatgpt --load LOAD_PATH
```

## Some commands

Run `mychatgpt`, and input "help", you will see:

```
----------------------------------------
HELP:
img IMAGE_URL [TEXT]: pass an url or a local path to an image for image understanding. [TEXT] is optional.
back: back to the previous conversation.
history: show the conversation history.
clear: clear the conversation history.
temperature: check and change the temperature.
load FILE_PATH: load the conversation history from a file.
save FILE_PATH: save the conversation history to a file.
help: show the help message.
----------------------------------------
```


