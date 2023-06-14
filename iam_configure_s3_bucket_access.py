import boto3
import json

def configure_s3_bucket_access(bucket_name, iam_username):
    # Создание клиента IAM
    iam_client = boto3.client('iam')

    # Создание политики доступа для S3
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}/*",
                    f"arn:aws:s3:::{bucket_name}"
                ]
            }
        ]
    }

    policy_name = f"{bucket_name}-policy"

    # Создание политики IAM
    response = iam_client.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_document)
    )

    policy_arn = response['Policy']['Arn']

    # Применение политики к пользователю IAM
    iam_client.attach_user_policy(
        UserName=iam_username,
        PolicyArn=policy_arn
    )

    print(f"Политика доступа {policy_name} успешно создана и применена к пользователю {iam_username}!")

# Замените 'name' на имя вашего бакета
bucket_name = 'name'

# Замените 'my-iam-username' на имя пользователя IAM, которому нужно предоставить доступ к бакету
iam_username = 'my-iam-username'

# Настройка доступа к бакету
configure_s3_bucket_access(bucket_name, iam_username)