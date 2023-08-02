import requests
import pprint
import tokens

"""
Required modules:
   requests 2.22.0
"""

token = tokens.bluescape

if __name__ == "__main__":
    portal = "https://api.apps.us.bluescape.com"
    workspaceId = "IjQ19gMfrHfJRxfBL44f"
    API_version = "v3"

    # Get all the images from a workspace

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

    pprint.pprint(json_response)
