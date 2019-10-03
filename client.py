import os
import sys
import datetime
from pyfiglet import figlet_format
from termcolor import colored
import sqlite3


# Function to print text on the screen
def out(string, color="white", font="slant", figlet=False):
    if not figlet:
        print(colored(string, color))
    else:
        print(colored(figlet_format(string, font=font), color))

# Function to get computer system uptime
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

def update_user(db, callsign):
    """ Update the user table with the current user and current time
    :param db: database file
    :param callsign: callsign of the currently active user
    """
    conn, c = open_db(db)  # Get db connection and cursor

    # Store current user callsign and update last active date
    c.execute('REPLACE INTO users VALUES (?,datetime(\'now\'))', (callsign,))
    
    close_db(conn)  # Close db connection

def get_users(db, callsign):
    """ Retrieve and print out all active users
    :param db: database file
    """
    conn, c = open_db(db)  # Get db connection and cursor
   
    users = []  # List to hold active users from db

    # Fetch all users in tables
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    
    # Store users from database
    for row in rows:
        users.append((row[0], row[1]))

    # Print out active users
    os.system('clear')
    out("Here is a list of current users:\n")
    out("{:<10s}{:>24s}".format("Callsign","Last Active Time (UTC)"))
    out("-" * 34)
    for user in users:
        out("{:<10s}{:>24s}".format(user[0], user[1]))

    # Prompt for return to the main menu
    out("\nPress Enter key to return to menu...")
    input("")

    close_db(conn)  # Close db connection
    open_menu(db, callsign)

def new_message(db, callsign):
    """ Write a new message and store in the database
    :param db: database file
    """
    os.system('clear')

    out("Message editor:\n")

    recipient = input("Enter recipient callsign: ")
    subject = input("Enter message subject: ")
    message = input("Enter message text: ")

    os.system('clear')

    out("Message Details:\n")
    out("Recipient: " + recipient)
    out("Sender: " + callsign)
    out("Subject: " + subject)
    out("Message Text: " + message + "\n")
   
    # Function to confirm message is correct and to send
    def ask_confirm():
        send = input("Send message now? (Y/N) ")
        if send == "y" or send == "Y":
            send_message(db, callsign, recipient, subject, message)
            open_menu(db, callsign)
        elif send == "n" or send == "N":
            open_menu(db, callsign)        
        else:
            ask_confirm()

    # Ask for send confirmation
    ask_confirm()

def send_message(db, callsign, recipient, subject, message):
    """ Take the previously written message and write it into
        the database
    """
    conn, c = open_db(db)  # Open the database connection

    # Store message in the database
    read = 0
    data = (recipient, callsign, subject, message, read)
    c.execute('INSERT into messages VALUES (?,?,datetime(\'now\'),?,?,?)', data) 

    close_db(conn)  # Close the database connection

    out("\nMessage sent!", color='green')
    out("Press Enter to continue...")
    input("")

def get_messages(db, callsign):
    """ Get messages from the database for the currently
        logged in user
    """
    conn, c = open_db(db)  # Open the database connection

    messages = []

    # Fetch all messages from database
    c.execute('SELECT * FROM messages')
    rows = c.fetchall()

    os.system('clear')

    for row in rows:
        print(row)

    close_db(conn)  # Close database connection
    
    out("\nPress Enter key to return to menu...")
    input("")
    open_menu(db, callsign)

def open_db(db):
    """ Helper functiom to open a database connection
    :param db: database file
    :return: connection object and cursor
    """
    # Make connection to storage database
    conn = sqlite3.connect(db)
    c = conn.cursor()

    return conn, c

def close_db(conn):
    """ Helper function to commit and close database
    :param conn: database connection object
    """
    # Close database connection
    conn.commit()
    conn.close()

def open_menu(db, callsign):
    os.system('clear')
    out("Local Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out("System Uptime: " + str(round(get_uptime()/60/60,2)) + " hours")
    out("System Callsign: AF5E-1")
    out("AF5E AMS", color="green", figlet=True)
    out("Welcome to the AF5E AX.25 messaging server (AMS) system!")
    print(colored("You are currently connected as callsign: ", 'white') + 
            colored(callsign + "\n", 'red'))
    out("Select an option from the menu below:\n")
    out("   1. View Online Users")
    out("   2. View Messages")
    out("   3. Create New Message")
    out("   4. Logoff\n")

    choice = input("")

    if choice == '1':
        get_users(db, callsign)
    elif choice == '2':
        get_messages(db, callsign)
    elif choice == '3':
        new_message(db, callsign)
    elif choice == '4':
        pass
    else:
        open_menu(db, callsign)

def main(db, callsign):
    # Update the user database with the current user
    update_user(db_file, callsign)
    # Open the main menu
    open_menu(db, callsign)


if __name__ == "__main__":

    # Name of database file
    db_file = 'radio_ams.db'

    # Get logged in user callsign
    callsign = None
    try:
        callsign = sys.argv[1]
    except:
        out("Callsign not supplied", color="red")

    # Run main code
    if callsign is not None:
        main(db_file, callsign)


