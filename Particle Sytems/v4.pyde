import math

NUM_PARTICLES = 500  # Reduced for clarity
MAX_SPEED = 5  # Maximum speed of particles
MAX_SIZE = 10  # Maximum size of particles
MAX_LIFESPAN = 150  # Maximum lifespan of particles
GRAVITY = 0.1  # Strength of gravity

WATER_COLOR = (90,188,216, 100)       # Color for water particles
SUNLIGHT_COLOR = (255, 255, 0, 100)  # Color for sunlight particles with alpha value of 150
FERTILIZER_COLOR = (128, 99, 71, 50)   # Color for fertilizer particles
MOON = (255, 255, 255, 50)
SUN = (250, 250, 51, 20)

water_can_position = None


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = MAX_SIZE
        self.speed_x = random(MAX_SPEED) - MAX_SPEED / 2
        self.speed_y = random(-MAX_SPEED * 3) 
        self.lifespan = MAX_LIFESPAN
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += GRAVITY  # Apply gravity
    
    def display(self):
        fill(*self.color)
        stroke(*self.color)
        ellipse(self.x, self.y, self.size, self.size)
    
    def lifeSpan(self):
        self.lifespan -= 1

class WaterParticle(Particle):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5
        self.speed_x = (MAX_SPEED) - MAX_SPEED / 2
        self.speed_y = (-MAX_SPEED * 2)  # Increased initial upward velocity
        self.lifespan = MAX_LIFESPAN        
        self.color = WATER_COLOR
        
    def move(self):
        self.x -= self.speed_x
        self.y -= self.speed_y
        if self.x >= 470 and self.x <=520 and self.y >= 500:
            self.lifespan = 0
    
    def display(self):
        fill(*self.color)
        stroke(*self.color)
        size = 5
        x = self.x
        y = self.y
        beginShape()
        vertex(x, y + self.size)  # Bottom point
        bezierVertex(x - self.size / 2, y + self.size / 2, x - self.size / 2, y - self.size / 2, x, y - self.size)  # Left curve
        bezierVertex(x + self.size / 2, y - self.size / 2, x + self.size / 2, y + self.size / 2, x, y + self.size)  # Right curve
        endShape(CLOSE)
        
class SunlightParticle(Particle):
    def __init__(self, x, y, sx, sy):
        self.y = y
        self.x = x
        self.size = 5
        self.speed_x = sx  
        self.speed_y = sy  
        self.lifespan = MAX_LIFESPAN
        self.color = SUNLIGHT_COLOR
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if ((self.x**2)+(self.y**2)) >= (400**2):
            self.lifespan=0

    def display(self):
        fill(*self.color)
        stroke(*self.color)
        ellipse(self.x, self.y, self.size, self.size)
    
        
class FertilizerParticle(Particle):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1
        self.speed_x = (MAX_SPEED) - MAX_SPEED / 2
        self.speed_y = (-MAX_SPEED * 2)  # Increased initial upward velocity
        self.lifespan = MAX_LIFESPAN
        self.color = FERTILIZER_COLOR
        
    def move(self):
        self.x -= self.speed_x
        self.y -= self.speed_y
        if self.x >= 470 and self.x <=520 and self.y >= 450:
            self.lifespan = 0

class Sun(SunlightParticle):
    def __init__(self, x, y, color=SUN):
        self.y = y
        self.x = x
        self.size = 15
        self.speed_x = 1  
        self.speed_y = 1  
        self.lifespan = MAX_LIFESPAN
        self.color = color
        self.initial_x = x  
        self.initial_y = y  
        self.angle = random(TWO_PI)  
        self.radius = random(10, 50)  
        self.angular_speed = 0.02  
            
    def move(self):
        # circular oscillations 
        self.angle += self.angular_speed  
        self.x = self.initial_x + cos(self.angle) * self.radius  # Calculate new x-coordinate
        self.y = self.initial_y + sin(self.angle) * self.radius  # Calculate new y-coordinate
        
    def display(self):
        fill(*self.color)
        stroke(*self.color)
        ellipse(self.x, self.y, self.size, self.size)

