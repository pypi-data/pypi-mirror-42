import logging

from driveline import DrivelineClient, run_async
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-2')


def query_cb(result):
    try:
        log.info("received document: %s", result.record)
    except Exception as e:
        log.error('subscription error: %s', e)


async def main():
    """ this example demonstrates how to set a subscriber.
        you should run it alongside example-1
    """
    async with DrivelineClient(WS_ENDPOINT) as client:
        log.debug('***** start *****')
        await client.continuous_query('SELECT * FROM STREAM "hello-world-stream"', query_cb)


if __name__ == '__main__':
    run_async(main())
