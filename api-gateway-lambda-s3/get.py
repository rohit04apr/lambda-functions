import json
import boto3

s3 = boto3.client('s3')
bucket = "rt-testing"
file = 'ips.json'


def lambda_handler(event, context):

    if "region" in event:
        input1 = event['region']
    else:
        input1 = ""

    if "office" in event:
        input2 = event['office']
    else:
        input2 = ""

    firmips = get_s3_bucket_ips(bucket, file)

    maintable = ""
    for i in firmips:

        if str(input1) != "" and str(input2) == "":
            if i['region'] == str(input1):
                table = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    i['region'], i['office'], i['ip_network'])
                maintable = maintable + table
        elif str(input1) != "" and str(input2) != "":
            if i['region'] == str(input1) and i['office'] == str(input2):
                table = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    i['region'], i['office'], i['ip_network'])
                maintable = maintable + table
        else:
            table = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                i['region'], i['office'], i['ip_network'])

            maintable = maintable + table

    longinformation = f"""
        <h1 style='color: #5e9ca0;'>List of <span style='color: #2b2301;'>Firm IPs</span></h1>
        <h2 style='color: #2e6c80;'>Below is the list of firm ips generated from api gateway using lambda and s3</h2>
        <style> table, th, td {{ border: 1px solid black; border-collapse: collapse; }} </style>
        </p> <table style="border:4px solid black;margin-right:auto;width:100%">
        <tr>
            <th>region</th>
            <th>office</th>
            <th>ip network</th>
        </tr>
        {maintable}
        </table>
        </p>
        """

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': longinformation
    }


def get_s3_bucket_ips(bucket, file):

    response = s3.get_object(Bucket=bucket, Key=file)

    content = response['Body']

    firm_ips = json.loads(content.read())

    return firm_ips

