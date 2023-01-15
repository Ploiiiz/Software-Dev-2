import sqlite3
import coinranking

def search(find):
    coinranking.data()
    # Connect to the database
    conn = sqlite3.connect("coinranking.db")

    # Create a cursor
    cursor = conn.cursor()


    query = '''
    SELECT name,symbol,price,uuid,change FROM coinrankingdata WHERE symbol = ?
    '''
    # Execute the SELECT statement
    cursor.execute(query, (find,))

    # Iterate through the rows returned by the SELECT statement and print out the data for each column
    for (name, symbol, price,uuid,change) in cursor:
        uuid = uuid
        print(f'Name: {name}')
        print(f'Price: {price}')
        print(f'Change: {change}')
    



    # Close the cursor and connection
    cursor.close()
    conn.close()

    return uuid  
# search('BTC')