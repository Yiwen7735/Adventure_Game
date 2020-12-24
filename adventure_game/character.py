class Character:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

    def take_damage(self, points: int):
        """
        Inflict damage on the Character.

        Args:
            points: The amount of hp damage to deal to the Character.

        """
        self.hp = max(0, self.hp - points)

    def is_alive(self) -> bool:
        """
        Checks whether the Character is alive.

        Returns:
            True if the Character is alive, False otherwise.

        """
        return self.hp > 0
