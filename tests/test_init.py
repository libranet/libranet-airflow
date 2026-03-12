# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module libranet_airflow.__init__."""

import packaging.version


def test_version() -> None:
    from libranet_airflow import __version__

    assert isinstance(__version__, str)
    assert packaging.version.parse(__version__) >= packaging.version.parse("0.0")


def test_license() -> None:
    import libranet_airflow
    # from libranet_airflow import __license__

    assert isinstance(libranet_airflow.__license__, str)
    assert "Copyright" in libranet_airflow.__license__
