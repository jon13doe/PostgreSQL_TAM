import boto3

def connect_to_s3_bucket(bucket_name):
    # Создание клиента S3
    s3_client = boto3.client('s3')

    # Подключение к бакету
    bucket = s3_client.Bucket(bucket_name)

    return bucket

# Замените 'my-unique-bucket-name' на имя вашего бакета
bucket_name = 'my-unique-bucket-name'

# Подключение к бакету
s3_bucket = connect_to_s3_bucket(bucket_name)

# Пример использования: получение списка объектов в бакете
objects = s3_bucket.objects.all()
for obj in objects:
    print(obj.key)