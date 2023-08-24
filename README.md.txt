# Investment growth calculator
#### Video Demo:  <https://youtu.be/MCyUckG6WkQ>
#### Description: 
## data.py file:

---

This file contains all the data that are going to be used in the `main.py` file.

Certainly! Here's the README file with detailed explanations for the provided code:

---

# Investment Analysis README

This file contains all the data and code used for investment analysis.

## Libraries

The following libraries are imported for the analysis:

- `dateutil`: Used for relative date calculations.
- `datetime`: Provides functionality for working with dates.
- `requests`: Enables making HTTP requests.
- `bs4` (BeautifulSoup): Used for HTML parsing.

## Pension Data

The `pension_data` dictionary contains pension percentages based on age. It maps age values to their corresponding pension percentages. This data is used for pension calculations in the analysis.

## Funds

The `funds` dictionary maps investment fund names to their respective URLs. Each fund is represented by a key-value pair, where the key is the fund name and the value is the URL to the fund's website. This data is used for retrieving information about the funds.

## `get_current_price(fund_name: str)`

This function retrieves the current price of a fund from its website.

### Parameters

- `fund_name` (str): The name of the fund for which to retrieve the current price.

### Functionality

This function takes the name of a fund as input and retrieves its current price by scraping the fund's webpage using BeautifulSoup. It makes an HTTP GET request to the fund's URL using the `requests` library and parses the HTML content using BeautifulSoup. The current price is extracted from the HTML structure of the webpage. For the special case of the 'Vanguard FTSE All-World UCITS ETF' fund, the price is located in a different HTML element.

### Returns

- `price` (float): The current price of the specified fund.

## `get_years_of_fund(fund_name: str)`

This function calculates the number of years since the release of a fund.

### Parameters

- `fund_name` (str): The name of the fund for which to calculate the number of years.

### Functionality

This function takes the name of a fund as input and calculates the number of years since its release. It retrieves the fund's webpage using the `requests` library and parses the HTML content using BeautifulSoup. The release date of the fund is extracted from the HTML structure of the webpage. The release date is converted to a `datetime` object, and the current date is obtained using `datetime.now()`. The `dateutil.relativedelta` module is used to calculate the difference between the two dates in years and months, resulting in the number of years as a float.

### Returns

- `years_of_fund` (float): The number of years since the release of the specified fund.

## Passive Strategy Funds

The `passive_strategy_funds` dictionary contains information about various passive investment funds.

Each fund is represented by a key-value pair, where the key is the fund name and the value is another dictionary. The inner dictionary contains the following data:

- `starting_price` (float): The starting price of the fund.
- `current_price` (float): The current price of the fund (retrieved using the `get_current_price` function).
- `years` (float): The number of years since the release of the fund (calculated using the `get_years_of_fund` function).

This data is used for further analysis and reporting on the performance of passive investment funds.

---

This README file provides detailed information about the code and data used for investment analysis. It serves as a guide to understanding and utilizing the code effectively for investment fund analysis purposes.

---

## main.py file:

---


This file contains the code for investment analysis and provides several functions for various calculations related to investments and financial planning.

## Libraries

The following libraries are imported for the analysis:

- `numpy_financial as npf`: Used for financial calculations.
- `matplotlib.pyplot as plt`: Used for plotting investment data.

## Constants

- `NATIONAL_PENSION`: A constant representing the national pension amount.

## Functions

### `annual_return_calculation(num_of_funds: int)`

This function calculates the annual return for a given fund.

#### Parameters

- `num_of_funds` (int): The number of funds for which to calculate the annual return.

#### Functionality

The function prompts the user to enter the starting price, current price, and number of years for each fund. It then calculates the annual return for the fund by taking the difference between the current and starting prices, dividing it by the starting price, and dividing the result by the number of years.

#### Returns

- `annual_return` (float): The annual return for the specified fund.

### `portfolio_return_calculation(percentages: list, annual_returns: list)`

This function calculates the total return for a portfolio of funds.

#### Parameters

- `percentages` (list): A list of percentages representing the allocation of funds in the portfolio.
- `annual_returns` (list): A list of annual returns for each fund in the portfolio.

#### Functionality

The function calculates the total return for the portfolio by multiplying each fund's annual return by its corresponding percentage and summing up the results.

#### Returns

- `total_return` (float): The total return for the portfolio.

### `passive_strategy_return(data: dict)`

This function calculates the return for a passive investment strategy.

#### Parameters

- `data` (dict): A dictionary containing information about various passive investment funds.

#### Functionality

The function calculates the average annual return for each fund in the `data` dictionary by taking the difference between the current and starting prices, dividing it by the starting price, and dividing the result by the number of years. It then uses the `portfolio_return_calculation` function to calculate the overall return for the passive strategy.

#### Returns

- `strategy_return` (float): The overall return for the passive investment strategy.

### `value_after_inflation(money, years)`

This function calculates the value of money after a certain number of years, accounting for inflation.

#### Parameters

- `money` (float): The initial amount of money.
- `years` (int): The number of years.

#### Functionality

The function applies an annual inflation rate of 3% to the initial amount of money for each year, subtracting the resulting amount from the previous year's total. The final amount is rounded to two decimal places.

#### Returns

- `value_after_inflation` (float): The value of money after the specified number of years, accounting for inflation.

### `return_of_investment(final_average_return)`

This function calculates the return on investment based on the average annual return and additional investment parameters.

#### Parameters

- `final_average_return` (float): The average annual return on investment.

#### Functionality

The function prompts the user to enter the monthly contribution, investment duration in years, and annual adjustment rate. It then calculates the investment value, total contribution, and profit over the investment period. The function also plots a graph showing the value of the investment over time.

#### Returns

- `investment_value` (float): The final value of the investment.
- `total_contribution` (float): The total amount contributed to the investment.
- `profit` (float

): The profit earned from the investment.

### `pension_calculation()`

This function calculates the total pension amount based on the average salary and years of work.

#### Parameters

None

#### Functionality

The function prompts the user to enter the average salary and years of work. It then calculates the total pension amount by adding the national pension to the product of the average salary and the pension data for the specified number of years.

#### Returns

- `total_pension` (float): The total pension amount.

### `inflation_calculation()`

This function calculates the price of a product after a certain number of years, accounting for inflation.

#### Parameters

None

#### Functionality

The function prompts the user to enter the inflation rate, number of years, and the current price of the product. It then calculates the final price by applying the inflation rate to the current price for each year.

#### Returns

- `price` (float): The final price of the product after accounting for inflation.

### `target_amount(target: int, years: int, annual_return: int)`

This function calculates the monthly contribution required to achieve a target investment amount within a specified time frame.

#### Parameters

- `target` (int): The target investment amount.
- `years` (int): The investment duration in years.
- `annual_return` (int): The expected average annual return.

#### Functionality

The function uses the `npf.pmt` function from the `numpy_financial` library to calculate the monthly contribution required to reach the target amount. It returns the calculated monthly contribution.

#### Returns

- `monthly_contribution` (float): The monthly contribution required to achieve the target investment amount.

## Main Program

The main program is an infinite loop that presents a menu of options to the user and performs the corresponding calculations based on the user's input.

The available options are:

1. Calculate Investment Return
    - Sub-menu options:
        1. Multifund Passive Strategy return
        2. Other

2. Calculate Investment Value

3. Calculate Pension

4. Example of Inflation Calculation

5. Calculate Capital Value After Years

6. Calculate Monthly Investment Amount to Reach a Target

7. Exit

The program prompts the user to select an option and performs the corresponding calculations based on the chosen option.

---



