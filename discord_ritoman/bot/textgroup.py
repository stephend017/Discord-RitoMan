from discord_ritoman.bot.bot_command import bot_command
from discord_ritoman.db.accessors import add_lol_text_group


@bot_command("textgroup")
class TextGroupCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("<:PepoG:773739956958658560>")

    @staticmethod
    async def option_list(ctx, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    async def option_add(ctx, *args, **kwargs):
        author_id = ctx.message.author.id
        group_name: str = args[0]
        group_description: str = args[1]

        add_lol_text_group(group_name, group_description, author_id)

    @staticmethod
    async def option_remove(ctx, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def help():
        return """
        Function to add, list and remove textgroups from the ritoman database

        Usage:
            @ritoman textgroup --add <group_name> <group_description>
            @ritoman textgroup --list
            @ritoman textgroup --remove <group_name>
        """
