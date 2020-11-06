from docx import Document
from docx.shared import Inches
from docxtpl import DocxTemplate
from django.core import serializers as ser
import os
import hashlib
import random
import string

from modeltools import save_new_guid


def check_unique(guid):
    try:
        Guid = getattr(sys.modules["utils.models"], "Guid")
    except:
        from utils.models import Guid
    if guid in Guid.objects.values_list("guid", flat=True):
        return True
    else:
        return False


def make_guid():
    string_length = 16
    r = "".join(
        random.choice(string.letters + string.digits) for i in xrange(string_length)
    )
    m = hashlib.md5()
    m.update(r)
    guid = m.hexdigest()
    return guid


def get_guid():
    flag = True
    while flag:
        guid = make_guid()
        flag = check_unique(guid)
    save_new_guid(guid)
    return "%s" % (guid)


def check_or_make_dir(name):
    if os.access(name, os.F_OK):
        return True
    else:
        os.mkdir(name)


def check_if_file_exists(name):
    name = name[1:]
    if os.access(name, os.F_OK):
        return True
    else:
        return False


def new_report(report_object):
    r = report_object

    context = {}
    contributors = []
    vulnerability = []
    PATH_PREFIX = "media/"
    EXTENSION = ".docx"
    SLASH = "/"
    PROJECT_TITLE = str(r.project.title)
    REPORT_CREATED = str(r.created)[:18]
    REPORT_UPDATED = str(r.updated)[:18]

    context["title"] = str(r.title)
    context["created"] = REPORT_CREATED
    context["created_by"] = str(r.created_by)
    context["project"] = PROJECT_TITLE
    for item in r.contributors.all():
        name = "%s %s" % (str(item.first_name), str(item.last_name))
        if name != context["created_by"]:
            contributors.append(str(name))
    context["contributors"] = contributors
    if context["contributors"] == []:
        context.pop("contributors", None)

    doc = DocxTemplate("template.docx")

    doc.render(context)

    DIR = PATH_PREFIX + PROJECT_TITLE

    DOC_NAME = REPORT_UPDATED + EXTENSION

    check_or_make_dir(DIR)

    doc.save(DIR + SLASH + DOC_NAME)

    r.file_url = SLASH + DIR + SLASH + DOC_NAME
    r.file_name = DOC_NAME
    r.save()

    # r.report_file.save(DOC_NAME,DIR+SLASH+DOC_NAME, save=True)
