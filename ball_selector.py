import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
from threading import Timer


class GasMolecule:
    """气体分子类"""

    def __init__(self, x, y, vx, vy, color, size, mass=1):
        self.x = x
        self.y = y
        self.vx = vx  # x方向速度
        self.vy = vy  # y方向速度
        self.color = color
        self.size = size
        self.mass = mass
        self.trail = []  # 轨迹记录
        self.max_trail_length = 20

    def move(self, dt=1):
        """移动分子"""
        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 记录轨迹
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def bounce_walls(self, width, height):
        """与墙壁碰撞检测"""
        # 左右墙壁
        if self.x - self.size <= 0:
            self.x = self.size
            self.vx = -self.vx * 0.8  # 添加能量损失
        elif self.x + self.size >= width:
            self.x = width - self.size
            self.vx = -self.vx * 0.8

        # 上下墙壁
        if self.y - self.size <= 0:
            self.y = self.size
            self.vy = -self.vy * 0.8
        elif self.y + self.size >= height:
            self.y = height - self.size
            self.vy = -self.vy * 0.8

    def collide_with(self, other):
        """分子间碰撞检测和处理"""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < (self.size + other.size):
            # 碰撞发生，计算新的速度
            # 简化的弹性碰撞
            if distance > 0:
                # 单位法向量
                nx = dx / distance
                ny = dy / distance

                # 相对速度在法向量上的投影
                dvn = (other.vx - self.vx) * nx + (other.vy - self.vy) * ny

                # 只有当分子相互接近时才处理碰撞
                if dvn > 0:
                    # 碰撞冲量
                    impulse = 2 * dvn / (self.mass + other.mass)

                    # 更新速度
                    self.vx += impulse * other.mass * nx
                    self.vy += impulse * other.mass * ny
                    other.vx -= impulse * self.mass * nx
                    other.vy -= impulse * self.mass * ny

                    # 分离重叠的分子
                    overlap = (self.size + other.size) - distance
                    separation = overlap / 2 + 1
                    self.x -= nx * separation
                    self.y -= ny * separation
                    other.x += nx * separation
                    other.y += ny * separation


class GasDiffusionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("气体扩散动画模拟器")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f4f8')

        # 模拟参数
        self.box_width = 600
        self.box_height = 400
        self.molecules = []
        self.is_running = False
        self.animation_speed = 50  # 毫秒
        self.temperature = 300  # 温度（影响分子速度）
        self.show_trails = True
        self.gravity_enabled = False
        self.barrier_enabled = False
        self.barrier_x = self.box_width // 2

        self.setup_ui()
        self.setup_simulation()

    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="🧪 气体扩散动画模拟器",
            font=('微软雅黑', 18, 'bold'),
            bg='#f0f4f8',
            fg='#1e293b'
        )
        title_label.pack(pady=(0, 10))

        # 控制面板
        control_frame = tk.LabelFrame(
            main_frame,
            text="控制面板",
            font=('微软雅黑', 12, 'bold'),
            bg='#f0f4f8',
            fg='#374151'
        )
        control_frame.pack(fill='x', pady=(0, 10))

        # 第一行控制按钮
        control_row1 = tk.Frame(control_frame, bg='#f0f4f8')
        control_row1.pack(fill='x', padx=10, pady=5)

        # 开始/暂停按钮
        self.start_btn = tk.Button(
            control_row1,
            text="▶️ 开始模拟",
            font=('微软雅黑', 11, 'bold'),
            bg='#10b981',
            fg='white',
            width=12,
            command=self.toggle_simulation
        )
        self.start_btn.pack(side='left', padx=5)

        # 重置按钮
        reset_btn = tk.Button(
            control_row1,
            text="🔄 重置",
            font=('微软雅黑', 11, 'bold'),
            bg='#ef4444',
            fg='white',
            width=10,
            command=self.reset_simulation
        )
        reset_btn.pack(side='left', padx=5)

        # 添加分子按钮
        add_gas1_btn = tk.Button(
            control_row1,
            text="➕ 氮气(蓝)",
            font=('微软雅黑', 11),
            bg='#3b82f6',
            fg='white',
            width=12,
            command=lambda: self.add_gas('N2')
        )
        add_gas1_btn.pack(side='left', padx=5)

        add_gas2_btn = tk.Button(
            control_row1,
            text="➕ 氧气(红)",
            font=('微软雅黑', 11),
            bg='#dc2626',
            fg='white',
            width=12,
            command=lambda: self.add_gas('O2')
        )
        add_gas2_btn.pack(side='left', padx=5)

        add_gas3_btn = tk.Button(
            control_row1,
            text="➕ 氦气(绿)",
            font=('微软雅黑', 11),
            bg='#059669',
            fg='white',
            width=12,
            command=lambda: self.add_gas('He')
        )
        add_gas3_btn.pack(side='left', padx=5)

        # 第二行控制选项
        control_row2 = tk.Frame(control_frame, bg='#f0f4f8')
        control_row2.pack(fill='x', padx=10, pady=5)

        # 温度控制
        temp_label = tk.Label(control_row2, text="温度:", font=('微软雅黑', 10), bg='#f0f4f8')
        temp_label.pack(side='left', padx=5)

        self.temp_var = tk.IntVar(value=self.temperature)
        temp_scale = tk.Scale(
            control_row2,
            from_=100, to=800,
            orient='horizontal',
            variable=self.temp_var,
            command=self.update_temperature,
            length=150
        )
        temp_scale.pack(side='left', padx=5)

        # 显示轨迹选项
        self.trail_var = tk.BooleanVar(value=self.show_trails)
        trail_check = tk.Checkbutton(
            control_row2,
            text="显示轨迹",
            variable=self.trail_var,
            command=self.toggle_trails,
            bg='#f0f4f8',
            font=('微软雅黑', 10)
        )
        trail_check.pack(side='left', padx=15)

        # 重力选项
        self.gravity_var = tk.BooleanVar(value=self.gravity_enabled)
        gravity_check = tk.Checkbutton(
            control_row2,
            text="启用重力",
            variable=self.gravity_var,
            command=self.toggle_gravity,
            bg='#f0f4f8',
            font=('微软雅黑', 10)
        )
        gravity_check.pack(side='left', padx=15)

        # 隔板选项
        self.barrier_var = tk.BooleanVar(value=self.barrier_enabled)
        barrier_check = tk.Checkbutton(
            control_row2,
            text="中央隔板",
            variable=self.barrier_var,
            command=self.toggle_barrier,
            bg='#f0f4f8',
            font=('微软雅黑', 10)
        )
        barrier_check.pack(side='left', padx=15)

        # 模拟显示区域
        sim_frame = tk.LabelFrame(
            main_frame,
            text="模拟区域",
            font=('微软雅黑', 12, 'bold'),
            bg='#f0f4f8',
            fg='#374151'
        )
        sim_frame.pack(fill='both', expand=True)

        # 画布
        self.canvas = tk.Canvas(
            sim_frame,
            width=self.box_width,
            height=self.box_height,
            bg='#1f2937',
            highlightthickness=2,
            highlightcolor='#374151'
        )
        self.canvas.pack(padx=20, pady=10)

        # 信息显示
        info_frame = tk.Frame(main_frame, bg='#f0f4f8')
        info_frame.pack(fill='x', pady=(10, 0))

        self.info_var = tk.StringVar()
        self.info_var.set("分子数量: 0 | 平均速度: 0.0 | 温度: 300K")

        info_label = tk.Label(
            info_frame,
            textvariable=self.info_var,
            font=('微软雅黑', 11),
            bg='#f0f4f8',
            fg='#6b7280'
        )
        info_label.pack()

        # 绘制箱子边框
        self.draw_container()

    def setup_simulation(self):
        """设置初始模拟状态"""
        # 添加初始分子
        self.add_gas('N2', count=20)
        self.add_gas('O2', count=15)

    def draw_container(self):
        """绘制容器"""
        # 清除画布
        self.canvas.delete("container")

        # 绘制箱子边框
        self.canvas.create_rectangle(
            2, 2, self.box_width - 2, self.box_height - 2,
            outline='#60a5fa', width=3, tags="container"
        )

        # 绘制隔板（如果启用）
        if self.barrier_enabled:
            self.canvas.create_line(
                self.barrier_x, 2,
                self.barrier_x, self.box_height // 2 - 50,
                fill='#fbbf24', width=4, tags="container"
            )
            self.canvas.create_line(
                self.barrier_x, self.box_height // 2 + 50,
                self.barrier_x, self.box_height - 2,
                fill='#fbbf24', width=4, tags="container"
            )

    def add_gas(self, gas_type, count=10):
        """添加气体分子"""
        gas_properties = {
            'N2': {'color': '#3b82f6', 'size': 4, 'mass': 28},
            'O2': {'color': '#dc2626', 'size': 5, 'mass': 32},
            'He': {'color': '#059669', 'size': 3, 'mass': 4}
        }

        props = gas_properties[gas_type]

        for _ in range(count):
            # 随机位置（避开边界）
            if self.barrier_enabled and len(self.molecules) % 2 == 0:
                # 在左半边添加
                x = random.uniform(props['size'] + 5, self.barrier_x - 10)
            elif self.barrier_enabled:
                # 在右半边添加
                x = random.uniform(self.barrier_x + 10, self.box_width - props['size'] - 5)
            else:
                x = random.uniform(props['size'] + 5, self.box_width - props['size'] - 5)

            y = random.uniform(props['size'] + 5, self.box_height - props['size'] - 5)

            # 根据温度计算初始速度
            speed_factor = math.sqrt(self.temperature / props['mass']) / 10
            vx = random.uniform(-1, 1) * speed_factor
            vy = random.uniform(-1, 1) * speed_factor

            molecule = GasMolecule(
                x, y, vx, vy,
                props['color'],
                props['size'],
                props['mass']
            )

            self.molecules.append(molecule)

    def update_temperature(self, value):
        """更新温度"""
        self.temperature = int(value)
        # 调整所有分子的速度
        for molecule in self.molecules:
            speed_factor = math.sqrt(self.temperature / molecule.mass) / 10
