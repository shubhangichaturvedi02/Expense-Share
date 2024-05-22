
import csv
import boto3
import os
from django.core.management.base import BaseCommand
from expenses.models import User

class Command(BaseCommand):
    help = 'Export user data to S3'

    def handle(self, *args, **kwargs):
        try:
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
            
            if not all([aws_access_key_id, aws_secret_access_key, bucket_name]):
                raise ValueError("AWS credentials or bucket name not provided in environment variables.")
            
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            users = User.objects.all()

            with open('user_data.csv', 'w', newline='') as csvfile:
                fieldnames = ['user_id', 'name', 'email', 'mobile']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for user in users:
                    writer.writerow({
                        'user_id': user.user_id,
                        'name': user.name,
                        'email': user.email,
                        'mobile': user.mobile
                    })

            s3.upload_file('user_data.csv', bucket_name, 'user_data.csv')
            print('User data exported to S3 successfully.')

        except Exception as e:
            print(f'Failed to export user data to S3: {e}')
