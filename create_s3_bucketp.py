import boto3

def create_s3_bucket(bucket_name):
    # Создание клиента S3
    s3_client = boto3.client('s3')

    # Создание бакета
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-central-1'  # Замените на нужную вам региональную конфигурацию
        }
    )
    print(f"Бакет {bucket_name} успешно создан!")

# Замените 'my-unique-bucket-name' на уникальное имя бакета, которое вы хотите использовать
bucket_name = 'my-unique-bucket-name'

# Вызов функции для создания бакета
create_s3_bucket(bucket_name)