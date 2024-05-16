
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread
from map import MapFileManager
from traveling_salesman_problem import TSP, SolverStopException
from traveling_salesman_problem import InvalidStartCityError, InvalidMapError, InvalidProvidedValueError

class AppTSP(tk.Tk):
    def __init__(self, map_file_path: str) -> None:
        super().__init__()
        # Set title for the window
        self.title("TSP - Traveling Salsman Problem")

        # Setup protocol for exit
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Setup logic
        with MapFileManager(file_path=map_file_path) as map_file_manager:
            map_file_manager.create_map_from_file()
            complete_map = map_file_manager.get_map()
        self.cities = list(sorted(complete_map.cities, key=lambda city: city.name))
        self.tsp_solver = TSP(complete_map=complete_map, start_city_name="New York")
        self.calc_running = False
        self.calc_thread = None

        # Setup GUI
        self.setup_ui()

        # Some update for safe resiziable
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    # Setup GUI
    def setup_ui(self):
        # Basic settings
        primary_color = "gray50"
        secondary_color = "gray70"
        self.padding_size = 15
        self.config(bg=primary_color)

        # - Left Side

        left_frame = tk.Frame(self, bg=secondary_color)
        left_frame.pack(side=tk.LEFT, padx=(self.padding_size,self.padding_size/2), pady=self.padding_size, fill=tk.Y)

        cities_frame = tk.Frame(left_frame, bg=secondary_color)
        cities_frame.pack(side=tk.TOP, padx=self.padding_size, pady=self.padding_size, fill=tk.X)

        cities_label = tk.Label(cities_frame, text="Cities", font=("Arial", 10, "bold"), bg=secondary_color)
        cities_label.pack(anchor=tk.W)

        self.city_checkbox_values = []
        for city in self.cities:
            city_checkbox_value = tk.BooleanVar()
            city_checkbox = tk.Checkbutton(cities_frame, text=city.name, variable=city_checkbox_value, command=self.update_cities, bg=secondary_color)
            city_checkbox.pack(anchor=tk.W)
            self.city_checkbox_values.append(city_checkbox_value)

        control_frame = tk.Frame(left_frame, bg=secondary_color)
        control_frame.pack(side=tk.BOTTOM, padx=self.padding_size, pady=self.padding_size, fill=tk.X)

        start_city_label = tk.Label(control_frame, text="Start City", font=("Arial", 10, "bold"), bg=secondary_color)
        start_city_label.pack(anchor=tk.W)

        self.start_city_var = tk.StringVar()
        start_city_entry = tk.Entry(control_frame, textvariable=self.start_city_var)
        start_city_entry.pack()
        start_city_entry.insert(tk.END, "New York")
        self.start_city_var.trace_add("write", self.update_cities)

        nn_btn = tk.Button(control_frame, text="Nearest Neighbor")
        nn_btn.config(command = lambda : self.calculate_path(method="nn"))
        nn_btn.pack(fill=tk.X, pady=(self.padding_size, self.padding_size/4))

        bf_btn = tk.Button(control_frame, text="Brute Force")
        bf_btn.config(command = lambda : self.calculate_path(method="bf"))
        bf_btn.pack(fill=tk.X, pady=(self.padding_size/4, self.padding_size))

        population_size_label = tk.Label(control_frame, text="Population Size", font=("Arial", 10, "bold"), bg=secondary_color)
        population_size_label.pack(anchor=tk.W)

        self.population_size_entry = tk.Entry(control_frame)
        self.population_size_entry.pack()
        self.population_size_entry.insert(tk.END, "100")

        generations_label = tk.Label(control_frame, text="Generations", font=("Arial", 10, "bold"), bg=secondary_color)
        generations_label.pack(anchor=tk.W)

        self.generations_entry = tk.Entry(control_frame)
        self.generations_entry.pack()
        self.generations_entry.insert(tk.END, "100")

        mutation_rate_label = tk.Label(control_frame, text="Mutation Rate", font=("Arial", 10, "bold"), bg=secondary_color)
        mutation_rate_label.pack(anchor=tk.W)

        self.mutation_rate_entry = tk.Entry(control_frame)
        self.mutation_rate_entry.pack()
        self.mutation_rate_entry.insert(tk.END, "0.01")

        ga_btn = tk.Button(control_frame, text="Genetic Algorithm")
        ga_btn.config(command = lambda : self.calculate_path(method="ga"))
        ga_btn.pack(fill=tk.X, pady=(self.padding_size,0))

        # - Right Side

        right_frame = tk.Frame(self, bg=secondary_color)
        right_frame.pack(side=tk.RIGHT, padx=(self.padding_size/2,self.padding_size), pady=self.padding_size, expand=True, fill=tk.BOTH)

        self.canvas_x = 800
        self.canvas_y = 500
        self.canvas = tk.Canvas(right_frame, width=self.canvas_x, height=self.canvas_y, highlightthickness=0)
        self.canvas.pack(expand=True, padx=self.padding_size, pady=self.padding_size)
        image = Image.open("bg.jpg").resize((self.canvas_x, self.canvas_y))
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.image = image_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

        self.elapsed_time_label = tk.Label(right_frame, text=f"Elapsed Time: 0.00 seconds", font=("Arial", 13, "bold"), bg=secondary_color)
        self.elapsed_time_label.pack(side=tk.LEFT, anchor=tk.W, padx=self.padding_size, pady=self.padding_size)

        stop_btn = tk.Button(right_frame, text="STOP")
        stop_btn.config(command = self.stop_tsp)
        stop_btn.pack(side=tk.RIGHT, padx=self.padding_size, pady=self.padding_size, ipadx=self.padding_size)

    # Update cities
    def update_cities(self, *_):
        if self.calc_running == False:
            # Update start city
            self.tsp_solver.start_city_name = self.start_city_var.get()
            self.tsp_solver.ga_solver.start_city_name = self.start_city_var.get()
            # Clear (deactivate all cities)
            self.tsp_solver.map.deactivate_all()
            self.canvas.delete("city")
            self.canvas.delete("path")
            # Draw (and activate the active cities)
            num_selected = sum(value.get() for value in self.city_checkbox_values)
            if num_selected > 0:
                self.max_x = max(city.coord_x for city in self.cities)
                self.min_x = min(city.coord_x for city in self.cities)
                self.max_y = max(city.coord_y for city in self.cities)
                self.min_y = min(city.coord_y for city in self.cities)
                for city in self.cities:
                    if self.city_checkbox_values[self.cities.index(city)].get():
                        x = int((city.coord_y - self.min_y) / (self.max_y - self.min_y) * (self.canvas_x - 4 * self.padding_size) + 2 * self.padding_size)
                        y = int((self.max_x - city.coord_x) / (self.max_x - self.min_x) * (self.canvas_y - 4 * self.padding_size) + 2 * self.padding_size)
                        self.tsp_solver.map.activate_city(city_name=city.name)
                        color = "green" if self.start_city_var.get() == city.name else "red"
                        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, outline="black", width=3, tags="city")

    # Draw the path 
    def connect_cities(self, path):
        # Clear
        self.canvas.delete("path")
        # Draw
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i+1]
            x1 = int((start.coord_y - self.min_y) / (self.max_y - self.min_y) * (self.canvas_x - 4 * self.padding_size) + 2 * self.padding_size)
            y1 = int((self.max_x - start.coord_x) / (self.max_x - self.min_x) * (self.canvas_y - 4 * self.padding_size) + 2 * self.padding_size)
            x2 = int((end.coord_y - self.min_y) / (self.max_y - self.min_y) * (self.canvas_x - 4 * self.padding_size) + 2 * self.padding_size)
            y2 = int((self.max_x - end.coord_x) / (self.max_x - self.min_x) * (self.canvas_y - 4 * self.padding_size) + 2 * self.padding_size)
            self.canvas.create_line(x1, y1, x2, y2, fill="black", tags="path", width=5)
        self.canvas.tag_raise("city")

    # Start the selected solver on a different thread
    def calculate_path(self, method: str):
        if self.calc_running == False:
            self.calc_running = True
            self.update_estimated_remaining_time()
            if method == "nn" : self.calc_thread = Thread(target=self.run_nn)
            elif method == "bf" : self.calc_thread = Thread(target=self.run_bf)
            else : self.calc_thread = Thread(target=self.run_ga)
            self.calc_thread.start()

    # Solve by Neirest Neighbor
    def run_nn(self):
        try:
            solution = self.tsp_solver.nearest_neighbor()
            elapsed_time = solution["time"]
            self.connect_cities(path=solution["path"])
            self.elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
            self.calc_running = False
        except Exception as e: self.tsp_solution_handle(exception=e)

    # Solve by Brute Force
    def run_bf(self):
        try:
            solution = self.tsp_solver.brute_force()
            elapsed_time = solution["time"]
            self.connect_cities(path=solution["path"])
            self.elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
            self.calc_running = False
        except Exception as e: self.tsp_solution_handle(exception=e)

    # Solve by Genetic Algorithm
    def run_ga(self):
        try:
            population_size = int(self.population_size_entry.get())
            generations = int(self.generations_entry.get())
            mutation_rate = float(self.mutation_rate_entry.get())
            solution = self.tsp_solver.genetic_algorithm(population_size, generations, mutation_rate)
            elapsed_time = solution["time"]
            self.connect_cities(path=solution["path"])
            self.elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
            self.calc_running = False
        except Exception as e: self.tsp_solution_handle(exception=e)

    # Handle the exceptions for TSP
    def tsp_solution_handle(self, exception: Exception):
        try: raise exception
        except ValueError: 
            messagebox.showerror("Invalid GA parameters", "Population size, generations and mutation rate should be an integer!")
            self.elapsed_time_label.config(text=f"Elapsed Time: 0.00 seconds")
        except InvalidStartCityError as e:
            msg = str(e).split("!",1)
            messagebox.showerror(msg[0], msg[1])
            self.elapsed_time_label.config(text=f"Elapsed Time: 0.00 seconds")
        except InvalidMapError as e:
            msg = str(e).split("!",1)
            messagebox.showerror(msg[0], msg[1])
            self.elapsed_time_label.config(text=f"Elapsed Time: 0.00 seconds")
        except SolverStopException as e: 
            pass
        except InvalidProvidedValueError as e:
            msg = str(e).split("!",1)
            messagebox.showerror(msg[0], msg[1])
            self.elapsed_time_label.config(text=f"Elapsed Time: 0.00 seconds")
        finally:
            self.calc_running = False
    
    # Update estimated time label
    def update_estimated_remaining_time(self):
        if self.calc_running == True: 
            est_time_remaining = self.tsp_solver.get_estimated_remaining_time()
            self.elapsed_time_label.config(text=f"Estimated Remaining Time: {est_time_remaining:.2f} seconds")
            self.after(100, self.update_estimated_remaining_time)

    # Stop the tsp
    def stop_tsp(self):
        if self.calc_running == True:
            self.tsp_solver.stop_solver()
            self.calc_running = False
            self.elapsed_time_label.config(text=f"Elapsed Time: 0.00 seconds")

    # Handle what happen when close the window
    def on_close(self):
        self.tsp_solver.stop_solver()
        if self.calc_thread != None: self.calc_thread.join()
        self.destroy()

def main():
    app = AppTSP(map_file_path="cities.json")
    app.mainloop()

if __name__ == "__main__":
    main()
