from dateutil import relativedelta
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import os




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)


#CREATE TABLE
class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    starting_price = db.Column(db.String(20))
    current_price = db.Column(db.String(20))
    years = db.Column(db.String(20))

    def __init__(self, name, starting_price, current_price, years):
        self.name = name
        self.starting_price = starting_price
        self.current_price = current_price
        self.years = years


with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = 'my secret key'

pension_data = {
    15: 11.55,
    16: 12.39,
    17: 13.23,
    18: 14.07,
    19: 14.97,
    20: 15.87,
    21: 16.77,
    22: 17.73,
    23: 18.69,
    24: 19.65,
    25: 20.68,
    26: 21.71,
    27: 22.74,
    28: 23.95,
    29: 25.16,
    30: 26.37,
    31: 28.35,
    32: 30.33,
    33: 32.31,
    34: 34.81,
    35: 37.31,
    36: 39.81,
    37: 42.36,
    38: 44.91,
    39: 47.46,
    40: 50.01,
    41: 50.51,
    42: 51.01,
    43: 51.51,
    44: 52.01,
    45: 52.51
}

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


# dictionary with Keys the name of the mutual fund and Values the site of them
funds = {
    'Vanguard Global Equity Stock Index Fund': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00b03hd191:eur',
    'iShares Developed World Index Fund': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00b62wcl09:eur',
    'Vanguard FTSE All-World UCITS ETF': 'https://www.vanguard.co.uk/professional/product/etf/equity/9679/ftse-all-world-ucits-etf-usd-accumulating',
    'Vanguard US 500 Stock Index Fund Eur H': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00b1g3dh73:eur',
    'Vanguard European Stock Index Fund': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie0007987708:eur',
    'Vanguard Eurozone Stk': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie0008248803:eur',
    'Vanguard Japan Stock Index Fund': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie0007286036:eur'
}

bonds = {
    'Vanguard Global Bond Index Fund EUR Hedged Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=IE00B18GC888:EUR',
    'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00bh65qp47:eur',
    'Vanguard Euro Investment Grade Bond Index Fund EUR Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00b04ffj44:eur',
    'Vanguard U.S. Investment Grade Credit Index Fund EUR Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie00b04gqt48:eur',
    'Vanguard Euro Government Bond Index Fund EUR Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=IE0007472990:EUR',
    'Vanguard U.S. Government Bond Index Fund EUR Hedged Acc': 'https://markets.ft.com/data/funds/tearsheet/summary?s=ie0007471471:eur',
    'iShares Global Government Bond Index Fund (LU) D2 EUR': 'https://markets.ft.com/data/funds/tearsheet/summary?s=lu0875157884:eur'
}

equities_filenames = ['Vanguard Global Equity Stock Index Fund.xlsx',
                      'iShares Developed World Index Fund.xlsx',
                      'Vanguard FTSE All-World UCITS ETF.xlsx',
                      'Vanguard US 500 Stock Index Fund Eur H.xlsx',
                      'Vanguard European Stock Index Fund.xlsx',
                      'Vanguard Eurozone Stk.xlsx',
                      'Vanguard Japan Stock Index Fund.xlsx',
                      ]

bonds_filenames = ['Vanguard Global Bond Index Fund EUR Hedged Acc.xlsx',
                   'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc.xlsx',
                   'Vanguard Euro Investment Grade Bond Index Fund EUR Acc.xlsx',
                   'Vanguard U.S. Investment Grade Credit Index Fund EUR Acc.xlsx',
                   'Vanguard Euro Government Bond Index Fund EUR Acc.xlsx',
                   'Vanguard U.S. Government Bond Index Fund EUR Hedged Acc.xlsx',
                   'iShares Global Government Bond Index Fund (LU) D2 EUR.xlsx'
                   ]
BONDS_FILEPATH = './historical_prices/Passive Strategy Bonds/'
EQUITIES_FILEPATH = './historical_prices/Passive Strategy Equities/'


def excel_to_dict(filepath, name):
    data = pd.read_excel(filepath)
    date_column = 'Date'
    price_column = 'NAV (EUR)'
    data_dict = {}

    for index, row in data.iterrows():
        date = row[date_column].replace('/', ' ')
        price = row[price_column]
        if type(price) is str:
            if '€' in price:
                data_dict[date] = round(float(price[1:]), 2)
            else:
                data_dict[date] = round(float(price[3:]), 2)
        else:
            data_dict[date] = round(float(price), 2)

    return data_dict


dict_of_bonds = {bonds[:-5]: excel_to_dict(filepath=BONDS_FILEPATH + bonds, name=bonds) for bonds in bonds_filenames}
dict_of_equities = {equities[:-5]: excel_to_dict(filepath=EQUITIES_FILEPATH + equities, name=equities) for equities in equities_filenames}


