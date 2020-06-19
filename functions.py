#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from database import *
from base import *


def get_n_column_keyb(data, n):
    # creating markup with n columns per line 
    flag = []
    btns = []

    if len(data) <= n:
        btns = [InlineKeyboardButton(d[0], callback_data=d[1]) for d in data]
        return [btns]

    for d in data:
        if len(flag) + 1 < n:
            flag.append(InlineKeyboardButton(d[0], callback_data=d[1]))
        else:
            flag.append(InlineKeyboardButton(d[0], callback_data=d[1]))
            btns.append(flag)
            flag = []
    if flag:
        btns.append(flag)
    return btns


def get_user_info(chat_id):
    # returns info string about user
    user = User.get(User.chat_id == chat_id)
    # if exists
    if user:
        # if username is set
        if user.username:
            username = user.username
        else:
            username = texts['username_not_set']
        return texts['user_info'].replace('<n>', user.first_name).replace('<l>', user.last_name).replace('<s>', str(user.start_time)).replace('<u>', username)
    else: 
        return False


def remove_keyboard(update, context):
    m_id = context.bot.send_message(update._effective_chat.id,  '1', reply_markup=ReplyKeyboardRemove()).message_id
    context.bot.delete_message(chat_id=update._effective_chat.id, message_id=m_id)


''' working with content from user '''


def send_draft(context, draft, to_chat_id):
    # parsing & sending part of draft
    if draft['type'] == 'text':
        m = context.bot.send_message(chat_id=to_chat_id, text=draft['text'])
    elif draft['type'] == 'document':
        m = context.bot.send_document(to_chat_id, draft['file_id'], caption=draft['caption'])
    elif draft['type'] == 'video':
        m = context.bot.send_voice(to_chat_id, draft['file_id'], caption=draft['caption'])
    elif draft['type'] == 'voice':
        m = context.bot.send_voice(to_chat_id, draft['file_id'])
    elif draft['type'] == 'video_note':
        m = context.bot.send_video_note(to_chat_id, draft['file_id'])
    elif draft['type'] == 'sticker':
        m = context.bot.send_sticker(to_chat_id, draft['file_id'])
    # elif draft['type'] == 'contact':
    #     m = context.bot.send_video_note(to_chat_id, draft['file_id'], caption=draft['caption'])
    # elif draft['type'] == 'location':
    #     m = context.bot.send_video(to_chat_id, draft['file_id'], caption=draft['caption'])
    elif draft['type'] == 'audio':
        m = context.bot.send_audio(to_chat_id, draft['file_id'], caption=draft['caption'])
    elif draft['type'] == 'poll':
        m = context.bot.forward_message(to_chat_id, draft['from_chat_id'], draft['message_id'])
    elif draft['type'] == 'photo':
        m = context.bot.send_photo(to_chat_id, draft['file_id'], caption=draft['caption'])
    return m


def get_data(update, context, key, **kwargs):
    # parsing content from update
    msg = update.message

    if kwargs.get('all'):
        kwargs['text'] = True
        kwargs['document'] = True
        kwargs['photo'] = True
        kwargs['video'] = True
        kwargs['voice'] = True
        kwargs['video_note'] = True
        kwargs['location'] = True
        kwargs['audio'] = True
        kwargs['sticker'] = True
        kwargs['poll'] = True
        kwargs['contact'] = True

    # text
    if msg.text and kwargs.get('text'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'text',
            'message_id': msg.message_id,
            'text': msg.text})
    # document
    elif msg.document and kwargs.get('document'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'document',
            'message_id': msg.message_id,
            'file_name': msg.document.file_name,
            'file_id': msg.document.file_id,
            'caption': msg.caption})
    # photo
    elif msg.photo and kwargs.get('photo'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'photo',
            'message_id': msg.message_id,
            'file_id': msg.photo[-1].file_id,
            'caption': msg.caption})
    # video
    elif msg.video and kwargs.get('video'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'video',
            'message_id': msg.message_id,
            'file_id': msg.video.file_id,
            'caption': msg.caption})
    # voice
    elif msg.voice and kwargs.get('voice'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'voice',
            'message_id': msg.message_id,
            'file_id': msg.voice.file_id})
    # video_note
    elif msg.video_note and kwargs.get('video_note'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'video_note',
            'message_id': msg.message_id,
            'file_id': msg.video_note.file_id})
    # location
    elif msg.location and kwargs.get('location'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'location',
            'message_id': msg.message_id,
            'longitude': msg.location.longitude,
            'latitude': msg.location.latitude})
    # audio
    elif msg.audio and kwargs.get('audio'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'audio',
            'message_id': msg.message_id,
            'file_id': msg.audio.file_id})
    # sticker
    elif msg.sticker and kwargs.get('sticker'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'sticker',
            'message_id': msg.message_id,
            'file_id': msg.sticker.file_id})
    # poll
    elif msg.poll and kwargs.get('poll'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'poll',
            'message_id': msg.message_id,
            'id': msg.poll.id})
    # contact
    elif msg.contact and kwargs.get('contact'):
        context.user_data['drafts'][key]['other'].append({
            'type': 'contact',
            'message_id': msg.message_id,
            'phone_number': msg.contact.phone_number,
            'first_name': msg.contact.first_name,
            'user_id': msg.contact.user_id})
    else:
        return False


