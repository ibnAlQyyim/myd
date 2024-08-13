
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , CallbackQuery
from pyrogram import Client, filters
import os, time, yt_dlp, wget, subprocess
from datetime import timedelta
import gradio as gr
from multiprocessing import Process

def execute_terminal_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        return output
    except Exception as e:
        return str(e)

def terminal_interface(command):
    output = execute_terminal_command(command)
    return output
  
iface = gr.Interface(fn=terminal_interface, inputs="text", outputs="text", title="Terminal Interface")

app = Client(
    "yt_bot",
    api_id=1234556,
    api_hash="442u447737KfocinLpw0e",
    bot_token="123456789:Labcxowv37eghwidbd8383zfkqqqpzmnnxHFE"
)


@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(message.chat.id, "Hi I'am ytdlp", disable_web_page_preview=True)

@app.on_message(filters.regex(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$'))
def url(client, message):
    buttons = [
            [InlineKeyboardButton("مقطع", callback_data="format_video")],
            [InlineKeyboardButton("صوت", callback_data="format_audio")],
            [InlineKeyboardButton("إلغاء", callback_data="cancel")]
        ]

    reply_markup = InlineKeyboardMarkup(buttons)
    print(message.id)
    message.reply("اختر:", reply_markup=reply_markup, reply_to_message_id=message.id)

@app.on_callback_query(filters.regex(r'format_'))
def quality(client, callback_query: CallbackQuery):
    typ = callback_query.data.split("_")[1]
    buttons = [
            [InlineKeyboardButton("low", callback_data=f"quality_{typ}_low")],
            [InlineKeyboardButton("medium", callback_data=f"quality_{typ}_medium")],
            [InlineKeyboardButton("best", callback_data=f"quality_{typ}_best")],
            [InlineKeyboardButton("إلغاء", callback_data="cancel")]
        ]

    reply_markup = InlineKeyboardMarkup(buttons)
    client.edit_message_text(callback_query.from_user.id, message_id=callback_query.message.id, text="quality", reply_markup=reply_markup)

@app.on_callback_query(filters.regex(r'quality_'))
def download(client, callback_query: CallbackQuery):
    print("download")
    message = client.get_messages(callback_query.from_user.id, message_ids=callback_query.message.reply_to_message.id)
#    progress_message = client.send_message(message.chat.id, '\U0001F4E5**Downloading ...**', reply_to_message_id=message.id)
    client.edit_message_text(callback_query.from_user.id, message_id=callback_query.message.id, text="downloading....")
    typ = callback_query.data.split("_")[1]
    qty = callback_query.data.split("_")[2]

    url = message.text
    if typ == "video":
        print("video")

        if qty == "low":
            qtyfmt = "worst"

        if qty == "medium":
            qtyfmt = "18"

        if qty == "best":
            qtyfmt = "best[ext=mp4]+bestaudio"

        ydl_opts = {"format": qtyfmt}
        path = ""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)

        title = info['title']
        dur =  info['duration']
        perf = info['channel']
        thumbnail = wget.download(info['thumbnail'])
        width = info['width']
        height = info['height']
        app.send_video(message.chat.id, path, caption=f"**{title}***", duration=dur, width=width, height=height, thumb=thumbnail, reply_to_message_id=message.id)

    if typ == "audio":
        print("audio")

        if qty == "low":
            qtyfmt = "139"

        if qty == "medium":
            qtyfmt = "139-drc"

        if qty == "best":
            qtyfmt = "bestaudio[ext=m4a]"

        ydl_opts = {"format": qtyfmt}
        path = ""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)

        title = info['title']
        dur =  info['duration']
        perf = info['channel']
        thumbnail = wget.download(info['thumbnail'])
        channel_name = info['channel']
        client.send_audio(message.chat.id, audio=path, duration=dur, performer=perf, title=title, caption=f"**{title}**", reply_to_message_id=message.id, thumb=thumbnail)

    os.system(f"rm -rf '{thumbnail}' '{path}'")


if __name__ == '__main__':
    Process(target=iface.launch).start()   
try:
    app.run()
except Exception as e:
    print("Error:",e)
