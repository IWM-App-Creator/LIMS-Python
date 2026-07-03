class GlobalProperties:
    def __init__(self):
        # Global Variables
        self.user_id = ""
        self.role_id = ""
        self.ws_role_id = ""
        self.workspace_id = ""
        self.workspace_name = ""
        self.ws_url = ""
        self.schema_name = ""

        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.user_settings = {}

        # Env Variables
        self.APP_URL = "" #Full URL e.g https://dev-miidata.com.au, https://miidata.io
        self.APP_DOMAIN = "" # Domain e.g dev-miidata.com.au, miidata.io
        
        self.APP_PATH = "" # Full Path TEMPLATES_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.AI_API_URL = ""
        self.ASSET_URL = ""

        self.IS_LOCAL_DEV = "" # Is Local Development
        self.JWT_USER_ID = ""  # Local Dev User ID

globalps = GlobalProperties()