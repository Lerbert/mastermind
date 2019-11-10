from enum import Enum

Color = Enum(
    value = "Color",
    names = [
        ("blue", 1),
        ("b", 1),
        ("BLUE", 1),
        ("red", 2),
        ("r", 2),
        ("RED", 2),
        ("green", 3),
        ("g", 3),
        ("GREEN", 3),
        ("yellow", 4),
        ("y", 4),
        ("YELLOW", 4),
    ]
)