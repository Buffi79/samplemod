from flask import Flask, render_template, flash, redirect, request
from flask_ini import FlaskIni
from app.forms import ConfigForm
from app.forms import EditentryForm
from app.table import ItemTable
from app import routes
from flask_bootstrap import Bootstrap



app = Flask(__name__)
#bootstrap = Bootstrap(app)
app.iniconfig = FlaskIni()
with app.app_context():
    app.iniconfig.read('./config/settings.ini')


@app.route('/')
@app.route('/index')
def index():
    if app.debug: # True
        endpoint = app.iniconfig.get('LOG', 'level')
        timeout  = app.iniconfig.getint('backend', 'timeout', fallback=300)
        return render_template('base.html', title='Home')
    else:
        return "Won't get here, thanks to the config file"

@app.route('/sipconfig', methods=['GET', 'POST'])
def sipconfig():
    form = ConfigForm()
    if request.method == 'GET':
        form.level.data = app.iniconfig.get('LOG', 'level')
        form.format.data = app.iniconfig.get('LOG', 'format')
        form.telsearchkey.data = app.iniconfig.get('TelSearch', 'key')
    elif form.validate_on_submit():
        print (form.level.data)

    return render_template('config.html', title='Sign In', form=form)

@app.route('/table')
def showtable():
    items = Item.get_elements()
    table = ItemTable(items)

    # You would usually want to pass this out to a template with
    # render_template.
    #return table.__html__()
    return render_template('table.html', title='List', table=table)

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = EditentryForm()
    item = Item.get_element_by_id(id)
    if request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
    elif form.validate_on_submit():
        print (form.name.data)

    return render_template('editentry.html', title='Edit', form=form)
 #   flash('Album updated successfully!')
 #   return "Won't get here, thanks to the config file"
 #   qry = db_session.query(Album).filter(
 #               Album.id==id)
 #   album = qry.first()#3
#
#    if album:
#        form = AlbumForm(formdata=request.form, obj=album)
#        if request.method == 'POST' and form.validate():
#            # save edits
#            save_changes(album, form)
#            flash('Album updated successfully!')
#            return redirect('/')
#        return render_template('edit_album.html', form=form)
#    else:
#        return 'Error loading #{id}'.format(id=id)

class Item(object):
    """ a little fake database """
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def get_elements(cls):
        return [
            Item(1, 'Z', 'zzzzz'),
            Item(2, 'K', 'aaaaa'),
            Item(3, 'B', 'bbbbb')]

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]






if __name__ == '__main__':
    app.run(debug=True)