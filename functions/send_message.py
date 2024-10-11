import asyncio
import json
from globals import Globals
from datetime import datetime

async def send_message(message):
    """
    Send a message to all connected clients.

    Args:
        message: The message to send, typically a dictionary.
    """
    globals_instance = Globals()  # Get the singleton instance
    if globals_instance.connected_clients:  # Check if there are any connected clients
        message_data = json.dumps(message)
        
        # Print statement to show the date, time, message info, and its length
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time} - sending message - length: {len(message_data)}")

        # Create a list of tasks for sending messages to all clients.
        # This is necessary to ensure non-blocking execution, allowing
        # all send operations to occur concurrently. By using
        # asyncio.create_task(), we can handle multiple clients efficiently
        # without waiting for each send operation to complete individually.
        # This approach also facilitates centralized error handling
        # and enhances scalability, ensuring our application remains responsive
        # even with a large number of connected clients.
        tasks = [
            asyncio.create_task(client.send(message_data))
            for client in globals_instance.connected_clients
        ]
        await asyncio.gather(*tasks)  # Wait for all tasks to complete
