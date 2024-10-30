import json
import openai #GPT based prompt engineering
from openai import OpenAI
#import os #read enviroment variables
from ics import Calendar, Event #create files
import datetime
import ast
from zoneinfo import ZoneInfo

client = OpenAI()


def get_events_from_text(user_input, today_date):
    prompt = f"""
    1. Extract the date from the following input: {user_input} and today's date: {today_date}.
       - If you don't find an explicit date, the user_input could contain phrases like 'Today', 'Tomorrow', 'Next Thursday'. In such cases, calculate the date based on today_date.
       - If no date is mentioned, assume today's date.

    2. Extract all events from the following text: {user_input}.

    - Each event should include:
      - A start_time in the format 'YYYY-MM-DD HH:MM' (24-hour format).
      - An end_time minute in the format 'YYYY-MM-DD HH:MM' (end_time is start_time + 1 hour if no end_time is provided).
      - end_time = end_time - 1 minute
      - A description of the event.

    - ONLY return the output in the following structure as a **Python list of dictionaries**, without additional explanations or comments:
    [
      {{'start_time': 'YYYY-MM-DD HH:MM', 'end_time': 'YYYY-MM-DD HH:MM', 'description': 'event details'}},
      {{'start_time': 'YYYY-MM-DD HH:MM', 'end_time': 'YYYY-MM-DD HH:MM', 'description': 'event details'}},
      ...
    ]

    - Do not include any additional explanations, comments, or text outside of the Python list of dictionaries.
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


def create_ics(events):
    cal = Calendar()

    # Loop through each event in the list
    for my_event in events:
        e = Event()

        # Parse the start and end times
        e.begin = datetime.datetime.strptime(my_event['start_time'], '%Y-%m-%d %H:%M').replace(tzinfo=ZoneInfo('America/New_York'))
        e.end = datetime.datetime.strptime(my_event['end_time'], '%Y-%m-%d %H:%M').replace(tzinfo=ZoneInfo('America/New_York'))

        # Add description to the event
        e.name = my_event['description']

        # Add the event to the calendar
        cal.events.add(e)

    # Write the calendar to an ICS file
    with open('schedule.ics', 'w') as my_file:
        my_file.writelines(cal.serialize_iter())

if __name__ == "__main__":
    today_date = datetime.date.today()
    user_input = "Today I need to study for the COP exam I will start at 8 AM and will study 6 hours, then I will have dinner with my family at 7 PM"
    print(today_date)
    # Getting the list of events
    events = get_events_from_text(user_input, today_date)
    create_ics(events)

    # If valid, print the list of events
    #if events:
       # print(events)

    for event in events:
        print(event)

