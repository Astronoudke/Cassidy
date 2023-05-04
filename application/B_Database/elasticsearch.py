from elasticsearch import Elasticsearch


class DatabaseManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.es = Elasticsearch([{"host": self.host, "port": self.port}])

    def close(self):
        # Elasticsearch does not require closing connections explicitly
        pass

    def create_indices(self):
        self.create_categories_index()
        self.create_forums_index()
        self.create_discussions_index()
        self.create_messages_index()

    def create_categories_index(self):
        self.es.indices.create(index="categories", ignore=400)

    def create_forums_index(self):
        self.es.indices.create(index="forums", ignore=400)

    def create_discussions_index(self):
        self.es.indices.create(index="discussions", ignore=400)

    def create_messages_index(self):
        self.es.indices.create(index="messages", ignore=400)

    def add_category(self, name):
        document = {"name": name}
        response = self.es.index(index="categories", doc_type="_doc", body=document)
        return response["_id"]

    def add_forum(self, name, base_url, category_id):
        document = {"name": name, "base_url": base_url, "category_id": category_id}
        response = self.es.index(index="forums", doc_type="_doc", body=document)
        return response["_id"]

    def edit_forum(self, id, name, base_url):
        updated_document = {"name": name, "base_url": base_url}
        self.es.update(index="forums", doc_type="_doc", id=id, body={"doc": updated_document})

    def delete_forum(self, id):
        self.es.delete(index="forums", doc_type="_doc", id=id)


if __name__ == "__main__":
    # Initialize the database manager
    manager = DatabaseManager(host='localhost', port=9200)

    # Connect to the database
    manager.connect()

    # Create the indices
    manager.create_indices()

    # Add a category
    category_id = manager.add_category("Energy")

    # Add data to the forums index
    forum_id = manager.add_forum("Example Forum", "https://example.com/forum", category_id)
    print(f"Added forum with ID: {forum_id}")

    # Close the connection
    manager.close()