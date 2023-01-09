from logging import Filter
import boto3
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph,SimpleDocTemplate, Table, TableStyle, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

client = boto3.client('ce')

start_date=str(date(year=date.today().year, month=date.today().month, day=1).strftime('%Y-%m-%d'))
end_date=str(date.today())
print(start_date,end_date)

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

print(billed_resources)
print('---')
print(resource_name)
print('---')
print(resource_cost)


# Create PDF 
doc = SimpleDocTemplate("table.pdf", pagesize=letter)

data = [["Service", "Cost ($)"]]  # Table header

# Add the key-value pairs from the dictionary to the table
for service, cost in billed_resources.items():
    data.append([service, cost])

total_cost = sum(billed_resources.values())

# Custom paragraph style
total_style = ParagraphStyle(name="Total", fontName='Helvetica-Bold', fontSize=12, bold=True)
total_label = Paragraph('Total', total_style)
total_cost_paragraph = Paragraph(f'{total_cost}', total_style)

data.append([total_label, total_cost_paragraph])



title = "AWS Cost Report"
subtitle = "Summary of costs for different services"

title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])

subtitle_style = ParagraphStyle(name="Subtitle",
                                fontSize=14,
                                leading=16,
                                alignment=1,  # Center alignment
                                leftIndent=-30,
                                rightIndent=-30)

subtitle_paragraph = Paragraph(subtitle, subtitle_style)
second_heading = Paragraph("Active Services",subtitle_style)

style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                   ('TEXTCOLOR',(0,0),(1,0),colors.red),
                   ('VALIGN',(0,0),(-1,-1),'TOP'),
                   ('TEXTCOLOR',(1,1),(-1,-1),colors.blue),
                   ('ALIGN',(0,0),(-1,-1),'LEFT'),
                   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                   ])

table = Table(data)
table.setStyle(style)

item_style = ParagraphStyle(
    name='Item',
    alignment=TA_JUSTIFY,
    fontName='Helvetica',
    fontSize=12,
    leading=16,
    leftIndent=0.2*inch,
    bulletIndent=0,
    bulletFontSize=12,
    bulletType='bullet',
    textColor='black',
    spaceBefore=0,
    spaceAfter=0,
    wordWrap='LTR'
)

items = resource_name


ordered_list = ListFlowable(
    [ListItem(Paragraph(item, item_style) for item in items)],
    bulletType='bullet',
    align='center'
)

flowables = [Paragraph(item, item_style) for item in items]
ordered_list = ListFlowable(flowables, bulletType='bullet',start='square')

doc.build([title_paragraph, Spacer(1, 0.25*inch), subtitle_paragraph, Spacer(1, 0.5*inch), table,Spacer(1, 0.5*inch),second_heading, Spacer(1, 0.25*inch), ordered_list])
