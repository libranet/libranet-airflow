"""Tests for libranet_airflow.logging."""

import logging as std_logging

from libranet_airflow import logging


def test_initialize(capsys) -> None:
    """Test that initialize configures logging and log output works."""
    logging.initialize()

    logger = std_logging.getLogger("libranet_airflow")
    logger.info("test message")

    captured = capsys.readouterr()
    assert "test message" in captured.out
