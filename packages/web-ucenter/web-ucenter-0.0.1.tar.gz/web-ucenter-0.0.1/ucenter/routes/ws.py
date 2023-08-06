# coding=utf-8

from ws_handler.manage_handler import ManageHandler

base = 'ws'
routes = [
    (r'/%s/manage' % base, ManageHandler)
]
