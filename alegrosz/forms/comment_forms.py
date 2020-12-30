from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField("Comment",
                            validators=[InputRequired("Input is required"), DataRequired("Data is required")])
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Submit")
