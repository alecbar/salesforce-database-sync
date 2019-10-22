import json
import psycopg2
import datetime
from simple_salesforce import Salesforce

# JSON config variables
with open('config.json') as json_config:
    config = json.load(json_config)


# Database setup
connection = psycopg2.connect(
    user=config["database"]["user"], password=config["database"]["password"], database=config["database"]["database"])
cursor = connection.cursor()

# Salesforce setup
sf = Salesforce(username=config["salesforce"]["username"],
                password=config["salesforce"]["password"], security_token=config["salesforce"]["token"])
partner_opportunity_query = "SELECT Partner_Owner__c, convertCurrency(Amount) FROM Opportunity WHERE IsClosed = False and Partner_Owner__c != null"
records = sf.query(partner_opportunity_query)['records']

# Query Salesforce and add to dictionaries
partner_count = {}
partner_sum = {}

result = sf.query(partner_opportunity_query)

print("Opportunity Count: " + str(result["totalSize"]))

for record in result['records']:
    if record['Partner_Owner__c'] in partner_count:
        partner_count[record['Partner_Owner__c']] += 1
        if record['Amount'] != None:
            partner_sum[record['Partner_Owner__c']] += record['Amount']
    else:
        partner_count[record['Partner_Owner__c']] = 1
        if record['Amount'] == None:
            partner_sum[record['Partner_Owner__c']] = 0
        else:
            partner_sum[record['Partner_Owner__c']] = record['Amount']

current_date = datetime.datetime.now().strftime('%x')

# Add results to database
for partner in partner_count:

    cursor.execute("INSERT INTO partners (account_id, current_count, current_sum, record_date) VALUES  (%s, %s, %s, %s)",
                   (partner, partner_count[partner], partner_sum[partner], current_date))

    connection.commit()

