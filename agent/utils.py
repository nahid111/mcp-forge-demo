import json


def print_messages(conversation_data):
    """
    Nicely prints the messages from a conversation data structure.

    Args:
        conversation_data (dict): Dictionary containing a 'messages' key with list of message objects
    """
    messages = conversation_data.get('messages', [])

    for i, message in enumerate(messages, 1):
        print(f'\n--- Message {i} ---')

        # Handle HumanMessage
        if message.__class__.__name__ == 'HumanMessage':
            print('👤 User:')
            print(f'   Content: {message.content}')

        # Handle AIMessage
        elif message.__class__.__name__ == 'AIMessage':
            print('🤖 Assistant:')
            if message.content:
                print(f'   Response: {message.content}')
            elif hasattr(message, 'tool_calls') and message.tool_calls:
                tool_call = message.tool_calls[0]
                print(f'   Tool Call: {tool_call["name"]}')
                print(f'   Arguments: {tool_call["args"]}')

        # Handle ToolMessage
        elif message.__class__.__name__ == 'ToolMessage':
            print('🛠️  Tool Response:')
            print(f'   Tool: {message.name}')

            # Try to parse JSON content if possible
            try:
                tool_data = json.loads(message.content)
                print('   Data:')
                print(
                    f'     Location: {tool_data.get("name", "N/A")}, {tool_data.get("sys", {}).get("country", "N/A")}'
                )
                print(
                    f'     Temperature: {tool_data.get("main", {}).get("temp", "N/A")}°C'
                )
                print(
                    f'     Condition: {tool_data.get("weather", [{}])[0].get("description", "N/A")}'
                )
                print(
                    f'     Humidity: {tool_data.get("main", {}).get("humidity", "N/A")}%'
                )
            except json.JSONDecodeError:
                print(f'   Content: {message.content}')

        print(f'   ID: {message.id}')
