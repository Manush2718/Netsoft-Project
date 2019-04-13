#!/usr/bin/env python
import os
import sys
import time
import random
import paramiko
import logging

import novaclient.v1_1.client as novaClient


# Set logging format and logging level
# Can change INFO to DEBUG for more information, or WARNING for less information
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__) # Get logger for *this* module
logger.setLevel(logging.DEBUG)

# List of used VNIs in the overlay
USED_VNIS = []

################################################################################
################################################################################

# Waits until a given VM is active
#
# Input:
#   - vmObj: A VM object created by Nova
def waitUntilVMActive(vmObj):
    while vmObj.status != 'ACTIVE':
        logger.debug("Waiting for VM %s to become active..." % vmObj.name)
        time.sleep(5)
        vmObj.get() # Re-sync object state w/ OpenStack

    logger.info("VM %s is now active" % vmObj.name)

# Sets up an SSH session with a target host
#
# Input:
#   - targetIP: The target host's IP address
#   - username: The username to log-in with
#   - password: The password associated with the username
#
# Returns:
#   - A Paramiko SSH session object
def getSSHSession(targetIP, username, password):
    # Set up SSH
    sshSession = paramiko.SSHClient()
    sshSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        try:
            sshSession.connect(targetIP, username = username, password = password)
            logger.debug("SSH to %s successful" % targetIP)
            break
        except Exception as e:
            logger.debug("Waiting for SSH daemon to come up in %s..." % targetIP)
            time.sleep(5)

    return sshSession

# Runs a command over an established SSH session
#
# Input:
#   - sshSession: An active SSH session to a VM
#   - command: A string command to run within the VM
#
# Returns:
#   - A tuple containing strings of stdout and stderr (stdout, stderr), or
#     else None if an exception occurred from SSH
def runCommandOverSSH(sshSession, command):
    assert type(sshSession) is paramiko.client.SSHClient,\
            "'sshSession' is type %s" % type(sshSession)
    assert type(command) in (str, unicode), "'command' is type %s" % type(command)
    logger.debug("Running command in host %s" % sshSession._transport.sock.getpeername()[0])
    logger.debug("\t\"%s\"" % command)

    try:
        stdin, stdout, stderr = sshSession.exec_command(command)

        # Wait for command to finish (may take a while for long commands)
        while not stdout.channel.exit_status_ready() or \
                not stderr.channel.exit_status_ready():
            time.sleep(1)
    except Exception as e:
        logger.error(e)
        logger.error("ERROR: Unable to execute command over SSH:")
        logger.error("\t%s" % cmd)

        return None
    else:
        # exec_command() completed successfully
        # Check if command printed anything to stderr
        err = stderr.readlines()
        err = ''.join(err) # Convert to single string
        if err:
            logger.error("%s\n" % err)

        # Check if command printed anything to stdout
        out = stdout.readlines()
        out = ''.join(out) # Convert to single string
        if out:
            logger.debug("%s\n" % out)

        return (out, err)

# Ensures the OVS daemon is up before continuing. If OVS isn't installed in the
# system, it will be installed first. Assumes the host is a Debian-based OS
# using the aptitude package management system.
#
# Input:
#   - sshSession: An active SSH session to a VM
def waitUntilOVSActive(sshSession):
    assert type(sshSession) is paramiko.client.SSHClient,\
            "'sshSession' is type %s" % type(sshSession)

    # Check if OVS is installed, install if it's not
    cmd = "dpkg -l | grep openvswitch"
    stdout, stderr = runCommandOverSSH(sshSession, cmd)
    if not stdout: # dpkg -l didn't find anything
        logger.info("Open vSwitch is not installed, installing now...")
        cmd = "sudo apt-get update && sudo apt-get install -y openvswitch-switch"
        stdout, stderr = runCommandOverSSH(sshSession, cmd)

    cmd = "sudo service openvswitch-switch status"
    stdout, stderr = runCommandOverSSH(sshSession, cmd)
    while "not running" in stdout:
        logger.debug("Waiting for OVS to become active")
        time.sleep(5)
        stdout, stderr = runCommandOverSSH(sshSession, cmd)

# Generates a unique VXLAN Network Identifier (VNI)
# Ensures generated number isn't being used in the overlay
#
# Returns:
#   - A randomly generated number between 1 and 65536
def generateVNI():
    global USED_VNIS

    vni = random.randint(1, 2**16)
    while vni in USED_VNIS:
        vni = random.randint(1, 2**16)

    USED_VNIS.append(vni)
    return vni

