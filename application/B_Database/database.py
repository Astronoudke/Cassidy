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
            title VARCHAR(255),
            link VARCHAR(255),
            creation_date DATE,
            last_post_time TIMESTAMP,
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
            discussion_id INT,
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


if __name__ == "__main__":
    # Initialize the database manager
    manager = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')

    # Connect to the database
    manager.connect()

    category_id = manager.add_category("Energy")

    # Add data to the forums table
    forum_id = manager.add_forum("Example Forum", "https://example.com/forum", category_id)
    print(f"Added forum with ID: {forum_id}")

    # Close the connection
    manager.close()
