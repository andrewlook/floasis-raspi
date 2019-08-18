#!/bin/bash

sudo cp system/services/fcserver.service /etc/systemd/system/fcserver.service
sudo cp system/services/anim.service /etc/systemd/system/anim.service
sudo cp system/services/anim_test.service /etc/systemd/system/anim_test.service
sudo cp system/services/anim_all.service /etc/systemd/system/anim_all.service

sudo systemctl enable fcserver.service
sudo systemctl disable anim.service
sudo systemctl disable anim_test.service
sudo systemctl enable anim_all.service

sudo systemctl restart fcserver.service
sudo systemctl stop anim.service
sudo systemctl stop anim_test.service
sudo systemctl restart anim_all.service

sudo systemctl status fcserver.service
sudo systemctl status anim.service
sudo systemctl status anim_test.service
sudo systemctl status anim_all.service
