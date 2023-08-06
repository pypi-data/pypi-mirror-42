import asyncio

import logging
import random

from driveline import DrivelineClient, run_async
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-1')


async def main():
    """ this example publishes every second a record of the form:
        { index: number of second since start, msg: message }
    """
    log.info('***** start *****')
    nonce = ''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(0, 16)])
    async with DrivelineClient(WS_ENDPOINT) as client:
        demo = await client.open_stream('hello-world-stream')
        i = 0
        while True:
            document = dict(index=i, msg='hello world at %s' % i, nonce=nonce)
            await demo.append(document)
            log.info('published object index %d to hello-world-stream', i)
            i += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    run_async(main())