class CloudParticle(Particle):
    def __init__(self, x, y, s):
        self.x = x
        self.y = y
        self.size = random(5, 50)  
        self.lifespan = random(50, 100)
        self.speed_x = windSpeed + random(-3, 3)  
        self.speed_y = random(-MAX_SPEED / 2, MAX_SPEED / 2)  
        self.color = (255, 255, 255, 10)  
        self.noise_offset_x = random(1000)
        self.noise_offset_y = random(1000)

    def move(self):
        self.x += self.speed_x
        if self.x > 1000:
            self.lifespan = 0

    def display(self):
        noStroke()  
        fill(*self.color)
        
        noise_x = noise(self.noise_offset_x)
        noise_y = noise(self.noise_offset_y)
        
        offset_x = map(noise_x, 0, 1, -5, 5)
        offset_y = map(noise_y, 0, 1, -5, 5)
        
        puffy_x = self.x + offset_x
        puffy_y = self.y + offset_y
        
        ellipse(puffy_x, puffy_y, self.size, self.size)
        self.noise_offset_x += 0.01
        self.noise_offset_y += 0.01

class Raindrop(WaterParticle):
    def __init__(self, x, y, sx):
        self.x = x
        self.y = y
        self.size = 7  
        self.color = WATER_COLOR  
        self.speed_x = sx
        self.speed_y = (-MAX_SPEED * 5)  
        self.lifespan = MAX_LIFESPAN

    def move(self):
        self.x += self.speed_x
        self.y -= self.speed_y
        if self.y >= height or self.x>950:
            self.lifespan = 0

