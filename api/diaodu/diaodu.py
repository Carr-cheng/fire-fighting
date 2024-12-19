import numpy as np
import random
from api import ok
import heapq
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
import threading
from matplotlib.ticker import MaxNLocator
from fastapi import APIRouter, Response
from io import BytesIO
import base64

router = APIRouter()
thread_local = threading.local()
lock = threading.Lock()


plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False

# Constants
P_range = (0, 30)  # Water discharge rate range per fire truck (liters/second)
Refill_rate_range = (0, 30)  # Water refill rate from hydrants (liters/second)
Truck_capacity = 6000  # Each fire truck water capacity (liters)
Max_time = 10000  # Maximum allowed time to extinguish the fire (seconds)
Hydrant_count = 3  # Number of available hydrants
Refill_distance_time = 20  # Time to reach hydrant for refill (seconds)
img=''

# Fire spreading rate function
def fire_spread_rate(Q):
    return 0.000028 * Q ** 2 + 0.016 * Q


# Fire reduction function when q > x
def fire_reduction(Q, q, x):
    return Q - 6 / (1 + np.exp(-0.1 * ((q - x) - 3)))


# Fire increase function when q <= x
def fire_increase(Q, q, x):
    return Q + 6 / (1 + np.exp(-0.1 * ((x - q) - 3)))


# Determine the number of fire trucks needed to extinguish the fire within the allowed time
def find_min_trucks(Q0, x0):
    num_trucks = 1
    while True:
        time_taken, _, _ = simulate_fire_fighting(Q0, x0, num_trucks, plot=False)
        if time_taken <= Max_time:
            return num_trucks
        num_trucks += 1

