#!/usr/bin/env python3

import json
from typing import List
import requests
import time
import os

from checker.get_slots import get_slots_json

# Your webhook goes here
# See https://api.slack.com/messaging/webhooks
SLACK_WEB_HOOK = os.getenv("SLACK_WEB_HOOK")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# Your address goes here
POSTCODE = os.getenv("POSTCODE")
HOUSENUMBER = os.getenv("HOUSENUMBER")

assert all(
    [SLACK_CHANNEL, SLACK_WEB_HOOK, POSTCODE, HOUSENUMBER]
), "Need to define all variables in environment variables"


def slots_to_text(slots: List):
    text = "There are slots!\n"

    for slot in slots:
        text += f"{slot['dateFormatted']} {slot['startTimeFormatted']}-{slot['endTimeFormatted']}, {slot['serviceCharge']}\n"

    return text


def post_to_slack(text):
    slack_data = {"channel": SLACK_CHANNEL, "username": "webhookbot", "text": text}
    response = requests.post(
        SLACK_WEB_HOOK,
        data=json.dumps(slack_data),
        headers={"Content-Type": "application/json"},
    )


def query_once():
    result_json = get_slots_json(POSTCODE, HOUSENUMBER)
    slots = result_json["slots"]
    available_slots = [
        slot for slot in slots if slot["bookedDeliveries"] < slot["maxDeliveries"]
    ]

    if not available_slots:
        print("All slots are full")
    else:
        print(f"There are slots {available_slots}")
        print(slots_to_text(available_slots))
        post_to_slack(slots_to_text(available_slots))


def main():
    while True:
        try:
            query_once()
        except Exception as e:
            print(f"Exception {e}")
            time.sleep(300)


if __name__ == "__main__":
    main()
