import tkinter as tk
import tkinter.ttk as ttk
import re as regex
import utilities as util
import lsystem as lsys
import math

class VariablesFrame(tk.Frame):
    '''
    This frame holds the entries & submit button widgets for the variables list.
    '''
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(self, text = "Variables", font = ("", 9, "bold"))
        self.entry_frame = tk.Frame(self.label_frame)
        self.submit_frame = tk.Frame(self.label_frame)

        #Setup labels
        self.var_label = tk.Label(self.entry_frame, text = "var:")
        self.val_label = tk.Label(self.entry_frame, text = "value:")
        self.func_label = tk.Label(self.entry_frame, text = "f(x):")

        #Setup entries
        self.var_entry = tk.Entry(self.entry_frame)
        self.val_entry = tk.Entry(self.entry_frame)
        self.func_combobox = ttk.Combobox(self.entry_frame, 
                                            values = ["Move", "Rotate", "Save", "Load"], 
                                            state = "readonly",
                                            width = 17)
        #Setup submit button
        self.submit_button = tk.Button(self.submit_frame, 
                                        text = "submit", 
                                        width = 21, 
                                        state = tk.DISABLED,
                                        command = self.submit_button_clicked_event)

        #Event bindings
        self.func_combobox.bind("<<ComboboxSelected>>", self.func_selection_event)
        self.func_combobox.bind("<<ComboboxSelected>>", self.update_submit_button_state, add = "+")
        self.var_entry.bind("<KeyRelease>", self.var_key_released_event)
        self.var_entry.bind("<KeyRelease>", self.update_submit_button_state, add = "+")
        self.val_entry.bind("<KeyRelease>", self.val_key_released_event)
        self.val_entry.bind("<KeyRelease>", self.update_submit_button_state, add = "+")

        #Placement
        self.label_frame.pack(padx = 5, pady = 5)
        self.entry_frame.pack(padx = 5, pady = 5)
        self.submit_frame.pack()

        self.var_label.grid(column = 0, row = 0, sticky = tk.W)
        self.func_label.grid(column = 0, row = 1, sticky = tk.W)
        self.val_label.grid(column = 0, row = 2, sticky = tk.W)

        self.var_entry.grid(column = 1, row = 0, pady = 5)
        self.func_combobox.grid(column = 1, row = 1, pady = 5)
        self.val_entry.grid(column = 1, row = 2, pady = 5)

        self.submit_button.pack(pady = (0, 6))

    def set_instances(self, variable_treeview_frame, rules_frame):
        self.var_treeview_obj = variable_treeview_frame
        self.rules_frame_obj = rules_frame
    
    def var_key_released_event(self, args):
        '''
        Checks if entry has more than one char,
        if it has delete everything but the first char.
        '''
        if len(self.var_entry.get()) > 1:
            self.var_entry.delete(1, tk.END)

    def func_selection_event(self, args):
        '''
        Checks whether LOAD or SAVE has been selected,
        if it has then disable the val_entry else enable it.
        '''
        item = self.func_combobox.get()
        if item == "Save" or item == "Load":
            self.val_entry.delete(0, tk.END)
            self.val_entry["state"] = tk.DISABLED
        else:
            self.val_entry["state"] = tk.NORMAL
    
    def val_key_released_event(self, args):
        '''
        Checks if the value entry text can be converted to a number.
        If not it highlights the value entry background with red.
        '''
        value = self.val_entry.get()
        if util.isdigit(value) or value == "":
            self.val_entry["bg"] = "#FFFFFF"
        else:
            self.val_entry["bg"] = "#FFAAAA"
    
    def update_submit_button_state(self, args):
        '''
        Checks if all requirements are met to enable the submit button.
        The requirements are:
        1.  That both the variable & value entries length must exceed 0. 
        2.  The function combobox must have a selected item.
        '''
        var_length = len(self.var_entry.get())
        func_item = self.func_combobox.get()
        val_isdigit = util.isdigit(self.val_entry.get())

        if var_length > 0 and func_item != "" and (val_isdigit or func_item in ["Save", "Load"]):
            self.submit_button["state"] = tk.NORMAL
        else:
            self.submit_button["state"] = tk.DISABLED
    
    def submit_button_clicked_event(self):
        '''
        Inserts the variable data (var-name, func, value) to the variable list widget.
        '''
        var = self.var_entry.get()
        func = self.func_combobox.get()
        val = self.val_entry.get()

        self.var_treeview_obj.insert_variable(var, func, val)
        self.rules_frame_obj.update_combobox_values()

