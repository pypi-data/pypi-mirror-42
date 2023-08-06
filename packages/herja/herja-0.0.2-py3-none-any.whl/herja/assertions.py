"""A collection of assertions."""


def assert_type(item, *item_types):
    """Assert the given item is a particular type."""
    assert isinstance(item, item_types), 'Item type {0} not in types: {1}'.format(type(item), item_types)
