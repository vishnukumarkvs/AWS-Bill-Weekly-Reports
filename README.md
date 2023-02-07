# AWS Cost Report

This is an AWS Lambda function that retrieves cost and usage data for your AWS accounts using the AWS Cost Explorer API and sends an email report to a specified recipient.

## Features

- Retrieves cost and usage data for the current month
- Sends an email report that includes:
  - List of active resources
  - Total cost
  - Breakdown of costs by resource

## Requirements

- AWS account with access to the AWS Cost Explorer API
- AWS Simple Email Service (SES)
- AWS Lambda function

## Usage

1. Deploy the AWS Lambda function code
2. Set up a trigger for the function (e.g. a CloudWatch Event)
3. Update the `send_email` function with the desired sender and recipient email addresses
4. The function will run and send the cost report to the specified recipient

## License

This project is licensed under the Apache License 2.0.
