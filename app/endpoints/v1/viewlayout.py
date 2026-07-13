from fastapi import APIRouter
from app.controllers.v1 import viewlayoutcontroller as viewapi

router = APIRouter(prefix = "/viewly")

ROUTES = [
    # ("/create", viewapi.createBlankView, ["GET"]),
    
    ("/jointblcolor", viewapi.setJoinTblColor, ["GET"]), # Route::any('view/jointblcolor', 'App\Http\Controllers\ModelData\LayoutAPIController@setJoinTblColor');

    # ("/upddatefrmt", viewapi.updateViewDateFormat, ["GET"]), # Route::any('view/upddatefrmt', 'App\Http\Controllers\ModelData\LayoutAPIController@updateViewDateFormat'); 

    # ("/childstatus", viewapi.getViewChildStatus, ["GET"]), # Route::any('layout/options', 'App\Http\Controllers\ModelData\LayoutAPIController@saveLayoutOptions');

    # ("/srchthreshold", viewapi.duplicateFullView, ["GET"]), # Route::any('', 'App\Http\Controllers\ModelData\LayoutAPIController@saveSrchThreshold');


    # ("/savetbldata", viewapi.saveTableData, ["GET"]), # Route::any('layout/cndtcolclr', 'App\Http\Controllers\ModelData\LayoutAPIController@saveConditionalColColor');

    # ("/duplicateitem", viewapi.duplicateItemData, ["GET"]),
    # # ("/group", viewapi.saveUserViewGroup, ["GET"]), # Move To Layout
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)


# Route::any('layout/mergecolumn', 'App\Http\Controllers\ModelData\LayoutAPIController@mergeViewColumn'); ** DB Table Function
# Route::any('layout/getoptions', 'App\Http\Controllers\ModelData\LayoutAPIController@getLayoutOptions'); ** Remove
# Route::any('layout/getview', 'App\Http\Controllers\ModelData\LayoutAPIController@getSaveFilterView'); ** Move To View Filter
# Route::any('layout/reset', 'App\Http\Controllers\ModelData\LayoutAPIController@resetUserViewLayout'); ** Remove
# Route::any('layout/copyfilter', 'App\Http\Controllers\ModelData\LayoutAPIController@copySaveFilterView'); ** Move To View Filter
# Route::any('layout/removeview', 'App\Http\Controllers\ModelData\LayoutAPIController@removeSaveFilterView'); ** Move To View Filter
# Route::any('layout/savedarkmode', 'App\Http\Controllers\ModelData\LayoutAPIController@saveDarkMode'); ** Move To User

# View Column Data
# Route::any('get/stddltemplate', 'App\Http\Controllers\ModelData\LayoutAPIController@getStDdlTemplateList');
# Route::any('status/gettemplate', 'App\Http\Controllers\ModelData\LayoutAPIController@getStatusFromTemplate');
# Route::any('opt/manageitem', 'App\Http\Controllers\ModelData\LayoutAPIController@manageDynamicOPT');
# Route::any('opt/rank', 'App\Http\Controllers\ModelData\LayoutAPIController@manageOptRank');
# Route::any('opt/getdefault', 'App\Http\Controllers\ModelData\LayoutAPIController@getDefaultOpt');
# Route::any('opt/upddefault', 'App\Http\Controllers\ModelData\LayoutAPIController@updateDefaultOptValue');
# Route::any('dd/manageitem', 'App\Http\Controllers\ModelData\LayoutAPIController@manageDyanmicDropdown');
# Route::any('dd/rank', 'App\Http\Controllers\ModelData\LayoutAPIController@manageDyncDdRank');
# Route::any('dd/gettemplate', 'App\Http\Controllers\ModelData\LayoutAPIController@getDropdownFromTemplate');
# Route::any('tinymce/saveimg', 'App\Http\Controllers\ModelData\LayoutAPIController@saveTinyMCEImage');
