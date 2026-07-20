from fastapi import APIRouter
from app.controllers.v1 import associationcontroller as associationapi

router = APIRouter(prefix = "/association")

ROUTES = [
    ("/getlist", associationapi.getAssociations, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)


# Route::any('getdesignation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@getWSDesignation');
# Route::any('savedesignation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveWSDesignation');
# Route::any('deletedesignation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@deleteWSDesignation');

# Route::any('ws_association/get', 'App\Http\Controllers\ModelData\WsAssociationAPIController@getWSAssociation');
# Route::any('ws_association/save', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveWSAssociation');
# Route::any('ws_association/delete', 'App\Http\Controllers\ModelData\WsAssociationAPIController@deleteWSAssociation');
# Route::any('ws_association/update_designation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@UpdateAssociationDesignation');

# Route::any('ws_association/saveassodesignation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveWSAssoDesignation');
# Route::any('ws_assocuser/save', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveWSAssociationUser');
# Route::any('ws_assocuser/saveviewteam', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveWSAssociationViewTeam');

# Route::any('association/getusers', 'App\Http\Controllers\ModelData\WsAssociationAPIController@getAssociationUsers');
# Route::any('association/saveviews', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveAssociationView');
# Route::any('association/saveviewassociation', 'App\Http\Controllers\ModelData\WsAssociationAPIController@saveViewAssociation');


# Route::any('ws_assouser/gethelperdata', 'App\Http\Controllers\ModelData\WsAssociationAPIController@getAssociationHelperData');
# Route::any('ws_assouser/getlookupdata', 'App\Http\Controllers\ModelData\WsAssociationAPIController@getWSLookupData');
