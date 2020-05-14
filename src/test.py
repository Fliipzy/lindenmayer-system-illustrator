import tkinter as tk
import tkinter.ttk as ttk
import widgets

class VariablesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self,
            text = "Variables",
            font = ("", 12),
            padx = 0,
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)
        self.buttons_frame = tk.Frame(self.label_frame)

        #Setup label
        self.variable_label = tk.Label(self.input_frame, text = "Var:")
        self.value_label = tk.Label(self.input_frame, text = "Value:")
        self.operation_label = tk.Label(self.input_frame, text = "f(x):")

        #Setup entries
        self.variable_entry = widgets.Entry(self.input_frame, width = 6)
        self.value_entry = widgets.NumberEntry(self.input_frame, width = 6)
        self.operation_combobox = ttk.Combobox(
            self.input_frame,
            values = ["Move", "Rotate", "Save", "Load"],
            state = "readonly")

        #Setup buttons
        self.add_button = tk.Button(self.buttons_frame, text = "Add", state = tk.DISABLED)
        self.delete_button = tk.Button(self.buttons_frame, text = "Delete", state = tk.DISABLED)

        #Setup treeview
        self.treeview = widgets.ScrollableTreeviewFrame(self.label_frame)
        self.treeview.configure_treeview(
            columns = ["var", "op", "val"],
            show = "headings",
            selectmode = "browse",
            height = 4)
        
        self.treeview.modify_heading("var", text = "Variable")
        self.treeview.modify_heading("op", text = "Operation")
        self.treeview.modify_heading("val", text = "Value")
        self.treeview.modify_column("var", minwidth = 30, width = 0)
        self.treeview.modify_column("op", minwidth = 30, width = 0)
        self.treeview.modify_column("val", minwidth = 30, width = 0)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)

        self.treeview.pack(fill = tk.X, padx = 5, pady = (5, 0))

        self.input_frame.pack(side = tk.LEFT, padx = 5, pady = (5, 0))
        self.variable_label.grid(column = 0, row = 0)
        self.variable_entry.grid(column = 1, row = 0)
        self.value_label.grid(column = 2, row = 0)
        self.value_entry.grid(column = 3, row = 0)
        self.operation_label.grid(column = 0, row = 1, pady = 5)
        self.operation_combobox.grid(column = 1, row = 1, columnspan = 3)

        self.buttons_frame.pack(side = tk.RIGHT, anchor = tk.N, padx = 5, pady = 5)
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.delete_button.grid(column = 1, row = 0)

class RulesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self, 
            text = "Rules", 
            font = ("", 12), 
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)
        self.entries_frame = tk.Frame(self.input_frame)
        self.buttons_frame = tk.Frame(self.input_frame)

        #Setup buttons
        self.add_button = tk.Button(self.buttons_frame, text = "Add", state = tk.DISABLED)
        self.delete_button = tk.Button(self.buttons_frame, text = "Delete", state = tk.DISABLED)

        #Setup entries
        self.var_combobox = ttk.Combobox(self.entries_frame, width = 2)
        self.mutation_entry = widgets.Entry(self.entries_frame)

        #Setup labels
        self.var_label = tk.Label(self.entries_frame, text = "Var:")

        #Setup treeview
        self.treeview = widgets.ScrollableTreeviewFrame(self.label_frame)
        self.treeview.configure_treeview(
            columns = ["var", "mut"],
            show = "headings",
            selectmode = "browse",
            height = 4)

        self.treeview.modify_heading("var", text = "Variable")
        self.treeview.modify_heading("mut", text = "Mutation")
        self.treeview.modify_column("var", minwidth = 30, width = 0)
        self.treeview.modify_column("mut", minwidth = 30, width = 0)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)
        self.treeview.pack(fill = tk.X, padx = 5, pady = (5, 0))
        self.input_frame.pack(fill = tk.X, padx = 5, pady = 5)

        self.entries_frame.pack(side = tk.LEFT)
        self.var_label.grid(column = 0, row = 0)
        self.var_combobox.grid(column = 1, row = 0, padx = (0, 5))
        self.mutation_entry.grid(column = 2, row = 0)

        self.buttons_frame.pack(side = tk.RIGHT)
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.delete_button.grid(column = 1, row = 0)

class SettingsFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self, text = "Settings", 
            font = ("", 12),
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)

        #Setup labels
        self.axiom_label = tk.Label(self.input_frame, text = "Axiom:")
        self.position_x_label = tk.Label(self.input_frame, text = "Position X:")
        self.position_y_label = tk.Label(self.input_frame, text = "Position Y:")
        self.angle_label = tk.Label(self.input_frame, text = "Angle (deg):")

        self.iteration_label = tk.Label(self.input_frame, text = "Iterations:")
        self.line_start_thickness_label = tk.Label(self.input_frame, text = "Line start thickness:")
        self.line_end_thickness_label = tk.Label(self.input_frame, text = "Line end thickness:")
        self.line_type_label = tk.Label(self.input_frame, text = "Line type:")

        #Setup entries
        self.axiom_entry = widgets.Entry(self.input_frame, width = 8)
        self.position_x_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.position_y_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.angle_entry = widgets.NumberEntry(self.input_frame, width = 8)

        self.iteration_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8, 
            from_ = 1, 
            to = 10,
            state = "readonly")

        self.line_start_thickness_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8,
            from_ = 1,
            to = 100,
            state = "readonly")

        self.line_end_thickness_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8,
            from_ = 1,
            to = 100,
            state = "readonly")

        self.line_type_combobox = ttk.Combobox(
            self.input_frame, 
            width = 7, 
            state = "readonly",
            values = ["Straight", "Curvy", "Arrow"])


        #Placement
        self.label_frame.pack(fill = tk.BOTH)
        self.input_frame.pack(fill = tk.BOTH, padx = 5, pady = 5)

        self.axiom_label.grid(column = 0, row = 0, sticky = tk.W, pady = (0,5))
        self.position_x_label.grid(column = 0, row = 1, sticky = tk.W, pady = (0,5))
        self.position_y_label.grid(column = 0, row = 2, sticky = tk.W, pady = (0,5))
        self.angle_label.grid(column = 0, row = 3, sticky = tk.W, pady = (0,5))

        self.axiom_entry.grid(column = 1, row = 0, pady = (0,5))
        self.position_x_entry.grid(column = 1, row = 1, pady = (0,5))
        self.position_y_entry.grid(column = 1, row = 2, pady = (0,5))
        self.angle_entry.grid(column = 1, row = 3, pady = (0,5))

        self.iteration_label.grid(column = 2, row = 0, sticky = tk.W, padx = (10, 0), pady = (0,5))
        self.line_start_thickness_label.grid(column = 2, row = 1, sticky = tk.W, padx = (10, 0), pady = (0,5))
        self.line_end_thickness_label.grid(column = 2, row = 2, sticky = tk.W, padx = (10, 0), pady = (0,5))
        self.line_type_label.grid(column = 2, row = 3, sticky = tk.W, padx = (10, 0), pady = (0,5))

        self.iteration_spinbox.grid(column = 3, row = 0, pady = (0,5))
        self.line_start_thickness_spinbox.grid(column = 3, row = 1, pady = (0,5))
        self.line_end_thickness_spinbox.grid(column = 3, row = 2, pady = (0,5))
        self.line_type_combobox.grid(column = 3, row = 3, pady = (0,5))



        


app = tk.Tk()
app.title("Lindenmayer Systems Illustrator")
app.geometry("1150x750")
app.resizable(0,0)

#Setup main frames
control_frame = tk.Frame(app, padx = 5, pady = 5)
drawing_frame = tk.Frame(app, bg = "#212121")

#Setup widgets
variables_frame = VariablesFrame(control_frame)
rules_frame = RulesFrame(control_frame)
settings_frame = SettingsFrame(control_frame)

#Placement
control_frame.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)
drawing_frame.place(relx = 0.3, rely = 0, relwidth = 0.7, relheight = 1)

variables_frame.pack(fill = tk.X)
rules_frame.pack(fill = tk.X)
settings_frame.pack(fill = tk.X)

app.mainloop()