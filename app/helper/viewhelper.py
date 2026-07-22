import json
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.dbfunctions.associationfunctions import getViewAssociationByUser
from app.helper.generalfunctions import sortObjectsByKey, updateNestedJsonVal
from app.properties.dbproperties import dbps
from app.properties.associationproperties import associationps
from app.helper import dbhelper as dbhlp

from app.helper.templatehelper import getPriorityTemplate

class ViewHelper:

    @staticmethod
    def setViewInputParam(viewps, params):
        viewps.view_id.set(params.get("view_id", -1))
        viewps.call_from.set(params.get("call_from", "DynamicView"))
        viewps.tab_id.set(params.get("tab_id", "0"))
        viewps.page_no.set(params.get("page_no", 1))
        viewps.txtsearch.set(params.get("txtsearch", ""))
        viewps.filterqry.set(params.get("filterqry", ""))

    @staticmethod
    def setViewDataProperties(viewps):
        userview = viewps.userview.get()
        viewps.view_id.set(userview.view_id)
        viewps.view_name.set(userview.view_name)
        viewps.view_url.set(userview.url)
        viewps.view_type.set(userview.view_type)
        viewps.view_options.set(userview.view_options)
        viewps.view_cols.set(userview.view_cols)
        viewps.view_joins.set(userview.view_joins)
        viewps.view_child.set(userview.view_child)
        viewps.view_actions.set(userview.view_actions)
        ViewHelper.parseViewOptions(viewps)

    @staticmethod
    def parseViewOptions(viewps):
        viewopt = viewps.view_options.get() or {}
        viewps.table_id.set(viewopt.get("table_id", 0))
        viewps.table_name.set(viewopt.get("table_name", ""))
        viewps.view_qry.set(viewopt.get("view_qry", ""))
        primary_col = viewopt.get("primary_col", "")
        viewps.primary_col.set(primary_col)
        viewps.primary_colnm.set( primary_col.split("|", 1)[1] if "|" in primary_col else "" )
        viewps.delete_col.set(viewopt.get("delete_col", ""))
        viewps.show_deleted.set(viewopt.get("show_deleted", 0))
        viewps.enable_newline.set(viewopt.get("enable_newline", 0))
        viewps.enable_join_save.set(viewopt.get("enable_join_save", 0))
        viewps.is_child_view.set(viewopt.get("is_child_view", 0))
        viewps.enable_child_srch.set(viewopt.get("enable_child_srch", 0))
        viewps.enable_chart.set(viewopt.get("enable_chart", 0))

    @staticmethod
    def setViewTableCols(viewps):
        # Get View Columns
        view_cols = viewps.view_cols.get()
        view_cols = view_cols.get("view_cols", [])
        col_id_arr = []
        for col in view_cols:
            col_id_arr.append(col["col_id"])
        col_id_arr = list(dict.fromkeys(col_id_arr))
        # Get Table Col
        dbps.col_ids.set(col_id_arr)
        dbps.is_del_tbl.set(0)
        dbps.is_del_col.set(0)
        tblcol = getDBTableData(dbps)
        tbl_cols = []
        for col in tblcol:
            col_options = (col.col_options or {}).copy()
            col_options.pop("csv_col_name", None)
            col_options.pop("csv_col_type", None)
            col_options.pop("csv_map_col_nm", None)
            tbl_cols.append({
                "col_id": col.col_id,
                "col_options": col_options
            })
        viewps.tbl_cols.set(tbl_cols)

    @staticmethod
    def setViewLayout(viewps):
        viewlayout = getViewLayoutDataByID(viewps)
        if viewlayout:
            viewps.col_metadata.set(viewlayout.col_metadata)
            viewps.col_colors.set(viewlayout.col_colors)
            viewps.action_group_list.set(viewlayout.action_group_list)
            viewps.user_setting.set(viewlayout.user_setting)

    @staticmethod
    def checkViewAssociation(viewps):
        associationps.user_id.set(userps.user_id.get())
        associationps.view_id.set(viewps.view_id.get())
        assousers = getViewAssociationByUser(associationps)
        # print("assousers --> ", assousers)
        viewps.full_access.set(0)
        viewps.association_qry.set("")
        assocol_ids = []
        qry_alias = "mtbl"
        asso_col = ""
        view_cols = viewps.view_cols.get()
        view_cols = view_cols.get("view_cols", [])
        for assoc in assousers:
            if assoc.full_access == 1:
                viewps.full_access.set(1)
                viewhlp.setHighestPermission(assoc)
            assocol_ids.append(assoc.col_p_val)
        
        if viewps.full_access.get() == 0:
            for assoc in assousers:
                if asso_col:
                    break
                for col in view_cols:
                    if assoc.col_id == col["col_id"]:
                        qry_alias = col["qry_alias"]
                        asso_col = col["col_name"]
                        break
            if assocol_ids:
                viewps.association_qry.set(f"{qry_alias}.{asso_col} IN ({','.join(map(str, assocol_ids))})")

    @staticmethod
    def setHighestPermission(viewps, assoc):
        if viewps.fa_is_owner.get() == 0 and assoc.is_owner > 0:
            viewhlp.copyAssociation(viewps, assoc)
            viewps.fa_is_edit.set(1)
            viewps.fa_is_view.set(1)
            viewps.fa_is_noaccess.set(1)

        elif viewps.fa_is_edit.get() == 0 and assoc.is_edit > 0:
            viewhlp.copyAssociation(viewps, assoc)
            viewps.fa_is_edit.set(assoc.is_edit)
            viewps.fa_is_view.set(1)
            viewps.fa_is_noaccess.set(1)

        elif viewps.fa_is_view.get() == 0 and assoc.is_view > 0:
            viewhlp.copyAssociation(viewps, assoc)
            viewps.fa_is_view.set(assoc.is_view)
            viewps.fa_is_noaccess.set(1)

        elif viewps.fa_is_noaccess.get() == 0 and assoc.is_noaccess > 0:
            viewhlp.copyAssociation(viewps, assoc)
            viewps.fa_is_noaccess.set(assoc.is_noaccess)
    
    @staticmethod
    def copyAssociation(viewps, assoc):
        viewps.fa_asso_id.set(assoc.associations_id)
        viewps.fa_dsgn_id.set(assoc.designation_id)
        viewps.fa_dsgn_nm.set(assoc.designation_name)
        viewps.fa_is_owner.set(assoc.is_owner)
        viewps.fa_is_edit.set(assoc.is_edit)
        viewps.fa_is_view.set(assoc.is_view)
        viewps.fa_is_noaccess.set(assoc.is_noaccess)
        
    @staticmethod
    def setViewSorting(viewps):
        user_setting = viewps.user_setting.get() or {}
        current_tab = f"tab_{viewps.tab_id.get()}"
        tab_setting = user_setting.get(current_tab)
        # print("tab_setting --> ", tab_setting)
        if not tab_setting:
            return
        # Sorting
        # sortby = tab_setting.get("sortby", "")
        # sortorder = tab_setting.get("sortorder", "")

        # if not sortorder:
        #     sortorder = "DESC"
        # viewps.sortby.set(sortby)
        # viewps.sortorder.set(sortorder)
        # sorting = ""
        # if sortby:
        #     tmp_sortby = sortby.split(",")
        #     tmp_sortorder = sortorder.split(",")
        #     sort_parts = []
        #     for i, srt in enumerate(tmp_sortby):
        #         if "FIELD(" in srt:
        #             srt = srt.replace("^^", ",")
        #             srt = srt.split("**")[0]
        #             tmp = srt.split(",")[0].replace("FIELD(", "")
        #             tmp_srt = getSortByColIDName(tmp)
        #             srt = srt.replace(tmp, tmp_srt)
        #         else:
        #             srt = getSortByColIDName(srt)
        #         order = tmp_sortorder[i] if i < len(tmp_sortorder) else "DESC"
        #         sort_parts.append(f"{srt} {order}")
        #     sorting = ", ".join(sort_parts)
        # # Convert list to comma-separated string if needed
        # if isinstance(viewps.sortby.get(), list):
        #     viewps.sortby.set(",".join(viewps.sortby.get()))
        # if isinstance(viewps.sortorder.get(), list):
        #     viewps.sortorder.set(",".join(viewps.sortorder.get()))
        # viewps.sorting.set(sorting)

    @staticmethod
    def setViewPaging(viewps):
        user_setting = viewps.user_setting.get() or {}
        current_tab = f"tab_{viewps.tab_id.get()}"
        tab_setting = user_setting.get(current_tab)
        # print("tab_setting --> ", tab_setting)
        if tab_setting:
            page_size = tab_setting.get("page_size", 10)
            if page_size in ("", "0"):
                page_size = 10
            viewps.page_size.set(page_size)
            offset = (int(viewps.page_no.get()) - 1) * int(viewps.page_size.get())
            viewps.offset.set(offset)
        else :
            viewps.page_size.set(20)
            viewps.offset.set(0)

    @staticmethod
    def getSortByColIDName(srt: str):
        srtarr = srt.split(".")
        if len(srtarr) != 2:
            return srt
        table_name, col_name = srtarr
        tblcols = DB.getTableMeta("sys_db_tables_cols").alias("tblcols")
        tblmaster = DB.getTableMeta("sys_db_tables").alias("tbl")
        stmt = (
            select(
                tblcols.c.col_id,
                tblcols.c.col_name
            )
            .select_from(
                tblcols.outerjoin(
                    tblmaster,
                    tblmaster.c.table_id == tblcols.c.table_id
                )
            )
            .where(tblmaster.c.table_name == table_name)
            .where(tblcols.c.col_name == col_name)
            .where(tblcols.c.is_delete == 0)
            .limit(1)
        )
        row = DB.executeDBSelectSingle(stmt)
        if row:
            return f"{row.col_id}{row.col_name}"
        return srt

    @staticmethod
    def getRecordCount(viewps):
        view_qry = viewps.view_qry.get()
        tmpstr = view_qry.split(f"FROM {viewps.table_name.get()} mtbl")[1]
        tmpstr = tmpstr.strip()
        cnt_qry = f"Select count(*) as total_record From {viewps.table_name.get()} mtbl {tmpstr}"
        cnt_qry = cnt_qry.split("Order By")[0]
        total_record = DB.getSingleColumnValue(cnt_qry, "total_record", 0)
        viewps.total_record.set(total_record)

    @staticmethod
    def setViewOutputArray(viewps):
        viewps.output_array.set({
            "view_id": viewps.view_id.get(),
            "view_name": viewps.view_name.get(),
            "view_type": viewps.view_type.get(),
            "rcdcnt": viewps.total_record.get(),
            "view_cols": viewps.view_cols.get(),
            "tbl_cols": viewps.tbl_cols.get(),
            "col_metadata": viewps.col_metadata.get(),
            "col_colors": viewps.col_colors.get(),
            "action_group_list": viewps.action_group_list.get(),
            "user_setting": viewps.user_setting.get(),
            "view_qry": viewps.view_qry.get(),
            "itm_list": viewps.item_list.get()
        })

    @staticmethod
    def setViewItemArray(viewps):
        item_list = []
        view_qry_data = viewps.view_qry_data.get()
        view_cols = viewps.view_cols.get()
        view_cols = view_cols.get("view_cols", [])
        primary_col = viewps.primary_col.get().replace("|", "")
        item_id_name = f"{primary_col}_mtbl"
        for data in view_qry_data:
            item = {
                "item_id": getattr(data, item_id_name, ""),
                "is_delete": getattr(data, "is_delete", 0),
                "noti_cnt": getattr(data, "noti_cnt", "")
            }
            # Join Table Is Delete
            # foreach($dvps->tablenames as $tbl) {
            #     $is_main_tbl = 0;
            #     if($tbl && explode("|", $tbl)[0] == $dvps->table_id) {
            #         $is_main_tbl = 1;
            #     }
            #     if($is_main_tbl == 0) {
            #         $tbl_alias = explode("|", $tbl)[1] . "_is_delete";
            #         $item_array[$tbl_alias] = $data->$tbl_alias;
            #     }
            # }
            # Association Per Item
            # if($dvps->full_access == 1) { /* Full Access */
            #     $item_array['associations_id'] = $dvps->fa_asso_id;
            #     $item_array['designation_id'] = $dvps->fa_dsgn_id;
            #     $item_array['designation_name'] = $dvps->fa_dsgn_nm;
            #     $item_array['is_owner'] = $dvps->fa_is_owner;
            #     $item_array['is_edit'] = $dvps->fa_is_edit;
            #     $item_array['is_view'] = $dvps->fa_is_view;
            #     $item_array['is_noaccess'] = $dvps->fa_is_noaccess;
            # } else { /* Limited Access */
            #     foreach($dvps->assousers as $assousr) {
            #         if($data->$item_id_name == $assousr->col_p_val) {
            #             $item_array['associations_id'] = $assousr->associations_id;
            #             $item_array['designation_id'] = $assousr->designation_id;
            #             $item_array['designation_name'] = $assousr->designation_name;
            #             $item_array['is_owner'] = $assousr->is_owner;
            #             $item_array['is_edit'] = $assousr->is_edit;
            #             $item_array['is_view'] = $assousr->is_view;
            #             $item_array['is_noaccess'] = $assousr->is_noaccess;
            #             break;
            #         }
            #     }
            # }
            for colhd in view_cols:
                col_id = colhd["col_id"]
                col_name = colhd["col_name"]
                qry_alias = colhd["qry_alias"]
                if colhd["col_type"] == "PChild":
                    continue
                dbcol = f"{col_id}{col_name}_{qry_alias}"
                item[f"{col_id}|{col_name}"] = str(getattr(data, dbcol, ""))
                # Display label for lookup/user columns
                if (dbhlp.isUserColumn(col_name, 0) or (colhd["col_type"] in ("MAPCOL", "DISPLAYAS") and colhd["lookup_colid"] > 0) ):
                    lbl_col = f"{col_id}{col_name}_lbl_{qry_alias}"
                    item[f"{col_id}|{col_name}lbl"] = str(getattr(data, lbl_col, ""))
            item_list.append(item)
        viewps.item_list.set(item_list)

