def ImageUrl(miro_workspace_ID):
    return "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/images"


def DocUrl(miro_workspace_ID):
    return "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/documents"


def TextUrl(miro_workspace_ID):
    return "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/texts"


def NoteUrl(miro_workspace_ID):
    return "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/sticky_notes"


def ShapeUrl(miro_workspace_ID):
    return "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/shapes"
