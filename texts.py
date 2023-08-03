import requests
import json
import io
import os


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def TextReader(
    bluescape_API_version,
    bluescape_workspaceId,
    bluescape_portal,
    bluescape_token,
    miro_text_url,
    miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Text"
    )

    bluescape_the_request = requests.get(
        bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )

    bluescape_json_response = bluescape_the_request.json()

    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currenttext = data["text"]
        bluescape_currenttextFontSize = data["style"]["fontSize"]
        bluescape_currentX = data["transform"]["x"]
        bluescape_currentY = data["transform"]["y"]
        colorNotSet = True
        try:
            for subdata in data["blocks"]:
                for subdata2 in subdata["content"]:
                    bluescape_currentcolor = rgb_to_hex(
                        subdata2["span"]["color"]["r"],
                        subdata2["span"]["color"]["g"],
                        subdata2["span"]["color"]["b"],
                    )
                    colorNotSet = False
        except TypeError as e:
            if colorNotSet:
                bluescape_currentcolor = rgb_to_hex(
                    data["style"]["color"]["r"],
                    data["style"]["color"]["g"],
                    data["style"]["color"]["b"],
                )
        except KeyError as e:
            if colorNotSet:
                bluescape_currentcolor = rgb_to_hex(
                    data["style"]["color"]["r"],
                    data["style"]["color"]["g"],
                    data["style"]["color"]["b"],
                )
        miro_payload = {
            "data": {"content": bluescape_currenttext},
            "position": {"x": bluescape_currentX, "y": bluescape_currentY},
            "style": {
                "fontSize": bluescape_currenttextFontSize,
                "color": bluescape_currentcolor,
            },
        }

        requests.post(url=miro_text_url, json=miro_payload, headers=miro_headers)
    print(f"\nUploaded {count} Texts")
