from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from B_Database.my_sql import DatabaseManager

if __name__ == "__main__":
    db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
    db.connect()

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
                                   category_id=forum["category_id"],
                                   page_param="page-",
                                   start_page=1,
                                   page_increment=1
                                   )

    app = ForumApplication(psv_collector, db)

    ds = app.store_discussions_by_forum_link(
        discussion_class="structItem structItem--thread js-inlineModContainer js-threadListItem",
        full_discussion_class=False,
        discussion_name_class="structItem-title", discussion_creation_date_class="structItem-startDate",
        discussion_views_class="pairs pairs--justified structItem-minor",
        discussion_replies_class="pairs pairs--justified",
        discussion_last_post_time_class="structItem-latestDate u-dt")
