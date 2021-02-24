# rescue_quadrotor

## Install hector quadrotor
```
wstool init src https://raw.github.com/tu-darmstadt-ros-pkg/hector_quadrotor/kinetic-devel/tutorials.rosinstall
```

## and Dependencies
```
sudo apt-get install ros-melodic-geographic-info

sudo apt-get install ros-melodic-ros-control

sudo apt-get install ros-melodic-gazebo-ros-control

sudo apt-get install ros-melodic-joy

sudo apt-get install ros-melodic-teleop-twist-keyboard

```

Install hector_localization

To **enable motors**


	rosservice call /enable_motors "enable: true"
