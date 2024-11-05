import openai #GPT based prompt engineering
from openai import OpenAI
import ast

client = OpenAI()
client = OpenAI()
def get_events_from_text(user_input:str) -> dict:
    prompt = f"""
    For the events in the {user_input}:
    ONLY return the output in the following structure as a **Python list of dictionaries**, without additional explanations or comments:
    [
      {{'start_time': 'YYYY-MM-DD HH:MM', 'end_time': 'YYYY-MM-DD HH:MM', 'description': 'event details', 'location': 'location details'}},
      {{'start_time': 'YYYY-MM-DD HH:MM', 'end_time': 'YYYY-MM-DD HH:MM', 'description': 'event details','location': 'location details'}},
      ...
    ]
    Do not include any additional explanations, comments, or text outside of the Python list of dictionaries.
    """

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # Get the content of the message
    message_content = completion.choices[0].message.content.strip()

    # Find the first occurrence of "[" and extract the content from there
    start_idx = message_content.find('[')
    if start_idx != -1:
        # Extract the valid Python list-like content
        list_content = message_content[start_idx:]

        try:
            # Safely evaluate the list of dictionaries from the string
            events = ast.literal_eval(list_content)
            return events  # Returning the list of events
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing the events: {e}")
            print(f"Received content: {list_content}")
            return None
    else:
        print("No valid list found in the response.")
        return None