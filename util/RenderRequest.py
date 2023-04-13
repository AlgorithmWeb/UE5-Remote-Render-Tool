import os
from datetime import datetime, timedelta
import socket

from dotenv import load_dotenv

from util.StorableEntity import StorableEntity

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../.env'))

DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER"))


class RenderStatus(object):
    unassigned = 'Un-Assigned'
    ready_to_start = 'Ready to Start'
    in_progress = 'In Progress'
    finished = 'Finished'
    errored = 'Errored'
    cancelled = 'Cancelled'
    paused = 'Paused'


class RenderRequest(StorableEntity):
    DATABASE = DATABASE

    def __init__(
            self,
            uuid='',
            name='',
            owner='',
            worker='',
            time_created='',
            priority=0,
            category='',
            tags=None,
            status='',
            project_path='',
            level_path='',
            sequence_path='',
            config_path='',
            output_path='',
            width=0,
            height=0,
            frame_rate=0,
            format='',
            start_frame=0,
            end_frame=0,
            time_estimate='',
            estimated_finish='',
            progress=0
    ):
        super().__init__(uuid)
        self.name = name
        self.owner = owner or socket.gethostname()
        self.worker = worker
        self.time_created = time_created or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.priority = priority or 0
        self.category = category
        self.tags = [] if tags is None else tags
        self.status = status or RenderStatus.unassigned
        self.project_path = project_path
        self.level_path = level_path
        self.sequence_path = sequence_path
        self.config_path = config_path
        self.output_path = output_path
        self.width = width or 1280
        self.height = height or 720
        self.frame_rate = frame_rate or 30
        self.format = format or 'JPG'
        self.start_frame = start_frame or 0
        self.end_frame = end_frame or 0
        self.length = self.end_frame - self.start_frame
        self.time_estimate = time_estimate
        self.progress = progress
        self.estimated_finish = estimated_finish or ''
        self.calcFinish(estimated_finish)

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        name = data.get('name') or ''
        owner = data.get('owner') or ''
        worker = data.get('worker') or ''
        time_created = data.get('time_created') or ''
        priority = data.get('priority') or 0
        category = data.get('category') or ''
        tags = data.get('tags') or []
        status = data.get('status') or ''
        project_path = data.get('project_path')
        level_path = data.get('level_path') or ''
        sequence_path = data.get('sequence_path') or ''
        config_path = data.get('config_path') or ''
        output_path = data.get('output_path') or ''
        width = data.get('width') or 0
        height = data.get('height') or 0
        frame_rate = data.get('frame_rate') or 0
        format = data.get('format') or ''
        start_frame = data.get('start_frame') or 0
        end_frame = data.get('end_frame') or 0
        time_estimate = data.get('time_estimate') or ''
        estimated_finish = data.get('estimated_finish') or ''
        progress = data.get('progress') or 0

        return cls(
            uuid=uuid,
            name=name,
            owner=owner,
            worker=worker,
            time_created=time_created,
            priority=priority,
            category=category,
            tags=tags,
            status=status,
            project_path=project_path,
            level_path=level_path,
            sequence_path=sequence_path,
            config_path=config_path,
            output_path=output_path,
            width=width,
            height=height,
            frame_rate=frame_rate,
            format=format,
            start_frame=start_frame,
            end_frame=end_frame,
            time_estimate=time_estimate,
            estimated_finish=estimated_finish,
            progress=progress
        )

    def assign(self, worker):
        self.worker = worker

        self.__class__.write_db(self.__dict__)

    def calcFinish(self, defaultVal, ignoreDefault=False):
        if self.time_estimate == 'N/A':
            self.estimated_finish = 'N/A'
            return

        if self.time_estimate != '':
            start = datetime.now()
            end = datetime.strptime(self.time_estimate, '%Hh:%Mm:%Ss')
            delta = timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
            self.estimated_finish = ((not ignoreDefault) and defaultVal) or (
                (start + delta).strftime("%m/%d/%Y, %H:%M:%S"))
        else:
            self.estimated_finish = ((not ignoreDefault) and defaultVal) or ''
