import csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog
import sys
import os
 
#Start
class LoginWindow: # Initialize the login window
    def __init__(self, root):
        self.root = root
        self.root.title("NutriTrack Login")
        self.root.geometry("400x250")
        self.apply_style()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.terminate_program)
 
    def terminate_program(self):
        sys.exit() # Closes the application when the window is closed (so user cant be directed to the software without login)
 
    def apply_style(self):
        style = ttk.Style()
        style.theme_use('clam')
 
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="20") #login window widgets
        frame.pack(expand=True, fill="both")
 
        self.username_label = ttk.Label(frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
 
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
 
        self.password_label = ttk.Label(frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
 
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
 
        self.login_button = ttk.Button(frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
 
        self.signup_button = ttk.Button(frame, text="Sign Up", command=self.open_signup_window)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=10)
 
    def login(self):
        # User Authentication 
        username = self.username_entry.get()
        password = self.password_entry.get()
 
        # Check if the entered credentials match any stored credentials for users
        if self.check_credentials(username, password):
            messagebox.showinfo("Login Successful", "Welcome to NutriTrack!")
            self.root.destroy()  # Close the login window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
 
    def check_credentials(self, entered_username, entered_password):
        # Read the stored credentials from the CSV file for checking 
        with open("User_Credentials.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                stored_username, stored_password = row
                if entered_username == stored_username and entered_password == stored_password:
                    return True
        return False
 
    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root) # Open the sign-up window
        signup_window.title("Sign Up")
        signup_window.geometry("400x200")
        self.apply_style()
 
        username_label = ttk.Label(signup_window, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
 
        username_entry = ttk.Entry(signup_window)
        username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
 
        password_label = ttk.Label(signup_window, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
 
        password_entry = ttk.Entry(signup_window, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
 
        signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: self.register_user(signup_window, username_entry.get(), password_entry.get()))
        signup_button.grid(row=2, column=0, columnspan=2, pady=10)
 
    def register_user(self, window, username, password):
        # Stores the user credentials in a CSV file
        with open("User_Credentials.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
 
        messagebox.showinfo("Sign Up Successful", "Your account has been created!")
        window.destroy()
 
def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
 
if __name__ == "__main__":
    main()



# BMI classification chart
bmi_classification = {
    "Severe Thinness": "< 16",
    "Moderate Thinness": "16 - 17",
    "Mild Thinness": "17 - 18.5",
    "Normal": "18.5 - 25",
    "Overweight": "25 - 30",
    "Obese Class I": "30 - 35",
    "Obese Class II": "35 - 40",
    "Obese Class III": "> 40",
}

# Function to calculate BMI
def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    return bmi

# Function to classify BMI
def classify_bmi(bmi):
    for classification, bmi_range in bmi_classification.items():
        if "<" in bmi_range:
            upper_limit = float(bmi_range[1:])
            if bmi < upper_limit:
                return classification
        elif ">" in bmi_range:
            lower_limit = float(bmi_range[1:])
            if bmi > lower_limit:
                return classification
        else:
            lower_limit, upper_limit = map(float, bmi_range.split(" - "))
            if lower_limit <= bmi < upper_limit:
                return classification
    return "Unknown"

# Function to get user input with options
def get_option_input(prompt, options):
    while True:
        user_input = simpledialog.askstring("Input", prompt).lower()
        if user_input in options:
            return user_input
        else:
            invalid_message = f"Invalid input. Please choose from the options: {' / '.join(options)}"
            messagebox.showinfo("Invalid Input", invalid_message)
 

# GUI setup
root = tk.Tk()
root.title("NutriTrack")
root.geometry("500x450")
 

# Welcome Message
tk.Label(root, text="--- WELCOME TO THE NUTRITRACK ---", font=("Helvetica", 20)).pack()
 
# Getting user information
name = simpledialog.askstring("Name", "What's your name?")
gender_options = ["male", "female"]
gender = get_option_input("What's Your Gender? (Male / Female)", gender_options)
age = simpledialog.askinteger("Age", f"Hi, {name} may I know your age please?")
weight = simpledialog.askfloat("Weight", f"COOL {name}! I would like to know your weight? (KG)")
height = simpledialog.askfloat("Height", f"{name}, May I know your height? (cm)")
 
# Display information
info_message = f"Name: {name}\nGender: {gender}\nAge: {age}\nWeight: {weight} KG\nHeight: {height} cm"
tk.Label(root, text=info_message, font=("Helvetica", 16)).pack()
 
# Calculate BMI and classify
bmi = calculate_bmi(weight, height)
bmi_classification_result = classify_bmi(bmi)
 
bmi_message = f"{name}, your BMI is: {bmi:.2f}\nBMI Classification: {bmi_classification_result}"
tk.Label(root, text=bmi_message, font=("Helvetica", 16)).pack()
 
# BMR Calculation
def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        s=5
    elif gender.lower() == "female":
        s = -161
    else:
        return None
    bmr = 10*weight + 6.25*height - 5*age + s
    return bmr
 
bmr = calculate_bmr(weight, height, age, gender)
 
# Display BMR information
bmr_message = f"Your BMR is: {bmr:.2f} kcal/day"
tk.Label(root, text=bmr_message, font=("Helvetica", 16)).pack()
 
# Getting fitness goals and dietary preference
goals_options = ["gaining weight", "losing weight", "improving strength"]
goals = get_option_input("What are your fitness goals? (Gaining weight / Losing weight / Improving strength)", goals_options)
 
dietary_preference_options = ["meat lover", "vegetarian", "flexitarian"]
dietary_preference = get_option_input(f"{name}, are you A Vegetarian / A Meat Lover / A Flexitarian(Both)", dietary_preference_options)
 
# Display goals and preferences
goal_preference_message = f"Fitness Goals: {goals}\nDietary Preference: {dietary_preference}"
tk.Label(root, text=goal_preference_message, font=("Helvetica", 16)).pack()
 
def log_meal():
    root.destroy() # Close the current window (basic logic that direcs program to meal logging)
   
log_meal_button = tk.Button(root, text="Log Your Meal", command=log_meal, font=("Helvetica", 14))
log_meal_button.pack(pady=10)
 
Exit_button = tk.Button(root, text="Exit",command= sys.exit, font=("Helvetica", 14))
Exit_button.pack(pady=10)
 
# End GUI
root.mainloop()
 

# Meal Logging
class NutriTrack:
    def __init__(self, root):
        self.root = root # Initialising the NutriTrack application
        root.title("NutriTrack (Meal Logging)")
 
        style = ttk.Style()
        style.theme_use('clam') 
 
        self.create_widgets()
   
    def show_nutrition_info(self):
        # Function to display nutrition information from a CSV file
        file_path = "Food-Database.csv"
 
        try:
            # Read CSV file
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
 
                # Creating a new window to display the nutrition info
                nutrition_info_window = tk.Toplevel(self.root)
                nutrition_info_window.title("Nutrition Information")
 
                # Creating Treeview for displaying data
                tree = ttk.Treeview(nutrition_info_window, columns=header, show="headings")
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=150)
 
                # Insert data into Treeview
                for row in reader:
                    tree.insert("", "end", values=row)
 
                # Adding scrollbar
                scrollbar = ttk.Scrollbar(nutrition_info_window, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
 
                # Pack components
                tree.pack(expand=True, fill=tk.BOTH)
                scrollbar.pack(side="right", fill="y")
 
        except FileNotFoundError:
            messagebox.showinfo("File not found", f"The selected file '{file_path}' was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
           
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill=tk.BOTH)
 
        self.page1 = ttk.Frame(self.notebook)
        self.page2 = ttk.Frame(self.notebook)
 
        self.notebook.add(self.page1, text="Log Your Meal")
        self.notebook.add(self.page2, text="View Your Meals")
 
        self.create_log_meal_page()
        self.create_view_meals_page()
       
    def destroy_window(self):
        self.root.destroy() # Function to destroy the current window (again the same logic)
 
    def create_log_meal_page(self):
        frame = ttk.Frame(self.page1) # Function to create the "Log Your Meal" page widgets
        frame.grid(row=0, column=0, padx=20, pady=20)
 
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=5)
 
        ttk.Label(frame, text="Meal:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.meal_entry = ttk.Entry(frame)
        self.meal_entry.grid(row=1, column=1, pady=5)
 
        ttk.Label(frame, text="Date(YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(frame)
        self.time_entry.grid(row=2, column=1, pady=5)
 
        log_button = ttk.Button(frame, text="Log Meal", command=self.log_meal)
        log_button.grid(row=3, column=0, columnspan=2, pady=10)
       
        calculate_button = ttk.Button(frame, text="Calculate Your Activity Metric", command=self.destroy_window)
        calculate_button.grid(row=5, column=0, columnspan=2, pady=10)
       
    def log_meal(self):
        username = self.username_entry.get() # Function to log a meal entry
        meal = self.meal_entry.get()
        time = self.time_entry.get()
 
        if not username or not meal or not time:
            messagebox.showerror("Error", "Pleas fill in all fields.")
            return
 
        log_meal(username, meal, time)
        messagebox.showinfo("Successfully", f"Meal logged for {username} on {time}: {meal}")
 
    def create_view_meals_page(self):
        frame = ttk.Frame(self.page2) # Function to create the "View Your Meals" page widgets
        frame.grid(row=0, column=0, padx=20, pady=20)
 
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_view_entry = ttk.Entry(frame)
        self.username_view_entry.grid(row=0, column=1, pady=5)
 
        view_button = ttk.Button(frame, text="View Meals", command=self.view_meals)
        view_button.grid(row=1, column=0, columnspan=2, pady=10)
       
        nutrition_info_button = ttk.Button(frame, text="Nutrition Info", command=self.show_nutrition_info)
        nutrition_info_button.grid(row=3, column=2, columnspan=2, pady=10)
 
        self.log_text = ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
        self.log_text.grid(row=2, column=0, columnspan=2, pady=10)
 
    def view_meals(self):
        username = self.username_view_entry.get() # Function to view logged meals for a specific user
 
        if not username:
            messagebox.showerror("Error", "Please enter valid Username.")
            return
 
        try:
            with open(f"{username}_meals.txt", "r") as log_file:
                meals = log_file.read()
                self.log_text.insert(tk.END, meals)
        except:
            messagebox.showinfo(f"No meal entries found for {username}.")
 
def log_meal(username, meal, time): # Function to log a meal entry to a text file
    log_entry = f"{time}: {meal}\n"
    with open(f"{username}_meals.txt", "a") as log_file:
        log_file.write(log_entry)
 
def main():
    root = tk.Tk()
    app = NutriTrack(root)
    root.geometry("500x500")
    root.mainloop()
 
if __name__ == "__main__":
    main()
 
# Defining activity levels and corresponding activity factors
activity_levels = {
    "1": "Sedentary",
    "2": "Lightly active",
    "3": "Moderately active",
    "4": "Active",
    "5": "Very active"
}
 
activity_factors = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Active": 1.725,
    "Very active": 1.9
}
 
def close_current_window():
    root.destroy() # Function to close the current window (again same logic)
 
def calculate_activity_metric(): # Function to calculate the activity metric based on user input
    global activity_metric
    customer_activity_level = entry.get()
 
    if customer_activity_level in ["1", "2", "3", "4", "5"]: # Check if the input is a valid activity level
        activity_level_description = activity_levels.get(customer_activity_level)
        activity_metric = activity_factors[activity_level_description]
        result_label.config(text=f"Your activity level is: {activity_level_description}\n"
                                  f"Activity metric: {activity_metric}")
        diet_recommendation_button.config(state="normal") 
    else:
        messagebox.showerror("Error", "Invalid input. Please enter a number from 1 to 5.")
 
# Create the main window
root = tk.Tk()
root.title("Activity Level Calculator")
 
# Create and place widgets in the window
instruction_label = tk.Label(root, text="Please select your activity level by entering the corresponding number:")
instruction_label.pack()
 
options_label = tk.Label(root, text="1. Sedentary (little or no exercise)\n"
                                    "2. Lightly active (exercise 1–3 days/week)\n"
                                    "3. Moderately active (exercise 3–5 days/week)\n"
                                    "4. Active (exercise 6–7 days/week)\n"
                                    "5. Very active (hard exercise 6–7 days/week)")
options_label.pack()
 
entry = tk.Entry(root)
entry.pack()
 
calculate_button = tk.Button(root, text="Calculate", command=calculate_activity_metric)
calculate_button.pack()
 
diet_recommendation_button = tk.Button(root, text="Get Food Recommendation", command=close_current_window, state="disabled")
diet_recommendation_button.pack()
 
result_label = tk.Label(root, text="")
result_label.pack()
 
root.mainloop()

# Function to provide personalized diet recommendations based on user's goal and dietary preference
def personalized_diet_recommendations(goal, dietary_preference):
    recommendations = {
        "gaining weight": {
            "vegetarian": "Include calorie-dense vegeterian foods like avocados, nuts, whole grains, and legumes. Consider protein supplements.",
            "meat lover": "Focus on lean meats, chicken, fish, and dairy products. Incorporate whole grains and nuts for additional calories.",
            "flexitarian": "Balance meat-based proteins with plant-based sources like tofu and beans. Include whole grains and healthy fats."
            },
        "losing weight": {
            "vegetarian": "Emphasize low-calorie vegetables, fruits, and plant-based proteins. Reduce intake of high-carb foods.",
            "meat lover": "Opt for lean meats, avoid processed meats, and include plenty of vegetables and fruits in your meals.",
            "flexitarian": "Limit meat consumption to lean options, focus on vegetables, fruits, and whole grains."
            },
        "improve strength": {
            "vegetarian": "Focus on protein-rich plant foods like legumes, quinoa, and tofu. Include nuts and seeds for healthy fats.",
            "meat lover": "Emphasize protein intake through lean meats, eggs, and dairy. Include complex carbs and vegetables.",
            "flexitarian": "Combine lean meats and plant-based proteins. Ensure a good intake of whole grains and vegetables."
            },
         "default": {
             "vegetarian": "Maintain a balanced diet with a variety of vegetables, fruit, grains, and plant-based proteins.",
             "meat lover": "Focus on a balanced diet with lean meats, vegetables, fruits, and whole grains.",
             "flexitarian": "Enjoy a mix of meat and plant-based meals, focusing on variety and balance."
             }
    }
    # Get the specific diet recommendation based on the user's goal and dietary preference
    specific_recommendation = recommendations.get(goal, recommendations["default"]).get(dietary_preference, "Maintain a balanced and varied diet.")
 
    return specific_recommendation
 
def get_recommendation(): # Function to get the food recommendation based on user input
    goal = goal_var.get()
    dietary_preference = dietary_preference_var.get()
    diet_recommendation = personalized_diet_recommendations(goal, dietary_preference)
    result_label.config(text="Food Recommendation: " + diet_recommendation)
 
# Create main window
root = tk.Tk()
root.title("NutriTrack Food Recommendation")
 
# Create and configure widgets
goal_label = ttk.Label(root, text="Select Goal:")
goal_var = tk.StringVar()
goal_combobox = ttk.Combobox(root, textvariable=goal_var, values=["gaining weight", "losing weight", "improve strength"])
goal_combobox.set("gaining weight")
 
preference_label = ttk.Label(root, text="Select Dietary Preference:")
dietary_preference_var = tk.StringVar()
preference_combobox = ttk.Combobox(root, textvariable=dietary_preference_var, values=["vegetarian", "meat lover", "flexitarian"])
preference_combobox.set("vegetarian")
 
get_recommendation_button = ttk.Button(root, text="Food Recommendation", command=get_recommendation)
result_label = ttk.Label(root, text="Food Recommendation: ")

get_meal_planning_button = ttk.Button(root, text="Get Meal Planning", command= close_current_window)
get_meal_planning_button.grid(row=4, column=0, columnspan=2, pady=10)
 
# Layout widgets
goal_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
goal_combobox.grid(row=0, column=1, padx=10, pady=10)
 
preference_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
preference_combobox.grid(row=1, column=1, padx=10, pady=10)
 
get_recommendation_button.grid(row=2, column=0, columnspan=2, pady=10)
result_label.grid(row=3, column=0, columnspan=2, pady=10)
 
# Start the main loop
root.mainloop()



def calculate_daily_calorie_intake(bmr, activity_metric):
    return bmr * activity_metric
 
bmi_classification_result = classify_bmi(bmi)
bmr = calculate_bmr(weight, height, age, gender)
 
daily_calorie_intake = calculate_daily_calorie_intake(bmr, activity_metric)
 

def adjust_calorie_intake_and_diet(goal, daily_calorie_intake, dietary_preference):
    if goal == "gaining weight":
        adjusted_calorie_intake = daily_calorie_intake + 500
        diet_recommendation = "High protein, high carb diet. Include lean meats, whole grains, and nuts."
    elif goal == "losing weight":
        adjusted_calorie_intake = daily_calorie_intake - 500
        diet_recommendation = "Low carb, high fiber diet. Focus on vegetables, fruits, and lean proetins."
    elif goal == "improve strenght":
        adjusted_calorie_intake = daily_calorie_intake + 350
        diet_recommendation = "Balanced diet with an emphasis on protein. Include chicken, fish, eggs, and legumes."
    else:
        adjusted_calorie_intake = daily_calorie_intake
        diet_recommendation = "Maintain a balanced diet."
 

    if dietary_preference == "vegetarian":
        diet_recommendation += "Replace meats with plant-based proteins like tofu and lentils."
    elif dietary_preference == "meat lover":
        diet_recommendation += "Focus on lean meats and reduce red meat intake."
    elif dietary_preference == "flexitarian":
        diet_recommendation += "Mix of plant-based and meat options, focusing on variety."
 
    return adjusted_calorie_intake, diet_recommendation
 
adjusted_calorie_intake, diet_recommendation = adjust_calorie_intake_and_diet(goals, daily_calorie_intake, dietary_preference)
 
def calculate_macros(goal_calorie_intake, goal):
 
    if goal == "gaining weight":
        carbs_percentage = 0.55 # Higher carbs for energy
        protein_percentage = 0.25 # adequate protein for muscle gain
        fat_percentage = 0.20 # essential fats
    elif goal == "losing weight":
        carbs_percentage = 0.40 # lower carbs
        protein_percentage = 0.35 # higher protein for satiety and muscle maintenance
        fat_percentage = 0.25 # essential fats
    elif goal == "improve strength":
        carbs_percentage = 0.50 # balanced carbs for energy
        protein_percentage = 0.30 # higher protein for muscle repair and growth
        fat_percentage = 0.20 # essential fats
    else: # default balanced distribution
        carbs_percentage = 0.50
        protein_percentage = 0.25
        fat_percentage = 0.25
 
    carbs_calories = goal_calorie_intake * carbs_percentage
    protein_calories = goal_calorie_intake * protein_percentage
    fat_calories = goal_calorie_intake * fat_percentage
 
    # convert calories ro grams (1g carb = 4 kcal, 1g protein = 4 kcal, 1g fat = 9 kcal)
    carbs_grams = carbs_calories / 4
    protein_grams = protein_calories / 4
    fat_grams = fat_calories / 9
 
    return carbs_grams, protein_grams, fat_grams
 
# adjuted calorie intake for the customer goal
 
carbs_grams, protein_grams, fat_grams = calculate_macros(adjusted_calorie_intake, goals)
 
 
def calculate_sugar_intake(gender):
    if gender.lower() == "male":
        return 37.5 # max daily sugar intake in grams for men
    elif gender.lower() == "female":
        return 25 # max daily sugar intake in grams for women
   
daily_sugar_intake = calculate_sugar_intake(gender)
 
def calculate_totals(carbs, protein, fats, sugar, period='daily'):
    # converts daily intake to weekly or monthly totals
    multiplier = 1
    if period == 'weekly':
        multiplier = 7
    elif period == 'monthly':
        multiplier = 30
 
    total_carbs = carbs * multiplier
    total_protein = protein * multiplier
    total_fats = fats * multiplier
    total_sugar = sugar * multiplier
 
    return total_carbs, total_protein, total_fats, total_sugar
 
def divide_balanced_macros_into_meals(carbs, protein, fats, increase_macro=None):
    total_macros = carbs + protein + fats
    equal_distribution = total_macros / 3
 
    # Adjusting for increased protein or carbs if specified
    if increase_macro == "protein":
        extra = protein - equal_distribution
        carbs -= extra / 2
        fats -= extra / 2
        protein = equal_distribution + extra
    elif increase_macro == "carbs":
        extra = carbs - equal_distribution
        protein -= extra / 2
        carbs = equal_distribution + extra
 
    # Dividing each macro into 5 equal parts for the meals
    carbs_per_meal = carbs / 5
    protein_per_meal = protein / 5
    fats_per_meal = fats / 5
 
    meals = {
        "Breakfast": {"Carbs": carbs_per_meal, "Protein": protein_per_meal, "Fats": fats_per_meal},
        "Snack": {"Carbs": carbs_per_meal, "Protein": protein_per_meal, "Fats": fats_per_meal},
        "Lunch": {"Carbs": carbs_per_meal, "Protein": protein_per_meal, "Fats": fats_per_meal},
        "Second Snack": {"Carbs": carbs_per_meal, "Protein": protein_per_meal, "Fats": fats_per_meal},
        "Dinner": {"Carbs": carbs_per_meal, "Protein": protein_per_meal, "Fats": fats_per_meal},
    }
    return meals
 
def divide_macros_into_meals(carbs, protein, fats, sugar):
    # Define the proportion of macros for each meal
    proportions = {
        "Breakfast": 0.25, # 25% of daily macros for breakfast
        "Snack": 0.10, # 10% for each snack
        "Lunch": 0.20, # 20% for lunch
        "Second Snack": 0.10,
        "Dinner": 0.15 # 15% for dinner
    }
 
    meals = {}
    for meal, proportion in proportions.items():
        meal_carbs = carbs * proportion
        meal_protein = protein * proportion
        meal_fats = fats * proportion
        meal_sugar = sugar * proportion
 
        meals[meal] = {"Carbs": meal_carbs, "Protein": meal_protein, "Fats": meal_fats, "Sugar": meal_sugar}
    return meals
 
carbs_grams, protein_grams, fat_grams = calculate_macros(adjusted_calorie_intake, goals)
daily_sugar_intake = calculate_sugar_intake(gender)
meal_plan = divide_macros_into_meals(carbs_grams, protein_grams, fat_grams, daily_sugar_intake)
 

def on_submit():
    # Get values from GUI input fields
    goal = goal_var.get()
    daily_calorie_intake = float(daily_calorie_intake_entry.get())
    dietary_preference = dietary_preference_var.get()
    gender = gender_var.get()

    # Call your existing functions
    adjusted_calorie_intake, diet_recommendation = adjust_calorie_intake_and_diet(goal, daily_calorie_intake, dietary_preference)
    carbs_grams, protein_grams, fat_grams = calculate_macros(adjusted_calorie_intake, goal)
    daily_sugar_intake = calculate_sugar_intake(gender)
    meal_plan = divide_macros_into_meals(carbs_grams, protein_grams, fat_grams, daily_sugar_intake)

    # Display the results in a messagebox (you can customize this part based on your GUI design)
    result_message = ""
    for meal, macros in meal_plan.items():
        result_message += f"{meal}: Carbs: {macros['Carbs']:.2f}g, Protein: {macros['Protein']:.2f}g, Fats: {macros['Fats']:.2f}g, Sugar: {macros['Sugar']:.2f}g\n"

    messagebox.showinfo("Meal Plan", result_message)

# Create the main window
root = tk.Tk()
root.title("NutriTrack Meal Planner")

# Create and place GUI components
goal_label = tk.Label(root, text="Goal:")
goal_var = tk.StringVar(root)
goal_var.set("gaining weight")  # Default value
goal_menu = tk.OptionMenu(root, goal_var, "gaining weight", "losing weight", "improve strength", "maintain")
goal_label.grid(row=0, column=0, padx=10, pady=10)
goal_menu.grid(row=0, column=1, padx=10, pady=10)

daily_calorie_intake_label = tk.Label(root, text="Daily Calorie Intake:")
daily_calorie_intake_entry = tk.Entry(root)
daily_calorie_intake_label.grid(row=1, column=0, padx=10, pady=10)
daily_calorie_intake_entry.grid(row=1, column=1, padx=10, pady=10)

# Add more GUI components for dietary_preference and gender...
gender_label = tk.Label(root, text="Gender:")
gender_var = tk.StringVar(root)
gender_var.set("male")  # Default value
gender_menu = tk.OptionMenu(root, gender_var, "male", "female")
gender_label.grid(row=2, column=0, padx=10, pady=10)
gender_menu.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=20)

# Start the GUI main loop
root.mainloop()
 
def append_to_csv(file_name, data):
    try:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")
 
# Function to load data from CSV
def load_data(file_name):
    if not pd.os.path.exists(file_name):
        print(f"Error: File not found - {file_name}")
        return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist
 
    try:
        data = pd.read_csv(file_name, header=None)
        data.columns = ['Date', 'Calories', 'Protein', 'Carbs', 'Fats', 'Sugars']
        data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
        return data
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return pd.DataFrame()
 
def select_graph_type():
    print("Select the type of graph you want to view:")
    print("1. Bar Chart")
    print("2. Pie Chart")
    choice = int(input("Enter your choice (1-2) >> "))
    return choice
 
def plot_bar_chart(data, start_date, end_date):
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
 
    # Filter data for the specified period
    period_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]
 
    if period_data.empty:
        print(f"No data available for the period {start_date} to {end_date}.")
        return
 
    plt.figure(figsize=(10,6))
 
    # Summing up the data for the period
    carbs = period_data['Carbs'].sum()
    protein = period_data['Protein'].sum()
    fats = period_data['Fats'].sum()
    sugars = period_data['Sugars'].sum()
    total_macros = carbs + protein + fats + sugars
    macros = [carbs, protein, fats, sugars]
    categories = ['Carbs', 'Protein', 'Fats', 'Sugars']
   
    # Calculate percentages
    percentages = [(macro / total_macros) * 100 for macro in macros]
 
    # Plotting the bar chart for grams
    bars = plt.bar(categories, macros, color='teal')
 
    # Adding percentages as text labels on the bars
    for bar, percentage in zip(bars, percentages):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{percentage:.2f}%', va='bottom')
 
        # Draw horizontal lines for each macro
        plt.axhline(y=yval, color='grey', linestyle='--', alpha=0.7)
 
    plt.title(f'Daily Intake from {start_date} to {end_date}')
    plt.xlabel('Macros')
    plt.ylabel('Units (grams)')
 
    # Total calories for the selected period
    total_calories = period_data['Calories'].sum()
 
    # Displaying total calories as an annotation
    plt.annotate(f'Total Calories: {total_calories}',
                 xy=(0.75, 0.95),
                 xycoords='axes fraction',
                 fontsize=12,
                 bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1))
 
    plt.show()
 
def plot_pie_chart(data, selected_date):
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
 
    # Filter data for the selected day
    day_data = data[data['Date'] == pd.to_datetime(selected_date)]
 
    if day_data.empty:
        print(f"No data available for {selected_date}.")
        return
 
    # Retrieving data for the specific day
    carbs = day_data['Carbs'].iloc[0]
    protein = day_data['Protein'].iloc[0]
    fats = day_data['Fats'].iloc[0]
    sugars = day_data['Sugars'].iloc[0]
   
    macros = [carbs, protein, fats, sugars]
    labels = ['Carbs', 'Protein', 'Fats', 'Sugars']
 
    plt.figure(figsize=(8,8))
    plt.pie(macros, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Macro Nutrient Distribution for {selected_date}')
    plt.show()
 
def visualize_data(data):
    while True:
        # Prompt for the type of graph
        choice = select_graph_type()
 
        if choice == 1 or choice == 2:
            selected_date = input("Enter the date (YYYY-MM-DD) >> ")
            if choice == 1:
                # Use the same date for start and end for a single-day bar chart
                plot_bar_chart(data, selected_date, selected_date)
            elif choice == 2:
                plot_pie_chart(data, selected_date)
        else:
            print("Invalid choice")
 
        # Ask the user if they want to view another chart
        continue_choice = input("Do you want to view another chart? (yes/no) >> ").lower().strip()
 
        # Explicitly handle the response
        if continue_choice == "yes":
            continue
        elif continue_choice == "no":
            print("Exiting visualization function.")
            break
        else:
            print("Invalid input. Exiting visualization function.")
            break
 
# Example usage
file_name = 'Nutrition_Data(2).csv'
data = pd.read_csv(file_name, parse_dates=['Date'], names=['Date', 'Calories', 'Protein', 'Carbs', 'Fats', 'Sugars'])
visualize_data(data)
 
def load_data(file_name):
    if not os.path.exists(file_name):
        print(f"Error: File not found - {file_name}")
        return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist
 
    try:
        # Reading the CSV file without specifying header names
        data = pd.read_csv(file_name, header=None)
        # Assigning column names
        data.columns = ['Date', 'Calories', 'Protein', 'Carbs', 'Fats', 'Sugars']
        # Converting 'Date' column to datetime format
        data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
        return data
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of other errors
 
# Path to the uploaded file
file_name = 'Nutrition_Data(2).csv'
data = load_data(file_name)
# Now you can use this file_name in your existing functions
if not data.empty:
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    visualize_data(data)
 
def plot_progress_towards_goal(file_name, user_goal):
    data = load_data(file_name)
    if data.empty:
        return
   
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
   
    # Hardcoding the metric as 'Calories'
    metric = 'Calories'
    
    print("**LINEAR REGRESSION**")
    start_date_str = input("Enter the start date for the period (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date for the period (YYYY-MM-DD): ")
 
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)
   
    # Group by date and sum the values
    grouped_data = data.groupby('Date').sum().reset_index()
 
    user_data = grouped_data[(grouped_data['Date'] >= start_date) & (grouped_data['Date'] <= end_date)]
 
    if user_data.shape[0] < 2:
        print("Not enough data for regression analysis.")
        return
   
    user_data['Date_Ordinal'] = user_data['Date'].apply(lambda date: date.toordinal())
 
    model = LinearRegression()
    model.fit(user_data[['Date_Ordinal']], user_data[metric])
 
    prediction_dates = [end_date + timedelta(days=i) for i in range(1, 11)]
    prediction_ordinals = [d.toordinal() for d in prediction_dates]
    predicted_values = model.predict(pd.DataFrame({'Date_Ordinal': prediction_ordinals}))
 
    plt.figure(figsize=(10, 6))
    plt.scatter(user_data['Date'], user_data[metric], color='blue', label='Recorded Data')
    plt.plot(user_data['Date'], model.predict(user_data[['Date_Ordinal']]), color='red', label='Trend Line')
    plt.scatter(prediction_dates, predicted_values, color='green', label='Predicted Future Values')
 
    plt.title('Progress Towards Calorie Goal')
    plt.xlabel('Date')
    plt.ylabel('Calories')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
 
    for i, val in enumerate(predicted_values, 1):
        print(f"Day {i} prediction: {round(val, 2)}")
 
    return predicted_values
 
# Example usage
file_name = 'Nutrition_Data(2).csv'
user_goal = goals
predicted_values = plot_progress_towards_goal(file_name, user_goal)
 