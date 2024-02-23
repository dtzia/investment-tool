import traceback
from io import BytesIO
import base64
from data import *
from functions import *
from classes import *
from flask import Flask, render_template, url_for, redirect, flash, request, session
import os


matplotlib.use('Agg')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


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
