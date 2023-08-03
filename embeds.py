import requests
import pprint
import tokens
import io
import os
import json


def embedReads(miro_workspace_ID, miro_headers, bluescape_workspaceId):
    token = tokens.bluescape

    portal = "https://api.apps.us.bluescape.com"
    workspaceId = bluescape_workspaceId
    API_version = "v3"

    miro_frame_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/embeds"
    )

    API_endpoint = (
        "/" + API_version + "/workspaces/" + workspaceId + "/elements?type=Browser"
    )

    the_request = requests.get(
        portal + API_endpoint,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
    )

    json_response = the_request.json()

    # with io.open(
    #     os.path.join("jsonfiles", "Embeds.json"), "w", encoding="utf8"
    # ) as outfile:
    #     str_ = json.dumps(
    #         json_response,
    #         indent=4,
    #         sort_keys=True,
    #         separators=(",", ": "),
    #         ensure_ascii=False,
    #     )
    #     outfile.write((str_))

    count = 0
    for data in json_response["data"]:
        count += 1
        frame_width = data["boundingBox"]["width"]
        frame_x = data["boundingBox"]["x"]
        frame_y = data["boundingBox"]["y"]
        frame_url = data["url"]

        miro_payload = {
            "data": {
                "url": frame_url,
                "previewUrl": frame_url,
                "mode": "inline",
            },
            "position": {"x": frame_x, "y": frame_y},
            "geometry": {"width": frame_width},
        }

        requests.post(url=miro_frame_url, json=miro_payload, headers=miro_headers)

    print(f"\nUploaded {count} Embeds")
