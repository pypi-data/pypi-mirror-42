# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2015 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import collections
import datetime
import logging
import os
import platform
import random
import re
import signal
import sys
import tempfile
import time
import urllib.parse

import dateutil.parser
from stoqlib.api import api
from stoqlib.exceptions import DatabaseError
from stoqlib.database.runtime import get_default_store, set_default_store
from stoqlib.database.settings import db_settings
from stoqlib.domain.plugin import PluginEgg
from stoqlib.lib.configparser import get_config
from stoqlib.lib.pluginmanager import get_plugin_manager
from stoqlib.lib.process import Process
from stoqlib.lib.settings import UserSettings

from stoqserver import library
from stoqserver.common import (APP_BACKUP_DIR, SERVER_XMLRPC_PORT,
                               SERVER_FLASK_PORT)
from stoqserver.lib.xmlrpcresource import run_xmlrpcserver
from stoqserver.server import StoqServer

if platform.system() != 'Windows':
    from stoqserver.lib import duplicitybackup as backup
else:
    from stoqserver.lib import duplicatibackup as backup

_lock_remove_threshold = datetime.timedelta(hours=3)
logger = logging.getLogger(__name__)


class TaskException(Exception):
    """Default tasks exception"""


def _setup_signal_termination():
    def _sigterm_handler(_signal, _stack_frame):
        os._exit(0)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, _sigterm_handler)


def backup_database(full=False):
    if not os.path.exists(APP_BACKUP_DIR):
        os.makedirs(APP_BACKUP_DIR)

    filename = os.path.join(APP_BACKUP_DIR, 'stoq.dump')
    if not db_settings.dump_database(filename, format='plain'):
        raise TaskException("Failed to dump the database")

    # FIXME: Change this to a global import when windows support it
    backup.backup(APP_BACKUP_DIR, full=full)
    logger.info("Database backup finished sucessfully")


def restore_database(user_hash, time=None):
    assert user_hash

    # If the database doesn't exist, get_default_store will fail
    try:
        default_store = get_default_store()
    except Exception:
        default_store = None

    if default_store is not None and db_settings.has_database():
        try:
            default_store.lock_database()
        except DatabaseError:
            raise TaskException(
                "Could not lock database. This means that there are other "
                "clients connected. Make sure to close every Stoq client "
                "before updating the database")
        except Exception:
            raise TaskException(
                "Database is empty or in a corrupted state. Fix or drop it "
                "before trying to proceed with the restore")
        else:
            default_store.unlock_database()

        # FIXME: Windows will not liberate resource for other process to
        # write to the file. We should write our own TemporaryFile on Stoq
        # that handles all those cases for us and use here
        with tempfile.NamedTemporaryFile(delete=False) as f:
            pass
        try:
            if not db_settings.dump_database(f.name):
                raise TaskException("Failed to dump the database")
            backup_name = db_settings.restore_database(f.name)
            logger.info("Created a backup of the current database state on %s",
                        backup_name)
        finally:
            os.unlink(f.name)

    tmp_path = tempfile.mkdtemp()
    try:
        restore_path = os.path.join(tmp_path, 'stoq')
        logger.info("restoring database to %s", restore_path)
        backup.restore(restore_path, user_hash, time=time)

        # None will make the default store be closed, which we need
        # to sucessfully restore the database
        set_default_store(None)
        db_settings.clean_database(db_settings.dbname, force=True)
        db_settings.execute_sql(os.path.join(restore_path, 'stoq.dump'),
                                lock_database=True)

        logger.info("Backup restore finished sucessfully")
    finally:
        # get_default_store will recreate it (since we closed it above)
        get_default_store()
        # Dont remove the directory. Since the restauration could have failed, we could use the
        # files to inspect what happend
        #shutil.rmtree(tmp_path, ignore_errors=True)


def backup_status(user_hash=None):
    backup.status(user_hash=user_hash)


