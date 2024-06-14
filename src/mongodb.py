import json
import unittest
import pymongo.collection
from dataclasses import asdict
from normalize import CrowdstrikeScan, QualysScan
from pymongo import MongoClient
from pymongo.collection import BulkWriteResult
from pymongo.errors import BulkWriteError


def bulk_write(mongo_collection: pymongo.collection, documents: list) -> BulkWriteResult:
    """
    Upsert many host scans into the database.
    https://www.mongodb.com/docs/languages/python/pymongo-driver/current/write/bulk-write/#bulk-write-operations
    :param mongo_collection: pymongo.collection
    :param documents: list
    :return:
    """
    # Step 1: Draft the database operations:
    bulk_writes = list()
    for d in documents:
        scan_vendor = type(d).__name__
        hostname_to_find = None
        if scan_vendor == 'CrowdstrikeScan':
            hostname_to_find = d.hostname
        if scan_vendor == 'QualysScan':
            hostname_to_find = d.dnsHostName

        query_filter = {'hostname': hostname_to_find}
        update_op    = {'$set': {scan_vendor: asdict(d)}}
        operation    = pymongo.collection.UpdateOne(filter = query_filter,
                                                    update = update_op,
                                                    upsert = True)
        bulk_writes.append(operation)

    # Step 2: Execute the database operations:
    try:
        results = mongo_collection.bulk_write(bulk_writes)
        print(f"BulkWrite success! Upserted {results.bulk_api_result['nMatched']} records into MongoDB '{mongo_collection.full_name}'.")
        return results
    except BulkWriteError as e:
        print(f"BulkWriteError {e.details}")
        exit()


class MongoDBClientTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.mongodb    = MongoClient('mongodb://python-sa:password@localhost:27017/host_scans')
        self.db         = self.mongodb['host_scans']  # Get access to the main database.
        # self.raw        = self.db['raw']              # Get the "raw" document collection.
        self.normalized = self.db['normalized']       # Get the "normalized" document collection.

    async def asyncTearDown(self):
        self.mongodb.close()

    async def test_mongodb_upsert_many(self, ):

        # Step 1: Load our test data:
        with open('tests/sample_crowdstrike_data.json', 'r') as file:
            crowdstrike_data = json.load(file)
        with open('tests/sample_qualys_data.json', 'r') as file:
            qualys_data = json.load(file)

        # Step 2: Compile our scans from our two sources.
        # This can be made faster with a list comprehension or a map().
        # Both methods are more performant due to optimizations in Python's built-in iterator.
        # I chose less performance for easier-to-read code.
        docs = list()
        for item in crowdstrike_data:
            d  = CrowdstrikeScan(hostname  = item['hostname'],
                                 device_id = item['device_id'],
                                 scan_data = item)
            docs.append(d)
        for item in qualys_data:
            d  = QualysScan(dnsHostName  = item['dnsHostName'],
                            agentId      = item['agentInfo']['agentId'],
                            scan_data    = item)
            docs.append(d)

        # Step 3: Write our scans to the database in a way that matches them to the correct hostnames.
        results = bulk_write(mongo_collection = self.normalized, documents = docs)
        self.assertIsInstance(results, BulkWriteResult, 'Successfully loaded and updated scans into the collection.')


if __name__ == '__main__':
    unittest.main()
