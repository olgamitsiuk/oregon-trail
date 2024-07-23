import pygame
import sys
import random
from datetime import datetime, timedelta
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE OREGON TRAIL: PREPARE FOR DYSENTERY EDITION")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (126, 64, 88)
PURPLE = (100, 50, 150)
ICON_COLOR = (237, 240, 72)
CARD_BG = (240, 240, 240)
CARD_SELECTED = (200, 220, 255)
CARD_BORDER = (180, 180, 180)
CONFIRM_BUTTON_INACTIVE = (150, 150, 150)
CONFIRM_BUTTON_ACTIVE = (0, 150, 0)

background_image = pygame.image.load('background_image.jpg')


# Fonts
title_font = pygame.font.Font(None, 36)
subtitle_font = pygame.font.Font(None, 28)
button_font = pygame.font.Font(None, 24)
text_font = pygame.font.Font(None, 18)

game_start_date = datetime(1848, 5, 1)
current_date = game_start_date
distance_travelled = 0
weather_conditions = ["Sunny", "Partly Cloudy", "Rainy", "Stormy"]
current_weather = random.choice(weather_conditions)
resources = {
    "Food": 1000,
    "Water": 500,
    "Ammunition": 200
}

money = 1600  # Starting money (adjust based on character selection)
inventory = {
    "Oxen": 0,
    "Food": 0,
    "Clothing": 0,
    "Ammunition": 0,
    "Spare parts": 0
}

# Button class
class Button:
    def __init__(self, x, y, width, height, text, icon_path=None, rating=None, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = pygame.image.load(icon_path) if icon_path else None
        if self.icon:
            self.icon = pygame.transform.scale(self.icon, (40, 40))
        self.rating = rating
        self.color = color
        self.shadow_offset = 4
        self.border_radius = 10

    def draw(self, surface):
         # Draw shadow
        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=self.border_radius)
        
        # Draw main button
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
        if self.icon:
            surface.blit(self.icon, (self.rect.x + 10, self.rect.y + 10))
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        if self.rating is not None:
            # Draw star rating
            for i in range(5):
                star_color = ICON_COLOR if i < self.rating else GRAY
                pygame.draw.polygon(surface, star_color, [
                    (self.rect.right - 80 + i*15, self.rect.y + 20),
                    (self.rect.right - 75 + i*15, self.rect.y + 15),
                    (self.rect.right - 70 + i*15, self.rect.y + 20),
                    (self.rect.right - 75 + i*15, self.rect.y + 25)
                ])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.text
        return None

# Create buttons
buttons = [
    Button(50, 100, 700, 60, "Travel the Trail", "icon_travel.png", 5),
    Button(50, 180, 700, 60, "Learn About the Trail", "icon_learn.png", 4),
    Button(50, 260, 700, 60, "See the Oregon Top Ten", "icon_top_ten.png", 3),
    Button(50, 340, 700, 60, "Turn Sound Off", "icon_sound.png", 5),
    Button(50, 420, 700, 60, "Choose Management Options", "icon_manage.png", 4),
    Button(50, 500, 700, 60, "End", "icon_end.png", 5)
]

back_button = Button(20, 20, 100, 40, "Back")

