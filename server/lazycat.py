"""Lazycat app notifications through the system notify-send channel.

lzcos injects /lzcinit/notify-send into the app's containers when the package
declares the user.notify permission (lzcos 1.6.0+). Outside Lazycat the file is
absent and the channel reports itself unavailable.
"""
import logging
import os
import re
import subprocess

NOTIFY_SEND = '/lzcinit/notify-send'
# Ingress sets this header on every request from a logged-in Lazycat user.
USER_HEADER = 'X-HC-User-ID'
_UID = re.compile(r'[A-Za-z0-9._@-]{1,128}')


def available():
    return os.access(NOTIFY_SEND, os.X_OK)


def valid_uid(value):
    return isinstance(value, str) and _UID.fullmatch(value) is not None


def send(uid, title, body):
    if not available() or not valid_uid(uid):
        return False
    args = [NOTIFY_SEND, '--uid', uid]
    domain = os.environ.get('LAZYCAT_APP_DOMAIN', '')
    if re.fullmatch(r'[A-Za-z0-9.-]{1,253}', domain):
        args += ['--deeplink-url', 'https://' + domain]
    # Same argument shape as the proven herdr-mobile caller; titles and bodies
    # here never start with "-", so they cannot be read as options.
    args += [title[:200], body[:2000]]
    try:
        result = subprocess.run(args, capture_output=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        logging.warning('懒猫通知发送异常：%s', type(exc).__name__)
        return False
    if result.returncode != 0:
        # Exit status only: output could echo the message body.
        logging.warning('懒猫通知发送失败：exit=%s', result.returncode)
        return False
    return True
