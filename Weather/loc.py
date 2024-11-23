from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable
from timezonefinder import TimezoneFinder
import json, requests


def location(area):
    location = Nominatim(user_agent="geo_location")
    getloc = location.geocode(area)
    zone = TimezoneFinder()
    timezone = zone.timezone_at(lng=getloc.longitude, lat=getloc.latitude)
    add = getloc.address
    long = getloc.longitude
    lat = getloc.latitude
    tz = timezone
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "is_day", "precipitation"],
        "daily": ["sunrise", "sunset"],
        "timezone": "auto",
        "forecast_days": 1,
    }
    responses = requests.get(url, params=params, verify=False)
    response = responses.content
    response1 = json.loads(response.decode("utf-8"))
    temp = response1["current"]["temperature_2m"]
    isaday = response1["current"]["is_day"]
    sunrise = " ".join((response1["daily"]["sunrise"])[0].split("T"))
    sunset = " ".join((response1["daily"]["sunset"])[0].split("T"))

    return (add, long, lat, tz, temp, isaday, sunrise, sunset)
