import tkinter as tk
import PIL
from tkinter import ttk
from PIL import Image, ImageTk
import random

allowed_dislikes = [
    "tomaten", "kartoffeln", "brokkoli", "hähnchenbrust", "eiernudeln", "spinat", "zwiebeln",
    "knoblauch", "paprika", "lachs", "reis", "quinoa", "bananen", "erdbeeren", "möhren", "avocado",
    "rucola", "mozzarella", "olivenöl", "joghurt"]

dishes = [
    {"name": "Gemüsepfanne", "ingredients": ["Zucchini", "Paprika", "Tomaten", "Zwiebeln"], "calories": 185},
    {"name": "Hähnchen Curry", "ingredients": ["Hähnchenbrust", "Currypaste", "Kokosmilch", "Zwiebeln"], "calories": 350},
    {"name": "Veganer Salat", "ingredients": ["Quinoa", "Avocado", "Tomaten", "Rucola"], "calories": 275},
    {"name": "Quinoa Salat", "ingredients": ["Quinoa", "Spinat", "Avocado", "Kichererbsen"], "calories": 375},
    {"name": "Linsensuppe", "ingredients": ["Linsen", "Karotten", "Zwiebeln", "Sellerie"], "calories": 225},
    {"name": "Vegane Pizza", "ingredients": ["Teig", "Tomatensauce", "Veganer Käse", "Pilze", "Oliven"], "calories": 300},
    {"name": "Kürbisrisotto", "ingredients": ["Reis", "Kürbis", "Parmesan", "Zwiebeln"], "calories": 350},
    {"name": "Tofu Stir Fry", "ingredients": ["Tofu", "Brokkoli", "Paprika", "Sojasauce"], "calories": 225},
    {"name": "Avocado Toast", "ingredients": ["Brot", "Avocado", "Tomaten", "Rucola"], "calories": 275}
]

ingredients = [    "Quinoa", "Spinat", "Avocado", "Kichererbsen", "Linsen", "Karotten", "Zwiebeln", "Sellerie",
    "Teig", "Tomatensauce", "Veganer Käse", "Pilze", "Oliven", "Reis", "Kürbis", "Parmesan",
    "Tofu", "Brokkoli", "Paprika", "Sojasauce", "Brot", "Tomaten", "Rucola"
]
workouts = [
    {"name": "Yoga", "suitable_for": ["Rückenprobleme", "Stressabbau", "Migräne", "Schlafstörungen"]},
    {"name": "Gewichtheben", "suitable_for": ["Kraftaufbau", "Muskelaufbau"]},
    {"name": "Schwimmen", "suitable_for": ["Gelenkschmerzen", "Bluthochdruck", "Herzerkrankungen", "Asthma"]},
    {"name": "Pilates", "suitable_for": ["Flexibilität", "Rückenprobleme"]},
    {"name": "Crossfit", "suitable_for": ["Kraftaufbau", "Ausdauer"]},
    {"name": "Spinning", "suitable_for": ["Kalorienverbrennung", "Ausdauer", "Herzerkrankungen"]},
    {"name": "Wandern", "suitable_for": ["Stressabbau", "Gelenkschmerzen"]},
    {"name": "Zumba", "suitable_for": ["Spaß", "Kalorienverbrennung", "Diabetes"]},
    {"name": "Boxen", "suitable_for": ["Stressabbau", "Kraftaufbau"]},
    {"name": "Tai Chi", "suitable_for": ["Stressabbau", "Flexibilität", "Bluthochdruck", "Herzerkrankungen"]},
    {"name": "Aerobic", "suitable_for": ["Kalorienverbrennung", "Ausdauer", "Diabetes"]},
    {"name": "Nordic Walking", "suitable_for": ["Gelenkschmerzen", "Herzerkrankungen", "Diabetes"]},
    {"name": "Aquafitness", "suitable_for": ["Gelenkschmerzen", "Herzerkrankungen", "Asthma"]},
    {"name": "Radsport", "suitable_for": ["Ausdauer", "Herzerkrankungen", "Bluthochdruck"]},
    {"name": "Leichtathletik", "suitable_for": ["Kraftaufbau", "Ausdauer", "Diabetes"]},
    {"name": "Gymnastik", "suitable_for": ["Flexibilität", "Rückenprobleme", "Magen-Darm-Beschwerden"]}
]
def valid_food_dislike(dislike, error_label):
    if dislike.lower() not in allowed_dislikes:
        error_label.config(text="Fehler: Diese Zutat ist nicht erlaubt.")
        return False
    error_label.config(text="")
    return True
def valid_goal(goal):
    return goal in ["Fit", "Zunehmen", "Abnehmen"]
def valid_age(age):
    try:
        age = int(age)
        return 0 < age < 100
    except ValueError:
        return False
def valid_weight(weight):
    try:
        weight = float(weight)
        return 0 < weight < 300
    except ValueError:
        return False

def valid_height(height):
    try:
        height = int(height)
        return 0 < height < 250
    except ValueError:
        return False
def valid_name(name):
    return name.isalpha() and len(name) < 50

def on_resize(event):
    global width, height
    width = event.width
    height = event.height

def set_image_background(frame, image_path):
    def resize_background(event=None):
        try:
            new_image = Image.open(image_path)
            new_image = new_image.resize((frame.winfo_width(), frame.winfo_height()), Image.BICUBIC)
            photo = ImageTk.PhotoImage(new_image)
            background_label.config(image=photo)
            background_label.image = photo
        except Exception as e:
            print(f"Fehler beim Hochladen des Bildes: {e}")

    background_label = tk.Label(frame)
    background_label.place(relwidth=1, relheight=1)

    frame.bind("<Configure>", resize_background)

    resize_background()

