import urllib3
import requests
import json


def make_request(endpoint=None, data={}, auth=None, type_of_call="GET", BASE_URL=None):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if type_of_call == "DELETE":
        do_request = requests.delete
    elif type_of_call == "POST":
        do_request = requests.post
    elif type_of_call == "PATCH":
        do_request = requests.patch
    elif type_of_call == "PUT":
        do_request = requests.put
    else:
        do_request = requests.get

    headers = {}

    if auth:
        headers["Authorization"] = auth

    headers["Content-type"] = "application/json"
    data = json.dumps(data)

    url = f"{BASE_URL}/{endpoint}"

    if type_of_call != "GET":
        response = do_request(url, headers=headers, data=data, verify=False)
    else:
        response = do_request(url, headers=headers, verify=False)

    if response.status_code == 401:
        return False, "Unable to Authorise admin user"

    http_status = str(response.status_code)[0]

    # In case server completely down or crashed
    if http_status == "5":
        try:
            response = response.text
        except Exception:
            pass
        return False, response

    if type_of_call == "DELETE" and http_status == "2":
        # since the response if empty in this case
        return True, None

    content_type = response.headers.get("Content-Type")
    if content_type in ["application/json", "application/json; charset=utf-8"]:
        try:
            json_response = json.loads(response.text)
        except Exception as e:
            return False, str(e)

        if http_status != "2":
            return False, json_response

        return True, json_response
    else:
        return True, response.text