def publication_preview(arr):
    # creating preview text by parsing user_data
    t = texts['parts_names']
    out_text = ''
    i = 1
    count = config['preview_chars']
    for content in arr:
        # text
        if content['type'] == 'text':
            if len(content['text']) > count:
                out_text += f"{i}. <b>{t[2]}</b>{content['text'].replace('>', '').replace('<', '')[:count]}...\n"
            else:
                out_text += f"{i}. <b>{t[2]}</b>{content['text'].replace('>', '').replace('<', '')}\n"

        # document
        elif content['type'] == 'document':
            if not content['caption']:
                out_text += f"{i}. <b>{t[1]}</b><i>{content['file_name']}</i>\n"
            else:
                if len(content['caption']) > count:
                    out_text += f"{i}. <b>{t[1]}</b>{content['file_name']} <i>{content['caption'][:count]}...</i>\n"
                else:
                    out_text += f"{i}. <b>{t[1]}</b>{content['file_name']} <i>{content['caption']}</i>\n"

        # photo
        elif content['type'] == 'photo':
            if not content['caption']:
                out_text += f"{i}. <b>{t[0][:-2]}</b>\n"
            else:
                if len(content['caption']) > count:
                    out_text += f"{i}. <b>{t[0]}</b><i>{content['caption'][:count]}...</i>\n"
                else:
                    out_text += f"{i}. <b>{t[0]}</b><i>{content['caption']}</i>\n"

        # poll
        elif content['type'] == 'poll':
            out_text += f"{i}. <b>{t[4]}</b>\n"

        # video
        elif content['type'] == 'video':
            if not content['caption']:
                out_text += f"{i}. <b>{t[3][:-2]}</b>\n"
            else:
                if len(content['caption']) > count:
                    out_text += f"{i}. <b>{t[3]}</b><i>{content['caption'][:count]}...</i>\n"
                else:
                    out_text += f"{i}. <b>{t[3]}</b><i>{content['caption']}</i>\n"

        # audio
        elif content['type'] == 'audio':
            if not content['caption']:
                out_text += f"{i}. <b>{t[5]}</b>{content['audio_title']}\n"
            else:
                if len(content['caption']) > count:
                    out_text += f"{i}. <b>{t[5]}</b>{content[[audio_title]]} <i>{content['caption'][:count]}...</i>\n"
                else:
                    out_text += f"{i}. <b>{t[5]}</b>{content['audio_title']} <i>{content['caption']}</i>\n"

        # sticker
        elif content['type'] == 'sticker':
            out_text += f"{i}. <b>{t[6]}</b>\n"

        # contact
        elif content['type'] == 'contact':
            out_text += f"{i}. <b>{t[7]}</b> {content['first_name']}\n"

        # location
        elif content['type'] == 'location':
            out_text += f"{i}. <b>{t[8]}</b>\n"

        # voice
        elif content['type'] == 'voice':
            out_text += f"{i}. <b>{t[9]}</b>\n"

        # video_note
        elif content['type'] == 'video_note':
            out_text += f"{i}. <b>{t[10]}</b>\n"

        i += 1
    return out_text