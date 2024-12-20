import pygame
import heapq
import math

# Kích thước cửa sổ
WIDTH, HEIGHT = 288 * 4, 180 * 4
NODE_RADIUS = 5

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Thiết lập pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tìm đường đi ngắn nhất bằng Dijkstra")

# Tải ảnh background
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Danh sách các điểm và cạnh
coordinates = [
    (100, 100), (200, 150), (300, 100), (400, 200), (500, 300),
    (600, 400), (700, 200), (250, 400), (350, 500), (450, 450),
    (550, 150), (650, 300), (150, 300), (300, 250), (400, 100),
    (500, 500), (600, 100), (700, 500), (200, 500), (700, 400)
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 13),
    (13, 3), (7, 13), (7, 8), (8, 9), (9, 4), (10, 11), (6, 11),
    (0, 12), (12, 13), (10, 2), (17, 9), (18, 7), (15, 16), (14, 17)
]



# Hàm tính khoảng cách giữa hai điểm
def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Chuyển đổi danh sách cạnh thành đồ thị
graph = {i: [] for i in range(len(coordinates))}
for start, end in edges:
    dist = calculate_distance(coordinates[start], coordinates[end])
    graph[start].append((end, dist))
    graph[end].append((start, dist))  # Đồ thị vô hướng

# Thuật toán Dijkstra
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
            return path

        for neighbor, weight in graph[current_node]:
            new_cost = current_cost + weight
            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                parent_map[neighbor] = current_node
                heapq.heappush(open_list, (new_cost, neighbor))

    return None 




# Tìm điểm gần nhất với vị trí chuột
def find_nearest_point(mouse_pos, points):
    nearest_idx = -1
    min_dist = float("inf")
    for idx, point in enumerate(points):
        dist = calculate_distance(mouse_pos, point)
        if dist < min_dist:
            min_dist = dist
            nearest_idx = idx
    return nearest_idx

# Vẽ đồ thị
def draw_graph(coordinates, edges, path=None, selected_points=None, choose_point=[]):
    # Hiển thị background
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # Vẽ các cạnh
    for start, end in edges:
        pygame.draw.line(screen, GRAY, coordinates[start], coordinates[end], 1)

    # Vẽ các điểm
    for idx, point in enumerate(coordinates):
        color = BLUE  # Màu mặc định
        if selected_points and idx in selected_points:
            color = YELLOW  # Màu cho các điểm đã chọn
        pygame.draw.circle(screen, color, point, NODE_RADIUS)

    # Vẽ đường đi ngắn nhất
    if len(choose_point) == 2 and path != None:
        pygame.draw.circle(screen, RED, choose_point[0], NODE_RADIUS)
        pygame.draw.circle(screen, RED, choose_point[1], NODE_RADIUS)
        pygame.draw.line(screen, (0,0,0), choose_point[0], coordinates[path[0]], 2)
        pygame.draw.line(screen, (0,0,0), coordinates[path[-1]], choose_point[1], 2)
    if path:
        for i in range(len(path) - 1):
            start, end = coordinates[path[i]], coordinates[path[i + 1]]
            pygame.draw.line(screen, (0,0,0), start, end, 2)
            

    pygame.display.flip()

def main():
    running = True
    selected_points = []
    choose_point = []
    path = None

    draw_graph(coordinates, edges)  # Vẽ đồ thị ban đầu

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                nearest_idx = find_nearest_point(mouse_pos, coordinates)
                print(mouse_pos)
                
                # Lưu tọa độ vào file
                with open("mouse_positions.txt", "a") as file:
                    file.write(f"{mouse_pos}\n")
                
                if len(choose_point) < 2:
                    pygame.draw.circle(screen, BLUE, mouse_pos, NODE_RADIUS)
                    choose_point.append(mouse_pos)
                else:
                    choose_point = []
                    choose_point.append(mouse_pos)

                if nearest_idx != -1:
                    selected_points.append(nearest_idx)

                # Nếu đã chọn đủ 2 điểm, tìm đường đi ngắn nhất
                if len(selected_points) == 2:
                    start, goal = selected_points
                    path = dijkstra(graph, start, goal)
                    selected_points = []  # Reset lựa chọn để chọn lại

                # Nếu chọn nút thứ 3, reset tất cả dữ liệu
                if len(selected_points) > 2:
                    selected_points = []  # Reset các điểm đã chọn
                    path = None  # Xoá đường đi đã vẽ

                # Vẽ lại đồ thị và đường đi
                if len(choose_point) == 2:
                    draw_graph(coordinates, edges, path, selected_points, choose_point)
                

    pygame.quit()

if __name__ == "__main__":
    main()


