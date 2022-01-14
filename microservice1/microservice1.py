import boto3
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
    print("started microservice1.py", flush=True)

    while True:
        print("sending message", flush=True)
        queue.send_message(MessageBody='hello from the microservice')
        time.sleep(1)
