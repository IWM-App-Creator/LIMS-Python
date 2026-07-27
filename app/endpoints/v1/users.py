from fastapi import APIRouter
from app.controllers.v1 import usercontroller as usersapi

router = APIRouter(prefix = "/user")

ROUTES = [
    ("/getlist", usersapi.getUserList, ["GET"]),
    ("/getdetail", usersapi.getUserDetail, ["GET"]),
    ("/search", usersapi.searchWSUser, ["GET"]),
    ("/updateprofile", usersapi.updateUserProfile, ["POST"]),
    ("/changepassword", usersapi.changeUserPassword, ["POST"]),
    ("/getlist", usersapi.getUserList, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)

# Route::any('getuserlist', 'App\Http\Controllers\API\UsersAPIController@getUserList');
# Route::any('savelinkuser', 'App\Http\Controllers\API\UsersAPIController@saveLinkedUser');
# Route::any('deletelinkeduser', 'App\Http\Controllers\API\UsersAPIController@deleteLinkedUser');
# Route::any('saveandlinkuser', 'App\Http\Controllers\API\UsersAPIController@saveUserAndLinkToClient');
# Route::any('emailuserdtl', 'App\Http\Controllers\API\UsersAPIController@sendUserEmail');