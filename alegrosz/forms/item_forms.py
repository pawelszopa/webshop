from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FloatField, TextAreaField, FileField, SelectField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length


class ItemForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired("Input is required"), DataRequired("Data is required"),
                                    Length(min=5, max=20, message="Input must be between 5 and 20 characters long")])
    price = FloatField('Price')
    description = TextAreaField("Description",
                                validators=[InputRequired("Input is required"), DataRequired("Data is required"),
                                            Length(min=5, max=40,
                                                   message="Input must be between 5 and 20 characters long")])
    image = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="Images only.")])


class NewItemForm(ItemForm):
    category = SelectField('Category', coerce=int)
    subcategory = SelectField('Subcategory', coerce=int)
    submit = SubmitField("Add")


class EditItem(ItemForm):
    submit = SubmitField("Edit")


class DeleteItem(FlaskForm):
    submit = SubmitField("Delete")


class FilterForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=20, message='Less then 20')])
    price = SelectField('Price', coerce=int, choices=[(0, '---'), (1, 'Max to min'), (2, 'Min to max')])
    category = SelectField('Category', coerce=int)
    subcategory = SelectField('Subcategory', coerce=int)
    submit = SubmitField('Filter')