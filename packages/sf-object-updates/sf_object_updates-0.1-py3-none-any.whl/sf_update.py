# this library contains the routines and classes for a client to get salesforce object updates
# there is an assumption that AWS environment variables are set or there exists an AWS credential fiel to
# get the default profile from

import logging
import boto3
from threading import Thread, Lock, current_thread
import time
import json
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)

DEFAULT_REGION_NAME = 'us-west-1'

RETRY_EXCEPTIONS = ('ProvisionedThroughputExceededException',
                    'ThrottlingException')


class SFUpdates:
    def __init__(self, stream_name, region_name = DEFAULT_REGION_NAME, shard_position_table_name = 'shard_positions',
                 shard_position_region_name = DEFAULT_REGION_NAME):
        self.stream_name = stream_name
        self.kinesis_client = boto3.client('kinesis', region_name = region_name)
        self.shard_position_table = boto3.resource('dynamodb', region_name = 'us-west-2').Table(shard_position_table_name)
        self.lock = Lock()
        return

    
    def stop(self):
        """To stop all threads"""
        logger.info('stopping all threads')
        self._stop = True
        for thread in self.threads:
            if thread != current_thread():
                thread.join()
        logger.info('stopped')

    def run(self, callback, shard_number):
        logger.info('running thread for shard_number %d' % shard_number)
        with self.lock:
            shard_position = self.shard_positions[str(shard_number)]
            shard_id = self.shards[shard_number]['ShardId']
        if '' == shard_position:
            logger.info('not found any position, starting at oldest record in shard')
            shard_iterator = self.kinesis_client.get_shard_iterator(StreamName=self.stream_name,
                                                                    ShardId=shard_id,
                                                                    ShardIteratorType='TRIM_HORIZON')
        else:
            logger.info('starting at position %s' % shard_position)
            shard_iterator = self.kinesis_client.get_shard_iterator(StreamName=self.stream_name,
                                                                    ShardId=shard_id,
                                                                    ShardIteratorType='AFTER_SEQUENCE_NUMBER',
                                                                    StartingSequenceNumber=shard_position)

        while not self._stop:
            my_shard_iterator = shard_iterator['ShardIterator']
            while True:
                if self._stop:
                    break
                try:
                    record_response = self.kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=1000)
                    logger.info('record response: %s' % record_response)
                except ClientError as err:
                    if err.response['Error']['Code'] not in RETRY_EXCEPTIONS:
                        self.stop()
                        raise
                    # sleep for another second and continue
                    logger.warning('got ProvisionedThroughputExceededException, sleeping for 1 second')
                    time.sleep(1)
                    continue
                    
                my_shard_iterator = record_response.get('NextShardIterator', None)
                if not my_shard_iterator:
                    break
                records = record_response['Records']
                logger.info('found %d records in shard %d' % (len(records), shard_number))
                for record in record_response['Records']:
                    data = json.loads(record['Data'])
                    try:
                        callback(data)
                        with self.lock:
                            self.shard_positions[str(shard_number)] = record['SequenceNumber']
                            logger.info('storing %s in dynamodb table' % self.shard_positions)
                            self.shard_position_table.put_item(Item={'stream_name':self.stream_name, 'shard_positions':json.dumps(self.shard_positions)})
                        # wait for 5 seconds
                    except:
                        # if there is an error, then shutdown all threads
                        logger.exception('error in shard %d, shutting down all threads' % shard_number)
                        self.stop()
                time.sleep(5)
        logger.info('exiting thread for shard %d' % shard_number)
        return

                

    def put_record(self, data, partition_key):
        data = json.dumps(data)
        logger.info('writing %s to kinesis stream' % data)
        return self.kinesis_client.put_record(StreamName=self.stream_name, Data=data, PartitionKey=partition_key)
    
    def start(self, callback, from_start = False):
        """call callback function for each sf update, arguments will be:
        OBJECT-TYPE, OBJECT-INSTANCE-ID, OPERATION-TYPE and OBJECT-FIELDS
        """
        self._stop = False
        response = self.kinesis_client.describe_stream(StreamName = self.stream_name)
        self.shards = response['StreamDescription']['Shards']
        logger.info('Found %d shards for stream %s' % (len(self.shards), self.stream_name))

        response = {}
        if not from_start:
            response = self.shard_position_table.get_item(Key={'stream_name': self.stream_name})
        if 'Item' in response:
            self.shard_positions = json.loads(response['Item']['shard_positions'])
        else:
            self.shard_positions = {str(j):'' for j in range(0, len(self.shards))}
        self.threads = [Thread(target=self.run, args=(callback, j)) for j in range(0, len(self.shards))]
        for thread in self.threads:
            thread.start()
            
        

        
        
