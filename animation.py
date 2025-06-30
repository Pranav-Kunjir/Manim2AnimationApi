from manim import *

class MovingCircle(Scene):
    def construct(self):
        config.aspect_ratio = "16:9"
        config.background_color = WHITE * 0.1

        # Define the circle
        circle = Circle(color=BLUE, fill_opacity=0.5, radius=1.0)
        circle.x = 0 # Keep circle centered horizontally relative to final position

        # Calculate the initial off-screen position
        start_x = config["frame_width"]/2 + 1.5
        start_y = 0
        start_point = np.array([start_x, start_y, 0])
        end_point = np.array([0, 0, 0])

        # Create the path for the circle to move along
        path = Line(start_point, end_point)

        # Animate the circle moving in from the right
        self.play(MoveAlongPath(circle, path), run_time=1, rate_func=linear)

        # Pause for 1 second
        self.wait(1)

        # Fade out the circle
        self.play(FadeOut(circle), run_time=1)