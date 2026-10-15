import pygame, sys, random, math 
import numpy as np
from pygame.locals import *
pygame.init()
 

BACKGROUND = (255, 255, 255)
 
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
bg = pygame.image.load("spaceBG.jpg")

dt =10
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
G = 6.67430e-11

WHITE = (255, 255, 255)
GREEN = (0,128,0)
fallen = False
planetData = {
    "Earth": {
        "mass": 5.972e24,
        "radius": 6.371e6,
        "color": (0, 128, 0),
        "image": "theEarth.png"

    },
    "Venus": {
        "mass": 4.8675e24,
        "radius": 6.0518e6,
        "color": (255, 204, 153),
        "image": "venus.png"
    },
    "Mercury": {
        "mass": 3.3011e23,
        "radius": 2.4397e6,
        "color": (169, 169, 169),
        "image": "mercury.png"
    },
    "Mars": {
        "mass": 6.4171e23,
        "radius": 3.3895e6,
        "color": (255, 51, 51),
        "image": "mars.png"
    },
    "Jupiter": {
        "mass": 1.8982e27,
        "radius": 6.9911e7,
        "color": (255, 165, 0),
        "image": "jupiter.png"
    },
    "Saturn": {
        "mass": 5.6834e26,
        "radius": 5.8232e7,
        "color": (255, 223, 128),
        "image": "saturn.png"
    },
    "Uranus": {
        "mass": 8.6810e25,
        "radius": 2.5362e7,
        "color": (173, 216, 230),
        "image": "uranus.png"
    },
    "Neptune": {
        "mass": 1.02413e26,
        "radius": 2.4622e7,
        "color": (0, 0, 255),
        "image": "neptune.png"
    }
}


class Planet:
    def __init__(self, x, y, mass, radius, color, image):
        #recieve input in terms of pixels and converts to meters
        self.x = x*scaleFactor
        self.y = y*scaleFactor
        self.mass = mass
        self.radius = radius*scaleFactor
        self.color = color
        self.imagePath = image
        self.img = pygame.image.load(self.imagePath)
        self.radius_scaled = int(self.radius / scaleFactor)
        self.img = pygame.transform.scale(self.img, (self.radius_scaled * 2, self.radius_scaled * 2))
        

        
    def draw(self):
        self.img = pygame.image.load(self.imagePath)
        self.radius_scaled = int(self.radius / scaleFactor)
        self.img = pygame.transform.scale(self.img, (self.radius_scaled * 2, self.radius_scaled * 2))
        pygame.draw.circle(screen, self.color, (int(self.x/scaleFactor), int(self.y/scaleFactor)), self.radius/scaleFactor)
        screen.blit(self.img, (int((self.x-self.radius)/scaleFactor), int((self.y-self.radius)/scaleFactor)))


        
class Projectile:
    def __init__(self, x, y, mass, radius, vx, vy):
        self.x = x*scaleFactor
        self.y = y*scaleFactor
        self.pos = [self.x,self.y]
        self.mass = mass
        self.radius = radius #set to 1e6 large size just for visuals 
        self.vx = vx*scaleFactor
        self.vy = vy*scaleFactor
        self.exist = True
        self.startTime = pygame.time.get_ticks() / 1000.0
        self.time = 0
        self.positions = []
        self.timesUpdated = 0

    
    def update(self, planet, realTime, fallen):
        
        self.x += self.vx*dt 
        self.y += self.vy *dt
        
        self.pos = [self.x, self.y]
        self.time = pygame.time.get_ticks() / 1000.0 - self.startTime
        self.fallen = fallen
        self.timesUpdated+=1

    
        dx = self.x - planet.x  
        dy = self.y - planet.y  
        r = math.sqrt(dx**2 + dy**2)

        F = (G * self.mass * planet.mass) / r**2
        a = F / self.mass

        dirVec = np.array((planet.x - self.x, planet.y - self.y))
        eV = dirVec / np.linalg.norm(dirVec)  
        
        aVector = a * eV
        self.vx += aVector[0] * dt
        self.vy += aVector[1] * dt
        
        
        #print(math.sqrt(self.vx**2+self.vy**2)*1e-3)
        pygame.draw.circle(screen, WHITE, (int(self.x / scaleFactor), int(self.y / scaleFactor)), 10)

        dist = r
        if dist < planet.radius:  # does not take into account the object's radius
            self.exist = False
            self.fallen = True
            print("jaja")
        if self.timesUpdated%200==0:
            self.positions.append([self.x,self.y])
            
    def draw(self):
        if len(self.positions) > 1:
            for i in range(1, len(self.positions),3):
                start_pos = (int(self.positions[i-1][0] / scaleFactor), int(self.positions[i-1][1] / scaleFactor))
                end_pos = (int(self.positions[i][0] / scaleFactor), int(self.positions[i][1] / scaleFactor))
                #pygame.draw.line(screen, WHITE, start_pos, end_pos, 4)
        maxTrailLength = 10
        if len(self.positions) > maxTrailLength:
            self.positions.pop(0)
            
    def drawPath(self, planet, steps=100, timeStep=dt):
        predictedPositions = []
        xPred = self.x
        yPred = self.y
        vxPred = self.vx
        vyPred = self.vy

        for _ in range(steps):
            dx = xPred - planet.x
            dy = yPred - planet.y
            r = math.sqrt(dx**2 + dy**2)
            
            F = (G * self.mass * planet.mass) / r**2
            a = F / self.mass
            
            dirVec = np.array((planet.x - xPred, planet.y - yPred))
            eV = dirVec / np.linalg.norm(dirVec)
            
            aVector = a * eV
            vxPred += aVector[0] * timeStep
            vyPred += aVector[1] * timeStep
            
            xPred += vxPred * timeStep
            yPred += vyPred * timeStep
            
            predictedPositions.append([xPred, yPred])

        return predictedPositions

        
    
