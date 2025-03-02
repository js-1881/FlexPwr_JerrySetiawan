# Task 1: Jerry Setiawan

import sqlite3              # Import the sqlite3 library

def connect_db():
    """"connect to the database"""
    return sqlite3.connect("trades.sqlite")


# Task 1.1a: Compute total buy volume
def compute_total_buy_volume ():
    """computes total buy volume"""

    connection = connect_db() #connect to the database using previous def
    cursor = connection.cursor()

    # Execute query that calculates the sum of the 'quantity' column for all trades 
    # where the 'side' is 'buy'
    cursor.execute("""SELECT SUM(quantity) FROM epex_12_20_12_13 WHERE side = 'buy'""")
    

    # Fetch the result of the query, take the first element [0]
    result = cursor.fetchone()[0]

    connection.close() #close database'

    return result if result else 0 # Return 0 if there are no 'buy' trades


# Task 1.1b: Compute total sell volume
def compute_total_sell_volume ():
    """computes total sell volume"""

    connection = connect_db() #connect to the database using previous def
    cursor = connection.cursor()

    # Execute query that calculates the sum of the 'quantity' column for all trades 
    # where the 'side' is 'sell'
    cursor.execute("""SELECT SUM(quantity) FROM epex_12_20_12_13 WHERE side = 'sell'""")
    

    # Fetch the result of the query, take the first element [0]
    result = cursor.fetchone()[0]

    connection.close() #close database'

    return result if result else 0 # Return 0 if there are no 'buy' trades


# print the calculated volume
print("Total Buy Volume:", compute_total_buy_volume())
print("Total Sell Volume:", compute_total_sell_volume())






# Task 1.2 computing the profit/loss
def compute_pnl(strategy_id: str)-> float:
    """computes profit and loss of each strategy"""
    connection = connect_db()
    cursor = connection.cursor()

    #calculating total profit/loss based on buy/sell transaction
    #when sell, quantity * price
    #when buy, -quantity * price
    cursor.execute("""
        SELECT SUM(
            CASE
                WHEN side = 'sell' THEN quantity * price
                WHEN side = 'buy' THEN -quantity * price
                ELSE 0  
            END  
        ) FROM epex_12_20_12_13 WHERE strategy = ? """,
        (strategy_id,))
            

    result = cursor.fetchone()[0]
    connection.close()

    return result if result else 0




# Fetch all unique strategy IDs from the database
def get_all_strategies():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT strategy FROM epex_12_20_12_13")

    # Extracting strategy names inside the table
    strategies = [row[0] for row in cursor.fetchall()]

    connection.close()
    return strategies


# Compute and print PnL for all strategies
    # calling all the listed strategies
strategies = get_all_strategies()

# Loop through each strategy in the list and compute its PnL
for strategy in strategies:
    pnl = compute_pnl(strategy)  # Compute profit/loss for the current strategy

    print(f"{strategy}: {pnl} EUR") # Print the strategy name and its profit/loss




# Task 1.3 

from flask import Flask, jsonify # import flask for creating a web API, convert to json
from datetime import datetime # import datetime to generate timestamps


# Create a flask web app
app = Flask(__name__)

# Defines a URL path and links it to a function to expose the profit/loss computation
@app.route("/pnl/<strategy_id>", methods=["GET"])

def get_pnl(strategy_id):
    """API endpoint to get the profit/loss of a strategy"""

    # compute the amount for a given strategy
    pnl_amount = compute_pnl(strategy_id)

    # create a JSON response
    response = {
        "strategy": strategy_id,
        "value": pnl_amount,
        "unit": "euro",
        "capture time": datetime.utcnow().isoformat() #timestamp
    }

    return jsonify(response) #return JSON response to the user


# run the flask application if the script is executed
if __name__ == "__main__":
    app.run(debug=True) # run API in debug mode
    