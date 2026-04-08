import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
from datetime import datetime, timezone

class PollView(View):
    def __init__(self, poll_id, options):
        super().__init__(timeout=None)
        self.poll_id = poll_id
        self.votes = {i: set() for i in range(len(options))}
        
        for i, option in enumerate(options):
            button = Button(
                label=f"{option} (0)",
                style=discord.ButtonStyle.primary,
                custom_id=f"poll_{poll_id}_{i}"
            )
            button.callback = self.create_vote_callback(i, option)
            self.add_item(button)
        
        results_button = Button(
            label="📊 Show Results",
            style=discord.ButtonStyle.secondary,
            custom_id=f"poll_{poll_id}_results"
        )
        results_button.callback = self.show_results
        self.add_item(results_button)
    
    def create_vote_callback(self, option_index, option_text):
        async def vote_callback(interaction: discord.Interaction):
            user_id = interaction.user.id
            
            for i in self.votes:
                if user_id in self.votes[i]:
                    self.votes[i].remove(user_id)
            
            self.votes[option_index].add(user_id)
            
            for i, item in enumerate(self.children[:-1]):
                if isinstance(item, Button):
                    vote_count = len(self.votes[i])
                    original_label = item.label.rsplit(' (', 1)[0]
                    item.label = f"{original_label} ({vote_count})"
            
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(
                f"✅ You voted for: **{option_text}**",
                ephemeral=True
            )
        
        return vote_callback
    
    async def show_results(self, interaction: discord.Interaction):
        total_votes = sum(len(votes) for votes in self.votes.values())
        
        results = "📊 **Poll Results:**\n\n"
        for i, votes in self.votes.items():
            option_label = self.children[i].label.rsplit(' (', 1)[0]
            vote_count = len(votes)
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            bar_length = int(percentage / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            results += f"**{option_label}**\n{bar} {percentage:.1f}% ({vote_count} votes)\n\n"
        
        results += f"\n**Total Votes:** {total_votes}"
        
        embed = discord.Embed(
            title="Poll Results",
            description=results,
            color=0x8B00FF,
            timestamp=datetime.now(timezone.utc)
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_counter = 0
    
    @app_commands.command(name='poll', description='Create a poll with question and options')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def create_poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
        options = [op for op in [option1, option2, option3, option4, option5] if op]
        
        if len(options) < 2:
            await interaction.response.send_message("❌ You need at least 2 options for a poll!")
            return
        
        self.poll_counter += 1
        
        embed = discord.Embed(
            title=f"📊 {question}",
            description="Click the buttons below to vote!",
            color=0x8B00FF,
            timestamp=datetime.now(timezone.utc)
        )
        
        for i, option in enumerate(options, 1):
            embed.add_field(name=f"Option {i}", value=option, inline=False)
        
        embed.set_footer(text=f"Poll created by {interaction.user}")
        
        view = PollView(self.poll_counter, options)
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name='quickpoll', description='Create a quick poll with yes/no/maybe')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def quick_poll(self, interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            title="📊 Quick Poll",
            description=question,
            color=0x8B00FF,
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_footer(text=f"Poll created by {interaction.user}")
        
        message = await interaction.response.send_message(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await message.add_reaction("🤷")
        # Message deletion not supported in slash commands

async def setup(bot):
    await bot.add_cog(Polls(bot))
