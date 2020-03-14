#!/usr/bin/env python
"""Ansible Interface"""
import logging
import subprocess  # nosec
from lib.vagrant_exception import VagrantInterfaceException
from lib.vagrant_exception import VagrantParamsException

class Vagrant_Interface(object):
    """Vagrant interface module"""
    _vagrant_command = 'vagrant'

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cmd_output_logger = self._init_cmd_logger()

    def _init_cmd_logger(self):
        # Init streamer
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        stream_handler.setFormatter(formatter)
        # Configure logger
        cmd_output_logger = logging.getLogger(self._vagrant_command)
        cmd_output_logger.propagate = False
        cmd_output_logger.handlers = []
        cmd_output_logger.addHandler(stream_handler)
        cmd_output_logger.setLevel(logging.INFO)
        return cmd_output_logger

    def run(self, params):
        """Execute wrapper command with params (AnsibleParams type)"""
        try:
            cmd_list = params.get_cmd_params(self._vagrant_command)
        except VagrantParamsException as exc:
            self._logger.error(str(exc))
            raise VagrantInterfaceException("Could not get wrapper parameters")
        except AttributeError as exc:
            self._logger.error(str(exc))
            raise VagrantInterfaceException("Could not access to params")
        self._logger.debug("Command formed: %s", cmd_list)
        return self._execute(cmd_list)

    def _execute(self, cmd_list):
        self._logger.info("Command to execute: %s", " ".join(cmd_list))

        popen = self._start_process(cmd_list)
        return_code, stdout, stderr = self._live_output_manage(popen)
        if return_code != 0:
            self._logger.error(
                "Error executing cmd. Exit code: %s. Command: %s",
                return_code, " ".join(cmd_list))
            if len(stderr) > 0:
                self._logger.error("Command stderr: %s", "\n".join(stderr))
        elif len(stderr) > 0:
            self._logger.warning("Command stderr: %s", "\n".join(stderr))

        return return_code, stdout, stderr

    def _start_process(self, cmd_list):
        """Open subprocess"""
        if not isinstance(cmd_list, list) or len(cmd_list) == 0:
            self._logger.error("Command received not valid: %s", cmd_list)
            raise VagrantInterfaceException(
                "Command received not valid: %{0}".format(cmd_list))
        try:
            popen = subprocess.Popen(  # nosec
                cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        except OSError as exc:
            self._logger.error(str(exc))
            raise VagrantInterfaceException(
                "Could not find command to execute: {0}".format(cmd_list[0]))
        return popen

    def _live_output_manage(self, popen):
        stdout = []  # Var with std out
        stderr = []  # Var with std err

        # Print outout while executing
        for stdout_line in iter(popen.stdout.readline, ""):
            self._cmd_output_logger.info(stdout_line.rstrip('\n'))
            self._logger.debug(stdout_line.rstrip('\n'))
            stdout.append(stdout_line.rstrip('\n'))

        for stderr_line in iter(popen.stderr.readline, ""):
            self._cmd_output_logger.error(stderr_line.rstrip('\n'))
            self._logger.error(stderr_line.rstrip('\n'))
            stderr.append(stderr_line.rstrip('\n'))

        popen.stderr.close()
        popen.stdout.close()
        return_code = popen.wait()

        return return_code, stdout, stderr