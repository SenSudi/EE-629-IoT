from utils.imports import *
from django.core.files import File
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

from django.contrib.auth.forms import PasswordChangeForm as CPF
from django.contrib.auth.forms import AdminPasswordChangeForm as ACPF
from models import Tester, Context
from notes.models import Scratchpad
from forms import TesterForm as TF
from forms import UserForm as UF
from forms import UserEditForm as UEF
from forms import UserDeleteForm as UDF

from project.views import get_context_items
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from project.models import Project

context = {}

# Create your views here.
###############################################################################
# USERS DB #
############
@login_required(login_url="/login/")
def user_manage(request):
    u = request.user
    context["users"] = User.objects.exclude(username="admin").order_by("username")
    context["item_name"] = "User"
    context["section"] = "User Manager"
    context["where"] = "user_manage"
    return render(request, "udb.html", context)


###############################################################################
@login_required(login_url="/login/")
def user_add_form(request):
    form = UF()
    try:
        form.fields["projects"].queryset = Project.objects.all()
    except:
        pass
    try:
        form.fields["groups"].queryset = Group.objects.all()
    except:
        pass
    context["form"] = form
    context["action"] = "/user_add/"
    context["form_id"] = "form-udb-user-add"
    context["title"] = "Add <b>User</b>"
    context["drop_footer"] = True
    return render(request, "user_add_form_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def user_add(request):
    base = settings.BASE_DIR
    avatar_path = static("images/avatar_default.png")
    username = request.POST.get("username", False)
    password = request.POST.get("password", False)
    tier = request.POST.get("tier", False)
    email = request.POST.get("email", False)
    first = request.POST.get("first_name", False)
    last = request.POST.get("last_name", False)
    phone = request.POST.get("phone", False)
    pids = request.POST.getlist("projects", [])
    gids = request.POST.getlist("groups", [])

    if username and tier:
        avatar = File(open(base + avatar_path))
        scratch = Scratchpad()
        scratch.save()
        uc = Context()
        uc.save()
        user = User.objects.create_user(username=username, password=password)
        if first:
            user.first_name = first
        if last:
            user.last_name = last
        if email:
            user.email = email
        user.save()

        for pid in pids:
            project = get_object_or_404(Project, id=pid)
            project.members.add(user)
        for gid in gids:
            group = get_object_or_404(Group, id=gid)
            user.groups.add(group)

        tester = Tester(
            tier=tier, avatar=avatar, scratchpad=scratch, context=uc, user=user
        )
        if phone:
            tester.phone_number = phone

        if tester.tier == "1":
            ti = "I"
        elif tester.tier == "2":
            ti = "II"
        elif tester.tier == "3":
            ti = "III"
        elif tester.tier == "4":
            ti = "IV"
        else:
            ti = "Wizard"
        tester.role = "Tester - Tier %s" % ti
        tester.save()
        return JR({"success": "success"})
    else:
        return JR({"errors": {"username": "required", "tier": "required"}})


###############################################################################
@login_required(login_url="/login/")
def user_update(request):
    if request.method == "POST":
        uid = request.POST.get("id", False)
        user = User.objects.get(id=uid)
        p = request.POST.getlist("projects", False)
        if p:
            user.project_set.clear()
            for project in p:
                user.project_set.add(project)
        u = request.POST.get("username", False)
        if u:
            user.username = u
        a = request.FILES.get("avatar", False)
        if a:
            user.tester.avatar = a
        f = request.POST.get("first", False)
        if f:
            user.first_name = f
        l = request.POST.get("last", False)
        if l:
            user.last_name = l
        e = request.POST.get("email", False)
        if e:
            user.email = e
        v = request.POST.get("active", False)
        user.active = v
        t = request.POST.get("tier", False)
        if t:
            user.tester.tier = t
        g = request.POST.getlist("groups", False)
        if g:
            user.groups.clear()
            user.tester.role = ""
            user.save()
            user.tester.save()
            for group in g:
                user.groups.add(group)
                name = Group.objects.get(id=group).name
                if "hv_admin" in name:
                    user.tester.role = "HV Admin"
                if "project_admin" in name:
                    if user.tester.role != "HV Admin":
                        user.tester.role = "Project Admin"
                if "tester" in name:
                    if user.tester.role != "HV Admin":
                        if user.tester.tier == "1":
                            ti = "I"
                        elif user.tester.tier == "2":
                            ti = "II"
                        elif user.tester.tier == "3":
                            ti = "III"
                        elif user.tester.tier == "4":
                            ti = "IV"
                        else:
                            ti = "Wizard"
                        user.tester.role = "Tester - Tier %s" % ti
                if "db_admin" in name:
                    if user.tester.role != "HV Admin":
                        user.tester.role = "DB Admin"
        user.save()
        user.tester.save()
        return HRR("/display_users/")
    else:
        uid = request.GET.get("id", False)
        user = User.objects.get(id=uid)
        form = UEF()
        try:
            form.fields["groups"].queryset = Group.objects.all()
        except:
            form.fields["groups"].queryset = []
        gl = user.groups.values_list("id", flat=True)
        form.fields["groups"].initial = gl
        try:
            form.fields["projects"].queryset = Project.objects.all()
        except:
            form.fields["projects"].queryset = []
        pl = user.project_set.values_list("id", flat=True)
        form.fields["projects"].initial = pl
        form.fields["avatar"].label = (
            "<b>Avatar - Current:</b> %s" % user.tester.avatar_thumb
        )
        form.fields["username"].initial = user.username
        form.fields["first"].initial = user.first_name
        form.fields["last"].initial = user.last_name
        form.fields["email"].initial = user.email
        form.fields["active"].initial = user.is_active
        form.fields["tier"].initial = user.tester.tier
        context["form"] = form
        context["uid"] = uid
        context["title"] = "Update user <b>%s</b>" % user.username
        context["drop_footer"] = True
        return render(request, "user_edit_form_modal.html", context)


###############################################################################
@login_required(login_url="/login/")
def user_details(request):
    uid = request.GET.get("uid", False)
    if uid:
        context["user"] = User.objects.get(id=uid)
    return render(request, "user_details.html", context)


###############################################################################
@login_required(login_url="/login/")
def display_users(request):
    context["users"] = User.objects.exclude(username="admin").order_by("username")
    return render(request, "display_users.html", context)


###############################################################################
@login_required(login_url="/login/")
def user_delete(request):
    uid = request.GET.get("id", False)
    user = User.objects.get(id=uid)
    form = UDF()
    context["form"] = form
    context["delete_user"] = user
    context["drop_footer"] = True
    context["drop_header"] = True
    return render(request, "user_delete.html", context)


###############################################################################
@login_required(login_url="/login/")
def user_delete_confirm(request):
    uid = request.POST.get("id", None)
    delete_user = get_object_or_404(User, id=uid)
    form = UDF(request.POST)
    user = request.user
    auth = AuthenticationForm(request.POST)
    if form.is_valid():
        if form.check_match:
            if user.check_password(
                request.POST.get("password", "")
            ):  # auth.confirm_login_allowed(user):
                delete_user.delete()
                return JR({"success": "success"})
            return JR({"errors": {"non_field": "invalid user password"}})
        else:
            return JR({"errors": {"non_field": "passwords do not match"}})
    return JR({"errors": form.errors})


###############################################################################
@login_required(login_url="/login/")
def ucip(request):
    uid = request.GET.get("id", False)
    user = get_object_or_404(User, id=uid)
    context["udb_user"] = user
    return render(request, "user_card_info_panel.html", context)


###############################################################################
@login_required(login_url="/login/")
def ucgp(request):
    uid = request.GET.get("id", False)
    user = get_object_or_404(User, id=uid)
    context["udb_user"] = user
    return render(request, "user_card_perm_panel.html", context)


###############################################################################
@login_required(login_url="/login/")
def ucpp(request):
    uid = request.GET.get("id", False)
    user = get_object_or_404(User, id=uid)
    context["udb_user"] = user
    return render(request, "user_card_projects_panel.html", context)


###############################################################################
###############################################################################
##								################							 ##
##								# END USERS DB #							 ##
##								################							 ##
###############################################################################
###############################################################################
@login_required(login_url="/login/")
def change_pass(request):
    user = request.user
    if request.method == "POST":
        if request.POST.get("check_old", False):
            # form = CPF(user,request.POST)
            if user.check_password(request.POST.get("old", "")):
                return JR({"success": "success"})
            else:
                return JR(
                    {
                        "errors": {
                            "old_password": "Incorrect Password - Please try again"
                        }
                    }
                )
        else:
            form = CPF(user, request.POST)
            if form.is_valid():
                form.save()
                return JR({"success": "success"})
            else:
                return JR({"errors": form.errors})
    form = CPF(user)
    form.fields["new_password1"].label = "<b>New Password</b>"
    form.fields["new_password2"].label = "<b>Confirm Password</b>"
    context["form"] = form
    return render(request, "change_pass.html", context)


@login_required(login_url="/login/")
def user_profile(request):
    uid = request.GET.get("id", False)
    user = get_object_or_404(User, id=uid)
    context["profile_user"] = user
    form = TF()
    context["form"] = form
    return render(request, "user_profile_modal.html", context)


@login_required(login_url="/login/")
def user_profile_update(request):
    if request.method == "POST":
        user = request.user
        messages = {}
        errors = {}
        if request.POST.get("f_name", False):
            first_name = request.POST["f_name"]
            user.first_name = first_name
            user.save()
            messages["f_name_success"] = "First Name Updated"
        if request.POST.get("l_name", False):
            last_name = request.POST["l_name"]
            user.last_name = last_name
            user.save()
            messages["l_name_success"] = "Last Name Updated"
        if request.POST.get("phone", False):
            phone = request.POST["phone"]
            try:
                int(phone)
            except:
                errors["phone"] = "Phone is not valid, enter numbers only"
                messages["phone_error"] = "Phone Is Invalid Format"
            else:
                user.tester.phone_number = phone
                user.tester.save()
                messages["phone_success"] = "Phone Updated"
        if request.POST.get("email", False):
            email = request.POST["email"]
            user.email = email
            user.save()
            messages["email_success"] = "Email Updated"
        if errors.__len__() > 0:
            return JR(errors)
        else:
            return JR(messages)
    else:
        return HR("not authorized")


###############################################################################
def profile(request):
    if request.method == "POST":
        if request.POST.get("update", False):
            user = request.user
            messages = {}
            if request.POST.get("password", False):
                password = request.POST["password"]
                if len(password) < 8:
                    messages["length_error"] = "Must be 8 characters or longer!"
                elif "pass" in password:
                    messages["content_error"] = "Must not use pass or password"
                else:
                    user.set_password(request.POST["password"])
                    user.save()
                    messages["pass_update_success"] = "Password Successfully Updated"
            else:
                # messages['pass_error'] = 'No Pass Entered!'
                pass
            if request.POST.get("f_name", False):
                first_name = request.POST["f_name"]
                user.first_name = first_name
                user.save()
                messages["f_name_success"] = "First Name Updated"
            if request.POST.get("l_name", False):
                last_name = request.POST["l_name"]
                user.last_name = last_name
                user.save()
                messages["l_name_success"] = "Last Name Updated"
            if request.POST.get("email", False):
                email = request.POST["email"]
                user.email = email
                user.save()
                messages["email_success"] = "Email Updated"
            return JR(messages)
    else:
        get_context_items(context, request)
        user = request.user
        form = TF()
        context["form"] = form
        context["user"] = user
        return render(request, "profile.html", context)


def upload_avatar(request):
    if request.method == "POST":
        user = request.user
        if request.FILES.get("avatar", False):
            if user.tester.avatar:
                user.tester.avatar.delete()
                user.tester.avatar = request.FILES["avatar"]
                user.tester.save()
            else:
                user.tester.avatar = request.FILES["avatar"]
                user.tester.save()
    return HRR("/profile")


def user_pw_reset(request):
    if request.method == "GET":
        uid = request.GET.get("uid", False)
        user = User.objects.get(id=uid)
        context["user"] = user
        form = ACPF(user)
        form.fields["password1"].label = "<b>New Password</b>"
        form.fields["password2"].label = "<b>Confirm Password</b>"
        context["form"] = form
        return render(request, "password_reset.html", context)
    else:
        uid = request.POST.get("uid", False)
        user = User.objects.get(id=uid)
        form = ACPF(user, request.POST)
        if form.is_valid():
            form.save()
            return JR({"success": "success"})
        else:
            return JR({"errors": form.errors})
