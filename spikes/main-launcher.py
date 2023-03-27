import main
import uasyncio as asyncio

try:
    asyncio.run(main.audioInputMain())
finally:
    asyncio.new_event_loop()


###########################################

import main
import uasyncio as asyncio

try:
    asyncio.run(main.eventReceiverMain())
finally:
    asyncio.new_event_loop()
