from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange

class optionsForm(FlaskForm):
    option1 = SelectField(label='Αποδόσεις διαθέσιμων επενδυτικών πακέτων')


class TargetCapital(FlaskForm):
    target_capital = IntegerField('Στόχος κεφαλαίου', validators=[DataRequired(), NumberRange(min=0)])
    years = IntegerField('Χρονική διάρκεια μέχρι την ρευστοποίηση', validators=[DataRequired(), NumberRange(min=0)])
    annual_return = FloatField('Εκτιμώμενη ετήσια μεσοσταθμική απόδοση', validators=[DataRequired(), NumberRange(min=0)])


class PensionForm(FlaskForm):
    age = IntegerField('Ηλικία', validators=[DataRequired(), NumberRange(min=0)])
    years_of_work = IntegerField('Χρόνια εργασίας μέχρι σήμερα', validators=[DataRequired(), NumberRange(min=0)])
    salary = IntegerField('Μισθός', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Υπολόγισε')


class ReturnOfInvestmentForm(FlaskForm):
    final_return = FloatField(
        'Απόδοση:',
        validators=[DataRequired()]
    )
    annual_contribution = IntegerField(
        'Μηνιαία Συνεισφορά:',
        validators=[DataRequired()],
    )
    years_of_investment = IntegerField(
        'Χρόνια Επένδυσης:',
        validators=[DataRequired(), NumberRange(min=1)],
    )
    annual_adjustment = IntegerField(
        'Ετήσια Αναπροσαρμογή (2, 3 ή 5%):',
        validators=[DataRequired(), NumberRange(min=2, max=5)],
    )
    calculate = SubmitField('Calculate')


class InflationForm(FlaskForm):
    initial_amount = IntegerField('Αρχικό κεφάλαιο', validators=[DataRequired(), NumberRange(min=0)])
    years = IntegerField('Χρόνια που πέρασαν', validators=[DataRequired(), NumberRange(min=0)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Go to app')