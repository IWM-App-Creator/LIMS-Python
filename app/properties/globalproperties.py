class GlobalProperties:
    def __init__(self):
        # Global Variables
        self.user_id = ""
        self.workspace_id = ""
        self.workspace_name = ""
        self.ws_url = ""
        self.schema_name = ""

        # Env Variables
        self.APP_URL = ""
        self.APP_DOMAIN = ""
        self.APP_DOMAIN_FRONT = ""
        self.SESSION_DOMAIN = ""
        self.IS_LOCAL_DEV = ""
        self.JWT_USER_ID = ""
        self.LOCAL_SUBDOMAIN = ""
        self.AI_API_URL = ""
        self.ASSET_URL = ""

globalps = GlobalProperties()