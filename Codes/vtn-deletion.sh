#!/bin/bash

curl --user "admin":"admin" -H "Content-type: application/json" -X POST http://142.150.208.218:8181/restconf/operations/vtn:remove-vtn -d '{"input":{"tenant-name":"vtn1"}}'

