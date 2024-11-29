import psycopg2

def setup_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS card (
                          id SERIAL PRIMARY KEY, 
                          number TEXT UNIQUE
                       );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                          id SERIAL PRIMARY KEY, 
                          card_id TEXT, 
                          pin TEXT, 
                          balance NUMERIC(10, 2) DEFAULT 0, 
                          currency CHAR(3), 
                          failed_attempts INTEGER DEFAULT 0, 
                          locked BOOLEAN DEFAULT FALSE, 
                          FOREIGN KEY (card_id) REFERENCES card(number)
                       );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                          id SERIAL PRIMARY KEY,
                          account_id INTEGER, 
                          transaction_type TEXT, 
                          amount NUMERIC(10, 2), 
                          date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                          FOREIGN KEY (account_id) REFERENCES account(id)
                       );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS daily_limits (
                          id SERIAL PRIMARY KEY, 
                          account_id INTEGER,
                          daily_limit NUMERIC(10, 2), 
                          set_date TEXT,
                          changes_today INTEGER DEFAULT 0,
                          FOREIGN KEY (account_id) REFERENCES account(id)
                       );''')
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error setting up the database: {e}")
        raise