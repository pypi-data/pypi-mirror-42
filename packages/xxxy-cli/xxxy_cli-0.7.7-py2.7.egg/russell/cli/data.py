# coding: utf-8
import json
import traceback

import click
import webbrowser

import requests
from tabulate import tabulate
import sys
import os
import shutil
import russell
from russell.cli.utils import (
    get_file_count,
    get_size,
    sizeof_fmt,
    get_files_in_current_directory
)
from russell.client.base import RussellHttpClient
from russell.client.data import DataClient
from russell.client.files import FsClient, SOCKET_STATE
from russell.client.module import ModuleClient
from russell.config import generate_uuid
from russell.manager.auth_config import AuthConfigManager
from russell.manager.data_config import DataModuleConfig, DataConfigManager
from russell.manager.russell_ignore import RussellIgnoreManager
from russell.model.module import *
from russell.log import logger as russell_logger, configure_logger
from russell.cli.utils import (get_task_url, get_module_task_instance_id,
                               get_mode_parameter, wait_for_url, force_unicode,
                               get_files_in_directory, save_dir, copy_files)


@click.group()
def data():
    """
    Subcommand for data operations
    """
    pass


@click.command()
@click.option('--id',
              help='Remote dataset id to init')
@click.option('--name',
              help='Remote dataset name to init')
# @click.argument('name', nargs=1)
def init(id, name):
    """
    Initialize a new data upload.
    After init ensure that your data files are in this directory.
    Then you can upload them to Russell. Example:

        russell data upload
    """
    if not id and not name:
        russell_logger.error("Neither id or name offered")
        return
    RussellIgnoreManager.init()
    data_info = {}
    try:
        dc = DataClient()
    except Exception as e:
        russell_logger.error(e.message)
        return

    access_token = AuthConfigManager.get_access_token()
    try:
        if id:
            data_info = dc.get_data_info_by_id(id=id)
        elif name:
            data_info = dc.get_data_info_by_name(access_token.username, name)
    except Exception as e:
        russell_logger.error(e.message)
        return

    name = data_info.get('name')
    data_id = data_info.get('id')
    latest_version = data_info.get('latest_version')  # mostly as 0 on remote
    data_config = DataModuleConfig(name=name,
                                   dataset_id=data_id,
                                   version=latest_version,
                                   family_id=generate_uuid())
    DataConfigManager.set_config(data_config)
    russell_logger.info("Data source \"{}\" initialized in current directory".format(name))
    russell_logger.info("""
    You can now upload your data to Russell by:
        russell data upload
    """)


@click.command()
def _upload():
    """
    Deprecated: Upload data in the current dir to Russell.
    """
    data_config = DataConfigManager.get_config()
    access_token = AuthConfigManager.get_access_token()
    version = data_config.version + 1

    # Create data object
    data_name = "{}/{}:{}".format(access_token.username,
                                  data_config.name,
                                  version)
    data = ModuleRequest(name=data_config.name,
                         description=version,
                         version=version,
                         entity_id=data_config.dataset_id,
                         module_type="data")
    data_id = DataClient()._create(data)
    russell_logger.debug("Created data with id : {}".format(data_id))
    russell_logger.info("Upload finished")

    # Update expt config including predecessor
    data_config.increment_version()
    data_config.set_data_predecessor(data_id)
    DataConfigManager.set_config(data_config)

    # Print output
    table_output = [["DATA ID", "NAME", "VERSION"],
                    [data_id, data_name.encode("utf-8"), version]]
    russell_logger.info(tabulate(table_output, headers="firstrow"))


def check_compress(file, is_zip=False, is_compress=True):
    file_type = file.split('.')[-1]
    if file_type == 'zip':
        is_zip = True
    elif file_type == 'tar':
        is_compress = False
    elif file[-6:] == 'tar.gz':
        is_compress = True
    else:
        russell_logger.error("File type not support")
        sys.exit()
    return is_zip, is_compress


@click.command()
@click.option('--remote',
              default=False,
              help='Remote dataset upload status')
@click.option('--message', '-m',
              help='Message to commit',
              type=click.STRING,
              default="")
@click.option('--nopack',
              is_flag=True,
              help="only tar dataset, not compress it")
# @click.option('--is_increment', "-i",
#               default=True,
#               is_flag=True,
#               help="Use increment upload")
@click.option('--file', '-cf',
              help='Upload single packaged file(zip/tar/tar.gz)',
              type=click.STRING,
              default="")
# @click.option('-r', '--resume',
#               is_flag=True, default=False, help='Resume previous upload')
# @click.option('--hdf5',
#               is_flag=True,
#               help="transfer file to hdf5 format.")
# @click.option('--bit',
#               is_flag=True,
#               help="transfer file to binary format.")
# @click.option('--chunksize',
#               default='2G',
#               help="default to 2GB, require >= 100MB")
@click.pass_context
def upload(ctx, remote, message, nopack, file):
    # pass
