import psycopg2

def setup_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''  CREATE TABLE IF NOT EXISTS customer (
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR(100) NOT NULL,
                            last_name VARCHAR(100) NOT NULL,
                            email VARCHAR(50) UNIQUE NOT NULL,
                            phone VARCHAR(9) UNIQUE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );''')
        cursor.execute('''  CREATE TABLE IF NOT EXISTS account (
                            id SERIAL PRIMARY KEY, 
                            customer_id INTEGER NOT NULL UNIQUE,
                            customer_number VARCHAR(7) UNIQUE NOT NULL,
                            password TEXT NOT NULL, 
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
                        );''')
        cursor.execute('''  CREATE TABLE IF NOT EXISTS sub_account (
                            id SERIAL PRIMARY KEY,
                            account_id INTEGER NOT NULL,
                            currency CHAR(3) NOT NULL,
                            balance NUMERIC(15, 2) DEFAULT 0 CHECK (balance >= 0),
                            FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
                        );''')
        cursor.execute('''  CREATE TABLE IF NOT EXISTS card (
                            id SERIAL PRIMARY KEY,
                            sub_account_id INTEGER NOT NULL UNIQUE,
                            card_number VARCHAR(16) UNIQUE NOT NULL,
                            expiry_date DATE NOT NULL,
                            cvv VARCHAR(3) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (sub_account_id) REFERENCES sub_account(id) ON DELETE CASCADE
                        );''')
        cursor.execute('''  CREATE TABLE IF NOT EXISTS transactions (
                            id SERIAL PRIMARY KEY,
                            sub_account_id INTEGER NOT NULL, 
                            transaction_type TEXT, 
                            amount NUMERIC(10, 2) CHECK (amount > 0),
                            description TEXT, 
                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            FOREIGN KEY (sub_account_id) REFERENCES sub_account(id) ON DELETE CASCADE
                        );''')
        cursor.execute('''  CREATE TABLE IF NOT EXISTS daily_limits (
                            id SERIAL PRIMARY KEY, 
                            sub_account_id INTEGER NOT NULL,
                            daily_limit NUMERIC(10, 2), 
                            set_date DATE,
                            changes_today INTEGER DEFAULT 0,
                            FOREIGN KEY (sub_account_id) REFERENCES sub_account(id) ON DELETE CASCADE
                        );''')
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error setting up the database: {e}")
        raise