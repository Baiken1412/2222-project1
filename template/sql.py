import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password ='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, admin=1)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False
        

        # Function to get a user ID from the database
    def get_user_id(username):
        # Connect to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Get the user ID
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()

        # Close the database connection
        conn.close()

        # If the user was found, return the ID
        if result:
            return result[0]
        else:
            return None

    # Function to insert a message into the database
    def insert_message(user_id, message):
        # Connect to the database
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()

        # Insert the message into the database
        c.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (user_id, message))
        conn.commit()

        # Close the database connection
        conn.close()
