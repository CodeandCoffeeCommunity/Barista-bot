from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim

import requests


def _url(chapter: str):
    return f"https://api.meetup.com/{chapter}/events"


def get_upcoming_meetup_events(chapter: str):
    """
    request events from Meetup REST API
    """
    response = requests.get(_url(chapter))
    return response.json()


def create_datetime_obj(unix_time: int, time_zone: str):
    """
    returns a timezone aware datetime object
    """

    if len(str(unix_time)) == 13:  # API returns unix time in milliseconds
        unix_time /= 1000.0  # Python handle unix time in secconds

    return datetime.fromtimestamp(unix_time, tz=ZoneInfo(time_zone))


def get_address(lat, lon):
    geolocator = Nominatim(user_agent="discord-meetup-bot")
    location = geolocator.reverse((lat, lon))

    if len(location.address) > 100:
        return location.address[:99]

    return location.address


def fetch_meetup_events_detail(chapter):
    meetup_events = get_upcoming_meetup_events(chapter)

    scheduled_events = {}
    for event in meetup_events:
        start_time = create_datetime_obj(event["time"], event["group"]["timezone"])
        end_time = start_time + timedelta(milliseconds=event["duration"])
        scheduled_event = {
            "name": event["name"],
            # "description": event["description"], # need to fix length issue
            "start_time": start_time,
            "end_time": end_time,
            "location": get_address(event["group"]["lat"], event["group"]["lon"]),
            "description": event["link"],
        }
        scheduled_events[event["id"]] = scheduled_event

    return scheduled_events