# def upload(ctx=None, remote=None, message=None, nopack=None, is_increment=False, file=None, resume=False):
    """
    Upload data in the current dir to Russell.
    """
    if message and len(message) > 1024:
        russell_logger.error("Message body length over limit")
        sys.exit()

    try:
        data_config = DataConfigManager.get_config()  # type: DataModuleConfig
        access_token = AuthConfigManager.get_access_token()
    except Exception as e:
        russell_logger.error("Configuration Error. {}".format(e))
        russell_logger.debug("Configuration Error. {}".format(traceback.format_exc(e)))
        return

    is_compress = not nopack

    # if hdf5 and bit:
    #     russell_logger.error("choose only one model from hdf5 and bit")
    #     sys.exit()
    is_zip = False
    resume = True
    resume_file = None
    if resume:
        data_module_id = data_config.data_predecessor
        if not data_module_id:  # 初次上传
            resume = False
        else:
            temp_dir = os.path.expanduser("~/.russellDataTemp/{}".format(data_module_id))
            if not os.path.exists(temp_dir):
                resume = False
            else:
                files = os.listdir(temp_dir)
                if len(files) <= 0 or not os.path.exists("{}/{}".format(temp_dir, files[0])):  # 先检查文件是否仍存在
                    # russell_logger("Can't resume upload. Compressed data lost. Please upload again.")
                    # return
                    resume = False
                else:
                    resume_file = "{}/{}".format(temp_dir, files[0])
                    is_zip, is_compress = check_compress(resume_file, is_zip, is_compress)
                    http_client = RussellHttpClient()
                    http_client.base_url = "https://" + russell.russell_fs_host + "/api/v{}"
                    res = requests.get("https://{}/api/v1/resume_check".format(russell.russell_fs_host),
                                       params={"file_id": data_module_id, "is_zip": is_zip, "is_compress": is_compress})
                    result = json.loads(res.content).get("data", "False") == "True"
                    if not result or not click.confirm('Detect old upload exist. Use resume upload?', default=True):
                        resume = False

    if resume_file and resume:
        file = resume_file

    if file:
        is_zip, is_compress = check_compress(file, is_zip, is_compress)
        size = os.path.getsize(file)
    else:
        file_count, size = get_files_in_current_directory('data')

    if not resume and size > 20 * 1024 * 1024 * 1024:
        sys.exit("Total size: {}. Data size too large to sync, please keep it under 20GB.".format(sizeof_fmt(size)))

    if remote:
        module_info = ModuleClient().get(id=data_config.data_predecessor)
        print_upload([module_info])
        return

    # 检查是否可使用断点续传
    if resume:
        fc = FsClient()
        try:
            fc.socket_upload(file_type="data",
                             filename=file,
                             access_token=access_token.token,
                             file_id=data_module_id,
                             user_name=access_token.username,
                             data_name=data_config.name,
                             entity_id=data_config.dataset_id,
                             is_increment=True,
                             is_compress=is_compress,
                             is_zip=is_zip,
                             is_direct=True,
                             resume=resume)
        except Exception as e:
            russell_logger.error("Upload failed: {}".format(e.message))
            return
        else:
            ### check socket state, some errors cannot be catched by `except`
            state = fc.get_state()
            if state == SOCKET_STATE.FAILED:
                russell_logger.error("Upload failed, please try after a while...")
                return
            if state in [SOCKET_STATE.FAILED, SOCKET_STATE.FINISH] and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    else:
        ###
        # if len(files) > 100:
        #     russell_logger.warning("Too many files to upload.It is better to reduce the number of files.")

        # _TEMP_UPLOAD_DIR = '.russellUploadTemp'
        # copy_files('.', _TEMP_UPLOAD_DIR)

        # if bit:  # TODO: support hdf5
        #     is_compress = True  # must compress
        #     # Gen temp dir
        #     _TEMP_DIR = '.russellDataTemp'

        # version = data_config.version + 1

        try:
            dc = DataClient()
        except Exception as e:
            russell_logger.error(e.message)
            return

        version = data_config.version

        # Create data module object
        data = ModuleRequest(name=data_config.name,
                             description=message,
                             module_type="data",
                             entity_id=data_config.dataset_id,
                             version=version)

        create_module_info = dc.create_module(data)
        data_module_id = create_module_info.get('id')
        data_module_version = int(create_module_info.get('version'))

        # Update expt config including predecessor
        data_config.set_version(data_module_version)
        data_config.set_data_predecessor(data_module_id)
        DataConfigManager.set_config(data_config)

        if file:
            fc = FsClient()
            try:
                fc.socket_upload(file_type="data",
                                 filename=file,
                                 access_token=access_token.token,
                                 file_id=data_module_id,
                                 user_name=access_token.username,
                                 data_name=data_config.name,
                                 entity_id=data_config.dataset_id,
                                 is_increment=True,
                                 is_compress=is_compress,
                                 is_zip=is_zip,
                                 is_direct=True,
                                 resume=resume)
            except Exception as e:
                russell_logger.error("Upload failed: {}".format(e.message))
                return
            else:
                ### check socket state, some errors cannot be catched by `except`
                state = fc.get_state()
                if state == SOCKET_STATE.FAILED:
                    russell_logger.error("Upload failed, please try after a while...")
                    return
        else:
            _TEMP_DIR = os.path.expanduser("~/.russellDataTemp/{}".format(data_module_id))

            fc = FsClient()
            try:
                if not os.path.exists(_TEMP_DIR):
                    os.makedirs(_TEMP_DIR)
                fc.socket_upload_tar(file_type="data",
                                     filename='.',
                                     access_token=access_token.token,
                                     file_id=data_module_id,
                                     entity_id=data_config.dataset_id,
                                     is_increment=True,
                                     user_name=access_token.username,
                                     data_name=data_config.name,
                                     is_compress=is_compress,
                                     temp_dir=_TEMP_DIR,
                                     resume=resume)
            except Exception as e:
                russell_logger.error("Upload failed: {}".format(e.message))
                if os.path.exists(_TEMP_DIR):
                    shutil.rmtree(_TEMP_DIR)
                return
            else:
                ### check socket state, some errors cannot be catched by `except`
                state = fc.get_state()
                if state == SOCKET_STATE.FAILED:
                    russell_logger.error("Upload failed, please try after a while...")
                    return
                if state in [SOCKET_STATE.FAILED, SOCKET_STATE.FINISH] and os.path.exists(_TEMP_DIR):
                    shutil.rmtree(_TEMP_DIR)
            # finally:
            # rm temp dir
            # shutil.rmtree(_TEMP_DIR)

    russell_logger.debug("Created data with id : {}".format(data_module_id))
    russell_logger.info("\nUpload finished")

    data_name = "{}/{}:{}".format(access_token.username,
                                  data_config.name,
                                  data_config.version)
    # Print output
    table_output = [["DATA ID", "NAME", "VERSION"],
                    [data_module_id, data_name.encode("utf-8"), data_config.version]]
    russell_logger.info(tabulate(table_output, headers="firstrow"))
    russell_logger.info('''
Upload finished, start extracting to data module\n
    To check data status enter:
        russell data status {}\n'''.format(data_module_id))


