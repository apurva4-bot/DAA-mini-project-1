import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import random


class InsertionSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Insertion Sort Step-by-Step Visualizer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Data
        self.original_array = [64, 34, 25, 12, 22, 11, 90, 88]
        self.array = self.original_array.copy()
        self.steps = []
        self.current_step = 0
        self.sorting_active = False
        self.auto_play = False
        self.speed = 1.0

        # Colors
        self.colors = {
            'unsorted': '#E3F2FD',
            'sorted': '#4CAF50',
            'current': '#FF9800',
            'comparing': '#F44336',
            'inserting': '#9C27B0',
            'background': '#f0f0f0',
            'text': '#333333'
        }

        self.setup_ui()
        self.generate_steps()
        self.display_current_step()

    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, pady=(10, 0))

        title_label = tk.Label(title_frame, text="Insertion Sort Visualizer",
                               font=('Arial', 20, 'bold'),
                               bg=self.colors['background'],
                               fg=self.colors['text'])
        title_label.pack()

        subtitle_label = tk.Label(title_frame,
                                  text="Watch how insertion sort builds the sorted array one element at a time",
                                  font=('Arial', 11),
                                  bg=self.colors['background'],
                                  fg='#666666')
        subtitle_label.pack()

        # Control panel
        control_frame = tk.LabelFrame(self.root, text="Controls",
                                      font=('Arial', 12, 'bold'),
                                      bg=self.colors['background'],
                                      padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        # Input controls
        input_frame = tk.Frame(control_frame, bg=self.colors['background'])
        input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(input_frame, text="Array:", font=('Arial', 10, 'bold'),
                 bg=self.colors['background']).pack(side=tk.LEFT, padx=(0, 5))

        self.array_entry = tk.Entry(input_frame, font=('Arial', 10), width=40)
        self.array_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.array_entry.insert(0, ' '.join(map(str, self.original_array)))

        tk.Button(input_frame, text="Set Array", command=self.set_custom_array,
                  bg='#2196F3', fg='black', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(input_frame, text="Random Array", command=self.generate_random_array,
                  bg='#FF9800', fg='black', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(input_frame, text="Reset", command=self.reset_visualization,
                  bg='#F44336', fg='black', font=('Arial', 9, 'bold')).pack(side=tk.LEFT)

        # Playback controls
        playback_frame = tk.Frame(control_frame, bg=self.colors['background'])
        playback_frame.pack(fill=tk.X)

        tk.Button(playback_frame, text="◀◀ First", command=self.first_step,
                  bg='#607D8B', fg='black', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(playback_frame, text="◀ Previous", command=self.previous_step,
                  bg='#607D8B', fg='black', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 5))

        self.play_button = tk.Button(playback_frame, text="▶ Play", command=self.toggle_auto_play,
                                     bg='black', fg='black', font=('Arial', 9, 'bold'))
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(playback_frame, text="Next ▶", command=self.next_step,
                  bg='#607D8B', fg='black', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(playback_frame, text="Last ▶▶", command=self.last_step,
                  bg='#607D8B', fg='black', font=('Arial', 9)).pack(side=tk.LEFT)

        # Speed control
        speed_frame = tk.Frame(playback_frame, bg=self.colors['background'])
        speed_frame.pack(side=tk.RIGHT)

        tk.Label(speed_frame, text="Speed:", font=('Arial', 10),
                 bg=self.colors['background']).pack(side=tk.LEFT, padx=(10, 5))

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(speed_frame, from_=0.2, to=3.0, resolution=0.1,
                               orient=tk.HORIZONTAL, variable=self.speed_var,
                               bg=self.colors['background'], length=100)
        speed_scale.pack(side=tk.LEFT)
        speed_scale.bind("<Motion>", self.update_speed)

        # Main visualization area
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Array visualization
        self.viz_frame = tk.LabelFrame(main_frame, text="Array Visualization",
                                       font=('Arial', 12, 'bold'),
                                       bg=self.colors['background'])
        self.viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Step information
        info_frame = tk.Frame(main_frame, bg=self.colors['background'])
        info_frame.pack(fill=tk.X)

        # Step counter and description
        step_info_frame = tk.LabelFrame(info_frame, text="Step Information",
                                        font=('Arial', 12, 'bold'),
                                        bg=self.colors['background'])
        step_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.step_label = tk.Label(step_info_frame, text="", font=('Arial', 11),
                                   bg=self.colors['background'], fg=self.colors['text'],
                                   justify=tk.LEFT, wraplength=400)
        self.step_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Statistics
        stats_frame = tk.LabelFrame(info_frame, text="Statistics",
                                    font=('Arial', 12, 'bold'),
                                    bg=self.colors['background'])
        stats_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_label = tk.Label(stats_frame, text="", font=('Arial', 10),
                                    bg=self.colors['background'], fg=self.colors['text'],
                                    justify=tk.LEFT)
        self.stats_label.pack(padx=10, pady=10)

        # Progress bar
        progress_frame = tk.Frame(self.root, bg=self.colors['background'])
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(progress_frame, text="Progress:", font=('Arial', 10),
                 bg=self.colors['background']).pack(side=tk.LEFT)

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                            maximum=100, length=300)
        self.progress_bar.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        self.progress_label = tk.Label(progress_frame, text="0/0", font=('Arial', 10),
                                       bg=self.colors['background'])
        self.progress_label.pack(side=tk.RIGHT, padx=(10, 0))

    def set_custom_array(self):
        """Set custom array from user input"""
        try:
            array_str = self.array_entry.get().strip()
            if array_str:
                new_array = list(map(int, array_str.split()))
                if len(new_array) > 20:
                    messagebox.showwarning("Warning", "Array too large! Using first 20 elements.")
                    new_array = new_array[:20]
                elif len(new_array) < 2:
                    messagebox.showwarning("Warning", "Array too small! Need at least 2 elements.")
                    return

                self.original_array = new_array
                self.reset_visualization()
            else:
                messagebox.showwarning("Warning", "Please enter array elements separated by spaces.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter integers separated by spaces.")

    def generate_random_array(self):
        """Generate a random array"""
        size = random.randint(5, 12)
        self.original_array = [random.randint(1, 99) for _ in range(size)]
        self.array_entry.delete(0, tk.END)
        self.array_entry.insert(0, ' '.join(map(str, self.original_array)))
        self.reset_visualization()

    def reset_visualization(self):
        """Reset the visualization to initial state"""
        self.array = self.original_array.copy()
        self.current_step = 0
        self.auto_play = False
        self.play_button.config(text="▶ Play")
        self.generate_steps()
        self.display_current_step()

    def update_speed(self, event):
        """Update animation speed"""
        self.speed = self.speed_var.get()

    def generate_steps(self):
        """Generate all steps for insertion sort"""
        self.steps = []
        arr = self.original_array.copy()
        n = len(arr)

        # Initial state
        self.steps.append({
            'array': arr.copy(),
            'description': "Initial unsorted array",
            'current_element': -1,
            'sorted_part': 0,
            'comparing_with': -1,
            'action': 'start',
            'comparisons': 0,
            'movements': 0
        })

        comparisons = 0
        movements = 0

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            # Show current element being inserted
            self.steps.append({
                'array': arr.copy(),
                'description': f"Step {i}: Select element {key} at index {i} to insert into sorted portion",
                'current_element': i,
                'sorted_part': i,
                'comparing_with': -1,
                'action': 'select',
                'comparisons': comparisons,
                'movements': movements
            })

            # Find correct position
            while j >= 0:
                comparisons += 1

                # Show comparison
                self.steps.append({
                    'array': arr.copy(),
                    'description': f"Compare {key} with {arr[j]} at index {j}",
                    'current_element': i,
                    'sorted_part': i,
                    'comparing_with': j,
                    'action': 'compare',
                    'comparisons': comparisons,
                    'movements': movements
                })

                if arr[j] > key:
                    # Show shift
                    self.steps.append({
                        'array': arr.copy(),
                        'description': f"{arr[j]} > {key}, so shift {arr[j]} one position right",
                        'current_element': i,
                        'sorted_part': i,
                        'comparing_with': j,
                        'action': 'shift',
                        'comparisons': comparisons,
                        'movements': movements
                    })

                    arr[j + 1] = arr[j]
                    movements += 1

                    # Show after shift
                    self.steps.append({
                        'array': arr.copy(),
                        'description': f"Array after shifting: {arr}",
                        'current_element': i,
                        'sorted_part': i,
                        'comparing_with': j,
                        'action': 'shifted',
                        'comparisons': comparisons,
                        'movements': movements
                    })

                    j -= 1
                else:
                    self.steps.append({
                        'array': arr.copy(),
                        'description': f"{arr[j]} ≤ {key}, found correct position at index {j + 1}",
                        'current_element': i,
                        'sorted_part': i,
                        'comparing_with': j,
                        'action': 'found_position',
                        'comparisons': comparisons,
                        'movements': movements
                    })
                    break

            # Insert element
            arr[j + 1] = key
            movements += 1

            self.steps.append({
                'array': arr.copy(),
                'description': f"Insert {key} at position {j + 1}. Sorted portion now: {arr[:i + 1]}",
                'current_element': j + 1,
                'sorted_part': i + 1,
                'comparing_with': -1,
                'action': 'insert',
                'comparisons': comparisons,
                'movements': movements
            })

        # Final state
        self.steps.append({
            'array': arr.copy(),
            'description': f"Sorting complete! Final sorted array: {arr}",
            'current_element': -1,
            'sorted_part': len(arr),
            'comparing_with': -1,
            'action': 'complete',
            'comparisons': comparisons,
            'movements': movements
        })

    def display_current_step(self):
        """Display the current step"""
        if not self.steps:
            return

        step_data = self.steps[self.current_step]

        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create array visualization
        array_frame = tk.Frame(self.viz_frame, bg=self.colors['background'])
        array_frame.pack(expand=True)

        # Array elements
        elements_frame = tk.Frame(array_frame, bg=self.colors['background'])
        elements_frame.pack(pady=20)

        for i, value in enumerate(step_data['array']):
            # Determine color
            if step_data['action'] == 'complete':
                color = self.colors['sorted']
            elif i < step_data['sorted_part']:
                color = self.colors['sorted']
            elif i == step_data['current_element']:
                color = self.colors['current']
            elif i == step_data['comparing_with']:
                color = self.colors['comparing']
            else:
                color = self.colors['unsorted']

            # Create element frame
            element_frame = tk.Frame(elements_frame, bg=color, relief=tk.RAISED, bd=2)
            element_frame.pack(side=tk.LEFT, padx=3, pady=5)

            # Value label
            value_label = tk.Label(element_frame, text=str(value),
                                   font=('Arial', 14, 'bold'),
                                   bg=color, fg='white' if color != self.colors['unsorted'] else 'black',
                                   width=4, height=2)
            value_label.pack()

            # Index label
            index_label = tk.Label(element_frame, text=str(i),
                                   font=('Arial', 8),
                                   bg=color, fg='white' if color != self.colors['unsorted'] else 'black')
            index_label.pack()

        # Legend
        legend_frame = tk.Frame(array_frame, bg=self.colors['background'])
        legend_frame.pack(pady=(10, 0))

        legends = [
            ("Sorted", self.colors['sorted']),
            ("Current", self.colors['current']),
            ("Comparing", self.colors['comparing']),
            ("Unsorted", self.colors['unsorted'])
        ]

        for text, color in legends:
            legend_item = tk.Frame(legend_frame, bg=self.colors['background'])
            legend_item.pack(side=tk.LEFT, padx=10)

            color_box = tk.Label(legend_item, bg=color, width=3, height=1, relief=tk.RAISED)
            color_box.pack(side=tk.LEFT, padx=(0, 5))

            tk.Label(legend_item, text=text, font=('Arial', 9),
                     bg=self.colors['background']).pack(side=tk.LEFT)

        # Update step information
        self.step_label.config(text=step_data['description'])

        # Update statistics
        stats_text = f"Comparisons: {step_data['comparisons']}\n"
        stats_text += f"Movements: {step_data['movements']}\n"
        stats_text += f"Current Step: {self.current_step + 1}/{len(self.steps)}"
        self.stats_label.config(text=stats_text)

        # Update progress
        progress = int((self.current_step / (len(self.steps) - 1)) * 100) if len(self.steps) > 1 else 0
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{self.current_step + 1}/{len(self.steps)}")

    def first_step(self):
        """Go to first step"""
        self.current_step = 0
        self.display_current_step()

    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.display_current_step()

    def next_step(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_current_step()
            return True
        return False

    def last_step(self):
        """Go to last step"""
        self.current_step = len(self.steps) - 1
        self.display_current_step()

    def toggle_auto_play(self):
        """Toggle auto play mode"""
        self.auto_play = not self.auto_play

        if self.auto_play:
            self.play_button.config(text="⏸ Pause")
            self.start_auto_play()
        else:
            self.play_button.config(text="▶ Play")

    def start_auto_play(self):
        """Start auto play in separate thread"""

        def auto_play_thread():
            while self.auto_play and self.current_step < len(self.steps) - 1:
                time.sleep(1.0 / self.speed)
                if self.auto_play:  # Check again in case it was stopped
                    self.root.after(0, self.next_step)

            # Auto play finished
            self.root.after(0, lambda: self.play_button.config(text="▶ Play"))
            self.auto_play = False

        if not self.sorting_active:
            self.sorting_active = True
            thread = threading.Thread(target=auto_play_thread, daemon=True)
            thread.start()


def main():
    """Main function to run the visualizer"""
    root = tk.Tk()
    app = InsertionSortVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()