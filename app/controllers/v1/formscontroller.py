from app.utils.common import JSONResponse, Request, RequestData, raiseAPIError, raiseInvalidError
from app.dbfunctions.logfunctions import saveErrorLogtoDB

# https://testws1.miidata.dev:5173/api/v1/form/getfield?form_id=1
def getDynamicFormField(request: Request):
    try:
        # params = RequestData.params(request)
        # params --> view_name: "labour", "expense", "scopeofwork"
        # params --> item_id: 0, 
        # params --> form_id: 0

        # '110','14','3280','Status','YESNO','0','0','0','','1','925~~926~~927~~','2','0','0','0','2026-08-07 06:16:10'
        # '111','14','3283','Created By','LOOKUP','0','2','0','','1','','3','0','0','0','2026-08-07 06:16:10'
        # '112','14','3284','Created Date','NOW','0','0','0','','1','','4','0','0','0','2026-08-07 06:16:12'
        # '113','14','3291','Title','TEXT','0','0','0','','1','','5','0','0','0','2026-08-07 06:16:12'
        # '114','14','3314','DD Col','DDL','0','0','0','','1','83~~84~~85~~','6','0','0','0','2026-08-07 06:16:13'
        # '115','14','3315','Num Col','NUMBER','1','0','0','','1','','7','0','0','0','2026-08-07 06:16:14'
        # '119','14','3319','Assign People','FULLNAME','0','0','492','','1','','11','0','0','0','2026-08-07 06:16:17'

        form_cols = []
        item = {
            "col_id": 3293, "table_id": 214, "col_name": "python___react_v3_id", "col_alias": "Python - React V3 ID",
            "col_type":	"NUMBER", "data_type": "bigint", "col_key": 1,  "length": "11", "is_mandatory": 0,
        }
        form_cols.append(item)
        item = {
            "col_id": 3294, "table_id": 214, "col_name": "status_1", "col_alias": "Status 1",
            "col_type":	"STATUS", "data_type": "int", "col_key": 0,  "length": "4", "is_mandatory": 1,
            "col_data_items": [{"opt_val": "933", "label": "PR3 1", "clrcode": "#E495A5"}, {"opt_val": "934", "label": "PR3 2", "clrcode": "#E495A5"}, {"opt_val": "934", "label": "PR3 3", "clrcode": "#E495A5"}, {"opt_val": "934", "label": "PR3 3", "clrcode": "#E495A5"} ]
        }
        form_cols.append(item)
        item = {
            "col_id": 3312, "table_id": 214, "col_name": "label", "col_alias": "Label",
            "col_type":	"TEXT", "data_type": "varchar", "col_key": 0,  "length": "45", "is_mandatory": 1,
        }
        form_cols.append(item)
        item = {
            "col_id": 3313, "table_id": 214, "col_name": "show_hide_setting_id", "col_alias": "SH Setting ID",
            "col_type":	"DISPLAYAS", "data_type": "bigint", "col_key": 0,  "length": "11", "is_mandatory": 1, 
            "lookup_colid": 3040, "lookup_colnm": "lj1.title"
        }
        form_cols.append(item)
        item = {
            "col_id": 3022, "table_id": 214, "col_name": "yn_1", "col_alias": "Yes No",
            "col_type":	"YN_INT", "data_type": "int", "col_key": 0,  "length": "1", "is_mandatory": 1,
            "col_data_items": [{"opt_val": "1", "label": "YES", "clrcode": "#10b759"}, {"opt_val": "0", "label": "No", "clrcode": "#c66565"}]
        }
        form_cols.append(item)
        item = {
            "col_id": 3023, "table_id": 214, "col_name": "tf_1", "col_alias": "True False",
            "col_type":	"TF_INT", "data_type": "tinyint", "col_key": 0,  "length": "1", "is_mandatory": 1,
            "col_data_items": [{"opt_val": "1", "label": "True", "clrcode": "#10b759"}, {"opt_val": "0", "label": "False", "clrcode": "#c66565"}]
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