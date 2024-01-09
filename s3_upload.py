import boto3
import os
s3 = boto3.client('s3')




bucket = 'op.gg-league-data'

s3.upload_file(r'C:\\Users\\eroma\\PycharmProjects\\pythonProject\\top_100_richest.csv', bucket, 'top_100_richest.csv')
