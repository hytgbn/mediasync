#!/usr/bin/python3.7

import os
from subprocess import call
import sys
import time
import logging
import argparse

def get_logger():
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)
    logger_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    return logger

logger = get_logger()

SRC_DIR = "/mediadir"
LOCK_FILE = ".lock"

EXCLUDES = ["sync.py", "sync.sh", ".lock"]

class FileSnapshot:
    """
    Snapshot of a file.
    Taking size and mtime.
    A file is considered as changed if size or mtime has changed.
    """

    def __init__(self, path):
        statinfo = os.stat(path)
        self.size = statinfo.st_size
        self.mtime = statinfo.st_mtime

    def dict(self):
        return {"size": self.size, "mtime": self.mtime}

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.dict() == other.dict()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.dict())


def get_snapshots(root):
    """
    return a list of FileSnapshot objects from given directory.
    Not recursive.
    """
    snapshots = {}
    for f in os.listdir(root):
        filepath = os.path.join(root, f)
        if os.path.isfile(filepath):
            if f in EXCLUDES:
                continue
            if f.startswith("."):
                continue
            snapshot = FileSnapshot(filepath)
            snapshots[filepath] = snapshot
    return snapshots


class LockFile(object):
    def __init__(self, lock_path):
        self.lock_path = lock_path

    def __enter__(self):
        try:
            os.open(self.lock_path, os.O_CREAT | os.O_EXCL)
        except Exception as e:
            raise Exception("Lock file already exists. exiting") from e

    def __exit__(self, type, value, traceback):
        os.remove(self.lock_path)


def parse_args():
    parser = argparse.ArgumentParser(description='mediasync')
    parser.add_argument('--sshkey', dest='sshkey', action='store', required=True)
    parser.add_argument('--server', dest='server', action='store', required=True)
    parser.add_argument('--user', dest='user', action='store', required=True)
    parser.add_argument('--path', dest='path', action='store', required=True)
    return parser.parse_args()

def run_sync(opts):
    logger.info("opts: {}".format(opts))

    if not os.path.isdir(SRC_DIR):
        raise Exception("{} not found. ".format(SRC_DIR))

    logger.info("src: {}".format(SRC_DIR))
    logger.info("dst: {}@{}:{}".format(opts.user, opts.server, opts.path))

    lock_path = os.path.join(SRC_DIR, LOCK_FILE)
    with LockFile(lock_path):
        old_snapshots = get_snapshots(SRC_DIR)

        logger.info("old_snapshots: {} ".format(old_snapshots))

        if not old_snapshots:
            logger.info("no file found. exiting...")
            return

        time.sleep(10)

        new_snapshots = get_snapshots(SRC_DIR)

        logger.info("new_snapshots: {} ".format(new_snapshots))

        for filepath, new_snapshot in new_snapshots.items():
            logger.info("checking file. {}".format(filepath))
            try:
                old_snapshot = old_snapshots[filepath]
            except KeyError:
                logger.info("new file. skipping...")
                continue

            if old_snapshot != new_snapshot:
                logger.info("file has not changed. skipping...")
                continue

            cmd = ("/usr/bin/rsync -e \"ssh -i {} -o StrictHostKeyChecking=no\" -t --progress --remove-source-files " +
                "\"{}\"" +
                " {}@{}:{} ").format(opts.sshkey, filepath, opts.user, opts.server, opts.path)

            logger.info("rsyncing... cmd={}".format(cmd))
            call(cmd, shell=True)


if __name__ == "__main__":
    logger.info("Starting sync")
    opts = parse_args()
    run_sync(opts)
    logger.info("Completed sync")
