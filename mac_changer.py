import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC Address, use -help for help")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address, use -help for help")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Specify Interface")
    elif not options.new_mac:
        parser.error("[-] Specify New MAC Address")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for" + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not find MAC Address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[+] Current MAC Address: "+str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address Changed Successfully")
else:
    print("[-] Failed to Change MAC Address")



