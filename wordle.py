import discord, random, utils, traceback, json
from discord import app_commands
from discord.ext import commands
from utils import generate_blanks, generate_puzzle_embed, is_valid_word, random_puzzle_id, generate_color_word, update_embed

class wordle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="wordle", description="Play a nice game of wordle")
    async def wordle(self, interaction: discord.Interaction):
        puzlle_id = random_puzzle_id()
        embed = generate_puzzle_embed(puzlle_id)
        await interaction.response.send_message(embed=embed)

    @wordle.error
    async def on_wordle_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=str(error), ephemeral=True)

    @app_commands.command(name="wordle-info",description="info about wordle game")
    async def wordle_info(self, interaction: discord.Interaction):
        info_embed=discord.Embed(title="info about the wordle game!")
        info_embed.add_field(name="Game info", value="Players have six attempts to guess a five-letter word, with feedback given for each guess in the form of colored tiles indicating when letters match or occupy the correct position.")
        info_embed.set_footer(text="If you want to play you can use the command '/wordle' or click on the play button")
        await interaction.response.send_message(embed=info_embed)

    @wordle_info.error
    async def on_wordle_info_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=str(error), ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            ref = message.reference
            if not ref or not isinstance(ref.resolved, discord.Message):
                return

            parent = ref.resolved

            if not parent or not parent.embeds or len(parent.embeds) == 0:
                return

            if parent.author.id != self.client.user.id:
                return

            if not is_valid_word(message.content):
                await message.reply("That is not a valid word!\nEnter a valid word of 5 letters in English only!", delete_after=5)
                await message.delete(delay=5)
                return

            embed = parent.embeds[0]

            embed = update_embed(embed, message.content)
            await parent.edit(embed=embed)

            await message.delete()
        except Exception as e:
            print(e)
            traceback.print_exc()


async def setup(client):
    await client.add_cog(wordle(client))