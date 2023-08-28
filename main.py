import traceback
from io import BytesIO
import base64
import matplotlib
from data import *
import numpy_financial as npf
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange
from datetime import timedelta
import os


matplotlib.use('Agg')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

NATIONAL_PENSION = 413.76


#keeps tracks of the number of calling the "annual_return_calculation()" function
calls_of_function = 1


class optionsForm(FlaskForm):
    option1 = SelectField(label='Αποδόσεις διαθέσιμων επενδυτικών πακέτων')


def annual_return_calculation(num_of_funds: int):
    global calls_of_function
    print(f'Fund {calls_of_function}:')
    starting_price = float(input('starting price: '))
    current_price = float(input('current price: '))
    years = float(input('years: '))
    calls_of_function += 1
    return ((current_price - starting_price) / starting_price) / years


def portfolio_return_calculation(percentages: list, annual_returns: list):
    sum = 0
    for i in range(len(percentages)):
        sum += percentages[i] * annual_returns[i]
    total_return = round(sum, 2)
    return total_return


def passive_strategy_equities_return(data: dict, year):
    percentages = [19.5, 19.5, 19.5, 19.5, 10, 9, 3]
    average_return = []  # list of annual return of each mutual fund of passive multifund strategy
    if year == 'max':
        average_return.clear()
        for fund, prices in data.items():
            average_return.append(((prices['current_price'] - prices['starting_price']) / prices['starting_price']) / prices['years'])
    elif year == 1:
        average_return.clear()
        one_year_ago = (datetime.now() - timedelta(days=365)).date()
        for fund, prices in data.items():
            while True:
                try:
                    price = dict_of_equities[fund][one_year_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    # we add one day if one year ago that day the market was closed, so we check for the next available day that the market was open
                    one_year_ago = one_year_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price))
    elif year == 3:
        average_return.clear()
        three_years_ago = (datetime.now() - timedelta(days=365*3)).date()
        for fund, prices in data.items():
            while True:
                try:
                    price = dict_of_equities[fund][three_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    three_years_ago = three_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price)/ 3)
    elif year == 5:
        average_return.clear()
        five_years_ago = (datetime.now() - timedelta(days=365*5)).date()
        for fund, prices in data.items():
            while True:
                try:
                    if fund == 'Vanguard FTSE All-World UCITS ETF':
                        price = list(dict_of_equities[fund].values())[-1]
                    else:
                        price = dict_of_equities[fund][five_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    five_years_ago = five_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 5)
    elif year == 10:
        average_return.clear()
        ten_years_ago = (datetime.now() - timedelta(days=365*10)).date()
        for fund, prices in data.items():
            while True:
                try:
                    if fund == 'Vanguard FTSE All-World UCITS ETF':
                        price = list(dict_of_equities[fund].values())[-1]
                    else:
                        price = dict_of_equities[fund][ten_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    ten_years_ago = ten_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 10)
    elif year == 15:
        average_return.clear()
        fifteen_years_ago = (datetime.now() - timedelta(days=365*15)).date()
        for fund, prices in data.items():
            while True:
                try:
                    if fund == 'Vanguard FTSE All-World UCITS ETF':
                        price = list(dict_of_equities[fund].values())[-1]
                    elif fund == 'iShares Developed World Index Fund':
                        price = list(dict_of_equities[fund].values())[-1]
                    else:
                        price = dict_of_equities[fund][fifteen_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    fifteen_years_ago = fifteen_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 15)

    strategy_return = portfolio_return_calculation(percentages, average_return)
    return strategy_return

