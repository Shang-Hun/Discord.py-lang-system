import discord
import json
import sqlite3

from discord.ext import commands

with open('config.json', mode='r', encoding='utf8') as config:
    c = json.load(config)

owner_id = int(c['owner_id'])


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        lang = sqlite3.connect('database/lang.db')
        cursor = lang.cursor()
        cursor.execute(f"SELECT lang FROM datas WHERE guild_id = {guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = ("INSERT INTO datas(guild_id, lang) VALUES(?,?)")
            val = (str(guild.id), 'en')
            cursor.execute(sql, val)
            lang.commit()
        cursor.close()
        lang.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lang(self, ctx, l=None):
        lang = sqlite3.connect('database/lang.db')
        cursor = lang.cursor()
        cursor.execute(f"SELECT lang FROM datas WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        owner = await self.bot.fetch_user(owner_id)
        ownera = owner.avatar_url
        
        if str(result[0]) == 'en':
            if l == 'en-US':
                embed=discord.Embed(description=f'The language is already English!',
                color=discord.Color.red())
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            elif l == 'zh-TW':
                sql = ("UPDATE datas SET lang = ? WHERE guild_id = ?")
                val = ('tw', str(ctx.guild.id))
                cursor.execute(sql, val)
                lang.commit()
                embed=discord.Embed(description=f'語言已切換成繁體中文!',
                color=discord.Color.green())
                embed.set_footer(text=f'作者 {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'**目前只支援英文還有繁體中文! `en-US` __英文__ `zh-TW` __繁體中文__**\n**Currently only supports English and Taiwanese `en-US` __English__ `zh-TW` __Taiwanese__**')
        if str(result[0]) == 'tw':
            if l == 'zh-TW':
                embed=discord.Embed(description=f'語言已經是繁體中文了!',
                color=discord.Color.red())
                embed.set_footer(text=f'作者 {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            elif l == 'en-US':
                sql = ("UPDATE datas SET lang = ? WHERE guild_id = ?")
                val = ('en', str(ctx.guild.id))
                cursor.execute(sql, val)
                lang.commit()
                embed=discord.Embed(description=f'Language has been switched to English!',
                color=discord.Color.green())
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'**目前只支援英文還有繁體中文! `en-US` __英文__ `zh-TW` __繁體中文__**\n**Currently only supports English and Taiwanese `en-US` __English__ `zh-TW` __Taiwanese__**')
        cursor.close()
        lang.close()


def setup(bot):
    bot.add_cog(Main(bot))