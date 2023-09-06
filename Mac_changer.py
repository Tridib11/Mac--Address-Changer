import subprocess
import optparse
import re

def get_Arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC Address")

    (options, arguments) = parser.parse_args()  # Parse the command-line arguments

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.newMac:
        parser.error("[-] Please specify a new MAC address, use --help for more info")

    return options

def change_Mac(interface, newMac):
    print("[+] Changing MAC address for " + interface + " to " + newMac)

    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
def get_current_mac(interface):
    ifconfig_result_bytes = subprocess.check_output(["ifconfig", interface])
    ifconfig_result_str = ifconfig_result_bytes.decode('utf-8')  # Decode the bytes to a string
    # print(ifconfig_result_str)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_str)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read the MAC address")


options = get_Arguments()
interface = options.interface
newMac = options.newMac

current_mac=get_current_mac(options.interface)
print("Current Mac = "+str(current_mac))
change_Mac(interface, newMac)
current_mac=get_current_mac(options.interface)
if current_mac==options.newMac:
    print("[-] MAC address was successfully changed to "+current_mac)
else:
    print("[-] MAC address didnot get changed")

