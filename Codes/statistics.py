# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 12:31:06 2019

@author: Shivani
"""


#coding: utf-8

import json
import httplib2
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation

odl_controller = '142.150.208.238:8181'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

openflow_sw1 = '196220950163533'
openflow_sw2 = '11822005146949'
openflow_sw3 = '173987648823878'
openflow_sw4 = '178303508195663'

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


'''
    @name: portStat()
    @input: openflow id of swicth, port number of switch 
    @output: any quantity we want to plot
'''

def portStat(openflow_id, port_num):
    
    port_stat_url = 'http://'+odl_controller+'/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+openflow_id+'/node-connector/openflow:'+openflow_id+':'+port_num
    
    #print(port_stat_url)
    resp, content = h.request(
    uri = port_stat_url,
    method = "GET",
    headers = {'Content-Type' : 'application/json'}
    )
    a = json.loads(content)
    
    rx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['received']
    tx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['transmitted']
    port_number = a['node-connector'][0]['flow-node-inventory:port-number']
    recd_frame_err = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-frame-error']
    transmit_drops = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-drops']
    rx_err = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-errors']
    rx_bytes = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']
    tx_bytes = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
    collision_cnt = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['collision-count']
    rx_drops = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-drops']
    rx_crc_err = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-crc-error']
    tx_err =  a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-errors']
    rx_overrun_err = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-over-run-error']
    port_name = a['node-connector'][0]['flow-node-inventory:name']
    port_l2_addr = a['node-connector'][0]['flow-node-inventory:hardware-address']
    link_state_down = a['node-connector'][0]['flow-node-inventory:state']['link-down']
    
    rx_bytes_per_pkt = rx_bytes/rx_pkts
    tx_bytes_per_pkt = tx_bytes/tx_pkts 
    
    return(port_number)
    
'''
    @name: flowStat
    @inputs: openflow id of switch, table id of switch flows
    @output: any value that needs to be analyzed
'''
def flowStat(openflow_id, table_id):
    #GET  http://<controller-ip>:8080/restconf/operational/opendaylight-inventory:nodes/node/{node-id}/table/{table-id}
    
    flow_stat_url = 'http://'+odl_controller+'/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+openflow_id+'/table/'+table_id
    resp, content = h.request(
    uri = flow_stat_url,
    method = "GET",
    headers = {'Content-Type' : 'application/json'}
    )
    a = json.loads(content)
    #print(a)
    active_flows = a['flow-node-inventory:table'][0]['opendaylight-flow-table-statistics:flow-table-statistics']['active-flows']
    pkts_lookup = a['flow-node-inventory:table'][0]['opendaylight-flow-table-statistics:flow-table-statistics']['packets-looked-up']
    pkts_matched = a['flow-node-inventory:table'][0]['opendaylight-flow-table-statistics:flow-table-statistics']['packets-matched']
    
    return(active_flows)
    
'''
    @name: meterFeatures
    @input: openflow id of the switch, node id, meter id
    
def meterFeatures(openflow_id):
#GET  http://<controller-ip>:8080/restconf/operational/opendaylight-inventory:nodes/node/{node-id}
    meter_feat_url = 'http://'+odl_controller+'/restconf/operational/opendaylight-inventory:nodes/node/'+openflow_id
    resp, content = h.request(
    uri = sw1_port4stat,
    method = "GET",
    headers = {'Content-Type' : 'application/json'}
    )
    a = json.loads(content)
    port_status = a['node'][0]['node-connector'][0]['flow-node-inventory:configuration']
    return(port_status)
    '''
    
def sw1stat():
    for port_num in range(1,6):
        port_stat_sw1 = portStat(openflow_sw1, port_num)
        flow_stat_sw1 = flowStat(openflow_sw1, '0')
    return(port_stat_sw1, flow_stat_sw1)
        

def sw2stat():
    for port_num in range(1,6):
        port_stat_sw2 = portStat(openflow_sw2, port_num)
        flow_stat_sw2 = flowStat(openflow_sw1, '1')
    return(port_stat_sw2, flow_stat_sw2)
    
def sw3stat():
    for port_num in range(1,6):
        port_stat_sw3 = portStat(openflow_sw3, port_num)
        flow_stat_sw3 = flowStat(openflow_sw1, '2')
    return(port_stat_sw3, flow_stat_sw3)
    
def sw4stat():
    for port_num in range(1,5):
        port_stat_sw4 = portStat(openflow_sw4, port_num)
        flow_stat_sw4 = flowStat(openflow_sw1, '3')
    return(port_stat_sw4, flow_stat_sw4)
    
    
def animate(i, xs, ys):
    
    port_stat_sw1, flow_stat_sw1 = sw1stat()
    
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(flow_stat_sw1)
    
    ax.clear()
    ax.plot(xs, ys)
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Active flows in sw1')
    plt.ylabel('Number of active flows')
    
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
 
if __name__ == "__main__":
    sw1stat()
    


