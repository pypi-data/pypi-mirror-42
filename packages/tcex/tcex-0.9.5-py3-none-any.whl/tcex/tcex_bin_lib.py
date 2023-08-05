#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TcEx Library Builder."""
import json
import os
import re
import platform
import shutil
import subprocess
import sys
from distutils.version import StrictVersion  # pylint: disable=E0611

import colorama as c


class TcExLib(object):
    """Install Required Modules for App."""

    def __init__(self, _arg):
        """Init TcLib Module."""
        self.args = _arg
        self.app_path = os.getcwd()
        self.exit_code = 0
        self.requirements_file = 'requirements.txt'
        self.requirements_temp = False
        self.static_lib_dir = 'lib_latest'

        # initialize colorama
        c.init(autoreset=True, strip=False)

    def install_libs(self):
        """Install Required Libraries using easy install."""
        using = 'Default'
        # default or current python version
        lib_directory = 'lib_{}.{}.{}'.format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        lib_data = [{'python_executable': sys.executable, 'lib_dir': lib_directory}]

        # check for requirements.txt
        if not os.path.isfile(self.requirements_file):
            print((
                '{}{}A requirements.txt file is required to install modules.'.format(
                    c.Style.BRIGHT, c.Fore.RED
                )
            ))
            sys.exit(1)

        if self.args.branch is not None:
            self.requirements_temp = True
            # Replace tcex version with develop branch of tcex
            with open(self.requirements_file, 'r') as fh:
                current_requirements = fh.read().strip().split('\n')

            self.requirements_file = 'temp-{}'.format(self.requirements_file)
            with open(self.requirements_file, 'w') as fh:
                new_requirements = ''
                for line in current_requirements:
                    if not line:
                        continue
                    if line.startswith('tcex'):
                        line = 'git+https://github.com/ThreatConnect-Inc/tcex.git@{}#egg=tcex'
                        line = line.format(self.args.branch)
                    # print('line', line)
                    new_requirements += '{}\n'.format(line)
                fh.write(new_requirements)

        # load configuration
        config_data = {}
        file_path = os.path.join(self.app_path, self.args.config)
        if os.path.isfile(file_path):
            print((
                'Loading Config File: {}{}{}'.format(c.Style.BRIGHT, c.Fore.CYAN, self.args.config)
            ))
            with open(file_path, 'r') as fh:
                config_data = json.load(fh)

        # overwrite default with config data
        if config_data.get('lib_versions'):
            lib_data = config_data.get('lib_versions')
            using = 'Config'

        # install all requested lib directories
        latest_version = None
        for data in lib_data:
            # pattern to match env vars in data
            env_var = re.compile(r'\$env\.([a-zA-Z0-9]+)')

            lib_dir = data.get('lib_dir')
            # replace env vars with env val in the lib dir
            matches = re.findall(env_var, lib_dir)
            if matches:
                env_val = os.environ.get(matches[0])
                lib_dir = re.sub(env_var, env_val, lib_dir)

            lib_dir_fq = os.path.join(self.app_path, lib_dir)

            if os.access(lib_dir_fq, os.W_OK):
                # remove lib directory from previous runs
                shutil.rmtree(lib_dir_fq)

            # replace env vars with env val in the python executable
            python_executable = data.get('python_executable')
            matches = re.findall(env_var, python_executable)
            if matches:
                env_val = os.environ.get(matches[0])
                python_executable = re.sub(env_var, env_val, python_executable)

            print((
                'Building Lib Dir: {}{}{} ({})'.format(
                    c.Style.BRIGHT, c.Fore.CYAN, lib_dir_fq, using
                )
            ))
            exe_command = [
                os.path.expanduser(python_executable),
                '-m',
                'pip',
                'install',
                '-r',
                self.requirements_file,
                '--ignore-installed',
                '--quiet',
                '--target',
                lib_dir_fq,
            ]
            if self.args.no_cache_dir:
                exe_command.append('--no-cache-dir')

            # handle authenticated proxy settings
            if (
                self.args.proxy_host is not None
                and self.args.proxy_port is not None
                and self.args.proxy_user is not None
                and self.args.proxy_pass is not None
            ):
                # create environmental variables with the proxy details (these are deleted later)
                os.putenv(
                    'HTTP_PROXY',
                    'http://{}:{}@{}:{}'.format(
                        self.args.proxy_user,
                        self.args.proxy_pass,
                        self.args.proxy_host,
                        self.args.proxy_port,
                    ),
                )
                os.putenv(
                    'HTTPS_PROXY',
                    'https://{}:{}@{}:{}'.format(
                        self.args.proxy_user,
                        self.args.proxy_pass,
                        self.args.proxy_host,
                        self.args.proxy_port,
                    ),
                )
                # trust the pypi hosts to avoid ssl errors
                trusted_hosts = ['pypi.org', 'pypi.python.org', 'files.pythonhosted.org']

                for host in trusted_hosts:
                    exe_command.append('--trusted-host')
                    exe_command.append(host)
            # handle unauthenticated proxy settings
            elif self.args.proxy_host is not None and self.args.proxy_port is not None:
                # create environmental variables with the proxy details (these are deleted later)
                os.putenv(
                    'HTTP_PROXY', 'http://{}:{}'.format(self.args.proxy_host, self.args.proxy_port)
                )
                os.putenv(
                    'HTTPS_PROXY',
                    'https://{}:{}'.format(self.args.proxy_host, self.args.proxy_port),
                )
                # trust the pypi host to avoid ssl errors
                exe_command.append('--trusted-host')
                exe_command.append('pypi.org')

            print(('Running: {}{}{}'.format(c.Style.BRIGHT, c.Fore.GREEN, ' '.join(exe_command))))
            p = subprocess.Popen(
                exe_command,
                shell=False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = p.communicate()  # pylint: disable=W0612

            if p.returncode != 0:
                print(('{}{}FAIL'.format(c.Style.BRIGHT, c.Fore.RED)))
                print(('{}{}{}'.format(c.Style.BRIGHT, c.Fore.RED, err.decode('utf-8'))))
                sys.exit('ERROR: {}'.format(err.decode('utf-8')))

            # version comparison
            try:
                python_version = lib_dir.split('_', 1)[1]
            except IndexError:
                print((
                    '{}{}{}'.format(
                        c.Style.BRIGHT, c.Fore.RED, 'Could not determine version from lib string.'
                    )
                ))
                sys.exit(1)

            # track the latest Python version
            if latest_version is None:
                latest_version = python_version
            elif StrictVersion(python_version) > StrictVersion(latest_version):
                latest_version = python_version

        # create sym link to point to latest Python version lib directory
        if platform.system() != 'Windows':
            if os.path.islink(self.static_lib_dir):
                os.unlink(self.static_lib_dir)
            os.symlink('lib_{}'.format(latest_version), self.static_lib_dir)

        # cleanup temp file if required
        if self.requirements_temp:
            os.remove(self.requirements_file)
