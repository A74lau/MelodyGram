import sqlite3

# Connect to or create the database
conn = sqlite3.connect('music.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create a table to store music information
c.execute(""" CREATE TABLE IF NOT EXISTS music (
                id TEXT,
                title TEXT,
                artist TEXT,
                link TEXT) """)


# create a function that updates the database
def update(id, title, artist, link):

    # 'id' must be wrapped in square brackets because a string is being interpreted as a list of characters
    c.execute('''SELECT * FROM music WHERE id = ?''', [id])
    data_fetch = c.fetchall()

    # if the song is not in the database, then it should be added
    if not data_fetch:
        c.execute('INSERT INTO music VALUES (?,?,?,?)' , (id, title, artist, link))
        print(title + " by " + artist + " has been added to the playlist")
    else:
        print("This song is already in your playlist!")
    

    #commit changes and close connection
    conn.commit()

def close_database():
    conn.close()





