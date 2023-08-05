from .. import Menu

from .ConfigType import ConfigType


@ConfigType("bot.addct")
class AddCT(Menu.FireableCmd):
    defaultName = "Bot Add CT"
    defaultDesc = "Add a bot to the Counter-Terrorist team."
    cmd = "bot_add_ct"


@ConfigType("bot.addt")
class AddT(Menu.FireableCmd):
    defaultName = "Bot Add T"
    defaultDesc = "Add a bot to the Terrorist team."
    cmd = "bot_add_t"


@ConfigType("bot.kick")
class Kick(Menu.FireableCmd):
    defaultName = "Bot Kick"
    defaultDesc = "Kick all bots."
    cmd = "bot_kick"


@ConfigType("bot.kill")
class Kill(Menu.FireableCmd):
    defaultName = "Bot Kill"
    defaultDesc = "Kill all bots."
    cmd = "bot_kill"


@ConfigType("bot.stop")
class Stop(Menu.ChoiceVarBinary):
    defaultName = "Bot Stop"
    defaultDesc = "Enable/disable all bot processing."
    var = "bot_stop"


@ConfigType("bot.allweps")
class AllWeps(Menu.FireableCmd):
    defaultName = "Bot Allow All Weapons"
    defaultDesc = "Allow bots to use all weapons."
    cmd = "bot_all_weapons"


@ConfigType("bot.allowrogues")
class AllowRogues(Menu.ChoiceVarBinary):
    defaultName = "Bot Allow Rogues"
    defaultDesc = "Allow bots to become 'rogue' randomly."
    var = "bot_allow_rogues"


@ConfigType("bot.chatter")
class Chatter(Menu.ChoiceVar):
    defaultName = "Bot Chatter Set"
    defaultDesc = "Configure bots' talking."

    def __init__(self, parent, options):
        Menu.ChoiceVar.__init__(self, parent, options)
        self.addChoice("off")
        self.addChoice("radio")
        self.addChoice("minimal")
        self.addChoice("normal")
        self.setVar("bot_chatter")
        self.makeChoices()


@ConfigType("bot.difficulty")
class Difficulty(Menu.Bar):
    defaultName = "Bot Difficulty Set"
    defaultDesc = "Set bots' difficulty."

    def __init__(self, parent, options):
        Menu.Bar.__init__(self, parent, options)
        self.setMin(0)
        self.setMax(3)
        self.setDefault(1.0)
        self.setSteps(3)
        self.setVar("bot_difficulty")
        self.makeChoices()


@ConfigType("bot.dontshoot")
class DontShoot(Menu.ChoiceVarBinary):
    defaultName = "Bot Don't Shoot"
    defaultDesc = "Enable/Disable bots' shooting."
    var = "bot_dont_shoot"


@ConfigType("bot.freeze")
class Freeze(Menu.ChoiceVarBinary):
    defaultName = "Bot Freeze"
    defaultDesc = "Enable/disable bot freeze."
    var = "bot_freeze"


@ConfigType("bot.quota")
class Quota(Menu.Bar):
    defaultName = "Bot Quota Set"
    defaultDesc = "Set the max amount of bots in a game."

    def __init__(self, parent, options):
        Menu.Bar.__init__(self, parent, options)
        self.setMin(0)
        self.setMax(self.optValue(options, "max", 16))
        self.setDefault(0)
        self.setStyle("int")
        self.setSteps(self.optValue(options, "max", 16))
        self.setVar("bot_quota")
        self.makeChoices()


@ConfigType("bot.mimic")
class Mimic(Menu.ChoiceVarBinary):
    defaultName = "Bot Mimic"
    defaultDesc = "Enable/disable bots mimicing you."
    var = "bot_mimic"


@ConfigType("bot.zombie")
class Zombie(Menu.ChoiceVarBinary):
    defaultName = "Bot Zombie"
    defaultDesc = "Enable/disable bot zombie (sicko) mode."
    var = "bot_zombie"
