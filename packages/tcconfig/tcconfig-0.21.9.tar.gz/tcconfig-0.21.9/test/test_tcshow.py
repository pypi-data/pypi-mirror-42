# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
import simplejson as json
from subprocrunner import SubprocessRunner

from tcconfig._const import Tc

from .common import execute_tcdel, print_test_result


@pytest.fixture
def device_value(request):
    return request.config.getoption("--device")


class Test_tcshow(object):
    """
    Tests in this class are not executable on CI services.
    Execute the following command at the local environment to running tests:

        python setup.py test --addopts "--runxfail --device=<test device>"
    """

    @pytest.mark.parametrize(["colorize_option"], [[""], ["--color"]])
    def test_normal_empty(self, device_value, colorize_option):
        if device_value is None:
            pytest.skip("device option is null")

        for tc_target in [device_value, "--device {}".format(device_value)]:
            execute_tcdel(tc_target)

            runner = SubprocessRunner(" ".join([Tc.Command.TCSHOW, tc_target, colorize_option]))

            expected = (
                "{"
                + '"{:s}"'.format(device_value)
                + ": {"
                + """
                        "outgoing": {
                        },
                        "incoming": {
                        }
                    }
                }"""
            )
            print_test_result(expected=expected, actual=runner.stdout, error=runner.stderr)

            assert runner.run() == 0
            assert json.loads(runner.stdout) == json.loads(expected)

    @pytest.mark.parametrize(["colorize_option"], [[""], ["--color"]])
    def test_normal_ipv4(self, device_value, colorize_option):
        if device_value is None:
            pytest.skip("device option is null")

        for tc_target in [device_value, "--device {}".format(device_value)]:
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "10",
                            "--delay-distro",
                            "2",
                            "--loss",
                            "0.01",
                            "--duplicate",
                            "0.5",
                            "--reorder",
                            "0.2",
                            "--rate",
                            "0.25K",
                            "--network",
                            "192.168.0.10",
                            "--port",
                            "8080",
                            "--overwrite",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "1",
                            "--loss",
                            "1",
                            "--rate",
                            "100M",
                            "--network",
                            "192.168.1.0/24",
                            "--add",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "10",
                            "--delay-distro",
                            "2",
                            "--rate",
                            "500K",
                            "--direction",
                            "incoming",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "1",
                            "--loss",
                            "0.02",
                            "--duplicate",
                            "0.5",
                            "--reorder",
                            "0.2",
                            "--rate",
                            "0.1M",
                            "--network",
                            "192.168.11.0/24",
                            "--port",
                            "80",
                            "--direction",
                            "incoming",
                            "--add",
                        ]
                    )
                ).run()
                == 0
            )

            runner = SubprocessRunner(" ".join([Tc.Command.TCSHOW, tc_target, colorize_option]))
            runner.run()

            expected = (
                "{"
                + '"{:s}"'.format(device_value)
                + ": {"
                + """
                        "outgoing": {
                        "dst-network=192.168.0.10/32, dst-port=8080, protocol=ip": {
                                "filter_id": "800::800",
                                "delay": "10.0ms",
                                "loss": "0.01%",
                                "duplicate": "0.5%",
                                "reorder": "0.2%",
                                "rate": "248bps",
                                "delay-distro": "2.0ms"
                            },
                            "dst-network=192.168.1.0/24, protocol=ip": {
                                "filter_id": "800::801",
                                "delay": "1.0ms",
                                "loss": "1%",
                                "rate": "100Mbps"
                            }
                        },
                        "incoming": {
                            "dst-network=192.168.11.0/24, dst-port=80, protocol=ip": {
                                "filter_id": "800::801",
                                "delay": "1.0ms",
                                "loss": "0.02%",
                                "duplicate": "0.5%",
                                "reorder": "0.2%",
                                "rate": "100Kbps"
                            },
                            "protocol=ip": {
                                "filter_id": "800::800",
                                "delay": "10.0ms",
                                "delay-distro": "2.0ms",
                                "rate": "500Kbps"
                            }
                        }
                    }
                }"""
            )

            print_test_result(expected=expected, actual=runner.stdout, error=runner.stderr)

            assert json.loads(runner.stdout) == json.loads(expected)

            execute_tcdel(tc_target)

    @pytest.mark.parametrize(["colorize_option"], [[""], ["--color"]])
    def test_normal_ipv6(self, device_value, colorize_option):
        if device_value is None:
            pytest.skip("device option is null")

        for tc_target in [device_value, "--device {}".format(device_value)]:
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "10",
                            "--delay-distro",
                            "2",
                            "--loss",
                            "0.01",
                            "--duplicate",
                            "5",
                            "--reorder",
                            "2",
                            "--rate",
                            "0.25K",
                            "--network",
                            "::1",
                            "--port",
                            "8080",
                            "--overwrite",
                            "--ipv6",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "1",
                            "--loss",
                            "1",
                            "--rate",
                            "100M",
                            "--network",
                            "2001:db00::0/24",
                            "--add",
                            "--ipv6",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "10",
                            "--delay-distro",
                            "2",
                            "--rate",
                            "500K",
                            "--direction",
                            "incoming",
                            "--ipv6",
                        ]
                    )
                ).run()
                == 0
            )
            assert (
                SubprocessRunner(
                    " ".join(
                        [
                            Tc.Command.TCSET,
                            tc_target,
                            "--delay",
                            "1",
                            "--loss",
                            "0.02",
                            "--duplicate",
                            "5",
                            "--reorder",
                            "2",
                            "--rate",
                            "0.1M",
                            "--network",
                            "2001:db00::0/25",
                            "--port",
                            "80",
                            "--direction",
                            "incoming",
                            "--add",
                            "--ipv6",
                        ]
                    )
                ).run()
                == 0
            )

            runner = SubprocessRunner(
                " ".join([Tc.Command.TCSHOW, tc_target, "--ipv6", colorize_option])
            )
            runner.run()

            expected = (
                "{"
                + '"{:s}"'.format(device_value)
                + ": {"
                + """
                        "outgoing": {
                            "dst-network=::1/128, dst-port=8080, protocol=ipv6": {
                                "filter_id": "800::800",
                                "delay": "10.0ms",
                                "loss": "0.01%",
                                "duplicate": "5%",
                                "reorder": "2%",
                                "rate": "248bps",
                                "delay-distro": "2.0ms"
                            },
                            "dst-network=2001:db00::/24, protocol=ipv6": {
                                "filter_id": "800::801",
                                "delay": "1.0ms",
                                "loss": "1%",
                                "rate": "100Mbps"
                            }
                        },
                        "incoming": {
                            "dst-network=2001:db00::/25, dst-port=80, protocol=ipv6": {
                                "filter_id": "800::801",
                                "delay": "1.0ms",
                                "loss": "0.02%",
                                "duplicate": "5%",
                                "reorder": "2%",
                                "rate": "100Kbps"
                            },
                            "protocol=ipv6": {
                                "filter_id": "800::800",
                                "delay": "10.0ms",
                                "rate": "500Kbps",
                                "delay-distro": "2.0ms"
                            }
                        }
                    }
                }"""
            )

            print_test_result(expected=expected, actual=runner.stdout, error=runner.stderr)

            assert json.loads(runner.stdout) == json.loads(expected)

            execute_tcdel(tc_target)
