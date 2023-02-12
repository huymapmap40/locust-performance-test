from locust import TaskSet, task, HttpUser, between
from westeros_test_scenario_1 import Scenario1
from westeros_test_scenario_2 import Scenario2
from westeros_test_scenario_3 import Scenario3
from westeros_test_scenario_4 import Scenario4
from westeros_test_scenario_5 import Scenario5
from westeros_test_scenario_6 import Scenario6
from westeros_test_scenario_7 import Scenario7
from westeros_test_scenario_8 import Scenario8
from westeros_test_scenario_9 import Scenario9
from westeros_test_scenario_10 import Scenario10
from westeros_test_scenario_11 import Scenario11
from westeros_test_scenario_12 import Scenario12
from westeros_test_scenario_13 import Scenario13
from westeros_test_scenario_14 import Scenario14
from westeros_test_scenario_15 import Scenario15
from westeros_test_scenario_16 import Scenario16
from westeros_test_scenario_17 import Scenario17
from westeros_test_scenario_18 import Scenario18
import westeros_common
class WesterosBehaviour(TaskSet):
    def on_start(self):
        westeros_common.sign_in(self, 'Preparation')

    tasks = {
        Scenario1: 12,
        Scenario2: 2,
        Scenario3: 6,
        Scenario4: 8,
        Scenario5: 4,
        Scenario6: 8,
        Scenario7: 4,
        Scenario8: 8,
        Scenario9: 2,
        Scenario10: 8,
        Scenario11: 8,
        Scenario12: 8,
        Scenario13: 1,
        Scenario14: 1,
        Scenario15: 1,
        Scenario16: 1,
        Scenario17: 6,
        Scenario18: 12
    }



class SimulatedUserAction(HttpUser):
    tasks = [WesterosBehaviour]
    min_wait = 1
    max_wait = 10
