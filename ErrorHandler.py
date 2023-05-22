from datetime import datetime
import time
import discord
from discord.ext import commands
import traceback


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.error_color = 0xdd5e53
        self.default_color = 0x4286f4
        self.success_color = 0x32ad32
    
    def cog_unload(self) -> None:
        self.bot.loaded_extensions.remove("ErrorHandler")
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error):
        error = getattr(error, 'original', error)
        await self.handle_error(ctx, error)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        error = getattr(error, 'original', error)
        await self.handle_error(ctx, error)

    async def handle_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Command nicht gefunden", color=self.error_color)
            command = str(error).split('\"')[1]
            embed.description = f"Der command `{command}` existiert nicht.."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Keine Berechtigung", color=self.error_color)
            embed.description = f"Du hast keine Berechtigung, diesen Command zu verwenden."
            embed.set_footer(text=f"ID: {ctx.author.id}", icon_url=ctx.author.display_avatar.url if ctx.author.display_avatar else ctx.author.default_avatar.url)
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.MissingRole):
            embed = discord.Embed(title="Fehlende Rolle", color=self.error_color)
            embed.description = f"Du benötigst die Rolle `{error.missing_role}`, um diesen Command auszuführen."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Cooldown", color=self.error_color)
            embed.description = f"Du musst noch warten, um diesen command auszuführen." \
                                f" Du kannst ihn <t:{int(time.time() + error.retry_after)}:R> wieder Nutzen."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Keine Berechtigung", color=self.error_color)
            embed.description = f" Nur der Owner dieses Bots darf diesen Command ausführen."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(title="Fehlende Rolle", color=self.error_color)
            embed.description = f"Du brauchst eine beliebige Rolle, um diesen Command auszuführen."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Fehlendes Argument", color=self.error_color)
            embed.description = f"Für diesen Befehl fehlt ein oder mehrere benötigte Argumente."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, discord.errors.CheckFailure) or isinstance(error, commands.errors.CheckAnyFailure):
            embed = discord.Embed(title="Keine Berechtigung", color=self.error_color)
            embed.description = f"Du hast keine Berechtigung, diesen Command zu verwenden."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.errors.NoPrivateMessage):
            embed = discord.Embed(title="Keine Berechtigung", color=self.error_color)
            embed.description = f"{self.no_emote} Du hast keine Berechtigung, diesen Command in den Privatnachrichten zu verwenden."
            embed.set_footer(text=f"ID: {ctx.author.id}")
            embed.timestamp = datetime.now()
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Leider ist ein unerwarteter Fehler aufgetreten.",
                description="Es tut uns leid, das ein unerwarteter Fehler aufgetreten ist. "
                            "Das Development Team wurde bereits benachrichtigt. ",
                color=self.error_color)
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                await ctx.channel.send(embed=embed)

            try:
                raise error
            except Exception as e:
                traceback.print_exc()
                error = traceback.format_exc()
            exception_channel = await self.bot.create_dm(discord.Object(self.bot.owner_id))
            embed = discord.Embed(title=f"Exception in {ctx.guild_id} {ctx.channel.id}", color=0xFF0000)
            if len(error) > 4050:
                error = error[:4050] + "..."
            embed.description = error
            await exception_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))