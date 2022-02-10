from youtubesearchpython import VideosSearch
import os
from os import path
import random
import asyncio
import shutil
from time import time
import yt_dlp
from .. import converter
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from Yukki import (app, BOT_USERNAME, BOT_ID)
from ..YukkiUtilities.tgcallsrun import (yukki, convert, download, clear, get, is_empty, put, task_done, smexy)
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.database.onoff import (is_on_off, add_on, add_off)
from Yukki.YukkiUtilities.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from Yukki.YukkiUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Yukki.YukkiUtilities.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from Yukki.YukkiUtilities.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from Yukki.YukkiUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from ..config import DURATION_LIMIT, ASS_ID
from ..YukkiUtilities.helpers.decorators import errors
from ..YukkiUtilities.helpers.filters import command, other_filters
from ..YukkiUtilities.helpers.gets import (get_url, themes, random_assistant)
from ..YukkiUtilities.helpers.thumbnails import gen_thumb
from ..YukkiUtilities.helpers.chattitle import CHAT_TITLE
from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from ..YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, )


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",]   


@Client.on_message(command(["playlist", "playlist@Venzastreambot"]) & other_filters)
async def start_playlist_cmd(_, message):
    thumb ="cache/playlist.png"
    await message.reply_photo(
    photo=thumb, 
    caption=("**❓ Playlist mana yang ingin kamu mainkan ?**"),    
    reply_markup=play_list_keyboard) 
    return 


@Client.on_message(command(["delmyplaylist", "delmyplaylist@Venzastreambot"]) & other_filters)
async def delmyplaylist(_, message):
    usage = ("usage:\n\n/delmyplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delmyplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"💡 **Konfirmasi** !!\n\nApakah Anda yakin ingin menghapus seluruh daftar putar Anda? ?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("Anda tidak memiliki daftar putar di database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"✅ Menghapus {count} musik di daftar putar")
                else:
                    return await message.reply_text("tidak ada musik yang disimpan dalam daftar putar !")                                
        await message.reply_text("Anda tidak memiliki musik seperti itu di daftar putar !")                             


@Client.on_message(command(["delchatplaylist", "delchatplaylist@Venzstreambot"]) & other_filters)
async def delchatplaylist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("Anda kehilangan hak admin untuk menggunakan perintah ini.\n\n» ❌ Dapat_Mengelola_Obrolan_Suara")
    usage = ("usage:\n\n/delchatplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delchatplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 21:
        return await message.reply_text(f"💡 Konfirmasi !\n\nApakah Anda yakin ingin menghapus seluruh daftar putar Grup? ?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("Grup tidak memiliki daftar putar di basis data !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"**✅ Menghapus {count} musik dalam daftar putar grup**")
                else:
                    return await message.reply_text(f"**tidak ada musik yang disimpan dalam daftar putar grup !**")                                
        await message.reply_text("Anda tidak memiliki musik seperti itu di daftar putar Grup!")
