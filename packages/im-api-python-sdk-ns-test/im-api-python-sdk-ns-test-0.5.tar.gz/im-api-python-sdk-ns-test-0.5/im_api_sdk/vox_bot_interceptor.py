r"""
Class to carry credential data that will be sent to the server via request
metadata for each RPC.

This class provides a bot authentication.

This is used by ``grpc.intercept_channel``.
"""

import generic_client_interceptor
import time
import jwt
import json


def create_from_json(fp):
	"""
	Process the [CreateBotResponse] structure that is provided as JSON
	and create credentials data that will be sent to the server via
	request metadata for each RPC.
	:param fp: a ``.read()``-supporting file-like object containing a JSON document
	:return:
	"""
	json_object = json.load(fp)

	if not json_object["client_email"] or not json_object["key_id"] or not json_object["private_key"]:
		raise ValueError("Error reading credential from JSON, expecting  'client_email', 'private_key' and 'private_key_id'")
	return create(json_object["client_email"], json_object["key_id"], json_object["private_key"])


def create(email, private_key_id, private_key):
	"""
	Create credentials data that will be sent to the server via
	request metadata for each RPC.
	:param email: Email of the current Voximplant developer account.
	:param private_key_id: Unique ID of a private key.
	:param private_key: Private key for authentication.
	:return:
	"""
	def get_token():
		curr_time = int(round(time.time()))
		payload = {
			"iat": curr_time,
			"exp": curr_time + 30,
			"iss": email
		}
		headers = {
			"kid": private_key_id
		}
		return jwt.encode(payload, private_key, "RS256", headers)

	return generic_client_interceptor.create(get_token)
