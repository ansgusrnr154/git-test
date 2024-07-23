import boto3
import sys
from botocore.exceptions import ClientError

def list_my_buckets(s3):
  print('Buckets:\n\t', *[b.name for b in s3.buckets.all()], sep="\n\t")

def create_and_delete_my_bucket(bucket_name, region, keep_bucket):
  s3 = boto3.resource('s3', region_name=region)

  list_my_buckets(s3)

  try:
    print('\nCreating new bucket:', bucket_name)
    bucket = s3.create_bucket(
      Bucket=bucket_name,
      CreateBucketConfiguration={
        'LocationConstraint': region
      }
    )
  except ClientError as e:
   print(e)
   sys.exit('Exiting the script because bucket creation failed.')

  bucket.wait_until_exists()
  list_my_buckets(s3)

  if not keep_bucket:
     print('\nDeleting bucket:', bucket.name)
     bucket.delete()

     bucket.wait_until_not_exists()
     list_my_buckets(s3)
  else:
    print('\nKeeping bucket:', bucket.name)

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('bucket_name', help='The name of the bucket to create.')
  parser.add_argument('region', help='The region in which to create your bucket.')
  parser.add_argument('--keep_bucket', help='Keeps the created bucket. When not specified, the bucket is deleted.',action='store_true')

  args = parser.parse_args()

  create_and_delete_my_bucket(args.bucket_name, args.region, args.keep_bucket)

if __name__ == '__main__':
  main()