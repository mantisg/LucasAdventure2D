import pygame as pg

def crop_image(image):
    rect = image.get_bounding_rect()
    return image.subsurface(rect).copy()

class Player:
    def __init__(self, x, y):
        self.run_right = []
        self.run_left = []
        self.jump_right = []
        self.jump_left = []
        self.roll_right = []
        self.roll_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pg.image.load(f'assets/Rogue/Run/run{num}.png')
            img_right = pg.transform.scale(crop_image(img_right), (80, 80))
            img_left = pg.transform.flip(img_right, True, False)
            self.run_right.append(img_right)
            self.run_left.append(img_left)
        for num in range(1, 8):
            img_jump_right = pg.image.load(f'assets/Rogue/Jump/jump{num}.png')
            img_jump_right = pg.transform.scale(crop_image(img_jump_right), (80, 80))
            img_jump_left = pg.transform.flip(img_jump_right, True, False)
            self.jump_right.append(img_jump_right)
            self.jump_left.append(img_jump_left)
        for num in range(1, 10):
            img_roll_right = pg.image.load(f'assets/Rogue/Duck/duck{num}.png')
            img_roll_right = pg.transform.scale(crop_image(img_roll_right), (80, 80))
            img_roll_left = pg.transform.flip(img_roll_right, True, False)
            self.roll_right.append(img_roll_right)
            self.roll_left.append(img_roll_left)
        self.image = self.run_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 80
        self.rect.width = 80
        self.vel_y = 0
        self.jumped = False
        self.rolled = False
        self.direction = 0
        self.jumping = False
        self.rolling = False
        self.on_ground = False

    def update(self, world):
        dx = 0
        dy = 0
        run_cooldown = 6
        jump_cooldown = 10
        roll_cooldown = 10

        key = pg.key.get_pressed()
        if key[pg.K_UP] and not self.jumped and self.on_ground:
            self.vel_y = -15  # Adjusted jump velocity
            self.jumped = True
            self.jumping = True
            self.index = 0
        if not key[pg.K_UP]:
            self.jumped = False
        if key[pg.K_LEFT]:
            dx -= 5  # Adjusted horizontal speed
            self.counter += 1
            self.direction = -1
        if key[pg.K_RIGHT]:
            dx += 5  # Adjusted horizontal speed
            self.counter += 1
            self.direction = 1
        if key[pg.K_DOWN] and self.on_ground:
            self.rolled = True
            self.rolling = True
            self.index = 0
            dx += (10 * self.direction)
        if not key[pg.K_DOWN]:
            self.rolled = False
        if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.run_right[self.index]
            if self.direction == -1:
                self.image = self.run_left[self.index]
                
        if self.rolling:
            self.counter += 1
            #self.rect.height = 50
            if self.counter > roll_cooldown:
                self.counter = 0
                self.index += 1
                if self.direction == 1:
                    if self.index >= len(self.roll_right):
                        self.index = 0
                        self.rolling = False
                    self.image = self.roll_right[self.index]
                elif self.direction == -1:
                    if self.index >= len(self.roll_left):
                        self.index = 0
                        self.rolling = False
                    self.image = self.roll_left[self.index]
        else:
            # Restore the rect size
            self.rolled = False
            if self.counter > run_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.run_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.run_right[self.index]
                if self.direction == -1:
                    self.image = self.run_left[self.index]

        if self.jumping:
            self.counter += 1
            if self.counter > jump_cooldown:
                self.counter = 0
                self.index += 1
                if self.direction == 1:
                    if self.index >= len(self.jump_right):
                        self.index = len(self.jump_right) - 1  # Stop at the last frame of jump animation
                        self.jumping = False
                    self.image = self.jump_right[self.index]
                if self.direction == -1:
                    if self.index >= len(self.jump_left):
                        self.index = len(self.jump_left) - 1  # Stop at the last frame of jump animation
                        self.jumping = False
                    self.image = self.jump_left[self.index]
        else:
            if self.counter > run_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.run_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.run_right[self.index]
                if self.direction == -1:
                    self.image = self.run_left[self.index]

        self.vel_y += 0.5  # Adjusted gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collisions in the x direction
        self.rect.x += dx
        for tile in world.tile_list:
            if tile[2] == 1 or tile[2] == 5:  # Only check collision with "1" tiles
                if tile[1].colliderect(self.rect):
                    if dx > 0:  # Moving right
                        self.rect.right = tile[1].left
                    if dx < 0:  # Moving left
                        self.rect.left = tile[1].right

        # Check for collisions in the y direction
        self.rect.y += dy
        self.on_ground = False
        for tile in world.tile_list:
            if tile[2] == 1 or tile[2] == 5:  # Only check collision with "1" tiles
                if tile[1].colliderect(self.rect):
                    if self.vel_y > 0:  # Falling
                        self.rect.bottom = tile[1].top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping
                        self.rect.top = tile[1].bottom
                        self.vel_y = 0

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))