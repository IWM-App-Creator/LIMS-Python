from app.utils.common import JSONResponse, Request, RequestData, raiseAPIError, raiseInvalidError
from app.dbfunctions.logfunctions import saveErrorLogtoDB

# https://testws1.miidata.dev:5173/api/v1/form/getfield?form_id=1
def getDynamicFormField(request: Request):
    try:
        # params = RequestData.params(request)
        # params --> view_name: "labour", 
        # params --> item_id: 0, 
        # params --> form_id: 0
        form_cols = []
        item = {
            "col_id": "3312",
            "table_id": "214",
            "col_name":	"label",
            "col_alias": "Label",
            "col_type":	"TEXT",
            "data_type": "varchar",
            "col_key": 0,
            "length": "45",
            "is_mandatory": 0,
        }
        form_cols.append(item)

        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Form Field",
                "form_id": 1,
                "form_name": "Python - React V1 Form",
                "form_cols": form_cols,
                # //form_meta, form_cols, output_type, dync_cat_id, is_delete, created_by, is_metadata, created_date
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)