import datetime as dt
from datetime import datetime,timedelta

# Closest Future Date function
def cfd(day: str, date: datetime) -> datetime:
    # Define days of the week for reference
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    # Convert day to lowercase and get the target day index
    #day = day.lower()
    target_day_index = days_of_week.index(day) 
    
    # Get the weekday index of the provided date
    date_day_index = date.weekday()  #0 would be monday - 6 is sunday
    
    # Calculate the number of days to the target day
    delta_to_target_day = (target_day_index - date_day_index) % 7 # how many days from my date to the expected day
    
    # If the target day is today, delta will be 0; otherwise, it will point to the next occurrence
    closest_date = date + timedelta(days=delta_to_target_day)
    
    return closest_date