class VariableTreeViewFrame(tk.Frame):
    '''
    This frame holds the treeview that displays all the variables. Also,
    it holds buttons for deleting or editing functionality.
    '''
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.treeview_frame = tk.Frame(self)
        self.buttons_frame = tk.Frame(self)

        #Setup buttons
        self.remove_button = tk.Button(self.buttons_frame, 
                                        text = "remove", 
                                        state = tk.DISABLED,
                                        command = self.remove_button_clicked_event)
        self.edit_button = tk.Button(self.buttons_frame, 
                                        text = "edit", 
                                        state = tk.DISABLED,
                                        command = self.edit_button_clicked_event)

        #Setup treeview
        self.treeview = ttk.Treeview(self.treeview_frame, 
                                        columns = ["var", "function", "value"], 
                                        show = "headings",
                                        selectmode = "browse",
                                        height = 5)
        self.treeview.column("var", minwidth = 20, width = 60)
        self.treeview.heading("var", text = "var")
        self.treeview.column("function", minwidth = 40, width = 80)
        self.treeview.heading("function", text = "f(x)")
        self.treeview.column("value", minwidth = 40, width = 70)
        self.treeview.heading("value", text = "value")

        #Setup treeview vertical scrollbar
        self.treeview_scrollbar = tk.Scrollbar(self.treeview_frame, 
                                                orient = tk.VERTICAL, 
                                                command = self.treeview.yview)
        self.treeview.configure(yscrollcommand = self.treeview_scrollbar.set)

        #Event bindings
        self.treeview.bind("<<TreeviewSelect>>", self.treeview_item_selected_event)

        #Adjust grid weights
        self.treeview_frame.columnconfigure(0, weight = 1)
        self.treeview_frame.columnconfigure(1, weight = 0)

        #Placement
        self.treeview_frame.pack(padx = 5, pady = 5)
        self.buttons_frame.pack(padx = 5, pady = (0, 5), fill = tk.X)

        self.treeview.grid(column = 0, row = 0, sticky = tk.W + tk.E)
        self.treeview_scrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S + tk.W + tk.E)

        self.remove_button.grid(column = 0, row = 0, padx = (0, 5))
        self.edit_button.grid(column = 1, row = 0)

    def set_instances(self, rules_frame):
        self.rules_frame_obj = rules_frame

    def insert_variable(self, var, func, val):
        '''
        Inserts the given parameters into the treeview
        '''
        self.treeview.insert("", tk.END, values = [var, func, val])

    def change_buttons_states(self, state):
        '''
        Changes both the remove & edit buttons states to the given state argument
        '''
        self.remove_button["state"] = state
        self.edit_button["state"] = state

    def treeview_item_selected_event(self, args):
        '''
        If an item from the treeview is selected the delete & edit buttons state
        will be set to NORMAL, making them able to be clicked.
        '''
        self.change_buttons_states(tk.NORMAL)

    def remove_button_clicked_event(self):
        '''
        First the function removes the selected item/variable from the treeview.
        After that it changes the state of both the buttons - remove & edit - to disabled.
        '''
        selected_item = self.treeview.selection()[0]
        self.treeview.delete(selected_item)
        self.change_buttons_states(tk.DISABLED)

        self.rules_frame_obj.update_combobox_values()

    def edit_button_clicked_event(self):
        '''
        Open a temporary window with widgets to edit the selected item/variable
        from the treeview.
        '''
        pass

    def get_tree_rows_data(self, column_index):
        '''
        Returns all the data from the specified column name, from the treeview. 
        '''
        data = []
        for child in self.treeview.get_children():
            data.append(self.treeview.item(child)["values"][column_index])
        return data
    

