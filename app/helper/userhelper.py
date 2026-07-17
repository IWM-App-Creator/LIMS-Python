def setUserProperties(userps, params):
    userps.othr_userid.set(params.get("othr_userid", ""))
    userps.first_name.set(params.get("first_name", ""))
    userps.last_name.set(params.get("last_name", ""))
    userps.password.set(params.get("password", ""))
    userps.phone.set(params.get("phone", ""))
    userps.company_name.set(params.get("company_name", ""))
    userps.user_timezone.set(params.get("timezone", ""))