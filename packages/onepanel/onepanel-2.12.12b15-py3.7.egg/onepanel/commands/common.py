import os
import subprocess
import sys
import logging

import click

from onepanel.commands import jobs
from onepanel.commands.datasets import datasets_clone, datasets_download, DatasetViewController, general_push, _datasets_pull, _datasets_push
from onepanel.commands.jobs import jobs_download_output, JobViewController
from onepanel.commands.login import login_required
from onepanel.commands.projects import projects_clone, ProjectViewController
from onepanel.gitwrapper import GitWrapper
from onepanel.utilities.timer import Timer

COMMON_LOGGER = 'common_logger'

def get_entity_type(path):
    dirs = path.split('/')
    entity_type = None
    if len(dirs) == 3:
        account_uid, dir, uid = dirs
        if dir == 'projects':
            entity_type = 'project'
        elif dir == 'datasets':
            entity_type = 'dataset'
    elif len(dirs) == 5:
        account_uid, parent, project_uid, dir, uid = dirs
        if parent == 'projects' and dir == 'jobs':
            entity_type = 'job'
    return entity_type

@click.command('clone', help='Clone project or dataset from server.')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.pass_context
@login_required
def clone(ctx, path, directory,quiet):
    entity_type = get_entity_type(path)
    if entity_type == 'project':
        projects_clone(ctx, path, directory)
    elif entity_type == 'dataset':
        datasets_clone(ctx, path, directory,quiet)
    else:
        click.echo('Invalid project or dataset path.')

@click.command('download', help='Download a dataset')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '--archive',
    type=bool,
    is_flag=True,
    default=False,
    help='Download the output as a compressed file.'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b','--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.pass_context
@login_required
def download(ctx, path, directory,archive,quiet,background):
    entity_type = get_entity_type(path)
    if entity_type == 'dataset':
        datasets_download(ctx, path, directory,quiet,background)
    elif entity_type == 'job':
        jobs_download_output(ctx, path, directory,archive)
    else:
        click.echo('Invalid path.')


@click.command('push', help='Push changes to onepanel')
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Datasets only: Add a message to this version. Up to 255 chars.\"text\".'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Datasets only: Add a name to this version. Use \"text\".'
)
@click.option(
    '-u', '--update-version',
    is_flag=True,
    default=False,
    help='Datasets only, pushes up a new version.'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b', '--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.option(
    '-w', '--watch',
    is_flag=True,
    help='Datasets only: Syncs up local files to remote. Does not create new dataset versions.'
)
@click.option(
    '-t', '--threads',
    type=int,
    help='Datasets only, when doing a watch: Number of threads allowed.'
)
@click.option(
    '-y', '--yes',
    is_flag=True,
    default=False,
    help='Automatic yes to prompts'
)
@click.pass_context
@login_required
def push(ctx, message, name, quiet, background, update_version, watch, threads, yes):
    home = os.getcwd()
    # Are we uploading job output? A project? Or Dataset?
    if os.path.isfile(JobViewController.JOB_OUTPUT_FILE):
        jobs.upload_output(ctx,quiet)
    elif os.path.isfile(ProjectViewController.PROJECT_FILE):
        if message is not None or name is not None:
            click.echo(
                "Projects do not support these arguments. Remove arguments and try again.")
            return
        GitWrapper().push(home)
    elif os.path.isfile(DatasetViewController.DATASET_FILE):
        if background and update_version:
            close_fds = False
            cmd_list = ['onepanel', 'dataset-background-push']
            if message is not None:
                cmd_list.append('--message')
                cmd_list.append('\"'+message+'\"')
            if name is not None:
                cmd_list.append('--name')
                cmd_list.append('\"'+name+'\"')
            if quiet:
                cmd_list.append('-q')
            if background:
                cmd_list.append('-b')
            if sys.platform != 'win32':
                cmd_list.insert(0, 'nice')
                cmd_list.insert(0, 'nohup')
                close_fds = True
            else:
                # /i so that windows doesn't create "%SYSTEM_DRIVE%" folder
                cmd_list.insert(0, 'start /b /i')
            cmd = ' '.join(cmd_list)
            if sys.platform != 'win32':
                stdout = open(os.path.devnull,'a')
                stderr = open(os.path.devnull,'a')
                subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=stdout,
                                 stderr=stderr, shell=True, close_fds=close_fds,preexec_fn=os.setpgrp)
            else:
                # Windows specific instructions
                # https://docs.microsoft.com/en-us/windows/desktop/ProcThread/process-creation-flags
                CREATE_NO_WINDOW = 0x08000000
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True, close_fds=close_fds,
                                 creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP)

            click.echo("Starting upload in the background.")
        elif update_version:
            general_push(ctx, message, name, quiet, background)
        else:
            _datasets_push(ctx, message, name, update_version, quiet, background, watch, threads, yes)
    else:
        click.echo("Cannot determine if you are trying to push job output, dataset files, or project files. Are you in the right directory?")

@click.command('dataset-background-push', help='This is to be called by a python sub-process.',hidden=True)
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Datasets only: Add a message to this version. Up to 255 chars.\"text\".'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Datasets only: Add a name to this version. Use \"text\".'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b','--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.pass_context
@login_required
def background_dataset_push(ctx,message,name,quiet,background):
    general_push(ctx, message, name, quiet, background)


@click.command('pull', help='Pull changes from onepanel (fetch and merge)')
@click.option(
    '-y', '--yes',
    is_flag=True,
    default=False,
    help='Automatic yes to prompts'
)
@click.option(
    '-t', '--threads',
    type=int,
    help='Number of threads allowed for network requests.'
)
@click.pass_context
@login_required
def pull(ctx, yes, threads):
    if os.path.isfile(ProjectViewController.PROJECT_FILE):
        home = os.getcwd()
        GitWrapper().pull(home)
    elif os.path.isfile(DatasetViewController.DATASET_FILE):
        _datasets_pull(ctx, yes, threads)
    else:
        click.echo('Path is not a project or dataset. Nothing to pull.')


@click.command('timer-sync-output', help='Syncs job output and logs repeated on a timer', hidden=True)
@click.option('-j', '--job_uid', type=str, help='The job uid')
@click.option('-p', '--project_uid', type=str, help='The uid of the project the job is for')
@click.option('-a', '--project_account_uid', type=str, help='The uid of the account that owns the project the job is in')
@click.option('-d', '--delay', type=str, help='What interval the timer sends a request')
@click.option('-d', '--path', type=str, help='Path to sync files from')
@click.option('-d', '--destination', type=str, help='Path to sync files to')
@click.option('-v', '--verbose', type=bool, help='If command should log what it is doing')
@click.pass_context
@login_required
def timer_sync_output(ctx, job_uid, project_uid, project_account_uid, path, destination, delay, verbose):
    if delay is None:
        delay = 5.0

    if verbose is None:
        verbose = False

    if verbose:
        logger = logging.getLogger(COMMON_LOGGER)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    def onepanel_push_wrapper():
        if not os.path.exists(path):
            logging.getLogger(COMMON_LOGGER).info('Waiting until path {} exists'.format(path))
            # Wait until path exists
            return

        logging.getLogger(COMMON_LOGGER).info('Doing command')
        jobs.upload_output_with_parameters(ctx, job_uid, project_uid, project_account_uid, source_directory=path, destination=destination)

    timer = Timer(delay, onepanel_push_wrapper)
    timer.start()
    timer.join()