import requests
import json
import os


def get_home_assistant_url() -> str:
    return os.environ.get("HOME_ASSISTANT_URL")


def get_api_token() -> str:
    return os.environ.get("HOME_ASSISTANT_API_TOKEN")


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {get_api_token()}",
        "Content-Type": "application/json"
    }


def filter_response(response):
    filtered_response = []
    valid_prefixes = ("light", "switch", "scene", "fan",
                      "temperature", "humidity", "sensor", "monetary")

    for item in response:
        if item['entity_id'].startswith(valid_prefixes) is False:
            continue

        if item['attributes'] is None:
            item['attributes'] = {}

        if 'device_class' not in item['attributes']:
            item['attributes']['device_class'] = item['entity_id'].split(".")[
                0]

        if item['entity_id'].startswith("sensor"):
            # Filter out the sensors that are not temperature or humidity
            if item['attributes']['device_class'] not in {"temperature", "humidity", "monetary"} or "steam_wishlist" in item['entity_id']:
                continue

        filtered_response.append({
            "entity_id": item['entity_id'],
            "state": item['state'],
            "friendly_name": item['attributes']['friendly_name'],
            "device_class": item['attributes']['device_class'],
        })

    return filtered_response


def get_devices():
    try:
        response = requests.get(
            f"{get_home_assistant_url()}/api/states", headers=get_headers(), timeout=3)

        if response.status_code == 200:
            response_json = response.json()
            filtered_response = filter_response(response_json)
            return filtered_response
        else:
            print(f"Error: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        return []


def toggle_device_state(entity_id, device_class, state):
    try:
        action = "turn_on" if state == "on" else "turn_off"
        data = {
            "entity_id": entity_id,
        }
        response = requests.post(
            f'{get_home_assistant_url()}/api/services/{device_class}/{action}', headers=get_headers(), data=json.dumps(data), timeout=5)

        if response.status_code == 200:
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        return False
