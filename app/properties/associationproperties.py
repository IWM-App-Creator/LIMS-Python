from contextvars import ContextVar

class AssociationProperties:

    def __init__(self):
        self.associations_id = ContextVar("associations_id", default = 0)
        self.designation_id = ContextVar("designation_id", default = 0)

        self.user_id = ContextVar("user_id", default = 0)
        self.col_id = ContextVar("col_id", default = 0)
        self.col_p_val = ContextVar("col_p_val", default = 0)

associationps = AssociationProperties()