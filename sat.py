import pygame
import requests
import json

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 24)
camera_x, camera_y = 0, 0
dragging = False
last_mouse_x, last_mouse_y = 0, 0
API_KEY = "SBN5DE-MX433Y-QVNQHX-5FI1"
SATELLITES = [25544, 33591, 37849]

def get_satellite_positions():
    positions = []
    for sat_id in SATELLITES:
        url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/0/0/0/1/&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "positions" in data:
            pos = data["positions"][0]
            positions.append((pos["satlatitude"], pos["satlongitude"]))
    return positions

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            last_mouse_x, last_mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            dx, dy = event.pos[0] - last_mouse_x, event.pos[1] - last_mouse_y
            camera_x += dx
            camera_y += dy
            last_mouse_x, last_mouse_y = event.pos

    for lat, lon in get_satellite_positions():
        x, y = int((lon + 180) * (800 / 360)) + camera_x, int((90 - lat) * (600 / 180)) + camera_y
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)
        text = font.render(f"{lat:.2f}, {lon:.2f}", True, (255, 255, 255))
        screen.blit(text, (x + 10, y))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
