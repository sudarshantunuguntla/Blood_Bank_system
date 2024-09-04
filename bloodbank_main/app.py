from flaskapp.user.routes import *
from flask import render_template

@app.route('/')
def home():
    return render_template('bbs_login.html')

if __name__=='__main__':
    app.run(debug=True)