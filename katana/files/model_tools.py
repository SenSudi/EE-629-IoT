from models import Associated_File as AF
import sys


def save_new_afile(file, subdirectory, guid):
    new_file = AF()
    new_file.filename = file.name
    new_file.file = file
    try:
        new_file.guid = get_guid()
    except:
        get_guid = getattr(sys.modules["utils.tools"], "get_guid")
        new_file.guid = get_guid()
    new_file.subdirectory = subdirectory
    new_file.a_i_guid = guid
    new_file.save()
    return new_file
