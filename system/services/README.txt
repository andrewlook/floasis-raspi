
https://www.raspberrypi.org/documentation/linux/usage/systemd.md

https://learn.adafruit.com/running-programs-automatically-on-your-tiny-computer/systemd-writing-and-enabling-a-service

```
sudo cp system/services/fcserver.service /etc/systemd/system/fcserver.service
sudo cp system/services/anim.service /etc/systemd/system/anim.service
sudo cp system/services/anim_test.service /etc/systemd/system/anim_test.service
sudo cp system/services/anim_all.service /etc/systemd/system/anim_all.service

sudo systemctl enable fcserver.service
sudo systemctl enable anim.service
sudo systemctl enable anim_test.service
sudo systemctl enable anim_test.service

sudo systemctl restart fcserver.service
sudo systemctl restart anim.service
sudo systemctl restart anim_test.service
sudo systemctl restart anim_all.service

sudo systemctl status fcserver.service
sudo systemctl status anim.service
sudo systemctl status anim_test.service
sudo systemctl status anim_all.service


sudo systemctl daemon-reload
sudo systemctl start fcserver.service
sudo systemctl status fcserver.service
sudo systemctl stop fcserver.service
sudo systemctl enable fcserver.service
sudo systemctl status fcserver.service
sudo systemctl restart fcserver.service
sudo systemctl status fcserver.service
```
