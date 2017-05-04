#!/bin/bash

echo "{\"remote_addr\": \"${remote_addr}\", \"request_addr\": \"${request_addr}\", \"request_uri\": \"${request_uri}\" }" > /hmmweb_rule/requests
curl -XPOST -H "Content-Type: application/json" -d @/hmmweb_rule/requests http://192.168.38.1:8000/requests/
echo Done.