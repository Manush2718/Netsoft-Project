#!/bin/bash
while true
do
	a=`curl --user "admin":"admin" -H "Content-type: application/json" -X GET http://142.150.208.218:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:156638244188750/node-connector/openflow:156638244188750:3`
	echo "$a" | grep -o NO-FWD
	b=`echo "$a" | grep -o NO-FWD`

	if [ "$b" == "NO-FWD" ]; then
		echo "VTN is established"
		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn:update-vtn -d '{"input":{"tenant-name":"vtn1"}}'

		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vbridge:update-vbridge -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1"}}'

		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vinterface:update-vinterface -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if1"}}'

		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-vinterface:update-vinterface -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if2"}}'

		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-port-map:set-port-map -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if1", "node":"openflow:196663245581123", "port-name":"sw2-vxlan1"}}'

		curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn-port-map:set-port-map -d '{"input":{"tenant-name":"vtn1", "bridge-name":"vbr1", "interface-name":"if2", "node":"openflow:156638244188750", "port-name":"sw1-vxlan2"}}'
	else
		echo "Switch 1 is forwarding"
	fi
	sleep 1s
done 	
