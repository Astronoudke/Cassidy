import mysql.connector
import json


class DatabaseManager:
    def __init__(self, user, password, host, database_name):
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database_name)
        self.cursor = self.cnx.cursor(buffered=True)

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def create_tables(self):
        self.create_categories_table()
        self.create_forums_table()
        self.create_discussions_table()
        self.create_authors_table()
        self.create_messages_table()

    def export_table_to_json(self, table_name, file_path):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]  # Fetching column names

        # Converting tuples to dictionary
        dict_rows = [dict(zip(column_names, row)) for row in rows]

        # Writing to file
        with open(file_path, 'w') as f:
            json.dump(dict_rows, f, default=str)  # default=str is for handling date and datetime objects

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
            forum_id INT,
            FOREIGN KEY (forum_id) REFERENCES forums(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_authors_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS authors (
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
            creation_date TIMESTAMP,
            author_id INT,
            discussion_id INT,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (discussion_id) REFERENCES discussions(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def create_articles_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            text LONGTEXT,
            category_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        '''
        self.cursor.execute(query)
        self.cnx.commit()

    def clear_category_table(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        self.cursor.execute("TRUNCATE TABLE categories;")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()

    def clear_forum_table(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        self.cursor.execute("TRUNCATE TABLE forums;")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()

    def clear_discussion_table(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        self.cursor.execute("TRUNCATE TABLE discussions;")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()

    def clear_author_table(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        self.cursor.execute("TRUNCATE TABLE authors;")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()

    def clear_message_table(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        self.cursor.execute("TRUNCATE TABLE messages;")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()

    def add_category(self, name):
        query = "INSERT INTO categories (name) VALUES (%s)"
        self.cursor.execute(query, (name,))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_category(self, id, name):
        query = "UPDATE categories SET name = %s WHERE id = %s"
        self.cursor.execute(query, (name, id))
        self.cnx.commit()

    def select_category(self, id):
        query = "SELECT * FROM categories WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
            }

    def delete_category(self, id):
        query = "DELETE FROM categories WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_forum(self, name, base_url, description, category_id):
        query = "INSERT INTO forums (name, base_url, description, category_id) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, base_url, description, category_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_forum(self, id, name, base_url):
        query = "UPDATE forums SET name = %s, base_url = %s WHERE id = %s"
        self.cursor.execute(query, (name, base_url, id))
        self.cnx.commit()

    def select_forum(self, id):
        query = "SELECT * FROM forums WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'base_url': result[2],
                'description': result[3],
                'category_id': result[4],
            }
        else:
            return None

    def delete_forum(self, id):
        query = "DELETE FROM forums WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_discussion(self, name, link, forum_id):
        query = "INSERT INTO discussions (name, link, forum_id) " \
                "VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, link, forum_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_discussion(self, id, name, link):
        query = "UPDATE discussions SET name = %s, link = %s WHERE id = %s"
        self.cursor.execute(query, (name, link, id))
        self.cnx.commit()

    def select_discussion(self, via_id: bool = False, via_link: bool = False, id: str = None, link: str = None):
        if via_id:
            query = "SELECT * FROM discussions WHERE id = %s"
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
        else:
            query = "SELECT * FROM discussions WHERE link = %s"
            self.cursor.execute(query, (link,))
            result = self.cursor.fetchone()
        self.cursor.execute(query, (id,))
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'link': result[2],
                'forum_id': result[3]
            }
        else:
            return None

    def select_discussions_by_forum_id(self, forum_id: int):
        query = "SELECT * FROM discussions WHERE forum_id = %s"
        self.cursor.execute(query, (forum_id,))
        results = self.cursor.fetchall()
        discussions = []

        if results:
            for result in results:
                discussions.append({
                    'id': result[0],
                    'name': result[1],
                    'link': result[2],
                    'forum_id': result[3]
                })
            return discussions
        else:
            return None

    def delete_discussion(self, id):
        query = "DELETE FROM discussions WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_message(self, text, author_id, discussion_id):
        query = "INSERT INTO messages (text, author_id, discussion_id) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (text, author_id, discussion_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_message(self, id, text):
        query = "UPDATE messages SET text = %s WHERE id = %s"
        self.cursor.execute(query, (text, id))
        self.cnx.commit()

    def select_message(self, id):
        query = "SELECT * FROM messages WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'text': result[1],
                'author_id': result[3],
                'discussion_id': result[4]
            }
        else:
            return None

    def select_messages_by_discussion_id(self, discussion_id):
        query = "SELECT * FROM messages WHERE discussion_id = %s"
        self.cursor.execute(query, (discussion_id,))
        results = self.cursor.fetchall()
        messages = []

        if results:
            for result in results:
                messages.append({
                    'id': result[0],
                    'text': result[1],
                    'author_id': result[2],
                    'discussion_id': result[3]
                })
            return messages
        else:
            return None

    def select_messages_by_forum_id(self, forum_id):
        query = """
        SELECT messages.* 
        FROM messages
        JOIN discussions ON messages.discussion_id = discussions.id
        WHERE discussions.forum_id = %s
        """
        self.cursor.execute(query, (forum_id,))
        results = self.cursor.fetchall()
        messages = []

        if results:
            for result in results:
                messages.append({
                    'id': result[0],
                    'text': result[1],
                    'author_id': result[2],
                    'discussion_id': result[3]
                })
            return messages
        else:
            return None

    def select_message_by_discussion_date_author_and_text(self, discussion_id, author_id, text):
        query = "SELECT * FROM messages WHERE discussion_id = %s AND author_id = %s AND text = %s"
        print(query)
        print("Discussion id: " + str(discussion_id))
        print("Author id: " + str(author_id))
        print("Text: " + str(text))
        self.cursor.execute(query, (discussion_id, author_id, text))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'text': result[1],
                'author_id': result[2],
                'discussion_id': result[3]
            }
        else:
            return None

    def delete_message(self, id):
        query = "DELETE FROM messages WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_author(self, username, forum_id):
        query = "INSERT INTO authors (username, forum_id) VALUES (%s, %s)"
        self.cursor.execute(query, (username, forum_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def edit_author(self, id, username):
        query = "UPDATE authors SET username = %s WHERE id = %s"
        self.cursor.execute(query, (username, id))
        self.cnx.commit()

    def select_author(self, id):
        query = "SELECT * FROM authors WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'forum_id': result[2]
            }
        else:
            return None

    def select_author_by_username_and_forum_id(self, username, forum_id):
        query = "SELECT * FROM authors WHERE username = %s AND forum_id = %s"
        self.cursor.execute(query, (username, forum_id))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'forum_id': result[2]
            }
        else:
            return None

    def delete_author(self, id):
        query = "DELETE FROM authors WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()

    def add_article(self, article_dict, category_id):
        query = "INSERT INTO articles (title, text, category_id) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (article_dict['title'], json.dumps(article_dict), category_id))
        self.cnx.commit()
        return self.cursor.lastrowid

    def select_article(self, id):
        query = "SELECT * FROM articles WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'title': result[1],
                'text': json.loads(result[2]),
                'category_id': result[3]
            }
        else:
            return None

    def delete_article(self, id):
        query = "DELETE FROM articles WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.cnx.commit()
