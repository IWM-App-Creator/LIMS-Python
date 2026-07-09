from fastapi import APIRouter
from app.controllers.v1 import dbtablecontroller as tableapi

router = APIRouter(prefix = "/dbtable")

ROUTES = [
    ("/gettbls", tableapi.getDBTableList, ["GET"]),
    ("/getcols", tableapi.getDBTableColumns, ["GET"]),
    ("/updatetbl", tableapi.updateDBTableAlias, ["GET"]),
    ("/renamecol", tableapi.updateDBTblColAlias, ["GET"]),
    ("/addcol", tableapi.addDynamicColumn, ["GET"]),
    ("/updatecol", tableapi.updateDBTableColumn, ["GET"]),
    ("/removecol", tableapi.removeDBTableColumn, ["GET"]),
    ("/getdesc", tableapi.getDBTableDesc, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)

# Route::any('dbtable/getlist', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTableList');
# Route::any('dbtable/getcol', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTableColumns');
# Route::any('dbtable/datacnt', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTableDataCount');
# Route::any('refreshtblcol', 'App\Http\Controllers\ModelData\DBTablesAPIController@singleRefreshTableCols');
# Route::any('cron/savetblcol', 'App\Http\Controllers\ModelData\DBTablesAPIController@saveTableColumnsCron');
# Route::any('dbtables/update', 'App\Http\Controllers\ModelData\DBTablesAPIController@updateDBTableAlias');
# Route::any('dbcol/rename', 'App\Http\Controllers\ModelData\DBTablesAPIController@updateDBTblColAlias');
# Route::any('dbcol/update', 'App\Http\Controllers\ModelData\DBTablesAPIController@updateDBTableColumn');
# Route::any('dbcol/remove', 'App\Http\Controllers\ModelData\DBTablesAPIController@removeDBTableColumn');

# Route::any('dbtable/gettmpcat', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTemplateCategory');
# Route::any('dbtable/createsql', 'App\Http\Controllers\ModelData\DBTablesAPIController@getCreateTableQuery');
# Route::any('dbtable/savetblsql', 'App\Http\Controllers\ModelData\DBTablesAPIController@saveCreateTableQuery');
# Route::any('dbtable/gettemplates', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTableTemplates');
# Route::any('dbtable/savetmplt', 'App\Http\Controllers\ModelData\DBTablesAPIController@saveDBTableTemplate');
# Route::any('dbtable/getdesc', 'App\Http\Controllers\ModelData\DBTablesAPIController@getDBTableDesc');

