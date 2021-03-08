import asyncio
import json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from fake_web_events import Simulation


async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str='<connection-string>', eventhub_name='<event-hub>')
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch() 

        # Create dummy event data
        simulation = Simulation(user_pool_size=100, sessions_per_day=100000)
        events = simulation.run(duration_seconds=60)
        for event in events:
            event_data = json.dumps(event)

            # Add events to the batch.
            event_data_batch.add(EventData(event_data))

            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

