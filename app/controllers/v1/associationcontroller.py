from app.utils.common import Request, JSONResponse
from app.helper.associationhelper import getAssociationList
from app.properties.associationproperties import associationps

def getAssociations(request: Request):
    print("getAssociation --> ")
    associations = getAssociationList(associationps)
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "Association List",
            "associations": associations
        }
    )