# Sets controller for OVS within a switch VM to a TCP endpoint
#
# Input:
#   - switchVMObj: A VM object created by Nova
#   - ctrlEndpoint: A string of the TCP endpoint for setting the OVS controller
#       - Example: "10.20.30.40:6633"
def setController(switchVMObj, ctrlEndpoint): #Modified according to the bridge name
    tenant_name = "workshop-12"
    logger.info("Setting controller for switch in %s with IP %s" %
                                    (switchVMObj.name, ctrlEndpoint))
    networkName = tenant_name + '-net'

    switchVMIP = switchVMObj.networks.get(networkName)[0]
    switchSSH = getSSHSession(switchVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(switchSSH)

    ovsName = "sw1-br"
    cmd = "sudo ovs-vsctl set-controller %s tcp:%s" % (ovsName, ctrlEndpoint)
    runCommandOverSSH(switchSSH, cmd)


def setController2(switchVMObj, ctrlEndpoint): #Modified according to the bridge name
    tenant_name = "workshop-12"
    logger.info("Setting controller for switch in %s with IP %s" %
                                    (switchVMObj.name, ctrlEndpoint))
    networkName = tenant_name + '-net'

    switchVMIP = switchVMObj.networks.get(networkName)[0]
    switchSSH = getSSHSession(switchVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(switchSSH)

    ovsName = "sw2-br"
    cmd = "sudo ovs-vsctl set-controller %s tcp:%s" % (ovsName, ctrlEndpoint)
    runCommandOverSSH(switchSSH, cmd)

def setController3(switchVMObj, ctrlEndpoint): #Modified according to the bridge name
    tenant_name = "workshop-12"
    logger.info("Setting controller for switch in %s with IP %s" %
                                    (switchVMObj.name, ctrlEndpoint))
    networkName = tenant_name + '-net'

    switchVMIP = switchVMObj.networks.get(networkName)[0]
    switchSSH = getSSHSession(switchVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(switchSSH)

    ovsName = "sw3-br"
    cmd = "sudo ovs-vsctl set-controller %s tcp:%s" % (ovsName, ctrlEndpoint)
    runCommandOverSSH(switchSSH, cmd)

def setController4(switchVMObj, ctrlEndpoint): #Modified according to the bridge name
    tenant_name = "workshop-12"
    logger.info("Setting controller for switch in %s with IP %s" %
                                    (switchVMObj.name, ctrlEndpoint))
    networkName = tenant_name + '-net'

    switchVMIP = switchVMObj.networks.get(networkName)[0]
    switchSSH = getSSHSession(switchVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(switchSSH)

    ovsName = "sw4-br"
    cmd = "sudo ovs-vsctl set-controller %s tcp:%s" % (ovsName, ctrlEndpoint)
    runCommandOverSSH(switchSSH, cmd)

################################################################################
################################################################################

# Creates a VM using OpenStack Nova
#
# Input:
#   - vmName: Name of desired VM to be created, must be of type string
#
# Returns:
#   - The VM object created by Nova

# Boot VM for Host1

host1_ip = []
host1_name = []
host1_id = []
def bootVM1(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_1 = "EDGE-CG-1"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova1 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_1, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova1.networks.find(label = net_name)
    image = nova1.images.find(name = image)
    flavor = nova1.flavors.find(name = flavor)
    vm1 = nova1.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm1)
    host1_id.append(vm1.id)
    host1_ip.append(vm1.networks[net_name][0])
    host1_name.append(vm1)

# Boot VM for Host 2

host2_ip = []
host2_name = []
host2_id = []
def bootVM2(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_2 = "EDGE-TR-1"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova2 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_2, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova2.networks.find(label = net_name)
    image = nova2.images.find(name=image)
    flavor = nova2.flavors.find(name=flavor)
    vm2 = nova2.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm2)
    host2_id.append(vm2.id)
    host2_ip.append(vm2.networks[net_name][0])
    host2_name.append(vm2)

# Boot VM for Switch 1

switch1_ip = []
switch1_name = []
switch1_id = []
def bootVM3(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_1 = "EDGE-CG-1"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova1 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_1, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova1.networks.find(label = net_name)
    image = nova1.images.find(name=image)
    flavor = nova1.flavors.find(name=flavor)
    vm3 = nova1.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm3)
    switch1_id.append(vm3.id)
    switch1_ip.append(vm3.networks[net_name][0])
    switch1_name.append(vm3)

# Boot VM for switch sw2

switch2_ip = []
switch2_name = []
switch2_id = []
def bootVM4(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)


    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_2 = "EDGE-TR-1"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova2 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_2, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova2.networks.find(label = net_name)
    image = nova2.images.find(name=image)
    flavor = nova2.flavors.find(name=flavor)
    vm4 = nova2.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm4)
    switch2_id.append(vm4.id)
    switch2_ip.append(vm4.networks[net_name][0])
    switch2_name.append(vm4)

#Boot VM for switch sw3

switch3_ip = []
switch3_name = []
switch3_id = []
def bootVM5(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_3 = "CORE"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova3 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_3, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova3.networks.find(label = net_name)
    image = nova3.images.find(name=image)
    flavor = nova3.flavors.find(name=flavor)
    vm5 = nova3.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm5)
    switch3_id.append(vm5.id)
    switch3_ip.append(vm5.networks[net_name][0])
    switch3_name.append(vm5)

#Boot VM for host h3

host3_ip = []
host3_name = []
host3_id = []
def bootVM6(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_3 = "CORE"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova3 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_3, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova3.networks.find(label = net_name)
    image = nova3.images.find(name=image)
    flavor = nova3.flavors.find(name=flavor)
    vm6 = nova3.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm6)
    host3_id.append(vm6.id)
    host3_ip.append(vm6.networks[net_name][0])
    host3_name.append(vm6)

#Boot VM for switch sw4

switch4_ip = []
switch4_name = []
switch4_id = []
def bootVM7(vmName):
    assert type(vmName) in (str, unicode), "'vmName' is type %s" % type(vmName)

    username = "netsoft24"
    vmName = username + '-' + vmName

    logger.info("Creating VM %s" % vmName)

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_4 = "CORE"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    key_name = "netsoft24key"
    flavor = "m1.small"
    image = "ECE1508-overlay"
    nova4 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_4, no_cache=True)
    net_name = tenant_name + "-net"
    net = nova4.networks.find(label = net_name)
    image = nova4.images.find(name=image)
    flavor = nova4.flavors.find(name=flavor)
    vm7 = nova4.servers.create(name=vmName, image=image, flavor=flavor, key_name=key_name, security_groups=['netsoft24'], nics=[{'net-id': net.id}])
    waitUntilVMActive(vm7)
    switch4_id.append(vm7.id)
    switch4_ip.append(vm7.networks[net_name][0])
    switch4_name.append(vm7)

def setOverlayInterfaceHost1(hostVMObj, hostOverlayIP):
    tenant_name = "workshop-12"
    logger.info("Setting overlay for %s with IP %s" %
                        (hostVMObj.name, hostOverlayIP))
    networkName = tenant_name + '-net'

    hostVMIP = hostVMObj.networks.get(networkName)[0]
    hostSSH = getSSHSession(hostVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(hostSSH)

    h1bridge = "sudo ovs-vsctl --may-exist add-br h1-br"
    h1bridgeproto = "sudo ovs-vsctl set bridge h1-br protocols=OpenFlow10"
    h1internal = "sudo ovs-vsctl --may-exist add-port h1-br h1-internal -- set interface h1-internal type=internal"
    h1OverlayIPassign = "sudo ifconfig h1-internal "+hostOverlayIP+"/24 mtu 1450 up"
    runCommandOverSSH(hostSSH, h1bridge)
    runCommandOverSSH(hostSSH, h1bridgeproto)
    runCommandOverSSH(hostSSH, h1internal)
    runCommandOverSSH(hostSSH, h1OverlayIPassign)

def setOverlayInterfaceHost2(hostVMObj, hostOverlayIP):
    tenant_name = "workshop-12"
    logger.info("Setting overlay for %s with IP %s" %
                        (hostVMObj.name, hostOverlayIP))
    networkName = tenant_name + '-net'
    hostVMIP = hostVMObj.networks.get(networkName)[0]
    hostSSH = getSSHSession(hostVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(hostSSH)

    h2bridge = "sudo ovs-vsctl --may-exist add-br h2-br"
    h2bridgeproto = "sudo ovs-vsctl set bridge h2-br protocols=OpenFlow10"
    h2internal = "sudo ovs-vsctl --may-exist add-port h2-br h2-internal -- set interface h2-internal type=internal"
    h2OverlayIPassign = "sudo ifconfig h2-internal "+hostOverlayIP+"/24 mtu 1450 up"
    runCommandOverSSH(hostSSH, h2bridge)
    runCommandOverSSH(hostSSH, h2bridgeproto)
    runCommandOverSSH(hostSSH, h2internal)
    runCommandOverSSH(hostSSH, h2OverlayIPassign)

def setOverlayInterfaceHost3(hostVMObj, hostOverlayIP):
    tenant_name = "workshop-12"
    logger.info("Setting overlay for %s with IP %s" %
                        (hostVMObj.name, hostOverlayIP))
    networkName = tenant_name + '-net'

    hostVMIP = hostVMObj.networks.get(networkName)[0]
    hostSSH = getSSHSession(hostVMIP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running
    waitUntilOVSActive(hostSSH)

    h3bridge = "sudo ovs-vsctl --may-exist add-br h3-br"
    h3bridgeproto = "sudo ovs-vsctl set bridge h3-br protocols=OpenFlow10"
    h3internal = "sudo ovs-vsctl --may-exist add-port h3-br h3-internal -- set interface h3-internal type=internal"
    h3OverlayIPassign = "sudo ifconfig h3-internal "+hostOverlayIP+"/24 mtu 1450 up"
    runCommandOverSSH(hostSSH, h3bridge)
    runCommandOverSSH(hostSSH, h3bridgeproto)
    runCommandOverSSH(hostSSH, h3internal)
    runCommandOverSSH(hostSSH, h3OverlayIPassign)

ip_h1 = host1_ip
ip_h2 = host2_ip
ip_h3 = host3_ip
ip_sw1 = switch1_ip
ip_sw2 = switch2_ip
ip_sw3 = switch3_ip
ip_sw4 = switch4_ip
VNI_1 = []
VNI_2 = []
VNI_3 = []
VNI_4 = []
VNI_5 = []
VNI_6 = []
VNI_7 = []
def connectNodes_h1_sw1(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_1 = generateVNI()
    sw1bridge = "sudo ovs-vsctl add-br sw1-br"
    sw1bridgeproto = "sudo ovs-vsctl set bridge sw1-br protocols=OpenFlow10"
    sw1internal = "sudo ovs-vsctl add-port sw1-br sw1-internal -- set interface sw1-internal type=internal"
    h1_sw1_vxlaninterface = "sudo ovs-vsctl add-port h1-br h1-vxlan -- set interface h1-vxlan type=vxlan options:remote_ip=%s options:key=%s" % (ip_sw1[0], VNI_1)
    sw1_h1_vxlaninterface = "sudo ovs-vsctl add-port sw1-br sw1-vxlan1 -- set interface sw1-vxlan1 type=vxlan options:remote_ip=%s  options:key=%s" % (ip_h1[0], VNI_1)
    runCommandOverSSH(node2SSH, sw1bridge)
    runCommandOverSSH(node2SSH, sw1bridgeproto)
    runCommandOverSSH(node2SSH, sw1internal)
    runCommandOverSSH(node2SSH, sw1_h1_vxlaninterface)
    runCommandOverSSH(node1SSH, h1_sw1_vxlaninterface)

def connectNodes_sw1_sw2(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_2 = generateVNI()
    sw2bridge = "sudo ovs-vsctl add-br sw2-br"
    sw2bridgeproto = "sudo ovs-vsctl set bridge sw2-br protocols=OpenFlow10"
    sw2internal = "sudo ovs-vsctl add-port sw2-br sw2-internal -- set interface sw2-internal type=internal"
    sw1_sw2_vxlaninterface = "sudo ovs-vsctl add-port sw1-br sw1-vxlan2 -- set interface sw1-vxlan2 type=vxlan options:remote_ip=%s options:key=%s" % (ip_sw2[0], VNI_2)
    sw2_sw1_vxlaninterface = "sudo ovs-vsctl add-port sw2-br sw2-vxlan1 -- set interface sw2-vxlan1 type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw1[0], VNI_2)
    runCommandOverSSH(node2SSH, sw2bridge)
    runCommandOverSSH(node2SSH, sw2bridgeproto)
    runCommandOverSSH(node2SSH, sw2internal)
    runCommandOverSSH(node2SSH, sw2_sw1_vxlaninterface)
    runCommandOverSSH(node1SSH, sw1_sw2_vxlaninterface)

def connectNodes_sw2_h2(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_3 = generateVNI()
    sw2_h2_vxlaninterface = "sudo ovs-vsctl add-port sw2-br sw2-vxlan2 -- set interface sw2-vxlan2 type=vxlan options:remote_ip=%s options:key=%s" % (ip_h2[0], VNI_3)
    h2_sw2_vxlaninterface = "sudo ovs-vsctl add-port h2-br h2-vxlan -- set interface h2-vxlan type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw2[0], VNI_3)
    runCommandOverSSH(node1SSH, sw2_h2_vxlaninterface)
    runCommandOverSSH(node2SSH, h2_sw2_vxlaninterface)

def connectNodes_sw1_sw3(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_4 = generateVNI()
    sw3bridge = "sudo ovs-vsctl add-br sw3-br"
    sw3bridgeproto = "sudo ovs-vsctl set bridge sw3-br protocols=OpenFlow10"
    sw3internal = "sudo ovs-vsctl add-port sw3-br sw3-internal -- set interface sw3-internal type=internal"
    sw1_sw3_vxlaninterface = "sudo ovs-vsctl add-port sw1-br sw1-vxlan3 -- set interface sw1-vxlan3 type=vxlan options:remote_ip=%s options:key=%s" % (ip_sw3[0], VNI_4)
    sw3_sw1_vxlaninterface = "sudo ovs-vsctl add-port sw3-br sw3-vxlan1 -- set interface sw3-vxlan1 type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw1[0], VNI_4)
    runCommandOverSSH(node2SSH, sw3bridge)
    runCommandOverSSH(node2SSH, sw3bridgeproto)
    runCommandOverSSH(node2SSH, sw3internal)
    runCommandOverSSH(node2SSH, sw3_sw1_vxlaninterface)
    runCommandOverSSH(node1SSH, sw1_sw3_vxlaninterface)

def connectNodes_sw3_h3(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'
    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_5 = generateVNI()
    sw3_h3_vxlaninterface = "sudo ovs-vsctl add-port sw3-br sw3-vxlan2 -- set interface sw3-vxlan2 type=vxlan options:remote_ip=%s options:key=%s" % (ip_h3[0], VNI_5)
    h3_sw3_vxlaninterface = "sudo ovs-vsctl add-port h3-br h3-vxlan -- set interface h3-vxlan type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw3[0], VNI_5)
    runCommandOverSSH(node1SSH, sw3_h3_vxlaninterface)
    runCommandOverSSH(node2SSH, h3_sw3_vxlaninterface)

def connectNodes_sw3_sw4(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_6 = generateVNI()
    sw4bridge = "sudo ovs-vsctl add-br sw4-br"
    sw4bridgeproto = "sudo ovs-vsctl set bridge sw4-br protocols=OpenFlow10"
    sw4internal = "sudo ovs-vsctl add-port sw4-br sw4-internal -- set interface sw4-internal type=internal"
    sw3_sw4_vxlaninterface = "sudo ovs-vsctl add-port sw3-br sw3-vxlan3 -- set interface sw3-vxlan3 type=vxlan options:remote_ip=%s options:key=%s" % (ip_sw4[0], VNI_6)
    sw4_sw3_vxlaninterface = "sudo ovs-vsctl add-port sw4-br sw4-vxlan1 -- set interface sw4-vxlan1 type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw3[0], VNI_6)
    runCommandOverSSH(node2SSH, sw4bridge)
    runCommandOverSSH(node2SSH, sw4bridgeproto)
    runCommandOverSSH(node2SSH, sw4internal)
    runCommandOverSSH(node2SSH, sw4_sw3_vxlaninterface)
    runCommandOverSSH(node1SSH, sw3_sw4_vxlaninterface)

def connectNodes_sw2_sw4(node1, node2):
    tenant_name = "workshop-12"
    logger.info("Making VXLAN links between %s and %s" % (node1.name, node2.name))
    networkName = tenant_name + '-net'

    node1IP = node1.networks.get(networkName)[0]
    node1SSH = getSSHSession(node1IP, 'ubuntu', 'savi')

    node2IP = node2.networks.get(networkName)[0]
    node2SSH = getSSHSession(node2IP, 'ubuntu', 'savi')

    # Ensure OVS daemon is up and running in both nodes
    waitUntilOVSActive(node1SSH)
    waitUntilOVSActive(node2SSH)

    VNI_7 = generateVNI()
    sw2_sw4_vxlaninterface = "sudo ovs-vsctl add-port sw2-br sw2-vxlan3 -- set interface sw2-vxlan3 type=vxlan options:remote_ip=%s options:key=%s" % (ip_sw4[0], VNI_7)
    sw4_sw2_vxlaninterface = "sudo ovs-vsctl add-port sw4-br sw4-vxlan2 -- set interface sw4-vxlan2 type=vxlan options:remote_ip=%s  options:key=%s" % (ip_sw2[0], VNI_7)
    runCommandOverSSH(node2SSH, sw4_sw2_vxlaninterface)
    runCommandOverSSH(node1SSH, sw2_sw4_vxlaninterface)

def deployOverlay():
    print "In deployOverlay()"

    # Dictionaries to map switch/host names to their Nova VM objects
    createdSwitches = {}
    createdHosts = {}

    bootVM1("h1")
    bootVM2("h2")
    bootVM3("sw1")
    bootVM4("sw2")
    bootVM5("sw3")
    bootVM6("h3")
    bootVM7("sw4")
    setOverlayInterfaceHost1(host1_name[0], '192.168.200.7')
    setOverlayInterfaceHost2(host2_name[0], '192.168.200.11')
    setOverlayInterfaceHost3(host3_name[0], '192.168.200.21')
    connectNodes_h1_sw1(host1_name[0], switch1_name[0])
    connectNodes_sw1_sw2(switch1_name[0], switch2_name[0])
    connectNodes_sw2_h2(switch2_name[0], host2_name[0])
    connectNodes_sw1_sw3(switch1_name[0], switch3_name[0])
    connectNodes_sw3_h3(switch3_name[0], host3_name[0])
    connectNodes_sw3_sw4(switch3_name[0], switch4_name[0])
    connectNodes_sw2_sw4(switch2_name[0], switch4_name[0])
    ctrlEndpoint = "10.12.132.3:6633"
    setController(switch1_name[0], ctrlEndpoint)
    setController2(switch2_name[0], ctrlEndpoint)
    setController3(switch3_name[0], ctrlEndpoint)
    setController4(switch4_name[0], ctrlEndpoint)

def listOverlay():
    print "In listOverlay()"

    username = "netsoft24"
    password = "manush2718"
    tenant_name = "workshop-12"
    region_name_1 = "EDGE-CG-1"
    region_name_2 = "EDGE-TR-1"
    region_name_4 = "CORE"
    tenant_name = "workshop-12"
    auth_url = "http://iam.savitestbed.ca:5000/v2.0/"
    nova1 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_1, no_cache=True)
    nova2 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_2, no_cache=True)
    nova4 = novaClient.Client(username, password, tenant_name, auth_url, region_name=region_name_4, no_cache=True)
    net_name = tenant_name + '-net'
    controller = nova4.servers.list()[3]
    print "%s: %s (%s)" % (controller.name,controller.id,controller.networks.get(net_name)[0])
    h1 = nova1.servers.list()[1]
    print "%s: %s (%s)" % (h1.name,h1.id,h1.networks.get(net_name)[0])
    h2 = nova2.servers.list()[1]
    print "%s: %s (%s)" % (h2.name,h2.id,h2.networks.get(net_name)[0])
    sw1 = nova1.servers.list()[0]
    print "%s: %s (%s)" % (sw1.name,sw1.id,sw1.networks.get(net_name)[0])
    sw2 = nova2.servers.list()[0]
    print "%s: %s (%s)" % (sw2.name,sw2.id,sw2.networks.get(net_name)[0])
    sw3 = nova4.servers.list()[2]
    print "%s: %s (%s)" % (sw3.name,sw3.id,sw3.networks.get(net_name)[0])
    h3 = nova4.servers.list()[1]
    print "%s: %s (%s)" % (h3.name,h3.id,h3.networks.get(net_name)[0])
    sw4 = nova4.servers.list()[0]
    print "%s: %s (%s)" % (sw4.name,sw4.id,sw4.networks.get(net_name)[0])

if __name__ == "__main__":
    deployOverlay()
    listOverlay()
