import requests
import json
import io
import os


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def CanvasReader(
    bluescape_API_version,
    bluescape_workspaceId,
    bluescape_portal,
    bluescape_token,
    miro_workspace_ID,
    miro_headers,
):
    miro_frame_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/frames"
    )

    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Canvas"
    )

    bluescape_the_request = requests.get(
        bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )

    bluescape_json_response = bluescape_the_request.json()

    with io.open(
        os.path.join("jsonfiles", "Canvas.json"), "w", encoding="utf8"
    ) as outfile:
        str_ = json.dumps(
            bluescape_json_response,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
            ensure_ascii=False,
        )
        outfile.write(str_)

    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currentcanvastitle = data["name"]
        bluescape_currentX = data["boundingBox"]["x"]
        bluescape_currentY = data["boundingBox"]["y"]
        bluescape_currentWidth = data["boundingBox"]["width"]
        bluescape_currentheight = data["boundingBox"]["height"]
        bluescape_currentcolor = rgb_to_hex(
            data["style"]["fillColor"]["r"],
            data["style"]["fillColor"]["g"],
            data["style"]["fillColor"]["b"],
        )
        miro_payload = {
            "data": {"title": bluescape_currentcanvastitle},
            "position": {
                "x": bluescape_currentX + (bluescape_currentWidth / 2),
                "y": bluescape_currentY + (bluescape_currentheight / 2.5),
            },
            "style": {
                "fillColor": bluescape_currentcolor,
            },
            "geometry": {
                "width": bluescape_currentWidth,
                "height": bluescape_currentheight,
            },
        }
        requests.post(url=miro_frame_url, json=miro_payload, headers=miro_headers)
    print(f"\nUploaded {count} Canvases")
