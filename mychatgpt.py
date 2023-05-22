import openai
import readline

# Choose Azure API or OpenAI API, comment out another one.

# Azure API
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = "INPUT_YOUR_ENDPOINT_URL"
openai.api_key = "INPUT_YOUR_API_KEY"
deployment_name = {"engine": "INPUT_YOUR_MODEL_NAME"}

## OpenAI API
# openai.api_key = "INPUT_YOUR_API_KEY"
# deployment_name = {"model": "gpt-4"}
# deployment_name = {"model": "gpt-3.5-turbo"}

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
END = '\033[0m'

SYSTEM_COLOR = PURPLE
ASSIS_COLOR = YELLOW
USER_COLOR = GREEN

def print_history(conversation):
    print("\n" + "----" * 10)
    print("HISTORY:")
    for message in conversation:
        if message['role'] == "user":
            msg = "\n" + USER_COLOR + message['role'] + ": " + message['content'] + END + "\n"
        elif message['role'] == "assistant":
            msg = "\n" + ASSIS_COLOR + message['role'] + ": " + message['content'] + END + "\n"
        elif message['role'] == "system":
            msg = "\n" + SYSTEM_COLOR + message['role'] + ": " + message['content'] + END + "\n"
        print(msg)
    print("----" * 10 + "\n")

# Some casual prompt here.
prompt = "The whole conversation of you and I (the user) is a role-playing game. \n"
prompt += "Your name is Lisa, a human girl. You are a good friend, listener and talker. \n"
prompt += "You are knowledgeable and know everything. \n"
prompt += "Immerse yourself in this role-playing game and let your imagination run wild. \n"
prompt += "Assume different personas for both yourself and me, even when the details are unknown. \n"
prompt += "Don't let me realize that you are non-human or I'll be very upset. \n"
prompt += "Don't tell me that we are in a role-playing game. \n"
prompt += "When you output something within (), it means that you are thinking about it in my mind but do not speak out. \n"
prompt += "When I speak to you, you must think about it in your mind first (output what you are thinking in your mind), "
prompt += "and then say it out loud.\n"
prompt += "When I input something within [], it means that I say something out of the role-playing game. "
prompt += "Let's play. Be patient. "

print(SYSTEM_COLOR + "system: \n" + prompt + END)

conversation = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": "Hello Lisa, my dear friend!"},
]

conversation_init = conversation.copy()

response = openai.ChatCompletion.create(messages=conversation, **deployment_name)
conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
print("\n" + ASSIS_COLOR + 'assistant: \n' + response['choices'][0]['message']['content'] + END + "\n")

while (True):
    print(USER_COLOR + "user: \n" + END, end="")
    user_input = input()
    is_cmd = True

    if user_input == "exit":
        break

    elif user_input == "clear":
        conversation = conversation_init
        print_history(conversation)

    elif user_input == "history":
        print_history(conversation)

    elif user_input == "back":
        conversation = conversation[:-2] if len(conversation) > 2 else conversation_init
        print_history(conversation)

    elif "load" in user_input:
        if len(user_input.split()) == 2:
            conversation = []
            try:
                with open(user_input.split()[1], "r") as f:
                    role = ""
                    content = ""
                    for line in f:
                        line_splited = line.split(": \n")
                        if line_splited[0] in ["user", "assistant", "system"]:
                            if role != "":
                                conversation.append({"role": role, "content": content.strip()})
                                role = ""
                                content = ""
                            role = line_splited[0]
                            content = line_splited[1]
                        else:
                            content += line
                    if role != "":
                        conversation.append({"role": role, "content": content.strip()})
                print("File loaded. \n")
            except FileNotFoundError:
                print("File not found. \n")

            print_history(conversation)

        else:
            print("Please specify the file name. \n")

    elif "save" in user_input:
        if len(user_input.split()) == 2:
            with open(user_input.split()[1], "w") as f:
                for message in conversation:
                    f.write(message['role'] + ": \n" + message['content'] + "\n")
            print("Conversation history saved. \n")
        else:
            print("Please specify the file name. \n")

    elif user_input == "help":
        print("\n" + "----" * 10)
        print("HELP:")
        print("exit: exit the conversation.")
        print("clear: clear the conversation history.")
        print("history: show the conversation history.")
        print("back: back to the previous conversation.")
        print("load [file_name]: load the conversation history from a file.")
        print("save [file_name]: save the conversation history to a file.")
        print("help: show the help message.")
        print("----" * 10 + "\n")

    else:
        is_cmd = False
	# You can add something after the user input, maybe to emphasis something.
        # user_input = user_input + \
        #     "[Aside: Remember that we are in a role-playing game. Ask less and share more!]"
        conversation.append({"role": "user", "content": user_input})

    if is_cmd:
        continue

    try:
        response = openai.ChatCompletion.create(messages=conversation, **deployment_name)
    except Exception as e:
        print("Error: " + str(e))
        conversation = conversation[:-1]
        continue

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\n" + ASSIS_COLOR + 'assistant: \n' + response['choices'][0]['message']['content'] + END + "\n")