def show_frame(frame):
    frame.tkraise()

def go_back(current_frame, previous_frame):
    current_frame.withdraw()
    previous_frame.deiconify()

def calculate_calorie_needs(bmr, goal):
    if goal == "Fit":
        return bmr
    elif goal == "Zunehmen":
        return bmr * 1.1
    elif goal == "Abnehmen":
        return bmr * 0.9
def filter_dishes(dishes, disliked_food, max_calories):
    lower_dislikes = [dislike.lower() for dislike in disliked_food]

    filtered_dishes = [
        dish for dish in dishes
        if not any(dislike in [ingredient.lower() for ingredient in dish['ingredients']] for dislike in lower_dislikes)
    ]

    sorted_dishes = sorted(filtered_dishes, key=lambda x: x['calories'], reverse=True)

    selected_dishes = []
    total_calories = 0

    for dish in sorted_dishes:
        if total_calories + dish['calories'] <= max_calories:
            selected_dishes.append(dish)
            total_calories += dish['calories']

    if total_calories < max_calories:
        for dish in sorted_dishes:
            if dish not in selected_dishes:
                potential_addition = total_calories + dish['calories']
                if potential_addition <= max_calories:

                    for selected in selected_dishes:
                        if potential_addition - selected['calories'] >= total_calories:
                            selected_dishes.remove(selected)
                            selected_dishes.append(dish)
                            total_calories = total_calories + dish['calories'] - selected['calories']
                            break
                if total_calories >= max_calories:
                    break

    output_dishes_info = {
        "dishes":selected_dishes,
        "total_calories": total_calories,
        "max_calories": max_calories
    }

    return output_dishes_info
def filter_ingredients(ingredients, disliked_food):
    lower_dislikes = [dislike.lower() for dislike in disliked_food]
    return [
        ingredient for ingredient in ingredients
        if ingredient.lower() not in lower_dislikes
    ]

def filter_workouts(workouts, restrictions):
    return [
        workout for workout in workouts
        if all(restriction.lower() in [suitable.lower() for suitable in workout['suitable_for']] for restriction in restrictions)
    ]
def calculate_bmr(geschlecht, gewicht, körpergröße, alter):
    gewicht = float(gewicht)
    körpergröße = float(körpergröße)
    alter = int(alter)
    if geschlecht == 'Männlich':
        bmr = 88.362 + (13.397 * gewicht) + (4.799 * körpergröße) - (5.677 * alter)
    elif geschlecht == 'Weiblich':
        bmr = 447.593 + (9.247 * gewicht) + (3.098 * körpergröße) - (4.330 * alter)
    else:
        bmr_male = 88.362 + (13.397 * gewicht) + (4.799 * körpergröße) - (5.677 * alter)
        bmr_female = 447.593 + (9.247 * gewicht) + (3.098 * körpergröße) - (4.330 * alter)
        bmr = (bmr_male + bmr_female) / 2
    return bmr

def show_plan(goal):
    bmr = calculate_bmr(user_data['gender'], user_data['weight'], user_data['height'], user_data['age'])
    calorie_needs = calculate_calorie_needs(bmr, goal)

    suitable_dishes = filter_dishes(dishes, user_data['disliked_food'], max_calories)
    suitable_workouts = filter_workouts(workouts, user_data['restrictions'])

    plan_label = tk.Label(root, text=f"Plan für {goal}", font=("Helvetica", 12, "bold"))
    plan_label.pack()
    calorie_label = tk.Label(root, text=f"Kalorienbedarf: {calorie_needs}", font=("Helvetica", 10))
    calorie_label.pack()
    dishes_label = tk.Label(root, text=f"Geeignete Gerichte: {[dish['name'] for dish in suitable_dishes]}", font=("Helvetica", 10))
    dishes_label.pack()
    workouts_label = tk.Label(root, text=f"Geeignete Workouts: {[workout['name'] for workout in suitable_workouts]}", font=("Helvetica", 10))
    workouts_label.pack()

def show_goal_selection(user_data):

    if not all(user_data.values()):
        label.config(text="Bitte füllen Sie alle Felder aus", font=("Helvetica", 12, "bold"))
        return

    user_name = user_data["Name"]
    user_age = user_data["Alter"]
    user_weight = user_data["Gewicht"]
    user_height = user_data["Körpergröße"]

    if not valid_name(user_name):
        label.config(text="Bitte geben Sie nur einen gültigen Name ein", font=("Helvetica", 12, "bold"))
        return
    if not valid_age(user_age):
        label.config(text="Bitte geben Sie ein gültiges Alter ein", font=("Helvetica", 12, "bold"))
        return
    if not valid_weight(user_weight):
        label.config(text="Bitte geben Sie ein gültiges Gewicht ein", font=("Helvetica", 12, "bold"))
        return
    if not valid_height(user_height):
        label.config(text="Bitte geben Sie eine gültige Körpergröße ein", font=("Helvetica", 12, "bold"))
        return

    goal_frame = tk.Toplevel(root)
    goal_frame.title("Ziel Auswahl")
    goal_frame.geometry("1200x800")
    set_image_background(goal_frame, r"logo2.jpeg")

    goal_label = tk.Label(goal_frame, text="Wählen Sie Ihr Ziel:", font=("Helvetica", 25, "bold"))
    goal_label.pack(pady=20)

    goal_options = ["Fit", "Zunehmen", "Abnehmen"]
    goal_var = tk.StringVar()
    goal_var.set(goal_options[0])

    def open_goal_panel():
        selected_goal = goal_var.get()

        if valid_goal(selected_goal):
            bmr = calculate_bmr(user_data["Geschlecht"], float(user_data["Gewicht"]), int(user_data["Körpergröße"]),
                                int(user_data["Alter"]))
            calorie_needs = calculate_calorie_needs(bmr, selected_goal)
            goal_frame.withdraw()

            if selected_goal == "Fit":
                show_fit_panel(user_data, goal_frame)
            elif selected_goal == "Zunehmen":
                show_gain_weight_panel(user_data, goal_frame)
            elif selected_goal == "Abnehmen":
                show_lose_weight_panel(user_data, goal_frame)
        else:
            label.config(text="Ungültiges Ziel ausgewählt", font=("Helvetica", 20, "bold"))

    for goal_option in goal_options:
        goal_button = tk.Radiobutton(goal_frame, text=goal_option, variable=goal_var, value=goal_option,
                                     font=("Helvetica", 20))
        goal_button.pack()

    back_button = tk.Button(goal_frame, text="Zurück", command=lambda: go_back(goal_frame, root))
    back_button.pack(pady=40)

    confirm_button = tk.Button(goal_frame, text="Bestätigen", command=open_goal_panel)
    confirm_button.pack(pady=10)
