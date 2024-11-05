import datetime as dt
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
#FUNCTIONS
from Closest_Future_Date import cfd
from Rewrite import rewrite
from Extract_Events import get_events_from_text
from Write_ICS import create_main_ics


#Reading Data
data = pd.read_excel("data.xlsx")
data= data.drop("Timestamp",axis=1)
#Changind Column names
Col_names=["email","DOB","gender","term","monday","tuesday","wednesday","thursday",
           "friday","saturday","sunday","socialtime_monday","socialtime_tuesday","socialtime_wednesday",
           "socialtime_thursday","socialtime_friday","socialtime_saturday","socialtime_sunday",
           "commute_to_work","commute_to_university","other_Commute",
           "work_break","study_break","other_Break","sleeptime"]
data.columns=Col_names

#Main Schedule Time Frame
today_date = dt.date.today()
no_month = 1 #Number of months that I want the main schedule to be the same
end_main_schedule_date = today_date + relativedelta(months=no_month)
end_main_schedule_date = datetime.combine(end_main_schedule_date, datetime.min.time()) #I could ask the user to write a exact end date


#Create user input string
user_input_raw = str()
for i in range(4,11):
    user_input_raw = user_input_raw + str(cfd(Col_names[i],today_date)) + " : " + str(data.iloc[3, i]) + ".\n"
print(user_input_raw)

#Rewrite user input
user_input=rewrite(user_input_raw)

#Dictionary of events
events=get_events_from_text(user_input)
print(events)

create_main_ics(events,end_main_schedule_date)

