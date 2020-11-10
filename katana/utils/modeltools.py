from models import Guid


def save_new_guid(guid):
    g = Guid(guid=guid)
    g.save()
