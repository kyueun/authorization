from flask_table import Table, Col


class item_table(Table):
    name = Col('name')
    email = Col('email')


class Item(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

