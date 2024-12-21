import pygame
import heapq
import math
import time 
import pygame_menu


WIDTH, HEIGHT = 288 * 4, 180 * 4
NODE_RADIUS = 5


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bản đồ Phường Nguyễn Trung Trực")


background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


coordinates = [
    (660, 717), (614, 588), (578, 415), (567, 224), (660, 382), (417, 387),
    (290, 360), (341, 180), (265, 412), (371, 474), (983, 618), (573, 677),
    (1026, 576), (587, 145), (432, 8), (641, 675), (878, 649), (366, 111),
    (836, 523), (784, 680), (742, 552), (727, 341), (801, 434), (830, 465),
    (864, 428), (864, 471), (882, 464), (773, 370), (781, 413), (601, 139),
    (997, 582), (1000, 607), (1019, 583), (993, 611), (1001, 590), (966, 554),
    (1023, 580), (1006, 600), (879, 479), (610, 127), (1012, 592), (570, 161),
    (392, 29), (837, 404), (821, 384), (807, 565), (799, 531), (514, 604),
    (459, 531), (469, 592), (491, 673), (761, 606), (710, 705), (1005, 557),
    (604, 117), (621, 138), (595, 158), (576, 135), (607, 146), (590, 126),
    (962, 590), (449, 19), (631, 205), (287, 222), (323, 231), (575, 556),
    (606, 547), (573, 537), (601, 532), (437, 418), (448, 389), (273, 276),
    (309, 286), (317, 263), (627, 464), (588, 471), (634, 523), (603, 521),
    (330, 333), (296, 324), (358, 274), (864, 501), (322, 542), (279, 525),
    (342, 519), (376, 540), (384, 523), (316, 481), (351, 501), (281, 482),
    (261, 500), (275, 507), (225, 486), (205, 408), (253, 437), (207, 442),
    (236, 466), (161, 341), (331, 576), (367, 620), (342, 556), (378, 602),
    (412, 515), (417, 568), (452, 589), (491, 618), (566, 611), (557, 676),
    (542, 607), (539, 679), (560, 581), (611, 566), (546, 589), (476, 513),
    (434, 461), (417, 481), (504, 485), (400, 8), (523, 191), (519, 217), 
    (611, 178), (653, 239), (689, 288), (780, 336),(738, 285),(690, 225),(643, 163),
    (492, 48), (547, 94), (564, 70), (693, 623), (855, 582), (570, 303), (431, 197),
    (449, 156)
]






