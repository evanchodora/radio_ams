#!/usr/bin/python3

import os
import sys
import datetime
from pyfiglet import figlet_format
from termcolor import colored
import sqlite3
import uuid


# Helper function to print text on the screen
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

def update_user():
    """ Update the user table with the current user and current time
    :param db: database file
    :param callsign: callsign of the currently active user
    """
    conn, c = open_db(db_file)  # Get db connection and cursor

    # Store current user callsign and update last active date
    c.execute('REPLACE INTO users VALUES (?,datetime(\'now\'))', (callsign,))
    
    close_db(conn)  # Close db connection

def get_users():
    """ Retrieve and print out all active users
    :param db: database file
    """
    conn, c = open_db(db_file)  # Get db connection and cursor
   
    users = []  # List to hold active users from db

    # Fetch all users in tables
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    close_db(conn)  # Close db connection
    
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

    open_menu()

def new_message():
    """ Write a new message and store in the database
    :param db: database file
    """
    os.system('clear')

    # Prompt user for message details
    out("Message editor:\n")

    recipient = input("Enter recipient callsign: ").upper()
    subject = input("Enter message subject: ")
    message = input("Enter message text: ")

    os.system('clear')

    # Review created message for user confirmation
    out("Message Details:\n")
    out("Recipient: " + recipient)
    out("Sender: " + callsign)
    out("Subject: " + subject)
    out("Message Text: " + message + "\n")
   
    # Function to confirm message is correct and to send
    def ask_confirm():
        send = input("Send message now? (Y/N) ")
        if send == "y" or send == "Y":
            send_message(recipient, subject, message)
            open_menu()
        elif send == "n" or send == "N":
            open_menu()        
        else:
            ask_confirm()

    # Ask for send confirmation
    ask_confirm()

def send_message(recipient, subject, message):
    """ Take the previously written message and write it into
        the database
    """
    conn, c = open_db(db_file)  # Open the database connection

    # Store message in the database
    read = 0
    m_id = str(uuid.uuid4())  # Create a UUID for each message
    data = (recipient, m_id, callsign, subject, message, read)
    c.execute('''INSERT into messages VALUES 
            (?,?,?,datetime(\'now\'),?,?,?)''', data) 

    close_db(conn)  # Close the database connection

    out("\nMessage sent!", color='green')
    out("Press Enter to continue...")
    input("")

    return

def get_messages():
    """ Get messages from the database for the currently
        logged in user
    """
    conn, c = open_db(db_file)  # Open the database connection

    messages = []

    # Fetch all messages from database
    c.execute('SELECT * FROM messages WHERE recipient=?', (callsign,))
    messages = c.fetchall()

    close_db(conn)  # Close database connection
    
    os.system('clear')
    out("Stored messages for " + callsign + ":\n")
    out("{:<3s}{:<8s}{:<25s}{:<22s}{:>7s}".format(
        "#","Sender","Subject","Date","Unread?"))
    out("-" * 65)

    num = 0
    for message in messages:
        num += 1
        sender = message[2]
        date = message[3]
        subject = message[4]
        
        if message[6] == 0:
            unread = "YES"
        else:
            unread = "NO"

        out("{:<3s}{:<8s}{:<25s}{:<22s}{:>7s}".format(
            str(num),sender,subject,date,unread))

    out("\nSelect a message to view or Enter key to return to main menu...")
    selection = input("")

    # Allow user to select a message or return to the main menu
    try:
        m_number = int(selection)
        if m_number > 0 and m_number <= num+1:
            open_message(messages[m_number-1])
        else:
            get_messages()
    except:
        if selection is '':
            open_menu()
        else:
            get_messages()

def open_message(message):
    ''' Open and dispay the details for a selected message
    :param message: message tuple passed from get_message()
    '''
    os.system('clear')  # Clear the screen

    # If its a new message, then mark it read
    if message[6] == 0:
        mark_read(message[1])

    out("Message Details:\n")
    out("Recipient: " + message[0])
    out("Sender: " + message[2])
    out("Subject: " + message[4])
    out("Date: " + message[3] + "\n")
    out("Body:\n")
    out(message[5])
    out("\n[d]elete?, [r]eply?, or Enter key to return to the messages menu")
    choice = input("")

    # User can either delete, reply, or exit
    if choice == 'd':
        delete_message(message[1])
    elif choice == 'r':
        new_message()
    elif choice == '':
        get_messages()
    else:
        open_message(message)

def mark_read(message_id):
    ''' Marks a specific message read according to the supplied
    message unique id
    :param message_id: specific message uuid
    '''
    conn, c = open_db(db_file)  # Open the database connection
    
    c.execute('UPDATE messages SET read=? WHERE m_id=?', (1, message_id))

    close_db(conn)  # Close database connection

    return

def delete_message(message_id):
    ''' Deletes a specific message according to the supplied
    message unique id
    :param message_id: specific message uuid
    '''
    conn, c = open_db(db_file)  # Open the database connection
    
    c.execute('DELETE FROM messages WHERE m_id=?', (message_id,))
    
    close_db(conn)  # Close database connection
   
    get_messages()

    return

def open_db(database):
    """ Helper functiom to open a database connection
    :param db: database file
    :return: connection object and cursor
    """
    # Make connection to storage database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    return conn, c

def close_db(conn):
    """ Helper function to commit and close database
    :param conn: database connection object
    """
    # Close database connection
    conn.commit()
    conn.close()

    return

def open_menu():
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
        get_users()
    elif choice == '2':
        get_messages()
    elif choice == '3':
        new_message()
    elif choice == '4':
        return
    else:
        open_menu()

def main():
    # Update the user database with the current user
    update_user()
    # Open the main menu
    open_menu()

    return

if __name__ == "__main__":
    # Name of database file
    db_file = 'radio_ams.db'

    # Get logged in user callsign
    callsign = None
    try:
        callsign = sys.argv[1].upper()
    except:
        out("Callsign not supplied", color="red")

    # Run main code
    if callsign is not None:
        main()


