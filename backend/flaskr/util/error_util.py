# generic error handling using csv file
import csv
from typing import Dict
from flask import jsonify
import traceback

# static error handling class


class ErrorUtil:
    
	error_messages: dict = None
	DEFAULT_ERROR:int = 600
	JSON_DATA_MISSING: int  = 601
	MALFORMED_USER_ID: int = 602
	NO_USER_ID: int = 603
	NO_DIRECTORY_PATH: int = 604
	FAILED_TO_ADD_DIRECTORY: int = 605
	FAILED_TO_GET_ALBUMS: int = 606
	FAILED_TO_DELETE_ALBUM: int = 607
	DIR_PERMISSION_DENIED: int = 608
	DIR_NOT_FOUND: int = 609
	DIR_EMPTY: int = 610
	USERNAME_MISSING: int = 611
	PASSWORD_MISSING: int = 612
	FIRST_NAME_MISSING: int = 613
	LAST_NAME_MISSING: int = 614

	@staticmethod
	def get_error_message(error_code: int) -> str:
        
		if not ErrorUtil.error_messages:
			ErrorUtil.load_error_messages()
		
		return ErrorUtil.error_messages[error_code]['message']

	@staticmethod
	def load_error_messages() -> None:
		with open('error_messages.csv', mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for row in csv_reader:
				row['http_code'] = int(row['http_code'])
				row['internal_error_code'] = int(row['internal_error_code'])
				ErrorUtil.error_messages[row['internal_error_code']] = row
	

	@staticmethod
	def get_http_response_hint(http_error_code: str) -> str:
		
		response_hint: Dict[str, str] = {
			400: "Bad Request",
			401: "Unauthorized",
			403: "Forbidden",
			404: "Not Found",
			405: "Method Not Allowed",
			406: "Not Acceptable",
			408: "Request Timeout",
			409: "Conflict",
			410: "Gone",
			411: "Length Required",
			412: "Precondition Failed",
			413: "Payload Too Large",
			414: "URI Too Long",
			415: "Unsupported Media Type",
			416: "Range Not Satisfiable",
			417: "Expectation Failed",
			418: "I'm a teapot",
			422: "Unprocessable Entity",
			425: "Too Early",
			426: "Upgrade Required",
			428: "Precondition Required",
			429: "Too Many Requests",
			431: "Request Header Fields Too Large",
			451: "Unavailable For Legal Reasons",
			500: "Internal Server Error",
			501: "Not Implemented",
			502: "Bad Gateway",
			503: "Service Unavailable",
			504: "Gateway Timeout",
			505: "HTTP Version Not Supported",
			506: "Variant Also Negotiates",
			507: "Insufficient Storage",
			508: "Loop Detected",
			510: "Not Extended",
			511: "Network Authentication Required"
		}
		return response_hint[str(http_error_code)]

	@staticmethod
	def get_json_response(internal_error_code: int) -> str:
		status_fmt = 'Message:\n\n{message}\n\nResponse Hint:\n\n{response_hint}\n\nStacktrace:\n\n{stacktrace}'
		status = status_fmt.format(
			message=ErrorUtil.error_messages[internal_error_code]['message'],
			response_hint=ErrorUtil.get_http_response_hint(ErrorUtil.error_messages[internal_error_code]['http_code']),
			stacktrace=traceback.format_exc()
		)
		return jsonify({'status': status}), ErrorUtil.error_messages[internal_error_code]['http_code']