def generate_single_dish_plan(user_data, calorie_needs):
    max_calories = calorie_needs
    disliked_food = user_data.get('Disliked Food', [])
    dishes_info = filter_dishes(dishes, disliked_food, max_calories)

    if dishes_info['dishes']:
        single_dish_frame = tk.Toplevel(root)
        single_dish_frame.title("Einzelnes Gericht Plan")
        single_dish_frame.geometry("500x350")
        set_image_background(single_dish_frame, r"logo2.jpeg")

        selected_dish = random.choice(dishes_info['dishes'])
        tk.Label(single_dish_frame, text=f"Ausgewähltes Gericht: {selected_dish['name']} ({selected_dish['calories']} kcal)", font=("Helvetica", 12)).pack(pady=10)

        if user_data.get("Disliked Food"):
            disliked_food_text = "Nicht gemochte Lebensmittel: " + ', '.join(user_data["Disliked Food"])
            tk.Label(single_dish_frame, text=disliked_food_text, font=("Helvetica", 12)).pack(pady=5)

        back_button = tk.Button(single_dish_frame, text="Zurück", command=single_dish_frame.destroy)
        back_button.pack(pady=10)
    else:
        tk.Label(single_dish_frame, text="Keine geeigneten Gerichte gefunden", font=("Helvetica", 12)).pack(pady=10)

def generate_fit_panel(user_data, option1, option2, disliked_food, physical_limitations=None, goal_weight=None):
    print("Generating Fit Plan")
    bmr = calculate_bmr(user_data["Geschlecht"], user_data["Gewicht"], user_data["Körpergröße"], user_data["Alter"])
    calorie_needs = calculate_calorie_needs(bmr, "Fit")

    if option1 == "Einzelnes Gericht":
        generate_single_dish_plan(user_data, calorie_needs)
    elif option1 == "Diätplan":
        generate_diet_plan(user_data, calorie_needs)
    elif option1 == "Sportplan":
        generate_sport_plan(user_data, calorie_needs)

