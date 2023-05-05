from A_DataCollectors.ForumCollector.forum_collector import ForumCollector

if __name__ == "__main__":
    psv_collector = ForumCollector(base_url="https://forum.psv.nl/index.php?forums/psv-1-selectie-technische-staf.11/",
                                   page_param="page-",
                                   start_page=1,
                                   page_increment=1)



    psv_info_discussions = psv_collector.return_info_all_discussions_from_scraped(
        discussion_class="structItem structItem--thread js-inlineModContainer js-threadListItem",
        full_discussion_class=False, title_class="structItem-title", creation_date_class="structItem-startDate",
        views_class="pairs pairs--justified structItem-minor", replies_class="pairs pairs--justified",
        last_post_time_class="structItem-latestDate u-dt")

    psv_info_messages = psv_collector.return_info_all_messages_from_scraped(discussion_id=2,
                                                               message_class="message message--post js-post js-inlineModContainer",
                                                               full_message_class=False,
                                                               text_class="bbWrapper", date_class="u-dt",
                                                               author_class="username")

    print(psv_info_discussions)
