"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory,jsonify, make_response
from app.Form import PropertyForm
from app.models import UserProperty
import os, random, datetime, psycopg2 
from werkzeug.datastructures import CombinedMultiDict


psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])




###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Corey Anderson")

@app.route('/property/create', methods=['POST', 'GET'])
def property():
    """Render the website's property form page"""
    form = PropertyForm()
    files = PropertyForm(CombinedMultiDict((request.files, request.form)))
    if request.method == "POST" and form.validate_on_submit():
            title=form.title.data
            description=form.description.data
            numberBeds=form.bedroomNum.data
            numberRooms=form.bathRoomNum.data
            price=form.price.data
            propertyType=form.propertyType.data
            location=form.location.data
            picture=form.photo.data

            # Handling Database Procedure
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            UserProperty= UserProperty(propid, title, description, numberBeds, numberRooms, price, propertyType, location, filename, datecreated)
            propid = genId(title, filename) 
            datecreated = datetime.date.today()
            db.session.add(UserProperty)
            db.session.commit()
            flash("Property successfully listed", category="success")

            return redirect(url_for('properties'))
    return render_template("property.html", form = form)

@app.route('/propeties/', methods=["GET", "POST"])
def properties():
    """Render the websites property listing page""" 
    properties = UserProperty.query.all()
    
    if request.method == "POST":
        response = make_response(jsonify(properties)) 
        response.headers['Content-Type'] = 'application/json'
        return response 
    elif request.method == "GET":
        return render_template('properties.html', properties = properties) 

@app.route('/property/<propid>', methods=["GET", "POST"]) 
def getproperty(propid):

    prop = UserProperty.query.filter_by(id=propid).first()
    
    if request.method == "POST":
        if prop is not None:
            response = make_response(jsonify(id = prop.propid, title = prop.title, num_bedrooms = prop.num_bedrooms, num_bathrooms = prop.num_bathrooms, location = prop.location, price = prop.price, type_ = prop.type_, description = prop.description, upload = prop.filename, date_created = prop.date_created)) 
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            flash('Property Not Found', 'danger')
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("viewproperties.html", prop=prop)

    

def genId(title, filename):
    id = []
    for x in title:
        id.append(str(ord(x))) 
    for x in filename:
        id.append(str(ord(x))) 
    random.shuffle(id) 
    res= ''.join(id) 
    return int(res[:5]) 

@app.route("/uploads/<filename>") 
def getimage(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'], filename)   

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
