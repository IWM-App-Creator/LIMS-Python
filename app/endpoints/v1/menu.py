from fastapi import APIRouter
from app.controllers.v1 import menucontroller as menuapi

router = APIRouter(prefix = "/menu")

ROUTES = [
    ("/get", menuapi.getUserMenu, ["GET"]),
    ("/save", menuapi.saveUserMenu, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)


# Route::any('menu/get', 'App\Http\Controllers\ModelData\UserMenuAPIController@getMenuList');
# Route::any('menu/save', 'App\Http\Controllers\ModelData\UserMenuAPIController@saveUserMenu');
# Route::any('menu/update', 'App\Http\Controllers\ModelData\UserMenuAPIController@updateUserMenu');
# Route::any('menu/sort', 'App\Http\Controllers\ModelData\UserMenuAPIController@saveMenuSorting');
# Route::any('menu/remove', 'App\Http\Controllers\ModelData\UserMenuAPIController@removeUserMenu');

# Route::any('menucentre/save', 'App\Http\Controllers\ModelData\UserMenuAPIController@saveMenuCentre');
# Route::any('menucentre/setactive', 'App\Http\Controllers\ModelData\UserMenuAPIController@setMenuCentreActive');
# Route::any('menucentre/reset', 'App\Http\Controllers\ModelData\UserMenuAPIController@resetMenuCentre');
# Route::any('menucentre/copymenu', 'App\Http\Controllers\ModelData\UserMenuAPIController@copyMenuCentre');

# Route::any('menu/geticons', 'App\Http\Controllers\ModelData\UserMenuAPIController@getIcons');