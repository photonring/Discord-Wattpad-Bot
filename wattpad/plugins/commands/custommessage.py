from soupsieve import select
from wattpad.pluginsexecution.commandsexec.custommessageexec import CustomMessageExec
from wattpad.utils.config import Config
import lightbulb
from wattpad.logger.baselogger import BaseLogger
import hikari

plugin= lightbulb.Plugin("CustomMessagePlugin")

file_prefix= "wattpad.plugins.commands.custommessage"
logger=BaseLogger().loggger_init()

@plugin.command()
@lightbulb.command("set-custom-message","set a custom message for bot to use while sharing updates",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_custom_message(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message method invoked for server: %s", file_prefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e


@set_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.option("message","Your custom message",required=True)
@lightbulb.command("for-story","set a custom messages for a particular story", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_message_for_story(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message)

        guildId= str(ctx.guild_id)
        message= ctx.options.message
        story_url= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().set_custom_message_for_story(guildId, story_url, message)
    
    except Exception as e:
        logger.fatal("Exception occured in %s. method",exc_info=1)
        raise e
    




def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin) 