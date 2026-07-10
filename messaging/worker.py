from .main import RabbitMQMessagingConfig,ExchangeType
from .controllers.service_controller import service_main_controller
import asyncio

async def worker():
    rabbitmq_conn=await RabbitMQMessagingConfig.get_rabbitmq_connection()
    rabbitmq_msg_obj=RabbitMQMessagingConfig(rabbitMQ_connection=rabbitmq_conn)

    from .msgqueue_consumers.activity_logs_msgqueue_consumer import activity_logs_consumer_handler
    
    # Exchanges
    exchanges=[
        {'name':'activity_logs.exchange','exc_type':ExchangeType.TOPIC},
        {'name':'utility.service.exchange','exc_type':ExchangeType.TOPIC}
    ]

    for exchange in exchanges:
        await rabbitmq_msg_obj.create_exchange(name=exchange['name'],exchange_type=exchange['exc_type'])

    # Queues
    queues=[
        {'exc_name':'activity_logs.exchange','q_name':'activity_logs.queue','r_key':'activity_logs.routing.key'},
        {'exc_name':'utility.service.exchange','q_name':'utility.service.queue','r_key':'utility.service.routing.key'}
    ]

    for queue in queues:
        queue=await rabbitmq_msg_obj.create_queue(
            exchange_name=queue['exc_name'],
            queue_name=queue['q_name'],
            routing_key=queue['r_key']
        )

    # Consumers
    consumers=[
        {'q_name':'activity_logs.queue','handler':activity_logs_consumer_handler},
        {'q_name':'utility.service.queue','handler':service_main_controller}
    ]

    for consumer in consumers:

        await rabbitmq_msg_obj.consume_event(queue_name=consumer['q_name'],handler=consumer['handler'])

    await asyncio.Event().wait()
