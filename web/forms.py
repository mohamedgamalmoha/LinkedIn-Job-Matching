from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


replace_space = lambda x: x.replace(' ', '%20') if isinstance(x, str) else x
spilt_words = lambda x: replace_space(x).split(',') if isinstance(x, str) else x


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    def as_dict(self) -> dict:
        return {
            'username': self.username.data,
            'email': self.email.data,
            'password': self.password.data,
        }


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class JobMatchingForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()], filters=[replace_space])
    keywords = StringField('KeyWord', validators=[DataRequired()], filters=[replace_space])
    education = StringField('Education', validators=[DataRequired()])
    skills = StringField('KeyWord', validators=[DataRequired()], filters=[spilt_words])
    start = IntegerRangeField('Start', validators=[NumberRange(1, 500)], default=1)

    @property
    def employee_criteria(self) -> dict:
        return {
            'skills': self.skills.data,
            'education': self.education.data,
        }
