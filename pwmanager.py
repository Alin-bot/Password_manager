import sys # for comand line arguments
import sqlite3 # for db
import cryptocode # for encrypting


real_master_password = 'master' # the master password

# get the arguments from the command line
def get_arguments() -> list:
    return sys.argv[1:6]


# verify if the master password from command line if correct
def verify_master_password(master_password: str):
    if not master_password == real_master_password:
        print('Wrong master password! Please try again.')
        return False
    return True


# display list of websites, usernames and password
def display_list(cursor):
    for row in cursor.execute('SELECT * FROM passwords'):
        decrypted = cryptocode.decrypt(row[3], real_master_password) # decrypting password
        print('website: ' + row[1] + '\t\tusername: ' + row[2] + '\t\tpassword: ' + decrypted)


# adding website, username and password to db
def add_new_element_in_list(website: str, username: str, password: str, cursor):
    encoded = cryptocode.encrypt(password, real_master_password) # encrypting password

    cursor.execute('INSERT INTO passwords(website, username, password) VALUES(?,?,?)', (website, username, encoded,))

    print('The username: "', username, '" with the password: "', password, '" has been added to the website:', website)


# get username and password based on the input website
def get_username_and_password(website: str, cursor):
    for row in cursor.execute('SELECT * FROM passwords WHERE website = ?', (website,)):
        decrypted = cryptocode.decrypt(row[3], real_master_password) # decrypting password
        print('website: ' + row[1] + '\t\tusername: ' + row[2] + '\t\tpassword: ' + decrypted)


# remove username and password based on the input website
def remove_username_and_password(website: str, cursor):

    cursor.execute('DELETE FROM passwords WHERE website=?', (website,))

    print('Your usernames and passwords for the website:', website, 'have been removed')

# closing the connection with the db
def close_db_connection(conn):
    conn.commit()
    conn.close

def main():
    arguments = get_arguments()

    if len(arguments) == 0:
        print('Give arguments to command!')
        return 0

    if not verify_master_password(arguments[0]):
        return 0
   
    conn = sqlite3.connect('pwmanager.db') # connecting to the data base or creating if not exists
    cursor = conn.cursor() # create cursor to execute queries

    # creating the table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT)''')

    if len(arguments) == 5: # adding new password option
        if arguments[1] == '-add':
            add_new_element_in_list(arguments[2], arguments[3], arguments[4], cursor)
            close_db_connection(conn)
            return 1

    elif len(arguments) == 3: # get or remove password option
        if arguments[1] == '-get':
            get_username_and_password(arguments[2], cursor)
            close_db_connection(conn)
            return 1

        elif arguments[1] == '-remove':
            remove_username_and_password(arguments[2], cursor)
            close_db_connection(conn)
            return 1

    elif len(arguments) == 2: # list passwords option
        if arguments[1] == '-list':
            display_list(cursor)
            close_db_connection(conn)
            return 1

    print('Wrong command! Please try again.')
    return 0


if __name__ == "__main__":
    main()