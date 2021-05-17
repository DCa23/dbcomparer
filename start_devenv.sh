#!/usr/bin/env bash

cd dockerdb1
bin/start >> dockerenv.log 2>&1 &

cd ../dockerdb2
bin/start >> dockerenv.log 2>&1 &

echo "Data base containers started"