def start_xmlrpc_server(pipe_conn):
    _setup_signal_termination()
    logger.info("Starting the xmlrpc server")

    config = get_config()
    port = int(config.get('General', 'serverport') or SERVER_XMLRPC_PORT)

    run_xmlrpcserver(pipe_conn, port)


def start_flask_server(debug=False):
    # We need to delay importing from restfull so that the plugin infrastructure gets setup correcly
    from stoqserver.lib.restful import run_flaskserver

    _setup_signal_termination()
    logger.info("Starting the flask server")

    config = get_config()
    # XXX: Is flaskport a good name for this?
    port = int(config.get('General', 'flaskport') or SERVER_FLASK_PORT)

    run_flaskserver(port, debug)


def start_server():
    _setup_signal_termination()
    logger.info("Starting stoq server")

    stoq_server = StoqServer()
    stoq_server.run()


def start_htsql(port):
    config = get_config()
    if config.get('General', 'disable_htsql'):
        logger.info("Not starting htsql as requested in config file.")
        return

    logger.info("Starting htsql server")

    if db_settings.password:
        password = ':' + urllib.parse.quote_plus(db_settings.password)
    else:
        password = ''
    uri = 'pgsql://{}{}@{}:{}/{}'.format(
        db_settings.username, password,
        db_settings.address, db_settings.port, db_settings.dbname)

    config = library.get_resource_filename('stoqserver', 'htsql', 'config.yml')

    popen = Process(['htsql-ctl', 'server', '-C', config, uri,
                     '--host', '127.0.0.1', '--port', port])

    def _sigterm_handler(_signal, _stack_frame):
        popen.poll()
        if popen.returncode is None:
            popen.terminate()
        os._exit(0)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, _sigterm_handler)

    popen.wait()


def start_rtc():
    if not api.sysparam.get_bool('ONLINE_SERVICES'):
        logger.info("ONLINE_SERVICES not enabled. Not starting rtc...")
        return

    config = get_config()
    if config.get('General', 'disable_rtc'):
        logger.info("Not starting rtc as requested in config file.")
        return

    logger.info("Starting webRTC")

    cwd = library.get_resource_filename('stoqserver', 'webrtc')
    retry = True

    extra_args = []
    camera_urls = config.get('Camera', 'url') or None
    if camera_urls:
        extra_args.append('-c=' + ' '.join(set(camera_urls.split(' '))))

    xmlrpc_host = config.get('General', 'serveraddress') or '127.0.0.1'
    extra_args.append('-h={}'.format(xmlrpc_host))

    xmlrpc_port = config.get('General', 'serverport') or SERVER_XMLRPC_PORT
    extra_args.append('-p={}'.format(xmlrpc_port))

    while retry:
        retry = False
        popen = Process(
            ['bash', 'start.sh'] + extra_args, cwd=cwd)

        def _sigterm_handler(_signal, _stack_frame):
            popen.poll()
            if popen.returncode is None:
                popen.terminate()
            os._exit(0)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, _sigterm_handler)

        popen.wait()
        if popen.returncode == 11:
            logger.warning("libstdc++ too old, not running webRTC client. "
                           "A system upgrade may be required!")
            retry = False
        elif popen.returncode == 10:
            logger.warning("Something failed when trying to start webrtc. "
                           "Retrying again in 10 minutes...")
            time.sleep(10 * 60)
            retry = True
        elif popen.returncode == 12:
            logger.warning("webrtc installation corrupted. Restarting it...")
            time.sleep(1)
            retry = True
        elif popen.returncode == 139:
            logger.warning("Segmentation fault caught on wrtc. Restarting...")
            time.sleep(1)
            retry = True