class RulesFrame(tk.Frame):
    def __init__(self, master = None, **kw):
        super().__init__(master = master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(self, text = "Rules", font = ("", 9, "bold"))
        self.entries_frame = tk.Frame(self.label_frame)
        self.treeview_frame = tk.Frame(self)

        #Setup rules treeview
        self.treeview = ttk.Treeview(self.treeview_frame, 
                                            columns = ["var", "mutation"],
                                            show = "headings",
                                            selectmode = "browse",
                                            height = 3)
        self.treeview.column("var", minwidth = 20, width = 40, stretch = tk.NO)
        self.treeview.heading("var", text = "var")
        self.treeview.heading("mutation", text = "mutation")

        #Setup treeview vertical scrollbar
        self.treeview_scrollbar = tk.Scrollbar(self.treeview_frame, 
                                                    orient = tk.VERTICAL,
                                                    command = self.treeview.yview)
        self.treeview.configure(yscrollcommand = self.treeview_scrollbar.set)

        #Setup entries
        self.var_combobox = ttk.Combobox(self.entries_frame, 
                                        state = "readonly", 
                                        width = 3)
        self.mutation_entry = tk.Entry(self.entries_frame)

        #Setup labels
        self.equals_label = tk.Label(self.entries_frame, text = "=")

        #Setup buttons
        self.submit_button = tk.Button(self.label_frame, 
                                        text = "submit", 
                                        width = 21,
                                        state = tk.DISABLED,
                                        command = self.submit_button_clicked_event)

        #Setup event bindings
        self.var_combobox.bind("<<ComboboxSelected>>", self.var_combobox_item_selected_event)
        self.mutation_entry.bind("<KeyRelease>", self.mutation_entry_key_released_event)

        #Adjust grid weights
        self.treeview_frame.columnconfigure(0, weight = 1)
        self.treeview_frame.columnconfigure(1, weight = 0)

        #Placement
        self.label_frame.pack(padx = 5, pady = 5)
        self.entries_frame.pack(padx = 5, pady = 5)
        self.treeview_frame.pack(padx = 5, pady = 5)

        self.treeview.grid(column = 0, row = 0)
        self.treeview_scrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S)

        self.var_combobox.grid(column = 0, row = 0)
        self.equals_label.grid(column = 1, row = 0)
        self.mutation_entry.grid(column = 2, row = 0)

        self.submit_button.pack(pady = (0, 5))

    def set_instances(self, variable_treeview_frame):
        self.var_treeview_obj = variable_treeview_frame

    def update_combobox_values(self):
        '''
        Updates the values of the variable combobox to match the var names in the
        variable list.
        '''
        vars = set(self.var_treeview_obj.get_tree_rows_data(0))
        cbox_text = self.var_combobox.get()

        if cbox_text != "" and cbox_text not in vars:
            self.var_combobox.set("")
        if len(vars) == 0:
            self.var_combobox["values"] = ""
            self.var_combobox.set("")
        else:
            self.var_combobox["values"] = list(vars)

        self.update_submit_button_status()
    
    def update_submit_button_status(self):
        '''
        Checks if nessesary entries have been filled to submit rule to treeview list.
        If, then submit button's state is set to normal.
        '''
        var = self.var_combobox.get()
        mutation = self.mutation_entry.get()

        if var != "" and len(mutation) > 0:
            self.submit_button["state"] = tk.NORMAL
        else:
            self.submit_button["state"] = tk.DISABLED

    def insert_rule(self, var, mutation):
        '''
        Inserts given rule into the rule treeview.
        '''
        self.treeview.insert("", tk.END, values = [var, mutation])

    def submit_button_clicked_event(self):
        var = self.var_combobox.get()
        mutation = self.mutation_entry.get()
        self.insert_rule(var, mutation)

    def mutation_entry_key_released_event(self, args):
        self.update_submit_button_status()

    def var_combobox_item_selected_event(self, args):
        self.update_submit_button_status()

class DrawFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup canvas
        self.canvas = tk.Canvas(self, 
                                bg="#FFFFFF", 
                                borderwidth = 5, 
                                highlightthickness = 5,
                                relief = tk.SUNKEN)

        #Placement
        self.canvas.pack(fill = tk.BOTH, expand = True)

        #Draw edge coordinates to canvas 
        self.draw_corner_coordinates()

    def draw_lsystem(self, lsystem, variables, start_rot = 0, start_pos = (0, 0)):
        '''
        Takes in an lsystem and various other arguments to 
        draw the system to the canvas. 

        The algorithm supports four operations: move, rotate, save, load.
        Move draws a line with given length in a direction calculated by the rotation.
        Rotate changes the current rotation by the given value.
        Save pushes the current position and rotation (state) to a stack.
        Load pops the latest state from the stack and sets position and rotation to it.
        '''

        self.clear_canvas()

        position = start_pos
        rotation = start_rot
        states = []
        
        for char in lsystem:
            operation = variables.get(char)
            
            if operation == None:
                continue

            func = operation[0]
            value = operation[1]

            if func == "move":
                new_position = (position[0] + math.cos((rotation * math.pi / 180)) * value, 
                                position[1] + math.sin((rotation * math.pi / 180)) * value)
    
                self.canvas.create_line(position[0],
                                        position[1], 
                                        new_position[0], 
                                        new_position[1])
                position = new_position

            elif func == "rotate":
                rotation += value
            
            elif func == "save":
                states.insert(len(states), (position, rotation))

            elif func == "load":
                saved_state = states.pop()
                position = saved_state[0]
                rotation = saved_state[1]
        
    def draw_corner_coordinates(self):
        print(self.world_pos_to_normalized(600, 600))
        self.canvas.create_text(30, 20, text = "(-1, -1)", font = ("", 9, "bold"))
        self.canvas.create_text(685, 20, text = "(1, -1)", font = ("", 9, "bold"))
        self.canvas.create_text(30, 680, text = "(-1, 1)", font = ("", 9, "bold"))
        self.canvas.create_text(685, 680, text = "(1, 1)", font = ("", 9, "bold"))

    def world_pos_to_normalized(self, x, y):
        nx = 2 * (x / self.canvas.winfo_width()) - 1 
        ny = 2 * (y / self.canvas.winfo_height()) - 1 
        return (nx, ny) 

    def normalized_to_world_pos(self, x, y):
        wx = self.canvas.winfo_width() * ((x + 1) / 2) 
        wy = self.canvas.winfo_height() * ((y + 1) / 2) 
        return (wx, wy)

    def clear_canvas(self):
        '''
        Clears the canvas for graphics
        '''
        self.canvas.delete(tk.ALL)

    def change_canvas_background(self, color):
        '''
        Change the background color of the canvas
        '''
        self.canvas["bg"] = color
        

    
        
app = tk.Tk()

app.geometry("950x700")
app.resizable(0,0)

#Declare and initialize widgets
leftframe = tk.Frame(app)
drawframe = DrawFrame(app)

varlist = VariableTreeViewFrame(leftframe)
varinput = VariablesFrame(leftframe)
rules = RulesFrame(leftframe)

#Set instance binding
varlist.set_instances(rules)
varinput.set_instances(varlist, rules)
rules.set_instances(varlist)

#Placement
leftframe.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
drawframe.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight =1)

varinput.pack(anchor = tk.W)
varlist.pack(anchor = tk.W)
rules.pack(anchor = tk.W)

app.update()

app.mainloop()
