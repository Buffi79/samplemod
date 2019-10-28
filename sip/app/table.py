from flask_table import Table, Col, LinkCol, ButtonCol

# Declare your table
class ItemTable(Table):
    id = Col('Id', show=False)
    name = Col('Number')
    description = Col('Beschreibung')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']


# Get some objects
class Item(object):
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def get_elements(cls):
        return items

    @classmethod
    def get_element_by_id(cls, id):
        #return [i for i in cls.get_elements() if i.id == id][0]
        return [i for i in cls.get_elements() if i.get('id') == id][0]

def updateItem(id, value1, value2):
    item = items[id]
    item['name'] = value1
    item['description'] = value2


#items = [Item(1, 'Name1', 'Description1'),
#         Item(2, 'Name2', 'Description2'),
#         Item(3, 'Name3', 'Description3')]

def getItems():
    return items

items = [dict(id=1, name='Name1', description='Description1'),
         dict(id=2, name='Name2', description='Description2'),
         dict(id=3, name='Name3', description='Description3')]