def passive_strategy_bonds_return(data: dict, year):
    percentages = [19.5, 19.5, 10, 10, 10, 11.5, 19.5]
    average_return = []  # list of annual return of each mutual fund of passive multifund strategy
    if year == 'max':
        average_return.clear()
        for fund, prices in data.items():
            average_return.append(
                ((prices['current_price'] - prices['starting_price']) / prices['starting_price']) / prices['years'])
    elif year == 1:
        average_return.clear()
        one_year_ago = (datetime.now() - timedelta(days=365)).date()
        for fund, prices in data.items():
            while True:
                try:
                    price = dict_of_bonds[fund][one_year_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    # we add one day if one year ago that day the market was closed, so we check for the next available day that the market was open
                    one_year_ago = one_year_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price))
    elif year == 3:
        average_return.clear()
        three_years_ago = (datetime.now() - timedelta(days=365 * 3)).date()
        for fund, prices in data.items():
            while True:
                try:
                    price = dict_of_bonds[fund][three_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    three_years_ago = three_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 3)
    elif year == 5:
        average_return.clear()
        five_years_ago = (datetime.now() - timedelta(days=365 * 5)).date()
        for fund, prices in data.items():
            while True:
                try:
                    price = dict_of_bonds[fund][five_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    five_years_ago = five_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 5)
    elif year == 10:
        average_return.clear()
        ten_years_ago = (datetime.now() - timedelta(days=365 * 10)).date()
        for fund, prices in data.items():
            while True:
                try:
                    if fund == 'Vanguard Global Bond Index Fund EUR Hedged Acc' or 'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc' or 'Vanguard U.S. Government Bond Index Fund EUR Hedged Acc':
                        price = list(dict_of_bonds[fund].values())[-1]
                    else:
                        price = dict_of_bonds[fund][ten_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    ten_years_ago = ten_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 10)
    elif year == 15:
        average_return.clear()
        fifteen_years_ago = (datetime.now() - timedelta(days=365 * 15)).date()
        for fund, prices in data.items():
            while True:
                try:
                    if fund == 'Vanguard Global Bond Index Fund EUR Hedged Acc' or 'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc' or 'Vanguard U.S. Government Bond Index Fund EUR Hedged Acc' or 'iShares Global Government Bond Index Fund (LU) D2 EUR':
                        price = list(dict_of_bonds[fund].values())[-1]
                    else:
                        price = dict_of_bonds[fund][fifteen_years_ago.strftime("%d %b %Y")]
                    break
                except KeyError:
                    fifteen_years_ago = fifteen_years_ago + timedelta(days=1)
            average_return.append(((prices['current_price'] - price) / price) / 15)
    strategy_return = portfolio_return_calculation(percentages, average_return)
    return strategy_return


def value_after_inflation(money, years):
    for i in range(years):
        money = money - (0.03*money)
    return round(money, 2)


#total return of investment after putting the years and annual contribution. Returns a tuple with investment value, total contribution and profit
def returns_of_investment(final_average_return, monthly_contribution, years_of_investment, annual_adjustment):
    annual_contribution = 12*monthly_contribution
    investment_value = 0
    total_contribution = 0
    value_each_year = [0]
    for i in range(years_of_investment):
        investment_value += annual_contribution
        investment_value += ((final_average_return/100) * investment_value)
        total_contribution += annual_contribution
        value_each_year.append(round(investment_value))
        if i == years_of_investment - 1:
            break
        annual_contribution += (annual_contribution * (annual_adjustment/100))
    x = [year for year in range(years_of_investment+1)]
    y = value_each_year
    plt.plot(x, y)
    plt.xlabel('Χρόνια επένδυσης')
    plt.ylabel('Αξία επένδυσης')
    plt.title('Γράφημα της επένδυσης')

    # Save the plot to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the plot image as base64 and convert to a string
    plot_image = base64.b64encode(buffer.read()).decode('utf-8')

    # Close the plot to release resources
    plt.close()

    profit = round(investment_value - total_contribution, 2)
    return round(investment_value, 2), round(total_contribution, 2), profit, plot_image


# pension calculation
def pension_calculation(age, years_of_work, salary):
    if years_of_work + (62 - age) >= 40:
        total_pension = NATIONAL_PENSION + (salary * (pension_data[years_of_work + (62 - age)] / 100))
    else:
        total_pension = NATIONAL_PENSION + (salary * (pension_data[years_of_work + (67 - age)] / 100))

    return round(total_pension, 2)


# inflation calculation
def inflation_calculation():
    inflation = int(input("Ποσοστό Πληθωρισμού(2% ή 3%): "))
    years = int(input("Χρόνια που έχουν περάσει: "))
    price = float(input("Τωρινή αξία του προϊόντος: "))
    for i in range(years):
        price_addition = price * (inflation/100)
        price += price_addition
    return round(price, 2)


# Συνάρτηση υπολογισμού δοσεων ωστε να φτάσω ενα συγκεκριμένο κεφάλαιο. pmt(rate, nper, pv, fv): rate = αποδοση , nper = αριθμός δόσεων, pv = present value, fv = final value.
def monthly_money(target: int, years: int, annual_return: float):
    r = annual_return / 100
    return round(-npf.pmt(r / 12, years * 12, 0, target), 2)


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


