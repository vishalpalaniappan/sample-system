import uuid
import time
from random import randrange
import sqlite3
import atexit

LOGGER_INTERVAL = 0.1

def exit_handler():
    '''
        Close the database connection on exit.
    '''
    print("Shutting down logger.")
    global conn, cursor
    cursor.close()
    conn.commit()
    conn.close()
    print("Shutdown logger.")

def generate_data():
    '''
        Generates a random data node.
    '''
    return {
        "id": uuid.uuid4(),
        "temperature":randrange(10),
        "speed":randrange(10),
    }

def execute_cursor(data):
    '''
        Inserts data into the database.
    '''    
    global conn, cursor

    date = time.time()
    uid = data["id"]
    temperature = data["temperature"]
    speed = data["speed"]

    cursor.execute(f'''
        INSERT INTO tempdata VALUES (
        '"{date}"',
        '"{uid}"',
        '"{temperature}"',
        '"{speed}"')
    ''')

    conn.commit()

def run_logger():
    '''
        Runs the logger
    '''
    global conn, cursor
    conn = sqlite3.connect("../data.db", check_same_thread=False, timeout=10)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tempdata
                (date real, id text, temperature real, speed real)''')

    while(True):
        data = generate_data()
        print(data)
        execute_cursor(data)
        time.sleep(LOGGER_INTERVAL)

if __name__ == "__main__":
    atexit.register(exit_handler)
    run_logger()