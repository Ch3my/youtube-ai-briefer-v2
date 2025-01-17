# Backend de Youtube Briefer

Ejecuta todas las operaciones con AI, aprovechando LangChain y muchas otras librerias disponibles en Python, se comunica con el Frontend por medio de WebSockets.

Para permitir modificar los prompts con facilidad para finetune segun tus requerimientos, los prompts se encuentran en los archivos `condensa_prompt.txt` y `resume_prompt.txt`

- **resume_prompt.txt**: Es el Prompt que analiza cada seccion y genera las notas de esta seccion
- **condensa_prompt.txt**: Es el prompt que toma todas las notas y las condensa en un solo documento

Ambos archivos deben existir en la raiz del proyecto (a nivel de `main.py`)

Por defecto la App usa una configuracion por defecto, pero seria bueno que le hagas click en guardar a la configuracion para que cree el archivo `config.json` que tambien se encuentra en la raiz

## Entorno de Desarrollo
```
python -m venv .venv
.venv\Script\Activate
pip install ...
```
## Dependencias
```
pip install websockets pyinstaller youtube_transcript_api yt-dlp openai langchain-openai langchain langchain-core langchain-anthropic  langchain-huggingface rank_bm25 faiss-cpu flashrank langchain-community pydantic
``` 

## Compilar
El exe y su carpeta internal deben copiarse a src-tauri. Recuerda ajustar el nombre del exe segun la plataforma

```
pyinstaller --collect-all langchain  --collect-all scipy --collect-all sentence_transformers --collect-all transformers --collect-all posthog --collect-all pydantic --noconfirm main.py
```
