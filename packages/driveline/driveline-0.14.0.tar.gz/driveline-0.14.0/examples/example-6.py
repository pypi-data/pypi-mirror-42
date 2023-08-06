import logging

from driveline import DrivelineClient, run_async
from driveline.video import VideoHandler
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-6')


def message_cb(frame):
    log.info('received frame: %s', frame)


async def main():
    """ example demonstrating the use of driveline-video in conjunction with driveline
    """
    async with DrivelineClient(WS_ENDPOINT) as client:
        await client.continuous_query('SELECT * FROM STREAM video_stream', VideoHandler(message_cb))


if __name__ == '__main__':
    run_async(main())
