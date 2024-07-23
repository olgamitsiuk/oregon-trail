import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Load the header image
header_image = pygame.image.load("oregon_trail_header.png")
# Calculate the scaling factor to maintain aspect ratio
aspect_ratio = header_image.get_width() / header_image.get_height()
header_height = 200
header_width = int(header_height * aspect_ratio)
header_image = pygame.transform.smoothscale(header_image, (header_width, header_height))

# Set up the display
WIDTH, HEIGHT = max(800, header_width), 800  # Adjust width to fit header if necessary
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE OREGON TRAIL: PREPARE FOR DYSENTERY EDITION")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
ICON_COLOR = (100, 100, 100)
GREEN = (0, 155, 0)
RED = (155, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)
text_font = pygame.font.Font(None, 20)

# Sound state
sound_on = True

# Button class (updated to include highlights)
class Button:
    def __init__(self, x, y, width, height, text, icon_func=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon_func = icon_func
        self.hover = False
        self.alpha = 0  # Added for fade effect
        if icon_func:
            self.icon_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.icon_func(self.icon_surface)

    def draw(self, surface):
        color = DARK_GRAY if not self.hover else (100, 100, 100)  # Slightly lighter dark gray for hover
        # Adjust alpha for fade effect
        highlight_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        highlight_surface.fill((255, 255, 255, self.alpha))
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(highlight_surface, self.rect.topleft)

        if self.icon_func:
            surface.blit(self.icon_surface, (self.rect.x + 10, self.rect.y + 10))
        text_surf = button_font.render(self.text, True, GRAY)
        surface.blit(text_surf, (self.rect.x + (50 if self.icon_func else 10), self.rect.y + 15))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.text
        return None

    def update(self):
        if self.hover and self.alpha < 100:
            self.alpha += 10  # Increase alpha to a maximum of 100
        elif not self.hover and self.alpha > 0:
            self.alpha -= 10  # Decrease alpha to a minimum of 0

# Toggle button class (unchanged)
class ToggleButton(Button):
    def __init__(self, x, y, width, height, text, state=True):
        super().__init__(x, y, width, height, text)
        self.state = state

    def draw(self, surface):
        color = GREEN if self.state else RED
        pygame.draw.rect(surface, color, self.rect)
        text_surf = button_font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 15))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                self.text = "Sound: ON" if self.state else "Sound: OFF"
                return self.state
        return None

class Party:
    def __init__(self):
        self.members = []
        self.inventory = {
            'supplies': 0,
            'bullets': 0,
            'clothes': 0,
            'oxen': 0,
            'wagon_wheels': 0,
            'wagon_axles': 0,
            'wagon_tongues': 0
        }
        self.money = 0

    def add_member(self, name):
        self.members.append({
            'name': name,
            'health': 100,
            'money': 0,
            'diseases': {'dysentery': 0}
        })

def draw_gameplay_screen(party, distance_traveled, days_on_trail, food, health):
    screen.fill(BLACK)
    title_surf = title_font.render("The Oregon Trail", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))

    # Display status
    status_text = [
        f"Day: {days_on_trail}",
        f"Miles traveled: {distance_traveled}",
        f"Food remaining: {food} pounds",
        f"Party health: {health}%"
    ]
    for i, text in enumerate(status_text):
        text_surf = text_font.render(text, True, GRAY)
        screen.blit(text_surf, (50, 100 + i * 30))

    # Display party members
    for i, member in enumerate(party.members):
        text_surf = text_font.render(f"{member['name']}: Health - {member['health']}", True, GRAY)
        screen.blit(text_surf, (50, 250 + i * 30))

    # Action buttons
    action_buttons = [
        Button(50, 450, 200, 50, "Travel"),
        Button(275, 450, 200, 50, "Rest"),
        Button(500, 450, 200, 50, "Hunt"),
        Button(50, 520, 200, 50, "Status"),
        Button(275, 520, 200, 50, "Quit")
    ]
    for button in action_buttons:
        button.draw(screen)

    return action_buttons

# Icon drawing functions (unchanged)
def draw_path_icon(surface):
    pygame.draw.line(surface, ICON_COLOR, (5, 25), (25, 5), 2)
    pygame.draw.circle(surface, ICON_COLOR, (5, 25), 3)
    pygame.draw.circle(surface, ICON_COLOR, (25, 5), 3)

def draw_learn_icon(surface):
    pygame.draw.rect(surface, ICON_COLOR, (5, 5, 20, 25), 2)
    pygame.draw.line(surface, ICON_COLOR, (10, 10), (20, 10), 2)
    pygame.draw.line(surface, ICON_COLOR, (10, 15), (20, 15), 2)
    pygame.draw.line(surface, ICON_COLOR, (10, 20), (20, 20), 2)

def draw_top_ten_icon(surface):
    for i in range(3):
        pygame.draw.rect(surface, ICON_COLOR, (5 + i*8, 20 - i*5, 6, 5 + i*5))

