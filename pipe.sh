#!/bin/bash

export id=222
export region=sa-east-1
export cluster=cluster-1
export name=service-1
export alb=alb-1
export dns=dns-2
export destroy=true

python3 deploy_service.py
