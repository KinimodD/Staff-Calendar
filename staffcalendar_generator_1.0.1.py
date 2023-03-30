# Made by Dominik Dubis with the help of ChatGPT.
# Events are directly from richardchalloner.com/staffcalendar
# This script creates a .ics file which can be imported into any calendar

import requests
from icalendar import Calendar, Event
from datetime import datetime, date, timedelta

# The file size of the .ics file depends on the date range
startDate = "2023-02-27" # Start of calendar generation
endDate = "2023-07-14" # End of calendar generation

url = f"https://www.richardchalloner.com/calendar/api.asp?pid=18&viewid=6&calid=2,3,4&bgedit=false&start={startDate}T00%3A00%3A00&end={endDate}T00%3A00%3A00&_=1678549649244"

response = requests.get(url)
data = response.json()

cal = Calendar()

for event in data:
    cal_event = Event()

    cal_event['summary'] = event['title']

    if 'Location:' in event['desc']:
        location = event['desc'].replace('Location:', '').strip().rstrip('<br>')
    else:
        location = event['desc']
    cal_event['description'] = ''

    cal_event['location'] = location

    if 'All Day' in event['time']:
        start = datetime.strptime(event['start'], '%Y-%m-%d')
        cal_event['dtstart'] = date(start.year, start.month, start.day)
        if 'end' in event:
            end = datetime.strptime(event['end'], '%Y-%m-%d')
            cal_event['dtend'] = date(end.year, end.month, end.day) + timedelta(days=1)
        else:
            cal_event['dtend'] = cal_event['dtstart'] + timedelta(days=1)
        cal_event['dtstart'] = (cal_event['dtstart'] - timedelta(hours=1)).strftime('%Y%m%d')
        cal_event['dtend'] = (cal_event['dtend'] - timedelta(hours=1)).strftime('%Y%m%d')
    else:
        start = datetime.strptime(event['start'], '%Y-%m-%dT%H:%M:%S')
        cal_event['dtstart'] = (start - timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')
        if 'end' in event:
            end = datetime.strptime(event['end'], '%Y-%m-%dT%H:%M:%S')
            cal_event['dtend'] = (end - timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')
        else:
            cal_event['dtend'] = (start - timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')

    cal.add_component(cal_event)

with open('richard_challoner_calendar_mod.ics', 'wb') as f:
    f.write(cal.to_ical())
    # The file might be saved in C:/Users/(your username)/richard_challoner_calendar_mod.ics
