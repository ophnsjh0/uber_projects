from napalm import get_network_driver

driver = get_network_driver("eos")
device = driver("192.168.74.131", "admin", "admin")

device.open()

print(device.get_bgp_neighbors())

device.close()