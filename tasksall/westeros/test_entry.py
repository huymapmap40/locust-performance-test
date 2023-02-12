from locust import HttpUser, TaskSet, task, tag
import common
from test_scenario_1 import Scenario1
from test_scenario_2 import Scenario2
from test_scenario_3 import Scenario3
from test_scenario_4 import Scenario4
from test_scenario_5 import Scenario5
from test_scenario_6 import Scenario6
from test_scenario_7 import Scenario7
from test_scenario_8 import Scenario8
from test_scenario_9 import Scenario9
from test_scenario_10 import Scenario10
from test_scenario_11 import Scenario11
from test_scenario_12 import Scenario12
from test_scenario_13 import Scenario13
from test_scenario_14 import Scenario14
from test_scenario_15 import Scenario15
from test_scenario_16 import Scenario16
from test_scenario_17 import Scenario17
from test_scenario_18 import Scenario18


class WesterosBehaviour(TaskSet):
    def on_start(self):
        common.sign_in(self, 'Preparation')

    # Open homepage
    @task(12)
    def scenario1(self):
        Scenario1(self).task1()

    # Open homepage and click on "view more popular stores" (/all-stores)
    @task(2)
    def scenario2(self):
        Scenario2(self).task2()

    # Open homepage and click on a deal -> redirect to merchant site (/redirect/alink/)
    @task(6)
    def scenario3(self):
        Scenario3(self).task3()

    # Open campaign page (/CAMPAIGN_SLUG)
    @task(8)
    def scenario4(self):
        Scenario4(self).task4()

    # Open campaign page and click on a merchant -> merchant page (/MERCHANT_SHORTNAME)
    @task(4)
    def scenario5(self):
        Scenario5(self).task5()

    # Open campaign page and click on a deal -> redirect to merchant site (/redirect/alink/)
    @task(8)
    def scenario6(self):
        Scenario6(self).task6()

    # Open campaign page and click on a store -> merchant page (/MERCHANT_SHORTNAME)
    @task(4)
    def scenario7(self):
        Scenario7(self).task7()

    # Open campaign page and click on a coupon -> redirect to merchant site (/redirect/alink/)
    @task(8)
    def scenario8(self):
        Scenario8(self).task8()

    # Open merchant page (/MERCHANT_SHORTNAME)
    @task(2)
    def scenario9(self):
        Scenario9(self).task9()

    # Open merchant page and click on shop now button -> redirect to merchant site (/redirect/alink/)
    @task(8)
    def scenario10(self):
        Scenario10(self).task10()

    # Open merchant page and click on a deal -> redirect to merchant site (/redirect/alink/)
    @task(8)
    def scenario11(self):
        Scenario11(self).task11()

    # Open merchant page and click on a coupon -> redirect to merchant site (/redirect/alink/)
    @task(8)
    def scenario12(self):
        Scenario12(self).task12()

    # Open homepage and search a product
    @task(1)
    def scenario13(self):
        Scenario13(self).task13()

    # Open homepage and search a store
    @task(1)
    def scenario14(self):
        Scenario14(self).task14()

    # Open homepage and click on a product category
    @task(1)
    def scenario15(self):
        Scenario15(self).task15()

    # Open homepage and search a product and compare products
    @task(1)
    def scenario16(self):
        Scenario16(self).task16()

    # Open cashback overview and click on "Click Activity" tab
    @task(6)
    def scenario17(self):
        Scenario17(self).task17()

    # Open homepage without cache
    @task(12)
    def scenario18(self):
        Scenario18(self).task1()


class SimulatedUserAction(HttpUser):
    tasks = [WesterosBehaviour]
    min_wait = 1
    max_wait = 10