edges = [(0, 15), (0, 52), (1, 20), (1, 15), (2, 116), (2, 75), (2, 4), (2, 70), (3, 2), 
         (3, 119), (3, 62), (4, 20), (4, 21), (4, 2), (5, 9), (5, 70), (5, 6), (6, 79), 
         (6, 8), (6, 5), (7, 64), (7, 17), (8, 94), (8, 9), (8, 6), (8, 97), (9, 5), (9, 88), (9, 8), 
         (11, 107), (12, 36), (12, 53), (13, 56), (13, 29), (13, 41), (14, 61), (14, 117), (15, 11), (16, 10), 
         (16, 18), (17, 118), (17, 42), (17, 7), (18, 81), (18, 46), (18, 16), (19, 51), (19, 16), (20, 4), (20, 46), 
         (20, 51), (20, 1), (21, 28), (22, 23), (23, 25), (23, 81), (24, 43), (25, 38), (25, 60), (26, 38), (26, 24), (27, 58), 
         (27, 28), (28, 22), (29, 13), (29, 59), (29, 58), (29, 39), (30, 34), (30, 32), (30, 31), (31, 37), (31, 33), (31, 30), 
         (32, 36), (32, 40), (32, 30), (33, 31), (33, 35), (34, 30), (34, 40), (34, 37), (35, 38), (35, 36), (35, 33), (36, 32), 
         (36, 12), (36, 35), (37, 31), (37, 34), (38, 35), (38, 25), (38, 26), (39, 54), (39, 29), (40, 32), (40, 34), (41, 3), (41, 42), 
         (42, 117), (42, 41), (42, 61), (42, 17), (43, 44), (43, 22), (44, 27), (44, 55), (45, 46), (46, 45), (46, 18), (46, 20), (47, 48), 
         (48, 103), (48, 113), (48, 47), (49, 105), (50, 105), (51, 20), (51, 19), (51, 52), (52, 19), (52, 51), (53, 26), (53, 24), (54, 59), (55, 39), 
         (55, 58), (56, 62), (56, 58), (57, 13), (57, 59), (58, 55), (58, 56), (58, 29), (58, 27), (59, 29), (59, 54), (59, 57), (60, 10), (61, 57), (62, 21), 
         (63, 64), (64, 73), (64, 63), (64, 7), (65, 66), (66, 111), (66, 65), (67, 68), (68, 66), (68, 67), (69, 70), (70, 5), (70, 69), (70, 2), (71, 72), (72, 73), 
         (72, 79), (72, 71), (73, 64), (73, 72), (73, 80), (74, 75), (75, 77), (75, 74), (76, 77), (77, 68), (77, 76), (78, 79), (79, 72), (79, 78), (79, 6), (80, 73), 
         (81, 18), (81, 60), (82, 83), (82, 84), (83, 82), (84, 88), (84, 85), (84, 82), (85, 84), (86, 88), (87, 88), (88, 9), (88, 84), (88, 87), (88, 86), (89, 90), 
         (90, 89), (90, 91), (90, 92), (91, 90), (92, 96), (92, 90), (93, 94), (94, 8), (94, 96), (94, 93), (95, 96), (96, 94), (96, 92), (96, 95), (97, 8), (98, 99), 
         (99, 101), (99, 98), (100, 101), (101, 99), (101, 103), (101, 100), (102, 103), (103, 101), (103, 48), (103, 102), (104, 105), (105, 49), (105, 50), (105, 104), 
         (106, 107), (107, 106), (107, 109), (108, 109), (109, 108), (109, 50), (110, 111), (111, 1), (111, 110), (112, 113), (113, 48), (113, 116), (113, 114), (113, 112), 
         (114, 113), (114, 115), (114, 116), (115, 114), (116, 113), (116, 2), (116, 114), (117, 14), (117, 42), (118, 3), (118, 119), (119, 7), (56,120), (120,62), (62,121),
         (121,122), (122,21), (44,123), (123,124), (124,125), (125,126), (126,55), (61, 127), (127,128), (128,57), (54,129), (51,130), (130,51), (130, 52), (52, 130), (131,16), (16,131),
         (131,18), (18, 131), (3,132), (132,2), (119, 133), (133,7), (17, 134), (134, 118)]


border = [(158, 344),
          (203, 413),
          (205, 443),
          (227, 484),
          (262, 509),
          (280, 526),
          (329, 575),
          (366, 620),
          (488, 672),
          (659, 717),
          (712, 705),
          (785, 685),
          (881, 654),
          (985, 620),
          (1048, 573),
          (520, 12),
          (380, 2),
          (162, 338)]



def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


graph = {i: [] for i in range(len(coordinates))}
for start, end in edges:
    dist = calculate_distance(coordinates[start], coordinates[end])
    graph[start].append((end, dist))

