import logging

from driveline import DrivelineClient, run_async
from settings import WS_ENDPOINT

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('example-3')

KEY_NAME = 'key/%d'


async def main():
    async with DrivelineClient(WS_ENDPOINT) as client:
        log.info('***** starting *****')
        for i in range(1, 100):
            key_name = KEY_NAME % i
            log.info('storing document to key %s', key_name)
            document = dict(index=i, keyname=key_name)
            await client.store(key_name, document)
        log.info('***** done *****')
        await client.close()


if __name__ == '__main__':
    run_async(main())
