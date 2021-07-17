import discord
import time
import datetime
import psutil
import os
import json
import sqlite3

from discord.ext import commands

with open('config.json', mode='r', encoding='utf8') as config:
    c = json.load(config)

start_time = datetime.datetime.utcnow()
owner_id = int(c['owner_id'])


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())


    def en_get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    def tw_get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} 天, {h} 小時, {m} 分鐘, {s} 秒'
            else:
                fmt = '{h} 小時, {m} 分鐘, {s} 秒'
        else:
            fmt = '{h}小時 {m}分鐘 {s}秒'
            if days:
                fmt = '{d}天 ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


    @commands.command()
    async def ping(self, ctx):
        lang = sqlite3.connect('database/lang.db')
        cursor = lang.cursor()
        cursor.execute(f"SELECT lang FROM datas WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        owner = await self.bot.fetch_user(owner_id)
        ownera = owner.avatar_url
        t = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.trigger_typing()
        bot = round((t2 - t) * 1000)
        ws = int(self.bot.latency * 1000)
        us_text = self.en_get_bot_uptime(brief=True)
        tw_text = self.tw_get_bot_uptime(brief=True)
        
        if str(result[0]) == 'en':
            embed=discord.Embed(title=f'PING', description=f'🕒Uptime: {us_text}\n \n⌛Latency: `{bot}` (ms)\n \n🌐Websocket: `{ws}` (ms)',
            color=0xacacc1, timestamp= datetime.datetime.now())
            embed.set_footer(text=f'By {owner}', icon_url=ownera)
            await ctx.send(embed=embed)
        if str(result[0]) == 'tw':
            embed=discord.Embed(title=f'PING', description=f'🕒運行時間: {tw_text}\n \n⌛延遲: `{bot}` (毫秒)\n \n🌐Websocket: `{ws}` (毫秒)',
            color=0xacacc1, timestamp= datetime.datetime.now())
            embed.set_footer(text=f'作者 {owner}', icon_url=ownera)
            await ctx.send(embed=embed)
        cursor.close()
        lang.close()


def setup(bot):
    bot.add_cog(Ping(bot))