def dijkstra(graph, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    g_costs = {start: 0}
    parent_map = {start: None}

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent_map[current_node]
            path.reverse()
            return path, g_costs[goal]

        for neighbor, weight in graph[current_node]:
            new_cost = current_cost + weight
            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                parent_map[neighbor] = current_node
                heapq.heappush(open_list, (new_cost, neighbor))

    return None, float('inf')


def a_star(graph, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    g_costs = {start: 0}
    h_costs = {start: calculate_distance(coordinates[start], coordinates[goal])}
    parent_map = {start: None}

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent_map[current_node]
            path.reverse()
            return path, g_costs[goal]

        for neighbor, weight in graph[current_node]:
            tentative_g_cost = g_costs[current_node] + weight
            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_cost
                h_costs[neighbor] = calculate_distance(coordinates[neighbor], coordinates[goal])
                parent_map[neighbor] = current_node
                f_cost = g_costs[neighbor] + h_costs[neighbor]
                heapq.heappush(open_list, (f_cost, neighbor))

    return None, float('inf')


def bellman_ford(graph, start, goal):
    g_costs = {i: float('inf') for i in graph}
    g_costs[start] = 0
    parent_map = {start: None}

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if g_costs[node] + weight < g_costs[neighbor]:
                    g_costs[neighbor] = g_costs[node] + weight
                    parent_map[neighbor] = node

    if g_costs[goal] == float('inf'):
        return None, float('inf')

    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = parent_map[current_node]
    path.reverse()
    return path, g_costs[goal]


def floyd_warshall(graph, start, goal):
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
    for u in graph:
        for v, weight in graph[u]:
            dist[u][v] = weight
            next_node[u][v] = v

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    if dist[start][goal] == float('inf'):
        return None, float('inf')

    path = []
    current_node = start
    while current_node != goal:
        if current_node is None:
            return None, float('inf')
        path.append(current_node)
        current_node = next_node[current_node][goal]
    path.append(goal)
    return path, dist[start][goal]


def find_nearest_point(mouse_pos, points):
    nearest_idx = -1
    min_dist = float("inf")
    for idx, point in enumerate(points):
        dist = calculate_distance(mouse_pos, point)
        if dist < min_dist:
            min_dist = dist
            nearest_idx = idx
    return nearest_idx

def draw_graph(coordinates, edges, distance, time_taken, path=None, choose_point=[]):
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    for start, end in edges:
        pygame.draw.line(screen, (122, 15, 200), coordinates[start], coordinates[end], 1)
        
    for i in range(len(border) - 1):
        pygame.draw.line(screen, BLUE, border[i], border[i + 1], 4)
    pygame.draw.line(screen, BLUE, border[-1], border[0], 4)

    for idx, point in enumerate(coordinates):
        color = BLUE
        pygame.draw.circle(screen, color, point, 1)

    if len(choose_point) == 2 and path:
        pygame.draw.circle(screen, RED, choose_point[0], NODE_RADIUS)
        pygame.draw.circle(screen, RED, choose_point[1], NODE_RADIUS)
        pygame.draw.line(screen, (0, 0, 0), choose_point[0], coordinates[path[0]], 5)
        pygame.draw.line(screen, (0, 0, 0), coordinates[path[-1]], choose_point[1], 5)

    if path:
        for i in range(len(path) - 1):
            start, end = coordinates[path[i]], coordinates[path[i + 1]]
            pygame.draw.line(screen, (0, 0, 0), start, end, 5)

    if distance is not None and time_taken is not None:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance: {distance}, Time: {time_taken}s", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.topright = (WIDTH - 10, 10)
        screen.blit(text, text_rect)

    pygame.display.flip()

def main(mode):
    running = True
    choose_point = []
    path = None

    draw_graph(coordinates, edges, None, None)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                nearest_idx = find_nearest_point(mouse_pos, coordinates)

                if len(choose_point) < 2:
                    choose_point.append(mouse_pos)
                else:
                    choose_point = [mouse_pos]

                if nearest_idx != -1 and len(choose_point) == 2:
                    time_start = time.time()
                    start, goal = [find_nearest_point(p, coordinates) for p in choose_point]
                    
                    if mode == 'dijkstra':
                        path, distance = dijkstra(graph, start, goal)
                    elif mode == 'a_star':
                        path, distance = a_star(graph, start, goal)
                    elif mode == 'bellman_ford':
                        path, distance = bellman_ford(graph, start, goal)
                    elif mode == 'floyd_warshall':
                        path, distance = floyd_warshall(graph, start, goal)
                    time_taken = time.time() - time_start
                    time_taken = round(time_taken, 6)
                    distance += calculate_distance(choose_point[0], coordinates[path[0]]) + calculate_distance(choose_point[1], coordinates[path[-1]])
                    distance = round(distance, 2)
                    draw_graph(coordinates, edges, distance, time_taken, path, choose_point)

    pygame.quit()

