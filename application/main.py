from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from B_Database.my_sql import DatabaseManager

if __name__ == "__main__":
    db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
    db.connect()

    db.create_tables()

    category_id = db.add_category('PSV')

    forum_id = db.add_forum('PSV 1: Selectie & Technische Staf',
                            'https://forum.psv.nl/index.php?forums/psv-1-selectie-technische-staf.11/',
                            'In dit onderdeel kunnen alle spelers en trainers van PSV 1 besproken worden.', category_id)
    forum = db.select_forum(id=forum_id)
    db.close()

    psv_collector = ForumCollector(identification=forum["id"],
                                   name=forum["name"],
                                   base_url=forum["base_url"],
                                   description=forum["description"],
                                   category_id=forum["category_id"]
                                   )

    app = ForumApplication(psv_collector, db)

    ds = app.collect_discussions_by_forum_link(
        discussion_class="structItem structItem--thread js-inlineModContainer js-threadListItem",
        full_discussion_class=False, pagination_class="pageNav",
        discussion_name_class="structItem-title", discussion_creation_date_class="structItem-startDate",
        discussion_views_class="pairs pairs--justified structItem-minor",
        discussion_replies_class="pairs pairs--justified",
        discussion_last_post_time_class="structItem-latestDate u-dt",
        return_discussions=True)

    print(ds)

    print("Messages:")

    ds_messsages = app.collect_messages_by_discussion_link(
        discussion_link="https://forum.psv.nl/index.php?threads/guus-til-m.1346/",
        message_class="message message--post js-post js-inlineModContainer",
        full_message_class=False,
        pagination_class="pageNav-main",
        message_text_class="bbWrapper",
        message_date_class="u-dt",
        message_author_class="username ",
        return_messages=True)

    print(ds_messsages)

