from flask import Flask, request
from pathlib import Path
from time import sleep

app = Flask(__name__)
all_objects = dict()

"""
Class MountPoint that contains following fields:
Mount point name - string - Example: “c:\”
Total size of the volume - int
"""


class MountPoint:
    def __init__(self, mount_path: str, v_size: int):
        self.mount_path = Path(mount_path)
        if self.mount_path.root == '':
            raise ValueError('Incorrect path input')
        self.v_size = v_size

    def run(self):
        print(self.mount_path)


"""
Class Credentials that contains the following fields
Username - string
Password - string
Domain - string
"""


class Credentials:
    def __init__(self, username: str, password: str, domain: str):
        self.username = username
        self.password = password
        self.domain = domain


"""
Class Workload that contains following fields:
IP string, credentials of type Credentials
Storage that contains list of instances of type MountPoint
"""


class Workload:
    def __init__(self, ip: str, credentials: Credentials, storage: list):
        self.ip = ip
        self.credentials = credentials
        if all([isinstance(i, MountPoint) for i in storage]):
            self.storage = storage
        else:
            raise ValueError('Storage list should contain only MountPoint types')


"""
Add following business constraints to class Source:
Username, password, IP should not be None
IP cannot change for the specific source
"""


class Source:
    def __init__(self, username: str, password: str, ip: str):
        if username is None:
            raise ValueError('username can not b None')
        else:
            self.username = username
        if password is None:
            raise ValueError('username can not b None')
        else:
            self.password = password
        if ip is None:
            raise ValueError('username can not b None')
        else:
            self.__ip = ip

    def set_ip(self, ip):
        if self.__ip != "111.222.333.444":
            self.__ip = ip
        else:
            raise RuntimeError(f'ip can not be changed: {self.__ip}')

    def get_ip(self):
        return self.__ip


"""
Class MigrationTarget that contains following fields:
Cloud type: aws, azure, vsphere, vcloud - no other values are allowed
Cloud Credentials of type Credentials
Target Vm object of type Workload
"""


class MigrationTarget:
    def __init__(self, cloud_type: str, credentials: Credentials, vm: Workload):
        possible_types = {'aws', 'azure', 'vsphere', 'vcloud'}
        if cloud_type is not None and cloud_type in possible_types:
            self.type = cloud_type
        else:
            raise ValueError(f'Possible type values: {possible_types}')
        self.credentials = credentials
        self.vm = vm


"""
Define class Migration that contains the following
Selected Mount points: list of MountPoint
Source of type Workload
Migration Target of type MigrationTarget
Migration state: not started, running, error, success
Implement run() method - run method should sleep for X min (simulate running migration)
copy source object to the Migration Target.
"""


class Migration:
    def __init__(self, mount_points: list, source: Workload, target: MigrationTarget):
        if all([isinstance(i, MountPoint) for i in mount_points]):
            self.mount_points = mount_points
        self.source = source
        self.target = target
        self.__state = 'not started'

    def set_state(self, state: str):
        allowed_states = {'not started', 'running', 'error', 'success'}
        if state not in allowed_states:
            raise ValueError(f'Possible type values: {allowed_states}')
        else:
            self.__state = state

    def run(self):
        self.set_state('running')
        for source_point in self.source.storage:
            # Target VM and target should only have mount points that are selected.
            # For example, if source has: C:\ D: and E:\ and only C: was selected,
            # target should only have C:\
            if source_point in self.target.vm.storage:
                # Implement business logic to not allow running migrations
                # when volume C:\ is not allowed ???????
                if len([f for f in source_point.mount_path.glob('*')]) == 0:
                    self.set_state('error')
                sleep(600)
        self.set_state('success')


@app.route('/Workload')
def workload_handler():
    if request.args.get('action') == 'add':

    elif request.args.get('action') == 'del':

    return 'Hello World!'


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
