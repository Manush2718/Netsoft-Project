# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 20:42:51 2019

@author: Shivani
"""

#coding: utf-8
import sys
import time
import json
import httplib2
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation


odl_controller = '142.150.208.238:8181'


openflow_id = '196220950163533'
sw1_flow4stat = sw1_flow4stat = 'http://'+odl_controller+'/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+openflow_id+'/node-connector/openflow:'+openflow_id+':4'

h = httplib2.Http(".cache")

h.add_credentials('admin', 'admin')
resp, content = h.request(
    uri = sw1_flow4stat,
    method = "GET",
    headers = {'Content-Type' : 'application/json'}
    )
a = json.loads(content)
#print(a)
#rx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['received']
#tx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['transmitted']

#print(rx_pkts)

#print(tx_pkts)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def fetch():
    odl_controller = '142.150.208.238:8181'


    openflow_id = '173987648823878'
    sw1_flow4stat = sw1_flow4stat = 'http://'+odl_controller+'/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+openflow_id+'/node-connector/openflow:'+openflow_id+':4'
    
    h = httplib2.Http(".cache")
    
    h.add_credentials('admin', 'admin')
    resp, content = h.request(
        uri = sw1_flow4stat,
        method = "GET",
        headers = {'Content-Type' : 'application/json'}
        )
    a = json.loads(content)
    rx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['received']
    print(rx_pkts)
    tx_pkts = a['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['transmitted']
    print(tx_pkts)
    return(tx_pkts)
    
def animate(i, xs, ys):
    
    tx_pkts = fetch()
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(tx_pkts)
    
    xs = xs[-20:]
    ys = ys[-20:]
    
    ax.clear()
    ax.plot(xs, ys)
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Ping packets transmitted over time')
    plt.ylabel('Number of packets')
    return()

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=5000)
plt.show()
