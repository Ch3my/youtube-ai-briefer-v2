# Backend de Youtube Briefer

Ejecuta todas las operaciones con AI, aprovechando LangChain y muchas otras librerias disponibles en Python, se comunica con el Frontend por medio de WebSockets

## Entorno de Desarrollo
```
python -m venv .venv
.venv\Script\Activate
pip install ...
```
## Dependencias
Quiza puedo quitar langchain chorma

```
pip install websockets pyinstaller youtube_transcript_api yt-dlp openai langchain-openai langchain langchain-core langchain-anthropic  langchain-huggingface rank_bm25 faiss-cpu flashrank langchain-community pydantic
``` 

## Compilar
El exe y su carpeta internal deben copiarse a src-tauri. Recuerda ajustar el nombre del exe segun la plataforma

```
pyinstaller --collect-all langchain --collect-all langchain-community --collect-all scipy --collect-all sentence_transformers --collect-all transformers --collect-all posthog --collect-all pydantic --noconfirm main.py
```
