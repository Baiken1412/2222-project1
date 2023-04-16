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
            Id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, admin=1)
        self.add_user('Andy', '123')
       

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES(NULL, '{username}', '{password}', {admin})
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
    def get_user_id(self, username):
        # Get the user ID
        self.cur.execute("SELECT Id FROM Users WHERE username = ?", (username,))
        result = self.cur.fetchone()

        # If the user was found, return the ID
        if result:
            return result[0]
        else:
            return None

  
    def insert_message(self, sender_id, receiver_id, message):
        # Insert the message into the database
        sql_cmd = """
                INSERT INTO Messages
                VALUES(NULL, {sender_id}, {receiver_id}, '{message}')
            """

        sql_cmd = sql_cmd.format(sender_id=sender_id, receiver_id=receiver_id, message=message)

        self.execute(sql_cmd)
        self.commit()

    def get_conversation(user1_id, user2_id):
    # Connect to the database
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()

        # Get the conversation between the two users
        c.execute("SELECT message FROM Messages WHERE sender_id = ? AND receiver_id = ? OR sender_id = ? AND receiver_id = ?", (user1_id, user2_id, user2_id, user1_id))
        result = c.fetchall()

        # Close the database connection
        conn.close()

        # Return the conversation
        return result