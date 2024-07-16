import asyncio
import os
import sys
from normalize import CrowdstrikeScan, HostScan, QualysScan, TenableScan
from pymongo import MongoClient
from silk import SilkClient
from mongodb import bulk_write_host_scans
from analysis import *


async def main():
    """
    Extract data from the Silk Interview API,
    Transform/Merge the data into a unified HostScan document,
    Upload the data to MongoDB,
    Create charts of the data.
    :return:
    """

    # Step 0: Initialize our integrations:
    if (silk_api_token := os.getenv('silk_api_token')) is None:  # Attempt to get environment variable
        print(f"Environment variable silk_api_token is not set.")
        sys.exit('API token error')
    mongodb    = MongoClient('mongodb://python-sa:password@localhost:27017/host_scans')
    db         = mongodb['host_scans']  # Get access to the main database.
    normalized = db['normalized']       # Get the "normalized" document collection.

    # Step 1: Extract the data from the Silk API:
    async with SilkClient(silk_api_token = silk_api_token) as silk_client:
        crowdstrike_data = await silk_client.get_crowdstrike_data()
        qualys_data      = await silk_client.get_qualys_data()
        tenable_data     = await silk_client.get_tenable_data()

    # Step 2: Transform the data and upload it to MongoDB:
    docs = list()
    scans = list()
    for item in crowdstrike_data:
        d = CrowdstrikeScan(hostname  = item['hostname'],
                            device_id = item['device_id'],
                            scan_data = item)
        scans.append(d)
    for item in qualys_data:
        d = QualysScan(dnsHostName=item['dnsHostName'],
                       agentId=item['agentInfo']['agentId'],
                       scan_data=item)
        scans.append(d)
    for item in tenable_data:
        d = TenableScan(host_name=item['host_name'],
                        tenable_id=item['tenable_id'],
                        scan_data=item)
        scans.append(d)



    results = bulk_write(mongo_collection = normalized, documents = scans)


    results = bulk_write_host_scans(mongo_collection = normalized, documents = scans)

    # TO DO: Remove this code. Decided to use Grafana for graphing instead of hand-coding everything.
    # Step 3: Analyze the data inside MongoDB:
    # This totally does not scale with large databases. You would want to use the "dask" module to build dataframe in batches.
    # all_documents = [HostScan(hostname = d['hostname'], CrowdstrikeScan = , QualysScan =) for d in normalized.find()]
    # all_documents = list(normalized.find())
    # all_HostScans = [
    #                 HostScan(
    #                     hostname        = d['hostname'],
    #                     CrowdstrikeScan = (
    #                         CrowdstrikeScan(
    #                             hostname  = cs["hostname"],
    #                             device_id = cs["device_id"],
    #                             scan_data = cs["scan_data"]
    #                         ) if (cs := d.get("CrowdstrikeScan")) else None
    #                     ),
    #                     QualysScan=(
    #                         QualysScan(
    #                             dnsHostName = qs["dnsHostName"],
    #                             agentId     = qs["agentId"],
    #                             scan_data   = qs["scan_data"]
    #                         ) if (qs := d.get("QualysScan")) else None
    #                     )
    #                 ) for d in all_documents
    #                 ]
    print(f"Got {len(all_HostScans)} host scans.")
    # Disabled the visualization step because it can be demonstrated by running the analysis unittests:
    # graph_os_populations(collection   = all_HostScans, destination = './')
    # graph_old_vs_new_hosts(collection = all_HostScans, destination = './')


if __name__ == "__main__":
    asyncio.run(main())
