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
    print("started app.py", flush=True)

    while True:
        for message in queue.receive_messages(WaitTimeSeconds=1):
            print('received {0}'.format(message.body), flush=True)
            message.delete()
        time.sleep(1)
