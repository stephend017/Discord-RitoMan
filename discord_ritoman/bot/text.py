from discord_ritoman.bot.bot_command import bot_command
from discord_ritoman.db.accessors import add_lol_text


@bot_command(name="text")
class TextCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("<:PepoG:773739956958658560>")

    @staticmethod
    async def option_list(ctx, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    async def option_add(ctx, *args, **kwargs):
        group_name: str = args[0]
        content: str = args[1]
        author_id = ctx.message.author.id
        add_lol_text(group_name, content, author_id)

    @staticmethod
    async def option_remove(ctx, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def help():
        return """
        Function to add, list and remove text from the ritoman database

        Usage:
            @ritoman text --add <group_name> <content>
            @ritoman text --list <group_name>
            @ritoman text --remove <hash>
        """
