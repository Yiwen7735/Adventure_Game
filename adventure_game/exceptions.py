class InventoryFullException(Exception):
    pass


class NoSuchExitException(Exception):
    """
    A basic exception type to be raised if the caller tries to travel in
    a direction which does not have a room.

    """
    pass


class WeaponBrokenException(Exception):
    pass
