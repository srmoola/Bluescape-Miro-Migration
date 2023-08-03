import requests
import json
import io
import os


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rgb_to_string(r, g, b):
    colorstring = "yellow"
    if r == 254 and g == 232 and b == 108:
        colorstring = "yellow"
    elif r == 51 and g == 142 and b == 255:
        colorstring = "blue"
    elif r == 89 and g == 212 and b == 180:
        colorstring = "green"
    elif r == 255 and g == 164 and b == 107:
        colorstring = "orange"
    elif r == 255 and g == 110 and b == 110:
        colorstring = "red"
    return colorstring


def bluescapeShapeConvert(miro_shape):
    if "triangle" in miro_shape:
        return "triangle"
    elif "arrow" in miro_shape:
        return "right_arrow"
    elif "star" in miro_shape:
        return "star"
    else:
        return miro_shape


def NotecardReader(
    bluescape_API_version,
    bluescape_workspaceId,
    bluescape_portal,
    bluescape_token,
    miro_note_url,
    miro_shape_url,
    miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Shape"
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
        bluescape_currenttext = ""
        try:
            bluescape_currenttext = data["text"]
        except:
            pass
        bluescape_currentX = data["transform"]["x"]
        bluescape_currentY = data["transform"]["y"]
        bluescape_currentWidth = data["style"]["width"]
        bluescape_currentheight = data["style"]["height"]
        bluescape_currentcolor = rgb_to_hex(
            data["style"]["fillColor"]["r"],
            data["style"]["fillColor"]["g"],
            data["style"]["fillColor"]["b"],
        )
        bluescape_currenttextcolor = rgb_to_hex(
            data["textStyle"]["color"]["r"],
            data["textStyle"]["color"]["g"],
            data["textStyle"]["color"]["b"],
        )

        bluescape_currentfontsize = ""
        try:
            for subdata in data["blocks"]:
                for subdata2 in subdata["content"]:
                    bluescape_currentfontsize = subdata2["span"]["fontSize"]
        except:
            bluescape_currentfontsize = data["textStyle"]["fontSize"]

        if (
            data["kind"] == "rectangle"
            and bluescape_currentWidth == bluescape_currentheight
        ):
            bluescape_currentcolor = rgb_to_string(
                data["style"]["fillColor"]["r"],
                data["style"]["fillColor"]["g"],
                data["style"]["fillColor"]["b"],
            )
            miro_payload = {
                "data": {"shape": "square", "content": bluescape_currenttext},
                "style": {"fillColor": bluescape_currentcolor},
                "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                "geometry": {"width": bluescape_currentWidth},
            }

            requests.post(url=miro_note_url, json=miro_payload, headers=miro_headers)

            print(f"\nUploaded {count} Notes")
        #########Shape
        else:
            bluescape_shape = bluescapeShapeConvert(data["kind"])
            if type(bluescape_currentfontsize) == str:
                bluescape_currentfontsize = "144"
            else:
                bluescape_currentfontsize = round(int(bluescape_currentfontsize))
                if bluescape_currentfontsize > 288:
                    bluescape_currentfontsize = "288"

            miro_payload = {
                "data": {"shape": bluescape_shape, "content": bluescape_currenttext},
                "style": {
                    "fontSize": bluescape_currentfontsize,
                    "fillColor": bluescape_currentcolor,
                    "color": bluescape_currenttextcolor,
                },
                "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                "geometry": {
                    "height": bluescape_currentheight,
                    "width": bluescape_currentWidth,
                },
            }
            requests.post(url=miro_shape_url, json=miro_payload, headers=miro_headers)

        print(f"\nUploaded {count} Shapes")
