
https://www.raspberrypi.org/documentation/linux/usage/systemd.md

https://learn.adafruit.com/running-programs-automatically-on-your-tiny-computer/systemd-writing-and-enabling-a-service

```
sudo cp system/services/fcserver.service /etc/systemd/system/fcserver.service
sudo systemctl daemon-reload
sudo systemctl start fcserver.service
sudo systemctl status fcserver.service
sudo systemctl stop fcserver.service
sudo systemctl enable fcserver.service
sudo systemctl status fcserver.service
sudo systemctl restart fcserver.service
sudo systemctl status fcserver.service
```
