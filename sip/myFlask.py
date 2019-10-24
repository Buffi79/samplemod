from flask import Flask, render_template, flash, redirect, request
from flask_ini import FlaskIni
from app.forms import ConfigForm
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

if __name__ == '__main__':
    app.run(debug=True)