@click.command()
@click.argument('id', required=False, nargs=1)
def status(id):
    """
    Show the status of a run with id.
    It can also list status of all the runs in the project.
    """
    try:
        dc = DataClient()
    except Exception as e:
        russell_logger.error(e.message)
        return
    if id:
        datamodule_source = dc.get(id)
        print_data([datamodule_source])
    else:
        data_config = DataConfigManager.get_config()
        data_sources = dc.get_all(dataset_id=data_config.dataset_id)
        if isinstance(data_sources, list) and len(data_sources) > 0:
            print_data(data_sources)


def print_data(data_sources):
    headers = ["DATA ID", "CREATED", "STATE", "DISK USAGE", "NAME", "VERSION"]
    data_list = []
    for data_source in data_sources:
        data_list.append([data_source.id,
                          data_source.created_pretty,
                          data_source.state,
                          data_source.size_pretty,
                          data_source.name,
                          str(data_source.version)])
    russell_logger.info(tabulate(data_list, headers=headers))


def print_upload(module_sources):
    headers = ["MODULE ID", "STATE" "CREATED", "DISK USAGE", "VERSION"]
    data_list = []
    for data_source in module_sources:
        data_list.append([data_source.id,
                          data_source.state,
                          data_source.created_pretty,
                          data_source.size_pretty,
                          data_source.name.encode('utf-8'),
                          str(data_source.version)])
    russell_logger.info(tabulate(data_list, headers=headers))


@click.command()
@click.option('-u', '--url', is_flag=True, default=False, help='Only print url for viewing data')
@click.argument('id', nargs=1)
def output(id, url):
    """
    Shows the output url of the run.
    By default opens the output page in your default browser.
    """
    # data_source = DataClient().get(id)
    data_url = "{}/files/data/{}/".format(russell.russell_host, id)
    if url:
        russell_logger.info(data_url)
    else:
        russell_logger.info("Opening output directory in your browser ...")
        webbrowser.open(data_url)


@click.command()
@click.argument('id', nargs=1)
@click.option('-y', '--yes', is_flag=True, default=False, help='Skip confirmation')
def delete(id, yes):
    """
    Delete data set.
    """
    try:
        dc = DataClient()
    except Exception as e:
        russell_logger.error(e.message)
        return

    data_source = dc.get(id)
    if not yes:
        click.confirm('Delete Data: {}?'.format(data_source.name), abort=True, default=False)

    if dc.delete(id):
        russell_logger.info("Data deleted")
    else:
        russell_logger.error("Failed to delete data")


data.add_command(delete)
data.add_command(init)
data.add_command(upload)
data.add_command(status)
data.add_command(output)

if __name__ == '__main__':
    russell.russell_host = "https://top.xiaoxiangxueyuan.com"
    russell.russell_web_host = "https://lianxi.xiaoxiangxueyuan.com"
    russell.russell_proxy_host = ""
    russell.russell_fs_host = "fs.xiaoxiangxueyuan.com"
    russell.russell_fs_port = 443
    AuthConfigManager.CONFIG_FILE_PATH += "-dev"
    DataConfigManager.CONFIG_FILE_PATH += "-dev"
    configure_logger(True)
    upload()
