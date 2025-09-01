import time
from PIL import Image
from harvesters.core import Harvester
def force_ip(h):

    device_info_node_map = h.device_info_list[0].parent.node_map
    # Let ForceIP finish
    while not device_info_node_map.GevDeviceForceIP.is_done():
        time.sleep(0.1)
def c():
    # Create the Harvester instance
    h = Harvester()
    h.add_file('SICKGigEVisionTL.cti')

    h.files

    h.update()

    # Perform force IP to change to change to same subnet as PC.
    force_ip(h)
    h.update()

    with h.create(0) as ia:
        # Get the node map from the device

        
        node_map = ia.remote_device.node_map
        mac_address_node = node_map.GevMACAddress

                # Get and print the MAC address value
        mac_address = mac_address_node.value
        # print(f"Connected Camera MAC Address: {mac_address}")
        
    # return mac_address
        h.reset()
        return mac_address
if __name__ == "__main__":
    # execute only if run as a script
    c()