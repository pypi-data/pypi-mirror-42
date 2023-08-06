# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of kiwi.
#
# kiwi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi.  If not, see <http://www.gnu.org/licenses/>
#
import os
import re

# project
from kiwi.command import Command
from kiwi.utils.rpm_database import RpmDataBase
from kiwi.package_manager.base import PackageManagerBase
from kiwi.path import Path
from kiwi.exceptions import (
    KiwiRequestError
)


class PackageManagerYum(PackageManagerBase):
    """
    **Implements base class for installation/deletion of
    packages and collections using yum**

    :param list yum_args: yum arguments from repository runtime configuration
    :param dict command_env: yum command environment from repository runtime
        configuration
    """
    def post_init(self, custom_args=None):
        """
        Post initialization method

        Store custom yum arguments

        :param list custom_args: custom yum arguments
        """
        self.custom_args = custom_args
        if not custom_args:
            self.custom_args = []

        runtime_config = self.repository.runtime_config()
        self.yum_args = runtime_config['yum_args']
        self.command_env = runtime_config['command_env']

    def request_package(self, name):
        """
        Queue a package request

        :param str name: package name
        """
        self.package_requests.append(name)

    def request_collection(self, name):
        """
        Queue a collection request

        :param str name: yum group name
        """
        self.collection_requests.append('"' + name + '"')

    def request_product(self, name):
        """
        Queue a product request

        There is no product definition in the rhel repo data

        :param str name: unused
        """
        pass

    def request_package_exclusion(self, name):
        """
        Queue a package exclusion(skip) request

        :param str name: package name
        """
        self.exclude_requests.append(name)

    def _get_yum_binary_name(self, root=None):
        """
        Identify whether yum is 'yum' or 'yum-deprecated'

        :param str root: lookup binary name below this root directory

        :return: name of yum command

        :rtype: str
        """
        yum_binary = 'yum'
        yum_search_env = {
            'PATH': os.sep.join([root, 'usr', 'bin'])
        } if root else None

        if Path.which(
            filename='yum-deprecated',
            custom_env=yum_search_env,
            access_mode=os.X_OK
        ):
            yum_binary = 'yum-deprecated'
        return yum_binary

    def process_install_requests_bootstrap(self):
        """
        Process package install requests for bootstrap phase (no chroot)

        :return: process results in command type

        :rtype: namedtuple
        """
        yum = self._get_yum_binary_name()
        Command.run(
            [yum] + self.yum_args + ['makecache']
        )
        bash_command = [
            yum
        ] + self.yum_args + [
            '--installroot', self.root_dir
        ] + self.custom_args + ['install'] + self.package_requests
        if self.collection_requests:
            bash_command += [
                '&&', yum
            ] + self.yum_args + [
                '--installroot', self.root_dir
            ] + self.custom_args + ['groupinstall'] + self.collection_requests
        self.cleanup_requests()
        return Command.call(
            ['bash', '-c', ' '.join(bash_command)], self.command_env
        )

    def process_install_requests(self):
        """
        Process package install requests for image phase (chroot)

        :return: process results in command type

        :rtype: namedtuple
        """
        yum = self._get_yum_binary_name(root=self.root_dir)
        if self.exclude_requests:
            # For Yum, excluding a package means removing it from
            # the solver operation. This is done by adding --exclude
            # to the command line. This means that if the package is
            # hard required by another package, it will break the transaction.
            for package in self.exclude_requests:
                self.custom_args.append('--exclude=' + package)
        Command.run(
            ['chroot', self.root_dir, 'rpm', '--rebuilddb']
        )
        chroot_yum_args = self.root_bind.move_to_root(
            self.yum_args
        )
        bash_command = [
            'chroot', self.root_dir, yum
        ] + chroot_yum_args + self.custom_args + [
            'install'
        ] + self.package_requests
        if self.collection_requests:
            bash_command += [
                '&&', 'chroot', self.root_dir, yum
            ] + chroot_yum_args + self.custom_args + [
                'groupinstall'
            ] + self.collection_requests
        self.cleanup_requests()
        return Command.call(
            ['bash', '-c', ' '.join(bash_command)], self.command_env
        )

    def process_delete_requests(self, force=False):
        """
        Process package delete requests (chroot)

        :param bool force: force deletion: true|false

        :raises KiwiRequestError: if none of the packages to delete is
            installed
        :return: process results in command type

        :rtype: namedtuple
        """
        delete_items = []
        for delete_item in self.package_requests:
            try:
                Command.run(['chroot', self.root_dir, 'rpm', '-q', delete_item])
                delete_items.append(delete_item)
            except Exception:
                # ignore packages which are not installed
                pass
        if not delete_items:
            raise KiwiRequestError(
                'None of the requested packages to delete are installed'
            )
        self.cleanup_requests()
        if force:
            delete_options = ['--nodeps', '--allmatches', '--noscripts']
            return Command.call(
                [
                    'chroot', self.root_dir, 'rpm', '-e'
                ] + delete_options + delete_items,
                self.command_env
            )
        else:
            chroot_yum_args = self.root_bind.move_to_root(self.yum_args)
            return Command.call(
                [
                    'chroot', self.root_dir, self._get_yum_binary_name()
                ] + chroot_yum_args + self.custom_args + [
                    'autoremove'
                ] + delete_items,
                self.command_env
            )

    def update(self):
        """
        Process package update requests (chroot)

        :return: process results in command type

        :rtype: namedtuple
        """
        yum = self._get_yum_binary_name(root=self.root_dir)
        chroot_yum_args = self.root_bind.move_to_root(
            self.yum_args
        )
        return Command.call(
            [
                'chroot', self.root_dir, yum
            ] + chroot_yum_args + self.custom_args + [
                'upgrade'
            ],
            self.command_env
        )

    def process_only_required(self):
        """
        Setup package processing only for required packages
        """
        if '--setopt=requires_policy=strong' not in self.custom_args:
            self.custom_args.append('--setopt=requires_policy=strong')

    def process_plus_recommended(self):
        """
        Setup package processing to also include recommended dependencies.
        """
        if '--setopt=requires_policy=strong' in self.custom_args:
            self.custom_args.remove('--setopt=requires_policy=strong')

    def match_package_installed(self, package_name, yum_output):
        """
        Match expression to indicate a package has been installed

        This match for the package to be installed in the output
        of the yum command is not 100% accurate. There might
        be false positives due to sub package names starting with
        the same base package name

        :param list package_list: list of all packages
        :param str log_line: yum status line

        :returns: match or None if there isn't any match

        :rtype: match object, None
        """
        return re.match(
            '.*Installing : ' + re.escape(package_name) + '.*', yum_output
        )

    def match_package_deleted(self, package_name, yum_output):
        """
        Match expression to indicate a package has been deleted

        :param list package_list: list of all packages
        :param str log_line: yum status line

        :returns: match or None if there isn't any match

        :rtype: match object, None
        """
        return re.match(
            '.*Removing: ' + re.escape(package_name) + '.*', yum_output
        )

    def post_process_install_requests_bootstrap(self):
        """
        Move the rpm database to the place as it is expected by the
        rpm package installed during bootstrap phase
        """
        rpmdb = RpmDataBase(self.root_dir)
        rpmdb.set_database_to_image_path()
