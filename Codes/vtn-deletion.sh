#!/bin/bash

a=`curl --user "admin":"admin" -H "Content-type: application/json" -X GET http://142.150.208.218:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:156638244188750/node-connector/openflow:156638244188750:3`
echo "$a" | awk 'NR==15{print $0}'