# Salesforce Database Sync

This project was created to store historical datapoints from Salesforce. Specifically, this captures counts and totals for open opportunities attached to partners. Information is queried from Salesforce and then saved to a local PostgreSQL database. This allows us to see trends overtime of our partner pipeline. 

## Requirements
- PostgreSQL Database
- Salesforce credentials

```
pip install psycopg2-binary simple-salesforce
```

config.json JSON configuration file 

```
{
    "database":{
        "user": "user",
        "password": "pass",
        "database": "name"
    },
    "salesforce":{
        "username": "user",
        "password": "password",
        "token": "token"
    }
}
```
