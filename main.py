import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random

class Tygrys:
    def __init__(self, x, y, alpha, beta, gamma, a, b, d):
        self.x = x
        self.y = y
        self.alpha = alpha # kat kierunku ruchu tygrysa
        self.beta = beta # kat ogona tygrysa
        self.gamma = gamma # kat pola widzenia tygrysa
        self.a = a # dlugosc pola widzenia tygrysa
        self.b = b # dlugosc ogona
        self.d = d # dlugosc owijki
        self.is_alive = True # na poczatku wszystkie tygrysy zyja
    
    def move(self, bounding_box=100):
        direction = self.alpha + random.uniform(-self.gamma, self.gamma)
        
        new_x = self.x + self.b * math.cos(math.radians(direction))
        new_y = self.y + self.b * math.sin(math.radians(direction))
        
        # kolizja z siatka
        if new_x < 0:
            new_x = -new_x
            self.alpha = 180 - self.alpha
        elif new_x > bounding_box:
            new_x = 2 * bounding_box - new_x
            self.alpha = 180 - self.alpha
        
        if new_y < 0:
            new_y = -new_y
            self.alpha = -self.alpha
        elif new_y > bounding_box:
            new_y = 2 * bounding_box - new_y
            self.alpha = -self.alpha
        
        self.x = new_x
        self.y = new_y
        
        return self.x, self.y
    
    def point_in_hull(self, point, hull_points):

        if not hull_points or len(hull_points) < 3:
            return True  
        
        x, y = point
        n = len(hull_points)
        inside = False
        
        p1x, p1y = hull_points[0]
        for i in range(n + 1):
            p2x, p2y = hull_points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def stopping_point(self, point, hull_points):

        if not hull_points or len(hull_points) < 3:
            return point
        
        if self.point_in_hull(point, hull_points):
            return point
        
        # najblizszy punkt na owijce
        min_dist = float('inf')
        closest_point = point
        
        for i in range(len(hull_points)):
            p1 = hull_points[i]
            p2 = hull_points[(i + 1) % len(hull_points)]
            
            line_vec = (p2[0] - p1[0], p2[1] - p1[1])
            point_vec = (point[0] - p1[0], point[1] - p1[1])
            
            t = max(0, min(1, 
                (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / 
                (line_vec[0]**2 + line_vec[1]**2)
            ))
            
            proj_point = (
                p1[0] + t * line_vec[0],
                p1[1] + t * line_vec[1]
            )
            
            dist = math.sqrt(
                (point[0] - proj_point[0])**2 + 
                (point[1] - proj_point[1])**2
            )
            
            if dist < min_dist:
                min_dist = dist
                closest_point = proj_point
        
        return closest_point
    
    def possible_tail_positions(self, hull_points=None):

        tail_positions = []
        for _ in range(5):
            tail_angle = self.alpha + 180 + random.uniform(-self.beta, self.beta)
            tail_x = self.x + self.b * math.cos(math.radians(tail_angle))
            tail_y = self.y + self.b * math.sin(math.radians(tail_angle))
            
            if hull_points:
                tail_x, tail_y = self.stopping_point((tail_x, tail_y), hull_points)
            
            tail_positions.append((tail_x, tail_y))
        return tail_positions
    
    def possible_future_positions(self, hull_points=None):

        future_positions = []
        for _ in range(5):
            future_alpha = self.alpha + random.uniform(-self.gamma, self.gamma)
            future_x = self.x + self.b * math.cos(math.radians(future_alpha))
            future_y = self.y + self.b * math.sin(math.radians(future_alpha))
            
            if hull_points:
                future_x, future_y = self.stopping_point((future_x, future_y), hull_points)
            
            future_positions.append((future_x, future_y))
        return future_positions

def direction(p, q, r):
    dir = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    
    if dir == 0: # punkty wspolliniowe
        return 0 
    return 1 if dir > 0 else 2 # obrot zgodnie z kierunkiem wskazowek zegara lub przeciwnie

def gift_wrapping(points, bounding_box=100):
    # punkty w ograniczonym obszarze
    filtered_points = [
        point for point in points 
        if 0 <= point[0] <= bounding_box and 0 <= point[1] <= bounding_box
    ]
    
    n = len(filtered_points)
    
    if n < 3: # nie mozna zrobic owijki jak jest mniej niz 3 punkty
        return filtered_points
    
    l = min(range(n), key=lambda i: filtered_points[i][0])
    
    hull = [] # lista punktow owijki
    p = l # punkt startowy
    q = 0 # kolejny punkt
    
    while True:
        hull.append(filtered_points[p])
        
        q = (p + 1) % n
        
        for i in range(n):
            if direction(filtered_points[p], filtered_points[i], filtered_points[q]) == 2:
                q = i
        
        p = q
        
        if p == l:
            break
    
    return hull

def spawn_tigers(num_tigers=20):
    random.seed(69)
    tigers = []
    for _ in range(num_tigers):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        alpha = random.uniform(0, 360)
        beta = random.uniform(0, 90)
        gamma = random.uniform(0, 45)
        a = random.uniform(0, 10)
        b = random.uniform(0, 20)
        d = 10
        
        tiger = Tygrys(x, y, alpha, beta, gamma, a, b, d)
        tigers.append(tiger)
    
    return tigers

def check_collision(tiger1, tiger2, collision_radius=5): 
    distance = math.sqrt((tiger1.x - tiger2.x)**2 + (tiger1.y - tiger2.y)**2)
    return distance < collision_radius

def collision(tigers):
    for i in range(len(tigers)):
        if not tigers[i].is_alive:
            continue
        
        for j in range(i+1, len(tigers)):
            if not tigers[j].is_alive:
                continue
            
            if check_collision(tigers[i], tigers[j]):
                # walka tygrysow
                if tigers[i].b < tigers[j].b:
                    tigers[i].is_alive = False
                else:
                    tigers[j].is_alive = False

def animate_tigers(time_steps=10):
    fig, ax = plt.subplots(figsize=(8, 8))
    bounding_box = 100
    
    # inicjacja pozycji tygrysow
    tigers = spawn_tigers()
    
    all_tiger_data = []
    for _ in range(time_steps):
        collision(tigers)
        
        # ruch tylko dla zywych tygrysow
        tiger_positions = []
        for tiger in tigers:
            if tiger.is_alive:
                tiger_positions.append(tiger.move(bounding_box))
        
        # dodatkowe punkty, czyli ogon i przyszle pozycje
        additional_points = []
        for tiger in tigers:
            if tiger.is_alive:
                additional_points.extend(tiger.possible_tail_positions())
                additional_points.extend(tiger.possible_future_positions())
        
        try:
            hull_points = gift_wrapping(tiger_positions + additional_points, bounding_box)
        except Exception:
            hull_points = []
        
        all_tiger_data.append({
            'positions': tiger_positions,
            'tail_positions': [tiger.possible_tail_positions(hull_points) for tiger in tigers if tiger.is_alive],
            'future_positions': [tiger.possible_future_positions(hull_points) for tiger in tigers if tiger.is_alive],
            'hull_points': hull_points,
            'tigers': tigers  
        })
    
    def update(frame):
        ax.clear()
        ax.set_xlim(0, bounding_box)
        ax.set_ylim(0, bounding_box)
        ax.set_title(f'Ruch tygrysów, czas: {frame}')
        ax.grid(True)
        
        current_data = all_tiger_data[frame]
        
        # rysowanie zywych tygrysow
        x_cords = [pos[0] for pos in current_data['positions']]
        y_cords = [pos[1] for pos in current_data['positions']]
        ax.scatter(x_cords, y_cords, c='orange', label='nie-zabity tygrys')
        
        # rysowanie martwych tygrysow
        dead_tigers = [tiger for tiger in current_data['tigers'] if not tiger.is_alive]
        if dead_tigers:
            dead_x = [tiger.x for tiger in dead_tigers]
            dead_y = [tiger.y for tiger in dead_tigers]
            ax.scatter(dead_x, dead_y, c='black', marker='x', label='tu zginie tygrys :(')
        
        # rysowanie owijki
        if current_data['hull_points'] and len(current_data['hull_points']) >= 3:
            hull_x = [p[0] for p in current_data['hull_points'] + [current_data['hull_points'][0]]]
            hull_y = [p[1] for p in current_data['hull_points'] + [current_data['hull_points'][0]]]
            ax.plot(hull_x, hull_y, 'b-', label='ogrodzenie')
        
        # rysowanie ogonow i przyszlych pozycji dla zywych tygrysow
        for tiger_index, tiger_pos in enumerate(current_data['positions']):
            tail_positions = current_data['tail_positions'][tiger_index]
            future_positions = current_data['future_positions'][tiger_index]
            
            tail_x = [pos[0] for pos in tail_positions]
            tail_y = [pos[1] for pos in tail_positions]
            future_x = [pos[0] for pos in future_positions]
            future_y = [pos[1] for pos in future_positions]
            
            # linie od aktualnej pozycji
            for tx, ty in zip(tail_x, tail_y):
                ax.plot([tiger_pos[0], tx], [tiger_pos[1], ty], 'y--')
            
            for fx, fy in zip(future_x, future_y):
                ax.plot([tiger_pos[0], fx], [tiger_pos[1], fy], 'r--')
            
            # ogony i przyszle pozycje
            ax.scatter(tail_x, tail_y, c='yellow', marker='o')
            ax.scatter(future_x, future_y, c='purple', marker='x')
        
        ax.legend(loc='best')
        return ax
    
    anim = animation.FuncAnimation(fig, update, frames=time_steps, interval=900, repeat=True)

    try:
        anim.save('tiger_movement.gif', writer='pillow')
    except Exception as e:
        print(f"Could not save GIF: {e}")
    
    plt.show()

animate_tigers()