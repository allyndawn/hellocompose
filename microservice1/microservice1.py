import boto3
import json
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
            device_id BIGINT NOT NULL PRIMARY KEY,
            device_name VARCHAR(100) NOT NULL
        )
        """
    cur.execute(query)
    print("Created devices table successuflly")
except mariadb.Error as e:
    print(f"Error: {e}")

if __name__ == "__main__":
    print("started microservice1.py", flush=True)

    while True:
        for message in queue.receive_messages(WaitTimeSeconds=1):
            print('received {0}'.format(message.body), flush=True)
            message_body = json.loads(message.body)
            message.delete()

            query = """\
                INSERT INTO devices (device_id, device_name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE device_name=%s
                """
            val = (message_body["device_id"], message_body["device_name"], message_body["device_name"])
            try:
                cur.execute(query, val)
            except mariadb.Error as e:
                print(f"Error: {e}")

            print("now the database contains", flush=True)

            cur.execute("SELECT device_id, device_name FROM devices")
            for (device_id, device_name) in cur:
                print(f"Successfully retrieved {device_id}, {device_name}", flush=True)

        time.sleep(1)

# TODO close on exit
