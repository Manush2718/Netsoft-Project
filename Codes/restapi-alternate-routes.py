import sys
import time
import json
import httplib2

# URL for Switch-3 Port-2 statistics
Port2_Stat_SW3_Url = 'http://142.150.208.228:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:86126267218505/node-connector/openflow:86126267218505:2'

# URLs for injecting 1 new flow in switch 1, 2 new flow in switch 3, 3 new flows in switch 2 and 4 new flows in switch 4
SW3_new_flow1 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:86126267218505/table/4/flow/5'
SW3_new_flow2 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:86126267218505/table/4/flow/6'
SW2_new_flow1 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:261711686589256/table/5/flow/5'
SW2_new_flow2 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:261711686589256/table/5/flow/6'
SW2_new_flow3 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:261711686589256/table/5/flow/7'
SW4_new_flow1 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:266350964029250/table/6/flow/1'
SW4_new_flow2 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:266350964029250/table/6/flow/2'
SW4_new_flow3 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:266350964029250/table/6/flow/3'
SW4_new_flow4 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:266350964029250/table/6/flow/4'
SW1_new_flow1 = 'http://142.150.208.228:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:266874693210436/table/7/flow/7'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def get_sw3_port2_info():
    resp, content = h.request(
        uri = Port2_Stat_SW3_Url,
        method = "GET",
        headers = {'Content-Type' : 'application/json'}
        )
    a = json.loads(content)
    b = a['node-connector'][0]['flow-node-inventory:configuration']
    return b

def put_sw3_flow5():
    resp, content = h.request(
        uri = SW3_new_flow1,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "4",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "4",
            "id": "5",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.21/32",
              "ipv4-destination": "192.168.200.11/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-3-flow-5",
            "priority": "49500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw3_flow6():
    resp, content = h.request(
        uri = SW3_new_flow2,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "4",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "4",
            "id": "6",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.21/32",
              "ipv4-destination": "192.168.200.7/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-3-flow-6",
            "priority": "49500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw2_flow5():
    resp, content = h.request(
        uri = SW2_new_flow1,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "4",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "5",
            "id": "5",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.11/32",
              "ipv4-destination": "192.168.200.21/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-2-flow-5",
            "priority": "9500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw2_flow6():
    resp, content = h.request(
        uri = SW2_new_flow2,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "4",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "5",
            "id": "6",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.7/32",
              "ipv4-destination": "192.168.200.21/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-2-flow-6",
            "priority": "9500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw2_flow7():
    resp, content = h.request(
        uri = SW2_new_flow3,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "2",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "5",
            "id": "7",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.21/32",
              "ipv4-destination": "192.168.200.7/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-2-flow-7",
            "priority": "9500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw4_flow1():
    resp, content = h.request(
        uri = SW4_new_flow1,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "2",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "6",
            "id": "1",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.11/32",
              "ipv4-destination": "192.168.200.21/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-4-flow-1",
            "priority": "4900"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw4_flow2():
    resp, content = h.request(
        uri = SW4_new_flow2,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "3",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "6",
            "id": "2",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.21/32",
              "ipv4-destination": "192.168.200.11/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-4-flow-2",
            "priority": "9500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw4_flow3():
    resp, content = h.request(
        uri = SW4_new_flow3,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "2",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "6",
            "id": "3",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.7/32",
              "ipv4-destination": "192.168.200.21/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-4-flow-3",
            "priority": "4900"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw4_flow4():
    resp, content = h.request(
        uri = SW4_new_flow4,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "3",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "6",
            "id": "4",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.21/32",
              "ipv4-destination": "192.168.200.7/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-4-flow-4",
            "priority": "9500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def put_sw1_flow1():
    resp, content = h.request(
        uri = SW1_new_flow1,
        method = "PUT",
        body = json.dumps({
          "flow": {
            "instructions": {
              "instruction": {
                "order": "0",
                "apply-actions": {
                  "action": {
                    "order": "0",
                    "output-action": {
                      "output-node-connector": "3",
                      "max-length": "60"
                    }
                  }
                }
              }
            },
            "table_id": "7",
            "id": "7",
            "match": {
              "ethernet-match": {
                "ethernet-type": { "type": "2048" }
              },
              "ipv4-source": "192.168.200.7/32",
              "ipv4-destination": "192.168.200.21/32",
              "ip-match": { "ip-protocol": "1" }
            },
            "hard-timeout": "600",
            "cookie": "0",
            "idle-timeout": "300",
            "flow-name": "switch-1-flow-7",
            "priority": "49500"
          }
        }),
        headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
        )
    return resp, content

def del_sw3_flow1():
    resp, content = h.request(
        uri = SW3_new_flow1,
        method = "DELETE"
        )
    return resp, content

def del_sw3_flow2():
    resp, content = h.request(
        uri = SW3_new_flow2,
        method = "DELETE"
        )
    return resp, content

def del_sw2_flow1():
    resp, content = h.request(
        uri = SW2_new_flow1,
        method = "DELETE"
        )
    return resp, content

def del_sw2_flow2():
    resp, content = h.request(
        uri = SW2_new_flow3,
        method = "DELETE"
        )
    return resp, content

def del_sw2_flow3():
    resp, content = h.request(
        uri = SW2_new_flow3,
        method = "DELETE"
        )
    return resp, content

def del_sw4_flow1():
    resp, content = h.request(
        uri = SW4_new_flow1,
        method = "DELETE"
        )
    return resp, content

def del_sw4_flow2():
    resp, content = h.request(
        uri = SW4_new_flow2,
        method = "DELETE"
        )
    return resp, content

def del_sw4_flow3():
    resp, content = h.request(
        uri = SW4_new_flow3,
        method = "DELETE"
        )
    return resp, content

def del_sw4_flow4():
    resp, content = h.request(
        uri = SW4_new_flow4,
        method = "DELETE"
        )
    return resp, content

def del_sw1_flow1():
    resp, content = h.request(
        uri = SW1_new_flow1,
        method = "DELETE"
        )
    return resp, content

if __name__ == "__main__":

    while True:
        x = get_sw3_port2_info()
        if str(x) == "NO-FWD" :
                print("Sw3 Port-3 is not forwarding")
                print("")
                print("New Flow rules injection in process")
                print("")
                put_sw3_flow5()
                put_sw3_flow6()
                put_sw2_flow5()
                put_sw2_flow6()
                put_sw2_flow7()
                put_sw4_flow1()
                put_sw4_flow2()
                put_sw4_flow3()
                put_sw4_flow4()
                put_sw1_flow1()
                print("New Rules are added")
                while True:
                        y = get_sw3_port2_info()
                        if str(y) == "NO-FWD" :
                                print("Execution with new flow rules")
                                time.sleep(1)
                        else:
                            del_sw3_flow1()
                            del_sw3_flow2()
                            del_sw2_flow1()
                            del_sw2_flow2()
                            del_sw2_flow3()
                            del_sw4_flow1()
                            del_sw4_flow2()
                            del_sw4_flow3()
                            del_sw4_flow4()
                            del_sw1_flow1()
                            print("New flow rules are deleted execution with old flow rules")
                            time.sleep(1)
        else:
                print("Sw3 Port-3 is forwarding")
        time.sleep(1)
