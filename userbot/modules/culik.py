# Remodified by @xxstanme

from telethon.tl import functions
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError)
from telethon.tl.functions.channels import GetFullChannelRequest

from userbot.events import register
from userbot import CMD_HELP


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**Channel/Grupnya invalid**")
            return None
        except ChannelPrivateError:
            await event.reply("**wah ga bisa nyulik karena channel/group di private**")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**Channel/Grupnya invalid**")
            return None
        except (TypeError, ValueError):
            await event.reply("**Channel/Grupnya invalid**")
            return None
    return chat_info


@register(outgoing=True, pattern=r"^\.duarrame(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        geez = await event.reply("`Proses...`")
    else:
        geez = await event.edit("`Tunggu sebentar...`")
    geezteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await geez.edit("`Wah ga bisa nyulik disini euyy.`")
    s = 0
    f = 0
    error = 'None'

    await geez.edit("Bismillah rame")
    async for user in event.client.iter_participants(geezteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await geez.edit(f"chuaakzz udah kena limit nih besok lagi yaa\n nyulik **{s}** org \n gagal nyulik **{f}** org\n\n**Semangat farmingnya xixi**")
            await event.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await geez.edit(f" nyulik **{s}** org \n gagal nyulik **{f}** org\n `ingfo aja itu gagal karna diprivate akunnya hehe`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await geez.edit(f"chuaakzz berhasil nyulik **{s}** org \n gagal nyulik **{f}** org\n\n**Semangat farmingnya xixi**")


CMD_HELP.update({
    "culik":
        " cmdnya ketik : `.duarrame username gcnya`\
          \nfungsinya : __buat nyulik member dari gc ke gc lain (Awas Kena Limit)__."
})
