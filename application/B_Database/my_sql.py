import mysql.connector


class DatabaseManager:
    def __init__(self, user, password, host, database_name):
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database_name)
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def create_tables(self):
        self.create_categories_table()
        self.create_forums_table()
        self.create_discussions_table()
        self.create_users_table()
        self.create_messages_table()

    def create_categories_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_forums_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS forums (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            base_url VARCHAR(255),
            description VARCHAR(400),
            category_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_discussions_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS discussions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            link VARCHAR(255),
            creation_date DATE,
            views INT,
            replies INT,
            last_post_time TIMESTAMP,
            forum_id INT,
            FOREIGN KEY (forum_id) REFERENCES forums(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_users_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            forum_id INT,
            FOREIGN KEY (forum_id) REFERENCES forums(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_messages_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT,
            date TIMESTAMP,
            author VARCHAR(255),
            user_id INT,
            discussion_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (discussion_id) REFERENCES discussions(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def add_category(self, name):
        query = "INSERT INTO forums (name) VALUES (%s)"
        self.cursor.execute(query, (name,))
        self.cnx.commit()
        return self.cursor.lastrowid

    def add_forum(self, name, base_url, category_id):
        query = "INSERT INTO forums (name, base_url, category_id) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, base_url, category_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_forum(self, id, name, base_url):
        query = "UPDATE forums SET name = %s, base_url = %s WHERE id = %s"
        self.cursor.execute(query, (name, base_url, id))
        self.cnx.commit()

    def delete_forum(self, id):
        query = "DELETE FROM forums WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_discussion(self, name, link, creation_date, views, replies, last_post_time, forum_id):
        query = "INSERT INTO discussions (name, link, creation_date, views, replies, last_post_time, forum_id) " \
                "VALUES (%s, %s, %s, %s, %s %s, %s)"
        self.cursor.execute(query, (name, link, creation_date, views, replies, last_post_time, forum_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_discussion(self, id, name, link, creation_date, views, replies, last_post_time):
        query = "UPDATE discussions SET name = %s, link = %s, creation_date = %s, views = %s, replies = %s, " \
                "last_post_time = %s WHERE id = %s"
        self.cursor.execute(query, (name, link, creation_date, views, replies, last_post_time, id))
        self.cnx.commit()

    def select_discussion(self, id):
        query = "SELECT * FROM discussions WHERE id = %s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def delete_discussion(self, id):
        query = "DELETE FROM discussions WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_message(self, text, creation_date, user_id, discussion_id):
        query = "INSERT INTO messages (text, creation_date, user_id, discussion_id) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (text, creation_date, user_id, discussion_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_message(self, id, text):
        query = "UPDATE messages SET text = %s WHERE id = %s"
        self.cursor.execute(query, (text, id))
        self.cnx.commit()

    def delete_message(self, id):
        query = "DELETE FROM messages WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_user(self, username, forum_id):
        query = "INSERT INTO users (username, forum_id) VALUES (%s, %s)"
        self.cursor.execute(query, (username, forum_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_user(self, id, username):
        query = "UPDATE users SET username = %s WHERE id = %s"
        self.cursor.execute(query, (username, id))
        self.cnx.commit()

    def delete_user(self, id):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()


if __name__ == "__main__":
    # Initialize the database manager
    manager = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')

    # Connect to the database
    manager.connect()

    # Create the tables
    manager.create_tables()

    # Close the connection
    manager.close()
