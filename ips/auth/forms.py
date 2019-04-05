from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

# from ips.auth.models import User


class LoginForm(FlaskForm):
    username = StringField(u'Username', render_kw={'autofocus': True}, validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])
    submit = SubmitField('Login', id="login_submit_button")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # user = User.query.filter_by(username=self.username.data).first()
        #
        # if not user:
        #     self.username.errors.append('You are not authorised to use this system')
        #     return False
        #
        # if not user.password:
        #     self.username.errors.append('Invalid account')
        #     return False
        #
        # # Do the passwords match
        # if not user.check_password(self.password.data):
        #     self.username.errors.append('Invalid username or password')
        #     return False

        return True
