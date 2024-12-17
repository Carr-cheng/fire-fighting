import numpy as np
from heapq import heappush, heappop

# 参数设置
FIRE_MIN_FLOW = 400  # 每分钟火灾最小需水量（升/分钟）
FIRE_TOTAL_WATER = 100000  # 火灾总蓄水量（升）
TRUCK_CAPACITY = 6000  # 消防车水容量（升）
TRUCK_FLOW_RATE = 5  # 消防车每秒出水量（升/秒）
HYDRANT_FLOW_RATE = [50, 60, 70]  # 消防栓补水速率（升/秒）
HYDRANT_DISTANCES = [100, 200, 300]  # 消防栓到火点距离（米）
TRUCK_SPEED = 20  # 消防车行驶速度（米/秒）

# 快速检查是否单车可行
def is_feasible_single_truck(hydrant_flow_rates, fire_min_flow, truck_capacity):
    max_refill_rate = max(hydrant_flow_rates)  # 最大补水速率
    single_truck_capacity = truck_capacity + max_refill_rate * 60  # 单车每分钟最大供水能力
    return single_truck_capacity >= fire_min_flow

# 动态水量模拟函数
def simulate_fire_fighting_with_strategy(num_trucks, hydrant_flow_rates, hydrant_distances, fire_min_flow, truck_capacity, truck_flow_rate):
    time = 0
    fire_total_water = FIRE_TOTAL_WATER
    available_water = [truck_capacity] * num_trucks
    hydrant_status = [0] * len(hydrant_flow_rates)  # 消防栓的空闲时间
    event_queue = []
    truck_routes = [[] for _ in range(num_trucks)]  # 记录每辆车的补水和灭火路线
    total_dispatches = 0
    total_distance = 0

    # 初始化任务
    for truck_idx in range(num_trucks):
        heappush(event_queue, (time, truck_idx, "fire"))

    while fire_total_water > 0:
        current_time, truck_idx, event_type = heappop(event_queue)

        if event_type == "fire":
            # 计算灭火所需水量
            water_needed = (fire_min_flow / 60)  # 每秒需求量
            supply = min(water_needed, truck_flow_rate, available_water[truck_idx])
            fire_total_water -= supply
            available_water[truck_idx] -= supply

            # 检查水量是否需要补充
            if available_water[truck_idx] <= truck_flow_rate * 2:  # 剩余不足两秒供水量
                hydrant_idx, travel_time = select_best_hydrant(hydrant_status, hydrant_distances, truck_idx, current_time)
                refill_time = truck_capacity / hydrant_flow_rates[hydrant_idx]

                # 更新消防栓空闲状态
                hydrant_ready_time = max(current_time, hydrant_status[hydrant_idx])
                hydrant_status[hydrant_idx] = hydrant_ready_time + refill_time
                truck_routes[truck_idx].append((hydrant_idx, travel_time))
                total_distance += hydrant_distances[hydrant_idx] * 2  # 往返距离
                total_dispatches += 1

                # 返回灭火点后继续任务
                total_travel_time = travel_time * 2 + refill_time
                heappush(event_queue, (current_time + total_travel_time, truck_idx, "fire"))

                # 补满水
                available_water[truck_idx] = truck_capacity
            else:
                # 如果水量充足，继续灭火
                heappush(event_queue, (current_time + 1, truck_idx, "fire"))

    return current_time, truck_routes, total_distance, total_dispatches

# 选择最佳消防栓
def select_best_hydrant(hydrant_status, hydrant_distances, truck_idx, current_time):
    best_hydrant_idx = -1
    best_time = float('inf')
    for idx, distance in enumerate(hydrant_distances):
        travel_time = distance / TRUCK_SPEED
        available_time = max(current_time, hydrant_status[idx]) + travel_time
        if available_time < best_time:
            best_time = available_time
            best_hydrant_idx = idx
    return best_hydrant_idx, hydrant_distances[best_hydrant_idx] / TRUCK_SPEED

# 目标函数
def objective_function(num_trucks, time, total_distance, total_dispatches):
    # 目标优先级：消防车数量 > 时间 > 调度次数 > 距离
    return (num_trucks * 100000 +
            time * 10 +
            total_dispatches * 2 +
            total_distance * 1)

# 搜索最优解
def optimize_fire_fighting(hydrant_flow_rates, hydrant_distances, fire_min_flow, truck_capacity, truck_flow_rate):
    if not is_feasible_single_truck(hydrant_flow_rates, fire_min_flow, truck_capacity):
        return float('inf'), None  # 单车直接不可行

    best_score = float('inf')
    best_solution = None

    for num_trucks in range(1, 10):  # 假设最多需要10辆车
        time, truck_routes, total_distance, total_dispatches = simulate_fire_fighting_with_strategy(
            num_trucks, hydrant_flow_rates, hydrant_distances, fire_min_flow, truck_capacity, truck_flow_rate
        )
        if time == float('inf'):  # 无法完成任务
            continue

        score = objective_function(num_trucks, time, total_distance, total_dispatches)
        if score < best_score:
            best_score = score
            best_solution = (num_trucks, time, total_distance, total_dispatches, truck_routes)

    return best_solution

# 主函数
def main():
    best_solution = optimize_fire_fighting(
        HYDRANT_FLOW_RATE, HYDRANT_DISTANCES, FIRE_MIN_FLOW, TRUCK_CAPACITY, TRUCK_FLOW_RATE
    )

    if best_solution is None:
        print("无法满足需求，请增加消防车数量或调整参数。")
    else:
        num_trucks, time, total_distance, total_dispatches, truck_routes = best_solution
        print(f"最少消防车数量: {num_trucks}")
        print(f"总灭火时间: {time:.2f} 秒")
        print(f"总行驶距离: {total_distance:.2f} 米")
        print(f"消防车调度总次数: {total_dispatches}")
        print("调度策略：")
        for i, route in enumerate(truck_routes):
            print(f"消防车 {i + 1} 的调度路线: {route}")

if __name__ == "__main__":
    main()
