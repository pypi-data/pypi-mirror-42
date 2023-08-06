import asyncio
import logging

from driveline import DrivelineClient, run_async
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-5')

TEST_TTL = 100  # in millisecond
WAIT_DURATION = TEST_TTL + 50  # in millisecond


async def main():
    """ this simple tests demonstrates the use of TTL with the key-value store
    """
    async with DrivelineClient(WS_ENDPOINT) as client:
        log.info('storing document')
        await client.store('ephemeral', dict(test='me'), ttl=TEST_TTL)

        log.info('waiting for document expiry')
        await asyncio.sleep(WAIT_DURATION / 1000.0)

        log.info('fetching document')
        future_result = await client.load('ephemeral')
        # await the future
        result = await future_result
        if result.record is not None:
            log.error('document is %s. After TTL expiry it should be None', result.record)
        else:
            log.info('document is None, which respects the TTL configuration')
        await client.close()


if __name__ == '__main__':
    run_async(main())
