import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List
import os
import psycopg2
from psycopg2.extras import execute_values

class UserDetails:
	"""
	Class to hold User's details.
	"""
	def __init__(self, user_id, device_type, ip, device_id, locale, app_version):
		self.user_id = user_id
		self.device_type = device_type
		self.masked_ip = self.generate_mask(ip)
		self.masked_device_id = self.generate_mask(device_id)
		self.locale = locale
		self.app_version = app_version
		self.create_date = datetime.now().isoformat()

	def generate_mask(self, key: str) -> str:
		"""
		Given a string `key` it returns the hash of it.

		Parameters:
			key
		"""
		return hashlib.sha512(key.encode("utf-8")).hexdigest()

	def get_record(self) -> tuple:
		"""
		Returns the User details as a tuple.

		Returns:
			tuple: The record as a tuple.
		"""
		return (
			self.user_id,
			self.device_type,
			self.masked_ip,
			self.masked_device_id,
			self.locale,
			self.app_version,
			self.create_date
		)


class UserLogins:
	"""
	Takes care of PostgreSQL operations for User login information.
	"""

	def __init__(self):
		"""
		Initializes the database connection parameters.
		"""
		self.db_conn = {
			"dbname":  os.environ["db_name"],
			"user": os.environ["db_user"],
			"password": os.environ["db_pass"],
			"host": os.environ["db_host"],
			"port": int(os.environ["db_port"]),
		}

		self.insert_user_query = "INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES %s;"

	def get_tuples(self, user_details_list: List[UserDetails]) -> List[tuple]:
		"""
		Convert user_details_list objects to tuples for insertion.

		Parameters:
			user_details (List[Any]): List of UserDetails objects into the PostgreSQL db.

		Returns:
			List[tuple]: List of tuples of UserDetails objects.
		"""
		tuple_list = []

		for user_details in user_details_list:
			tuple_list.append(user_details.get_record())

		return tuple_list

	def insert(self, user_details: List[UserDetails]) -> None:
		"""
		Inserts a list of UserDetails objects into the PostgreSQL db.

		Parameters:
			user_details (List[UserDetails]): List of UserDetails objects to be inserted.
		"""

		with psycopg2.connect(**self.db_conn) as connection:
			with connection.cursor() as cur:

				# Transform the UserDetails objects to tuples
				user_details_tuples = self.get_tuples(user_details)

				# Log the objects being inserted
				print(f"Inserting these user details: {user_details_tuples}")

				# Executing the insert query for the all the user tuples
				execute_values(cur, self.insert_user_query, user_details_tuples)

				# Close the cursor after executing the query
				cur.close()
			# Commit the written data to db.
			connection.commit()