def firstClick(num):
    if num%2!=0:
        return True

def main ():
    global scaleFactor
    scaleFactor = 1e5
    global projectile
    projectileRadius = 1e6
    looping = True
    clicks = 0
    projectiles = []
    
    simulationTime = 0.0  
    realTime = pygame.time.get_ticks() / 1000.0
    simulationSpeed = 10
    font = pygame.font.SysFont('Arial', 16)
    dx = 0
    dy = 0
    x1Pos = 0
    y1Pos = 0
    moving = False
    zoom = 1.2
    
    planetChoices = list(planetData.keys()) #returns a list of all names of the planets - nested dictionary is why the key in this case returns the names and not the other values. 
    planetIndex = 0
    planetChoice = "Earth"
    info = planetData[planetChoice]
    planet = Planet(300, 300, info["mass"], float(info["radius"]/scaleFactor), info["color"], info["image"])

    while looping:
        for event in pygame.event.get() :
          if event.type == QUIT :
            pygame.quit()
            sys.exit()
          if event.type == KEYDOWN:
              for projectile in projectiles:
                  projectile.dx = planet.x-projectile.x
                  projectile.dy = planet.y-projectile.y
              if event.key == pygame.K_RIGHT:
                  if planetIndex <(len(planetChoices)-1):
                      planetIndex+=1
                      planetChoice = planetChoices[planetIndex]
                      info = planetData[planetChoice]
                      planet = Planet(300, 300, info["mass"], float(info["radius"]/scaleFactor), info["color"], info["image"])
                      print(planetChoice)

              elif event.key == pygame.K_LEFT:
                          if planetIndex>0:
                              planetIndex-=1
                              planetChoice = planetChoices[planetIndex]
                              info = planetData[planetChoice]
                              planet = Planet(300, 300, info["mass"], float(info["radius"]/scaleFactor), info["color"], info["image"])
                              print(planetChoice)
              elif event.key == pygame.K_d:
                  projectiles=[]
                
                              
              if event.key == K_PLUS or event.key == K_EQUALS:
                  scaleFactor /= zoom
                  planet.radius_scaled = int(planet.radius / scaleFactor)
                  planet.img = pygame.transform.scale(planet.img, (planet.radius_scaled * 2, planet.radius_scaled * 2))
                  planet.x /= zoom
                  planet.y /= zoom
                  
                  #using the fact that the distance in meters between the planet and the projectiles are constant idependent of the zoom. Use minus since pygame uses different coordinate system(??)
                  for projectile in projectiles:
                      projectile.x = planet.x-projectile.dx
                      projectile.y = planet.y-projectile.dy


              elif event.key == K_MINUS:
                  scaleFactor *= zoom
                  planet.radius_scaled = int(planet.radius / scaleFactor)
                  planet.img = pygame.transform.scale(planet.img, (planet.radius_scaled * 2, planet.radius_scaled * 2))
                  planet.x *= zoom
                  planet.y *= zoom

                  for projectile in projectiles:
                      projectile.x = planet.x-projectile.dx
                      projectile.y = planet.y-projectile.dy
          

          if event.type == pygame.MOUSEBUTTONDOWN:
              clicks+=1
              pos = pygame.mouse.get_pos()
              if firstClick(clicks):
                  x1Pos = pos[0]
                  y1Pos = pos[1]

              else:
                  simulationTime = 0
                  x2Pos = pos[0]
                  y2Pos = pos[1]
                  dx = x2Pos-x1Pos
                  dy = y2Pos-y1Pos
                  
                  projectiles.append(Projectile(x1Pos, y1Pos, 1000, 1e6, dx*1e-3, dy*1e-3))
                  print(round(math.sqrt((dx*1e-3*scaleFactor)**2+(dy*1e-3*scaleFactor)**2)*1e-3, 2), "km/s")
                  
                  dx = x1Pos * scaleFactor - planet.x
                  dy = y1Pos * scaleFactor - planet.y
                  distance_m = math.sqrt(dx**2 + dy**2)
                  surface_distance_m = distance_m - planet.radius #does not take into account the radius of the projectile - size of the projectiles is only for visuals
                  print(int(surface_distance_m * 1e-3), "km unna (fra overflate)")

        if projectiles:
            timeElapsed = projectiles[-1].time
        else:
            timeElapsed = 0.0
        screen.blit(bg, (0, 0))

        
        userPos = pygame.mouse.get_pos()
        
        if firstClick(clicks):
            pygame.draw.line(screen, GREEN, (x1Pos, y1Pos), (userPos[0], userPos[1]), 4)
            pygame.draw.circle(screen, WHITE, (x1Pos, y1Pos), 10) #1e6/scaleFactor

        for i in range(simulationSpeed):
            for projectile in projectiles:
                if projectile.exist:
                    projectile.update(planet, realTime, fallen)
                    projectile.draw()
            #updates simulationTime only if the last projectile - the one of interest - has not fallen yet
            if projectiles and projectiles[-1].fallen == False: 
                #simulationTime += dt * simulationSpeed / FPS
                realTime = pygame.time.get_ticks() / 1000.0
                #simulationTime = projectiles[-1].time*100
                simulationTime += dt
            

        
        planet.draw()
        userPos = pygame.mouse.get_pos()
        mouseX = userPos[0]
        mouseY = userPos[1]
        dx = mouseX-x1Pos
        dy = mouseY-y1Pos
        speed = math.sqrt(dx**2+dy**2)*1e-1
        speed = round(math.sqrt((dx*1e-3*scaleFactor)**2+(dy*1e-3*scaleFactor)**2)*1e-3, 2)
        
        if clicks%2==1:
            tempProjectile = Projectile(x1Pos, y1Pos, 1000, 1e6, (userPos[0] - x1Pos) * 1e-3, (userPos[1] - y1Pos) * 1e-3)

            predictedPath = tempProjectile.drawPath(planet, steps=5000)
            for i in range(1, len(predictedPath)):
                start_pos = (int(predictedPath[i-1][0] / scaleFactor), int(predictedPath[i-1][1] / scaleFactor))
                end_pos = (int(predictedPath[i][0] / scaleFactor), int(predictedPath[i][1] / scaleFactor))
                pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)


        if firstClick(clicks):
            mousePlanetDist = math.sqrt((x1Pos * scaleFactor - planet.x)**2 + (y1Pos * scaleFactor - planet.y)**2) - planet.radius
        else:
            mousePlanetDist = math.sqrt((mouseX * scaleFactor - planet.x)**2 + (mouseY * scaleFactor - planet.y)**2) - planet.radius


        mousePlanetDist = round(mousePlanetDist*1e-3, 2)
        
        if projectiles and projectiles[-1].exist: #Only works if there is a projectile
            dxBallPlanet = projectiles[-1].x-planet.x
            dyBallPlanet = projectiles[-1].y-planet.y
        else:
            dxBallPlanet = 0
            dyBallPlanet = 0
        ballPlanetVec = np.array((dxBallPlanet, dyBallPlanet)) 
        ballPlanetDist = (np.linalg.norm(ballPlanetVec)-planet.radius)*1e-3 #Distance between the ball and the planet at all times
        
        dxInitBallPlanet = x1Pos*scaleFactor-planet.x
        dyInitBallPlanet = y1Pos*scaleFactor-planet.y
        initballPlanetVec = np.array((dxInitBallPlanet, dyInitBallPlanet)) #Vector from the initial ball position to the planet (earth)
        
        dxBallMouse = mouseX*scaleFactor-x1Pos*scaleFactor
        dyBallMouse = mouseY*scaleFactor-y1Pos*scaleFactor
        ballMouseVec = np.array((dxBallMouse, dyBallMouse)) #Vector from the initial ball position to the mouse position
        
        #theta = math.acos((np.dot(initballPlanetVec,ballMouseVec))/(np.linalg.norm(initballPlanetVec)*np.linalg.norm(ballMouseVec)))
        theta = math.acos(np.clip(np.dot(initballPlanetVec, ballMouseVec) / (np.linalg.norm(initballPlanetVec) * np.linalg.norm(ballMouseVec)), -1.0, 1.0))
        #TODO research np.clip
        theta = abs(np.rad2deg(theta)-90)
        #print(theta)
        
        

        
        timeText = font.render(f"Sim time: {simulationTime:.1f}s | Real time: {timeElapsed:.1f}s | Distance from planet {ballPlanetDist:.1f}" , True, WHITE)
        simText = font.render(f"New ball distance from surface {mousePlanetDist:.0f}km | Speed {speed:.1f}km/s | Angle {theta:.0f}°" , True, WHITE)
        
        #if not projectiles:
         #   projectileInfo = font.render("none", True, WHITE)
        #else:
         #   if projectiles[-1].fallen:
        projectileInfo = font.render(f"Planet: {planetChoice}", True, WHITE)
        
        screen.blit(timeText, (10, 10))
        screen.blit(simText, (10, 30))

        screen.blit(projectileInfo, (10,50))

        pygame.display.update()
        
        fpsClock.tick(FPS)
 
main()
