# AWS Weekly Bill report

This is an AWS Lambda function that retrieves cost and usage data for your AWS accounts using the AWS Cost Explorer API and sends an email report to a specified recipient.

## Features

- Retrieves cost and usage data for the current month
- Sends an email report that includes:
  - List of active resources
  - Total cost
  - Breakdown of costs by resource

## Tech Stack

- AWS account with access to the AWS Cost Explorer API
- AWS Lambda
- AWS Simple Email Service (SES)
- AWS Lambda function
- Amazon EventBridge

## Usage

#### Function: _get_cost_and_usage.py_
- To execute this function, run the below commands
  - `pip install boto3`
  - `python get_cost_and_usage.py`
- This function retrieves the current cost and usage of AWS Resources in you account.

#### Function: _lambda_email_bill_report.py_
- This is a Lambda function with core logic same as the above function. 
- Along with it, I have used AWS SES which sends the fetched data to your email. You can input your email in the `send_email` method.
- You can also create an Amazon EventBridge rule to run this Lambda Function Weekly.

#### Function: _pdf_report_for_aws_costs.py_
- This function will create a PDF with the costs and usage data using python's reportlab module.
- You can store this reports in a S3 bucket for future reference


## License

This project is licensed under the Apache License 2.0.

hello
