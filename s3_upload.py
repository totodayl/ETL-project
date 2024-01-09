import boto3


s3 = boto3.client('s3')
def upload_file(file,bucket,filename):

    s3.upload_file(file, bucket,filename)
    print(f"{file} successfully uploaded to {bucket}!")


