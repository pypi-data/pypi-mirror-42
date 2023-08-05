[![travis-ci.com](https://img.shields.io/travis/com/purple-ice/pygame-spritesheet.svg?logo=Travis%20CI)](https://travis-ci.com/purple-ice/pygame-spritesheet)
[![codacy.com](https://img.shields.io/codacy/grade/c8cf539ce0ab47d9adc7ffc3abb04f19.svg?label=code%20quality&logo=Codacy&style=flat)](https://app.codacy.com/project/purple-ice/pygame-spritesheet/dashboard)
[![license](https://img.shields.io/github/license/purple-ice/pygame-spritesheet.svg?logo=Read%20The%20Docs&logoColor=white&style=flat)](https://opensource.org/licenses/MIT)

# pygame-spritesheet

This is a lightweight sprite sheet implementation for pygame.

## Usage

Install `pygame-spritesheet` using pip:

```bash
pip install pygame-spritesheet
```

```python
import pygame
from pygame import Color as Colour
from spritesheet import SpriteSheet, Origin

# load a sprite sheet that has 12 columns and 12 rows of sprites
# with magenta colour key for transparency
sprites = SpriteSheet("sprites.png", columns=12, rows=12, colour_key=Colour(255, 0, 255))

#...

# blit your sprites onto a surface
sprites.blit(surface, sprite_id, position=(x, y), origin=Origin.TopLeft)
```

## Documentation

[As of now, there's none. This package has a single class. Please read docstrings.](spritesheet/__init__.py)

[Please also check out this minimal example.](examples/icons.py)

This might change in the future.
