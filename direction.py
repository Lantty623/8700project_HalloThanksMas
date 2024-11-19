class GameDirection:

    def __init__(self, title, point_guide, objective, control, title_color, images):
        self.title = title
        self.point_guide = point_guide
        self.objective = objective
        self.control = control
        self.title_color = title_color
        self.images = images

    def get_directions(self):

        return (
            f"{self.title}\n\n"
            f"Point Guide:\n{self.point_guide}\n\n"
            f"Objective:\n{self.objective}\n\n"
            f"Control:\n{self.control}"
        )


class HalloweenDirection(GameDirection):
    def __init__(self):
        super().__init__(
            title="Halloween: Trick-or-Treating",
            point_guide=[
                ("assets/images/candy.png", "+100 points"),
                ("assets/images/ghost.png", "-50 points")
            ],
            objective="Collect as many candies as you can while avoiding ghosts!",
            control="Use the Left and Right arrow keys to move. Press 'P' to pause and press 'P' again to continue",
            title_color="purple",
            images=["assets/images/candy.png", "assets/images/ghost.png"]
        )


class ThanksgivingDirection(GameDirection):
    def __init__(self):
        super().__init__(
            title="Thanksgiving: Harvesting Festival",
            point_guide=[
                ("assets/images/turkey.png", "+100 points"),
                ("assets/images/pie.png", "+50 points"),
                ("assets/images/mash.png", "+150 points")
            ],
            objective="Complete food sets by collecting required items.",
            control="Use the Left and Right arrow keys to move. Press 'P' to pause and press 'P' again to continue",
            title_color="orange",
            images=["assets/images/turkey.png", "assets/images/pie.png", "assets/images/mash.png"]
        )


class ChristmasDirection(GameDirection):
    def __init__(self):
        super().__init__(
            title="Christmas: Santa's Present",
            point_guide=[
                ("assets/images/present.png", "+100 points"),
                ("assets/images/snowball.png", "-50 points"),
                ("assets/images/snowman.png", "Freezes you for 5 seconds")
            ],
            objective="Catch presents while avoiding snowballs and snowmen.",
            control="Use the Left and Right arrow keys to move. Press 'P' to pause and press 'P' again to continue",
            title_color="green",
            images=["assets/images/present.png", "assets/images/snowball.png", "assets/images/snowman.png"]
        )

# Factory method for creating game directions.
class GameDirectionFactory:

    @staticmethod
    def create_direction(level_name):
        if level_name == "Trick-or-treating":
            return HalloweenDirection()
        elif level_name == "Harvesting Festival":
            return ThanksgivingDirection()
        elif level_name == "Santa's Present":
            return ChristmasDirection()
        else:
            raise ValueError(f"Unknown level name: {level_name}")
