import discord
from discord.ext import commands, pages


from . import db


def convert_color(r, g, b) -> int:
    return r * 256**2 + g * 256 + b


class ColorCog(commands.Cog):
    __command_group = discord.SlashCommandGroup(name="color")

    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.error_color = 0xdd5e53
        self.default_color = 0x4286f4
        self.success_color = 0x32ad32
        db.db_check()

    def cog_unload(self) -> None:
        self.bot.loaded_extensions.remove("ColorCog")
        return super().cog_unload()
    
    @__command_group.command(name="create", description="Creates a new color (details can be set in popup)")
    @commands.guild_only()
    async def create_command(self, ctx: discord.ApplicationContext):
        await ctx.send_modal(CreateModal(self.bot))

    @__command_group.command(name="delete", description="Deletes a color")
    @commands.guild_only()
    async def delete_command(self, ctx: discord.ApplicationContext, color: str):
        color: db.Color = db.get_color(ctx.guild_id, color)

        # check if color exists
        if not color:
            await ctx.respond(embed=discord.Embed(
                title="Color does not exist",
                color=self.error_color
            ), ephemeral=True)
            return
        
        # delete color from db
        db.delete_color(color.name, ctx.guild.id)

        # delete role
        role = ctx.guild.get_role(color.role_id)
        if role:
            await role.delete()

        # respond
        await ctx.respond(embed=discord.Embed(
            title="Deleted Color",
            color=self.success_color
        ), ephemeral=True)

    @__command_group.command(name="choose", description="Lets you choose a color")
    @commands.guild_only()
    async def choose_command(self, ctx: discord.ApplicationContext, color: str):
        color = db.get_color(ctx.guild_id, color)

        # check if color exists
        if not color:
            await ctx.respond(embed=discord.Embed(
                title="Color does not exist",
                color=self.error_color
            ), ephemeral=True)
            return
        
        # remove old colors
        color_ids = [color.role_id for color in db.get_colors(ctx.guild_id)]
        for role in ctx.user.roles:
            if role.id in color_ids:
                await ctx.user.remove_roles(role)

        # give new color
        role = ctx.guild.get_role(color.role_id)
        await ctx.user.add_roles(role)

        # response
        await ctx.respond(
            embed=discord.Embed(
            title="Color chosen", 
            color=self.success_color),
            ephemeral=True
        )

    @__command_group.command(name="list", description="Shows all colors")
    @commands.guild_only()
    async def list_command(self, ctx: discord.ApplicationContext):
        colors: tuple[db.Color] = db.get_colors(ctx.guild.id)

        # check if colors are empty
        if len(colors) == 0:
            await ctx.respond(embed=discord.Embed(
                title="Currently there is no color",
                color=self.default_color
            ), ephemeral=True)
            return

        # generate embeds
        embeds = []
        for color in colors:
            embed = discord.Embed(
                title=color.name,
                color=convert_color(color.r, color.g, color.b)
            )
            embed.add_field(name="Red", value=str(color.r))
            embed.add_field(name="Green", value=str(color.g))
            embed.add_field(name="Blue", value=str(color.b))
            embeds.append(embed)

        embeds = [embeds[i:i+5] for i in range(0, len(embeds), 5)]

        paginator = pages.Paginator(embeds)
        await paginator.respond(ctx.interaction)

    @__command_group.command(name="edit", description="Let's you edit a color")
    @commands.guild_only()
    async def edit_command(self, ctx: discord.ApplicationContext, color: str):
        await ctx.respond(embed=discord.Embed(
            title="Comming Soon",
            color=self.default_color
        ), ephemeral=True)


class CreateModal(discord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        self.error_color = 0xdd5e53
        self.default_color = 0x4286f4
        self.success_color = 0x32ad32

        super().__init__(title="Farbe erstellen")

        self.__name_input = discord.ui.InputText(
            label="Name", max_length=10, min_length=3, 
        )
        self.add_item(self.__name_input)

        self.__red_input = discord.ui.InputText(
            label="Red (0-255)", max_length=3, min_length=1
        )
        self.add_item(self.__red_input)

        self.__green_input = discord.ui.InputText(
            label="Green (0-255)", max_length=3, min_length=1
        )
        self.add_item(self.__green_input)
        
        self.__blue_input = discord.ui.InputText(
            label="Blue (0-255)", max_length=3, min_length=1
        )
        self.add_item(self.__blue_input)

    async def callback(self, interaction: discord.Interaction):
        # convert
        try:
            red = int(self.__red_input.value)
            green = int(self.__green_input.value)
            blue = int(self.__blue_input.value)
        except ValueError:
            await interaction.response.send_message(
                embed=discord.Embed(
                title="Could not convert the color values", 
                color=self.error_color),
                ephemeral=True
            )
            return

        # checkt color range
        if not 0 <= red <= 255 or not 0 <= green <= 255 or not 0 <= blue <= 255:
            await interaction.response.send_message(
                embed=discord.Embed(
                title="Color values out of range", 
                color=self.error_color),
                ephemeral=True
            )
            return

        # check color already exists
        if db.get_color(interaction.guild.id, self.__name_input.value):
            await interaction.response.send_message(
                embed=discord.Embed(
                title="Color already exists", 
                color=self.error_color),
                ephemeral=True
            )
            return

        # create role
        role = await interaction.guild.create_role(
            name=f"Color: {self.__name_input.value}", 
            color=convert_color(red, green, blue)
        )
        await role.edit(position=len(interaction.guild.roles)-2)

        # add to db
        db.add_color(self.__name_input.value, interaction.guild_id, role.id, red, green, blue)

        # respond
        await interaction.response.send_message(
            embed=discord.Embed(
            title="Color created", 
            color=self.success_color),
            ephemeral=True
        )


def setup(bot):
    bot.add_cog(ColorCog(bot))