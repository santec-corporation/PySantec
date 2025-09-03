# pysantec/tests/test_list_resources.py

"""
Test list resources functionality.
"""

import pytest
import pysantec


@pytest.fixture(scope="module")
def instrument_manager():
    """Fixture to create an InstrumentManager instance."""
    return pysantec.InstrumentManager()


def test_list_resources(instrument_manager):
    """Test the list_resources function."""
    resources = instrument_manager.list_resources()
    assert len(resources) > 0
    assert isinstance(resources, list)
    assert all(isinstance(resource, str) for resource in resources)
