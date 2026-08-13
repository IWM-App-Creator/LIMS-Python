from fastapi import APIRouter
from app.controllers.v1 import notificationcontroller as notiapi

router = APIRouter(prefix = "/notification")

ROUTES = [
    ("/counts", notiapi.getNotiCountByUserID, ["GET"]),
    ("/get", notiapi.getUserNotifications, ["GET"]),
    ("/update", notiapi.markNotificationRead, ["GET"]), # Read, Archive, Delete
    ("/accept", notiapi.markNotificationRead, ["GET"]), # Widget, Menu & Filters (Filter : send to dashboard)

    #TO Remove
    ("/markread", notiapi.markNotificationRead, ["GET"]),
    ("/markold", notiapi.markNotificationOld, ["GET"]),
    ("/delete", notiapi.markNotificationDeleted, ["GET"]),
    ("/archive", notiapi.markNotificationArchive, ["GET"]),
    ("/counts", notiapi.getNotiCountByUserID, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)



# Route::any('notifications/getlist', 'App\Http\Controllers\ModelData\NotificationsAPIController@getUserNotifications');
# Route::any('notifications/markread', 'App\Http\Controllers\ModelData\NotificationsAPIController@markNotificationRead');
# Route::any('notifications/markold', 'App\Http\Controllers\ModelData\NotificationsAPIController@markNotificationOld');
# Route::any('notifications/delete', 'App\Http\Controllers\ModelData\NotificationsAPIController@markNotificationDeleted');
# Route::any('notifications/archive', 'App\Http\Controllers\ModelData\NotificationsAPIController@markNotificationArchive');
# Route::any('notiview/counts', 'App\Http\Controllers\ModelData\NotificationsAPIController@getNotiCountByUserID');