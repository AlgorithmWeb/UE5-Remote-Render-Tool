import logging

from util import Client


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def send(d):
    rrequest = Client.add_request(d)
    if rrequest:
        LOGGER.info('request %s sent to server', rrequest.uuid)


if __name__ == '__main__':
    test_job_a = {
        'name': 'fullRenderShot3',
        'owner': 'VitorVicente',
        'project_path': r'D:\Projects\DingleStorageProject\DingleStorageProject.uproject',
        'level_path': '/Game/Level/Levels/DG_SHOT03.DG_SHOT03',
        'sequence_path': '/Game/Level/Level_Sequences/DG_SHOT_03_SEQ.DG_SHOT_03_SEQ',
        'config_path': '/Game/Camera_Rig/Render_Presets/FinalRenderSettingsFull4-8.FinalRenderSettingsFull4-8'
    }

    for job in [test_job_a]:
        send(job)
