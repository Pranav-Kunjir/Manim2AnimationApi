from manim import *

class InputAndButtonAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Input Field
        input_field = RoundedRectangle(
            width=6,
            height=0.75,
            corner_radius=0.2,
            stroke_color=WHITE,
            fill_color="#444444",
            fill_opacity=1,
            stroke_width=2,
        ).move_to(UP * 1)
        
        # Animate Button
        animate_button_rect = RoundedRectangle(
            width=2,
            height=0.6,
            corner_radius=0.3,
            stroke_color=WHITE,
            fill_color="#555555",
            fill_opacity=1,
            stroke_width=2,
        ).move_to(DOWN * 0.5)
        
        animate_button_text = Text(
            "Animate",
            font_size=24,
            color=WHITE,
        ).move_to(animate_button_rect.get_center())
        
        animate_button = VGroup(animate_button_rect, animate_button_text)
        
        # Typing animation
        input_text = "Create an animation for f(x) = x^2"
        typed_text = VGroup()
        
        for i, letter in enumerate(input_text):
            letter_mob = Text(
                letter,
                font_size=24,
                color=WHITE,
            ).move_to(input_field.get_center()).shift(RIGHT * i * 0.15 - RIGHT * len(input_text) * 0.075)
            typed_text.add(letter_mob)
        
        # Add input field and button first
        self.add(input_field, animate_button)
        
        # Animate typing
        self.play(
            LaggedStart(
                *[Write(letter) for letter in typed_text],
                lag_ratio=0.1
            ),
            run_time=2
        )
        
        # Button press animation
        self.play(
            animate_button_rect.animate.set_fill("#888888"),
            animate_button_text.animate.scale(0.9),
            run_time=0.2
        )
        self.play(
            animate_button_rect.animate.set_fill("#555555"),
            animate_button_text.animate.scale(1/0.9),
            run_time=0.2
        )
        
        self.wait(1)
        
        # Mouse cursor animation (using Polygon instead of SVG)
        mouse_cursor = Polygon(
            ORIGIN, RIGHT*0.5, UP*0.25,
            fill_color=WHITE, fill_opacity=1,
            stroke_color=WHITE
        ).scale(0.5).move_to(UP * 3 + LEFT * 5)
        
        self.play(
            mouse_cursor.animate.shift(RIGHT * 5 + DOWN * 3.5),
            run_time=2
        )
        
        self.play(
            mouse_cursor.animate.shift(RIGHT * 0.1 + UP * 0.1),
            animate_button_rect.animate.set_fill("#888888"),
            animate_button_text.animate.scale(0.9),
            run_time=0.1
        )
        self.play(
            mouse_cursor.animate.shift(LEFT * 0.1 + DOWN * 0.1),
            animate_button_rect.animate.set_fill("#555555"),
            animate_button_text.animate.scale(1/0.9),
            run_time=0.1
        )
        
        self.wait(2)