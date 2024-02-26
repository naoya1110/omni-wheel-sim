import pygame

# Initialize Pygame
pygame.init()

# Check for available joysticks
joystick_count = pygame.joystick.get_count()
print(f"Number of joysticks found: {joystick_count}")

# If any joystick is connected
if joystick_count > 0:
    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick Name: {joystick.get_name()}")
    print(f"Number of Axes: {joystick.get_numaxes()}")
    print(f"Number of Buttons: {joystick.get_numbuttons()}")

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Get joystick axis values
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            print(f"Axis {i}: {axis_value}")

        # Get button values
        for i in range(joystick.get_numbuttons()):
            button_value = joystick.get_button(i)
            print(f"Button {i}: {button_value}")

        # Add a short delay to avoid excessive printing
        pygame.time.delay(100)

# If no joystick is connected
else:
    print("No joystick found.")

# Quit Pygame
pygame.quit()
