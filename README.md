# Discord Chatbot

這是一個基於 Discord 的聊天機器人，具有多種功能，包括自然語言處理、翻譯和聊天歷史管理。

## 功能

- **聊天功能**：與用戶進行自然語言聊天。
- **翻譯功能**：支援語言翻譯模式，可設置來源語言和目標語言。
- **清除聊天歷史**：清除用戶的聊天歷史紀錄。
- **模式切換**：在聊天模式和翻譯模式之間切換。
- **更新提示詞**：更新機器人的回應風格提示詞。

## 安裝

1. 克隆這個專案到本地：
    ```bash
    git clone https://github.com/YukiHataRin/discord-gpt-chatbot.git
    cd discord-gpt-chatbot
    ```

2. 安裝所需的模組：
    ```bash
    pip install -r requirements.txt
    ```

3. 設定 `.env` 文件並添加你的 Discord Bot Token、OpenAI API Key以及要使用的自然語言處理模型：

## 使用

1. 確保已經按照上述步驟安裝了所有依賴並配置了環境變數。

2. 啟動機器人：
    ```bash
    python bot.py
    ```

3. 機器人上線後，可以在 Discord 中使用以下指令：
    - **`/prompt <new_prompt>`**：更新機器人的提示詞。
    - **`/clear`**：清除聊天歷史紀錄。
    - **`/mode`**：切換聊天模式和翻譯模式。
    - **`/set_language <src_language> <dst_language>`**：設定翻譯模式的來源語言和目標語言。
  
4. 使用時，若在伺服器想要與機器人對話則需要在訊息前加上$

## 文件結構

- `bot.py`：主程式，負責啟動機器人並載入擴展功能。
- `cogs/base.py`：擴展功能，包含處理訊息和指令的邏輯。
- `utils/nlp.py`：自然語言處理功能，處理聊天內容和模式切換等。
- `.env`：環境變數配置文件。
- `user.json`：用戶資料，存放用戶的提示詞、模式和翻譯設定。
- `users`：存放用戶的聊天歷史紀錄。
