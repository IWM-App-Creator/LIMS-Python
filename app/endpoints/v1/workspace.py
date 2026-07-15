from fastapi import APIRouter
from app.controllers.v1 import workspacecontroller as wsapi

router = APIRouter(prefix = "/workspace")

ROUTES = [
    ("/isvalidws", wsapi.isWSValid, ["GET"]),
    ("/getlist", wsapi.getWorkspaceList, ["GET"]),

    ("/save", wsapi.saveWorkspace, ["GET"]),
    # ("/activation", wsapi.activationWorkspace, ["GET"]),
    # ("/accept", wsapi.acceptWorkspaceInvitation, ["GET"]),
    # ("/recreate", wsapi.reCreateWSSchema, ["GET"]),
    # ("/remove", wsapi.removeWorkspace, ["GET"]),
    
    # ("/getusers", wsapi.getUserByWorkspace, ["GET"]),
    # ("/inviteuser", wsapi.inviteWorkspaceUser, ["GET"]),
    # ("/removeuser", wsapi.removeWorkspaceUsers, ["GET"]),
    # ("/sendemail", wsapi.sendWSInvEmail, ["GET"]),

    # ("/setactive", wsapi.saveActiveWorkspace, ["GET"]),
    # ("/updusrwsrole", wsapi.updateUserWsRole, ["GET"]),
    # ("/updusrrole", wsapi.updateUserRole, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)


# Route::any('workspace/get', 'App\Http\Controllers\ModelData\WorkspaceAPIController@getWorkspaceList');
# Route::any('workspace/getlist', 'App\Http\Controllers\ModelData\WorkspaceAPIController@getUserWorkspaceList');
# Route::any('workspace/save', 'App\Http\Controllers\ModelData\WorkspaceAPIController@saveWorkspace');
# Route::any('workspace/activation', 'App\Http\Controllers\ModelData\WorkspaceAPIController@activationWorkspace');
# Route::any('workspace/accept', 'App\Http\Controllers\ModelData\WorkspaceAPIController@acceptWorkspaceInvitation');
# Route::any('workspace/recreate', 'App\Http\Controllers\ModelData\WorkspaceAPIController@reCreateWSSchema');
# Route::any('workspace/remove', 'App\Http\Controllers\ModelData\WorkspaceAPIController@removeWorkspace');
# Route::any('workspace/getusers', 'App\Http\Controllers\ModelData\WorkspaceAPIController@getUserByWorkspace');
# Route::any('workspace/removeuser', 'App\Http\Controllers\ModelData\WorkspaceAPIController@removeWorkspaceUsers');
# Route::any('workspace/inviteuser', 'App\Http\Controllers\ModelData\WorkspaceAPIController@inviteWorkspaceUser');
# Route::any('workspace/setactive', 'App\Http\Controllers\ModelData\WorkspaceAPIController@saveActiveWorkspace');
# Route::any('workspace/updusrwsrole', 'App\Http\Controllers\ModelData\WorkspaceAPIController@updateUserWsRole');
# Route::any('users/updusrrole', 'App\Http\Controllers\ModelData\WorkspaceAPIController@updateUserRole');
# Route::any('workspace/sendemail', 'App\Http\Controllers\ModelData\WorkspaceAPIController@sendWSInvEmail');

# Route::any('workspace/addmodule', 'App\Http\Controllers\ModelData\ViewModuleAPIController@addModuleToWorkspace');