from discord.ext import commands
from discord.ui import Button
import discord

from utils.storage import UserConfig
from config import Settings , LOCAL_DB_FILE
from .wondermind import search_by_feelings

settings = Settings()

cfg = UserConfig(LOCAL_DB_FILE)

class ToggleButton(Button):
    def __init__(self, ctx, active, **kwargs):
        self.active = active
        label = "Deactivate" if active else "Activate"
        super().__init__(label=label, **kwargs)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        self.active = not self.active

        current_state = "Activated" if self.active else "Deactivated"
        label = "Deactivate" if self.active else "Activate"
        self.label = label
        await self.ctx.send(content=f"Morning Quotes. {current_state}", view=self.view)
        doc = {"daily": self.active, "when": self.view.when}
        cfg.write_config(self.ctx.author.id, doc)


class MyView(discord.ui.View):
    def __init__(self, ctx, when, active):
        self.when = when
        super().__init__(timeout=None)
        self.add_item(ToggleButton(ctx, active))

class Dropdown(discord.ui.View):
    @discord.ui.select( 
        placeholder = "How do you feel ?", 
        min_values = 1, 
        max_values = 1, 
        options = [
            discord.SelectOption(
                label="Happy",
                value="happy",
                emoji="😄"
            ),
            discord.SelectOption(
                label="Sad",
                value="sad",
                emoji="😢"
            ),
            discord.SelectOption(
                label="Angry",
                value="angry",
                emoji="😠"
            ),
            discord.SelectOption(
                label="Anxious",
                value="anxious",
                emoji="😟"
            ),
            discord.SelectOption(
                label="Stuck",
                value="stuck",
                emoji="🔒"
            ),
            discord.SelectOption(
                label="Envious",
                value="envious",
                emoji="😒"
            ),
            discord.SelectOption(
                label="Lonely",
                value="lonely",
                emoji="😔"
            )
        ]
    )

    async def select_callback(self, interaction, select):

        item = search_by_feelings(q=select.values[0], key=settings.google_custom_search_key, cx=settings.google_custom_search_engine_id)
        metatags = item['pagemap']['metatags'][0]
        embed = discord.Embed(title=item['title'], description=metatags['og:description'],
                               color=discord.Color.blue(),
                                 url=item['link'])
        embed.set_author(name="Wondermind", url=f"https://{item['displayLink']}", icon_url=metatags["msapplication-tileimage"])
        if 'og:image' in metatags:
            embed.set_image(url=metatags['og:image'])
            embed.set_thumbnail(url=metatags['og:image'])
        else:
            embed.set_image(url='https://cataas.com/cat/says/hello%20world!')
            embed.set_thumbnail(url="https://cataas.com/cat/says/hello%20world!")


        warning_message = "⚠️ **Warning: Content Source** ⚠️\n\n"
        warning_message += "The content provided in this app is sourced from wondermind.com.\n"
        warning_message += "All credit and ownership of the content belong to wondermind.\n"
        warning_message += "Please visit wondermind.com for more information.\n"
        embed.set_footer(text=warning_message)

        await interaction.response.send_message(embed=embed)