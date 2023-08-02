import requests
import json
import io
import os


def ImageReader(
    bluescape_API_version,
    bluescape_workspaceId,
    bluescape_portal,
    bluescape_token,
    miro_image_url,
    miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Image"
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
        os.path.join("jsonfiles", "Images.json"), "w", encoding="utf8"
    ) as outfile:
        str_ = json.dumps(
            bluescape_json_response,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
            ensure_ascii=False,
        )
        outfile.write((str_))

        count = 0
        for data in bluescape_json_response["data"]:
            count = count + 1
            bluescape_currentimageURL = data["asset"]["url"]
            bluescape_currentimageHeight = data["boundingBox"]["height"]
            bluescape_currentX = data["transform"]["x"]
            bluescape_currentY = data["transform"]["y"]

            miro_payload = {
                "data": {"url": bluescape_currentimageURL},
                "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                "geometry": {"height": bluescape_currentimageHeight},
            }
            requests.post(url=miro_image_url, json=miro_payload, headers=miro_headers)

        print(f"\nUploaded {count} Images")
