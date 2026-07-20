from app.dbfunctions.associationfunctions import getAssociationUsers, getAssociationData, getAssociationDesignationData

def getAssociationList(associationps):
    association_data = getAssociationData()
    itm_list = []
    for association in association_data:
        associationps.associations_id.set(association.associations_id)
        row = {
            "associations_id": association.associations_id,
            "name": association.name,
            "table_id": association.table_id,
            "table_alias": association.table_alias,
            "table_name": association.table_name,
            "col_id": association.col_id,
            "col_name": association.col_name,
            "col_alias": association.col_alias,
            "lookup_col_id": association.lookup_col_id,
            "lookup_col_name": association.lookup_col_name,
            "lookup_col_alias": association.lookup_col_alias,
            "full_access": association.full_access,
            "inter_msg": association.inter_msg,
            "views_json": association.views_json,
        }
        desig_list = getAssociationDesignationData(associationps)
        desig_data = []
        for desig in desig_list:
            desigrow = {
                "srno": desig.srno,
                "designation_id": desig.designation_id,
                "designation_name": desig.designation_name,
                "is_owner": desig.is_owner,
                "is_edit": desig.is_edit,
                "is_view": desig.is_view,
                "is_noaccess": desig.is_noaccess,
                "is_notify": desig.is_notify
            }
            desig_data.append(desigrow)
        row["designations"] = desig_data
        itm_list.append(row)
    return itm_list

def getViewIdByAssociation(associationps):
    associationps.is_distinct.set(1)
    associationps.fetch_single.set(0)
    view_ids = []
    getAssociationUsers(associationps)
    for assouser in associationps.ass_users_data.get():
        access_json = assouser.access_json
        if access_json not in (None, "", {}):
            dyncviews = access_json.get("dyncviews", None)
            if dyncviews not in (None, ""):
                dyncviews = str(dyncviews)
                dyncviews = [int(x) for x in dyncviews.split(",") if x.strip()]
                view_ids.extend(dyncviews)
    view_ids = list(set(view_ids))
    associationps.dyncviews.set(view_ids)
    print("dyncviews --> ", associationps.dyncviews.get())

def getCustomViewByAssociation(associationps):
    associationps.is_distinct.set(1)
    associationps.fetch_single.set(0)
    cust_view_ids = []
    cust_view_ids.append(-1)
    getAssociationUsers(associationps)
    for assouser in associationps.ass_users_data.get():
        access_json = assouser.access_json
        if access_json not in (None, "", {}):
            custlink = access_json.get("custlink", None)
            if custlink not in (None, ""):
                custlink = str(custlink)
                custlink = [int(x) for x in custlink.split(",") if x.strip()]
                cust_view_ids.extend(custlink)
    cust_view_ids = list(set(cust_view_ids))
    associationps.custlink.set(cust_view_ids)
    print("custlink --> ", associationps.custlink.get())

def getMenuCenterByAssociation(associationps):
    associationps.is_distinct.set(1)
    associationps.fetch_single.set(0)
    menucntr_ids = []
    getAssociationUsers(associationps)
    for assouser in associationps.ass_users_data.get():
        access_json = assouser.access_json
        if access_json not in (None, "", {}):
            menucntr = access_json.get("menuscentre", None)
            if menucntr not in (None, ""):
                menucntr = str(menucntr)
                menucntr = [int(x) for x in menucntr.split(",") if x.strip()]
                menucntr_ids.extend(menucntr)
    menucntr_ids = list(set(menucntr_ids))
    associationps.menucntr.set(menucntr_ids)
    print("menucntr --> ", associationps.menucntr.get())