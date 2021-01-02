class Character:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def take_damage(self, points: int):
        """
        Inflict damage on the Character.

        Args:
            points: The amount of hp damage to deal to the Character.

        """
        self.hp = max(0, self.hp - points)

    def heal(self, points: int):
        """
        Heals the Character.

        Args:
            points: The amount of hp points to restore to the Character.

        """
        self.hp = min(self.hp + points, self.max_hp)

    def is_alive(self) -> bool:
        """
        Checks whether the Character is alive.

        Returns:
            True if the Character is alive, False otherwise.

        """
        return self.hp > 0
