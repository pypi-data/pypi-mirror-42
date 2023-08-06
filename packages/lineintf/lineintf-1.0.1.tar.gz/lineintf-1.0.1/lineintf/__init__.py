import sys
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox


class LineIntf:
    __li_title = None
    __last_line = None
    __last_comp = None
    __name_index = 0
    __components = None
    __groups = None
    label_width = 14
    entry_width = None
    text_width = 40
    text_height = 10
    list_width = 14
    list_height = 8
    spin_width = None
    combo_width = None
    option_width = 18
    check_width = None
    radio_width = None
    button_width = None
    font_default = ("Arial", 12, "")
    font_title = ("Times", 16, "bold")
    font_ruler = ("Times", 14, "bold italic")

    def __init__(self, master, with_title=None):
        self.__li_title = with_title
        self.__components = []
        self.__groups = []
        if with_title is not None:
            if isinstance(master, Tk):
                master.title(with_title)
        if isinstance(master, LineIntf):
            master = master.root
        self.root = master
        self.root.contentFrame = Frame(self.root)
        self.root.contentFrame.pack(side=LEFT, padx=12, pady=12, fill="both", anchor="nw")
        self.new_line()

    def new_line(self):
        self.__last_line = Frame(self.root.contentFrame, pady=8)
        self.__last_line.pack(side=TOP, fill="both", anchor="sw")
        return self.__last_line

    def new_ruler(self, with_label=None):
        rtn = []
        new_ruler_1 = Frame(self.root.contentFrame, height=8)
        new_ruler_1.pack(side=TOP, fill="x", anchor="sw")
        rtn.append(new_ruler_1)

        if with_label is not None:
            new_label = Label(self.root.contentFrame, text=with_label, font=self.font_ruler, anchor="sw", justify=LEFT)
            new_label.pack(fill="x", side=TOP, pady=0, padx=8, ipady=2, ipadx=8, anchor="sw")
            rtn.append(new_label)

        new_ruler_2 = Frame(self.root.contentFrame, height=2, bg="SystemWindowText")
        new_ruler_2.pack(side=TOP, fill="x", anchor="sw")
        rtn.append(new_ruler_2)
        new_ruler_3 = Frame(self.root.contentFrame, height=8)
        new_ruler_3.pack(side=TOP, fill="x", anchor="sw")
        rtn.append(new_ruler_3)
        self.new_line()
        return rtn

    def new_title(self, new_value=None, new_name=None):
        if new_value is None:
            new_value = self.__li_title
        new_label = Label(self.__last_line, text=new_value, font=self.font_title, anchor="sw")
        new_label.pack(side=TOP, pady=0, padx=8, ipady=2, ipadx=8, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_label])
        self.__last_comp = new_label
        return new_label

    def new_label(self, new_value, new_name=None):
        new_label = Label(self.__last_line, text=new_value, font=self.font_default, anchor="sw")
        if self.label_width is not None:
            new_label["width"] = self.label_width
        new_label.pack(side=LEFT, padx=4, ipady=4, ipadx=4, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_label])
        self.__last_comp = new_label
        return new_label

    def new_entry(self, new_value=None, new_name=None, with_label=None):
        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.entry_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        new_entry = Entry(where_in, font=self.font_default)
        if new_value is not None:
            new_entry.insert(0, new_value)
        if self.entry_width is not None:
            new_entry["width"] = self.entry_width
        new_entry.pack(side=side_in, padx=4, ipady=4, ipadx=4, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_entry])
        self.__last_comp = new_entry
        return new_entry

    def new_text(self, new_value=None, new_name=None, with_label=None):
        where_in = Frame(self.__last_line)
        where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)

        if with_label is not None:
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.text_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        scrollbar = Scrollbar(where_in)
        scrollbar.pack(side=RIGHT, fill=Y)

        new_text = Text(where_in, font=self.font_default, yscrollcommand=scrollbar.set)
        if new_value is not None:
            new_text.insert(1.0, new_value)
        if self.text_width is not None:
            new_text["width"] = self.text_width
        if self.text_height is not None:
            new_text["height"] = self.text_height
        new_text.pack(side=LEFT, padx=4, ipady=4, ipadx=4, anchor="sw")

        scrollbar.config(command=new_text.yview)

        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_text])
        self.__last_comp = new_text
        return new_text

    @staticmethod
    def __list_add(in_list):
        try:
            in_list.list_add()
        except AttributeError:
            answer = simpledialog.askstring("Item", "Enter the value for:")
            if answer is not None:
                in_list.insert(END, answer)

    @staticmethod
    def __list_del(in_list):
        try:
            in_list.list_del()
        except AttributeError:
            selections = in_list.curselection()
            for selection in selections:
                in_list.delete(selection)

    @staticmethod
    def __list_edit(in_list):
        try:
            in_list.list_edit()
        except AttributeError:
            selections = in_list.curselection()
            if selections:
                var_edt = in_list.get(selections[0])
                answer = simpledialog.askstring("Item", "Enter the value for:", initialvalue=var_edt)
                if answer is not None:
                    in_list.delete(selections[0])
                    in_list.insert(selections[0], answer)

    @staticmethod
    def __list_up(in_list):
        try:
            in_list.list_up()
        except AttributeError:
            selections = in_list.curselection()
            if selections:
                if selections[0] > 0:
                    idx = selections[0]
                    itn = in_list.get(idx)
                    in_list.delete(idx)
                    in_list.insert(idx - 1, itn)
                    in_list.select_clear(0, "end")
                    in_list.select_set(idx - 1)
                    in_list.event_generate("<<ListboxSelect>>")
                    in_list.activate(idx - 1)

    @staticmethod
    def __list_down(in_list):
        try:
            in_list.list_down()
        except AttributeError:
            selections = in_list.curselection()
            if selections:
                if selections[0] < in_list.size() - 1:
                    idx = selections[0]
                    itn = in_list.get(idx)
                    in_list.delete(idx)
                    in_list.insert(idx + 1, itn)
                    in_list.select_clear(0, "end")
                    in_list.select_set(idx + 1)
                    in_list.event_generate("<<ListboxSelect>>")
                    in_list.activate(idx + 1)

    def new_list(self, new_values=None, new_name=None, with_label=None, put_buttons=True):
        where_in = Frame(self.__last_line)
        where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)

        if with_label is not None:
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.text_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        scrollbar = Scrollbar(where_in)
        scrollbar.pack(side=RIGHT, fill=Y)

        new_list = Listbox(where_in, font=self.font_default, yscrollcommand=scrollbar.set)

        if put_buttons:
            frm_buttons = Frame(where_in)
            frm_buttons.pack(side=LEFT, fill=Y)

            btn_add = Button(frm_buttons, text="+", font=self.font_default, width="1", height="1")
            btn_add["command"] = lambda: self.__list_add(new_list)
            btn_add.pack(side=TOP, padx=0, ipady=0, ipadx=0, anchor="n")

            btn_del = Button(frm_buttons, text="-", font=self.font_default, width="1", height="1")
            btn_del["command"] = lambda: self.__list_del(new_list)
            btn_del.pack(side=TOP, padx=0, ipady=0, ipadx=0, anchor="n")

            btn_edt = Button(frm_buttons, text="§", font=self.font_default, width="1", height="1")
            btn_edt["command"] = lambda: self.__list_edit(new_list)
            btn_edt.pack(side=TOP, padx=0, ipady=0, ipadx=0, anchor="n")

            btn_up = Button(frm_buttons, text="˄", font=self.font_default, width="1", height="1")
            btn_up["command"] = lambda: self.__list_up(new_list)
            btn_up.pack(side=TOP, padx=0, ipady=0, ipadx=0, anchor="n")

            btn_dn = Button(frm_buttons, text="˅", font=self.font_default, width="1", height="1")
            btn_dn["command"] = lambda: self.__list_down(new_list)
            btn_dn.pack(side=TOP, padx=0, ipady=0, ipadx=0, anchor="n")

        if new_values is not None:
            for value in new_values:
                new_list.insert(END, value)
        if self.list_width is not None:
            new_list["width"] = self.list_width
        if self.list_height is not None:
            new_list["height"] = self.list_height
        new_list.pack(side=LEFT, padx=4, ipady=4, ipadx=4, anchor="sw")

        scrollbar.config(command=new_list.yview)

        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_list, "list"])
        self.__last_comp = new_list
        return new_list

    def new_choice(self, new_values, new_value=None, new_name=None, with_label=None):
        where_in = Frame(self.__last_line)
        where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)

        if with_label is not None:
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.text_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        scrollbar = Scrollbar(where_in)
        scrollbar.pack(side=RIGHT, fill=Y)

        new_choice = Listbox(where_in, font=self.font_default, selectmode=SINGLE, yscrollcommand=scrollbar.set)
        ins_idx = 0
        value_idx = None
        for ins_value in new_values:
            if value_idx is None and ins_value == new_value:
                value_idx = ins_idx
            new_choice.insert(END, ins_value)
            ins_idx += 1
        if value_idx is not None:
            new_choice.select_set(value_idx)
            new_choice.event_generate("<<ListboxSelect>>")
        if self.list_width is not None:
            new_choice["width"] = self.list_width
        if self.list_height is not None:
            new_choice["height"] = self.list_height
        new_choice.pack(side=LEFT, padx=4, ipady=4, ipadx=4, anchor="sw")

        scrollbar.config(command=new_choice.yview)

        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_choice, "choice"])
        self.__last_comp = new_choice
        return new_choice

    def new_spin(self, new_value=0, new_name=None, with_label=None):
        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.entry_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        new_spin = Spinbox(where_in, from_=-1*sys.maxsize, to=sys.maxsize, font=self.font_default)
        new_spin.delete(0, END)
        new_spin.insert(0, new_value)
        if self.entry_width is not None:
            new_spin["width"] = self.entry_width
        new_spin.pack(side=side_in, padx=4, ipady=4, ipadx=4, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_spin])
        self.__last_comp = new_spin
        return new_spin

    def new_combo(self, new_values, new_value=None, new_name=None, with_label=None):
        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.entry_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        combo_var = StringVar()
        if new_value is not None:
            combo_var.set(new_value)
        new_combo = ttk.Combobox(where_in, values=new_values, textvariable=combo_var, font=self.font_default)
        if self.combo_width is not None:
            new_combo["width"] = self.combo_width
        new_combo.pack(side=side_in, padx=4, ipady=4, ipadx=4, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_combo, combo_var])
        self.__last_comp = new_combo
        return new_combo

    def new_option(self, new_values, new_value=None, new_name=None, with_label=None):
        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.entry_width is not None:
                new_label.width = self.entry_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        option_var = StringVar()
        option_var.set(new_value)
        new_option = OptionMenu(where_in, option_var, *new_values)
        new_option['anchor'] = "w"
        new_option['justify'] = LEFT
        new_option['font'] = self.font_default
        if self.option_width is not None:
            new_option["width"] = self.option_width
        new_option.pack(side=side_in, padx=4, ipady=4, ipadx=4, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_option, option_var])
        self.__last_comp = new_option
        return new_option

    def new_check(self, new_text, new_name=None, with_label=None):
        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            if self.check_width is not None:
                new_label.width = self.check_width
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        check_var = IntVar()
        new_check = Checkbutton(where_in, text=new_text, variable=check_var, font=self.font_default)
        if self.check_width is not None:
            new_check["width"] = self.check_width
        new_check.pack(side=side_in, padx=4, ipady=4, ipadx=0, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_check, check_var])
        self.__last_comp = new_check
        return new_check

    def new_radio(self, new_text, new_value, of_group_name, new_name=None, with_label=None):
        group_var = None
        for group in self.__groups:
            if group[0] == of_group_name:
                group_var = group[1]
        if group_var is None:
            if isinstance(new_value, str):
                group_var = StringVar()
            else:
                group_var = IntVar()
            self.__groups.append([of_group_name, group_var])

        where_in = self.__last_line
        side_in = LEFT

        if with_label is not None:
            where_in = Frame(self.__last_line)
            where_in.pack(fill="both", side=LEFT, padx=0, ipady=0, ipadx=0)
            side_in = BOTTOM
            new_label = Label(where_in, text=with_label, font=self.font_default, anchor="sw", justify=LEFT)
            new_label.pack(fill="x", side=TOP, pady=2, padx=0, ipady=0, ipadx=0, anchor="sw")

        new_radio = Radiobutton(where_in, text=new_text, variable=group_var, value=new_value,
                                font=self.font_default, anchor="sw")
        if self.radio_width is not None:
            new_radio["width"] = self.radio_width
        new_radio.pack(side=side_in, padx=4, ipadx=4, ipady=0, anchor="sw")
        group_var.set(None)
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_radio, group_var])
        self.__last_comp = new_radio
        return new_radio

    def new_button(self, new_text="*", new_command=None, new_name=None):
        new_button = Button(self.__last_line, text=new_text, font=self.font_default)
        if new_command is not None:
            new_button["command"] = new_command
        if self.button_width is not None:
            new_button.width = self.button_width
        new_button.pack(side=LEFT, padx=4, ipadx=4, ipady=0, anchor="sw")
        if new_name is None:
            self.__name_index += 1
            new_name = "li" + str(self.__name_index)
        self.__components.append([new_name, new_button])
        self.__last_comp = new_button
        return new_button

    def new_button_close(self, new_text="Close"):
        return self.new_button(new_text=new_text, new_command=lambda: self.close())

    def last_line(self):
        return self.__last_line

    def last_comp(self):
        return self.__last_comp

    def get_comp(self, with_name):
        for component in self.__components:
            if component[0] == with_name:
                return component[1]
        return None

    def get_value(self, with_name):
        for component in self.__components:
            if component[0] == with_name:
                if isinstance(component[1], Label):
                    return component[1]["text"]
                elif isinstance(component[1], Entry):
                    return component[1].get()
                elif isinstance(component[1], Text):
                    return component[1].get(1.0, END)
                elif isinstance(component[1], Listbox):
                    if component[2] == "choice":
                        return component[1].get(ACTIVE)
                    else:
                        return component[1].get(0, "end")
                elif isinstance(component[1], Spinbox):
                    return component[1].get()
                elif isinstance(component[1], ttk.Combobox):
                    return component[2].get()
                elif isinstance(component[1], OptionMenu):
                    return component[2].get()
                elif isinstance(component[1], Checkbutton):
                    return component[2].get()
                elif isinstance(component[1], Button):
                    return component[1]["command"]
        for group in self.__groups:
            if group[0] == with_name:
                return group[1].get()
        return None

    def set_value(self, with_name, the_value):
        for component in self.__components:
            if component[0] == with_name:
                if isinstance(component[1], Label):
                    component[1]["text"] = the_value
                    return True
                elif isinstance(component[1], Entry):
                    component[1].delete(0, END)
                    component[1].insert(0, the_value)
                    return True
                elif isinstance(component[1], Text):
                    component[1].delete(1.0, END)
                    component[1].insert(1.0, the_value)
                    return True
                elif isinstance(component[1], Listbox):
                    if component[2] == "choice":
                        value_idx = component[1].get(0, "end").index(the_value)
                        component[1].select_clear(0, "end")
                        component[1].select_set(value_idx)
                        component[1].event_generate("<<ListboxSelect>>")
                        component[1].activate(value_idx)
                    else:
                        component[1].delete(0, "end")
                        for value in the_value:
                            component[1].insert(END, value)
                    return True
                elif isinstance(component[1], Spinbox):
                    component[1].delete(0, END)
                    component[1].insert(0, the_value)
                    return True
                elif isinstance(component[1], ttk.Combobox):
                    component[2].set(the_value)
                    return True
                elif isinstance(component[1], OptionMenu):
                    component[2].set(the_value)
                    return True
                elif isinstance(component[1], Checkbutton):
                    component[2].set(the_value)
                    return True
                elif isinstance(component[1], Button):
                    component[1]["command"] = the_value
                    return True
        for group in self.__groups:
            if group[0] == with_name:
                group[1].set(the_value)
                return True
        return False

    def new_message(self, the_message, **options):
        rtn = messagebox.showinfo(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def new_error(self, the_message, **options):
        rtn = messagebox.showerror(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def new_warning(self, the_message, **options):
        rtn = messagebox.showwarning(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def new_string(self, the_message, **options):
        rtn = simpledialog.askstring(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def new_integer(self, the_message, **options):
        rtn = simpledialog.askinteger(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def new_float(self, the_message, **options):
        rtn = simpledialog.askfloat(self.__li_title, the_message, **options)
        if hasattr(self.root, 'focus_force'):
            self.root.focus_force()
        return rtn

    def close(self):
        self.root.destroy()
