from app.dbfunctions.modulefunctions import getViewModulesData

def getModules(moduleps):
    module_data = getViewModulesData(moduleps)
    modules = []
    for mod in module_data:
        row = {
            "template_id": mod.template_id,
            "template_name": mod.template_name,
            "tmplt_s_desc": mod.s_desc,
            "tmplt_l_desc": mod.l_desc,
            "template_type": mod.template_type,
            "t_cat_id": mod.t_cat_id
        }
        modules.append(row)
    return modules