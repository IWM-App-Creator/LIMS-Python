class UserProperties:
    def __init__(self):
        self.user_id = 0
        self.first_name = ""
        self.last_name = ""
        self.user_array = []
        self.user_json = {}

userps = UserProperties()


# $userdtlarr = DB::table('systemconfig.users')
#                         ->select('users.*', 'workspace_master.workspace_id', 'workspace_master.workspace_name', 'workspace_master.ws_url', 'workspace_master.schema_name', 'workspace_master.is_setup', 'users_workspace.ws_role_id')
#                         ->leftJoin('systemconfig.users_workspace', 'users_workspace.user_id', '=', 'users.id')
#                         ->leftJoin('systemconfig.workspace_master', 'workspace_master.workspace_id', '=', 'users_workspace.workspace_id')
#                         ->where('id', $user_id)
#                         ->where('ws_url', $ws_url)
#                         ->where('api_secret', $api_secret)
#                         ->first();