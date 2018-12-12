
import boto3


def sqs_connect():
    sqs = boto3.resource('sqs', region_name='us-west-2')
    q1 = sqs.get_queue_by_name(QueueName="skluma-universal.fifo")
    # print("Successfully connected to Skluma Job Queue Service. ")
    return q1, sqs


def sqs_producer(file_path, file_id):
    queue = sqs_connect()
    response = queue[0].send_message(MessageBody=file_id, MessageGroupId='skluma-jobs', MessageAttributes={
                'File_To_Process': {
                'StringValue': file_path,
                'DataType': 'String'
            }
        })

    return response


def sqs_consumer(data):
    queue = sqs_connect()
    for message in queue[0].receive_messages(MessageAttributeNames=['File_To_Process']):
        # Get the custom author message attribute if it was set
        tyler_text = ''
        if message.message_attributes is not None:
            file_to_process = message.message_attributes.get('File_To_Process').get('StringValue')
            if file_to_process:
                tyler_text = ' ({0})'.format(file_to_process)

        # Print out the body and author (if set)
        print("Receiving file with id {0} at address {1} from job queue...".format(message.body, tyler_text))

