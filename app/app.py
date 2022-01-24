import boto3
import json
import time

# Note: dummy values for aws_secret_access_key and aws_access_key_id are needed
# to avoid botocore.exceptions.NoCredentialsError: Unable to locate credentials
client = boto3.resource('sqs',
                        endpoint_url='http://elasticmq:9324',
                        region_name='elasticmq',
                        aws_secret_access_key='x',
                        aws_access_key_id='x',
                        use_ssl=False)
queue = client.get_queue_by_name(QueueName='devicemessage')

if __name__ == "__main__":
    print("started app.py", flush=True)

    device_updates=[
        { "device_id": 4257912359, "device_name": "Allen Phone" },
        { "device_id": 4254180648, "device_name": "Fox Phone" },
        { "device_id": 4257912359, "device_name": "Panda Phone" },
    ]

    for device_update in device_updates:
        message_body = json.dumps(device_update)
        queue.send_message(MessageBody=message_body)
        time.sleep(1)

    while True:
        time.sleep(1)
