from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from B_Database.my_sql import DatabaseManager

if __name__ == "__main__":
    db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
    db.connect()

    db.create_tables()

    # Creating a category
    category_id = db.add_category('Space')

    forum_id = db.add_forum('Telescopes, Star Charts, & Planetariums',
                            'https://forums.space.com/forums/telescopes-star-charts-planetariums.64/',
                            '', category_id)
    forum = db.select_forum(id=forum_id)
    db.close()

    space_collector = ForumCollector(identification=forum["id"],
                                   name=forum["name"],
                                   base_url=forum["base_url"],
                                   description=forum["description"],
                                   category_id=forum["category_id"]
                                   )

    app = ForumApplication(space_collector, db)

    ds = app.collect_discussions_by_forum_link(
        discussion_class="structItem structItem--thread js-trendingThreadItem",
        full_discussion_class=False, pagination_class="pageNav-main",
        discussion_name_class="structItem-title", discussion_creation_date_class="u-dt",
        discussion_views_class="",
        discussion_replies_class="pairs pairs--justified",
        discussion_last_post_time_class="structItem-latestDate u-dt",
        store_in_db=True,
        return_discussions=True)

    print(ds)

    ds_messages = app.collect_messages_by_discussion_link(
        discussion_link="https://forums.space.com/threads/constellations-space-travel.29641/",
        message_class="message-content js-messageContent",
        full_message_class=False,
        pagination_class="pageNav-main",
        message_text_class="bbWrapper",
        message_date_class="u-dt",
        message_author_class="username ",
        store_in_db=True,
        return_messages=True)

    print(ds_messages)

