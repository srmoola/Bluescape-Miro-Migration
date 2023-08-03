import concurrent.futures
import canvas
import images
import documents
import texts
import notecards
import urls
import tokens
import embeds

bluescape_token = tokens.bluescape


def MigrationMaster(bluescape, miro):
    bluescape_portal = "https://api.apps.us.bluescape.com"
    bluescape_workspaceId = bluescape
    bluescape_API_version = "v3"
    miro_workspace_ID = miro
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                canvas.CanvasReader,
                bluescape_API_version,
                bluescape_workspaceId,
                bluescape_portal,
                bluescape_token,
                miro_workspace_ID,
                miro_headers,
            ),
            executor.submit(
                embeds.embedReads,
                miro_workspace_ID,
                miro_headers,
                bluescape_workspaceId,
            ),
            executor.submit(
                images.ImageReader,
                bluescape_API_version,
                bluescape_workspaceId,
                bluescape_portal,
                bluescape_token,
                miro_image_url,
                miro_headers,
            ),
            executor.submit(
                documents.DocumentReader,
                bluescape_API_version,
                bluescape_workspaceId,
                bluescape_portal,
                bluescape_token,
                miro_document_url,
                miro_headers,
            ),
            executor.submit(
                texts.TextReader,
                bluescape_API_version,
                bluescape_workspaceId,
                bluescape_portal,
                bluescape_token,
                miro_text_url,
                miro_headers,
            ),
            executor.submit(
                notecards.NotecardReader,
                bluescape_API_version,
                bluescape_workspaceId,
                bluescape_portal,
                bluescape_token,
                miro_note_url,
                miro_shape_url,
                miro_headers,
            ),
        ]

        # Wait for all functions to complete
        concurrent.futures.wait(futures)
