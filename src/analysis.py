import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd
import unittest
from normalize import HostScan, CrowdstrikeScan, QualysScan, TenableScan


def safe_get(nested_dict: HostScan, path: str):
    """
    Check if a given field exists and is not None in a nested dictionary.

    :param nested_dict: The nested dictionary to check.
    :param path: List of keys representing the path to the field. Example: "CrowdstrikeScan.scan_data.os_version"
    :return: The value if the field exists. Otherwise, it returns None.
    """
    keys         = path.split('.')
    current_dict = nested_dict

    try:
        for key in keys:
            current_dict = getattr(current_dict, key)
        return current_dict
    except KeyError:
        return None


def extract_os(host: HostScan) -> dict:
    """
    Get hostnames and os for population graph.
    TODO Make this accept a HostScan object instead of dict
    :param host:
    :return:
    """
    # if (os := safe_get(nested_dict = item, path = "CrowdstrikeScan.scan_data.os_version")) is None:
    #     os  = safe_get(nested_dict = item, path = "QualysScan.scan_data.os")
    try:
        os = host.CrowdstrikeScan.scan_data['os_version']
    except AttributeError as e:
        # print(e)
        os = host.QualysScan.scan_data['os']


    result = {
        "hostname": host.hostname,
        "os":       os
    }
    return result


def extract_host_age(host: HostScan) -> dict:
    """
    Get hostname and first seen date from our database.
    :param host:
    :return dict:
    """
    try:
        first_seen = host.CrowdstrikeScan.scan_data['first_seen']
    except AttributeError as e:
        # print(e)
        first_seen = None

    result = {
        "hostname":   host.hostname,
        "first_seen": first_seen
    }
    return result


def graph_os_populations(collection: list[HostScan], destination: str):

    # Extract data from all items and convert to a DataFrame:
    chart_data = [extract_os(d) for d in collection]

    # Convert the extracted data to a DataFrame
    df = pd.DataFrame(chart_data)

    # Drop rows with missing 'os_version'
    df = df.dropna(subset=['os'])

    # Group by 'os_version' and count occurrences
    os_counts = df['os'].value_counts()

    # Plotting the pie chart
    plt.figure(figsize=(10, 8))  # Adjust figure size as needed

    # Plotting the pie chart
    plt.pie(x = os_counts, labels=os_counts.index, autopct='%1.1f%%', startangle=140)

    plt.title('Operating System Distribution Across Hosts')
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is drawn as a circle

    plt.tight_layout()
    # plt.show()

    file_name = destination + 'os_populations' + '_' + str(datetime.datetime.now(tz = datetime.timezone.utc)) + '.png'
    plt.savefig(file_name)


def graph_old_vs_new_hosts(collection: list[HostScan], destination: str):

    # Extract data from all items and convert to a DataFrame:
    chart_data = [extract_host_age(d) for d in collection]
    df = pd.DataFrame(chart_data)

    # Plotting the pie chart
    plt.figure(figsize = (10, 8))

    # Convert 'first_seen' column to datetime format
    df['first_seen'] = pd.to_datetime(df['first_seen'])

    # Qualys does not have a "first seen" datapoint:
    df = df.dropna(subset=['first_seen'])

    # Calculate the cutoff date (30 days ago from today)
    cutoff_date = datetime.datetime.now(tz = datetime.timezone.utc) - datetime.timedelta(days = 30)
    cutoff_date = pd.to_datetime(cutoff_date)

    # Count the number of hosts older and younger than 30 days:
    older_than_30_days   = df[df['first_seen'] <  cutoff_date].shape[0]
    younger_than_30_days = df[df['first_seen'] >= cutoff_date].shape[0]

    # Data for pie chart
    counts = [older_than_30_days, younger_than_30_days]
    labels = ['Older than 30 days', 'Younger than 30 days']

    # Plotting the pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(counts, labels = labels, autopct = '%1.1f%%', colors = ['lightcoral', 'lightskyblue'])
    plt.title('Distribution of Hosts Older and Younger than 30 Days')
    plt.tight_layout()
    # plt.show()

    file_name = destination + 'old_vs_new_hosts' + '_' + str(datetime.datetime.now(tz = datetime.timezone.utc)) + '.png'
    plt.savefig(file_name)


def graph_vuln_counts(collection: list[HostScan], destination: str):

    # Extract vulnerability IDs from the scans
    vuln_ids = []
    for d in collection:
        if qs := getattr(d, "QualysScan"):
            if 'vuln' in qs.scan_data:
                for i in qs.scan_data['vuln']['list']:
                    vuln_ids.append(i['HostAssetVuln']['qid'])  # Get vuln id

    # Convert the list to a pandas DataFrame
    vuln_df = pd.DataFrame(vuln_ids, columns=['qid'])

    # Count the occurrences of each vulnerability ID
    vuln_counts = vuln_df['qid'].value_counts()

    # Get the top vulnerabilities
    top_vulns = vuln_counts.head(20)

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    # vuln_counts.plot(kind='bar')
    top_vulns.plot(kind='bar')
    plt.title('Count of Each Vulnerability found')
    plt.xlabel('Vulnerability ID')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show the plot
    # plt.show()
    file_name = destination + 'vuln_counts' + '_' + str(datetime.datetime.now(tz = datetime.timezone.utc)) + '.png'
    plt.savefig(file_name)



class AnalysisTests(unittest.TestCase):
    """Run each test in parallel to save time"""

    def setUp(self):
        """Load the MongoDB sample data into a "collection" variable. """
        with open("tests/sample_db_host_scans.normalized.json", "r") as file:
            self.collection = json.load(file)
            file.close()
            self.collection = [
                HostScan(
                    hostname        = d['hostname'],
                    CrowdstrikeScan = (
                        CrowdstrikeScan(
                            hostname  = cs["hostname"],
                            device_id = cs["device_id"],
                            scan_data = cs["scan_data"]
                        ) if (cs := d.get("CrowdstrikeScan")) else None
                    ),
                    QualysScan=(
                        QualysScan(
                            dnsHostName = qs["dnsHostName"],
                            agentId     = qs["agentId"],
                            scan_data   = qs["scan_data"]
                        ) if (qs := d.get("QualysScan")) else None
                    ),
                    TenableScan = (
                        TenableScan(
                            host_name  = ts['host_name'],
                            tenable_id = ts['tenable_id'],
                            scan_data  = ts
                        ) if (ts := d.get("QualysScan")) else None
                    )
                ) for d in self.collection
            ]

    # TODO Generate each of these charts in a multithreaded manner:
    @unittest.skip
    def test_os_chart(self):
        graph_os_populations(collection = self.collection, destination = '../local_output/')

    @unittest.skip
    def test_hold_vs_new_hosts(self):
        # Old hosts (last seen more than 30 days ago) vs newly discovered hosts
        graph_old_vs_new_hosts(collection = self.collection, destination = '../local_output/')

    def test_vuln_counts(self):
        graph_vuln_counts(collection = self.collection, destination = '../local_output/')


if __name__ == "__main__":
    unittest.main()
