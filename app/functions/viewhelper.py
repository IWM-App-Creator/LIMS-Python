import json
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.properties.dbproperties import dbps
from app.functions.dbhelper import isUserColumn

class ViewHelper:

    @staticmethod
    def setViewInputParam(viewps, params):
        viewps.view_id.set(params.get("view_id", ""))
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
            viewps.page_size.set(10)
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
            viewps.page_size.set(10)
            viewps.offset.set(0)

    @staticmethod
    def getRecordCount(viewps):
        view_qry = viewps.view_qry.get()
        tmpstr = view_qry.split(f"From {viewps.table_name.get()} mtbl")[1]
        tmpstr = tmpstr.strip()
        cnt_qry = f"Select count(*) as total_record From {viewps.table_name.get()} mtbl {tmpstr}"
        cnt_qry = cnt_qry.split("Order By")[0]
        total_record = DB.getSingleColumnValue(cnt_qry, "total_record", 0)
        viewps.total_record.set(total_record)

    @staticmethod
    def setViewOutputArray(viewps):
        viewps.output_array.set({
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
            for colhd in view_cols:
                col_id = colhd["col_id"]
                col_name = colhd["col_name"]
                qry_alias = colhd["qry_alias"]
                if colhd["col_type"] == "PChild":
                    continue
                dbcol = f"{col_id}{col_name}_{qry_alias}"
                item[f"{col_id}|{col_name}"] = str(getattr(data, dbcol, ""))
                # Display label for lookup/user columns
                if (isUserColumn(col_name, 0) or (colhd["col_type"] in ("MAPCOL", "DISPLAYAS") and colhd["lookup_colid"] > 0) ):
                    lbl_col = f"{col_id}{col_name}_lbl_{qry_alias}"
                    item[f"{col_id}|{col_name}lbl"] = str(getattr(data, lbl_col, ""))
            item_list.append(item)
        viewps.item_list.set(item_list)

viewhlp = ViewHelper()

class CreateViewHelper:
    
    @staticmethod
    def getDefaultAddViewCols(viewps):
        view_name = viewps.view_name.get()
        primary_col_nm = view_name.lower().replace(" ", "_") + "_id"
        primary_col_alias = view_name + " ID"
        print("primary_col_nm --> ", primary_col_nm)
        print("primary_col_alias --> ", primary_col_alias)
        blank_view_cols = []
        blank_view_cols.append({"col_name": primary_col_nm, "col_alias": primary_col_alias, "datatype": "bigint", "col_type": "NUMBER", "colkey": 1, "length": 11, "is_primary": 1, "default_val": 0, "rank": 10 })

        blank_view_cols.append({"col_name": "status_1", "col_alias": "Status", "datatype": "int", "col_type": "YESNO", "length": 4, "is_index": 1, "default_val": 0, "rank": 20})

        blank_view_cols.append({"col_name": "is_delete", "col_alias": "ID Deleted", "datatype": "int", "length": 1, "is_index": 1, "actv_log_cols": 1, "default_val": 0, "rank": 30})
        
        blank_view_cols.append({"col_name": "is_metadata", "col_alias": "Metadata", "datatype": "json", "is_index": 1, "rank": 40})
        
        blank_view_cols.append({"col_name": "created_by", "col_alias": "Created By", "datatype": "bigint", "col_type": "FULLNAME", "colkey": 2, "lookup_colid": 492, "length": 11, "is_index": 1, "default_val": 0, "rank": 50})
        
        blank_view_cols.append({"col_name": "created_date", "col_alias": "Created Date", "datatype": "datetime", "col_type": "DATETIME", "length": "", "rank": 60})
        
        viewps.blank_view_cols.set(blank_view_cols) # Set To Property

createviewhlp = CreateViewHelper()

# TO DO --> Create above format in helper, when new column get added, reuse col and view col functions.
# Generate Create & Alter Query