def draw_sound_icon(surface):
    pygame.draw.polygon(surface, ICON_COLOR, [(5, 15), (10, 10), (10, 20), (5, 15)])
    pygame.draw.arc(surface, ICON_COLOR, (10, 5, 15, 20), -0.5, 0.5, 2)

def draw_options_icon(surface):
    pygame.draw.circle(surface, ICON_COLOR, (15, 15), 10, 2)
    pygame.draw.line(surface, ICON_COLOR, (15, 5), (15, 8), 2)
    pygame.draw.line(surface, ICON_COLOR, (15, 22), (15, 25), 2)
    pygame.draw.line(surface, ICON_COLOR, (5, 15), (8, 15), 2)
    pygame.draw.line(surface, ICON_COLOR, (22, 15), (25, 15), 2)

def draw_end_icon(surface):
    pygame.draw.line(surface, ICON_COLOR, (5, 5), (25, 25), 3)
    pygame.draw.line(surface, ICON_COLOR, (5, 25), (25, 5), 3)

# Create buttons (adjusted y-positions)
buttons = [
    Button(0, 250, 700, 50, "1. Travel the Trail", draw_path_icon),
    Button(0, 320, 700, 50, "2. Learn About the Trail", draw_learn_icon),
    Button(0, 390, 700, 50, "3. See the Oregon Top Ten", draw_top_ten_icon),
    Button(0, 460, 700, 50, "4. Sound Settings", draw_sound_icon),
    Button(0, 530, 700, 50, "5. Choose Management Options", draw_options_icon),
    Button(0, 600, 700, 50, "6. End", draw_end_icon)
]

# Top Ten list (unchanged)
top_ten = [
    ("John", 1000),
    ("Sarah", 950),
    ("Mike", 900),
    ("Emily", 850),
    ("David", 800),
    ("Lisa", 750),
    ("Tom", 700),
    ("Anna", 650),
    ("Chris", 600),
    ("Olivia", 550)
]

def draw_main_menu():
    screen.fill(BLACK)
    # Center the header image
    header_x = (WIDTH - header_width) // 2
    screen.blit(header_image, (header_x, 0))
    for button in buttons:
        # Calculate the x-coordinate to center the button
        button.rect.x = (WIDTH - button.rect.width) // 2
        button.draw(screen)

# Other screen drawing functions (unchanged)
def draw_top_ten_screen():
    screen.fill(BLACK)
    title_surf = title_font.render("The Oregon Top Ten", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))

    for i, (name, score) in enumerate(top_ten):
        pygame.draw.circle(screen, DARK_GRAY, (100, 100 + i * 40), 15)  # Avatar placeholder
        text_surf = text_font.render(f"{i+1}. {name}: {score}", True, GRAY)
        screen.blit(text_surf, (130, 90 + i * 40))

    back_button = Button(50, 720, 700, 50, "Back to Main Menu", draw_end_icon)
    back_button.draw(screen)
    return back_button

def draw_sound_settings_screen():
    screen.fill(BLACK)
    title_surf = title_font.render("Sound Settings", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))

    sound_toggle = ToggleButton(50, 100, 700, 50, "Sound: ON" if sound_on else "Sound: OFF", sound_on)
    sound_toggle.draw(screen)

    back_button = Button(50, 720, 700, 50, "Back to Main Menu", draw_end_icon)
    back_button.draw(screen)
    return sound_toggle, back_button

def draw_learn_screen():
    screen.fill(BLACK)
    title_surf = title_font.render("Chosen of the Oregon Trail... Prepare For Dysentery", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))

    text = [
        "Enter a Dark World That Stands Upon the Brink of Ruin",
        "",
        "In Oregon Trail, you lead a small band of travellers into the uncertainty of the American West - a",
        "world where horrors, starvation, and plagues beset you at every step.",
        "",
        "Drag yourself along the golden path toward Oregon with five cases of cholera, a thousand cases of",
        "fever! Utilise all 10 broken arms per member to supplement your dwindling supplies as you",
        "face the terror that waits you upon the Oregon Trail.",
        "",
        "So, rise - Chosen of the Oregon Trail! ... And Prepare... for Dysentery."
    ]

    for i, line in enumerate(text):
        text_surf = text_font.render(line, True, GRAY)
        screen.blit(text_surf, (50, 100 + i * 30))

    back_button = Button(50, 720, 700, 50, "Back to Main Menu", draw_end_icon)
    back_button.draw(screen)
    return back_button

def draw_management_options_screen():
    screen.fill(BLACK)
    title_surf = title_font.render("The Oregon Trail", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
    
    subtitle_surf = title_font.render("Management Options", True, GRAY)
    screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, 70))

    options = [
        "1. See the current Top Ten list",
        "2. See the original Top Ten list",
        "3. Erase the current Top Ten list",
        "4. Erase the tombstone messages",
        "5. Erase saved games",
        "6. Turn joystick on",
        "7. Calibrate joystick",
        "8. Return to the main menu"
    ]

    option_buttons = []
    for i, option in enumerate(options):
        button = Button(50, 120 + i * 50, 700, 40, option)
        button.draw(screen)
        option_buttons.append(button)

    return option_buttons

