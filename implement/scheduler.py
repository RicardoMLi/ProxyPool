import time

from multiprocessing import Process
from .settings import TESTER_CYCLE, GETTER_CYCLE
from .tester import Tester
from .getter import Getter


class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def run(self):
        print('代理池正在运行....')

        tester_process = Process(target=self.schedule_tester)
        tester_process.start()

        getter_process = Process(target=self.schedule_getter)
        getter_process.start()