def start_plugins_update_scheduler(event, doing_backup):
    _setup_signal_termination()

    if not api.sysparam.get_bool('ONLINE_SERVICES'):
        logger.info("ONLINE_SERVICES not enabled. Not scheduling plugin updates...")
        return

    manager = get_plugin_manager()

    while True:
        last_check_str = UserSettings().get('last-plugins-update', None)
        last_check = (dateutil.parser.parse(last_check_str)
                      if last_check_str else datetime.datetime.min)

        # Check for updates once per day
        if last_check.date() == datetime.date.today():
            time.sleep(24 * 60 * 60)
            continue

        logger.info("Checking for plugins updates...")
        updated = False
        default_store = get_default_store()
        for egg in default_store.find(PluginEgg):
            md5sum = egg.egg_md5sum
            manager.download_plugin(egg.plugin_name)

            # If download_plugin updated the plugin, autoreload will
            # make egg. be reloaded from the database
            if md5sum != egg.egg_md5sum:
                updated = True

        settings = UserSettings()
        settings.set('last-plugins-update',
                     datetime.datetime.now().isoformat())
        settings.flush()

        if updated:
            # Wait until any running backup is finished and restart
            while doing_backup.value:
                time.sleep(60)

            logger.info("Some plugins were updated. Restarting now "
                        "to reflect the changes...")
            event.set()
        else:
            logger.info("No update was found...")


def start_backup_scheduler(doing_backup):
    _setup_signal_termination()

    if not api.sysparam.get_bool('ONLINE_SERVICES'):
        logger.info("ONLINE_SERVICES not enabled. Not scheduling backups...")
        return

    logger.info("Starting backup scheduler")

    config = get_config()
    backup_schedule = config.get('Backup', 'schedule')
    if backup_schedule is None:
        # By defualt, we will do 2 backups. One in a random time between
        # 9-11 or 14-17 and another one 12 hours after that.
        # We are using 2, 3 and 4 because they will be summed with 12 bellow
        hour = random.choice([2, 3, 4, 9, 10])
        minute = random.randint(0, 59)
        backup_schedule = '%d:%d,%s:%d' % (hour, minute, hour + 12, minute)
        config.set('Backup', 'schedule', backup_schedule)
        config.flush()

    backup_hours = [list(map(int, i.strip().split(':')))
                    for i in backup_schedule.split(',')]
    now = datetime.datetime.now()
    backup_dates = collections.deque(sorted(
        now.replace(hour=bh[0], minute=bh[1], second=0, microsecond=0)
        for bh in backup_hours))

    while True:
        now = datetime.datetime.now()
        next_date = datetime.datetime.min
        while next_date < now:
            next_date = backup_dates.popleft()
            backup_dates.append(next_date + datetime.timedelta(1))

        time.sleep(max(1, (next_date - now).total_seconds()))

        for i in range(3):
            # FIXME: This is SO UGLY, we should be calling backup_database
            # task directly, but duplicity messes with multiprocessing in a
            # way that it will not work
            args = sys.argv[:]
            for i, arg in enumerate(args[:]):
                if arg == 'run':
                    args[i] = 'backup_database'
                    break

            doing_backup.value = 1
            try:
                p = Process(args)
                stdout, stderr = p.communicate()
            finally:
                doing_backup.value = 0

            if p.returncode == 0:
                break
            else:
                # When duplicity fails in unpredicted situations (e.g. the
                # power is shut down suddenly) it can leave a lockfile behind,
                # and that can make any future backup attempts fail to.
                # Check if that was the reason of the failure and, if the
                # lockfile is older than 3h remove it and try again.
                # Note that this only happens for duplicity (linux) and
                # not for duplicati (windows)
                match = re.search('/.*lockfile.lock', stderr)
                if match is not None:
                    lockfile = match.group(0)
                    now = datetime.datetime.now()
                    mdate = datetime.datetime.fromtimestamp(os.path.getmtime(lockfile))
                    if (now - mdate) > _lock_remove_threshold:
                        os.unlink(lockfile)

                logger.warning(
                    "Failed to backup database:\nstdout: %s\nstderr: %s",
                    stdout, stderr)
                # Retry again with a exponential backoff
                time.sleep((60 * 2) ** (i + 1))
