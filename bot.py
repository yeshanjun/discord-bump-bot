import discord
from discord.ext import commands
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BumpBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/', intents=intents)
        
        self.monitor_channels = self._parse_env_list(os.getenv('MONITOR_CHANNEL_IDS', '[]'))
        self.required_roles = self._parse_env_list(os.getenv('REQUIRED_ROLE_IDS', '[]'))
        self.admin_users = self._parse_env_list(os.getenv('ADMIN_USER_IDS', '[]'))
        self.config = self._load_config()
    
    def _parse_env_list(self, env_string: str) -> List[int]:
        """解析环境变量中的JSON数组为整数列表"""
        try:
            return [int(x) for x in json.loads(env_string)]
        except (json.JSONDecodeError, ValueError):
            return []
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("config.json not found, using empty config")
            return {"keywords": []}
        except json.JSONDecodeError:
            print("Invalid JSON in config.json")
            return {"keywords": []}
    
    def _has_required_role(self, member: discord.Member) -> bool:
        """检查用户是否有必需的角色"""
        if not self.required_roles:
            return True
        
        member_roles = [role.id for role in member.roles]
        return any(role_id in member_roles for role_id in self.required_roles)
    
    async def _send_keyword_response(self, message: discord.Message, keyword_config: Dict[str, Any]):
        """发送关键词回复"""
        embed_data = keyword_config.get('embed', {})
        embed = discord.Embed(
            title=embed_data.get('title', ''),
            description=embed_data.get('description', ''),
            color=int(embed_data.get('color', '0x0099ff'), 16)
        )
        
        view = discord.ui.View()
        buttons = keyword_config.get('buttons', [])
        
        for button_data in buttons:
            button = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label=button_data.get('label', '链接'),
                url=button_data.get('url', ''),
                emoji=button_data.get('emoji')
            )
            view.add_item(button)
        
        await message.reply(embed=embed, view=view, mention_author=False)
    
    async def on_ready(self):
        print(f'{self.user} 已连接到Discord!')
        print(f'监听频道: {self.monitor_channels}')
        print(f'必需角色: {self.required_roles}')
        print(f'管理员: {self.admin_users}')
    
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        if message.channel.id not in self.monitor_channels:
            return
        
        if not isinstance(message.author, discord.Member):
            return
        
        if not self._has_required_role(message.author):
            return
        
        message_content = message.content.strip()
        
        keyword_matched = False
        for keyword_data in self.config.get('keywords', []):
            if message_content == keyword_data.get('trigger', ''):
                await self._send_keyword_response(message, keyword_data['response'])
                keyword_matched = True
                break
        
        if not keyword_matched:
            await self.process_commands(message)
    
    @commands.command(name='reload')
    async def reload_config(self, ctx):
        """重新加载配置文件（仅管理员可用）"""
        if ctx.author.id not in self.admin_users:
            await ctx.reply("❌ 你没有权限使用此命令", mention_author=False)
            return
        
        try:
            self.config = self._load_config()
            await ctx.reply("✅ 配置已重新加载", mention_author=False)
        except Exception as e:
            await ctx.reply(f"❌ 配置加载失败: {str(e)}", mention_author=False)

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("错误: 请设置DISCORD_TOKEN环境变量")
        return
    
    bot = BumpBot()
    bot.run(token)

if __name__ == '__main__':
    main()