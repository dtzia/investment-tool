import numpy_financial as npf
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib
from data import *

NATIONAL_PENSION = 413.76


# keeps tracks of the number of calling the "annual_return_calculation()" function
# calls_of_function = 1
# def annual_return_calculation(num_of_funds: int):
#     global calls_of_function
#     print(f'Fund {calls_of_function}:')
#     starting_price = float(input('starting price: '))
#     current_price = float(input('current price: '))
#     years = float(input('years: '))
#     calls_of_function += 1
#     return ((current_price - starting_price) / starting_price) / years

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
            average_return.append(((prices['current_price'] - price) / price) / 3)
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
                    # These 2 funds where not existing before 15 years, so we are taking the first existing price
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

    STATIC_DIR = "static"
    os.makedirs(STATIC_DIR, exist_ok=True)
    plot_image_path = os.path.join(STATIC_DIR, "plot.png")
    plt.savefig(plot_image_path, format='png')

    # Close the plot to release resources
    plt.close()

    profit = round(investment_value - total_contribution, 2)
    return round(investment_value, 2), round(total_contribution, 2), profit, plot_image_path


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