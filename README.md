# Arknights Remote Control
## Background
Arknights Bilibili Server can only run on android devices. This project tries to control a Android simulator running on a personal PC through webpages. Based on the initial plan, this project consists of three components: local simulator controller, web server and web client (browser)

## Local Controller
See [LocalPC](localPC/)  
This part uses adb to control the Android simulator. Processes remote commands from the client. 