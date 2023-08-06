r"""
Carries credential data that will be sent to the server via request
metadata for each RPC.

This class can be treated as a wrapper for the
``AuthorizationServiceStub.login`` method to simplify the
authentication.

This is used by ``grpc.intercept_channel``.
"""

import generic_client_interceptor
import api_pb2_grpc
import structs_pb2
import threading
import time


def create(channel, **kwargs):
	"""
	Create credentials data that will be sent to the server via
	request metadata for each RPC.
	:param channel: Existing GRPC channel
	:param kwargs:
	:return:
	"""

	if "account_name" not in kwargs and "account_email" not in kwargs and "account_id" not in kwargs:
		raise ValueError("None of required fields is specified: account_name, account_email nor account_id") # TODO
	if "account_password" not in kwargs and "session_id" not in kwargs and "api_key" not in kwargs:
		raise ValueError("None of required fields is specified: account_password, session_id nor api_key") # TODO

	log_req = structs_pb2.LoginRequest()
	if "account_name" in kwargs:
		log_req.account_name = kwargs["account_name"]
	if "account_email" in kwargs:
		log_req.account_email = kwargs["account_email"]
	if "account_id" in kwargs:
		log_req.account_id = kwargs["account_id"]

	if "account_password" in kwargs:
		log_req.account_password = kwargs["account_password"]
	if "session_id" in kwargs:
		log_req.session_id = kwargs["session_id"]
	if "api_key" in kwargs:
		log_req.api_key = kwargs["api_key"]

	def current_milli_time():
		return int(round(time.time() * 1000))

	class Holder:

		def __init__(self, token="", last_update=0):
			self.token = token
			self.last_update = last_update
			pass

		def is_alive(self):
			return 20 * 1000 + self.last_update > current_milli_time()

	lock = threading.Lock()
	holder = [Holder()]

	def get_token():
		if holder[0].is_alive():
			return holder[0].token

		with lock.acquire():
			if holder[0].is_alive():
				return holder[0].token
			stub = api_pb2_grpc.AuthorizationServiceStub(channel)
			log_resp = stub.Login(log_req)
			holder[0] = Holder(log_resp.jwt_token, current_milli_time())
			return holder[0].token

	return generic_client_interceptor.create(get_token)
