from manim import *

class InsertionSortAnimation(Scene):
    def construct(self):
        # 1. Initialize an array of 5 elements
        array_data = [5, 2, 4, 6, 1]
        colors = [BLUE_D, GREEN_D, YELLOW_D, ORANGE, PURPLE_D]

        # Create a VGroup for each element (rectangle + number)
        elements = [
            VGroup(
                Rectangle(width=1.2, height=1.2, color=color, fill_color=color, fill_opacity=0.7),
                Text(str(val), font="Sans")
            )
            for val, color in zip(array_data, colors)
        ]
        
        # Group them all for initial arrangement and display
        elements_group = VGroup(*elements).arrange(RIGHT, buff=0.5)
        
        # Create and position indices
        indices = VGroup(*[Text(str(i), font="Sans", font_size=36) for i in range(len(array_data))])
        indices.arrange(RIGHT, buff=1.3).next_to(elements_group, DOWN, buff=0.4)
        
        # Title for the animation
        title = Text("Insertion Sort Algorithm", font_size=48, color=WHITE)
        title.to_edge(UP)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(elements_group, shift=UP), run_time=1)
        self.play(Write(indices), run_time=1)
        self.wait(0.5)
        
        # Store original positions for reference
        original_positions = [el.get_center() for el in elements]

        # Insertion Sort Algorithm
        for i in range(1, len(array_data)):
            key_val = array_data[i]
            key_group = elements[i]
            
            # Show current step indicator
            step_text = Text(f"Step {i}: Insert element {key_val} into sorted portion", 
                           font_size=36, color=YELLOW)
            step_text.to_edge(UP, buff=0.1)
            self.play(Write(step_text), run_time=0.5)
            
            j = i - 1
            
            # Animate lifting the key element to be sorted
            self.play(key_group.animate.shift(UP * 2), run_time=0.8)
            self.wait(0.3)

            hole_index = i

            # Inner loop for comparison and shifting
            while j >= 0 and key_val < array_data[j]:
                compare_group = elements[j]
                
                # Highlight elements being compared
                self.play(
                    key_group[0].animate.scale(1.1).set_fill(opacity=1.0),
                    compare_group[0].animate.scale(1.1).set_fill(opacity=1.0),
                    run_time=0.8
                )
                
                # Display comparison text
                comparison_text = MathTex(f"{key_val}", "<", f"{array_data[j]}", font_size=48)
                comparison_text.move_to(elements_group.get_center() + UP * 3.5)
                self.play(Write(comparison_text), run_time=0.6)
                self.wait(0.5)

                # Animate shifting the element to the right
                target_position = original_positions[j+1]
                self.play(
                    compare_group.animate.move_to(target_position),
                    run_time=1.0
                )
                self.play(FadeOut(comparison_text), run_time=0.3)

                # Unhighlight the compared element
                self.play(
                    key_group[0].animate.scale(1/1.1),
                    compare_group[0].animate.scale(1/1.1).set_fill(opacity=0.7),
                    run_time=0.5
                )
                
                # Update logical data structures for the next iteration
                array_data[j+1] = array_data[j]
                elements[j+1] = compare_group
                hole_index = j
                
                j -= 1
            
            # If no shifts happened, show the non-swap comparison
            if j == i - 1 and j >= 0:
                compare_group = elements[j]
                self.play(
                    key_group[0].animate.scale(1.1).set_fill(opacity=1.0),
                    compare_group[0].animate.scale(1.1).set_fill(opacity=1.0),
                    run_time=0.8
                )
                comparison_text = MathTex(f"{key_val}", "\\ge", f"{array_data[j]}", font_size=48)
                comparison_text.move_to(elements_group.get_center() + UP * 3.5)
                self.play(Write(comparison_text), run_time=0.6)
                self.wait(0.5)
                self.play(FadeOut(comparison_text), run_time=0.3)
                self.play(
                    key_group[0].animate.scale(1/1.1).set_fill(opacity=0.7),
                    compare_group[0].animate.scale(1/1.1).set_fill(opacity=0.7),
                    run_time=0.5
                )
            
            # Animate inserting the key into its correct position
            insert_position = original_positions[hole_index]
            self.play(key_group.animate.move_to(insert_position), run_time=1.0)
            
            # Highlight the moved element with a flash
            self.play(Flash(key_group, color=GREEN, line_length=0.3, num_lines=12, flash_radius=1.0), run_time=0.8)

            # Update the main data structures for the next outer loop iteration
            array_data[hole_index] = key_val
            elements[hole_index] = key_group
            
            self.play(FadeOut(step_text), run_time=0.3)
            self.wait(0.5)

        # Final sorted array highlight
        self.play(
            *[element[0].animate.set_fill(color=GREEN, opacity=0.9) for element in elements],
            run_time=1.5
        )
        
        # Conclude the animation
        final_text = Text("Array sorted using Insertion Sort", font="Sans", color=GREEN_C, font_size=48)
        final_text.next_to(elements_group, DOWN, buff=1.5)
        
        self.play(Write(final_text), run_time=1.2)
        self.wait(2)
        self.play(
            FadeOut(title),
            FadeOut(indices),
            final_text.animate.to_edge(DOWN, buff=0.5),
            run_time=1.0
        )
        self.wait(2)