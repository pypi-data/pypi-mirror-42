import boto3


def upload_file_to_s3(path='./', filename=None, bucket='sportybet-comprehend-us-east-1-test'):
    if not filename:
        s3 = boto3.resource('s3')
        s3.Object(bucket, filename).put(Body=open(path + filename, 'rb'))
    else:
        print("please specify your file.")

