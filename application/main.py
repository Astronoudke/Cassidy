from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from B_Database.my_sql import DatabaseManager

if __name__ == "__main__":
    db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
    db.connect()
    forum = db.select_forum(id=8)
    db.close()

    psv_collector = ForumCollector(identification=forum["id"],
                                   name=forum["name"],
                                   base_url=forum["base_url"],
                                   description=forum["description"],
                                   category_id=forum["category_id"],
                                   page_param="page-",
                                   start_page=1,
                                   page_increment=1
                                   )


    psv_collector.new_messages_via_discussionlink(discussion_link="https://forum.psv.nl/index.php?threads/guus-til-m.1346/",
                                                  message_class="message message--post js-post js-inlineModContainer",
                                                  full_message_class=False, message_text_class="bbWrapper", message_date_class="u-dt",
                                                  message_author_class="username")

