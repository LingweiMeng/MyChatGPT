# ref: https://github.com/openai/openai-python
# ref: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
# ref: https://platform.openai.com/docs/guides/vision

from openai import AzureOpenAI, OpenAI
import argparse
import readline
import base64

# Choose Azure API or OpenAI API, comment out another one.
# Azure API
client = AzureOpenAI(
    azure_endpoint="INPUT_YOUR_ENDPOINT_URL",
    api_version="2024-02-01",
    api_key="INPUT_YOUR_API_KEY",
    timeout=120
)
deployment_model = "INPUT_YOUR_MODEL_NAME"

'''
# OpenAI API
client = OpenAI(
    api_key="INPUT_YOUR_API_KEY",
    timeout=120
)
deployment_model = "gpt-4"
'''


# Some casual prompt here.
prompt = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. "
# prompt += "Respond using markdown."

creation_params = {
    "temperature": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
END = "\033[0m"

SYSTEM_COLOR = BLUE
ASSIS_COLOR = YELLOW
USER_COLOR = GREEN
ERROR_COLOR = RED
INFO_COLOR = PURPLE


class MyChatGPT:
    def __init__(self, args):
        self.conversation = []
        self.conversation_init = []
        self.save_on_the_fly = args.save

        self.temperature = args.temperature
        self.frequency_penalty = args.frequency_penalty
        self.presence_penalty = args.presence_penalty

        print(INFO_COLOR + "NOTE: Type 'help' to view help information and some commands." + END)
        print(INFO_COLOR + "      Your input must end with a '#'. \n" + END)

        if args.load is not None:
            self.load_from_file(args.load)
        else:
            self.conversation.append({"role": "system", "content": args.prompt})
            print(SYSTEM_COLOR + "system: \n" + args.prompt + END + "\n")
        self.conversation_init = self.conversation.copy()

    def print_history(self):
        print(f"\n┌{'──────'*10}\n")
        print("HISTORY:")
        for message in self.conversation:
            color = USER_COLOR if message["role"] == "user" \
                else ASSIS_COLOR if message["role"] == "assistant" \
                else SYSTEM_COLOR

            if isinstance(message['content'], list):
                content = ['[img] ' + c['image_url']['url'] if c['type'] == 'image_url' else c['text'] for c in message['content']]
                content = '\n'.join(content)
            else:
                content = message['content']

            print(f"\n{color}{message['role']}:\n{content}{END}")
        print(f"\n└{'──────'*10}\n")

    def load_from_file(self, file_name):
        try:
            with open(file_name, "r") as f:
                lines = f.readlines()
                conversation = []
                role = None
                content = ""
                # load temperature
                if lines[0].split()[0] == "temperature:":
                    self.temperature = float(lines[0].split()[1])
                    lines = lines[2:]
                for line in lines:
                    if line.strip() in ["user:", "assistant:", "system:"]:
                        if role is not None:
                            conversation.append({"role": role, "content": content.strip()})
                            content = ""
                        role = line.strip()[:-1]
                    else:
                        content += line
                if role is not None:
                    conversation.append({"role": role, "content": content.strip()})
                self.conversation = conversation
            self.print_history()
            print(INFO_COLOR + "Current temperature: " + str(self.temperature))
            print("File loaded.\n" + END)
        except FileNotFoundError:
            print(ERROR_COLOR + "File not found.\n" + END)

    def save_to_file(self, file_name, on_the_fly=False):
        try:
            lines = [f"{message['role']}:\n{message['content']}\n\n" for message in self.conversation]
            with open(file_name, "w") as f:
                f.write(f"temperature: {self.temperature}\n\n")
                f.writelines(lines)
            if not on_the_fly:
                print(INFO_COLOR + "Conversation history saved.\n" + END)
        except FileNotFoundError:
            print(ERROR_COLOR + "Error: Conversation history not saved. It may be a path error.\n" + END)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def multiline_input(self, ending_character='#'):
        input_list = []
        # is_cmd = True
        img_urls = []
        while True:
            temp = input()
            is_cmd = True

            if temp in ('back', 'back' + ending_character):
                self.conversation = self.conversation[:-2] if len(self.conversation) > 2 else self.conversation_init
                self.print_history()

            elif temp in ('clear', 'clear' + ending_character):
                self.conversation = self.conversation_init.copy()
                self.print_history()

            elif temp in ('history', 'history' + ending_character):
                self.print_history()

            elif temp in ('temperature', 'temperature' + ending_character):
                print(INFO_COLOR + "Current temperature: " + str(self.temperature) + END)
                print(INFO_COLOR + "Please input a new temperature value: " + END)
                self.temperature = float(input())
                print()

            elif len(temp.split()) == 2 and temp.split()[0] == "load":
                self.load_from_file(temp.split()[1].strip(ending_character))

            elif len(temp.split()) == 2 and temp.split()[0] == "save":
                self.save_to_file(temp.split()[1].strip(ending_character))

            elif temp in ('help', 'help' + ending_character):
                print(INFO_COLOR + "\n" + "----" * 10)
                print("HELP:")
                print("img IMAGE_URL: pass an url or a local path to an image for image understanding.")
                print("back: back to the previous conversation.")
                print("history: show the conversation history.")
                print("clear: clear the conversation history.")
                print("temperature: check and change the temperature.")
                print("load FILE_PATH: load the conversation history from a file.")
                print("save FILE_PATH: save the conversation history to a file.")
                print("help: show the help message.")
                print("----" * 10 + END + "\n")

            else:
                is_cmd = False

            if is_cmd:
                return

            if len(temp.split()) >= 2 and temp.split()[0] == "img":
                _img_url = temp.split()[1].rstrip('#')
                img_url = _img_url.strip("\"").strip("'")
                try:
                    img_url =  img_url if "http" in temp else f"data:image/jpeg;base64,{self.encode_image(f'{img_url}')}"
                except Exception as err:
                    print(ERROR_COLOR + "Error: " + str(err) + END)
                    print(ERROR_COLOR + "Or the path contains spaces. Please re-try.\n" + END)
                    img_url = None
                    continue
                img_urls.append(img_url)
                temp = temp.replace("img " + _img_url, "").lstrip()
                if temp == "":
                    continue

            # if temp == "":
            #     print()
            if temp == ending_character:
                break
            elif temp and temp[-1] == ending_character:
                input_list.append(temp[:-1])
                break
            input_list.append(temp)

        if len(img_urls) == 0:
            return "\n".join(input_list)
        else:
            return [{"type": "text", "text": "\n".join(input_list)}] + [{"type": "image_url", "image_url": {"url": u}} for u in img_urls]

    def run(self):
        while (True):
            print(USER_COLOR + "user: " + END)
            user_input = self.multiline_input()

            if user_input is None:
                continue
            else:
                self.conversation.append({"role": "user", "content": user_input})

            try:
                response = client.chat.completions.create(messages=self.conversation,
                    temperature=self.temperature,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    model = deployment_model
                )
            except Exception as err:
                print(ERROR_COLOR + "Error: " + str(err) + END)
                print(ERROR_COLOR + "Please re-try.\n" + END)
                self.conversation = self.conversation[:-1]
                continue

            self.conversation.append({"role": "assistant", "content": response.choices[0].message.content})
            print("\n" + ASSIS_COLOR + 'assistant: \n' + response.choices[0].message.content + END + "\n")

            if self.save_on_the_fly is not None:
                self.save_to_file(self.save_on_the_fly, on_the_fly=True)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--prompt", type=str, default=None)
    arg_parser.add_argument("--load", type=str, default=None)
    arg_parser.add_argument("--save", type=str, default=None)
    arg_parser.add_argument("--temperature", type=float, default=creation_params["temperature"],
                            help="The higher the value, the random the text.")
    arg_parser.add_argument("--frequency_penalty", type=float, default=creation_params["frequency_penalty"],
                            help="The higher the value, the less repetitive text.")
    arg_parser.add_argument("--presence_penalty", type=float, default=creation_params["presence_penalty"],
                            help="The higher the value, the more likely the model will talk about new topics.")
    # arg_parser.add_argument("--max_tokens", type=int, default=creation_params["max_tokens"],
    #                         help="The maximum number of tokens to generate.")
    # arg_parser.add_argument("--n", type=int, default=1,
    #                         help="How many chat completion choices to generate for each input message.")
    args = arg_parser.parse_args()

    args.prompt = prompt + "\n" + args.prompt if args.prompt is not None else prompt

    mychatgpt = MyChatGPT(args)
    mychatgpt.run()
