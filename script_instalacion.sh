#!/bin/bash
sudo sudo pip3 install virtualenv
virtualenv venvautoyaproto -p python3
source venvautoyaproto/bin/activate
pip3 install -r requirements.txt
