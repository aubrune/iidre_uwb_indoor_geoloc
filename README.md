# iidre_uwb_indoor_geoloc
ROS 1 package for Indoor geolocalisation with Ultra wideband (UWB) anchors from IIDRE

## Quickstart

### Part A: Place anchors and create the map
1. Connect an UWB sensor to an USB port of your ROS computer
2. Power up at least 4 UWB anchors through MicroUSB and place them at the edges of a room (make it easy to measure distances between them)
3. Build & launch uwbsupervisor, you should see realtime distance data from the 4 anchors and an incorrect map of them 
4. Click `Impart infra (flash)` and save the infra file with the `.json` extension
5. Manually open the previous infra JSON file, decide of a world frame in the room and measure distances between anchors to update `X, Y, Z` positions of anchors (in millimeters)
6. Click `Export infra (flash)`, select the edited infra JSON file, and wait a few dozens of seconds for the modal message "export positions: 4"
7. In the UWB Supervisor, check that the top view of the map looks correct, in temrs of achors (black points) and sensor (red point)

### Part B: Publish to ROS


## Build notepad for Ubuntu
### Error `Unknown module(s) in QT: serialport`
```
sudo apt install libqt5serialport5-dev
```

### module "QtCharts" is not installed
```
sudo apt install qml-module-qtcharts qml-module-qtquick-dialogs
sudo apt install qml-module-qt-labs-settings qml-module-qt-labs-folderlistmodel
```
