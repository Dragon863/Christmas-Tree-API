import time
try:
    from rpi_ws281x import PixelStrip, Color
except ImportError:
    PixelStrip = (
        None  # For systems without the rpi_ws281x library i.e. club members' PCs
    )


class TreeBase:
    def __init__(self, num_leds: int = 200, order=["green", "blue", "red"]):
        self.num_leds = num_leds
        self.colors = [(0, 0, 0)] * num_leds
        self.running = True
        self.order = order

    def set_pixel(self, index, color):
        if 0 <= index < self.num_leds:
            self.colors[index] = color

    def set_all_pixels(self, color):
        self.colors = [color] * self.num_leds

    def clear(self):
        self.set_all_pixels((0, 0, 0))

    def show(self):
        raise NotImplementedError("This method must be implemented by subclasses.")


class TreeSimulator(TreeBase):
    def __init__(self, num_leds: int = 200, led_size: int = 10):
        import pygame

        super().__init__(num_leds)
        self.led_size = 10
        self.led_size = led_size
        self.width = (num_leds * led_size) // 2
        self.height = led_size * 2

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tree Effect Simulator")

    @staticmethod
    def color_correction(color):
        r, g, b = color
        corrected_r = int(r * 0.4)
        corrected_g = int(g * 0.8)
        corrected_b = int(b * 0.6)
        return (
            min(255, max(0, corrected_r)),
            min(255, max(0, corrected_g)),
            min(255, max(0, corrected_b)),
        )

    def set_pixel(self, index, color):
        if 0 <= index < self.num_leds:
            self.colors[index] = self.color_correction(color)

    def set_all_pixels(self, color):
        corrected_color = self.color_correction(color)
        self.colors = [corrected_color] * self.num_leds

    def show(self):
        import pygame

        self.screen.fill((0, 0, 0))
        for i, color in enumerate(self.colors):
            x = i * self.led_size % self.width
            y = (i * self.led_size // self.width) * self.led_size
            pygame.draw.rect(
                self.screen, color, (x, y, self.led_size - 2, self.led_size - 2)
            )
        pygame.display.flip()

    def quit(self):
        import pygame

        pygame.quit()
        self.running = False


class TreeAPI(TreeBase):
    def __init__(self, pin: int = 18, num_leds: int = 200, brightness: int = 255):
        super().__init__(num_leds)
        if not PixelStrip:
            raise RuntimeError("rpi_ws281x library is not available.")
        self.strip = PixelStrip(
            num=num_leds,
            pin=pin,
            brightness=brightness,
        )
        self.strip.begin()

    def show(self):
        for i, color in enumerate(self.colors):
            if self.order != ["red", "green", "blue"]:
                r, g, b = color
                if self.order == ["green", "blue", "red"]:
                    self.strip.setPixelColor(i, Color(g, b, r))
                elif self.order == ["blue", "red", "green"]:
                    self.strip.setPixelColor(i, Color(b, r, g))
                elif self.order == ["blue", "green", "red"]:
                    self.strip.setPixelColor(i, Color(b, g, r))
                elif self.order == ["red", "blue", "green"]:
                    self.strip.setPixelColor(i, Color(r, b, g))
                elif self.order == ["green", "red", "blue"]:
                    self.strip.setPixelColor(i, Color(g, r, b))
            else:
                self.strip.setPixelColor(i, Color(*color))
        self.strip.show()

    def quit(self):
        self.clear()
        self.show()
        self.strip.stop()


class Tree:
    def __init__(self, debug=False, **kwargs):
        self.backend = TreeSimulator(**kwargs) if debug else TreeAPI(**kwargs)

    def __getattr__(self, name):
        return getattr(self.backend, name)


# Example usage
if __name__ == "__main__":
    tree = Tree(debug=True, num_leds=200)
    try:
        for i in range(tree.backend.num_leds):
            tree.set_pixel(i, (255, 0, 0))
            tree.show()
            time.sleep(0.05)
        tree.clear()
        tree.show()
    except KeyboardInterrupt:
        tree.backend.running = False
    tree.quit()
