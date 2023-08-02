import requests
import json
import io
import os
import migrationcounter


def DocumentReader(
    bluescape_API_version,
    bluescape_workspaceId,
    bluescape_portal,
    bluescape_token,
    miro_document_url,
    miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Document"
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
        os.path.join("jsonfiles", "Documents.json"), "w", encoding="utf8"
    ) as outfile:
        str_ = json.dumps(
            bluescape_json_response,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
            ensure_ascii=False,
        )
        outfile.write((str_))

    migrationcounter.fileMigrationCounter(
        os.path.join("jsonfiles", "Documents.json"), "FileCounter.txt"
    )

    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currentdocumentURL = data["asset"]["url"]
        bluescape_currentdocumentHeight = data["height"]
        bluescape_currentdocumentX = data["transform"]["x"]
        bluescape_currentdocumentY = data["transform"]["y"]

        miro_payload = {
            "data": {"url": bluescape_currentdocumentURL},
            "position": {
                "origin": "center",
                "x": bluescape_currentdocumentX,
                "y": bluescape_currentdocumentY,
            },
            "geometry": {"height": bluescape_currentdocumentHeight},
        }

        requests.post(url=miro_document_url, json=miro_payload, headers=miro_headers)

    print(f"\nUploaded {count} Documents")
