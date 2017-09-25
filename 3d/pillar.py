"""
This script defines a micromouse maze pillar.
"""
import cadquery
from Helpers import show


HEIGHT = 50.
WIDTH = 12.
HOLE_DIAMETER = 6.
HOLE_DEPTH = 21.
GROOVE_WIDTH = 4.3
GROOVE_DEPTH = 2.5
GROOVE_LENGTH = 26.


# Pillar body
pillar = cadquery.Workplane('XY')\
    .box(WIDTH, WIDTH, HEIGHT)\
    .faces('<Z').workplane()\
    .hole(diameter=HOLE_DIAMETER, depth=HOLE_DEPTH)

# Grooves
aux = WIDTH / 2. - GROOVE_DEPTH / 2.
pillar = pillar.faces('>Z').workplane()\
    .pushPoints([(aux, 0), (-aux, 0)]).rect(GROOVE_DEPTH, GROOVE_WIDTH)\
    .cutBlind(-GROOVE_LENGTH)
pillar = pillar.faces('>Z').workplane()\
    .pushPoints([(0, aux), (0, -aux)]).rect(GROOVE_WIDTH, GROOVE_DEPTH)\
    .cutBlind(-GROOVE_LENGTH)

show(pillar)
