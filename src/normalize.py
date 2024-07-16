from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CrowdstrikeScan:
    """
    1 Crowdstrike host scan.

    Attributes:
        hostname (str)
        device_id (str)
        scan_data (dict)
    """
    hostname: str
    device_id: str
    scan_data: dict


@dataclass
class QualysScan:
    """
    1 Qualys host scan.

    Attributes:
        dnsHostName (str)
        agentId (str)
        scan_data   (dict)
    """
    dnsHostName: str
    agentId: str
    scan_data: dict

@dataclass
class TenableScan:
    """
    1 Tenable host scan.

    Attributes:
        host_name (str)
        tenable_id (str)
        scan_data   (dict)
    """
    host_name: str
    tenable_id: str
    scan_data: dict

# Not used:
@dataclass
class HostScan:
    """
    1 host with all related scans.

    Attributes:
        hostname (str) The hostname of the scanned host/device.
        CrowdstrikeScan: Optional[CrowdstrikeScan] Optional nested object to normalize the two data sources.
        QualysScan:      Optional[QualysScan]      Optional nested object to normalize the two data sources.
    """
    vendor: str
    app_name: str
    version_installed: str

@dataclass
class HostScan:
    """
    1 host with all related scans.

    Attributes:
        hostname (str) The hostname of the scanned host/device.
        CrowdstrikeScan: Optional[CrowdstrikeScan] Optional nested object to normalize the two data sources.
        QualysScan:      Optional[QualysScan]      Optional nested object to normalize the two data sources.
    """
    hostname:        str
    CrowdstrikeScan: Optional[CrowdstrikeScan] = None
    QualysScan:      Optional[QualysScan]      = None
    TenableScan:     Optional[TenableScan]     = None
    install_apps:    Optional[List[App]]       = None

