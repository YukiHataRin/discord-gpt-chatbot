import discord
from discord.ext import commands
from discord import app_commands
from utils.nlp import ChatBot

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chatbot = ChatBot()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.guild == None:
            msg = self.chatbot.chat(message.content, message.author.name, message.author.id)
            i = 0

            while i < len(msg):
                if len(msg) - i <= 500:
                    await message.channel.send(msg[i:])

                else:
                    await message.channel.send(msg[i:i + 500])
                
                i += 500

        elif message.content.startswith("$"):
            msg = self.chatbot.chat(message.content[1:], message.author.name, message.author.id)
            i = 0

            while i < len(msg):
                if len(msg) - i <= 500:
                    print(msg[i:], end='\n==============\n')
                    await message.reply(msg[i:])

                else:
                    print(msg[i:i + 500], end='\n==============\n')
                    await message.reply(msg[i:i + 500])
                
                i += 500

    @app_commands.command(name="prompt", description="更新提示詞")
    @app_commands.describe(new_prompt = "輸入提示詞")
    async def prompt(self, interaction: discord.Interaction, new_prompt: str):
        user_id = str(interaction.user.id)
        self.chatbot.update_prompt(user_id, new_prompt)
        await interaction.response.send_message(f'你的提示詞已經更改成：{new_prompt}！', ephemeral=True)

    @app_commands.command(name="clear", description="清除聊天歷史紀錄")
    async def clear(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        self.chatbot.clear_history(user_id)
        await interaction.response.send_message(f'已清除聊天紀錄！', ephemeral=True)

    @app_commands.command(name="mode", description="切換聊天與翻譯模式")
    async def mode(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        new_mode = self.chatbot.toggle_mode(user_id)
        mode_text = "翻譯模式" if new_mode else "聊天模式"
        await interaction.response.send_message(f'你的模式已被更改成: {mode_text}！', ephemeral=True)

    @app_commands.command(name="set_language", description="設定翻譯語言")
    @app_commands.describe(src_language = "來源語言", dst_language = "目標語言")
    async def set_language(self, interaction: discord.Interaction, src_language: str, dst_language: str):
        user_id = str(interaction.user.id)
        self.chatbot.set_language(user_id, src_language, dst_language)
        await interaction.response.send_message(f'已將你的翻譯模式設定為: {src_language} -> {dst_language}！', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Base(bot))
