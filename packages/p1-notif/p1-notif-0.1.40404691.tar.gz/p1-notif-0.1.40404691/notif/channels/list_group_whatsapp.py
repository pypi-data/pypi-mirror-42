from .abstract_channel import AbstractChannel

class ListGroupWhatsapp(AbstractChannel):

    def __init__(self):

    def json(self):
        payload = dict()
        return payload

    def notif_type(self):
        return 'LIST_GROUP_WHATSAPP'