#!/usr/bin/env python3

# This script tests that humanity launches humanity-keyd automatically when humanity-keyd is not
# running yet.

import subprocess


def run_humanity_wallet_command(command: str, no_auto_humanity_keyd: bool):
    """Run the given humanity command and return subprocess.CompletedProcess."""
    args = ['./programs/humanity/humanity']

    if no_auto_humanity_keyd:
        args.append('--no-auto-humanity-keyd')

    args += 'wallet', command

    return subprocess.run(args,
                          check=False,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.PIPE)


def stop_humanity_keyd():
    """Stop the default humanity-keyd instance."""
    run_humanity_wallet_command('stop', no_auto_humanity_keyd=True)


def check_humanity_stderr(stderr: bytes, expected_match: bytes):
    if expected_match not in stderr:
        raise RuntimeError("'{}' not found in {}'".format(
            expected_match.decode(), stderr.decode()))


def humanity_keyd_auto_launch_test():
    """Test that humanity-keyd auto-launching works but can be optionally inhibited."""
    stop_humanity_keyd()

    # Make sure that when '--no-auto-humanity-keyd' is given, humanity-keyd is not started by
    # humanity.
    completed_process = run_humanity_wallet_command('list', no_auto_humanity_keyd=True)
    assert completed_process.returncode != 0
    check_humanity_stderr(completed_process.stderr, b'Failed http request to humanity-keyd')

    # Verify that humanity-keyd auto-launching works.
    completed_process = run_humanity_wallet_command('list', no_auto_humanity_keyd=False)
    if completed_process.returncode != 0:
        raise RuntimeError("Expected that humanity-keyd would be started, "
                           "but got an error instead: {}".format(
                               completed_process.stderr.decode()))
    check_humanity_stderr(completed_process.stderr, b'launched')


try:
    humanity_keyd_auto_launch_test()
finally:
    stop_humanity_keyd()
