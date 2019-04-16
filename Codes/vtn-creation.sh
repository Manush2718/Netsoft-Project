#!/bin/bash

#VTN 1 creation between H1 and H2
curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn:update-vtn -d '{"input":{"tenant-name":"vtn1"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vbridge:update-vbridge -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vinterface:update-vinterface -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if1"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vinterface:update-vinterface -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if2"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vinterface:update-vinterface -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if3"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-port-map:set-port-map -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if1", "node":"openflow:200951389990216", "port-name":"sw1-vxlan1"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-port-map:set-port-map -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if2", "node":"openflow:217996154732608", "port-name":"sw2-vxlan2"}}'

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-port-map:set-port-map -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if3", "node":"openflow:20480847422025", "port-name":"sw3-vxlan2"}}'


