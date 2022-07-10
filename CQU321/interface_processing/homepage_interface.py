import os
import datetime
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.SqlProcessor import SqlProcessor
from CQU321.utils.tools import *
from Website.settings import MEDIA_ROOT, BASE_DIR
from CQUWebsite.utils import announcement_path, announcement_default_name, cover_path

__all__ = ['homepage_process']

ADS_PATH = MEDIA_ROOT / 'homepage'


def _get_last_update() -> str:
    config = ConfigParser()
    config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')
    return config.get('Advertise_Setting', 'last_update_date')


def _set_last_update(date: str):
    config = ConfigParser()
    config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')
    config.set('Advertise_Setting', 'last_update_date', date)
    with open(str(BASE_DIR) + '/CQU321/321CQU_Config.ini', 'w') as f:
        config.write(f)


def _homepage_v_1_0() -> Dict:
    file_urls_list = []
    filenames = os.listdir(path=ADS_PATH)
    filenames.sort()
    for filename in filenames:
        if os.path.isfile(ADS_PATH / filename) and filename[0] != '_':
            file_url = '/media/homepage/' + filename
            file_urls_list.append(file_url)

    return {
        'PictureUrls': file_urls_list,
    }


def _launch_file_dict(ads_path, ads_filename):
    file = {
        'Url': '',
        'ContentUrl': None,
        'JumpType': None,
    }
    for filename in os.listdir(path=ads_path / ads_filename):
        suffix = os.path.splitext(filename)[1]
        if suffix == '.md':
            file['ContentUrl'] = '/media/homepage/' + ads_filename + '/' + filename
            file['JumpType'] = 'md'
        elif suffix == '.mk':
            file['ContentUrl'] = filename
            file['JumpType'] = 'mk'
        else:
            file['Url'] = '/media/homepage/' + ads_filename + '/' + filename

    return file


def _homepage_v_2_0():
    files = []
    ads_filenames = os.listdir(path=ADS_PATH)
    ads_filenames.sort()
    for ads_filename in ads_filenames:
        if os.path.isdir(ADS_PATH / ads_filename) and ads_filename[0] != '_':
            file = _launch_file_dict(ADS_PATH, ads_filename)
            files.append(file)

    return {
        'Pictures': files
    }


def _parse_timestamp_to_date(timestamp):
    # local_time = time.localtime(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)


def check_file_change(file_path):
    last_update = _get_last_update()
    modify_timestamp = os.path.getmtime(file_path)
    modify_date = _parse_timestamp_to_date(modify_timestamp)

    if modify_date > datetime.datetime.strptime(last_update, '%Y-%m-%d'):
        modify_time_str = modify_date.strftime('%Y-%m-%d')
        _set_last_update(modify_time_str)
        last_update = modify_time_str

    return last_update


def _launch_recommend_path(aid: int):
    return announcement_path + str(aid) + announcement_default_name


def _homepage_v_2_1():
    files = []
    local_files = []
    ads_filenames = os.listdir(path=ADS_PATH)
    ads_filenames.sort()
    for ads_filename in ads_filenames:
        if os.path.isdir(ADS_PATH / ads_filename) and ads_filename[0] != '_':
            check_file_change(ADS_PATH / ads_filename)
            file = _launch_file_dict(ADS_PATH, ads_filename)
            if ads_filename[0] == 'x':
                files.append(file)
            else:
                local_files.append({'index': int(ads_filename[0]), 'file': file})

    process = SqlProcessor()
    now_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    process.execute("select Aid, ImgPath, StartDate from RecommendApply where State = 1 and Position = 0 "
                    "and %s between StartDate and EndDate", now_date_str)
    res = process.fetchall()
    for apply in res:
        if str(apply[2]) == now_date_str:
            _set_last_update(now_date_str)
        files.insert(0, {
            'Url': cover_path + apply[1],
            'ContentUrl': _launch_recommend_path(apply[0]),
            'JumpType': 'md'
        })

    local_files.sort(key=lambda x: x['index'], reverse=True)
    while len(local_files) > 0:
        temp = local_files.pop()
        files.insert(temp['index'], temp['file'])

    return {
        'Pictures': files,
    }


@process_exception
def homepage_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': _homepage_v_1_0,
        '2.0': _homepage_v_2_0,
        '2.1': _homepage_v_2_1,
    }, params)

    result = func()

    result.update({
        'LastUpdate': _get_last_update(),
        'Version': params.pop('Version')
    })

    return result




