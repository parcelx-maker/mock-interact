#!/usr/bin/env bash
./build_docker.sh
docker tag parcelx/sp_mock:latest reg.int.parcelfuture.com/parcelx/sp-mock:latest
docker push reg.int.parcelfuture.com/parcelx/sp-mock:latest