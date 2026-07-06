from fastapi import APIRouter
from app.controllers.v1 import viewcontroller as viewapi

router = APIRouter(prefix = "/view")

ROUTES = [
    ("/create", viewapi.createBlankView, ["GET"]),
    ("/getlist", viewapi.getViewList, ["GET"]),
    ("/getdata", viewapi.getViewData, ["GET"]),
    ("/childstatus", viewapi.getViewChildStatus, ["GET"]),
    ("/duplicate", viewapi.duplicateFullView, ["GET"]),

    ("/savetbldata", viewapi.saveTableData, ["GET"]),
    ("/duplicateitem", viewapi.duplicateItemData, ["GET"]),

    # ("/group", viewapi.saveUserViewGroup, ["GET"]), # Move To Layout

    ("/lookupdata", viewapi.getLookupData, ["GET"]),
    ("/filterdata", viewapi.getDataForFilter, ["GET"]),
    ("/getquery", viewapi.getRawViewQuery, ["GET"]),
    ("/checkurl", viewapi.getViewURL, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)

# Route::any('view/getids', 'App\Http\Controllers\ModelData\DynamicViewAPIController@getPrimaryKeyIds');

# Route::any('view/share', 'App\Http\Controllers\ModelData\DynamicViewAPIController@saveViewShare');
# Route::any('view/savecatdata', 'App\Http\Controllers\ModelData\DynamicViewAPIController@saveViewCatData');
# Route::any('custview/savecatdata', 'App\Http\Controllers\ModelData\DynamicViewAPIController@saveCustomViewCatData');
# Route::any('view/getcols', 'App\Http\Controllers\ModelData\DynamicViewAPIController@getViewColumns');
# Route::any('view/itemremrst', 'App\Http\Controllers\ModelData\DynamicViewAPIController@itemRemoveRestore');
# Route::any('view/resetall', 'App\Http\Controllers\ModelData\DynamicViewAPIController@resetAllDynamicView');
# Route::any('view/getcharts', 'App\Http\Controllers\ModelData\DyncViewChartAPIController@getViewChart');

# Route::any('view/setdisplayas', 'App\Http\Controllers\ModelData\DynamicViewAPIController@setDisplayasCol');
# Route::any('view/enabledeljointbl', 'App\Http\Controllers\ModelData\DynamicViewAPIController@enableDisableJoinTblDelete');
# Route::any('endpoint/getdyncactions', 'App\Http\Controllers\ModelData\DynamicViewAPIController@getEndPointDyncActions');
# Route::any('view/savechild', 'App\Http\Controllers\ModelData\DynamicViewAPIController@saveChildView');
# Route::any('view/childsummary', 'App\Http\Controllers\ModelData\DynamicViewAPIController@saveChildSummary');
# Route::any('view/makehidden', 'App\Http\Controllers\ModelData\DynamicViewAPIController@makeHiddenColumn');
# Route::any('layout/mergecolumn', 'App\Http\Controllers\ModelData\LayoutAPIController@mergeViewColumn');
# Route::any('view/jointblcolor', 'App\Http\Controllers\ModelData\LayoutAPIController@setJoinTblColor');
# Route::any('view/upddatefrmt', 'App\Http\Controllers\ModelData\LayoutAPIController@updateViewDateFormat');
# Route::any('view/transfer', 'App\Http\Controllers\ModelData\DynamicFormAPIController@transferViewData');

