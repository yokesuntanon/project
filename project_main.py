import tkinter as tk
from tkinter import ttk

HUGEFONT = ("News Gothic", 20)
LARGEFONT = ("News Gothic", 15)
MEDIUMFONT = ("News Gothic", 13)
SMALLFONT = ("News Gothic", 10)

# Define the variables to calculate
class Data:
    salary = 0
    bonus = 0
    other_income = 0
    marriage_status = None
    dropdown_parents = None
    dropdown_parents_spouse = None
    dropdown_incompetent = None
    dropdown_incompetent_spouse = None
    dropdown_children = None
    children_before = 0
    children_after = 0
    children_before_1 = 0
    children_after_1 = 0
    children_before_2 = 0
    children_after_2 = 0
    pvd = 0
    social_security = 0
    interest_house = 0
    life_ip = 0
    health_ip = 0
    health_ip_parents = 0
    pension_life_ip = 0
    gpf = 0
    nsf = 0
    ptf = 0

class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Tax Calculator")
        self.geometry("630x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Income, Ex, PVD, Insurance, OtherFunds, Result):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Income)
       
    def show_frame(self, cont):
        if cont != Result:  
            self.frames[cont].tkraise()
        else:
            self.frames[Result].update_data()
            self.frames[Result].tkraise()

class CommonFrame(tk.Frame):

    def __init__(self, parent, controller, labels, title):
        tk.Frame.__init__(self, parent)
        
        # Create step icon
        for i, (bg_color, fg_color) in enumerate(labels):
            step_label = tk.Label(self, text=str(i + 1), font=MEDIUMFONT, bg=bg_color, fg=fg_color)
            step_label.place(x=30 + (i * 110), y=30)
            if i != len(labels) - 1:
                step_label = tk.Label(self, text="-------------", font=MEDIUMFONT, fg="black")
                step_label.place(x=50 + (i * 110), y=30)
        
        # Set the topic format
        step_label = tk.Label(self, text=title, font=LARGEFONT, fg="black")
        step_label.place(x=30, y=80)

# Page Income
class Income(CommonFrame):

    def __init__(self, parent, controller):

        labels = [("light blue", "white") if i == 0 else ("gray", "white") for i in range(6)]  # Change the color of the step icon
        super().__init__(parent, controller, labels, "Income")

        ttk.Label(self, text="Salary (Bath)", font=MEDIUMFONT).place(x=270, y=135)
        self.salary_entry = ttk.Entry(self)
        self.salary_entry.place(x=220, y=160)

        ttk.Label(self, text="Bonus (Bath/year)", font=MEDIUMFONT).place(x=260, y=225)
        self.bonus_entry = ttk.Entry(self)
        self.bonus_entry.place(x=220, y=250)

        ttk.Label(self, text="Other income (Bath/year)", font=MEDIUMFONT).place(x=240, y=315)
        self.other_incomes_entry = ttk.Entry(self)
        self.other_incomes_entry.place(x=220, y=340)

        ttk.Button(self, text="Next", command=lambda: [self.getdata(), controller.show_frame(Ex)]).place(x=270, y=430)

    def getdata(self):
        Data.salary = int(self.salary_entry.get())
        Data.bonus = int(self.bonus_entry.get())
        Data.other_income = int(self.other_incomes_entry.get())

# Page Exemption
class Ex(CommonFrame):

    def __init__(self, parent, controller):

        labels = [("light blue", "white") if i <= 1 else ("gray", "white") for i in range(6)]  # Change the color of the step icon
        super().__init__(parent, controller, labels, "Exemption")

        self.label_list = []  # Initialize label_list

        ttk.Label(self, text="Personal Exemption", font=MEDIUMFONT).place(x=360, y=120)
        tk.Label(self, text=" 60,000 ", font=MEDIUMFONT, bg="white").place(x=490, y=120)


        # Marriage status options
        ttk.Label(self, text="Marriage Status", font=MEDIUMFONT).place(x=30, y=120)
        options = ["Single", "Divorce", "Spouse has income", "Spouse has no income"]
        dropdown_var = tk.StringVar()
        dropdown_var.set("Select an option")
        self.dropdown_var_marriage = tk.OptionMenu(self, dropdown_var, *options, command=lambda *args: update_question(self, dropdown_var))
        self.dropdown_var_marriage.place(x=140, y=118)

        # Turn page buttons
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(Income)).place(x=220, y=450)
        ttk.Button(self, text="Next", command=lambda: [self.getdata(), controller.show_frame(PVD)]).place(x=330, y=450)

        # Keep track of the dynamically created dropdowns
        self.dynamic_dropdowns = []

        # Create dropdown for the parents exemption question
        def dropdown_parents(frame, set_x, set_y):
            
            # Dropdown menu options
            new_options = ["No Exemption", "Father Exemption", "Mother Exemption", "Father and Mother Exemption"]

            new_clicked = tk.StringVar()
            new_clicked.set(new_options[0])

            # Create Dropdown menu
            new_drop = tk.OptionMenu(frame, new_clicked, *new_options)
            new_drop.place(x=set_x, y=set_y)

            # Append the created dropdown to the list
            self.dynamic_dropdowns.append(new_drop)

            return new_clicked

        # Create dropdown for the children exemption question
        def dropdown_children(frame, set_x2, set_y2):          
            
            # Dropdown menu options
            new_options = ["No", "Yes"]

            new_clicked = tk.StringVar()
            new_clicked.set(new_options[0])

            # Create Dropdown menu
            new_drop = tk.OptionMenu(frame, new_clicked, *new_options)
            new_drop.place(x=set_x2, y=set_y2)

            # Append the created dropdown to the list
            self.dynamic_dropdowns.append(new_drop)

            return new_clicked

        # Create dropdown for the incompetent person support question
        def dropdown_incompetent(frame, set_x3, set_y3):
            
            # Dropdown menu options
            new_options = ["0", "1", "2", "3"]

            new_clicked = tk.StringVar()
            new_clicked.set(new_options[0])

            # Create Dropdown menu
            new_drop = tk.OptionMenu(frame, new_clicked, *new_options)
            new_drop.place(x=set_x3, y=set_y3)

            # Append the created dropdown to the list
            self.dynamic_dropdowns.append(new_drop)

            return new_clicked

        def update_question(frame, dropdown_var):
            selected_option = Data.marriage_status = dropdown_var.get()

            # Destroy previously created dropdowns
            for dropdown in self.dynamic_dropdowns:
                dropdown.destroy()
            self.dynamic_dropdowns = []
            
            # Destroy previously created questions
            for widget in frame.winfo_children():
                if widget.winfo_y() > 120 and widget.winfo_y() < 450: 
                    widget.destroy()

            # Create the questions for each type of marriage status options
            if selected_option == "Single":

                tk.Label(frame, text="Own Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=160)    
                tk.Label(frame, text="Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=230)

                self.dropdown_parents = dropdown_parents(frame, 30, 190)
                self.dropdown_incompetent = dropdown_incompetent(frame, 30 ,260)

            elif selected_option == "Divorce":
                tk.Label(frame, text="Own Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=160)
                tk.Label(frame, text="Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=230)

                tk.Label(frame, text="The first child", font=MEDIUMFONT).place(x=360, y=160)
                tk.Label(frame, text="The second child onwards:", font=MEDIUMFONT).place(x=360, y=230)            
                tk.Label(frame, text="Number of children born before 2018", font=MEDIUMFONT).place(x=360, y=255)
                self.children_before = ttk.Entry(self)
                self.children_before.place(x=360, y=280)
                tk.Label(frame, text="Number of children born after 2018", font=MEDIUMFONT).place(x=360, y=310)
                self.children_after = ttk.Entry(self)
                self.children_after.place(x=360, y=330)

                self.dropdown_parents = dropdown_parents(frame, 30, 190)
                self.dropdown_incompetent = dropdown_incompetent(frame, 30 ,260)
                self.dropdown_children = dropdown_children(frame, 360, 190)

            elif selected_option == "Spouse has income":
                tk.Label(frame, text="Own Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=160)
                tk.Label(frame, text="Own Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=230)

                tk.Label(frame, text="Spouse's Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=300)   
                tk.Label(frame, text="Spouse's Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=370)

                tk.Label(frame, text="The first child", font=MEDIUMFONT).place(x=360, y=160)
                tk.Label(frame, text="The second child onwards:", font=MEDIUMFONT).place(x=360, y=230)               
                tk.Label(frame, text="Number of children born before 2018", font=MEDIUMFONT).place(x=360, y=255)
                self.children_before_1 = ttk.Entry(self)
                self.children_before_1.place(x=360, y=280)
                tk.Label(frame, text="Number of children born after 2018", font=MEDIUMFONT).place(x=360, y=310)
                self.children_after_1 = ttk.Entry(self)
                self.children_after_1.place(x=360, y=330)

                self.dropdown_parents = dropdown_parents(frame, 30 ,190)
                self.dropdown_parents_spouse = dropdown_parents(frame, 30, 330)
                self.dropdown_children = dropdown_children(frame, 360, 190)
                self.dropdown_incompetent = dropdown_incompetent(frame, 30, 260)
                self.dropdown_incompetent_spouse = dropdown_incompetent(frame, 30, 400)

            elif selected_option == "Spouse has no income":
                tk.Label(frame, text="Own Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=160)
                tk.Label(frame, text="Own Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=230)

                tk.Label(frame, text="Spouse's Father-Mother Exemption", font=MEDIUMFONT).place(x=30, y=300)
                tk.Label(frame, text="Spouse's Disable/Incompetent person support", font=MEDIUMFONT).place(x=30, y=370)

                tk.Label(frame, text="The first child", font=MEDIUMFONT).place(x=360, y=160)
                tk.Label(frame, text="The second child onwards:", font=MEDIUMFONT).place(x=360, y=230)
                
                tk.Label(frame, text="Number of children born before 2018", font=MEDIUMFONT).place(x=360, y=255)
                self.children_before_2 = ttk.Entry(self)
                self.children_before_2.place(x=360, y=280)

                tk.Label(frame, text="Number of children born after 2018", font=MEDIUMFONT).place(x=360, y=310)
                self.children_after_2 = ttk.Entry(self)
                self.children_after_2.place(x=360, y=330)
                
                self.dropdown_parents = dropdown_parents(frame, 30, 190)
                self.dropdown_parents_spouse = dropdown_parents(frame, 30, 330)
                self.dropdown_children = dropdown_children(frame, 360, 190)
                self.dropdown_incompetent = dropdown_incompetent(frame, 30, 260)
                self.dropdown_incompetent_spouse = dropdown_incompetent(frame, 30, 400)

    def getdata(self):
        
        # Get the value from different type of selected options
        if Data.marriage_status == "Single":
            Data.dropdown_parents = str(self.dropdown_parents.get())
            Data.dropdown_incompetent = str(self.dropdown_incompetent.get())

        elif Data.marriage_status == "Divorce":
            Data.dropdown_parents = str(self.dropdown_parents.get())
            Data.dropdown_incompetent = str(self.dropdown_incompetent.get())
            Data.dropdown_children = str(self.dropdown_children.get())
            Data.children_before = int(self.children_before.get())
            Data.children_after = int(self.children_after.get())

        elif Data.marriage_status == "Spouse has income":
            Data.dropdown_parents = str(self.dropdown_parents.get())
            Data.dropdown_parents_spouse = str(self.dropdown_parents_spouse.get())
            Data.dropdown_incompetent = str(self.dropdown_incompetent.get())
            Data.dropdown_incompetent_spouse = str(self.dropdown_incompetent_spouse.get())
            Data.dropdown_children = str(self.dropdown_children.get())
            Data.children_before_1 = int(self.children_before_1.get())
            Data.children_after_1 = int(self.children_after_1.get())
        
        
        elif Data.marriage_status == "Spouse has no income":
            Data.dropdown_parents = str(self.dropdown_parents.get())
            Data.dropdown_parents_spouse = str(self.dropdown_parents_spouse.get())
            Data.dropdown_incompetent = str(self.dropdown_incompetent.get())
            Data.dropdown_incompetent_spouse = str(self.dropdown_incompetent_spouse.get())
            Data.dropdown_children = str(self.dropdown_children.get())
            Data.children_before_2 = int(self.children_before_2.get())
            Data.children_after_2 = int(self.children_after_2.get())

# Page Provide Fund
class PVD(CommonFrame):

    def __init__(self, parent, controller):
        labels = [("light blue", "white") if i <= 2 else ("gray", "white") for i in range(6)]  # Change the color of the step icon
        super().__init__(parent, controller, labels, "Provide Fund")
    
        ttk.Label(self, text="PVD", font=MEDIUMFONT).place(x=300, y=135)
        tk.Label(self, text="No more than 15 percent of salary (not including employer contributions) and no more than 500,000 baht", font=SMALLFONT, fg="brown").place(x=70, y=190)
        self.pvd_entry = ttk.Entry(self)
        self.pvd_entry.place(x=220, y=160)

        ttk.Label(self, text="Social Security Money", font=MEDIUMFONT).place(x=250, y=225)
        tk.Label(self, text="No more than 9,000 baht", font=SMALLFONT, fg="brown").place(x=250, y=280)
        self.social_security_entry = ttk.Entry(self)
        self.social_security_entry.place(x=220, y=250)

        ttk.Label(self, text="Interest on Housing Purchases", font=MEDIUMFONT).place(x=223, y=315)
        tk.Label(self, text="No more than 100,000 baht", font=SMALLFONT, fg="brown").place(x=240, y=370)
        self.interest_house_entry = ttk.Entry(self)
        self.interest_house_entry.place(x=220, y=340)
       
        # Turn page buttons
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(Ex)).place(x=220, y=430)
        ttk.Button(self, text="Next", command=lambda: [self.getdata(), controller.show_frame(Insurance)]).place(x=330, y=430) 
    
    def getdata(self):
        Data.pvd = int(self.pvd_entry.get())
        Data.social_security = int(self.social_security_entry.get())
        Data.interest_house = int(self.interest_house_entry.get())

# Page Insurance
class Insurance(CommonFrame):

    def __init__(self, parent, controller):
        
        labels = [("light blue", "white") if i <= 3 else ("gray", "white") for i in range(6)]  # Change the color of the step icon
        
        super().__init__(parent, controller, labels, "Insurance")
        
        ttk.Label(self, text="Life Insurance Premiums", font=MEDIUMFONT).place(x=80, y=130)
        tk.Label(self, text="No more than 100,000 baht", font=SMALLFONT, fg="brown").place(x=90, y=190)
        self.life_ip_entry = ttk.Entry(self)
        self.life_ip_entry.place(x=60, y=160)
        
        ttk.Label(self, text="Health Insurance Premiums", font=MEDIUMFONT).place(x=350, y=130)
        tk.Label(self, text="No more than 25,000 baht", font=SMALLFONT, fg="brown").place(x=370, y=190)
        self.health_ip_entry = ttk.Entry(self)
        self.health_ip_entry.place(x=340, y=160)

        tk.Label(self, text="Life insurance premiums and health insurance together must not exceed 100,000 baht", font=SMALLFONT, fg="brown").place(x=85, y=230)
        tk.Label(self, text="------------------------------------------------------------------------------------------------", font=MEDIUMFONT, fg="dark gray").place(x=20, y=250)
        
        ttk.Label(self, text="Health Insurance Premiums for Parents", font=MEDIUMFONT).place(x=40, y=280)
        tk.Label(self, text="No more than 15,000 baht", font=SMALLFONT, fg="brown").place(x=90, y=340)
        self.health_ip_parents_entry = ttk.Entry(self)
        self.health_ip_parents_entry.place(x=60, y=310)
        
        ttk.Label(self, text="Pension Life Insurance Premiums", font=MEDIUMFONT).place(x=335, y=280)
        tk.Label(self, text="Not more than 15 percent of annual income,", font=SMALLFONT, fg="brown").place(x=300, y=335)
        tk.Label(self, text="not more than 200,000 baht if life insurance rights,", font=SMALLFONT, fg="brown").place(x=300, y=350)
        tk.Label(self, text="are not used. Can be combined with a maximum of 300,000 baht", font=SMALLFONT, fg="brown").place(x=300, y=365)
        tk.Label(self, text="and combined with other funds not exceeding 500,000 baht.", font=SMALLFONT, fg="brown").place(x=300, y=380)
        self.pension_life_ip_entry = ttk.Entry(self)
        self.pension_life_ip_entry.place(x=340, y=310)

        # Turn page buttons
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(PVD)).place(x=220, y=430)
        ttk.Button(self, text="Next", command=lambda: [self.getdata(), controller.show_frame(OtherFunds)]).place(x=330, y=430)

    def getdata(self):
        Data.life_ip = int(self.life_ip_entry.get())
        Data.health_ip = int(self.health_ip_entry.get())
        Data.health_ip_parents = int(self.health_ip_parents_entry.get())
        Data.pension_life_ip = int(self.pension_life_ip_entry.get())

# Page Other Funds
class OtherFunds(CommonFrame):

    def __init__(self, parent, controller):
        
        labels = [("light blue", "white") if i <= 4 else ("gray", "white") for i in range(6)]  # Change the color of the step icon

        super().__init__(parent, controller, labels, "Other Funds")

        ttk.Label(self, text="Government Pension Fund (GPF)", font=MEDIUMFONT).place(x=220, y=135)
        self.gpf_entry = ttk.Entry(self)
        self.gpf_entry.place(x=220, y=160)
        tk.Label(self, text="Not more than 15 percent of annual income and combined with other funds not exceeding 500,000 baht", font=SMALLFONT, fg="brown").place(x=70, y=190)

        ttk.Label(self, text="National Savings Fund (National Savings Fund)", font=MEDIUMFONT).place(x=180, y=225)
        self.nsf_entry = ttk.Entry(self)
        self.nsf_entry.place(x=220, y=250)
        tk.Label(self, text="No more than 13,200 bath", font=SMALLFONT, fg="brown").place(x=250, y=280)

        ttk.Label(self, text="Private Teacher Fund", font=MEDIUMFONT).place(x=250, y=315)
        self.ptf_entry = ttk.Entry(self)
        self.ptf_entry.place(x=220, y=340)
        tk.Label(self, text="No more than 15 percent of annual income", font=SMALLFONT, fg="brown").place(x=210, y=370)

        # Turn page buttons
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(Insurance)).place(x=220, y=430)
        ttk.Button(self, text="Next", command=lambda: [self.getdata(), controller.show_frame(Result)]).place(x=330, y=430)

    def getdata(self):
        Data.gpf = int(self.gpf_entry.get())
        Data.nsf = int(self.nsf_entry.get())
        Data.ptf = int(self.ptf_entry.get())

# Page Total Tax Payment
class Result(CommonFrame):

    def __init__(self, parent, controller):

        labels = [("light blue", "white") for _ in range(6)]  # Change the color of the step icon

        super().__init__(parent, controller, labels, "Total Tax Payment")

        # Turn page buttons
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(OtherFunds)).place(x=220, y=430)
        ttk.Button(self, text="Home", command=lambda: controller.show_frame(Income)).place(x=330, y=430)

    # Calculate the tax payment from the collected data
    def update_data(self):

        # Define the value from different types of parents exemption dropdown options
        if Data.dropdown_parents == "No Exemption":
                num_p = 0
        elif Data.dropdown_parents == "Father Exemption" or Data.dropdown_parents == "Mother Exemption":
            num_p = 1
        elif Data.dropdown_parents == "Father and Mother Exemption":
            num_p = 2

        # Define the value from different types of incompetent support dropdown options
        if Data.dropdown_incompetent == "0":
            num_i = 0
        elif Data.dropdown_incompetent == "1":
            num_i = 1
        elif Data.dropdown_incompetent == "2":
            num_i = 2
        elif Data.dropdown_incompetent == "3":
            num_i = 3

        # Define the value from different types of spouse parents exemption dropdown options
        if Data.dropdown_parents_spouse == "No Exemption":
            num_p_s = 0
        elif Data.dropdown_parents_spouse == "Father Exemption" or Data.dropdown_parents_spouse == "Mother Exemption":
            num_p_s = 1
        elif Data.dropdown_parents_spouse == "Father and Mother Exemption":
            num_p_s = 2
        
        # Define the value from different types of spouse incompetent support dropdown options
        if Data.dropdown_incompetent_spouse == "0":
            num_i_s = 0
        elif Data.dropdown_incompetent_spouse == "1":
            num_i_s = 1
        elif Data.dropdown_incompetent_spouse == "2":
            num_i_s = 2
        elif Data.dropdown_incompetent_spouse == "3":
            num_i_s = 3

        # Define the value from different types of the first child dropdown options
        if Data.dropdown_children == "No":
            num_c = 0
            num_c_b = num_c_b1 = num_c_b2 = 0
            num_c_a = num_c_a1 = num_c_a2 = 0
        elif Data.dropdown_children == "Yes":
            num_c = 1
            num_c_b = Data.children_before
            num_c_a = Data.children_after
            num_c_b1 = Data.children_before_1
            num_c_a1 = Data.children_after_1
            num_c_b2 = Data.children_before_2
            num_c_a2 = Data.children_after_2

        # Create the net income fomula and calculate
        if Data.marriage_status == "Single":
            exemption = 60000 + (30000*num_p) + (60000*num_i) + Data.pvd + Data.social_security + Data.interest_house + Data.life_ip + Data.health_ip + Data.health_ip_parents + Data.pension_life_ip + Data.gpf + Data.nsf + Data.ptf
            income = Data.salary*12 + Data.bonus + Data.other_income
            net_income = income - exemption

        elif Data.marriage_status == "Divorce":
            exemption = 60000 + (30000*num_p) + (60000*num_i) + (30000*num_c) + (30000*num_c_b) + (60000*num_c_a) + Data.pvd + Data.social_security + Data.interest_house + Data.life_ip + Data.health_ip + Data.health_ip_parents + Data.pension_life_ip + Data.gpf + Data.nsf + Data.ptf
            income = Data.salary*12 + Data.bonus + Data.other_income
            net_income = income - exemption

        elif Data.marriage_status == "Spouse has income":
            exemption = 60000 + (30000*num_p) + (60000*num_i) + (30000*num_p_s) + (60000*num_i_s) + (30000*num_c) + (30000*num_c_b1) + (60000*num_c_a1) + Data.pvd + Data.social_security + Data.interest_house + Data.life_ip + Data.health_ip + Data.health_ip_parents + Data.pension_life_ip + Data.gpf + Data.nsf + Data.ptf
            income = Data.salary*12 + Data.bonus + Data.other_income
            net_income = income - exemption

        elif Data.marriage_status == "Spouse has no income":
            exemption = 60000 + (30000*num_p) + (60000*num_i) + (30000*num_p_s) + (60000*num_i_s) + (30000*num_c) + (30000*num_c_b2) + (60000*num_c_a2) + Data.pvd + Data.social_security + Data.interest_house + Data.life_ip + Data.health_ip + Data.health_ip_parents + Data.pension_life_ip + Data.gpf + Data.nsf + Data.ptf
            income = Data.salary*12 + Data.bonus + Data.other_income
            net_income = income - exemption

        # Calculate the total tax payment
        if net_income < 150000 and Data.other_income*12 < 60000:
            tax = 0
        elif 150000 <= net_income <= 300000:
            tax = ((net_income - 150000)*0.05)+0
        elif 300001 <= net_income <= 500000:
            tax = ((net_income - 300000)*0.1)+7500
        elif 500001 <= net_income <= 750000:
            tax = ((net_income - 500000)*0.15)+27500
        elif 750001 <= net_income <= 1000000:
            tax = ((net_income - 750000)*0.2)+65000
        elif 1000001 <= net_income <= 2000000:
            tax = ((net_income - 1000000)*0.25)+115000
        elif 2000001 <= net_income <= 5000000:
            tax = ((net_income - 2000000)*0.3)+365000
        elif net_income > 5000000:
            tax = ((net_income - 5000000)*0.35)+126500

        # Show the result
        ttk.Label(self, text="The Total Tax Payment", font=HUGEFONT).place(x=210, y=190)
        tk.Label(self, text=tax, font=HUGEFONT, bg="light blue", fg="black").place(x=240, y=250)
        ttk.Label(self, text="Bath", font=HUGEFONT).place(x=340, y=252)

app = tkinterApp()
app.mainloop()
