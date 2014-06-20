#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import psutil
import netifaces as ni

class OS_Info(object):
    """操作系统相关信息
    """
    def __init__(self):
        """
        """
        pass
    def get_cpu(self):
        """
        """
        # CPU
        cpu = dict(zip(("user","nice","system","idle","iowait","irq","softirq","steal","guest"), psutil.cpu_times_percent(interval=2,percpu=False)))
        return cpu
    def get_memory(self):
        # 内存
        memory = dict(zip(("total","available","percent","used","free","active","inactive","buffers","cached"), psutil.virtual_memory()))
        swap = dict(zip(("total","used","free","percent","sin","sout"), psutil.swap_memory()))
        return memory, swap
    def get_net(self):
        # 网络流量
        nw = ni.gateways()['default'][2][1]
        current_bytes = psutil.net_io_counters(pernic=True)[nw][1]
        time.sleep(60)
        previous, current_bytes = current_bytes, psutil.net_io_counters(pernic=True)[nw][1]
        # 网络连接数
        connections = len(psutil.net_connections())
        return connections
    def __del__(self):
        """
        """

def main():
    """
    """
    os_info = OS_Info()
    print os_info.get_cpu()
    print os_info.get_memory()
    print os_info.get_net()

if __name__ == "__main__":
    main()
