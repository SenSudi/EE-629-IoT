from django.http import JsonResponse as JR


def is_hv_admin(user):
    return user.groups.filter(name="hv_admin").exists()


def is_project_manager(user):
    return user.groups.filter(name="project_manager").exists()


def is_tester(user):
    return user.groups.filter(name="tester").exists()


def is_user_admin(user):
    return user.groups.filter(name="user_admin").exists()


def is_client_admin(user):
    return user.groups.filter(name="client_admin").exists()


def is_contact_admin(user):
    return user.groups.filter(name="contact_admin").exists()


def is_method_admin(user):
    return user.groups.filter(name="method_admin").exists()


def is_project_admin(user):
    return user.groups.filter(name="project_admin").exists()


def is_report_admin(user):
    return user.groups.filter(name="report_admin").exists()


"""
this function will be used to restrict access to certain pages
"""


def grant_access(user, perm, flag):
    deny = False

    if perm == "project_manager":
        if flag:
            if not is_project_manager(user):
                deny = True

    elif perm == "project_admin":
        if flag:
            if not is_project_admin(user):
                deny = True

    elif perm == "tester_admin":
        if flag:
            if not is_tester_admin(user):
                deny = True

    elif perm == "client_admin":
        if flag:
            if not is_client_admin(user):
                deny = True

    elif perm == "contact_admin":
        if flag:
            if not is_contact_admin(user):
                deny = True

    elif perm == "method_admin":
        if flag:
            if not is_method_admin(user):
                deny = True

    elif perm == "project_admin":
        if flag:
            if not is_project_admin(user):
                deny = True

    elif perm == "report_admin":
        if flag:
            if not is_report_admin(user):
                deny = True

                # if deny:
    return deny


PERM_ERROR = JR({"permerror": "You do not have permission to access this page"})
