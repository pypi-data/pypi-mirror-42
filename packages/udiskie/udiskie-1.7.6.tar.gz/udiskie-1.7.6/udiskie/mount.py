"""
Mount utilities.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from distutils.spawn import find_executable
from collections import namedtuple
from functools import partial
import inspect
import logging
import os

from .async_ import AsyncList, Coroutine, Return, sleep
from .common import wraps, setdefault, exc_message
from .config import IgnoreDevice, match_config
from .locale import _


__all__ = ['Mounter']


# TODO: add / remove / XXX_all should make proper use of the asynchronous
# execution.


@Coroutine.from_generator_function
def _False():
    yield Return(False)


def _find_device(fn):
    """
    Decorator for Mounter methods taking a Device as their first argument.

    Enables to pass the path name as first argument and does some common error
    handling (logging).
    """
    @wraps(fn)
    def wrapper(self, device_or_path, *args, **kwargs):
        try:
            device = self.udisks.find(device_or_path)
        except ValueError as e:
            self._log.error(exc_message(e))
            return _False()
        return Coroutine(fn(self, device, *args, **kwargs))
    return wrapper


def _find_device_auto_losetup(fn):
    @Coroutine.from_generator_function
    def wrapper(self, device_or_path, *args, **kwargs):
        try:
            try:
                device = self.udisks.find(device_or_path)
            except ValueError as e:
                if not os.path.isfile(device_or_path):
                    raise
                device = yield self.losetup(device_or_path)
                bound = inspect.getcallargs(fn, self, device, *args, **kwargs)
                if bound.get('recursive') is False:
                    yield Return(device)
        except Exception as e:
            self._log.error(exc_message(e))
            yield Return(False)
        result = yield Coroutine(fn(self, device, *args, **kwargs))
        yield Return(result)
    return wrapper


def _sets_async_error(fn):
    @wraps(fn)
    def wrapper(self, device, *args, **kwargs):
        async_ = fn(self, device, *args, **kwargs)
        async_.errbacks.append(partial(self._error, fn, device))
        return async_
    return wrapper


def _suppress_error(fn):
    """
    Prevent errors in this function from being shown. This is OK, since all
    errors happen in sub-functions in which errors ARE logged.
    """
    @wraps(fn)
    def wrapper(self, device, *args, **kwargs):
        async_ = fn(self, device, *args, **kwargs)
        async_.errbacks.append(lambda *args: True)
        return async_
    return wrapper


def _is_parent_of(parent, child):
    """Check whether the first device is the parent of the second device."""
    if child.is_partition:
        return child.partition_slave == parent
    if child.is_toplevel:
        return child.drive == parent and child != parent
    return False


def _get_parent(device):
    """Return the container device or ``None``."""
    return device.partition_slave or device.luks_cleartext_slave


class Mounter(object):

    """
    Mount utility.

    Stores environment variables (filter, prompt, browser, udisks) to use
    across multiple mount operations.

    :ivar udisks: adapter to the udisks service

    NOTE: The optional parameters are not guaranteed to keep their order and
    should always be passed as keyword arguments.
    """

    def __init__(self, udisks,
                 config=None,
                 prompt=None,
                 browser=None,
                 cache=None):
        """
        Initialize mounter with the given defaults.

        :param udisks: udisks service object. May be a Sniffer or a Daemon.
        :param list config: list of :class:`DeviceFilter`
        :param callable prompt: retrieve passwords for devices
        :param callable browser: open devices

        If prompt is None, device unlocking will not work.
        If browser is None, browse will not work.
        """
        self.udisks = udisks
        self._config = (config or []) + [
            IgnoreDevice({'symlinks': '/dev/mapper/docker-*', 'ignore': True}),
            IgnoreDevice({'symlinks': '/dev/disk/by-id/dm-name-docker-*', 'ignore': True}),
            IgnoreDevice({'is_loop': True, 'loop_file': '/*', 'ignore': False}),
            IgnoreDevice({'is_block': False, 'ignore': True}),
            IgnoreDevice({'is_external': False, 'ignore': True}),
            IgnoreDevice({'is_ignored': True, 'ignore': True})]
        self._prompt = prompt
        self._browser = browser
        self._cache = cache
        self._log = logging.getLogger(__name__)
        try:
            # propagate error messages to UDisks1 daemon for 'Job failed'
            # notifications.
            self._set_error = self.udisks.set_error
        except AttributeError:
            self._set_error = lambda device, action, message: None

    def _error(self, fn, device, err, fmt):
        message = exc_message(err)
        self._log.error(_('failed to {0} {1}: {2}',
                          fn.__name__, device, message))
        self._set_error(device, fn.__name__, message)
        return True

    @_sets_async_error
    @_find_device
    def browse(self, device):
        """
        Browse device.

        :param device: device object, block device path or mount path
        :returns: success
        :rtype: bool
        """
        if not device.is_mounted:
            self._log.error(_("not browsing {0}: not mounted", device))
            yield Return(False)
        if not self._browser:
            self._log.error(_("not browsing {0}: no program", device))
            yield Return(False)
        self._log.debug(_('opening {0} on {0.mount_paths[0]}', device))
        self._browser(device.mount_paths[0])
        self._log.info(_('opened {0} on {0.mount_paths[0]}', device))
        yield Return(True)

    # mount/unmount
    @_sets_async_error
    @_find_device
    def mount(self, device):
        """
        Mount the device if not already mounted.

        :param device: device object, block device path or mount path
        :returns: whether the device is mounted.
        :rtype: bool
        """
        if not self.is_handleable(device) or not device.is_filesystem:
            self._log.warn(_('not mounting {0}: unhandled device', device))
            yield Return(False)
        if device.is_mounted:
            self._log.info(_('not mounting {0}: already mounted', device))
            yield Return(True)
        options = match_config(self._config, device, 'options', None)
        kwargs = dict(options=options)
        self._log.debug(_('mounting {0} with {1}', device, kwargs))
        self._check_device_before_mount(device)
        mount_path = yield device.mount(**kwargs)
        self._log.info(_('mounted {0} on {1}', device, mount_path))
        yield Return(True)

    def _check_device_before_mount(self, device):
        if device.id_type == 'ntfs' and not find_executable('ntfs-3g'):
            self._log.warn(_(
                "Mounting NTFS device with default driver.\n"
                "Please install 'ntfs-3g' if you experience problems or the "
                "device is readonly."))

    @_sets_async_error
    @_find_device
    def unmount(self, device):
        """
        Unmount a Device if mounted.

        :param device: device object, block device path or mount path
        :returns: whether the device is unmounted
        :rtype: bool
        """
        if not self.is_handleable(device) or not device.is_filesystem:
            self._log.warn(_('not unmounting {0}: unhandled device', device))
            yield Return(False)
        if not device.is_mounted:
            self._log.info(_('not unmounting {0}: not mounted', device))
            yield Return(True)
        self._log.debug(_('unmounting {0}', device))
        yield device.unmount()
        self._log.info(_('unmounted {0}', device))
        yield Return(True)

    # unlock/lock (LUKS)
    @_sets_async_error
    @_find_device
    def unlock(self, device):
        """
        Unlock the device if not already unlocked.

        :param device: device object, block device path or mount path
        :returns: whether the device is unlocked
        :rtype: bool
        """
        if not self.is_handleable(device) or not device.is_crypto:
            self._log.warn(_('not unlocking {0}: unhandled device', device))
            yield Return(False)
        if device.is_unlocked:
            self._log.info(_('not unlocking {0}: already unlocked', device))
            yield Return(True)
        if not self._prompt:
            self._log.error(_('not unlocking {0}: no password prompt', device))
            yield Return(False)
        unlocked = yield self._unlock_from_cache(device)
        if unlocked:
            yield Return(True)
        unlocked = yield self._unlock_from_keyfile(device)
        if unlocked:
            yield Return(True)
        password = yield self._prompt(device, self.udisks.keyfile_support)
        if password is None:
            self._log.debug(_('not unlocking {0}: cancelled by user', device))
            yield Return(False)
        if isinstance(password, bytes):
            self._log.debug(_('unlocking {0} using keyfile', device))
            yield device.unlock_keyfile(password)
        else:
            self._log.debug(_('unlocking {0}', device))
            yield device.unlock(password)
        self._update_cache(device, password)
        self._log.info(_('unlocked {0}', device))
        yield Return(True)

    @Coroutine.from_generator_function
    def _unlock_from_cache(self, device):
        if not self._cache:
            yield Return(False)
        try:
            password = self._cache[device]
        except KeyError:
            yield Return(False)
        self._log.debug(_('unlocking {0} using cached password', device))
        try:
            yield device.unlock(password)
        except Exception:
            self._log.debug(_('failed to unlock {0} using cached password', device))
            yield Return(False)
        self._log.info(_('unlocked {0} using cached password', device))
        yield Return(True)

    @Coroutine.from_generator_function
    def _unlock_from_keyfile(self, device):
        if not self.udisks.keyfile_support:
            yield Return(False)
        filename = match_config(self._config, device, 'keyfile', None)
        if filename is None:
            self._log.debug(_('No matching keyfile rule for {}.', device))
            yield Return(False)
        try:
            with open(filename, 'rb') as f:
                keyfile = f.read()
        except IOError:
            self._log.warn(_('configured keyfile for {0} not found', device))
            yield Return(False)
        self._log.debug(_('unlocking {0} using keyfile {1}', device, filename))
        try:
            yield device.unlock_keyfile(keyfile)
        except Exception:
            self._log.debug(_('failed to unlock {0} using keyfile', device))
            yield Return(False)
        self._log.info(_('unlocked {0} using keyfile', device))
        yield Return(True)

    def _update_cache(self, device, password):
        if not self._cache:
            return
        self._cache[device] = password

    def forget_password(self, device):
        try:
            del self._cache[device]
        except KeyError:
            pass

    @_sets_async_error
    @_find_device
    def lock(self, device):
        """
        Lock device if unlocked.

        :param device: device object, block device path or mount path
        :returns: whether the device is locked
        :rtype: bool
        """
        if not self.is_handleable(device) or not device.is_crypto:
            self._log.warn(_('not locking {0}: unhandled device', device))
            yield Return(False)
        if not device.is_unlocked:
            self._log.info(_('not locking {0}: not unlocked', device))
            yield Return(True)
        self._log.debug(_('locking {0}', device))
        yield device.lock()
        self._log.info(_('locked {0}', device))
        yield Return(True)

    # add/remove (unlock/lock or mount/unmount)
    @_suppress_error
    @_find_device_auto_losetup
    def add(self, device, recursive=None):
        """
        Mount or unlock the device depending on its type.

        :param device: device object, block device path or mount path
        :param bool recursive: recursively mount and unlock child devices
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        if device.is_filesystem:
            success = yield self.mount(device)
        elif device.is_crypto:
            success = yield self.unlock(device)
            if success and recursive:
                yield self.udisks._sync()
                device = self.udisks[device.object_path]
                success = yield self.add(
                    device.luks_cleartext_holder,
                    recursive=True)
        elif (recursive
              and device.is_partition_table
              and self.is_handleable(device)):
            tasks = [
                self.add(dev, recursive=True)
                for dev in self.get_all_handleable()
                if dev.is_partition and dev.partition_slave == device
            ]
            results = yield AsyncList(tasks)
            success = all(results)
        else:
            self._log.info(_('not adding {0}: unhandled device', device))
            yield Return(False)
        yield Return(success)

    @_suppress_error
    @_find_device_auto_losetup
    def auto_add(self, device, recursive=None):
        """
        Automatically attempt to mount or unlock a device, but be quiet if the
        device is not supported.

        :param device: device object, block device path or mount path
        :param bool recursive: recursively mount and unlock child devices
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        success = True
        if device.is_luks_cleartext and self.udisks.version_info >= (2,7,0):
            yield sleep(1.5)    # temporary workaround for #153, unreliable...
        if not self.is_automount(device):
            pass
        elif device.is_filesystem:
            if not device.is_mounted:
                success = yield self.mount(device)
        elif device.is_crypto:
            if self._prompt and not device.is_unlocked:
                success = yield self.unlock(device)
            if success and recursive:
                yield self.udisks._sync()
                device = self.udisks[device.object_path]
                success = yield self.auto_add(
                    device.luks_cleartext_holder,
                    recursive=True)
        elif recursive and device.is_partition_table:
            tasks = [
                self.auto_add(dev, recursive=True)
                for dev in self.get_all_handleable()
                if dev.is_partition and dev.partition_slave == device
            ]
            results = yield AsyncList(tasks)
            success = all(results)
        else:
            self._log.debug(_('not adding {0}: unhandled device', device))
        yield Return(success)

    @_suppress_error
    @_find_device
    def remove(self, device, force=False, detach=False, eject=False,
               lock=False):
        """
        Unmount or lock the device depending on device type.

        :param device: device object, block device path or mount path
        :param bool force: recursively remove all child devices
        :param bool detach: detach the root drive
        :param bool eject: remove media from the root drive
        :param bool lock: lock the associated LUKS cleartext slave
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        if device.is_filesystem:
            if device.is_mounted or not device.is_loop or detach is False:
                success = yield self.unmount(device)
        elif device.is_crypto:
            if force and device.is_unlocked:
                yield self.auto_remove(device.luks_cleartext_holder, force=True)
            success = yield self.lock(device)
        elif (force
              and (device.is_partition_table or device.is_drive)
              and self.is_handleable(device)):
            kw = dict(force=True, detach=detach, eject=eject, lock=lock)
            tasks = [
                self.auto_remove(child, **kw)
                for child in self.get_all_handleable()
                if _is_parent_of(device, child)
            ]
            results = yield AsyncList(tasks)
            success = all(results)
        else:
            self._log.info(_('not removing {0}: unhandled device', device))
            success = False
        # if these operations work, everything is fine, we can return True:
        if lock and device.is_luks_cleartext:
            device = device.luks_cleartext_slave
            success = yield self.lock(device)
        if eject:
            success = yield self.eject(device)
        if (detach or detach is None) and device.is_loop:
            success = yield self.delete(device, remove=False)
        elif detach:
            success = yield self.detach(device)
        yield Return(success)

    @_suppress_error
    @_find_device
    def auto_remove(self, device, force=False, detach=False, eject=False,
                    lock=False):
        """
        Unmount or lock the device depending on device type.

        :param device: device object, block device path or mount path
        :param bool force: recursively remove all child devices
        :param bool detach: detach the root drive
        :param bool eject: remove media from the root drive
        :param bool lock: lock the associated LUKS cleartext slave
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        success = True
        if not self.is_handleable(device):
            pass
        elif device.is_filesystem:
            if device.is_mounted:
                success = yield self.unmount(device)
        elif device.is_crypto:
            if force and device.is_unlocked:
                yield self.auto_remove(device.luks_cleartext_holder, force=True)
            if device.is_unlocked:
                success = yield self.lock(device)
        elif force and (device.is_partition_table or device.is_drive):
            kw = dict(force=True, detach=detach, eject=eject, lock=lock)
            tasks = [
                self.auto_remove(child, **kw)
                for child in self.get_all_handleable()
                if _is_parent_of(device, child)
            ]
            results = yield AsyncList(tasks)
            success = all(results)
        else:
            self._log.debug(_('not removing {0}: unhandled device', device))
        # if these operations work, everything is fine, we can return True:
        if lock and device.is_luks_cleartext:
            device = device.luks_cleartext_slave
            success = yield self.lock(device)
        if eject and device.has_media:
            success = yield self.eject(device)
        if (detach or detach is None) and device.is_loop:
            success = yield self.delete(device, remove=False)
        elif detach and device.is_detachable:
            success = yield self.detach(device)
        yield Return(success)

    # eject/detach device
    @_sets_async_error
    @_find_device
    def eject(self, device, force=False):
        """
        Eject a device after unmounting all its mounted filesystems.

        :param device: device object, block device path or mount path
        :param bool force: remove child devices before trying to eject
        :returns: whether the operation succeeded
        :rtype: bool
        """
        if not self.is_handleable(device):
            self._log.warn(_('not ejecting {0}: unhandled device'))
            yield Return(False)
        drive = device.drive
        if not (drive.is_drive and drive.is_ejectable):
            self._log.warn(_('not ejecting {0}: drive not ejectable', drive))
            yield Return(False)
        if force:
            # Can't autoremove 'device.drive', because that will be filtered
            # due to block=False:
            yield self.auto_remove(device.root, force=True)
        self._log.debug(_('ejecting {0}', device))
        yield drive.eject()
        self._log.info(_('ejected {0}', device))
        yield Return(True)

    @_sets_async_error
    @_find_device
    def detach(self, device, force=False):
        """
        Detach a device after unmounting all its mounted filesystems.

        :param device: device object, block device path or mount path
        :param bool force: remove child devices before trying to detach
        :returns: whether the operation succeeded
        :rtype: bool
        """
        if not self.is_handleable(device):
            self._log.warn(_('not detaching {0}: unhandled device', device))
            yield Return(False)
        drive = device.root
        if not drive.is_detachable:
            self._log.warn(_('not detaching {0}: drive not detachable', drive))
            yield Return(False)
        if force:
            yield self.auto_remove(drive, force=True)
        self._log.debug(_('detaching {0}', device))
        yield drive.detach()
        self._log.info(_('detached {0}', device))
        yield Return(True)

    # mount_all/unmount_all
    @Coroutine.from_generator_function
    def add_all(self, recursive=False):
        """
        Add all handleable devices that available at start.

        :param bool recursive: recursively mount and unlock child devices
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        tasks = [self.auto_add(device, recursive=recursive)
                 for device in self.get_all_handleable_leaves()]
        results = yield AsyncList(tasks)
        success = all(results)
        yield Return(success)

    @Coroutine.from_generator_function
    def remove_all(self, detach=False, eject=False, lock=False):
        """
        Remove all filesystems handleable by udiskie.

        :param bool detach: detach the root drive
        :param bool eject: remove media from the root drive
        :param bool lock: lock the associated LUKS cleartext slave
        :returns: whether all attempted operations succeeded
        :rtype: bool
        """
        kw = dict(force=True, detach=detach, eject=eject, lock=lock)
        tasks = [self.auto_remove(device, **kw)
                 for device in self.get_all_handleable_roots()]
        results = yield AsyncList(tasks)
        success = all(results)
        yield Return(success)

    # loop devices
    @Coroutine.from_generator_function
    def losetup(self, image,
                read_only=True, offset=None, size=None, no_part_scan=None):
        """
        Setup a loop device.

        :param str image: path of the image file
        :param bool read_only:
        :param int offset:
        :param int size:
        :param bool no_part_scan:
        :returns: the device object for the loop device
        """
        try:
            device = self.udisks.find(image)
        except ValueError:
            pass
        else:
            self._log.info(_('not setting up {0}: already up', device))
            yield Return(device)
        if not os.path.isfile(image):
            self._log.error(_('not setting up {0}: not a file', image))
            yield Return(None)
        if not self.udisks.loop_support:
            self._log.error(_('not setting up {0}: unsupported in UDisks1', image))
            yield Return(None)
        self._log.debug(_('setting up {0}', image))
        fd = os.open(image, os.O_RDONLY)
        device = yield self.udisks.loop_setup(fd, {
            'offset': offset,
            'size': size,
            'read-only': read_only,
            'no-part-scan': no_part_scan,
        })
        self._log.info(_('set up {0} as {1}', image,
                         device.device_presentation))
        yield Return(device)

    @_sets_async_error
    @_find_device
    def delete(self, device, remove=True):
        """
        Detach the loop device.

        :param device: device object, block device path or mount path
        :param bool remove: whether to unmount the partition etc.
        :returns: whether the loop device is deleted
        :rtype: bool
        """
        if not self.is_handleable(device) or not device.is_loop:
            self._log.warn(_('not deleting {0}: unhandled device', device))
            yield Return(False)
        if remove:
            yield self.auto_remove(device, force=True)
        self._log.debug(_('deleting {0}', device))
        yield device.delete()
        self._log.info(_('deleted {0}', device))
        yield Return(True)

    # iterate devices
    def is_handleable(self, device):
        # TODO: handle pathes in first argument
        """
        Check whether this device should be handled by udiskie.

        :param device: device object, block device path or mount path
        :returns: handleability
        :rtype: bool

        Currently this just means that the device is removable and holds a
        filesystem or the device is a LUKS encrypted volume.
        """
        ignored = self._ignore_device(device)
        # propagate handleability of parent devices:
        if ignored is None and device is not None:
            return self.is_handleable(_get_parent(device))
        return not ignored

    def is_automount(self, device):
        if not self.is_handleable(device):
            return False
        return match_config(self._config, device, 'automount', True)

    def _ignore_device(self, device):
        return match_config(self._config, device, 'ignore', False)

    def is_addable(self, device):
        """
        Check if device can be added with ``auto_add``.
        """
        if not self.is_automount(device):
            return False
        if device.is_filesystem:
            return not device.is_mounted
        if device.is_crypto:
            return self._prompt and not device.is_unlocked
        if device.is_partition_table:
            return any(self.is_addable(dev)
                       for dev in self.get_all_handleable()
                       if dev.partition_slave == device)
        return False

    def is_removable(self, device):
        """
        Check if device can be removed with ``auto_remove``.
        """
        if not self.is_handleable(device):
            return False
        if device.is_filesystem:
            return device.is_mounted
        if device.is_crypto:
            return device.is_unlocked
        if device.is_partition_table or device.is_drive:
            return any(self.is_removable(dev)
                       for dev in self.get_all_handleable()
                       if _is_parent_of(device, dev))
        return False

    def get_all_handleable(self):
        """
        Enumerate all handleable devices currently known to udisks.

        :returns: handleable devices
        :rtype: list
        """
        nodes = self.get_device_tree()
        return [node.device
                for node in sorted(nodes.values(), key=DevNode._sort_key)
                if not node.ignored and node.device]

    def get_all_handleable_roots(self):
        """
        Get list of all handleable devices, return only those that represent
        root nodes within the filtered device tree.
        """
        nodes = self.get_device_tree()
        return [node.device
                for node in sorted(nodes.values(), key=DevNode._sort_key)
                if not node.ignored and node.device
                and (node.root == '/' or nodes[node.root].ignored)]

    def get_all_handleable_leaves(self):
        """
        Get list of all handleable devices, return only those that represent
        leaf nodes within the filtered device tree.
        """
        nodes = self.get_device_tree()
        return [node.device
                for node in sorted(nodes.values(), key=DevNode._sort_key)
                if not node.ignored and node.device
                and all(child.ignored for child in node.children)]

    def get_device_tree(self):
        """Get a tree of all devices."""
        root = DevNode(None, None, [], None)
        device_nodes = {
            dev.object_path: DevNode(dev, dev.parent_object_path, [],
                                     self._ignore_device(dev))
            for dev in self.udisks
        }
        for node in device_nodes.values():
            device_nodes.get(node.root, root).children.append(node)
        device_nodes['/'] = root
        for node in device_nodes.values():
            node.children.sort(key=DevNode._sort_key)
        # use parent as fallback, update top->down:
        def propagate_ignored(node):
            for child in node.children:
                if child.ignored is None:
                    child.ignored = node.ignored
                propagate_ignored(child)
        propagate_ignored(root)
        return device_nodes


