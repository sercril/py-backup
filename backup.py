import os
import sys
import boto3
import logging

s3 = boto3.resource('s3')
bucket = s3.Bucket('am-pc-backups')
prefix = 'laptop'
log_file_name='./out.log'
log_level='DEBUG'

existing_keys = []

def init():
    # TODO: Ouput setting from settings file when that is set up
    log_level_int = getattr(logging, log_level.upper(), None)
    if not isinstance(log_level_int, int):
        log_level_int = getattr(logging, 'WARNING', None)
    logging.basicConfig(
        filename=log_file_name,
        filemode='w',
        level=log_level_int,
        format='%(asctime)s %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logging.debug('Initializing list of existing keys...')
    existing_keys = [o.key for o in bucket.objects.filter(
        Prefix=prefix
    )]
    logging.debug(f'There are {len(existing_keys)} existing keys.')

def upload_file(filepath):
    try:
        bucket.Object(f'{prefix}{filepath}').upload_file(filepath)
    except e:
        logging.error(e)


def process_dir(path):
    for current_path, dirs, files in os.walk(dir):
        logging.debug(f'Current path: {current_path}')
        for f in files:
            current_file_path = os.path.join(current_path, f)
            logging.debug('In file loop...')
            logging.debug(current_file_path)
            upload_file(current_file_path)
        
        for d in dirs:
            logging.debug('In dir loop...')
            logging.debug(os.path.join(current_path, d))


# def is_new_object(path):


#     return path in existing_keys


if __name__ == "__main__":
    init()
    dir = '/home/august/Documents'

    process_dir(dir)
