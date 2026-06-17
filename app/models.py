from sqlalchemy.ext.automap import automap_base
from app.database import engine

AutomapBase = automap_base()
AutomapBase.prepare(autoload_with=engine)

User = AutomapBase.classes.users