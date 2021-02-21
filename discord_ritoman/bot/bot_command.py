from discord_ritoman.bot.bot import bot
from discord_ritoman.utils import create_logger

logger = create_logger(__file__)

GLOBAL_COMMAND_TABLE = {}


async def default_func(ctx, *args, **kwargs):
    pass


def bot_command(command_name: str):
    def decorator(cls):
        class Wrapper(object):
            def __init__(self):
                self.options = {}
                self.default_option = default_func
                self.main_func = default_func

        @bot.command(name=command_name)
        async def execute(ctx, *args, **kwargs):
            global GLOBAL_COMMAND_TABLE
            if len([*args]) > 0:
                option = f"option_{args[0]}"
                if option in GLOBAL_COMMAND_TABLE[command_name].options:
                    await GLOBAL_COMMAND_TABLE[command_name].options[
                        option
                    ].__get__(GLOBAL_COMMAND_TABLE[command_name])(
                        ctx, *args[1:], **kwargs
                    )
                else:
                    await GLOBAL_COMMAND_TABLE[
                        command_name
                    ].default_option.__get__(
                        GLOBAL_COMMAND_TABLE[command_name]
                    )(
                        ctx, *args, **kwargs
                    )
            else:
                await GLOBAL_COMMAND_TABLE[
                    command_name
                ].default_option.__get__(GLOBAL_COMMAND_TABLE[command_name])(
                    ctx, *args, **kwargs
                )

        w = Wrapper()

        for key, value in [
            (x, y) for x, y in cls.__dict__.items() if type(y) == staticmethod
        ]:
            # this is where we process special methods
            if key == "default":
                # this function is for processing default behavior (no flag)
                w.default_option = value
            if key.startswith("option_"):
                # this is for options that have flags
                w.options[key] = value

        w.main_func = execute
        if command_name in GLOBAL_COMMAND_TABLE:
            raise ValueError(f"{command_name} has already been defined")

        logger.info(command_name)
        logger.info(bot.all_commands)

        GLOBAL_COMMAND_TABLE[command_name] = w

        return execute

    return decorator
