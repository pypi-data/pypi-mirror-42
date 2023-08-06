import logging

from driveline import DrivelineClient, run_async
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-4')


async def main():
    async with DrivelineClient(WS_ENDPOINT) as client:
        log.info('***** started *****')
        await show_list(client, 'streams')
        await show_list(client, 'keys')
        log.info('***** done *****')
        await client.close()


async def show_list(client, kind):
    log.info('listing %s in driveline:', kind)
    count = 0
    async for entry_name in await getattr(client, 'list_%s' % kind)('*'):
        log.info('found %s "%s"', kind[:-1], entry_name)
        count += 1
    if count == 0:
        log.info('no %s could be found', kind)
    else:
        log.info('found %d %s', count, kind)

    log.info('done listing %s', kind)


if __name__ == '__main__':
    run_async(main())
