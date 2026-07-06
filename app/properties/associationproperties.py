from contextvars import ContextVar

class AssociationProperties:

    def __init__(self):
        self.associations_id = ContextVar("associations_id", default = 0)
        self.designation_id = ContextVar("designation_id", default = 0)

associationps = AssociationProperties()