class OnOffButton:
    def __init__(self, x, y, width=100, height=50, text="Make it Rain!"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.state = True
        self.color = color(255)  # Green color for "ON" state
        
    def display(self):
        fill(self.color)  
        rect(self.x, self.y, self.width, self.height)
    
        fill(128, 128, 128)  
        textSize(20)  
        textAlign(CENTER, CENTER)  
        textSize(15)
        text(self.text, self.x + self.width / 2, self.y + self.height / 2)
        
    def toggle_state(self):
        self.state = not self.state
        if self.state==False:
            self.color = color(135, 206, 235)  # Green color for "ON" state
            self.text = "Stop the Rain!"
        else:
            self.color = color(255)  # Red color for "OFF" state
            self.text = "Make it Rain!"
            
    def is_clicked(self, mx, my):
        # Check if mouse is within the button boundaries
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = 0
        self.pos_x = map(self.value, self.min_value, self.max_value, self.x, self.x + self.width)

    def display(self):
        stroke(135, 206, 235)
        strokeWeight(5)
        fill(255)
        rect(self.x, self.y, self.width, self.height)
        
        # Calculate slider position based on value
        slider_pos = map(self.value, self.min_value, self.max_value, self.x, self.x + self.width)
        
        strokeWeight(1)
        fill(135, 206, 235)
        rect(slider_pos - 5, self.y - 5, 10, self.height + 10)
        
        textAlign(CENTER)
        textSize(20)
        text("Increase Wind Speed", self.x + 50, self.y - 20)

    def update(self):
        global windSpeed
        if (self.x <= mouseX <= self.x + self.width and
                self.y <= mouseY <= self.y + self.height):
            
            # Update slider value based on mouse position
            self.value = int(map(constrain(mouseX, self.x, self.x + self.width),
                                 self.x, self.x + self.width, self.min_value, self.max_value))
        windSpeed = self.value
        return self.value

class HealthBar:
    def __init__(self, x, y, width, height, color, text, max_health=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health
        self.color = color
        self.text = text

    def display(self):
        fill(255)
        rect(self.x, self.y, self.width, self.height)
        
        fill(*self.color)  # Green color for health
        health_height = map(self.health, 0, self.max_health, 0, self.height) # Map height based on health value
        rect(self.x, self.y + self.height - health_height, self.width, health_height)
        
        textAlign(CENTER, CENTER)
        textSize(20)
        fill(*self.color)
        stroke(0)
        pushMatrix()  
        translate(self.x-15, self.y+80)  
        rotate(-HALF_PI) 
        text(self.text, 0,0)  
        popMatrix()  
    
    def decrease_health(self, amount):
        if self.health-amount <= 0:
            self.health = 0
        else:
            self.health -= amount

    def increase_health(self, amount):
        # self.health += amount
        if self.health+amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

def draw_plant(night):
    if night:
        plantImage = loadImage("sf1N.png")
    else:
        plantImage = loadImage("sf1.png")
    image(plantImage, 400, 450, 200, 350)

def draw_wilted_plant(night):
    if night:
        plantImage = loadImage("sf2N.png")
    else:
        plantImage = loadImage("sf2.png")
    image(plantImage, 400, 450, 200, 350)
    
    textAlign(CENTER)
    fill(135, 206, 235)
    textSize(23)
    text("The flower died :(", 1100 , 700)

def draw_water_can(x, y):
    canImage = loadImage("can2.png")
    image(canImage, x-20, y-200, 160, 210)

def draw_fertilizer_packet(x, y, width, height):
    fertilizerImage = loadImage("fert2.png")
    image(fertilizerImage, x, y, 170, 120)
    

def setup():
    size(1200, 800)
    
    #Initializing global values
    global water_particles, sunlight_particles, fertilizer_particles, sunray1, water_can, fertilizer, mouse_pressed, sun, cloud_particles, backgroundImage, wilted, start_time, seconds, wateredAt, fertilizedAt, slider, raindrops, button, night, windSpeed, water_bar, fertilizer_bar, light_bar, last_checked_time, dec, custom_font
    custom_font = createFont("Georgia", 25, True)
    textFont(custom_font)
    start_time = millis()  
    button = OnOffButton(1050, 300)
    slider = Slider(1050, 200, 100, 20, 0, 100)
    water_bar = HealthBar(1040, 400, 20, 150, (90,188,216),"Water Level", 24)
    fertilizer_bar = HealthBar(1100, 400, 20, 150,(128, 99, 71),"Fertilizer Level", 24)
    light_bar = HealthBar(1160, 400, 20, 150, (250, 250, 51), "Light Level",  24)
    water_bar.display()
    fertilizer_bar.display()
    light_bar.display()
    windSpeed = 0
    dec = False
    night = True
    wateredAt = fertilizedAt =  0
    water_can = wilted = fertilizer = mouse_pressed = False
    last_checked_time = 0
    raindrops = []
    water_particles = []
    sunlight_particles = []
    fertilizer_particles = []
    sun = []
    cloud_particles = []



def draw():
    global water_can, fertilizer, mouse_pressed, cloud_particles, backgroundImage, wilted, seconds, wateredAt, fertilizedAt, raindrops, last_checked_time, night, dec
    background(255, 255, 255)  # Set background to white
    stroke(255, 255, 0)
    slider.display()
    button.display()
    elapsed_time = millis() - start_time
    seconds = int(elapsed_time / 1000)
    minutes = int(0)
    hours = int(0)
    
    # Display the time
    fill(135, 206, 235)
    textSize(32)
    textAlign(RIGHT, TOP)
    textSize(20)
    text("Time", 1125, 40)
    textSize(40)
    text("{:02}:{:02}:{:02}".format( (seconds%25), minutes % 60, hours), 1190, 70)
    
    
    interval = 941  
    # Decrease health every hour
    if millis() - last_checked_time >= interval:
        if seconds-wateredAt>=0:
            water_bar.decrease_health(1)
        if seconds-fertilizedAt>=-1:
            fertilizer_bar.decrease_health(1)
        if dec or night:
            light_bar.decrease_health(1)
        last_checked_time = millis()
        
   # If any two health bars reacch health 0, then the flower dies
    if (water_bar.health == 0 and fertilizer_bar.health == 0) or (light_bar.health == 0 and fertilizer_bar.health == 0) or (water_bar.health == 0 and light_bar.health == 0):
        wilted = True
        water_bar.decrease_health(24)
        fertilizer_bar.decrease_health(24)
        light_bar.decrease_health(24)
        
    water_bar.display()
    fertilizer_bar.display()
    light_bar.display()
    
    # If daytime, set background and paramters accordingly
    if (seconds%25)>=6 and (seconds%25)<=19:
        backgroundImage = loadImage("bg6.jpeg")
        image(backgroundImage, 0, 0, 1000, height)
        sun = [Sun(random(0, 140), random(140)) for _ in range(4000)]
        sunlight_particles = [SunlightParticle(random(270), random(270),random(2), random(2)) for _ in range(20)]
        night = False
        if dec==False:
            light_bar.increase_health(24)
    # If nightime, set background and paramters accordingly
    else:
        backgroundImage = loadImage("bgN.jpeg")
        image(backgroundImage, 0, 0, 1000, height)
        sun = [] 
        sunlight_particles = []
        night = True
    
    # If button pressed, create rainfall particles
    if button.state==False:
        raindrops.append(Raindrop(random(1000), 0, windSpeed))
    
        # Display and move existing raindrops
        for raindrop in raindrops[:]:
            raindrop.move()
            raindrop.display()
            # Check if raindrop waters plant
            if raindrop.x >= 470 and raindrop.x <=520 and raindrop.y >= 500:
                wateredAt = seconds
                if wilted==False:
                    water_bar.increase_health(24)
            # Check if raindrop lifespan has finished
            if raindrop.lifespan <=0:
                raindrops.remove(raindrop)
    
    # check state of flower, draw accordingly
    if wilted:
        draw_wilted_plant(night)
    else:
        draw_plant(night)  
    
    # Draw water can if being used
    if water_can:
        if mouseX<=900:
            draw_water_can(mouseX, mouseY)
    # Draw fertilizer if being used    
    if fertilizer:
        if mouseX<=900:
            draw_fertilizer_packet(mouseX, mouseY, 50, 100)
    
    # Display water particles
    for particle in water_particles:
        particle.move()
        particle.display()
        if particle.lifespan<=0:
            water_particles.remove(particle)
    
    # Display Sun
    for particle in sun:
        particle.move()
        particle.display()
        particle.lifeSpan()
    
    # Display cloud
    dec = False 
    for particle in cloud_particles:
        if particle.x >=0 and particle.x<=80: # Check if cloud covering cloud 
           dec = True 
        particle.speed_x = windSpeed+5 # Update speed of cloud according to windspeed 
        particle.move()
        particle.display()
        if particle.lifespan<=0:
            cloud_particles.remove(particle)

    # Display Sun particles
    for particle in sunlight_particles:
        particle.move()
        particle.display()
        particle.lifeSpan()
        if particle.lifespan <= 0:
            sunlight_particles.remove(particle)
            sunlight_particles.append(SunlightParticle(random(170), random(170),random(5), random(5)))
            
    # Display fertilizer particles
    for particle in fertilizer_particles:
        particle.move()
        particle.display()
        if particle.lifespan<=0:
            fertilizer_particles.remove(particle)

def mousePressed():
    
    global water_can, fertilizer, cloud_particles, wateredAt, seconds, fertilizedAt, windSpeed, wilted
    
    # Toggle button state if clicked
    if button.is_clicked(mouseX, mouseY):
        button.toggle_state()
    
    # Store new wind speed
    windSpeed = slider.update()

    # Create cloud particles on mouse click
    if water_can==False and fertilizer==False and mouseX<=1000:
        for _ in range(800):
            angle = random(0, TWO_PI)  # Random angle in radians
            radius = random(0, 60)  # Random radius within a range
            x = mouseX + radius * cos(angle) +random(-100, 100)  # Calculate x-coordinate
            y = mouseY + radius * sin(angle)  # Calculate y-coordinate
            cloud_particles.append(CloudParticle(x, y, windSpeed))
    
    # Create water particles from can on mouse click
    if water_can:
        for i in range(30):
            drop = WaterParticle(random(mouseX-20, mouseX), random(mouseY-55, mouseY+55))
            water_particles.append(drop)
            if drop.x >= 410 and drop.x <=600 and drop.y >= 430: # check if drop watered flower
                wateredAt = seconds
                if wilted==False:
                    water_bar.increase_health(24)
                    
    # Create fertilizer particles from packet on mouse click
    if fertilizer:
        for i in range(100):
            p = FertilizerParticle(random(mouseX-15,mouseX+15), random(mouseY+20, mouseY+100))
            fertilizer_particles.append(p)
            if p.x >= 410 and p.x <=600 and p.y >= 430: # Check if particle fell on flower
                fertilizedAt = seconds
                if wilted==False:
                    fertilizer_bar.increase_health(24)
                
    
def keyPressed():
    global sunlight_particles, water_can, fertilizer, wilted
    
    # Enable/Disable fertilizer
    if key == 'f':
        if fertilizer:
            fertilizer = False
        else:
            fertilizer = True
    # Enable/Disable watering can
    elif key == 'c':
        if water_can:
            water_can = False
        else:
            water_can = True
