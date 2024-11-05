import ics
from ics import Calendar, Event #create files
import datetime as dt
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

def create_main_ics(events: list, end_date: datetime):
    cal = Calendar()
    
    # Calculate the number of weeks until the end_date
    for my_event in events:
        start_time = datetime.strptime(my_event['start_time'], '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(my_event['end_time'], '%Y-%m-%d %H:%M')
        
        # Create weekly occurrences until the specified end date
        while start_time <= end_date:
            # Create an instance of the event
            e = Event()
            e.begin = start_time
            e.end = end_time
            e.name = my_event['description']
            
            # Add the event to the calendar
            cal.events.add(e)
            
            # Move to the next week
            start_time += timedelta(weeks=1)
            end_time += timedelta(weeks=1)

    # Write the calendar to an ICS file
    with open('main_schedule.ics', 'w') as my_file:
        my_file.writelines(cal.serialize_iter())

# events=[{'start_time': '2024-11-04 19:00', 'end_time': '2024-11-04 20:00', 'description': 'Meeting', 'location': None}, {'start_time': '2024-11-05 18:00', 'end_time': '2024-11-05 21:00', 'description': 'Class', 'location': None}, {'start_time': '2024-11-06 10:00', 'end_time': '2024-11-06 18:00', 'description': 'Work on project', 'location': None}, {'start_time': '2024-11-07 18:00', 'end_time': '2024-11-07 21:00', 'description': 'Class', 'location': None}, {'start_time': '2024-11-08 10:00', 'end_time': '2024-11-08 18:00', 'description': 'Work on the project', 'location': None}, {'start_time': '2024-11-09 10:00', 'end_time': '2024-11-09 18:00', 'description': "It's weekend so chill.", 'location': None}, {'start_time': '2024-11-10 10:00', 'end_time': '2024-11-10 18:00', 'description': "It's weekend so chill.", 'location': None}]

# if __name__ == "__main__":
#     end_date = datetime(2024, 12, 3)
#     create_main_ics(events,end_date)