from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.helper.generalfunctions import uploadFile
from app.dbfunctions.logfunctions import saveErrorLogtoDB

async def uploadImage(request: Request):
    print("uploadImage --> ")
    try:
        params = RequestData.params(request)
        tinymce_img = await RequestData.file(request, "tinymce_img")
        if tinymce_img is None or not tinymce_img.filename:
            return raiseInvalidError("Please select an image.", 401)
        itm_image_name = uploadFile(userps.ws_url.get(), "tinymce", tinymce_img)
        if not itm_image_name:
            return raiseInvalidError("Image upload failed.", 500)
        tinymce_img_url = "https://" + userps.req_host.get() + "/wsassets/uploads/" + userps.ws_url.get() + "/tinymce/" + itm_image_name
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Image Uploaded Successfully",
                "tinymce_img_url": tinymce_img_url
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Tinymce", 0, "uploadImage", str(e))
        raiseAPIError(str(e), 500)
