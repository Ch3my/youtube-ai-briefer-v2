import asyncio
from functions.send_message import send_message
from functions.whisper_transcript import whisper_transcript
from functions.get_video_id import get_video_id
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


async def get_transcript(data):
    yt_vide_id = get_video_id(data.get("url"))
    transcript = ""
    try:
        chunks = YouTubeTranscriptApi.get_transcript(
            yt_vide_id, languages=["es", "en", "en-GB"]
        )
        transcript = "".join([i["text"] for i in chunks])
    except TranscriptsDisabled as e:
        if data.get("whisperConfirmed") != True:
            await send_message(
                {
                    "action": "message",
                    "msgCode": "useWhisper",
                    "msg":"La transcripcion esta desactivada para este video",
                }
            )
            return None
    except NoTranscriptFound as e:
        if data.get("whisperConfirmed") != True:
            await send_message(
                {
                    "action": "message",
                    "msgCode": "useWhisper",
                    "msg": "No existe una transcripcion en los idiomas aceptados",
                }
            )
            return None

    if transcript == None and data.get("whisperConfirmed") == True:
        transcript = whisper_transcript(data.get("url"))

    return transcript