class DevNode:

    def __init__(self, device, root, children, ignored):
        self.device = device
        self.root = root
        self.children = children
        self.ignored = ignored

    def _sort_key(self):
        return self.device.device_presentation if self.device else ''


# data structs containing the menu hierarchy:
Device = namedtuple('Device', ['root', 'branches', 'device', 'label', 'methods'])
Action = namedtuple('Action', ['method', 'device', 'label', 'action'])


class DeviceActions(object):

    _labels = {
        'browse': _('Browse {0}'),
        'mount': _('Mount {0}'),
        'unmount': _('Unmount {0}'),
        'unlock': _('Unlock {0}'),
        'lock': _('Lock {0}'),
        'eject': _('Eject {1}'),
        'detach': _('Unpower {1}'),
        'forget_password': _('Clear password for {0}'),
        'delete': _('Detach {0}'),
    }

    def __init__(self, mounter, actions={}):
        self._mounter = mounter
        self._actions = _actions = actions.copy()
        setdefault(_actions, {
            'browse': mounter.browse,
            'mount': mounter.mount,
            'unmount': mounter.unmount,
            'unlock': mounter.unlock,
            'lock': partial(mounter.remove, force=True),
            'eject': partial(mounter.eject, force=True),
            'detach': partial(mounter.detach, force=True),
            'forget_password': mounter.forget_password,
            'delete': mounter.delete,
        })

    def detect(self, root_device='/'):
        """
        Detect all currently known devices.

        :param str root_device: object path of root device to return
        :returns: root of device hierarchy
        :rtype: Device
        """
        root = Device(None, [], None, "", [])
        device_nodes = dict(map(self._device_node,
                                self._mounter.get_all_handleable()))
        # insert child devices as branches into their roots:
        for node in device_nodes.values():
            device_nodes.get(node.root, root).branches.append(node)
        device_nodes['/'] = root
        for node in device_nodes.values():
            node.branches.sort(key=lambda node: node.label)
        return device_nodes[root_device]

    def _get_device_methods(self, device):
        """Return an iterable over all available methods the device has."""
        if device.is_filesystem:
            if device.is_mounted:
                if self._mounter._browser:
                    yield 'browse'
                yield 'unmount'
            else:
                yield 'mount'
        elif device.is_crypto:
            if device.is_unlocked:
                yield 'lock'
            else:
                yield 'unlock'
            cache = self._mounter._cache
            if cache and device in cache:
                yield 'forget_password'
        if device.is_ejectable and device.has_media:
            yield 'eject'
        if device.is_detachable:
            yield 'detach'
        if device.is_loop and device.loop_support:
            yield 'delete'

    def _device_node(self, device):
        """Create an empty menu node for the specified device."""
        label = device.ui_label
        dev_label = device.ui_device_label
        # determine available methods
        methods = [Action(method, device,
                          self._labels[method].format(label, dev_label),
                          partial(self._actions[method], device))
                   for method in self._get_device_methods(device)]
        # find the root device:
        root = device.parent_object_path
        # in this first step leave branches empty
        return device.object_path, Device(root, [], device, dev_label, methods)


def prune_empty_node(node, seen):
    """
    Recursively remove empty branches and return whether this makes the node
    itself empty.

    The ``seen`` parameter is used to avoid infinite recursion due to cycles
    (you never know).
    """
    if node.methods:
        return False
    if id(node) in seen:
        return True
    seen = seen | {id(node)}
    for branch in list(node.branches):
        if prune_empty_node(branch, seen):
            node.branches.remove(branch)
        else:
            return False
    return True
