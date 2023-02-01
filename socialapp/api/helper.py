import requests,json,sys
from requests.adapters import HTTPAdapter, Retry


retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])

def is_email_valid(email):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.get(f"https://emailvalidation.abstractapi.com/v1/?api_key=eb5f0467e7be49e89eece580942a3623&email={email}")
        if response.status_code==200:
            data=json.loads(response.content.decode(sys.stdout.encoding))
            format=data['is_valid_format']['value']
            smtp=data['is_smtp_valid']['value']
            return (format,smtp)
        else:
            return (response.status_code)

    except Exception as e:
        print(e)


def get_geo_location():
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.get("https://ipgeolocation.abstractapi.com/v1/?api_key=34ea545ba9f644048b565e88c4cd8b76")
        if response.status_code==200:
            data=json.loads(response.content.decode(sys.stdout.encoding))
            city=data['city']
            country=data['country']
            country_code = data['country_code']
            return (city,country,country_code)
        else:
            return (response.status_code)
    except Exception as e:
        print(e)

def is_holiday(city,country_code):
    if not (city==None or country_code==None):
        location =city+","+country_code
    else:
        return (False,"")
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.get(f"https://timezone.abstractapi.com/v1/current_time/?api_key=e4e1af62e8db4dd2a539f202eac86243&location={location}")
        if response.status_code==200:
            data=json.loads(response.content.decode(sys.stdout.encoding))
            year,month,day=data['datetime'].split(' ')[0].split('-')
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=retries))
            response_1 = s.get(f"https://holidays.abstractapi.com/v1/?api_key=058bf6346c14479d94202d3967ab2b46&country={country_code}&year={year}&month={month}&day={day}")
            if response_1.status_code==200:
                data=json.loads(response_1.content.decode(sys.stdout.encoding))
                if data:
                    holiday=data[0]['name']
                    return (True,holiday)
                else:
                    return (False,"")
            else:
                return (response_1.status_code)

        else:
            return (response.status_code)
    except Exception as e:
        print(e)


def user_data(email):
    gl= get_geo_location()
    if  len(gl) == 1:
        city,country,country_code=""
    else:
        city,country,country_code=gl
        holi=is_holiday(city,country_code)
        if len(holi) ==1:
            bool_holi,holi_name=False,""
        else:
            bool_holi,holi_name=holi
    return (city,country,country_code,bool_holi,holi_name)

