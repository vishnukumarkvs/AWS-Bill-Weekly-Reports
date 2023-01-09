import boto3
import json
from datetime import date

# Accessing Cost Explorer API
client = boto3.client('ce')

# StartDate = 1st date of current month, EndDate = Todays date
start_date=str(date(year=date.today().year, month=date.today().month, day=1).strftime('%Y-%m-%d'))
end_date=str(date.today())

print(f'StartDate:{start_date} - EndDate:{end_date}\n')

# The get_cost_and_usage operation is a part of the AWS Cost Explorer API, which allows you to programmatically retrieve cost and usage data for your AWS accounts.
response = client.get_cost_and_usage(
    TimePeriod={
        'Start':start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    Filter={
        "Not":
        {
            'Dimensions':{
            'Key': 'RECORD_TYPE',
            'Values':['Credit','Refund']
             }
        }
    },
    GroupBy=[
        {
            'Type':'DIMENSION',
            'Key':'SERVICE'
        }
    ]
)

mydict=response
resource_name=[]
resource_cost=[]

total_resources_active = len(mydict['ResultsByTime'][0]['Groups'])

for i in range (total_resources_active):
    a=(mydict['ResultsByTime'][0]['Groups'][i].values())
    b=list(a)
    resource_name.append(b[0][0])
    resource_cost.append(float(b[1]['UnblendedCost']['Amount']))

dict0={}

for i in range(total_resources_active):
    dict0[resource_name[i]]=resource_cost[i]

billed_resources={k: v for k, v in dict0.items() if v}

print(f'Current Billed Resources of this month:-',json.dumps(billed_resources, indent=4, sort_keys=True))
print(f'Active Resources:-', json.dumps(resource_name, indent=4, sort_keys=True))

