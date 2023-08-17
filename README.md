## Realestate data to Database

This code acts as small data pipeline that:  
- Excracts data from realestate ad on <www.nehnutelnosti.sk>
- Transforms data so they are easier to handle later. (For example date to unix timestamp)
- Loads data into:
    - MongoDB document database
    - Postgresql database

With this data stored in database, we can continue create interesting analytics and reports in next steps.

### UML Diagram of repo

![UML Diagram](/docs/classes_pipeline.png)