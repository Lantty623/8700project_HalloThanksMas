from abc import ABC, abstractmethod


class GameDirection(ABC):
    """Abstract base class for game directions."""

    @abstractmethod
    def get_directions(self):
        """Provide directions for the game level."""
        pass


class TrickOrTreatingDirection(GameDirection):
    """Directions for the Trick-or-treating level."""

    def get_directions(self):
        return (
            "Welcome to Trick-or-treating!\n\n"
            "Points Guide:\n"
            "- Catch candies to earn points (+100).\n"
            "- Avoid ghosts; they deduct points (-50).\n\n"
            "Objective:\n"
            "Move the pumpkin left or right to catch as many candies as possible "
            "while avoiding ghosts.\n\n"
            "Controls:\n"
            "- Left Arrow: Move left\n"
            "- Right Arrow: Move right\n"
            "- Press 'P' to pause the game."
        )


class HarvestingFestivalDirection(GameDirection):
    """Directions for the Harvesting Festival level."""

    def get_directions(self):
        return (
            "Welcome to Harvesting Festival!\n\n"
            "Points Guide:\n"
            "- Collect items to complete combos and earn points.\n"
            "- Each item has different points:\n"
            "  * Turkey: +100\n"
            "  * Pie: +50\n"
            "  * Mashed Potatoes: +150\n\n"
            "Objective:\n"
            "Complete the required combo sets to maximize your score.\n\n"
            "Controls:\n"
            "- Left Arrow: Move left\n"
            "- Right Arrow: Move right\n"
            "- Press 'P' to pause the game."
        )


class SantasPresentDirection(GameDirection):
    """Directions for the Santa's Present level."""

    def get_directions(self):
        return (
            "Welcome to Santa's Present!\n\n"
            "Points Guide:\n"
            "- Catch presents to earn points (+100).\n"
            "- Avoid snowballs; they deduct points (-50).\n"
            "- Snowmen freeze you temporarily, so avoid them!\n\n"
            "Objective:\n"
            "Move the sleigh left or right to catch as many presents as possible "
            "while avoiding obstacles.\n\n"
            "Controls:\n"
            "- Left Arrow: Move left\n"
            "- Right Arrow: Move right\n"
            "- Press 'P' to pause the game."
        )


class GameDirectionFactory:
    """Factory for creating game direction instances."""

    @staticmethod
    def create_direction(level_name):
        """Create a direction instance based on the level name."""
        directions_map = {
            "Trick-or-treating": TrickOrTreatingDirection,
            "Harvesting Festival": HarvestingFestivalDirection,
            "Santa's Present": SantasPresentDirection,
        }
        direction_class = directions_map.get(level_name)
        if direction_class:
            return direction_class()
        else:
            raise ValueError(f"No directions available for level: {level_name}")
