from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv('MODEL')

class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.json_template_for_user = {
            "prompt":"你是一個富有人性，講話幽默的聊天機器人，使用繁體中文回答", 
            "translate":False,
            "translate_detail": {
                    "src":"繁體中文",
                    "dst":"english"
                }
            }

        # completion = client.chat.completions.create(
        # model=MODEL,
        # messages=[
        #         {"role": "system", "content": "你是一個富有人性，講話幽默的聊天機器人，使用繁體中文回答"},
        #         {"role": "user", "content": "請你說一個笑話"},
        #     ]
        # )

        # print(completion.choices[0].message.content)
        self.users_data = dict()

        with open('users.json', 'r', encoding='utf8') as file:
            self.users_data = json.load(file)

    def chat(self, msg, user_name, user_id):
        user_id = str(user_id)

        if user_id not in self.users_data:
            self.users_data[user_id] = self.json_template_for_user

            with open('users.json', 'w', encoding='utf8') as file:
                json.dump(obj = self.users_data, fp = file, ensure_ascii = False, indent = 4)

            with open(fr'users\{user_id}', 'w', encoding='utf8') as file:
                pass
    
        if not self.users_data[user_id]['translate']:
            try:
                with open(fr'users\{user_id}', 'r', encoding='utf8') as file:
                    chat_history = file.readlines()

            except:
                chat_history = []
            
            chat_history_str = '\n'.join(chat_history)
            prompt = f"""
            你的個性：{self.users_data[user_id]['prompt']}
            聊天歷史紀錄：{chat_history_str}
            """
            completion = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                        {"role": "system", "content": f"{prompt}"},
                        {"role": "user", "content": f"{user_name}: {msg}"},
                ]
            )

            response = completion.choices[0].message.content

            if len(chat_history) > 30:
                chat_history.pop(0)
                chat_history.pop(1)

            chat_history.append(f"user: {msg}\n")
            chat_history.append(f"you: {response}\n")

            with open(fr'users\{user_id}', 'w', encoding='utf8') as file:
                file.writelines(chat_history)

        else:
            prompt = f"""
            你是一個翻譯官，如果使用者輸入來源語言的內容，你則要翻譯成目的語言的內容，反之如果使用者輸入目的語言的內容，你則要翻譯成來源語言的內容
            來源語言：{self.users_data[user_id]['translate_detail']['src']}
            目的語言：{self.users_data[user_id]['translate_detail']['dst']}
            """
            completion = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                        {"role": "system", "content": f"{prompt}"},
                        {"role": "user", "content": f"{msg}"},
                ]
            )

            response = completion.choices[0].message.content

        return response

    def update_prompt(self, user_id, new_prompt):
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            self.users_data[user_id_str]['prompt'] = new_prompt
            with open('users.json', 'w', encoding='utf8') as file:
                json.dump(self.users_data, file, ensure_ascii=False, indent=4)

        else:
            self.users_data[user_id_str] = {
                "prompt": new_prompt,
                "translate": False,
                "translate_detail": {
                    "src":"繁體中文",
                    "dst":"english"
                }
            }

            with open('users.json', 'w', encoding='utf8') as file:
                json.dump(self.users_data, file, ensure_ascii=False, indent=4)

    def toggle_mode(self, user_id):
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            current_mode = self.users_data[user_id_str]['translate']
            new_mode = not current_mode
            self.users_data[user_id_str]['translate'] = new_mode
            with open('users.json', 'w', encoding='utf8') as file:
                json.dump(self.users_data, file, ensure_ascii=False, indent=4)
            return new_mode
        else:
            self.users_data[user_id_str] = {
                "prompt": "你是一個富有人性，講話幽默的聊天機器人，使用繁體中文回答",
                "translate": True,
                "translate_detail": {
                    "src":"繁體中文",
                    "dst":"english"
                }
            }

            with open('users.json', 'w', encoding='utf8') as file:
                json.dump(self.users_data, file, ensure_ascii=False, indent=4)
            return True
    
    def clear_history(self, user_id):
        user_id_str = str(user_id)
        user_file = os.path.join('users', f'{user_id_str}')
        if os.path.exists(user_file):
            with open(user_file, 'w', encoding='utf8') as file:
                file.write('')
        
    def set_language(self, user_id, src_language, dst_language):
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            self.users_data[user_id_str]['translate_detail']['src'] = src_language
            self.users_data[user_id_str]['translate_detail']['dst'] = dst_language
        else:
            self.users_data[user_id_str] = {
                "prompt": "你是一個富有人性，講話幽默的聊天機器人，使用繁體中文回答",
                "translate": False,
                "translate_detail": {
                    "src": src_language,
                    "dst": dst_language
                }
            }
        with open('users.json', 'w', encoding='utf8') as file:
            json.dump(self.users_data, file, ensure_ascii=False, indent=4)