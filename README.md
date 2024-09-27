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

`pip install websockets pyinstaller youtube_transcript_api yt-dlp openai langchain-openai langchain langchain-core langchain-anthropic langchain_chroma langchain-huggingface rank_bm25 faiss-cpu flashrank langchain-community` 



// Define the WebSocket URL
const wsUrl = 'ws://localhost:12345';

// Create a new WebSocket instance
const socket = new WebSocket(wsUrl);

// Define the data to be sent
const data = {
    whisperConfirmed: true, // Change this to false if needed
    url: 'https://www.youtube.com/watch?v=XOqGDLy1IGU',
    action: "build"
};

// Convert the data to a JSON string
const jsonData = JSON.stringify(data);

// Event handler for when the connection is open
socket.addEventListener('open', (event) => {
    console.log('Connected to WebSocket server');
    // Send the JSON data
    socket.send(jsonData);
    console.log('Sent data:', jsonData);
});

// Event handler for when a message is received
socket.addEventListener('message', (event) => {
    console.log('Received message:', event.data);
});

// Event handler for when the connection is closed
socket.addEventListener('close', (event) => {
    console.log('Disconnected from WebSocket server');
});

// Event handler for any errors
socket.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});