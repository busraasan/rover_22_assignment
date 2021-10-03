#include <stdlib.h>
#include <ros/ros.h>
#include "std_msgs/String.h"

/* 
    Author: Basan
    Date: 2021-10-02
*/

class encoderListener{
    ros::NodeHandle nh;

    ros::Subscriber drive_sub = nh.subscribe("/serial/drive",10,&encoderListener::driveCallback, this);
    ros::Subscriber arm_sub = nh.subscribe("/serial/robotic_arm",10,&encoderListener::rkCallback, this);

    ros::Publisher drive_pub = nh.advertise<std_msgs::String>("/position/drive",10);
    ros::Publisher arm_pub = nh.advertise<std_msgs::String>("/position/robotic_arm",10);

    void driveCallback(const std_msgs::String &data);
    void rkCallback(const std_msgs::String &data);
public:
    encoderListener();
};

encoderListener::encoderListener(){
    ros::spin();
}

void encoderListener::driveCallback(const std_msgs::String &msg){
    int len = msg.data.length();
    std_msgs::String drive_data;
    if(msg.data[0] == 'A' && msg.data[len-1] == 'B'){
        for(int i = 1; i < len-2; i+=4){
            std::string data = msg.data.substr(i,4);
            if(data[0] == '0'){
                drive_data.data.append("+");
            } else {
                drive_data.data.append("-");
            }
            if(std::stoi(data.substr(1,3)) >= 255){
                data.substr(1,3) = '255';
            }
            drive_data.data = drive_data.data + data.substr(1,3) + " ";
        }
        drive_pub.publish(drive_data);
    }
}

void encoderListener::rkCallback(const std_msgs::String &msg){
    int len = msg.data.length();
    std_msgs::String arm_data;
    if(msg.data[0] == 'A' && msg.data[len-1] == 'B'){
        for(int i = 1; i < len-2; i+=4){
            std::string data = msg.data.substr(i,4);
            if(data[0] == '0'){
                arm_data.data.append("+");
            } else {
                arm_data.data.append("-");
            }
            if(std::stoi(data.substr(1,3)) >= 255){
                data.substr(1,3) = '255';
            }
            arm_data.data = arm_data.data + data.substr(1,3) + " ";
        }
        this->arm_pub.publish(arm_data);
    }  
}

int main(int argc, char **argv){
    ros::init(argc, argv, "encoderListener");
    encoderListener();
    return 0;
}
