import manim

class HelloWorldAnimation(manim.Scene):
    def construct(self):
        # 1. Initial Setup
        text = manim.Text(
            "Hello, World!",
            font_size=96,
            color=manim.WHITE
        ).center()

        # 2. Animate "Hello"
        self.play(manim.Write(text[0:5]), run_time=1.5)

        # 3. Animate ", World!"
        self.play(manim.Write(text[5:]), run_time=2)

        # 4. Brief Pause
        self.wait(1)

        # 5. Color Transformation
        self.play(
            text.animate.set_color_by_gradient(manim.BLUE, manim.GREEN),
            run_time=2
        )

        # 6. Final Hold
        self.wait(3)