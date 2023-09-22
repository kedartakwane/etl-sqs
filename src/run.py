import json
from typing import List, Dict
from helpers.queue_service import QueueService
import time
from helpers.logins import *


def check_data(data: Dict[str, Any]) -> bool:
	"""
	Checks if the data has all the attributes desired to process it.

	Parameters:
		data (Dict[str, Any]): The data to create an UserDetails object.

	Returns:
		bool: If the data has all attributes then True else False
	"""
	if not data.get("user_id") and not data.get("device_type") and not data.get("ip") and not data.get("device_id") and not data.get("locale") and not data.get("app_version"):
		return False
	return True


def create_user_details(data: Dict[str, Any]) -> Optional[UserDetails]:
	"""
	Creates a UserDetails object from a dictionary of data.

	Parameters:
		data (Dict[str, Any]): The data to create an UserDetails object.

	Returns:
		Optional[UserDetails]: The created record or None if data is None.
	"""
	if data is None:
		return None

	if not check_data(data):
		return None

	user_details = UserDetails(
		data.get("user_id", ""),
		data.get("device_type", ""),
		data.get("ip", ""),
		data.get("device_id", ""),
		data.get("locale", ""),
		int(data.get("app_version", "1").split(".")[0])
	)
	return user_details


# Function to process messages read from the SQS queue and create UserLoginWrapper records
def process_message_list(message_list: List[Dict[str, Any]]) -> List[UserDetails]:
	"""
	This function will process messages from the queue to create UserDetails' objects.

	Parameters:
		message_list (List[Dict[str, Any]]): List of messages read from SQS queue.

	Returns:
		List[UserDetails]: List of UserDetails objects that are created from the messages.
	"""
	user_details_objs = []

	for message in message_list:
		print(f"Message to be processed: {message}")

		# Create a new UserDetails object from the message
		record = create_user_details(message)

		# Add the UserDetails' object to the list if it is valid
		if record is not None:
			user_details_objs.append(record)
	return user_details_objs


def run():
	"""
	This function read messages from the queue, process them, and insert the resulting
	UserDetails objects into the PostgreSQL db.
	"""
	# To continuously process the queue messages
	while True:
		# Initialize SQS service
		sqs = QueueService()

		# Read messages from the queue
		message_list = sqs.read_messages()
		print(f"List of messages in the queue : {message_list}")

		# Process the messages to create UserDetails objects
		user_details_list = process_message_list(message_list)
		print(f"UserDetails List: {user_details_list}")

		# Insert the UserDetails objects into the PostgreSQL database
		user_login_obj = UserLogins()
		user_login_obj.insert(user_details_list)

		# To avoid overloading the system, sleep for 10 sec
		time.sleep(10)


# Start executing the script
if __name__ == "__main__":
	run()
