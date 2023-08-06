from .vector_sprite import VectorSprite
from pygame import Rect

class Rectangle(VectorSprite) :
    def __init__(self, coords, size,
                 visible = True, interactive = True,
                 line_colour = (0, 0, 0, 255),
                 line_width = 1,
                 fill_colour = (255, 255, 255, 255)):
        super(Rectangle, self).__init__(coords, visible, interactive,
                                     line_colour, line_width, fill_colour)
        self.size = (size[0] + line_width, size[1] + line_width)

    def over(self, coords) :
        return self.in_bounds(coords)

    def fill_surface(self) :
        super(Rectangle, self).fill_surface()
        if self._fill_colour != None :
            self._surface.fill(self._fill_colour)
        if self._line_width > 0 and self._line_colour != None :
            self._surface.fill(self._line_colour,
                               Rect(0, 0, self.size[0], self._line_width))
            self._surface.fill(self._line_colour,
                               Rect(0, 0, self._line_width, self.size[1]))
            self._surface.fill(self._line_colour,
                               Rect(self.size[0] - self._line_width, 0,
                                    self._line_width, self.size[1]))
            self._surface.fill(self._line_colour,
                               Rect(0, self.size[1] - self._line_width,
                                    self.size[0], self._line_width))
