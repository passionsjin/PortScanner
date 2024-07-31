import logging
from xml.dom import minidom
from xml.etree import ElementTree

from nmap3 import Nmap, NmapCommandParser, user_is_root


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class CustomNmap(Nmap):
    def __init__(self, path=None):
        super(CustomNmap, self).__init__(path=path)
        self.parser = CustomNmapParser(None)

    @user_is_root
    def scan_command(self, target, arg, args=None, timeout=None):
        xml_root = super().scan_command(target, arg, args=None, timeout=None)
        logging.debug(prettify(xml_root))
        return self.parser.filter_custom(xml_root)


class CustomNmapParser(NmapCommandParser):
    def __init__(self, xml_et):
        super(CustomNmapParser, self).__init__(xml_et)

    def filter_custom(self, xmlroot):
        """
        Given the xmlroot return the all the ports that are open from
        that tree
        """
        try:
            port_result_dict = {}

            scanned_host = xmlroot.findall("host")
            stats = xmlroot.attrib

            for hosts in scanned_host:
                address = hosts.find("address").get("addr")
                port_result_dict[address] = {}  # A little trick to avoid errors

                port_result_dict[address]["osmatch"] = self.parse_os(hosts)
                port_result_dict[address]["osfingerprint"] = self.parse_osfingerprint(hosts)
                port_result_dict[address]["ports"] = self.parse_ports(hosts)
                port_result_dict[address]["hostname"] = self.parse_hostnames(hosts)
                port_result_dict[address]["macaddress"] = self.parse_mac_address(hosts)
                port_result_dict[address]["state"] = self.get_hostname_state(hosts)
                port_result_dict[address]["distance"] = self.get_distance(hosts)

            port_result_dict["runtime"] = self.parse_runtime(xmlroot)
            port_result_dict["stats"] = stats
            port_result_dict["task_results"] = self.parse_task_results(xmlroot)

        except Exception as e:
            raise e
        else:
            return port_result_dict

    def get_distance(self, xml):
        distance = xml.find("distance")
        if distance is not None:
            return distance.attrib['value']

    def parse_osfingerprint(self, os_results):
        """
        parses osfingerprint results
        """
        os = os_results.find("os")

        if os is not None:
            osfingerprint = os.find("osfingerprint")
            if osfingerprint is not None and 'fingerprint' in osfingerprint.attrib:
                return osfingerprint.attrib["fingerprint"]

        return None
