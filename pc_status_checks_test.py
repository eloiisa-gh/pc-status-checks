from unittest.mock import patch
from pc_status_checks import *


def test_check_reboot_exists():
    """Test that check_reboot returns True if the reboot-required file exists."""
    with patch("os.path.exists", return_value=True):
        assert check_reboot() is True


def test_check_reboot_not_exists():
    """Test that check_reboot returns False if the reboot-required file does not exist."""
    with patch("os.path.exists", return_value=False):
        assert check_reboot() is False


def test_check_root_full():
    """Test that check_root_full returns True if the root partition is considered full."""
    with patch("pc_health_checks.check_disk_full", return_value=True):
        assert check_root_full() is True


def test_check_root_full_not_full():
    """Test that check_root_full returns False if the root partition is not considered full."""
    with patch("pc_health_checks.check_disk_full", return_value=False):
        assert check_root_full() is False


def test_check_cpu_constrained_high_usage():
    """Test that check_cpu_constrained returns True if CPU usage is above the 75% threshold."""
    with patch("psutil.cpu_percent", return_value=80):
        assert check_cpu_constrained() is True


def test_check_cpu_constrained_low_usage():
    """Test that check_cpu_constrained returns False if CPU usage is below the 75% threshold."""
    with patch("psutil.cpu_percent", return_value=70):
        assert check_cpu_constrained() is False


def test_check_no_network_success():
    """Test that check_no_network returns False if network resolution is successful."""
    with patch("socket.gethostbyname", return_value="8.8.8.8"):
        assert check_no_network() is False


def test_check_no_network_failure():
    """Test that check_no_network returns True if network resolution fails."""
    with patch("socket.gethostbyname", side_effect=socket.gaierror):
        assert check_no_network() is True
