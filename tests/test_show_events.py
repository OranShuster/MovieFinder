import pytest
from click.testing import CliRunner
from main import actions


# noinspection PyMethodMayBeStatic
class ShowEventsTests:
    def test_show_events_no_args(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events"])
        assert result.exit_code == 0

    def test_show_events_today(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "today"])
        assert result.exit_code == 0

    def test_show_events_tomorrow(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "tomorrow"])
        assert result.exit_code == 0

    def test_show_events_bad_arg_str(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "blabla"])
        assert isinstance(result.exception, AssertionError)
        assert result.exit_code == 1

    def test_show_events_plus_0(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "+0"])
        assert result.exit_code == 0

    def test_show_events_plus_1(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "+1"])
        assert result.exit_code == 0

    def test_show_events_0(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "0"])
        assert result.exit_code == 0

    def test_show_events_1(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "1"])
        assert result.exit_code == 0

    def test_show_events_minus_1(self):
        runner = CliRunner()
        result = runner.invoke(actions, ["show-events", "--", "-1"])
        assert isinstance(result.exception, AssertionError)
        assert result.exit_code == 1


@pytest.fixture()
def mock_no_adapters(mocker):
    mocker.patch("settings.adapters")
    pass


@pytest.fixture()
def verify_no_query(mocker):
    mocked_requests = mocker.patch("requests.get")
    yield
    assert mocked_requests.call_count == 0


@pytest.mark.usefixtures(*["mock_no_adapters", "verify_no_query"])
class TestShowEventsNoAdapters(ShowEventsTests):
    pass


@pytest.mark.slow
class TestShowEvents(ShowEventsTests):
    pass
