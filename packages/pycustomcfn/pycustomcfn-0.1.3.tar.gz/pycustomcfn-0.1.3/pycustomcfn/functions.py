"""
Module to handle the CloudFormation Custom Lambda handler and replies
"""
import json
import urllib3, certifi

# In order to debug the urllib3 traffic this needs to be re-imported here
#

import logging

#
# In order to debug the urllib3 traffic this needs to be re-imported here

from pysimplelogger import newLogger
import pysimplelogger as SimpleLogger
import pyrandomtools as utils

def FakeEvent(ResourceType='Custom::CFN-Fake-Function', RequestType='Create', Properties={}):
	"""
	FakeEvent for py.test cases
	"""
	return {		
		"FakeEvent": True,
		"RequestType": RequestType,
		"ResponseURL": "http://pre-signed-S3-url-for-response",
		"StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/stack-name/guid",
		"RequestId" : "unique id for this create request",
		"LogicalResourceId": "FakeResource",
		"ResourceType": ResourceType,
		"ResourceProperties": Properties,
	}
		
class CustomCFN(object):
	"""
	.. autoclass
	"""

	_testmode = False
	_responseSent = False	
	_responseBody = dict()

	# Define Exceptions
	class TestFailure(Exception):
		def __init__(self,*args,**kwargs):
			Exception.__init__(self,*args,**kwargs)
			
	class TestSuccess(Exception):
		def __init__(self,*args,**kwargs):
			Exception.__init__(self,*args,**kwargs)		
		
	@property
	def event(self):
		"""Provide Read-Only access to the supplied event object from CFN
		
		:return: a copy of the event dictionary object
		:rtype: dict
		"""
		return dict(self._event)
			
	@property
	def properties(self):
		"""Provide Read-Only access to the Event.ResourceProperties dictionary
		
		:return: a copy of the ResourceProperties dictionary
		:rtype: dict
		"""
		return self.event.get('ResourceProperties', {})

	@property
	def old_properties(self):
		"""Provide Read-Only access to the Event.OldResourceProperties dictionary
		
		:return: a copy of the OldResourceProperties dictionary
		:rtype: dict
		"""
		return self.event.get('OldResourceProperties', {})
	
	@property
	def context(self):
		"""Provide access to the Lambda Context object
		
		:return: The current Lambda Context
		:rtype: LambdaContext:
		"""
		return self._context

	@property
	def account(self):
		"""The Amazon Account number this call originated from
		
		:return: Amazon Account Number
		:rtype: str
		"""
		return str(self._account)
	
	@property
	def region(self):
		"""The Amazon Region this call originated from
		
		:return: Amazon Region
		:rtype: str
		"""
		return str(self._region)
	

	@region.setter
	def region(self, region):
		"""Amazon Region to be used in Boto calls 
				
		:param region: The Amazon region
		:type region: str
		
		:return: Amazon Region
		:rtype: str
		"""
		# Not sure why we want to allow changing the region, There was a compelling argument that I need to remember and capture.

		# Add validation code here
		self.logger.critical("someone is attempting to change the region of the CustomCFN object")
		raise Exception
		
		self._region = region
		return self.region
		

	@property
	def RequestType(self):
		"""Return the RequestType from the event
		
		as described here https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requesttypes.html
		
		:return: "Create", "Update" or "Delete"
		:rtype: str
		"""
		return str( self.event.get('RequestType', 'Unknown') )
		

	@property
	def ResourceType(self):
		"""Return the ResourceType from the event
		
		If the generic "AWS::CloudFormation::CustomResource" is specified we will try to determine the name from the called function
		
		:return: Name of custom resource
		:rtype: str
		"""
		if self.event['ResourceType'].startswith('Custom::'):
			return str(self.event['ResourceType'])
		
		if self.event['ResourceType'] == 'AWS::CloudFormation::CustomResource':
			return str(self.event['ResourceType'])

		return 'Unknown'
		

	def get_property(self, propertyName=None, defaultReply=None):
		"""Fetches a specific property from the event, with the ability to chase sub-items including lists and dictionaries without burdening the caller. Simlar to the get method of a dictionary with tree decending features
		
		Example:
			Assume the following properties
			
			.. code-block::python
			
			>>> print(yaml.dumps(CustonCFN.properties))
			items:
				name: Main
				list: [ 'a', 'b', 'c' ]
				list2:
				  - title: Pinball Wizard
				    artist: The Who
				  - title: Manhattan Project
					artist: Rush	
			>>> CustomCFN.get_property('items.name', None)
			'Main'
			>>> CustomCFN.get_property('items.list[0]', None)
			'a'
			>>> CustomCFN.get_property('items.list2[0]', None)
			{'title': 'Pinball Wizard', 'artist': 'The Who'}
			>>> CustomCFN.get_property('items.list2[1].title', None)
			'Manhattan Project'
			>>> CustomCFN.get_property('items.list2[2].title', None)
			None

		:param propertyName: the name of the parameter to fetch
		:type propertyName: str
		:param defaultReply: What to return if the property cannot be found
		:type defaultReply: any
		:return: Either the discovered property, or defaultReply
		:rtype: any
		:raises ValueError: If propertyName is not specified
		
		"""
		logger = newLogger(self.logger)
		logger.trace_json_dumps('Looking for {} in'.format(propertyName), self.properties)
		
		if propertyName is None:
			raise ValueError('propertyName not specified')
		
		logger.trace_json_dumps('Returning', utils.treeGet(self.properties, propertyName, defaultReply))
		return utils.treeGet(self.properties, propertyName, defaultReply)
		   

	def get_old_property(self, propertyName=None, defaultReply=None):
		"""See get_property for a full explination. Used to fetch pre-existing properties during an Update
		"""
		logger = newLogger(self.logger)
		logger.trace_json_dumps('Looking for {} in'.format(propertyName), self.old_properties)

		if propertyName is None:
			raise ValueError('propertyName not specified')
			
		r = utils.treeGet(self.old_properties, propertyName, defaultReply)
		logger.trace_json_dumps('Returning', r)
		return r
	

	@property
	def responseBody(self):
		"""Returns the currently constructed responseBody that would be used when sendResponse is called
		
		:return: a copy of the responseBody
		:rtype: dict
		"""
		return dict(self._responseBody)
	

	@property
	def log_stream_name(self):
		"""The name of the CloudWatch log stream that messages are being sent to. This is wrapped because when using 'serverless invoke local' the FakeLambdaContext does not support this property so we are insuring a common interface for dev
		
		:return: Read only copy of the CloudWatch log stream name
		:rtype: str
		"""
		return str(self._log_stream_name)
		

	@property
	def stackID(self):
		"""StackID of the CloudFormation stack we were called by. If not availible return 'UnknownStackId' (This usually happens because of poorly written test cases)
		
		:return: StackId
		:rtype: str
		"""
		return str(self._responseBody['StackId'] or 'UnknownStackId')


	@property
	def requestID(self):
		"""RequestId of the CloudFormation stack we were called by. If not availible return 'UnknownRequestId' (This usually happens because of poorly written test cases)
		
		:return: RequestId
		:rtype: str
		"""
		return str(self._responseBody['RequestId'] or 'UnknownRequestId')
		

	@property
	def logicalResourceID(self):
		"""LogicalResourceId of the CloudFormation resource we were called by. If not availible return 'UnknownLogicalResourceId' (This usually happens because of poorly written test cases)
		
		:return: LogicalResourceId
		:rtype: str
		"""
		return str(self._responseBody.get('LogicalResourceId', 'UnknownLogicalResourceId'))
		

	@property
	def physicalResourceID(self):
		"""PhysicalResourceId of the CloudFormation resource we were called by. If not defined by CFN, then the current LogicalResourceID is returned. Create and Update methods should set the value in order to create a relationship between the CFN Logical resource and the created entity.
		
		:return: PhysicalResourceId
		:rtype: str
		"""
		return str(self._responseBody.get('PhysicalResourceId', self.logicalResourceID))
		

	@physicalResourceID.setter
	def physicalResourceID(self, value):
		"""Captures the supplied PhysicalResourceId and stores the value in the responseBody being assembled 
				
		:param value: The Amazon region
		:type value: str
		
		:return: The current value
		:rtype: str
		"""
		self._responseBody['PhysicalResourceId'] = value
		return self.physicalResourceID


	@physicalResourceID.deleter
	def physicalResourceID(self):
		"""When deleting the physicalResourceID, reset the value to the current logicalResourceID
 		"""
		self.physicalResourceID = self.logicalResourceID


	@property
	def responseURL(self):
		"""Fetch the URL to send the response to
		
		:return: URL or None
		:rtype: str
		"""
		return str(self.event.get('ResponseURL')) or None
		

	@property
	def isFakeEvent(self):
		return self.event.get('FakeEvent', False)
		

	@property
	def __debug_data__(self):
		"""Returns the relavant data in a dictionary without python objects simplifying creating debug messages
		
		:return: Dictionary of terms and values
		:rtype: dict
		"""
		return {
			'account': self.account,
			'region': self.region,
			'log_stream_name': self.log_stream_name,	
			'stackID': self.stackID,
			'requestID': self.requestID,
			'logicalResourceID': self.logicalResourceID,
			'physicalResourceID': self.physicalResourceID,
			'event': self.event,
			'responseBody': self.responseBody,
		}		


	@SimpleLogger.tracer
	def __testmode__(self):
		"""Method to be called during testing to deactivate the last-chance responder
		"""
		self._testmode = True
		self._responseSent = True
		

	@SimpleLogger.tracer
	def __del__(self):
		"""Represents a responder to CFN in case we encounter an un-handled python exception. __del__ is called during object deletion.
		
		This is NOT the prefered way to handle sending a failure message but is the last-chance responder to avoid a CloudFormation timeout
		"""
		
		if not self._responseSent:
			self.sendFailureMsg('Reason unknown, caught by __del__ handler')


	@SimpleLogger.tracer
	def __init__(self, event={}, context={}, logger=None, logLevel=None, *args, **kwargs):	
		"""Creates a new :class:`CustomCFN` Object
		
		:param event: Structure provided by CloudFormation to inform target lambda as to its responsibilities and actions to be taken
		:type event: dict
		:param context: This object contains information about the session and its associated data items and handlers. https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
		:type context: LambdaContext or FakeLambdaContext
		:param logger: (Optional) an instance of SimpleLogger, which is a wrapped python :class:logging object
		:type logger: SimpleLogger
		:param logLevel: representing the level of messages that should be included in logfiles.
		:type logLevel: int
		
		:return: CustomCFN Object
		:rtype: :class:CustomCFN
		"""
		
		self.logger = newLogger(logger, loggerName=utils.name_of(self), logLevel=logLevel)
		logging.getLogger('urllib3').setLevel(self.logger.level)

		# Store the event and context objects locally 
		#
		self._event = dict(event)
		self._context = context

		# If we do not have a responseURL, we need to raise an error
		#
		if self.responseURL is None:
			raise AttributeError('responseURL was not supplied, no practical way to proceed')
			
		# If the supplied event dictionary has an item FakeEvent set to true (likely because of the use of the supplied FakeEvent method in this module, then setup __testmode__
		#
		if event.get('FakeEvent', False):
			self.__testmode__()
	
		# This is really annoying, but FakeLambda Context doesn't support log_stream_name
		#
		try:
			self._log_stream_name = context.log_stream_name
		except:
			self._log_stream_name = None
		
		self._account = utils.parse_arn(context.invoked_function_arn).get('Account', None)
		self._region = utils.parse_arn(context.invoked_function_arn).get('Region', None)

		# extract data from args or event to create the responseBody for the eventual callback
		#
		self._responseBody['StackId'] = event.get('StackId', None)
		self._responseBody['RequestId'] = event.get('RequestId', None)
		self._responseBody['LogicalResourceId'] = event.get('LogicalResourceId', None)
		self._responseBody['PhysicalResourceId'] = event.get('PhysicalResourceId', None)
		
		self.logger.debug_json_dumps('Current Response', self.responseBody)


	@SimpleLogger.tracer
	def sendFailureMsg(self, reason=None):
		"""Simplified method for reporting a Falure, with support for sending an explination of the failure
		
		:param reason: An explination of the failure encountered
		:type reason: str
		
		:raises Exception: If an error occurs while sending the results, provides what is known about the issue
		"""
		logger = newLogger(self.logger)

		# Report the issues to the logs
		logger.error_tb(reason)

		try:
			self.sendResponse(responseStatus='FAILED', failureReason=reason)
			
		except Exception as e:
			msg='Unexpected issue sending FAILURE {}'.format(e)
			logger.error_tb(msg)
			raise Exception(msg)
		

	@SimpleLogger.tracer
	def sendSuccessMsg(self, responseData={}):
		"""Simplified method for reporting a Success, with support for sending attributes to be provided to the calling template
				
		:param responseData: Dictionary of keys, value to be returned
		:type responseData: dict
		
		:raises Exception: If an error occurs while sending the results, provides what is known about the issue
		"""
		logger = newLogger(self.logger)

		try:
			self.sendResponse(responseStatus='SUCCESS', responseData=responseData)
			
		except Exception as e:
			msg='Unexpected issue sending SUCCESS {}'.format(e)
			logger.error_tb(msg)
			raise Exception(msg)

			
	@SimpleLogger.tracer
	def sendResponse(self, responseStatus=None, failureReason=None, responseData=None):
		"""This method is the worker that posts the response to the HTTP endpoint specified by the caller. Typically this is a TLS protected endpoint with a S3 signature block
		
		:param responseStatus: Intended to be "SUCCESS" or "FAILED" but not strictly enforced due to AWS nature to extend existing fields
		:type responseStatus: str
		:param failureReason: Intended to be a human readable indication as to why a failure has occured and how it can be remediated. 
		:type failureReason: str
		:param responseData: a dictionary containing values to be returned to CloudFormation. Each value in the dictionary can be accessed within a template via the FN::GetAtt function. https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html
		:type responseData: dict
		"""
		
		logger = newLogger(self.logger)
		headers = {}
		
		url = self.responseURL
		
		# If responseStatus was not specified, then we are reporting a failure
		responseStatus = responseStatus or 'FAILED'

		if isinstance(responseData, dict):
			responseData = dict(responseData)
		elif responseData is None:
			pass
		else:
			responseStatus = 'FAILED'
			failureReason = "responseData can only be a 'dict' object"
		
		try:
			responseBody = self.responseBody
			responseBody['Status'] = responseStatus
			responseBody['PhysicalResourceId'] = self.physicalResourceID or self.logicalResourceID
			
			if responseData is not None:
				responseBody['Data'] = responseData

		except:
			# Bail out as best we can, as this should have never been invoked
			responseBody = self.responseBody
			responseBody['Status'] = 'FAILED'

		# Handle failures, all statements are wrapped with try/except-pass clauses
		#
		
		# Handle reporting a falure
		#
		if responseStatus == 'FAILED':
			# If we have a log_stream_name then include a link to the log in the reason
			#
			if self.log_stream_name is not None:
				try:
					responseBody['Reason'] = 'See the details in CloudWatch Log Stream: https://console.aws.amazon.com/cloudwatch/home?region={}#logEventViewer:group=/aws/lambda/CloudFormation-common-EntryPoint;stream={}'.format(self.region,self.log_stream_name)
				except:
					pass
			
			# If the caller specified a reason, prepend it to the message
			#
			if failureReason is not None:
				try:
					responseBody['Reason'] =  '{} {}'.format(failureReason, responseBody['Reason'])
				except:
					pass

		try:
			logger.debug_json_dumps('RESPONSE BODY', responseBody)
		except:
			# not great that logging failed, but no reason to bail out
			pass		
	
		try:
			encoded_responseBody = json.dumps(responseBody).encode('utf8')
		except:
			msg='Failed to marshal responseBody into utf8 json'
			logger.error(msg)
			raise Exception(msg)
			
		try:
			if url == 'http://pre-signed-S3-url-for-response':
				headers = { 'content-type': 'application/json' }
				url = 'http://httpbin.org/put'
		except:
			msg='Failed to handle faux url and divert to httpbin'
			logger.error(msg)
			raise Exception(msg)
	
		if self._testmode:
			# Well, we are not going to actually send the message, so our repsonse is 
			if responseBody['Status'] == 'FAILED':
				raise TestFailure
			else:
				raise TestSuccess
			
		# Create http connection object using certs from certifi
		#
		try:
			http = urllib3.PoolManager(ca_certs=certifi.where())
			
		except Exception as e:
			msg='Failed to create urllib3.PoolManager {}'.format(e)
			logger.error(msg)
			raise Exception(msg)

		try:
			response = http.request('PUT', url, body=encoded_responseBody, headers=headers)
			self._responseSent = True
			
		except Exception as e:
			msg='PUT Failed {}'.format(e)
			logger.error(msg)
			raise Exception(msg)

		logger.debug('Response Message "{}"'.format(response.read().decode('utf8')))
		logger.debug_json_dumps('Response Headers', dict(response.getheaders()))
		
		logger.info('Status {} Sent'.format(responseStatus))
