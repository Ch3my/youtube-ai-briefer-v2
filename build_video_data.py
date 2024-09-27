import threading
from functions.build_rag import build_rag
from functions.build_notas_detalladas import build_notas_detalladas
from functions.get_transcript import get_transcript
from functions.send_message import send_message


async def build_video_data(data):
    """
    Funcion que construye el rag y procesa el video, se utiliza la misma funcion
    cuando se utiliza whisper solo que debe venir la confirmacion desde el Front
    Args: {data: { whisperConfirmed: bool, url: string }}
    """
    transcript = None
    try:
        transcript = await get_transcript(data)
    except Exception as e:
        print("Error Fatal:", e)
        return

    # Si no se logro obtener salimos, mensajes ya debieron ser entregados al usuario
    if transcript is None:
        return

    await send_message(
        {
            "action": "message",
            "msgCode": "info",
            "msg": f"Transcript obtenido ({len(transcript):,})",
        }
    )
    await send_message(
        {
            "action": "transcript",
            "transcript": transcript,
        }
    )

    # ===== Build RAG, in other Thread ====
    # A penas tenemos el Transcript enviamos a crear el Rag, asi cuando probablemente terminenos el RAG
    # antes de que termine el procesamiento. La coma es necesaria, sino piensa que cada caracter es un argumento
    # A daemon thread is a thread that doesn’t prevent the program from exiting.
    # If the program ends or all non-daemon threads finish execution, any remaining daemon threads are stopped.
    rag_thread = threading.Thread(target=build_rag, args=(transcript,))
    rag_thread.setDaemon(True)
    rag_thread.start()

    # Build Resumen
    await send_message(
        {
            "action": "message",
            "msgCode": "info",
            "msg": "Construyendo Notas",
        }
    )
    notas_detalladas = await build_notas_detalladas(transcript)

    await send_message(
        {
            "action": "notasDetalladas",
            "notasDetalladas": notas_detalladas,
        }
    )
