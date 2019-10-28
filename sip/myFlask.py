from flask import Flask, render_template, flash, redirect, request
from flask_ini import FlaskIni
from app.forms import ConfigForm
from app.forms import EditentryForm
from app.table import ItemTable
from app.table import Item
from flask_bootstrap import Bootstrap
from app.table import getItems
from app.table import updateItem

from app.table2 import columns as table2col
from app.table2 import data as table2data


app = Flask(__name__)
bootstrap = Bootstrap(app)
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

@app.route('/table1')
def showtable1():
    #items = Item.get_elements()
    table = ItemTable(getItems())

    # You would usually want to pass this out to a template with
    # render_template.
    #return table.__html__()
    return render_template('table.html', title='Whitelist', table=table)

@app.route('/table2')
def showtable2():
    return render_template("table2.html",
      data=table2data,
      columns=table2col,
      title='Flask Bootstrap Table')


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    id = id-1
    form = EditentryForm()
    #item = Item.get_element_by_id(id)
    item = getItems()[id]
    if request.method == 'GET':
        form.name.data = item.get('name')
        form.description.data = item.get('description')
    elif form.validate_on_submit():
        #print (form.name.data)
        updateItem(id, form.name.data, form.description.data)
        table = ItemTable(getItems())
        return render_template('table.html', title='Whitelist', table=table)

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

if __name__ == '__main__':
    app.run(debug=True)

# pip3 isntall
#
#
#
#
#