class Card:
    def __init__(self, x, y, width, height, title, description, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.description = description
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width - 20, height // 3))
        self.selected = False

    def draw(self, surface):
        pygame.draw.rect(surface, CARD_BG if not self.selected else CARD_SELECTED, self.rect)
        pygame.draw.rect(surface, CARD_BORDER, self.rect, 2)

        surface.blit(self.image, (self.rect.x + 10, self.rect.y + 10))

        title_surf = subtitle_font.render(self.title, True, BLACK)
        surface.blit(title_surf, (self.rect.x + 10, self.rect.y + self.rect.height // 3 + 20))

        desc_lines = self.description.split('\n')
        for i, line in enumerate(desc_lines):
            desc_surf = text_font.render(line, True, BLACK)
            surface.blit(desc_surf, (self.rect.x + 10, self.rect.y + self.rect.height // 3 + 50 + i * 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False



def draw_main_menu():
    screen.blit(background_image, (0, 0))  # Draw the background image
    title_surf = title_font.render("THE OREGON TRAIL: PREPARE FOR DYSENTERY EDITION", True, WHITE)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 20))
    for button in buttons:
        button.draw(screen)

def draw_top_ten():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    # Title
    title_surf = title_font.render("Oregon Top Ten", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))
    
    # Subtitle
    subtitle_surf = subtitle_font.render("Honour the fallen... fear the Trail", True, BLACK)
    screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, 100))
    
    # Heroes label
    heroes_surf = subtitle_font.render("Heroes of The Trail", True, BLACK)
    screen.blit(heroes_surf, (WIDTH // 2 - heroes_surf.get_width() // 2, 150))
    
    # Hero icons
    hero_icon = pygame.Surface((80, 80))
    hero_icon.fill((200, 200, 200))
    for i in range(5):
        screen.blit(hero_icon, (100 + i * 150, 200))
        hero_text = button_font.render("Hero", True, BLACK)
        screen.blit(hero_text, (120 + i * 150, 290))
    
    return back_button

def draw_learn_about_trail():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    # Title
    title_surf = title_font.render("Learn About The Trail", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
    
    # Main image
    main_image = pygame.image.load("oregon_trail_main.png")
    main_image = pygame.transform.scale(main_image, (300, 200))
    screen.blit(main_image, (50, 80))
    
    # Main text
    main_text = [
        "Chosen of the Oregon Trail... Prepare For Dysentery",
        "Enter a Dark World That Stands Upon the Brink of Ruin",
        "In Oregon Trail, you lead a small band of travellers into the uncertainty of the American West, a",
        "world where horrors, starvation, and plagues beset you at every step.",
        "",
        "Drag yourself to the golden path of Oregon with five cases of cholera, a thousand cases of",
        "fever! Utilise all 10 broken arms per member to supplement your dwindling supplies as you",
        "face the terror that awaits you upon the Oregon Trail.",
        "",
        "So, rise - Chosen of the Oregon Trail! ... And Prepare... for Dysentery."
    ]
    
    for i, line in enumerate(main_text):
        text_surf = text_font.render(line, True, BLACK)
        screen.blit(text_surf, (370, 80 + i * 20))
    
    # Diseases section
    diseases_title = subtitle_font.render("Diseases and Other Negative Random Events For Players to Look Forward To", True, BLACK)
    screen.blit(diseases_title, (50, 300))
    
    diseases = [
        ("Dysentery", "What it do", "dysentery.png"),
        ("Cholera", "What it is", "cholera.png"),
        ("Broken Arms and how to eat them", "It was Mothron of the Golden Circle who discovered that basil accompanies the tender flesh of a broken arm so well", "broken_arm.png")
    ]
    
    for i, (name, desc, img_path) in enumerate(diseases):
        disease_img = pygame.image.load(img_path)
        disease_img = pygame.transform.scale(disease_img, (100, 100))
        screen.blit(disease_img, (50, 340 + i * 110))
        
        name_surf = button_font.render(name, True, BLACK)
        screen.blit(name_surf, (160, 340 + i * 110))
        
        desc_surf = text_font.render(desc, True, BLACK)
        screen.blit(desc_surf, (160, 365 + i * 110))
    
    return back_button

def draw_sound_toggle():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    # Title
    title_surf = title_font.render("Turn Sound Off/On", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 30))
    
    # Sound icon
    sound_icon = pygame.image.load("icon_sound.png")
    sound_icon = pygame.transform.scale(sound_icon, (100, 100))
    screen.blit(sound_icon, (50, 100))
    
    # Sound instructions
    instructions_title = subtitle_font.render("Sound Instructions", True, BLACK)
    screen.blit(instructions_title, (180, 100))
    
    published_date = text_font.render("Published date", True, GRAY)
    screen.blit(published_date, (180, 130))
    
    instructions = text_font.render("Press CTRL+S in game to turn on if turned off", True, BLACK)
    screen.blit(instructions, (180, 160))
    
    # Toggle button
    toggle_button = Button(180, 200, 150, 40, "Turn Sound Off", color=PURPLE)
    toggle_button.draw(screen)
    
    return back_button, toggle_button

def draw_management_options():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    # Title
    title_surf = title_font.render("Choose Management Options", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))
    
    # Management options
    options = [
        "1. Change pace",
        "2. Change food rations",
        "3. Stop to rest",
        "4. Attempt to trade",
        "5. Hunt for food"
    ]
    
    for i, option in enumerate(options):
        option_surf = text_font.render(option, True, BLACK)
        screen.blit(option_surf, (100, 150 + i * 40))
    
    return back_button

def draw_travel_screen():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    # Title
    title_surf = title_font.render("Travel the Trail", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))

    # Draw cards
    for card in travel_cards:
        card.draw(screen)

    # Draw confirm button
    confirm_button_color = CONFIRM_BUTTON_ACTIVE if any(card.selected for card in travel_cards) else CONFIRM_BUTTON_INACTIVE
    pygame.draw.rect(screen, confirm_button_color, confirm_button)
    confirm_text = button_font.render("Confirm", True, WHITE)
    screen.blit(confirm_text, (confirm_button.centerx - confirm_text.get_width() // 2, confirm_button.centery - confirm_text.get_height() // 2))

    return back_button

# Create travel option cards
card_width, card_height = 150, 200
margin = 20
cards_top = 120
cards_left = (WIDTH - (4 * card_width + 3 * margin)) // 2

travel_cards = [
    Card(cards_left, cards_top, card_width, card_height, "Banker", "Start with $1600\nEasier journey", "banker_image.png"),
    Card(cards_left + card_width + margin, cards_top, card_width, card_height, "Carpenter", "Start with $800\nBonus repairs", "carpenter_image.png"),
    Card(cards_left + 2 * (card_width + margin), cards_top, card_width, card_height, "Farmer", "Start with $400\nBonus animals", "farmer_image.png"),
    Card(cards_left + 3 * (card_width + margin), cards_top, card_width, card_height, "Differences", "Learn more", "info_image.png")
]

# Create confirm button
confirm_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

def draw_journey_screen():
    screen.fill(WHITE)
    
    back_button.draw(screen)
    
    title_surf = title_font.render("Start Your Journey", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surf, title_rect)

    instruction_text = [
        "You're about to embark on the Oregon Trail.",
        "Are you ready for the challenges ahead?",
        "Click 'Start Journey' when you're prepared to begin."
    ]

    for i, line in enumerate(instruction_text):
        text_surf = text_font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, 150 + i * 30))
        screen.blit(text_surf, text_rect)

    start_journey_button = Button(WIDTH // 2 - 75, 300, 150, 40, "Start Journey")
    start_journey_button.draw(screen)
    
    return back_button, start_journey_button

class ShopItem:
    def __init__(self, name, price, description, image_path):
        self.name = name
        self.price = price
        self.description = description
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.rect = self.image.get_rect()
        self.quantity = 0

    def draw(self, surface, pos):
        self.rect.topleft = pos
        surface.blit(self.image, self.rect)
        
        name_surf = subtitle_font.render(self.name, True, BLACK)
        surface.blit(name_surf, (pos[0], pos[1] + 110))
        
        price_surf = text_font.render(f"${self.price}", True, BLACK)
        surface.blit(price_surf, (pos[0], pos[1] + 130))
        
        quantity_surf = text_font.render(f"Quantity: {self.quantity}", True, BLACK)
        surface.blit(quantity_surf, (pos[0], pos[1] + 150))
        
        buy_button = pygame.Rect(pos[0], pos[1] + 170, 60, 30)
        pygame.draw.rect(surface, BUTTON_COLOR, buy_button)
        buy_text = text_font.render("Buy", True, WHITE)
        surface.blit(buy_text, (buy_button.centerx - buy_text.get_width() // 2, buy_button.centery - buy_text.get_height() // 2))
        
        return buy_button

def draw_shop_screen():
    global money, inventory
    
    screen.fill(WHITE)
    
    # Draw title
    title_surf = title_font.render("General Store", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 20))
    
    # Draw money
    money_surf = subtitle_font.render(f"Money: ${money}", True, BLACK)
    screen.blit(money_surf, (20, 70))
    
    # Draw inventory
    inventory_surf = subtitle_font.render("Inventory:", True, BLACK)
    screen.blit(inventory_surf, (20, 100))
    for i, (item, quantity) in enumerate(inventory.items()):
        item_surf = text_font.render(f"{item}: {quantity}", True, BLACK)
        screen.blit(item_surf, (20, 130 + i * 25))
    
    # Draw shop items
    buy_buttons = []
    for i, item in enumerate(shop_items):
        buy_button = item.draw(screen, (300 + (i % 3) * 180, 100 + (i // 3) * 220))
        buy_buttons.append(buy_button)
    
    # Draw continue button
    continue_button = Button(WIDTH // 2 - 75, HEIGHT - 60, 150, 40, "Continue to Journey")
    continue_button.draw(screen)
    
    return buy_buttons, continue_button

def handle_shop_events(event, buy_buttons):
    global money, inventory
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        for i, button in enumerate(buy_buttons):
            if button.collidepoint(event.pos):
                item = shop_items[i]
                if money >= item.price:
                    money -= item.price
                    item.quantity += 1
                    inventory[item.name] += 1
                else:
                    print("Not enough money!")  # Replace with on-screen message

# Create shop items
shop_items = [
    ShopItem("Oxen", 40, "You'll need a team of oxen to pull your wagon", "oxen_image.png"),
    ShopItem("Food", 0.20, "You'll need food for the journey", "food_image.png"),
    ShopItem("Clothing", 10, "You'll need warm clothing for the journey", "clothing_image.png"),
    ShopItem("Ammunition", 2, "You'll need ammunition for hunting and protection", "ammunition_image.png"),
    ShopItem("Spare parts", 10, "You'll need spare parts for wagon repairs", "spare_parts_image.png")
]

# Add this new function to draw the game screen
def draw_game_screen():
    screen.fill(GRAY)
    
    # Display game information
    date_surf = text_font.render(f"Date: {current_date.strftime('%B %d, %Y')}", True, BLACK)
    screen.blit(date_surf, (20, 20))
    
    weather_surf = text_font.render(f"Weather: {current_weather}", True, BLACK)
    screen.blit(weather_surf, (20, 50))
    
    distance_surf = text_font.render(f"Distance Travelled: {distance_travelled} miles", True, BLACK)
    screen.blit(distance_surf, (20, 80))
    
    resources_surf = text_font.render(f"Resources - Food: {resources['Food']}, Water: {resources['Water']}, Ammunition: {resources['Ammunition']}", True, BLACK)
    screen.blit(resources_surf, (20, 110))
    
    management_button = Button(WIDTH - 220, HEIGHT - 60, 200, 40, "Management Options")
    management_button.draw(screen)
    
    return management_button

# Add this function to update the game state
def update_game_state():
    global current_date, distance_travelled, current_weather, resources

    current_date += timedelta(days=1)
    if random.random() < 0.1:
        current_weather = random.choice(weather_conditions)
    distance_travelled += random.randint(10, 20)
    resources["Food"] = max(resources["Food"] - random.randint(5, 15), 0)
    resources["Water"] = max(resources["Water"] - random.randint(3, 10), 0)
    resources["Ammunition"] = max(resources["Ammunition"] - random.randint(0, 2), 0)

    

# Modify the main game loop
running = True
current_screen = "main"
sound_on = True
selected_character = None

while running:
    screen.blit(background_image, (0, 0))  # Draw the background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_screen == "main":
            for button in buttons:
                action = button.handle_event(event)
                if action == "Travel the Trail":
                    current_screen = "travel"
                elif action == "See the Oregon Top Ten":
                    current_screen = "top_ten"
                elif action == "Learn About the Trail":
                    current_screen = "learn_trail"
                elif action == "Turn Sound Off":
                    current_screen = "sound_toggle"
                elif action == "Choose Management Options":
                    current_screen = "management_options"
                elif action == "End":
                    running = False
        elif current_screen == "travel":
            back_action = back_button.handle_event(event)
            if back_action == "Back":
                current_screen = "main"
            else:
                for card in travel_cards:
                    if card.handle_event(event):
                        for c in travel_cards:
                            c.selected = False
                        card.selected = True
                        selected_character = card.title if card.title != "Differences" else None
                
                if event.type == pygame.MOUSEBUTTONDOWN and confirm_button.collidepoint(event.pos):
                    if selected_character:
                        current_screen = "shop"
                        if selected_character == "Banker":
                            money = 1600
                        elif selected_character == "Carpenter":
                            money = 800
                        else:  # Farmer
                            money = 400
        elif current_screen == "shop":
            buy_buttons, continue_button = draw_shop_screen()
            handle_shop_events(event, buy_buttons)
            if continue_button.handle_event(event) == "Continue to Journey":
                current_screen = "journey"
        elif current_screen == "journey":
            back_action = back_button.handle_event(event)
            start_action = start_journey_button.handle_event(event)
            if back_action == "Back":
                current_screen = "travel"
            elif start_action == "Start Journey":
                current_screen = "game"
                # Initialize game state here
                current_date = game_start_date
                distance_travelled = 0
                current_weather = random.choice(weather_conditions)
                resources = {"Food": 1000, "Water": 500, "Ammunition": 200}
        elif current_screen == "game":
            management_action = management_button.handle_event(event)
            if management_action == "Management Options":
                current_screen = "management_options"
            update_game_state()
        elif current_screen in ["top_ten", "learn_trail", "management_options"]:
            action = back_button.handle_event(event)
            if action == "Back":
                current_screen = "main"
        elif current_screen == "sound_toggle":
            back_action = back_button.handle_event(event)
            toggle_action = toggle_button.handle_event(event)
            if back_action == "Back":
                current_screen = "main"
            elif toggle_action == "Turn Sound Off":
                sound_on = not sound_on
                toggle_button.text = "Turn Sound On" if sound_on else "Turn Sound Off"

    if current_screen == "main":
        draw_main_menu()
    elif current_screen == "travel":
        back_button = draw_travel_screen()
    elif current_screen == "shop":
        draw_shop_screen()
    elif current_screen == "journey":
        back_button, start_journey_button = draw_journey_screen()
    elif current_screen == "game":
        management_button = draw_game_screen()
    elif current_screen == "top_ten":
        back_button = draw_top_ten()
    elif current_screen == "learn_trail":
        back_button = draw_learn_about_trail()
    elif current_screen == "sound_toggle":
        back_button, toggle_button = draw_sound_toggle()
    elif current_screen == "management_options":
        back_button = draw_management_options()

    pygame.display.flip()

pygame.quit()
sys.exit()