def generate_diet_plan(user_data, calorie_needs):
    disliked_food = user_data.get('Disliked Food', [])
    dishes_info = filter_dishes(dishes, disliked_food, calorie_needs)

    plan_frame = tk.Toplevel(root)
    plan_frame.title("Diätplan")
    plan_frame.geometry("800x600")
    set_image_background(plan_frame, r"logo2.jpeg")

    tk.Label(plan_frame, text="Ihr Diätplan", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(plan_frame, text=f"Gesamtkalorien: {dishes_info['total_calories']} von max. {dishes_info['max_calories']} kcal", font=("Helvetica", 12)).pack(pady=5)

    for dish in dishes_info['dishes']:
        tk.Label(plan_frame, text=f"{dish['name']} ({dish['calories']} kcal)", font=("Helvetica", 10)).pack()

    if not dishes_info['dishes']:
        tk.Label(plan_frame, text="Keine geeigneten Gerichte gefunden", font=("Helvetica", 10)).pack()

    back_button = tk.Button(plan_frame, text="Zurück", command=plan_frame.destroy)
    back_button.pack(pady=10)

def generate_sport_plan(user_data, calorie_needs):

    restrictions = user_data.get('Physical Limitations', [])
    suitable_workouts = filter_workouts(workouts, restrictions)

    plan_frame = tk.Toplevel(root)
    plan_frame.title("Sportplan")
    plan_frame.geometry("800x600")
    set_image_background(plan_frame, r"logo2.jpeg")

    tk.Label(plan_frame, text="Ihr Sportplan", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(plan_frame, text=f"Kalorienbedarf: {calorie_needs} kcal", font=("Helvetica", 12)).pack(pady=5)

    for workout in suitable_workouts:
        tk.Label(plan_frame, text=workout, font=("Helvetica", 10)).pack()

    if not suitable_workouts:
        tk.Label(plan_frame, text="Keine geeigneten Workouts gefunden", font=("Helvetica", 10)).pack()

    back_button = tk.Button(plan_frame, text="Zurück", command=lambda: go_back(plan_frame, root))
    back_button.pack(pady=10)

def show_plan_panel_with_calorie_needs(user_data, goal, previous_frame):
    bmr = calculate_bmr(user_data['gender'], user_data['weight'], user_data['height'], user_data['age'])
    calorie_needs = calculate_calorie_needs(bmr, goal)

    suitable_dishes = filter_dishes(dishes, user_data['disliked_food'] if 'disliked_food' in user_data else [], max_calories)
    suitable_workouts = filter_workouts(workouts, user_data['restrictions'] if 'restrictions' in user_data else [])

    plan_frame = tk.Toplevel(previous_frame)
    plan_frame.title(f"Plan für {goal}")
    plan_frame.geometry("800x600")
    set_image_background(plan_frame, r"logo2.jpeg")

    tk.Label(plan_frame, text=f"Planname: {goal} Plan", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(plan_frame, text=f"Kalorienbedarf: {calorie_needs} kcal", font=("Helvetica", 12)).pack(pady=5)

    if 'disliked_food' in user_data and user_data['disliked_food']:
        tk.Label(plan_frame, text="Nicht gemochte Lebensmittel: " + ", ".join(user_data['disliked_food']),
                 font=("Helvetica", 10)).pack(pady=5)

    if 'restrictions' in user_data and user_data['restrictions']:
        tk.Label(plan_frame, text="Körperliche Einschränkungen: " + ", ".join(user_data['restrictions']),
                 font=("Helvetica", 10)).pack(pady=5)

    if goal in ["Einzelnes Gericht", "Beides", "Diätplan"]:
        tk.Label(plan_frame, text="Geeignete Gerichte:", font=("Helvetica", 12, "bold")).pack(pady=5)
        for dish in suitable_dishes:
            tk.Label(plan_frame, text=dish, font=("Helvetica", 10)).pack()

    if goal in ["Sportplan", "Beides"]:
        tk.Label(plan_frame, text="Geeignete Workouts:", font=("Helvetica", 12, "bold")).pack(pady=5)
        for workout in suitable_workouts:
            tk.Label(plan_frame, text=workout, font=("Helvetica", 10)).pack()

    back_button = tk.Button(plan_frame, text="Zurück", command=lambda: go_back(plan_frame, previous_frame))
    back_button.pack(pady=10)

def show_fit_panel(user_data, previous_frame):
    def go_back(current_frame, previous_frame):
        current_frame.withdraw()
        previous_frame.deiconify()

    def validate_list_input(input_string, valid_items=None):
        if not input_string:
            return [], []

        items = [item.strip().capitalize() for item in input_string.split(',')]
        valid_items_lower = [item.lower() for item in valid_items] if valid_items else []

        error_messages = []
        for item in items:
            if not any(char.isalpha() for char in item):
                error_messages.append(
                    f"Ungültige Eingabe. Bitte stellen Sie sicher,\n dass jede Zutat existiert und keine Zahlen enthält.")
            elif item.lower() not in valid_items_lower:
                allowed_items_formatted = "\n - ".join(valid_items)
                error_messages.append(
                    f"Ungültige Zutat: {item}.\n Erlaubte Zutaten sind:\n - {allowed_items_formatted}")

        return items if not error_messages else None, error_messages


    def validate_food_input():
        disliked_food = dislike_food_entry.get().strip()
        error_label.config(text="")

        if disliked_food:
            valid_disliked_food, error_messages_disliked_food = validate_list_input(
                disliked_food,
                valid_items=["Tomaten", "Kartoffeln", "Brokkoli", "Hähnchenbrust", "Eiernudeln", "Spinat", "Zwiebeln",
                             "Knoblauch", "Paprika", "Lachs", "Reis", "Quinoa", "Bananen", "Erdbeeren", "Möhren",
                             "Avocado", "Rucola", "Mozzarella", "Olivenöl", "Joghurt"])

            if error_messages_disliked_food:
                error_label.config(text='\n'.join(error_messages_disliked_food), fg="red", wraplength= 200)
            else:
                error_label.config(text="")

                user_data['Disliked Food'] = valid_disliked_food

                generate_fit_panel(user_data, fit_var.get(), None, valid_disliked_food)
                fit_frame.withdraw()

        else:
            generate_fit_panel(user_data, fit_var.get(), None, None)
            fit_frame.withdraw()

    def update_combobox_color(*args):
        if fit_var.get() == "Einzelnes Gericht":
            fit_combobox.configure(style="Green.TCombobox")
        else:
            fit_combobox.configure(style="TCombobox")

    fit_frame = tk.Toplevel(root)
    fit_frame.title("Fit Panel")
    fit_frame.geometry("1000x700")
    fit_frame.bind("<Configure>", on_resize)
    set_image_background(fit_frame, r"logo2.jpeg")

    fit_label = tk.Label(fit_frame, text=f"Willkommen, {user_data['Name']}!", font=("Helvetica", 12, "bold"))
    fit_label.pack(pady=10)

    fit_options_label = tk.Label(fit_frame, text="Wählen Sie Ihre Option:", font=("Helvetica", 11, "bold"))
    fit_options_label.pack(pady=5)

    fit_options = ["Einzelnes Gericht", "Diätplan"]
    fit_var = tk.StringVar()
    fit_var.set(fit_options[0])

    fit_combobox = ttk.Combobox(fit_frame, values=fit_options, textvariable=fit_var, font=("Helvetica", 11, "bold"))
    fit_combobox.pack(pady=10)

    fit_var.trace_add("write", update_combobox_color)

    dislike_food_label = tk.Label(fit_frame, text="Welche Lebensmittel mögen Sie nicht?", font=("Helvetica", 11, "bold"))
    dislike_food_label.pack(pady=5)

    dislike_food_entry = tk.Entry(fit_frame, font=("Helvetica", 11, "bold"))
    dislike_food_entry.pack(pady=5)

    error_label = tk.Label(fit_frame, text='', fg='red')
    error_label.pack(pady=10)

    back_button = tk.Button(fit_frame, text="Zurück", command=lambda: go_back(fit_frame, previous_frame))
    back_button.pack(pady=10)
    confirm_button = tk.Button(fit_frame, text="Bestätigen", command=validate_food_input)
    confirm_button.pack(pady=10)

    update_combobox_color()

def show_gain_weight_panel(user_data, previous_frame):
    global gain_weight_var1, gain_weight_var2, gain_weight_var3, physical_limitations_checkboxes, dislike_food_entry, error_weight_label, error_food_label

    def go_back(current_frame, previous_frame):
        current_frame.withdraw()
        previous_frame.deiconify()
    def display_saved_inputs(user_data, new_frame, option1, option2, calorie_needs):
        saved_inputs_label = tk.Label(new_frame, text="Gespeicherte Eingaben:", font=("Helvetica", 12, "bold"))
        saved_inputs_label.pack(pady=10)

        if user_data.get("Physical Limitations"):
            limitations_text = "Ausgewählte körperliche Einschränkungen: " + ', '.join(
                user_data["Physical Limitations"])
            tk.Label(new_frame, text=limitations_text, font=("Helvetica", 12)).pack(pady=5)

        if user_data.get("Disliked Food"):
            disliked_food_text = "Nicht gemochte Lebensmittel: " + ', '.join(user_data["Disliked Food"])
            tk.Label(new_frame, text=disliked_food_text, font=("Helvetica", 12)).pack(pady=5)

        bmr = calculate_bmr(user_data["Geschlecht"], user_data["Gewicht"], user_data["Körpergröße"], user_data["Alter"])
        calorie_needs = calculate_calorie_needs(bmr, "Zunehmen")
        calorie_needs_label = tk.Label(new_frame, text=f"Kalorienbedarf: {calorie_needs:.2f} kcal",
                                       font=("Helvetica", 12))
        calorie_needs_label.pack(pady=10)

    def confirm_gain_weight_panel(user_data, option1, option2, disliked_food, goal_weight):
        global valid_disliked_food

        error_weight_label.config(text="")
        if goal_weight is None or goal_weight.strip() == "":
            error_weight_label.config(text="Wunschgewicht darf nicht leer sein", fg="red")
            return

        try:
            goal_weight = float(goal_weight)
            if not (0 < float(user_data["Gewicht"]) < goal_weight < 300):
                error_weight_label.config(text="Ungültiges Wunschgewicht", fg="red")
                return
        except ValueError:
            error_weight_label.config(text="Ungültiges Wunschgewicht", fg="red")
            return

        bmr = calculate_bmr(user_data["Geschlecht"], user_data["Gewicht"], user_data["Körpergröße"], user_data["Alter"])
        calorie_needs = calculate_calorie_needs(bmr, "Zunehmen")

        selected_physical_limitations = [checkbox.cget("text") for checkbox in physical_limitations_checkboxes if
                                         checkbox.var.get()]
        user_data["Physical Limitations"] = selected_physical_limitations

        valid_disliked_food, error_messages_disliked_food = validate_list_input(
            disliked_food, valid_items=allowed_dislikes)
        if error_messages_disliked_food:
            error_food_label.config(text='\n'.join(error_messages_disliked_food), fg="red", justify=tk.LEFT, wraplength=200)
            return
        user_data["Disliked Food"] = valid_disliked_food

        user_data["Option1"] = option1
        user_data["Option2"] = option2
        user_data["Goal Weight"] = goal_weight

        new_frame = tk.Toplevel(root)
        new_frame.title("Gain Weight")
        new_frame.geometry("800x600")
        set_image_background(new_frame, r"logo2.jpeg")

        display_saved_inputs(user_data, new_frame, option1, option2, calorie_needs)

        if gain_weight_var1.get():
            generate_sport_plan(user_data, calorie_needs)
        if gain_weight_var2.get():
            generate_diet_plan(user_data, calorie_needs)

        generate_fit_plan(user_data, option1, option2, valid_disliked_food, goal_weight)

        new_frame.withdraw()

    def validate_list_input(input_string, valid_items=None):
        if not input_string:
            return [], []

        items = [item.strip().capitalize() for item in input_string.split(',')]
        valid_items_lower = [item.lower() for item in valid_items] if valid_items else []

        error_messages = []
        for item in items:
            if not any(char.isalpha() for char in item):
                error_messages.append(
                    f"Ungültige Eingabe. Bitte stellen Sie sicher,\n dass jede Zutat existiert und keine Zahlen enthält.")
            elif item.lower() not in valid_items_lower:
                allowed_items_formatted = "\n - ".join(valid_items)
                error_messages.append(
                    f"Ungültige Zutat: {item}.\n Erlaubte Zutaten sind:\n - {allowed_items_formatted}")

        return items if not error_messages else None, error_messages

    gain_weight_frame = tk.Toplevel(root)
    gain_weight_frame.title("Zunehmen Panel")
    gain_weight_frame.geometry("1000x700")
    set_image_background(gain_weight_frame, r"logo2.jpeg")

    gain_weight_label = tk.Label(gain_weight_frame, text=f"{user_data['Name']}, wie möchten Sie zunehmen?",
                                 font=("Helvetica", 12, "bold"))
    gain_weight_label.pack(pady=10)
    gain_weight_goal_label = tk.Label(gain_weight_frame, text="Wunschgewicht (in kg):",
                                      font=("Helvetica", 11, "bold"))
    gain_weight_goal_label.pack(pady=5)
    gain_weight_entry = tk.Entry(gain_weight_frame, font=("Helvetica", 11, "bold"))
    gain_weight_entry.pack(pady=5)
    mandatory_label_weight = tk.Label(gain_weight_frame, text="*", font=("Helvetica", 11, "bold"), fg="red")
    mandatory_label_weight.pack(pady=5, padx=2)
    gain_weight_options_label = tk.Label(gain_weight_frame, text="Wählen Sie Ihre Optionen:",
                                         font=("Helvetica", 11, "bold"))
    gain_weight_options_label.pack(pady=5)
    gain_weight_options = ["Sportplan", "Diätplan", "Beides"]
    gain_weight_var1 = tk.BooleanVar()
    gain_weight_var2 = tk.BooleanVar()
    gain_weight_var3 = tk.BooleanVar()
    physical_limitations_checkboxes = []
    left_frame = tk.Frame(gain_weight_frame)
    right_frame = tk.Frame(gain_weight_frame)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    physical_limitations_label = tk.Label(left_frame, text="Haben Sie körperliche Einschränkungen?",
                                          font=("Helvetica", 11, "bold"))

    physical_limitations_choices = ["Herzprobleme", "Rückenprobleme", "Knieprobleme", "Armprobleme",
                                    "Diabetes", "Asthma", "Bluthochdruck", "Magen-Darm-Beschwerden",
                                    "Migräne", "Schlafstörungen"]
    physical_limitations_label.pack(padx=10, pady=10)

    physical_limitations_checkboxes = []
    for limitation in physical_limitations_choices:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(left_frame, text=limitation, font=("Helvetica", 11, "bold"), variable=var)
        checkbox.var = var
        physical_limitations_checkboxes.append(checkbox)
        checkbox.pack(anchor='w')

    dislike_food_label = tk.Label(right_frame, text="Welche Lebensmittel mögen Sie nicht?",
                                  font=("Helvetica", 11, "bold"))
    dislike_food_label.pack(padx=10, pady=10)
    dislike_food_entry = tk.Entry(right_frame, font=("Helvetica", 11, "bold"))
    dislike_food_entry.pack(padx=10, pady=10)

    error_weight_label = tk.Label(gain_weight_frame, text='', fg='red')
    error_weight_label.pack(pady=10)
    error_food_label = tk.Label(gain_weight_frame, text='', fg='red')
    error_food_label.pack(pady=10)

    allowed_dislikes = ["Tomaten", "Kartoffeln", "Brokkoli", "Hähnchenbrust", "Eiernudeln", "Spinat", "Zwiebeln",
                        "Knoblauch", "Paprika", "Lachs", "Reis", "Quinoa", "Bananen", "Erdbeeren", "Möhren",
                        "Avocado", "Rucola", "Mozzarella", "Olivenöl", "Joghurt"]

    def toggle_questions():
        if gain_weight_var1.get():
            for checkbox in physical_limitations_checkboxes:
                checkbox.pack(anchor='w')
        else:
            for checkbox in physical_limitations_checkboxes:
                checkbox.pack_forget()

        if gain_weight_var2.get():
            dislike_food_label.pack(padx=10, pady=10)
            dislike_food_entry.pack(padx=10, pady=10)
        else:
            dislike_food_label.pack_forget()
            dislike_food_entry.pack_forget()

    gain_weight_var1.trace_add('write', lambda name, index, mode: toggle_questions())
    gain_weight_var2.trace_add('write', lambda name, index, mode: toggle_questions())

    def update_checkboxes():
        if gain_weight_var1.get() and gain_weight_var2.get():
            gain_weight_var3.set(True)
        else:
            gain_weight_var3.set(False)

    options_frame = tk.Frame(gain_weight_frame)
    options_frame.pack(pady=10)

    gain_weight_checkbox1 = tk.Checkbutton(options_frame, text=gain_weight_options[0], variable=gain_weight_var1,
                                           font=("Helvetica", 11, "bold"), command=update_checkboxes)
    gain_weight_checkbox2 = tk.Checkbutton(options_frame, text=gain_weight_options[1], variable=gain_weight_var2,
                                           font=("Helvetica", 11, "bold"), command=update_checkboxes)
    gain_weight_checkbox3 = tk.Checkbutton(options_frame, text=gain_weight_options[2], variable=gain_weight_var3,
                                           font=("Helvetica", 11, "bold"), state=tk.DISABLED)
    gain_weight_checkbox1.pack(side=tk.LEFT, padx=10)
    gain_weight_checkbox2.pack(side=tk.LEFT, padx=10)
    gain_weight_checkbox3.pack(side=tk.LEFT, padx=10)
    back_button = tk.Button(gain_weight_frame, text="Zurück",
                            command=lambda: go_back(gain_weight_frame, previous_frame))
    back_button.pack(pady=10)

    confirm_button = tk.Button(gain_weight_frame, text="Bestätigen",
                               command=lambda: confirm_gain_weight_panel(user_data, gain_weight_options[0],
                                                                         gain_weight_options[1],
                                                                         dislike_food_entry.get(),
                                                                         gain_weight_entry.get()))
    confirm_button.pack(pady=10)
def show_lose_weight_panel(user_data, previous_frame):
    global lose_weight_var1, lose_weight_var2, lose_weight_var3, physical_limitations_checkboxes, dislike_food_entry, error_weight_label, error_food_label

    def go_back(current_frame, previous_frame):
        current_frame.withdraw()
        previous_frame.deiconify()
    def display_saved_inputs(user_data, new_frame, option1, option2, calorie_needs):
        saved_inputs_label = tk.Label(new_frame, text="Gespeicherte Eingaben:", font=("Helvetica", 12, "bold"))
        saved_inputs_label.pack(pady=10)

        if user_data.get("Physical Limitations"):
            limitations_text = "Ausgewählte körperliche Einschränkungen: " + ', '.join(
                user_data["Physical Limitations"])
            tk.Label(new_frame, text=limitations_text, font=("Helvetica", 12)).pack(pady=5)

        if user_data.get("Disliked Food"):
            disliked_food_text = "Nicht gemochte Lebensmittel: " + ', '.join(user_data["Disliked Food"])
            tk.Label(new_frame, text=disliked_food_text, font=("Helvetica", 12)).pack(pady=5)

        bmr = calculate_bmr(user_data["Geschlecht"], user_data["Gewicht"], user_data["Körpergröße"], user_data["Alter"])
        calorie_needs = calculate_calorie_needs(bmr, "Abnehmen")
        calorie_needs_label = tk.Label(new_frame, text=f"Kalorienbedarf: {calorie_needs:.2f} kcal",
                                       font=("Helvetica", 12))
        calorie_needs_label.pack(pady=10)

    def confirm_lose_weight_panel(user_data, option1, option2, disliked_food, goal_weight):
        global valid_disliked_food

        error_weight_label.config(text="")
        if goal_weight is None or goal_weight.strip() == "":
            error_weight_label.config(text="Wunschgewicht darf nicht leer sein", fg="red")
            return

        try:
            goal_weight = float(goal_weight)
            if not (0 < float(user_data["Gewicht"]) > goal_weight < 300):
                error_weight_label.config(text="Ungültiges Wunschgewicht", fg="red")
                return
        except ValueError:
            error_weight_label.config(text="Ungültiges Wunschgewicht", fg="red")
            return

        bmr = calculate_bmr(user_data["Geschlecht"], user_data["Gewicht"], user_data["Körpergröße"], user_data["Alter"])
        calorie_needs = calculate_calorie_needs(bmr, "Abnehmen")


        error_weight_label.config(text="")

        selected_physical_limitations = [checkbox.cget("text") for checkbox in physical_limitations_checkboxes if checkbox.var.get()]
        user_data["Physical Limitations"] = selected_physical_limitations
        valid_disliked_food, error_messages_disliked_food = validate_list_input(
            disliked_food, valid_items=allowed_dislikes)
        if error_messages_disliked_food:
            error_food_label.config(text='\n'.join(error_messages_disliked_food), fg="red", justify=tk.LEFT, wraplength=200)
            return

        user_data["Disliked Food"] = valid_disliked_food

        user_data["Option1"] = option1
        user_data["Option2"] = option2
        user_data["Goal Weight"] = goal_weight

        new_frame = tk.Toplevel(root)
        new_frame.title("Lose Weight")
        new_frame.geometry("800x600")
        set_image_background(new_frame, r"logo2.jpeg")

        display_saved_inputs(user_data, new_frame, option1, option2, calorie_needs)

        if lose_weight_var1.get():
            generate_sport_plan(user_data, calorie_needs)
        if lose_weight_var2.get():
            generate_diet_plan(user_data, calorie_needs)

        generate_fit_plan(user_data, option1, option2, valid_disliked_food, goal_weight)

        new_frame.withdraw()

    def validate_list_input(input_string, valid_items=None):
        if not input_string:
            return [], []

        items = [item.strip().capitalize() for item in input_string.split(',')]
        valid_items_lower = [item.lower() for item in valid_items] if valid_items else []

        error_messages = []
        for item in items:
            if not any(char.isalpha() for char in item):
                error_messages.append(
                    f"Ungültige Eingabe. Bitte stellen Sie sicher,\n dass jede Zutat existiert und keine Zahlen enthält.")
            elif item.lower() not in valid_items_lower:
                allowed_items_formatted = "\n - ".join(valid_items)
                error_messages.append(
                    f"Ungültige Zutat: {item}.\n Erlaubte Zutaten sind:\n - {allowed_items_formatted}")

        return items if not error_messages else None, error_messages

    lose_weight_frame = tk.Toplevel(root)
    lose_weight_frame.title("Abnehmen Panel")
    lose_weight_frame.geometry("1000x700")
    set_image_background(lose_weight_frame, r"logo2.jpeg")


    lose_weight_label = tk.Label(lose_weight_frame, text=f"{user_data['Name']}, wie möchten Sie abnehmen?",
                                 font=("Helvetica", 12, "bold"))
    lose_weight_label.pack(pady=10)
    lose_weight_goal_label = tk.Label(lose_weight_frame, text="Wunschgewicht (in kg):",
                                      font=("Helvetica", 11, "bold"))
    lose_weight_goal_label.pack(pady=5)
    lose_weight_entry = tk.Entry(lose_weight_frame, font=("Helvetica", 11, "bold"))
    lose_weight_entry.pack(pady=5)
    mandatory_label_weight = tk.Label(lose_weight_frame, text="*", font=("Helvetica", 11, "bold"), fg="red")
    mandatory_label_weight.pack(pady=5, padx=2)
    lose_weight_options_label = tk.Label(lose_weight_frame, text="Wählen Sie Ihre Optionen:",
                                         font=("Helvetica", 11, "bold"))
    lose_weight_options_label.pack(pady=5)
    lose_weight_options = ["Sportplan", "Diätplan", "Beides"]
    lose_weight_var1 = tk.BooleanVar()
    lose_weight_var2 = tk.BooleanVar()
    lose_weight_var3 = tk.BooleanVar()
    physical_limitations_checkboxes = []
    left_frame = tk.Frame(lose_weight_frame)
    right_frame = tk.Frame(lose_weight_frame)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    physical_limitations_label = tk.Label(left_frame, text="Haben Sie körperliche Einschränkungen?",
                                          font=("Helvetica", 11, "bold"))

    physical_limitations_choices = ["Herzprobleme", "Rückenprobleme", "Knieprobleme", "Armprobleme",
                                    "Diabetes", "Asthma", "Bluthochdruck", "Magen-Darm-Beschwerden",
                                    "Migräne", "Schlafstörungen"]
    physical_limitations_label.pack(padx=10, pady=10)

    physical_limitations_checkboxes = []
    for limitation in physical_limitations_choices:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(left_frame, text=limitation, font=("Helvetica", 11, "bold"), variable=var)
        checkbox.var = var
        physical_limitations_checkboxes.append(checkbox)
        checkbox.pack(anchor='w')

    dislike_food_label = tk.Label(right_frame, text="Welche Lebensmittel mögen Sie nicht?",
                                  font=("Helvetica", 11, "bold"))
    dislike_food_label.pack(padx=10, pady=10)
    dislike_food_entry = tk.Entry(right_frame, font=("Helvetica", 11, "bold"))
    dislike_food_entry.pack(padx=10, pady=10)

    error_weight_label = tk.Label(lose_weight_frame, text='', fg='red')
    error_weight_label.pack(pady=10)
    error_food_label = tk.Label(lose_weight_frame, text='', fg='red')
    error_food_label.pack(pady=10)

    allowed_dislikes = ["Tomaten", "Kartoffeln", "Brokkoli", "Hähnchenbrust", "Eiernudeln", "Spinat", "Zwiebeln",
                        "Knoblauch", "Paprika", "Lachs", "Reis", "Quinoa", "Bananen", "Erdbeeren", "Möhren",
                        "Avocado", "Rucola", "Mozzarella", "Olivenöl", "Joghurt"]

    def toggle_questions():
        if lose_weight_var1.get():
            for checkbox in physical_limitations_checkboxes:
                checkbox.pack(anchor='w')
        else:
            for checkbox in physical_limitations_checkboxes:
                checkbox.pack_forget()

        if lose_weight_var2.get():
            dislike_food_label.pack(padx=10, pady=10)
            dislike_food_entry.pack(padx=10, pady=10)
        else:
            dislike_food_label.pack_forget()
            dislike_food_entry.pack_forget()

    lose_weight_var1.trace_add('write', lambda name, index, mode: toggle_questions())
    lose_weight_var2.trace_add('write', lambda name, index, mode: toggle_questions())

    def update_checkboxes():
        if lose_weight_var1.get() and lose_weight_var2.get():
            lose_weight_var3.set(True)
        else:
            lose_weight_var3.set(False)

    options_frame = tk.Frame(lose_weight_frame)
    options_frame.pack(pady=10)

    lose_weight_checkbox1 = tk.Checkbutton(options_frame, text=lose_weight_options[0], variable=lose_weight_var1,
                                           font=("Helvetica", 11, "bold"), command=update_checkboxes)
    lose_weight_checkbox2 = tk.Checkbutton(options_frame, text=lose_weight_options[1], variable=lose_weight_var2,
                                           font=("Helvetica", 11, "bold"), command=update_checkboxes)
    lose_weight_checkbox3 = tk.Checkbutton(options_frame, text=lose_weight_options[2], variable=lose_weight_var3,
                                           font=("Helvetica", 11, "bold"), state=tk.DISABLED)
    lose_weight_checkbox1.pack(side=tk.LEFT, padx=10)
    lose_weight_checkbox2.pack(side=tk.LEFT, padx=10)
    lose_weight_checkbox3.pack(side=tk.LEFT, padx=10)
    back_button = tk.Button(lose_weight_frame, text="Zurück",
                            command=lambda: go_back(lose_weight_frame, previous_frame))
    back_button.pack(pady=10)
    confirm_button = tk.Button(lose_weight_frame, text="Bestätigen",
                               command=lambda: confirm_lose_weight_panel(user_data, lose_weight_options[0],
                                                                         lose_weight_options[1],
                                                                         dislike_food_entry.get(),
                                                                         lose_weight_entry.get()))
    confirm_button.pack(pady=10)


root = tk.Tk()
root.title("Idealer Körper")

width = 1350
height = 1000

root.geometry(f"{width}x{height}")
root.bind("<Configure>", on_resize)

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)

main_frame = tk.Frame(canvas)
main_frame.pack(fill="both", expand=True)

try:
    input_image = Image.open('logo.jpeg')
    input_image = input_image.resize((width, height), Image.BICUBIC)
    input_image = ImageTk.PhotoImage(input_image)
    logo_label = tk.Label(canvas, image=input_image)
    canvas.create_window(width / 2, height / 2, window=logo_label)
except Exception as e:
    print(f"Fehler beim Hochladen: {e}")

def text_input_fields(label_text, y_position):
    label = tk.Label(canvas, text=label_text, font=("Helvetica", 11, "bold"))
    canvas.create_window(width / 2 - 200, y_position, window=label)

    entry = tk.Entry(canvas, font=("Helvetica", 11, "bold"))
    canvas.create_window(width / 2, y_position, window=entry)

    return entry


input_name = text_input_fields("Name :", 400)
input_age = text_input_fields("Alter :", 430)
input_gender = text_input_fields("Geschlecht :", 460)
input_gender_option = ttk.Combobox(canvas, values=["Weiblich", "Männlich", "Divers"], font=("Helvetica", 11, "bold"))
canvas.create_window(width / 2 + 8, 460, window=input_gender_option)
input_height = text_input_fields("Körpergröße (in cm):", 490)
input_weight = text_input_fields("Gewicht (in kg):", 520)

button = tk.Button(canvas, text="Bestätigen", bg='darkred', fg='white', command=lambda: show_goal_selection({
    "Name": input_name.get(),
    "Alter": input_age.get(),
    "Geschlecht": input_gender_option.get(),
    "Körpergröße": input_height.get(),
    "Gewicht": input_weight.get()
}))

canvas.create_window(width / 2, 570, window=button)

label = tk.Label(canvas, text="", font=("Helvetica", 12, "bold"))
canvas.create_window(width / 2, 600, window=label)

style = ttk.Style()
style.configure("Green.TCombobox", fieldbackground="green", background="green")

root.mainloop()
