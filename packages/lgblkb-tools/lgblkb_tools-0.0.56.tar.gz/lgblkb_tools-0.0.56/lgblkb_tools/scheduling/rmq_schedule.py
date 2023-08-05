import json
from lgblkb_tools import global_support as gsup
import lgblkb_tools.log_support as logsup
from pika.adapters.blocking_connection import BlockingChannel
import pika
import functools
from functools import partial

pika_connection_params=partial(pika.ConnectionParameters)

def does_func_has_classarg(func,*args):
	has_classarg=False
	if args:
		funcattr=getattr(args[0],func.__name__,None)
		if funcattr is not None and hasattr(funcattr,'__self__'):
			has_classarg=True
	return has_classarg

class ConnectionManager(object):
	
	def __init__(self,**connection_kwargs):
		self.connection_kwargs=connection_kwargs
		pass
	
	def create_queue_manager(self,exchange='main_exchange'):
		return MessageManager(exchange,**self.connection_kwargs)

class MessageManager(object):
	
	def __init__(self,exchange,**connection_kwargs):
		self.connection_kwargs=connection_kwargs
		self.exchange=exchange
	
	def create_queue(self,queue_name,routing_key=None,exchange=None,channel=None,**queue_kwargs):
		if exchange is None: exchange=self.exchange
		if routing_key is None: routing_key=queue_name
		
		def create_queue_with_channel(_channel: BlockingChannel):
			_channel.exchange_declare(exchange=exchange,exchange_type='topic',durable=True,)
			_channel.queue_declare(queue=queue_name,**dict(dict(durable=True),**queue_kwargs),arguments={'x-max-priority':10})
			_channel.queue_bind(queue=queue_name,exchange=exchange,routing_key=routing_key)
		
		if channel is not None: create_queue_with_channel(channel)
		else:
			with pika.BlockingConnection(pika_connection_params(**self.connection_kwargs)) as connection:
				create_queue_with_channel(connection.channel())
	
	def send_message(self,message,routing_key,priority=5,exchange=None):
		with pika.BlockingConnection(pika_connection_params(**self.connection_kwargs)) as connection:
			channel: BlockingChannel=connection.channel()
			dumped_message=json.dumps(message)
			publish_result=channel.basic_publish(exchange=exchange,
			                                     routing_key=routing_key,body=dumped_message,
			                                     properties=pika.BasicProperties(delivery_mode=2,priority=priority))
			logsup.logger.info('Sent message: %s',dumped_message)
			return publish_result
	
	def with_send(self,routing_key,priority=5,exchange=None):
		if exchange is None: exchange=self.exchange
		
		def wrapper_getter(func):
			@functools.wraps(func)
			def wrapper(*args,**_kwargs):
				has_classarg=does_func_has_classarg(func,*args)
				with pika.BlockingConnection(pika_connection_params(**self.connection_kwargs)) as connection:
					channel: BlockingChannel=connection.channel()
					if has_classarg: result=func(args[0],*args[1:],**_kwargs)
					else: result=func(*args,**_kwargs)
					message=json.dumps(result)
					channel.basic_publish(exchange=exchange,
					                      routing_key=routing_key,body=message,
					                      properties=pika.BasicProperties(delivery_mode=2,priority=priority))
					logsup.logger.info('Sent message: %s',message)
					return result
			
			return wrapper
		
		return wrapper_getter
	
	def with_receive(self,queue_name,routing_key=None,exchange=None,**queue_kwargs):
		if routing_key is None: routing_key=queue_name
		
		def wrapper_getter(func):
			@functools.wraps(func)
			def wrapper(*args,**_kwargs):
				has_classarg=does_func_has_classarg(func,*args)
				
				with pika.BlockingConnection(pika_connection_params(**self.connection_kwargs)) as connection:
					channel: BlockingChannel=connection.channel()
					self.create_queue(queue_name,exchange=exchange,routing_key=routing_key,
					                  channel=channel,**queue_kwargs)
					
					def callback(ch: BlockingChannel,method,properties,body):
						message=json.loads(body)
						logsup.logger.info('Received message: %s',message)
						assert isinstance(message,dict),"The message should be of dict instance."
						success=False
						result=None
						try:
							if has_classarg: success,result=func(args[0],message,*args[1:],**_kwargs)
							else: success,result=func(message,*args,**_kwargs)
						
						except Exception as e:
							logsup.logger.inform(str(e),exc_info=True)
						assert type(success) is bool,"The message receiving function should return a tuple (success,payload)"\
						                             "with success (bool) indicating positive or negative acknowledgement."
						if success:
							ch.basic_ack(delivery_tag=method.delivery_tag)
						else:
							ch.basic_nack(delivery_tag=method.delivery_tag,requeue=False)
						return result
					
					channel.basic_qos(prefetch_count=1)
					channel.basic_consume(callback,queue=queue_name)
					logsup.logger.info(' [*] Waiting for messages. To exit press CTRL+C')
					channel.start_consuming()
			
			return wrapper
		
		return wrapper_getter