viewhlp = ViewHelper()

class CreateViewHelper:

    @staticmethod
    def getDefaultAddViewCols(viewps):
        view_name = viewps.view_name.get()
        table_id = viewps.table_id.get()
        view_type = viewps.view_type.get()
        dbps.table_id
        primary_col_nm = view_name.lower().replace(" ", "_") + "_id"
        primary_col_alias = view_name + " ID"
        blank_view_cols = []
        rank = 10
        blank_view_cols.append( dbhlp.getPrimaryColParam(table_id, primary_col_nm, primary_col_alias, rank) )
        rank = rank + 10
        if view_type in ("TaskList", "ScrumBoard") :
            blank_view_cols.append( dbhlp.getTextColParam(table_id, "Title", rank) ) # Title Column
            rank = rank + 10
        blank_view_cols.append( dbhlp.getStatusColParam(table_id, "Status", "1", rank) )
        rank = rank + 10
        if view_type == "ScrumBoard" :
            blank_view_cols.append( dbhlp.getDropdownColParam(table_id, "Label", "1", rank) ) # Label (DDL) Column
            rank = rank + 10
            blank_view_cols.append( dbhlp.getPeopleColParam(table_id, "People", "1", 1, rank) ) # PPL Column
            rank = rank + 10
            blank_view_cols.append( dbhlp.getTextColParam(table_id, "Description", rank) ) # Title Description
            rank = rank + 10
            blank_view_cols.append( dbhlp.getDateColParam(table_id, "Due Date", rank) ) # DueDate Column
            rank = rank + 10

        if view_type == "TaskList" :
            # Task -->  , title, status_2, status_3
            blank_view_cols.append( dbhlp.getTextColParam(table_id, "Title", rank) ) # Tick Column
            rank = rank + 10 
            blank_view_cols.append( dbhlp.getStatusColParam(table_id, "Priority", "2", rank) ) # Priority(Status) Column
            updateNestedJsonVal(fulljson = blank_view_cols, jsonkey = "col_options", srchkey= "", srchval = "", updkey = "col_data_items", updval = getPriorityTemplate)
            rank = rank + 10
            blank_view_cols.append( dbhlp.getPeopleColParam(table_id, "People", "1", 1, rank) ) # PPL Column
            rank = rank + 10
            blank_view_cols.append( dbhlp.getDateColParam(table_id, "Date", rank) ) # Date Column
            rank = rank + 10

        blank_view_cols.append( dbhlp.getIsDeleteColParam(table_id, rank) )
        rank = rank + 10
        blank_view_cols.append( dbhlp.getIsMetadataColParam(table_id, rank) )
        rank = rank + 10
        blank_view_cols.append( dbhlp.getCreatedByColParam(table_id, rank) )
        rank = rank + 10
        blank_view_cols.append( dbhlp.getCreatedDateColParam(table_id, rank) )
        viewps.blank_view_cols.set(blank_view_cols) # Set To Property

    @staticmethod
    def getDefaultViewOptions(viewps):
        view_options = {}
        view_options["table_id"] = viewps.table_id.get()
        view_options["table_name"] = viewps.table_name.get()
        view_options["primary_col"] = viewps.primary_col.get() + "|" + viewps.primary_colnm.get()
        view_options["delete_col"] = viewps.delete_col.get()
        view_options["enable_newline"] = viewps.enable_newline.get()
        view_options["enable_join_save"] = viewps.enable_join_save.get()
        view_options["show_deleted"] = viewps.show_deleted.get()
        view_options["is_child_view"] = viewps.is_child_view.get()
        view_options["enable_child_srch"] = viewps.enable_child_srch.get()
        view_options["enable_chart"] = viewps.enable_chart.get()
        view_options["view_qry"] = viewps.view_qry.get()
        viewps.view_options.set(view_options) # Set To Property
        # print("getDefaultViewOptions View Options --> ", viewps.view_options.get() )

    @staticmethod
    def setColForView(dbps, viewps):
        view_cols_item = {}
        # {"view_cols": [{"rank": 10, "col_id": 3255, "colkey": 1, "col_name": "join_v1_id", "col_type": "NUMBER", "table_id": 198, "col_alias": "ID", "link_text": "", "qry_alias": "mtbl", "url_prefix": "", "date_format": null, "calc_formula": null, "lookup_colid": 0, "lookup_colnm": ""}}
        view_cols_item = {
            "table_id": dbps.table_id.get(),
            "col_id": dbps.col_id.get(),
            "col_name": dbps.col_name.get(),
            "qry_alias": dbps.qry_alias.get(),
            "col_alias": dbps.col_alias.get(),
            "col_type": dbps.col_type.get(),
            "col_key": dbps.col_key.get(),
            "lookup_colid": dbps.lookup_colid.get(),
            "lookup_colnm": dbps.lookup_colnm.get(),
            "url_prefix": viewps.url_prefix.get(),
            "link_text": viewps.link_text.get(),
            "date_format": viewps.date_format.get(),
            "calc_formula": viewps.calc_formula.get(),
            "rank": dbps.rank.get(),
        }
        viewps.view_cols_item.set(view_cols_item) # Set To Property

    @staticmethod 
    def generateViewQuery(viewps) :
        view_cols = viewps.view_cols.get()
        sortObjectsByKey(view_cols["view_cols"], 'rank', 'asc'); # Sort By Rank
        view_cols = view_cols.get("view_cols", [])
        qry_col_list = ""
        for col in view_cols:
            if createviewhlp.isColExcludedFromQuery(col):
                # print("col_name --> ", col["col_name"])
                col_id = col["col_id"]
                col_name = col["col_name"]
                qry_alias = col["qry_alias"]
                qrycolnm = f"{qry_alias}.{col_name}"
                displayas = f"{col_id}{col_name}_{qry_alias}"
                tmpqry = f"{qrycolnm} AS `{displayas}`, " # Select Qry Column
                if dbhlp.isUserColumn(col_name, 0): # People / User column
                    qrycolnm = dbhlp.getViewCaseQuery(qrycolnm, col_name)
                    displayas = f"{col['col_id']}{col_name}_lbl_{qry_alias}"
                    tmpqry += f"{qrycolnm} AS `{displayas}`, " # Append User Label Value
                # Display As / Map Column
                # if (col["col_type"] in ("MAPCOL", "DISPLAYAS") and col["lookup_colid"] > 0 ):
                #     displayas = f"{col['col_id']}{dvps.col_name.get()}_lbl_{qry_alias}"
                #     tmpqry += f"{col['lookup_colnm']} AS `{displayas}`, "
            qry_col_list = qry_col_list + tmpqry
        viewps.qry_col_list.set(qry_col_list) # Set To Properties
        createviewhlp.includeDeleteQuery(viewps)
        viewps.qry_col_list.set( viewps.qry_col_list.get().rstrip(", ") ) # Stripe Last , and space.
        # print("qry_col_list --> ", viewps.qry_col_list.get())
    
    @staticmethod
    def includeDeleteQuery(viewps):
        qry_col_list = viewps.qry_col_list.get()
        qry_col_list += "mtbl.is_delete, " # Main table
        # # Joined tables
        # view_joins = viewps.view_joins.get()
        # merge_tbl = view_joins.get("view_joins", []) if isinstance(view_joins, dict) else []
        # for tjoin in merge_tbl:
        #     qry_col_list += f"{tjoin['join_alias']}.is_delete, "
        viewps.qry_col_list.set(qry_col_list)

    @staticmethod
    def getNotificationCountQuery(viewps):
        noti_cntcol = (
            "(SELECT CONCAT("
            "SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END), '|', "
            "SUM(CASE WHEN is_archive = 0 THEN 1 ELSE 0 END)"
            ") "
            "FROM sys_notificaitons "
            f"WHERE item_id = mtbl.{viewps.primary_colnm.get()} "
            f"AND table_id = {viewps.table_id.get()} "
            f"AND to_user_id = {userps.user_id.get()} "
            "AND is_delete = 0"
            ") AS noti_cnt"
        )
        viewps.qry_col_list.set(viewps.qry_col_list.get() + noti_cntcol)
        
    @staticmethod
    def getLeftJoinQuery(viewps):
        view_joins = viewps.view_joins.get()
        if isinstance(view_joins, dict):
            merge_tbl = view_joins.get("view_joins", [])
        else:
            merge_tbl = []
        # print("getLeftJoinQuery view_joins --> ", viewps.view_joins.get())
        # merge_tbl = viewps.view_joins.get().get("view_joins", [])
        # print("getLeftJoinQuery --> ", merge_tbl)
        join_qry = ""
        join_del_qry = ""
        for tjoin in merge_tbl:
            join_alias = tjoin["join_alias"]
            join_to_alias = ""
            if tjoin["table_id_1"] == viewps.table_id.get():
                join_to_alias = "mtbl"
            else:
                for tmploop in merge_tbl:
                    if tjoin["table_id_1"] == tmploop["table_id_2"]:
                        join_to_alias = tmploop["join_alias"]
                        break

            join_qry += (
                f" LEFT JOIN {tjoin['table_name_2']} {join_alias}"
                f" ON {join_alias}.{tjoin['col_name_2']}"
                f" = {join_to_alias}.{tjoin['col_name_1']}"
            )
            if tjoin.get("enable_del", 0) == 0:
                join_del_qry += (
                    f" AND ({join_alias}.is_delete = 0 "
                    f"OR {join_alias}.is_delete IS NULL)"
                )
        viewps.join_qry.set(join_qry)
        viewps.join_del_qry.set(join_del_qry)
        # print("getLeftJoinQuery --> ", viewps.join_del_qry.get())
    
    @staticmethod
    def getFullViewQuery(viewps):
        view_qry = (
            f"SELECT DISTINCT {viewps.qry_col_list.get()} "
            f"FROM {viewps.table_name.get()} mtbl"
            f"{viewps.join_qry.get()}"
        )
        if viewps.show_deleted.get() == "0":
            view_qry += " WHERE mtbl.is_delete = 0"
        else:
            view_qry += (
                f" WHERE mtbl.{viewps.primary_colnm.get()} != ''"
            )
        if viewps.join_del_qry.get():
            view_qry += viewps.join_del_qry.get()
        viewps.view_qry.set(view_qry)
        print("getFullViewQuery --> ", viewps.view_qry.get())

    @staticmethod 
    def isColExcludedFromQuery(col: dict) -> bool:
        return col.get("col_type") != "PCHILD"

createviewhlp = CreateViewHelper()

# TO DO --> Create above format in helper, when new column get added, reuse col and view col functions.
# Generate Create & Alter Query