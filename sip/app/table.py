# import things
from flask_table import Table, Col, LinkCol

# Declare your table
class ItemTable(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    description = Col('Description')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))

# Get some objects
class Item(object):
    def __init__(self, id, name, description, edit):
        self.id = id
        self.name = name
        self.description = description

#items = [Item('Name1', 'Description1'),
#         Item('Name2', 'Description2'),
#         Item('Name3', 'Description3')]
# Or, equivalently, some dicts
items = [dict(id=1, name='Name1', description='Description1'),
         dict(id=2, name='Name2', description='Description2'),
         dict(id=3, name='Name3', description='Description3')]