final_value = 0
profit = 0
contribution = 0
plot_url = None
total_pension = None
monthly_contribution = None
value_after_years = None


@app.route('/options')
def index():
    if session.get('logged_in'):
        # making these values 0 when the user is going back to home
        global final_value, profit, contribution, plot_url, total_pension, monthly_contribution
        final_value, profit, contribution, plot_url = 0, 0, 0, None
        total_pension, monthly_contribution, value_after_years = None, None, None
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/investment_return', methods=['GET', 'POST'])
def investment_return():
    if session.get('logged_in'):
        final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 'max')
        final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, 'max')
        selected_period = request.args.get('period', 1)
        if selected_period == '1':
            final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 1)
            final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, year=1)
        elif selected_period == '3':
            final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 3)
            final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, year=3)
        elif selected_period == '5':
            final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 5)
            final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, year=5)
        elif selected_period == '10':
            final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 10)
            final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, year=10)
        elif selected_period == '15':
            final_passive_equities_return = passive_strategy_equities_return(passive_strategy_equities_funds, 15)
            final_passive_bonds_return = passive_strategy_bonds_return(passive_strategy_global_bonds, year=15)
        elif selected_period == 'max':
            final_passive_equities_return = final_passive_equities_return
            final_passive_bonds_return = final_passive_bonds_return
        return render_template('investment_return.html', final_passive_equities_return=final_passive_equities_return, final_passive_bonds_return=final_passive_bonds_return)
    else:
        return redirect(url_for('login'))

@app.route('/value_after_inflation', methods=['GET', 'POST'])
def inflation_effect():
    if session.get('logged_in'):
        global value_after_years
        form = InflationForm()
        if form.validate_on_submit():
            initial_amount = form.initial_amount.data
            years = form.years.data
            value_after_years = value_after_inflation(initial_amount, years)

            return redirect(url_for('inflation_effect', value_after_years=value_after_years))
        return render_template('value_after_inflation.html', form=form, value_after_years=value_after_years)
    else:
        return redirect(url_for('login'))

@app.route('/return_of_investment', methods=['GET', 'POST'])
def return_of_investment():

    if session.get('logged_in'):
        global final_value, profit, contribution, plot_url
        form = ReturnOfInvestmentForm()
        try:
            if form.validate_on_submit():

                final_return = form.final_return.data
                annual_contribution = form.annual_contribution.data
                years_of_investment = form.years_of_investment.data
                annual_adjustment = form.annual_adjustment.data
                investment = returns_of_investment(final_return, annual_contribution, years_of_investment, annual_adjustment)
                final_value = investment[0]
                profit = investment[2]
                contribution = investment[1]
                plot_url = investment[3]

                return redirect(url_for('return_of_investment', final_value=final_value, profit=profit, contribution=contribution, plot_url=plot_url))
        except Exception as e:
            print(e)
        return render_template('return_of_investment.html', form=form, final_value=final_value, profit=profit, contribution=contribution, plot_url=plot_url)
    else:
        return redirect(url_for('login'))

@app.route('/pension', methods=['GET', 'POST'])
def pension():
    if session.get('logged_in'):
        global total_pension
        form = PensionForm()
        if form.validate_on_submit():
            age = form.age.data
            years_of_work = form.years_of_work.data
            salary = form.salary.data
            total_pension = pension_calculation(age, years_of_work, salary)
            return redirect(url_for('pension', pension=total_pension))
        return render_template('pension.html', form=form, pension=total_pension)
    else:
        return redirect(url_for('login'))

@app.route('/target_amount', methods=['GET', 'POST'])
def target_amount():
    if session.get('logged_in'):
        global monthly_contribution
        form = TargetCapital()
        if form.validate_on_submit():
            target_capital = form.target_capital.data
            years = form.years.data
            annual_return = form.annual_return.data
            monthly_contribution = monthly_money(target_capital, years, annual_return)
            return redirect(url_for('target_amount', monthly_contribution=monthly_contribution))
        return render_template('target_amount.html', form=form, monthly_contribution=monthly_contribution)
    else:
        return redirect(url_for('login'))
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == os.environ.get('ADMIN') and password == os.environ.get('PASS'):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password!', 'error')

    return render_template('login.html', form=form)


@app.route('/exit')
def exit_option():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
