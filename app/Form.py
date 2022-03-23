from flask_wtf  import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FileField, IntegerField, DecimalField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bedroomNum = IntegerField('No. of Rooms', validators=[DataRequired()])
    bathRoomNum = IntegerField('No. of Bathdrooms', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    propertyType = SelectField('Property type', choices=[('Apartment', 'Apartment'), ('House', 'House')] )
    location = StringField('Location', validators=[DataRequired()])
    photo = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])

