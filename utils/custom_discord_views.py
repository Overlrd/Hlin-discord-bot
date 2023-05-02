import discord
from utils.config_utils import update_dayly_quote_config

class ToggleButton(discord.ui.Button):
    def __init__(self, active, **kwargs):
        self.active = active
        label = "Deactivate" if active else "Activate"
        super().__init__(label=label, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.active = not self.active

        current_state = "Activated" if self.active else "Deactivated"
        label = "Deactivate" if self.active else "Activate"
        self.label = label
        await interaction.response.edit_message(content=f"Moring Quotes. {current_state} ", view=self.view)
        update_dayly_quote_config(interaction.user.id, dayly=self.active, when=self.view.when)


class MyView(discord.ui.View):
    def __init__(self, when, active):
        self.when = when
        super().__init__(timeout=None)
        self.add_item(ToggleButton(active))