def get_current_price(fund_name: str):
    try:
        response = requests.get(funds[fund_name])
    except KeyError:
        response = requests.get(bonds[fund_name])

    web_page = response.text
    soup = BeautifulSoup(web_page, 'html.parser')
    with app.app_context():
        session = db.session
        if fund_name == 'Vanguard FTSE All-World UCITS ETF':
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                service = ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
                driver = webdriver.Chrome(service=service, options=chrome_options)
                # Navigate to the webpage
                driver.get(
                    'https://www.vanguard.co.uk/professional/product/etf/equity/9679/ftse-all-world-ucits-etf-usd-accumulating')
                element = driver.find_element(By.XPATH, "//*[@id='back-to-top']/europe-core-root/europe-core-product-page/aem-page/aem-model-provider/nds-aem-base-responsive-grid/div/nds-aem-base-responsive-grid/div[3]/europe-core-jump-links-list/div[4]/europe-core-gpx-product-detail-fund-cards-container/europe-core-product-detail-fund-cards/div/div[1]/europe-core-product-detail-fund-card/div[1]/div[2]")
                element_text = element.text
                price = element_text[3:]
                fund_price = session.query(MutualFund).filter_by(name=fund_name).first()
                fund_price.current_price = price
                print(price)
                driver.quit()
            except AttributeError:
                fund = session.query(MutualFund).filter_by(name=fund_name).first()
                price = fund.current_price

            session.commit()
        else:
            try:
                price = soup.find('span', {'class': 'mod-ui-data-list__value'}).text
                fund_price = session.query(MutualFund).filter_by(name=fund_name).first()
                fund_price.current_price = price
            except AttributeError:
                price = session.query(MutualFund).filter_by(name=fund_name).first().current_price
            session.commit()

    return float(price)


# finds the years as a float between the released date of a fund until now
def get_years_of_fund(day, month, year):
    release_date = datetime(year=year, month=month, day=day)
    now = datetime.now()
    diff = relativedelta.relativedelta(now, release_date)
    years_of_fund = diff.years + round(diff.months/12, 2)
    return years_of_fund


# dictionary with prices of funds
passive_strategy_equities_funds = {
    'Vanguard Global Equity Stock Index Fund': {
        'starting_price': 12.53,
        'current_price': get_current_price('Vanguard Global Equity Stock Index Fund'),
        'years': get_years_of_fund(4, 5, 2007),

    },
    'iShares Developed World Index Fund': {
        'starting_price': 10.83,
        'current_price': get_current_price('iShares Developed World Index Fund'),
        'years': get_years_of_fund(27, 4, 2012)
    },
    'Vanguard FTSE All-World UCITS ETF': {
        'starting_price': 80.00,
        'current_price': get_current_price('Vanguard FTSE All-World UCITS ETF'),
        'years': get_years_of_fund(23, 7, 2019)
    },
    'Vanguard US 500 Stock Index Fund Eur H': {
        'starting_price': 11.23,
        'current_price': get_current_price('Vanguard US 500 Stock Index Fund Eur H'),
        'years': get_years_of_fund(4, 5, 2007)
    },
    'Vanguard European Stock Index Fund': {
        'starting_price': 15.33,
        'current_price': get_current_price('Vanguard European Stock Index Fund'),
        'years': get_years_of_fund(4, 5, 2007)
    },
    'Vanguard Eurozone Stk': {
        'starting_price': 162.46,
        'current_price': get_current_price('Vanguard Eurozone Stk'),
        'years': get_years_of_fund(4, 5, 2007)
    },
    'Vanguard Japan Stock Index Fund': {
        'starting_price': 135.12,
        'current_price': get_current_price('Vanguard Japan Stock Index Fund'),
        'years': get_years_of_fund(4, 5, 2007)
    }
}

passive_strategy_global_bonds = {
    'Vanguard Global Bond Index Fund EUR Hedged Acc': {
        'starting_price': 93.36,
        'current_price': get_current_price('Vanguard Global Bond Index Fund EUR Hedged Acc'),
        'years': get_years_of_fund(27, 2, 2014),

    },
    'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc': {
        'starting_price': 100,
        'current_price': get_current_price('Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc'),
        'years': get_years_of_fund(31, 3, 2014)
    },
    'Vanguard Euro Investment Grade Bond Index Fund EUR Acc': {
        'starting_price': 138.73,
        'current_price': get_current_price('Vanguard Euro Investment Grade Bond Index Fund EUR Acc'),
        'years': get_years_of_fund(4, 5, 2007)
    },
    'Vanguard U.S. Investment Grade Credit Index Fund EUR Acc': {
        'starting_price': 100,
        'current_price': get_current_price('Vanguard U.S. Investment Grade Credit Index Fund EUR Acc'),
        'years': get_years_of_fund(6, 8, 2008)
    },
    'Vanguard Euro Government Bond Index Fund EUR Acc': {
        'starting_price': 139.42,
        'current_price': get_current_price('Vanguard Euro Government Bond Index Fund EUR Acc'),
        'years': get_years_of_fund(4, 5, 2007)
    },
    'Vanguard U.S. Government Bond Index Fund EUR Hedged Acc': {
        'starting_price': 100,
        'current_price': get_current_price('Vanguard U.S. Government Bond Index Fund EUR Hedged Acc'),
        'years': get_years_of_fund(31, 3, 2016)
    },
    'iShares Global Government Bond Index Fund (LU) D2 EUR': {
        'starting_price': 99.56,
        'current_price': get_current_price('iShares Global Government Bond Index Fund (LU) D2 EUR'),
        'years': get_years_of_fund(18, 3, 2013)
    }
}

