import openai #GPT based prompt engineering
from openai import OpenAI
import ast

client = OpenAI()
def rewrite(user_input : str):
    prompt = f"""
    For each of the events extract the following information in a clear format:
    Event number. (Example: "Event 1:")
    - Description: Display the provided description. If no description is given, default to "Busy"
    - Start and End Times:
        If both the start and end times are not provided, default to:
            Start time: 10:00
            End time: 18:00
        - Start time: Display the start time in 'YYYY-MM-DD HH:MM' (24 Hour Format)
        - End time: Display the end time in 'YYYY-MM-DD HH:MM' (24 Hour Format), If no end time is provided, set it to one hour after the start time.
    - Location. If no location is give, default to "None"
    """

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # Get the content of the message
    message_content = completion.choices[0].message.content.strip() # the model create several responses and it choses the first one
    return(message_content)

# if __name__ == "__main__":
#     user_input="Date:12/3/2024. pickleball: 10a-1p, lunch: 1:30p-2:30p, school work: 4p-7p, dinner: 7:30p-8:30p, TV: 8:30p-10p"
#     events = rewrite(user_input)
#     print(type(events))
#     print(events)