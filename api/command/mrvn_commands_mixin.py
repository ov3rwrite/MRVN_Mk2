from typing import Union

from discord import Member, SlashCommand, SlashCommandGroup
from discord.abc import User

from api.command.permission.mrvn_permission import MrvnPermission
from api.models import CommandOverride, MrvnUser


class MrvnCommandsMixin:
    def get_sub_commands(self, group: SlashCommandGroup):
        commands = []

        for sub_cmd in group.subcommands:
            if isinstance(sub_cmd, SlashCommandGroup):
                commands.extend(self.get_sub_commands(sub_cmd))
            else:
                commands.append(sub_cmd)

        return commands

    async def is_owner(self, user: User) -> bool:
        mrvn_user = await MrvnUser.get_or_none(user_id=user.id)

        if not mrvn_user:
            return False

        return mrvn_user.is_owner

    async def has_permission(self, member: Member, command: Union[SlashCommand, SlashCommandGroup],
                             override: CommandOverride = None):
        obj = command if isinstance(command, SlashCommandGroup) else command.callback

        mrvn_perm: MrvnPermission = getattr(obj, "__mrvn_perm__", None)

        if mrvn_perm and mrvn_perm.owners_only:
            return await self.is_owner(member)
        elif override and len(override.discord_permissions):
            perms = override.discord_permissions
        elif mrvn_perm:
            perms = mrvn_perm.discord_permissions
        else:
            return True

        for k, v in iter(member.guild_permissions):
            if k in perms and not v:
                return False

        return True

    def is_guild_only(self, command: Union[SlashCommand, SlashCommandGroup]):
        obj = command if isinstance(command, SlashCommandGroup) else command.callback

        return getattr(obj, "__mrvn_guild_only__", False)