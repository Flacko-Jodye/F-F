import json
import os

# 创建节点
nodes = {str(i): {} for i in range(1, 101)}
nodes["source"] = {}
nodes["sink"] = {}

arcs = []

# 添加瓶颈路径: source -> 1 -> 2 -> ... -> 99 -> sink，每条边容量为1
arcs.append({"start": "source", "end": "1", "capacity": 1})
for i in range(1, 100):
    arcs.append({"start": str(i), "end": str(i + 1), "capacity": 1})
arcs.append({"start": "100", "end": "sink", "capacity": 1})

# 添加一些大容量路径
for i in range(1, 21):
    arcs.append({"start": "source", "end": str(i), "capacity": 1000000})
    arcs.append({"start": str(i), "end": "sink", "capacity": 1000000})

# 生成图的字典
network = {
    "nodes": nodes,
    "arcs": arcs
}

# 将图保存为JSON文件
output_dir = r"D:\Fub SS 2024\Metaheurisitk\F-F\Data"
output_file = os.path.join(output_dir, "Neuneuinstanz.json")
os.makedirs(output_dir, exist_ok=True)
with open(output_file, "w") as f:
    json.dump(network, f, indent=4)

print(f"JSON file saved to {output_file}")
