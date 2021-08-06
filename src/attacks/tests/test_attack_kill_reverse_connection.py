# Copyright 2016, 2017, 2018, 2019 Fraunhofer FKIE
#
# This file is part of BREACH.
#
# BREACH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BREACH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BREACH. If not, see <http://www.gnu.org/licenses/>.


from unittest.mock import Mock

import pytest

from attacks import AttackException
from attacks.attack_kill_reverse_connection import KillReverseConnectionAttack


@pytest.fixture()
def attack():
    KillReverseConnectionAttack.ssh_client_class = Mock
    attack = KillReverseConnectionAttack()
    attack.ssh_client.exec_command = Mock(return_value=(Mock(), [], []))
    return attack


class TestKillReverseConnectionAttack():
    def test_info(self):
        assert KillReverseConnectionAttack.info.name == "disinfect_client"

    def test_raise_exception_bad_output(self, attack: KillReverseConnectionAttack):
        attack.exec_commands_on_target = lambda _: attack.printer.print("Failure.")
        with pytest.raises(AttackException):
            attack.run()

    def test_no_exception_good_output(self, attack: KillReverseConnectionAttack):
        indicator = "Successful wmic execution"
        attack.exec_commands_on_target = lambda _: attack.printer.print(indicator)
        attack.run()
