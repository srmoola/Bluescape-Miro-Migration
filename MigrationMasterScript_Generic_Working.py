# Python Code (python 3.5+)
import canvas
import images
import documents
import texts
import notecards
import urls
import tokens
import embeds

"""
Required modules:
   requests 2.22.0
"""

bluescape_token = tokens.bluescape


if __name__ == "__main__":
    bluescape_portal = "https://api.apps.us.bluescape.com"
    # bluescape_workspaceId ='IQ7a_L7uMciYf5XH5VrH'
    bluescape_workspaceId = "IjQ19gMfrHfJRxfBL44f"
    #'ECBqXkhTJxQJdocaxXsY'
    bluescape_API_version = "v3"

    # miro_workspace_ID = "uXjVMx0ckRY"
    miro_workspace_ID = "uXjVMxAxZao"
    miro_image_url = urls.ImageUrl(miro_workspace_ID)
    miro_document_url = urls.DocUrl(miro_workspace_ID)
    miro_text_url = urls.TextUrl(miro_workspace_ID)
    miro_note_url = urls.NoteUrl(miro_workspace_ID)
    miro_shape_url = urls.ShapeUrl(miro_workspace_ID)

    miro_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + tokens.miro,
    }

    # Canvas

    canvas.CanvasReader(
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        bluescape_token,
        miro_workspace_ID,
        miro_headers,
    )

    # Embeds
    embeds.embedReads(miro_workspace_ID, miro_headers, bluescape_workspaceId)

    # Image

    images.ImageReader(
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        bluescape_token,
        miro_image_url,
        miro_headers,
    )

    # Documents

    documents.DocumentReader(
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        bluescape_token,
        miro_document_url,
        miro_headers,
    )

    texts.TextReader(
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        bluescape_token,
        miro_text_url,
        miro_headers,
    )

    # Notecard

    notecards.NotecardReader(
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        bluescape_token,
        miro_note_url,
        miro_shape_url,
        miro_headers,
    )


print("All Done!")
