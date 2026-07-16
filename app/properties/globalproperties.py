class GlobalProperties:
    def __init__(self):
        # Env Variables
        self.APP_URL = "" #Full URL e.g https://dev-miidata.com.au, https://miidata.io
        self.APP_DOMAIN = "" # Domain e.g dev-miidata.com.au, miidata.io
        
        self.APP_PATH = "" # Full Path TEMPLATES_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.AI_API_URL = ""
        self.ASSET_URL = ""

        self.IS_LOCAL_DEV = "" # Is Local Development
        self.JWT_USER_ID = ""  # Local Dev User ID

        self.MAIL_HOST = "mail.miidata.io"
        self.MAIL_PORT = 587
        self.MAIL_USERNAME = "info@miidata.io"
        self.MAIL_PASSWORD = "G}8oG]6Kmb{K"
        self.MAIL_ENCRYPTION="tls"
        self.MAIL_FROM_ADDRESS = "info@miidata.io"
        self.MAIL_FROM_NAME = "MiiData"

globalps = GlobalProperties()