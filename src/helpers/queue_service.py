from botocore.exceptions import ClientError
import boto3
import os
import json

class QueueService:
	"""
	A class to interact with an SQS (Simple Queue Service) queue.
	"""

	def __init__(self):
		"""
		Initializes an SQS client and sets the queue URL.
		"""
		# Set SQS queue URL
		self.queue_url = os.environ['queue_url']
		# Initialize SQS client
		self.sqs = boto3.client(
			os.environ['queue_type'],
			endpoint_url=os.environ['queue_endpoint'],
			region_name=os.environ['queue_region_name']
		)

	def read_messages(self, limit: int = 100) -> list:
		"""
		Reads and returns messages from the SQS queue up to the specified limit.

		Parameters:
			limit (int): Maximum number of messages to read from the queue.

		Returns:
			list: List of messages read from the queue.
		"""
		# Initialize an empty list to store message body's
		message_body = []
		try:
			# Request messages from the SQS queue
			resp_json = self.sqs.receive_message(
				QueueUrl=self.queue_url,
				MaxNumberOfMessages=limit
			)

			# Check if the response contains any messages
			if resp_json.get("Messages"):
				message_list = resp_json["Messages"]

				# Delete each message from the queue after it's read
				for message in message_list:
					message_body.append(json.loads(message["Body"]))
					self.remove_message(message["ReceiptHandle"])

		except ClientError as e:
			print(f"Error reading messages from SQS: {e}")

		return message_body

	def remove_message(self, handle: str):
		"""
		Remove the message from the SQS queue.

		Parameters:
			handle (str): The receipt handle of the message to be deleted.
		"""
		try:
			self.sqs.delete_message(
				QueueUrl=self.queue_url,
				ReceiptHandle=handle
			)
		except ClientError as e:
			print(f"[ERROR] Error deleting message from SQS: {e}")
