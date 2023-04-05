import logging
import os
import json
from dotenv import load_dotenv

from util.RenderRequest import RenderRequest

LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../.env'))

DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))


class HardwareStats(object):
    def __init__(
            self,
            name='',
            cpu='',
            gpu='',
            ram='',
            vram=''
    ):
        self.name = name
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.vram = vram

    @classmethod
    def from_dict(cls, data):
        name = (data.get('name') or '') if data else ''
        cpu = (data.get('cpu') or '') if data else ''
        gpu = (data.get('gpu') or '') if data else ''
        ram = (data.get('ram') or '') if data else ''
        vram = (data.get('vram') or '') if data else ''

        return cls(
            name=name,
            cpu=cpu,
            gpu=gpu,
            ram=ram,
            vram=vram
        )

    def to_dict(self):
        return self.__dict__


class RenderArchive(object):
    def __init__(
            self,
            uuid='',
            project_name='',
            render_request=None,
            hardware_stats=None,
            total_time='',
            finish_time='',
            avg_frame=0,
            frame_map=None,
            per_frame_samples=0,
            resolution=''
    ):
        if not frame_map:
            frame_map = []

        self.uuid = uuid or render_request.uuid
        self.project_name = project_name
        self.render_request = render_request
        self.hardware_stats = hardware_stats
        self.total_time = total_time
        self.finish_time = finish_time
        self.avg_frame = avg_frame
        self.frame_map = frame_map
        self.per_frame_samples = per_frame_samples
        self.resolution = resolution

    @classmethod
    def from_db(cls, uuid):
        request_file = os.path.join(DATABASE, '{}.json'.format(uuid))
        with open(request_file, 'r') as fp:
            try:
                request_dict = json.load(fp)
            except Exception as e:
                LOGGER.error('Failed to load request object from db: %s', e)
                return None
        return cls.from_dict(request_dict)

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        project_name = data.get('project_name') or ''
        total_time = data.get('total_time') or ''
        finish_time = data.get('finish_time') or ''
        avg_frame = data.get('avg_frame') or ''
        frame_map = data.get('frame_map') or ''
        per_frame_samples = data.get('per_frame_samples') or ''
        resolution = data.get('resolution') or ''

        render_request = RenderRequest.from_dict(data.get('render_request'))
        hardware_stats = HardwareStats.from_dict(data.get('hardware_stats'))

        return cls(
            uuid=uuid,
            project_name=project_name,
            render_request=render_request,
            hardware_stats=hardware_stats,
            total_time=total_time,
            finish_time=finish_time,
            avg_frame=avg_frame,
            frame_map=frame_map,
            per_frame_samples=per_frame_samples,
            resolution=resolution
        )

    def copy(self):
        return RenderArchive(
            uuid=self.uuid,
            project_name=self.project_name,
            render_request=self.render_request,
            hardware_stats=self.hardware_stats,
            total_time=self.total_time,
            finish_time=self.finish_time,
            avg_frame=self.avg_frame,
            frame_map=self.frame_map,
            per_frame_samples=self.per_frame_samples,
            resolution=self.resolution
        )

    def to_dict(self):
        copy = self.copy()
        if self.render_request:
            copy.render_request = self.render_request.to_dict()
        if self.hardware_stats:
            copy.hardware_stats = self.hardware_stats.to_dict()
        return copy.__dict__

    def write_json(self):
        write_db(self.to_dict())

    def remove(self):
        remove_db(self.uuid)


def read_all():
    reqs = list()
    files = os.listdir(DATABASE)
    uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
    for uuid in uuids:
        req = RenderArchive.from_db(uuid)
        reqs.append(req)

    return reqs


def remove_db(uuid):
    os.remove(os.path.join(DATABASE, '{}.json'.format(uuid)))


def remove_all():
    files = os.path.join(DATABASE, '*.json')
    for file in files:
        os.remove(file)


def write_db(d):
    uuid = d['uuid']
    LOGGER.info('writing to %s', uuid)
    with open(os.path.join(DATABASE, '{}.json'.format(uuid)), 'w') as fp:
        json.dump(d, fp, indent=4)