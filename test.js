const pythonCode = `python
from manim import *

class TypingAnimation(Scene):
    def construct(self):
        # Key parameters
        key_width = 1
        key_height = 0.75
        key_color = GRAY
        key_stroke_color = WHITE
        key_stroke_width = 2
        font_size = 36

        # Create keys
        super_key = Rectangle(width=key_width * 1.5, height=key_height, fill_color=key_color, fill_opacity=1, stroke_color=key_stroke_color, stroke_width=key_stroke_width)
        q_key = Rectangle(width=key_width, height=key_height, fill_color=key_color, fill_opacity=1, stroke_color=key_stroke_color, stroke_width=key_stroke_width)

        super_label = Text("Super", font_size=24).move_to(super_key.get_center())
        q_label = Text("q", font_size=24).move_to(q_key.get_center())

        super_group = VGroup(super_key, super_label).move_to(LEFT * 2)
        q_group = VGroup(q_key, q_label).move_to(RIGHT * 2)

        # Command text
        command_text = Text("", font_size=font_size).to_edge(UP)

        # Press key animation
        def press_key(key_group, command, duration=0.2):
            offset = DOWN * 0.15
            
            press = AnimationGroup(
                key_group.animate.shift(offset),
                UpdateFromFunc(command_text, lambda mob: mob.become(Text(command, font_size=font_size).to_edge(UP))),
                run_time=duration / 2
            )
            
            release = AnimationGroup(
                key_group.animate.shift(-offset),
                run_time=duration / 2
            )
            
            return Succession(press, release)

        # Animation sequence
        self.play(Create(super_group), Create(q_group), Write(command_text))
        self.wait(0.5)

        self.play(press_key(super_group, "super"))
        self.wait(0.2)
        self.play(press_key(q_group, "super + q"))

        self.wait(1)
        self.play(FadeOut(super_group, q_group, command_text))
        self.wait(0.5)
        `;



const jsonCompatibleString = JSON.stringify(pythonCode);

console.log(jsonCompatibleString);

