import boto3
from datetime import date, datetime
from botocore.exceptions import ClientError


class KinesisPipeline:
    """
    Scrapy pipeline to store items into Kinesis.
    """

    def __init__(self, settings, stats):
        self.stats = stats

        self.max_chunk_size = settings.getint('KINESISPIPELINE_MAX_CHUNK_SIZE', 100)
        self.stream_name = settings['KINESISSTREAM_NAME']
        self.partition_key = settings['KENISISPARTITION_KEY']

        self.kinesis = boto3.client('kinesis')
        self.items = []
        self.chunk_number = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)

    def process_item(self, item, spider):
        """
        Process single item. Add item to items and then send to Kinesis if size of items
        >= max_chunk_size.
        """

        # Send records to Kinesis
        self.items.append(item)
        if len(self.items) >= self.max_chunk_size:
            self._send_records()

    def open_spider(self, spider):
        """
        Callback function when spider is open.
        """

    def close_spider(self):
        """
        Callback function when spider is closed.
        """
        # Upload remaining items to Kinesis.
        self._send_records()

    def _send_records(self):
        """
        Send current item list to Kinesis.
        """
        if not self.items:
            return  # Do nothing when items is empty

        try:
            self.kinesis.put_records(StreamName=self.stream_name, Records=self.items)
        except ClientError:
            self.stats.inc_value('pipeline/kinesis/fail')
            raise
        else:
            self.stats.inc_value('pipeline/kinesis/success')
        finally:
            # Prepare for the next chunk
            self.chunk_number += len(self.items)
            self.items = []

    @staticmethod
    def _json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))