def draw_party_creation_screen():
    screen.fill(BLACK)
    title_surf = title_font.render("Create Your Party", True, GRAY)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
    # Display input fields for party member names
    # You will need to handle text input and display names here
    pygame.display.flip()

def play_game(party):
    global current_screen

    # Initialize game variables
    distance_traveled = 0
    days_on_trail = 0
    food = 1000
    health = 100
    
    while distance_traveled < 2000 and len(party.members) > 0:
        action_buttons = draw_gameplay_screen(party, distance_traveled, days_on_trail, food, health)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in action_buttons:
                action = button.handle_event(event)
                if action:
                    if action == "Travel":
                        miles = random.randint(10, 20)
                        distance_traveled += miles
                        food -= len(party.members) * 2
                        days_on_trail += 1
                        health -= random.randint(0, 5)
                    elif action == "Rest":
                        days_on_trail += 1
                        food -= len(party.members) * 2
                        health += random.randint(5, 15)
                        if health > 100:
                            health = 100
                    elif action == "Hunt":
                        days_on_trail += 1
                        food -= len(party.members) * 2
                        food_found = random.randint(20, 100)
                        food += food_found
                    elif action == "Status":
                        # Status is already shown on screen, no action needed
                        pass
                    elif action == "Quit":
                        current_screen = "main_menu"
                        return "quit"

        # Random events
        if random.random() < 0.1:
            event = random.choice(["illness", "oxen_death", "thief", "broken_wagon"])
            if event == "illness":
                sick_member = random.choice(party.members)
                sick_member['health'] -= 20
            elif event == "oxen_death":
                party.inventory['oxen'] -= 1
            elif event == "thief":
                stolen_food = random.randint(10, 50)
                food -= stolen_food
            elif event == "broken_wagon":
                days_on_trail += 3
                food -= len(party.members) * 6

        # Check for game over conditions
        if food <= 0 or health <= 0:
            current_screen = "main_menu"
            return "game_over"

        # Remove dead party members
        party.members = [member for member in party.members if member['health'] > 0]

    if distance_traveled >= 2000:
        current_screen = "main_menu"
        return "victory"
    else:
        current_screen = "main_menu"
        return "game_over"

def start_game():
    global current_screen
    party = Party()
    # Add party members (you can expand this to allow user input)
    party.add_member("Player 1")
    party.add_member("Player 2")
    party.add_member("Player 3")
    party.add_member("Player 4")
    party.add_member("Player 5")
    
    # Set initial inventory
    party.inventory['supplies'] = 100
    party.inventory['bullets'] = 100
    party.inventory['clothes'] = 50
    party.inventory['oxen'] = 2
    party.inventory['wagon_wheels'] = 2
    party.inventory['wagon_axles'] = 2
    party.inventory['wagon_tongues'] = 2
    party.money = 1000
    
    result = play_game(party)
    if result == "victory":
        print("You've won the game!")
    elif result == "game_over":
        print("Game Over. Better luck next time!")
    elif result == "quit":
        print("You've chosen to end the game. Goodbye!")

# Main game loop
running = True
current_screen = "main_menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_screen == "main_menu":
            for button in buttons:
                action = button.handle_event(event)
                if action == "1. Travel the Trail":
                    current_screen = "gameplay"
                    start_game()
                elif action == "2. Learn About the Trail":
                    current_screen = "learn"
                elif action == "3. See the Oregon Top Ten":
                    current_screen = "top_ten"
                elif action == "4. Sound Settings":
                    current_screen = "sound_settings"
                elif action == "5. Choose Management Options":
                    current_screen = "management_options"
                elif action == "6. End":
                    running = False
        elif current_screen == "top_ten":
            action = back_button.handle_event(event)
            if action == "Back to Main Menu":
                current_screen = "main_menu"
        elif current_screen == "sound_settings":
            sound_state = sound_toggle.handle_event(event)
            if sound_state is not None:
                sound_on = sound_state
            action = back_button.handle_event(event)
            if action == "Back to Main Menu":
                current_screen = "main_menu"
        elif current_screen == "learn":
            action = back_button.handle_event(event)
            if action == "Back to Main Menu":
                current_screen = "main_menu"
        elif current_screen == "management_options":
            for button in option_buttons:
                action = button.handle_event(event)
                if action:
                    if action == "8. Return to the main menu":
                        current_screen = "main_menu"
                    else:
                        print(f"{action} selected")  # Placeholder for management actions

    if current_screen == "main_menu":
        draw_main_menu()
        for button in buttons:
            button.update()  # Update button alpha for fade effect
    elif current_screen == "top_ten":
        back_button = draw_top_ten_screen()
    elif current_screen == "sound_settings":
        sound_toggle, back_button = draw_sound_settings_screen()
    elif current_screen == "learn":
        back_button = draw_learn_screen()
    elif current_screen == "management_options":
        option_buttons = draw_management_options_screen()
    # Note: The gameplay screen is now handled within the play_game function

    pygame.display.flip()

pygame.quit()
sys.exit()
