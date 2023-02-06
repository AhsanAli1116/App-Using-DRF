import json
import sys

import requests
from requests.adapters import HTTPAdapter, Retry
from rest_framework_simplejwt.tokens import RefreshToken

retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])


def is_email_valid(email):
    """Return: boolean values if email format and smtp is valid
    values: format, smtp
    It checks the format and smtp of email using abstract api.
    """

    try:
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=retries))
        response = s.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key=b7ebc0281bb34dcb8c6e0aa171f0dc8a&email={email}"
        )
        if response.status_code == 200:
            data = json.loads(response.content.decode(sys.stdout.encoding))
            format = data["is_valid_format"]["value"]
            smtp = data["is_smtp_valid"]["value"]
            return (format, smtp)
        else:
            return response.status_code

    except Exception as e:
        print(e)


def get_geo_location():
    """Returns: city,country,country_code
    It returns user city, countryname and country_code
    using abstract ipgeolocation api.
    """
    try:
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=retries))
        response = s.get(
            "https://ipgeolocation.abstractapi.com/v1/?api_key=cfce2b75a512448189caa9a69f8db160"
        )
        if response.status_code == 200:
            data = json.loads(response.content.decode(sys.stdout.encoding))
            city = data["city"]
            country = data["country"]
            country_code = data["country_code"]
            return (city, country, country_code)
        else:
            return response.status_code
    except Exception as e:
        print(e)


def is_holiday(city, country_code):
    """Returns: Boolean and String values
    values: boolean,holiday
    It returns the holiday name of the user country
    on his/her registration data.
    """

    if not (city is None or country_code is None):
        location = city + "," + country_code
    else:
        return (False, "")
    try:
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=retries))
        response = s.get(
            f"https://timezone.abstractapi.com/v1/current_time/?api_key=57ce3f044491430eac416bc6462d2913&location={location}"
        )
        if response.status_code == 200:
            data = json.loads(response.content.decode(sys.stdout.encoding))
            year, month, day = data["datetime"].split(" ")[0].split("-")
            s = requests.Session()
            s.mount("https://", HTTPAdapter(max_retries=retries))
            response_1 = s.get(
                f"https://holidays.abstractapi.com/v1/?api_key=b84bb02b6e384035a38d8bff5e518a59&country={country_code}&year={year}&month={month}&day={day}"
            )
            if response_1.status_code == 200:
                data = json.loads(
                    response_1.content.decode(sys.stdout.encoding)
                )
                if data:
                    holiday = data[0]["name"]
                    return (True, holiday)
                else:
                    return (False, "")
            else:
                return response_1.status_code

        else:
            return response.status_code
    except Exception as e:
        print(e)


def user_data(email):
    """Returns: dictionary object
    It is used to manipulate the data of user
    This function is used as wrapper function.
    """

    gl = get_geo_location()
    if type(gl) != tuple:
        city, country, country_code = ""
    else:
        city, country, country_code = gl
        holi = is_holiday(city, country_code)
        if type(holi) != tuple:
            bool_holi, holi_name = False, ""
        else:
            bool_holi, holi_name = holi
    return {
        "city": city,
        "country": country,
        "country_code": country_code,
        "is_holiday": bool_holi,
        "holiday": holi_name,
    }


def get_tokens_for_user(user):
    """Returns: Dictionary object
    This function is a wrapper function
    which returns the user JWT access and
    refresh token.
    """

    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
