## Realestate data to Database :house:

This code acts as small data pipeline that:  
- Extracts data from realestate ads on <www.nehnutelnosti.sk> (for Košice city)
- Transforms data so they are easier to handle later. (For example date to unix timestamp)
- Loads data into:
    - MongoDB document database
    - PostgreSQL database (using Neon, serverless postgre solution)

With this data stored in the database, we can now proceed to generate compelling analytics and reports in the next steps.

### Next steps  
- implement orchestration :pushpin:
- Create reports in Tableau :pushpin:

### UML Diagram of repo

![UML Diagram](/docs/classes_pipeline.png)
