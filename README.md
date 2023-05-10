![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)

*Cassidy is currently a work-in-progress*
# Cassidy
Cassidy is an open-source application for researchers and other users to easily collect text data from various sources, and analyze this text data using different text mining-functionalities. The goal of the application is to turn the plethora of public opinion that is available online, into information that allows researchers to gain possibly unique insights into a certain subject.

The application is separated in five parts:
- A_DataCollectors. In order to collect text data from different kinds of sources, separate DataCollector-classes are made in order to adapt to the different lay-outs of the sources. 
- B_Database. To make scraped data reusable, and prevent having to scrape text data every time the application gets started, a database is set up to store the scraped text data and relevant information regarding this data. 
- C_DataProcessors. Before applying text mining to the text data, preprocessing is applied to make this text data usable. Furthermore, each text mining-functionality may require a different set of preprocessing steps.
- D_Analyzers. After having applied preprocessing, the text data gets analyzed.
- E_UserInterface. To keep the application user-friendly, a UI is set up for researchers to make use of the application.

## Current focus
As of now, the application is a work-in-progress. The focus lies on collecting text data from online forums and scientific literature. Although an ElasticSearch-database is preferable to use, a MySQL-database is set up for now for the proof of concept, as this is free of charges. DataProcessors, Analyzers and a UI are yet to be created.

## Assumptions
The code currently makes assumptions regarding the lay-out or functioning of either the application itself, the text data or the source from which text data is collected.
- The name of a discussion and the link to the discussion are within the same element within the web page (forum_collector.py).
- Messages within a discussion are regarded as the same if the message is within the same discussion, on the same date, by the same author and contains the same text (forum_application.py)
- Last post times of a discussion are stored in a separate element within the web page (forum_collector.py); exposed by [NASA Earthdata Forum](https://forum.earthdata.nasa.gov/viewforum.php?f=7&start=25).
- When entering the pagination of a forum, it is assumed that both the minimum and maximum page number is included within the pagination of the first page (forum_collector.py).
