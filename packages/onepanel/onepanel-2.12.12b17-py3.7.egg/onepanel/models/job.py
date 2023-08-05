import datetime

from onepanel.models.api_json import APIJSON
from onepanel.utilities.time import parse_date, format_timedelta, utcnow
from onepanel.models.machine_type import MachineType
from onepanel.models.volume_type import VolumeType
from onepanel.models.instance_template import InstanceTemplate
from onepanel.models.dataset_mount_identifier import DatasetMountIdentifier
from onepanel.models.git_source import GitSource


class Job(APIJSON):
    CREATED = "created"
    STARTING = "starting"
    READY = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

    def __init__(self):
        self.uid = None
        self.created_at = None
        self.start_time = None
        self.completion_time = None
        self.active = 0
        self.succeeded = 0
        self.failed = 0
        self.log = None
        self.parent_uid = None
        self.user = None
        self.notes = None
        self.is_legacy = False
        self.dataset_mounts = []
        self.dataset_mount_claims = []
        self.uid = None
        self.command = None
        self.machine_type = MachineType()
        self.volume_type = VolumeType()
        self.instance_template = InstanceTemplate()
        self.git_source = None

    @classmethod
    def from_json(cls, dct):
        job = cls()

        job.uid = dct['uid']
        job.created_at = parse_date(dct['createdAt'])
        job.start_time = parse_date(dct['startTime'])
        job.completion_time = parse_date(dct['completionTime'])
        job.active = dct['active']
        job.succeeded = dct['succeeded']
        job.failed = dct['failed']
        job.log = dct['log']
        job.notes = dct['notes']
        job.is_legacy = dct['isLegacy']
        job.command = dct['command']
        job.machine_type = MachineType.from_json(dct['machineType'])
        job.volume_type = VolumeType.from_json(dct['volumeType'])
        job.instance_template = InstanceTemplate.from_json(dct['instanceTemplate']) 
        job.git_source = GitSource.from_json(dct['gitSource'])

        return job

    @classmethod
    def from_simple_json(cls, dct):
        job = cls()

        job.machine_type.uid = dct['machine']
        job.volume_type.uid = dct['storage']
        job.instance_template.uid = dct['environment']
        job.dataset_mount_claims = [DatasetMountIdentifier.from_simple_json(item) for item in dct['datasets']]
        job.git_source = GitSource.from_string(dct['git'])

        return job

#TODO document
    def simple_view(self):
        info = self.machine_type.info

        item = {
            'uid': self.uid,
            'command': self.command,
            'cpu': info['cpu'],
            'gpu': info['gpu'],
            'ram': info['ram'],
            'hdd': self.volume_type.info['size'],
            'duration_running': format_timedelta(self.duration_running()),
            'age': format_timedelta(self.age()),
            'state': self.state()
        }

        return item

    def state(self):
        if self.failed != 0:
            return Job.FAILED

        if self.succeeded != 0 and self.completion_time is not None:
            return Job.COMPLETED

        if self.start_time is None and self.active == 0:
            return Job.CREATED

        if self.start_time is None and self.active != 0:
            return Job.STARTING

        if self.start_time is not None and self.active != 0:
            return Job.READY

        return Job.STOPPED

    def duration_running(self, when=None):
        """How long the instance has been running for. This is calculated from the time it was
           ready to when."""
        if when is None:
            when = utcnow()

        if self.start_time is None:
            return datetime.timedelta(0)

        return when - self.start_time

    def age(self, when=None):
        """How long the instance has been created to when"""
        if when is None:
            when = utcnow()

        if self.created_at is None:
            return datetime.timedelta(0)

        return when - self.created_at

    def api_json(self):
        json = {
            'command': self.command,
            'uid': self.uid,
            'machineType': self.machine_type,
            'volumeType': self.volume_type,
            'instanceTemplate': self.instance_template,
            'datasetMountClaims': self.dataset_mount_claims,
        }

        if self.git_source is not None:
            json['gitSource'] = self.git_source

        return json

