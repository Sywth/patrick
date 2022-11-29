"""
Where the main game loop runs
"""

from patrick_namespace import *
from main_script import *

running = True
#main application loop
while running:
    p_frame_count += 1

    #refreshes the screen's background color to black 
    p_screen.fill((255,255,255))

    p_handle_events()
    p_update(p_delta_time)

    #run the user's code
    main_game_function()

    p_draw_frame(p_default_camera)
    p_draw_UI(p_default_camera)
    p_default_camera.draw_to_window()
    
    #pg_clock.tick tries to keep application running at '$FPS' frames per second,
    #this also returns in milliseconds the last it was called so we can also update delta time here
    p_delta_time = p_clock.tick()*p_TIME_SCALAR
    
pygame.quit() 