# Simulate the fire fighting process and return the time taken to extinguish the fire, total water used, and truck movements
def simulate_fire_fighting(Q0, x0, num_trucks, plot=False):
    time = 0
    Q = Q0
    total_water_used = 0
    # Preallocate lists for efficiency
    Q_history = np.zeros(Max_time + 1)
    q_total_history = np.zeros(Max_time + 1)
    x_history = np.zeros(Max_time + 1)
    num_trucks_active = np.zeros(Max_time + 1)
    total_water_history = np.zeros(Max_time + 1)
    trucks_water_history = [np.zeros(Max_time + 1) for _ in range(num_trucks)]

    trucks = [{'water': Truck_capacity, 'refilling': False, 'distance_time': 0, 'return_time': 0, 'movement_log': []}
              for _ in range(num_trucks)]
    hydrants = [None] * Hydrant_count  # Tracks which truck is using each hydrant
    refill_queue = []

    while Q > 0 and time < Max_time:
        # Record current fire intensity
        Q_history[time] = Q
        total_water_history[time] = total_water_used
        num_trucks_active[time] = sum(not truck['refilling'] and truck['return_time'] == 0 for truck in trucks)
        for truck_idx, truck in enumerate(trucks):
            trucks_water_history[truck_idx][time] = truck['water']

        # Calculate the spreading rate
        x = fire_spread_rate(Q)
        x_history[time] = x

        # Calculate the total extinguishing rate
        q_total = 0
        for truck_idx, truck in enumerate(trucks):
            if truck['return_time'] > 0:
                # Truck is returning to the fire site
                truck['return_time'] -= 1
                if truck['return_time'] == 0:
                    truck['movement_log'].append(f"Time {time}: Truck {truck_idx} returned to fire site")
            elif not truck['refilling']:
                p = random.uniform(*P_range)  # Random discharge rate within range
                q = 15 * p / (1 + 0.001 * Q) * np.log(1 + 0.01 * Q)
                if truck['water'] > 0:
                    truck['water'] -= p
                    total_water_used += p
                    if truck['water'] < 0:
                        truck['water'] = 0
                    q_total += q
                else:
                    # Send the truck to refill if it's out of water
                    if len(refill_queue) < Hydrant_count and truck_idx not in refill_queue:
                        truck['refilling'] = True
                        truck['distance_time'] = Refill_distance_time
                        assign_to_hydrant(truck, hydrants)
                        refill_queue.append(truck_idx)
                        truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            else:
                # If truck is traveling to the hydrant
                if truck['distance_time'] > 0:
                    truck['distance_time'] -= 1
                else:
                    # Refill the truck
                    refill_rate = random.uniform(*Refill_rate_range)
                    truck['water'] += refill_rate
                    if truck['water'] >= Truck_capacity:
                        truck['water'] = Truck_capacity
                        truck['refilling'] = False
                        truck['return_time'] = Refill_distance_time  # Add return time
                        release_hydrant(truck, hydrants)
                        if truck_idx in refill_queue:
                            refill_queue.remove(truck_idx)
                        truck['movement_log'].append(
                            f"Time {time}: Truck {truck_idx} finished refilling and returning to fire")

        q_total_history[time] = q_total

        # Update fire intensity based on extinguishing rate
        if q_total > x:
            Q = fire_reduction(Q, q_total, x)
        else:
            Q = fire_increase(Q, q_total, x)

        # Dynamic refill strategy
        for truck_idx, truck in enumerate(trucks):
            if truck['water'] <= 0.1 * Truck_capacity and random.random() < 0.8 and len(refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            elif truck['water'] <= 0.2 * Truck_capacity and random.random() < 0.6 and not truck['refilling'] and len(
                    refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            elif truck['water'] <= 0.4 * Truck_capacity and random.random() < 0.5 and not truck['refilling'] and len(
                    refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            elif truck['water'] <= 0.6 * Truck_capacity and random.random() < 0.2 and not truck['refilling'] and len(
                    refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            elif truck['water'] <= 0.9 * Truck_capacity and random.random() < 0.05 and not truck['refilling'] and len(
                    refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")
            elif truck['water'] == 0 * Truck_capacity and not truck['refilling'] and len(refill_queue) < Hydrant_count:
                truck['refilling'] = True
                truck['distance_time'] = Refill_distance_time
                assign_to_hydrant(truck, hydrants)
                refill_queue.append(truck_idx)
                truck['movement_log'].append(f"Time {time}: Truck {truck_idx} going to refill")

        time += 1

    # Collect movement logs for all trucks
    all_movements = []
    for truck in trucks:
        all_movements.extend(truck['movement_log'])

    # Plotting
    if plot:
        plt.figure(figsize=(15, 10))

        # Fire intensity over time
        plt.subplot(3, 2, 1)
        plt.plot(Q_history[:time], label='火势强度 (Q)', linestyle='-', color='black')
        plt.xlabel('时间 (s)')
        plt.ylabel('火势强度 ')
        plt.legend()
        plt.grid(True)

        # Extinguishing rate and spreading rate over time
        plt.subplot(3, 2, 2)
        plt.plot(q_total_history[:time], label='总灭火速率 (q)', linestyle='-', color='black')
        plt.plot(x_history[:time], label='蔓延速率 (x)', linestyle='--', color='black')
        plt.xlabel('时间 (s)')
        plt.ylabel('速率 (kW/s)')
        plt.legend()
        plt.grid(True)

        # Number of active trucks over time
        plt.subplot(3, 2, 3)
        plt.plot(num_trucks_active[:time], label='灭火车辆数量', linestyle='-', color='black')
        plt.xlabel('时间 (s)')
        plt.ylabel('车辆数量')
        # 设置纵坐标仅保留整数
        ax = plt.gca()  # 获取当前轴
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend()
        plt.grid(True)

        # Total water used over time
        plt.subplot(3, 2, 4)
        plt.plot(total_water_history[:time], label='总用水量 (L)', linestyle='-', color='black')
        plt.xlabel('时间 (s)')
        plt.ylabel('用水量 (L)')
        plt.legend()
        plt.grid(True)

        # Water level of each truck over time
        plt.subplot(3, 2, 5)
        for truck_idx in range(num_trucks):
            plt.plot(trucks_water_history[truck_idx][:time], label=f'车辆 {truck_idx}', linestyle='-', marker='o',
                     markersize=3, alpha=0.7)
        plt.xlabel('时间(s)')
        plt.ylabel('用水量(L)')
        plt.legend()
        plt.grid(True)
        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        plt.close()
        image_data = img_io.read()
        with lock:
            thread_local.image_data = image_data
       # plt.tight_layout()
        #plt.savefig('D://和彩云/4班5组/4班5组/fire_fighting.png') #/frontend/public
       # plt.show()
    return time if Q <= 0 else float('inf'), total_water_used, all_movements


# Assign a truck to an available hydrant based on priority (shortest distance or availability)
def assign_to_hydrant(truck, hydrants):
    for i in range(len(hydrants)):
        if hydrants[i] is None:
            hydrants[i] = truck
            return


# Release a hydrant when a truck finishes refilling
def release_hydrant(truck, hydrants):
    for i in range(len(hydrants)):
        if hydrants[i] == truck:
            hydrants[i] = None
            return


# Dynamic optimization using differential evolution to find optimal parameters
def optimize_fire_fighting(Q0, x0, num_trucks):
    bounds = [(0, 1) for _ in range(num_trucks)]
    result = differential_evolution(lambda x: simulate_fire_fighting(Q0, x0, num_trucks, plot=False)[0], bounds)
    return result.x

# Main function to find the minimum number of trucks and simulate optimal strategy
import asyncio
# 主函数，定义为异步函数
@router.get('/diaodu/{q}',summary="火场供水调度")
async def main(q:int):
    print(q)
    Q0 = q
    x0 = fire_spread_rate(Q0)

    # Find the minimum number of trucks needed
    min_trucks = find_min_trucks(Q0, x0)
    result = []
    movements1 = []
    print(f"Minimum number of trucks required: {min_trucks}")

    # Simulate with the minimum number of trucks to get the optimal time and water usage
    time_taken, total_water_used, movements =await asyncio.to_thread(simulate_fire_fighting(Q0, x0, min_trucks, plot=True))


    for movement in movements:
        movements1.append({"movement": movement})
    with lock:
        imgedata = getattr(thread_local, 'image_data', None)
        if imgedata is not None:
            imgedata = base64.b64encode(imgedata).decode('utf-8')
            del thread_local.image_data
        else:
            imgedata = ''
    result.append({"min_trucks": min_trucks,"time_taken": time_taken, "total_water_used": total_water_used,"img":imgedata, "movements": movements1})
    return ok(data={'result': result})
    # Optimization can be performed here if needed

