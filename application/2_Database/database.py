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
        self.create_forums_table()
        self.create_discussions_table()
        self.create_messages_table()

    def create_forums_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS forums (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            base_url VARCHAR(255)
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