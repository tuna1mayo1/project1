"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SPRITE_PIXEL_SIZE = 128
SCREEN_TITLE = "CPSC 410 - Project 1"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.moving_wall_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        self.game_over = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()

        self.game_over = False

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite(
            "images/player_1/player_stand.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        
        # TODO: change to grid system
        block_coordinate_list = [[512, 96],
                                 [256, 96],
                                 [768, 96]]

        self.add_static_blocks(block_coordinate_list)
        self.add_horizontal_moving_block(9, 4, 5, 9, -4)
        self.add_horizontal_moving_block(0, 0, 0, 3, 3)

        # Create the 'physics engine'
        # First argument is the moving sprite, second argument is list of sprites that moving sprite cannot move through
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def add_static_blocks(self, block_coordinates):
        """ 
        Parameters
        ----------
        block_coordinates : list
            List of coordinates [(x, y)] that denote the locations to position the blocks
        """
        for coordinate in block_coordinates:
            self.add_static_block(coordinate)

    def add_static_block(self, coordinate):
        block = arcade.Sprite(
            "images/tiles/grassMid.png", TILE_SCALING)
        block.position = coordinate
        self.wall_list.append(block)

    def add_horizontal_moving_block(self, center_x, center_y, boundary_left, boundary_right, change_x):
        """ 
        Parameters
        ----------
        center_x : int
            The x-tile that the block will be spawned on
        center_y: int
            The y-tile that the block will be spawned on
        boudary_left: int
            The x-tile that the block will not move past when going left
        boundary_right: int
            The x-tile that the block will not move past when going right
        change_x: int
            How many tiles to move per second
        """
        block = arcade.Sprite(
            ":resources:images/tiles/dirtMid.png", TILE_SCALING)
        block.center_x = (center_x * GRID_PIXEL_SIZE) + (GRID_PIXEL_SIZE / 2)
        block.center_y = (center_y * GRID_PIXEL_SIZE) + (GRID_PIXEL_SIZE / 2)
        block.boundary_left = (boundary_left * GRID_PIXEL_SIZE)
        block.boundary_right = (boundary_right * GRID_PIXEL_SIZE) + (GRID_PIXEL_SIZE / 2)
        block.change_x = change_x * TILE_SCALING
    
        self.wall_list.append(block)
        self.moving_wall_list.append(block)

        return block

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()