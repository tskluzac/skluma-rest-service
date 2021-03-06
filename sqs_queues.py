
import boto3


""" NOTE: This file is unnecessary and unused unless I decide to use queues again. """


def sqs_connect():
    sqs = boto3.resource('sqs', region_name='us-west-2')
    q1 = sqs.get_queue_by_name(QueueName="skluma-universal.fifo")
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


# Not needed, but nice to have just in case.
def sqs_consumer(data):
    print(data)
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
