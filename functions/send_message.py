# send_message.py

import asyncio
import json
from globals import Globals  # Import the Globals singleton

async def send_message(message):
    """
    Send a message to all connected clients.
    
    Args:
        message: The message to send, typically a dictionary.
    """
    globals_instance = Globals()  # Get the singleton instance
    if globals_instance.connected_clients:  # Check if there are any connected clients
        message_data = json.dumps(message)
        
        # Create a list of tasks for sending messages to all clients
        tasks = [asyncio.create_task(client.send(message_data)) for client in globals_instance.connected_clients]
        await asyncio.gather(*tasks)  # Wait for all tasks to complete
