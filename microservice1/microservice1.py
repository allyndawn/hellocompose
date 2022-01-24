import boto3
import mariadb
import sys
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

# Attempt to connect to the database for up to 10 seconds
# (to give time for the container with the database to start)

print("Attempting to connect to database", flush=True)

database_connection_attempts = 0
connected_to_database = False

while not connected_to_database and database_connection_attempts < 10:
    try:
        conn = mariadb.connect(
            user="test_user",
            password="test_user",
            host="db",
            port=3306,
            database="pandabase"
        )
        connected_to_database = True
    except mariadb.Error as e:
        print(".", flush=True)
        database_connection_attempts += 1
        time.sleep(1)

if not connected_to_database:
    sys.exit(1)

print("Connected to database successfully", flush=True)

# Get Cursor
cur = conn.cursor()

# Create our table for storing things
try:
    query = """\
        CREATE TABLE IF NOT EXISTS devices(
            device_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            device_name VARCHAR(100) NOT NULL
        )
        """
    cur.execute(query)
    print("Created devices table successuflly")
except mariadb.Error as e:
    print(f"Error: {e}")

conn.close()

if __name__ == "__main__":
    print("started microservice1.py", flush=True)

    while True:
        print("sending message", flush=True)
        queue.send_message(MessageBody='hello from the microservice')
        time.sleep(1)
