
import tkinter as tk
from tkinter import ttk
import random
import time
from threading import Timer
import math

class AnimatedBallSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("双色球动画选号器 - 5蓝+2红")
        self.root.geometry("900x650")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)
        
        # 球的配置
        self.blue_balls = list(range(1, 36))  # 35个蓝球：1-35
        self.red_balls = list(range(1, 13))   # 12个红球：1-12
        
        # 选中的球
        self.selected_blue = []
        self.selected_red = []
        self.is_selecting = False  # 是否正在选择动画中
        
        # 球体对象存储
        self.blue_ball_objects = {}  # 存储球体canvas对象
        self.red_ball_objects = {}
        
        # 动画相关
        self.selection_queue = []  # 选择队列
        self.current_animation = None
        
        # 装饰动画相关
        self.decoration_timers = []
        self.left_particles = []  # 左侧粒子系统
        self.right_wave_angle = 0  # 右侧波浪动画角度
        self.animation_frame = 0  # 动画帧计数
        
        self.setup_ui()
        self.create_balls()
        self.init_particles()
        self.start_decoration_animations()
    
    def setup_ui(self):
        # 创建主容器
        main_container = tk.Frame(self.root, bg='#f0f4f8')
        main_container.pack(fill='both', expand=True)
        
        # 顶部装饰区域
        top_frame = tk.Frame(main_container, bg='#f0f4f8', height=120)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        # 左上角装饰 - 粒子飘落动画
        self.left_decoration = tk.Canvas(
            top_frame, 
            bg='#f0f4f8', 
            width=200, 
            height=120,
            highlightthickness=0
        )
        self.left_decoration.pack(side='left', padx=10)
        
        # 中央标题区域
        center_frame = tk.Frame(top_frame, bg='#f0f4f8')
        center_frame.pack(side='left', expand=True, fill='both')
        
        # 标题
        title_label = tk.Label(
            center_frame,
            text="🎱 双色球动画选号器",
            font=("微软雅黑", 20, "bold"),
            bg='#f0f4f8',
            fg='#1e293b'
        )
        title_label.pack(pady=(15, 5))
        
        # 规则说明
        rule_label = tk.Label(
            center_frame,
            text="规则：从35个蓝球中选5个 + 从12个红球中选2个 = 共7个球",
            font=("微软雅黑", 11),
            bg='#f0f4f8',
            fg='#64748b'
        )
        rule_label.pack()
        
        # 动画说明
        anim_label = tk.Label(
            center_frame,
            text="✨ 动画选号：逐个选择，每个球间隔2秒，选中球会小幅弹出显示",
            font=("微软雅黑", 10),
            bg='#f0f4f8',
            fg='#7c3aed'
        )
        anim_label.pack()
        
        # 右上角装饰 - 彩虹波纹动画
        self.right_decoration = tk.Canvas(
            top_frame, 
            bg='#f0f4f8', 
            width=200, 
            height=120,
            highlightthickness=0
        )
        self.right_decoration.pack(side='right', padx=10)
        
        # 按钮和结果区域
        control_frame = tk.Frame(main_container, bg='#f0f4f8', height=80)
        control_frame.pack(fill='x', pady=5)
        control_frame.pack_propagate(False)
        
        # 按钮容器
        btn_container = tk.Frame(control_frame, bg='#f0f4f8')
        btn_container.pack(pady=10)
        
        # 选号按钮
        self.btn_select = tk.Button(
            btn_container,
            text="🎯 开始动画选号",
            font=("微软雅黑", 14, "bold"),
            bg='#3b82f6',
            fg='white',
            width=18,
            height=2,
            command=self.start_selection_animation,
            cursor='hand2',
            relief='raised',
            bd=3
        )
        self.btn_select.pack(side='left', padx=10)
        
        # 清空按钮
        self.btn_clear = tk.Button(
            btn_container,
            text="🔄 重新选号",
            font=("微软雅黑", 14, "bold"),
            bg='#ef4444',
            fg='white',
            width=15,
            height=2,
            command=self.clear_selection,
            cursor='hand2',
            relief='raised',
            bd=3
        )
        self.btn_clear.pack(side='left', padx=10)
        
        # 结果显示
        self.result_var = tk.StringVar()
        self.result_var.set('点击"开始动画选号"按钮进行选择')
        
        result_label = tk.Label(
            control_frame,
            textvariable=self.result_var,
            font=("微软雅黑", 12, "bold"),
            bg='#f0f4f8',
            fg='#1e293b',
            wraplength=800
        )
        result_label.pack(pady=(10, 0))
        
        # 球池显示区域
        balls_frame = tk.Frame(main_container, bg='#f0f4f8')
        balls_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # 蓝球区域
        self.blue_frame = tk.LabelFrame(
            balls_frame,
            text="🔵 蓝球池 (选5个)",
            font=("微软雅黑", 14, "bold"),
            bg='#f0f4f8',
            fg='#1e40af',
            bd=2,
            relief='groove'
        )
        self.blue_frame.pack(fill='x', pady=(0, 10))
        
        # 红球区域
        self.red_frame = tk.LabelFrame(
            balls_frame,
            text="🔴 红球池 (选2个)",
            font=("微软雅黑", 14, "bold"),
            bg='#f0f4f8',
            fg='#dc2626',
            bd=2,
            relief='groove'
        )
        self.red_frame.pack(fill='x')
        
        # 创建小弹出球显示区域
        self.popup_frame = tk.Frame(self.root, bg='#f0f4f8')
        self.popup_frame.place_forget()
        
        self.popup_canvas = tk.Canvas(
            self.popup_frame,
            bg='#f0f4f8',
            highlightthickness=0,
            width=60,
            height=60
        )
        self.popup_canvas.pack()
    
    def create_balls(self):
        # 创建蓝球Canvas - 12列3行布局
        blue_canvas = tk.Canvas(
            self.blue_frame, 
            bg='#f0f4f8', 
            height=180,
            highlightthickness=0
        )
        blue_canvas.pack(padx=15, pady=15, fill='x')
        
        # 计算蓝球位置并绘制
        ball_size = 28  # 球的直径
        spacing_x = 65   # 水平间距
        spacing_y = 55   # 垂直间距
        start_x = 40     # 起始X位置
        start_y = 35     # 起始Y位置
        
        for i, ball_num in enumerate(self.blue_balls):
            row = i // 12
            col = i % 12
            
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            # 绘制球体（圆形）
            ball_id = blue_canvas.create_oval(
                x - ball_size//2, y - ball_size//2,
                x + ball_size//2, y + ball_size//2,
                fill='#2563eb',
                outline='#1d4ed8',
                width=2,
                tags=f'blue_{ball_num}'
            )
            
            # 绘制球号
            text_id = blue_canvas.create_text(
                x, y,
                text=str(ball_num),
                fill='white',
                font=('Arial', 10, 'bold'),
                tags=f'blue_{ball_num}_text'
            )
            
            # 存储球对象信息
            self.blue_ball_objects[ball_num] = {
                'canvas': blue_canvas,
                'ball': ball_id,
                'text': text_id,
                'x': x,
                'y': y,
                'selected': False
            }
        
        # 创建红球Canvas - 12列1行布局
        red_canvas = tk.Canvas(
            self.red_frame,
            bg='#f0f4f8',
            height=80,
            highlightthickness=0
        )
        red_canvas.pack(padx=15, pady=15, fill='x')
        
        # 计算红球位置并绘制
        red_start_x = 40
        red_start_y = 40
        
        for i, ball_num in enumerate(self.red_balls):
            x = red_start_x + i * spacing_x
            y = red_start_y
            
            # 绘制红球
            ball_id = red_canvas.create_oval(
                x - ball_size//2, y - ball_size//2,
                x + ball_size//2, y + ball_size//2,
                fill='#dc2626',
                outline='#b91c1c',
                width=2,
                tags=f'red_{ball_num}'
            )
            
            # 绘制球号
            text_id = red_canvas.create_text(
                x, y,
                text=str(ball_num),
                fill='white',
                font=('Arial', 10, 'bold'),
                tags=f'red_{ball_num}_text'
            )
            
            # 存储红球对象信息
            self.red_ball_objects[ball_num] = {
                'canvas': red_canvas,
                'ball': ball_id,
                'text': text_id,
                'x': x,
                'y': y,
                'selected': False
            }
    
    def init_particles(self):
        """初始化粒子系统"""
        # 创建飘落的粒子
        colors = ['#fbbf24', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ef4444']
        shapes = ['●', '◆', '▲', '★']
        
        for i in range(12):
            particle = {
                'x': random.randint(10, 190),
                'y': random.randint(-50, 120),
                'speed': random.uniform(0.5, 2),
                'color': random.choice(colors),
                'shape': random.choice(shapes),
                'size': random.randint(8, 14),
                'swing': random.uniform(0, math.pi * 2),
                'swing_speed': random.uniform(0.05, 0.15)
            }
            self.left_particles.append(particle)
    
    def start_decoration_animations(self):
        """启动装饰动画"""
        self.animate_left_decoration()
        self.animate_right_decoration()
    
    def animate_left_decoration(self):
        """左上角粒子飘落动画"""
        self.left_decoration.delete("all")
        
        # 标题
        self.left_decoration.create_text(
            100, 15,
            text="🎊 幸运飘落",
            font=('微软雅黑', 11, 'bold'),
            fill='#6366f1'
        )
        
        # 更新和绘制每个粒子
        for particle in self.left_particles:
            # 更新位置
            particle['y'] += particle['speed']
            particle['swing'] += particle['swing_speed']
            swing_offset = 15 * math.sin(particle['swing'])
            
            # 绘制粒子
            self.left_decoration.create_text(
                particle['x'] + swing_offset, particle['y'],
                text=particle['shape'],
                font=('Arial', particle['size']),
                fill=particle['color']
            )
            
            # 重置超出屏幕的粒子
            if particle['y'] > 130:
                particle['y'] = random.randint(-30, -10)
                particle['x'] = random.randint(10, 190)
                particle['speed'] = random.uniform(0.5, 2)
        
        self.animation_frame += 1
        
        # 继续动画
        timer = Timer(0.08, self.animate_left_decoration)
        self.decoration_timers.append(timer)
        timer.start()
    
    def animate_right_decoration(self):
        """右上角彩虹波纹动画"""
        self.right_decoration.delete("all")
        
        # 标题
        self.right_decoration.create_text(
            100, 15,
            text="🌈 彩虹波纹",
            font=('微软雅黑', 11, 'bold'),
            fill='#db2777'
        )
        
        center_x, center_y = 100, 70
        
        # 绘制多层波纹
        colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899']
        
        for i in range(6):
            radius = 15 + i * 8 + 10 * math.sin(self.right_wave_angle + i * 0.5)
            color = colors[i % len(colors)]
            
            # 波纹圆环
            self.right_decoration.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=2, fill=''
            )
        
        # 中心闪烁点
        center_size = 3 + 2 * math.sin(self.right_wave_angle * 2)
        self.right_decoration.create_oval(
            center_x - center_size, center_y - center_size,
            center_x + center_size, center_y + center_size,
            fill='#fbbf24', outline='#f59e0b', width=1
        )
        
        # 旋转的小星星
        for i in range(4):
            angle = self.right_wave_angle * 1.5 + i * math.pi / 2
            star_x = center_x + 35 * math.cos(angle)
            star_y = center_y + 35 * math.sin(angle)
            
            self.right_decoration.create_text(
                star_x, star_y,
                text="✨",
                font=('Arial', 12),
                fill=colors[i % len(colors)]
            )
        
        self.right_wave_angle += 0.15
        
        # 继续动画
        timer = Timer(0.06, self.animate_right_decoration)
        self.decoration_timers.append(timer)
        timer.start()
    
    def start_selection_animation(self):
        """开始选号动画"""
        if self.is_selecting:
            return
            
        self.clear_selection()
        self.is_selecting = True
        self.btn_select.configure(state='disabled', text='⏳ 选号中...')
        
        # 随机选择球号
        selected_blue = random.sample(self.blue_balls, 5)
        selected_red = random.sample(self.red_balls, 2)
        
        # 创建选择队列（蓝球+红球）
        self.selection_queue = [(num, 'blue') for num in selected_blue] + [(num, 'red') for num in selected_red]
        random.shuffle(self.selection_queue)  # 打乱选择顺序
        
        # 开始逐个选择动画
        self.result_var.set('🎬 动画选号开始！正在选择第1个球...')
        self.animate_next_ball(0)
    
    def animate_next_ball(self, index):
        """动画选择下一个球"""
        if index >= len(self.selection_queue):
            # 所有球都选完了
            self.finish_selection()
            return
        
        ball_num, color = self.selection_queue[index]
        
        # 更新状态提示
        self.result_var.set(f'🎬 正在选择第{index + 1}个球：{color}球{ball_num}号')
        
        # 执行选择动画
        self.select_ball_with_animation(ball_num, color)
        
        # 2秒后选择下一个球
        Timer(2.0, lambda: self.animate_next_ball(index + 1)).start()
    
    def select_ball_with_animation(self, ball_num, color):
        """为单个球添加选中动画效果"""
        if color == 'blue':
            ball_obj = self.blue_ball_objects[ball_num]
            self.selected_blue.append(ball_num)
        else:
            ball_obj = self.red_ball_objects[ball_num]
            self.selected_red.append(ball_num)
        
        ball_obj['selected'] = True
        canvas = ball_obj['canvas']
        ball_id = ball_obj['ball']
        text_id = ball_obj['text']
        
        # 播放提示音
        self.root.bell()
        
        # 显示小弹出球
        self.show_popup_ball(ball_num, color)
        
        # 改变原球的颜色为金黄色
        canvas.itemconfig(ball_id, fill='#fbbf24', outline='#f59e0b', width=3)
        canvas.itemconfig(text_id, fill='#1f2937')
        
        # 添加选中标记
        canvas.itemconfig(text_id, text=f"✓{ball_num}")
    
    def show_popup_ball(self, ball_num, color):
        """显示小弹出球（10像素半径）"""
        # 计算弹出位置（屏幕中央偏右）
        popup_x = 420  # 窗口中央偏右
        popup_y = 300  # 窗口中央
        
        # 显示弹出框架
        self.popup_frame.place(x=popup_x, y=popup_y, width=60, height=60)
        self.popup_canvas.delete("all")
        
        # 确定球的颜色
        if color == 'blue':
            ball_color = '#2563eb'
            outline_color = '#1d4ed8'
        else:
            ball_color = '#dc2626'
            outline_color = '#b91c1c'
        
        # 执行小弹出动画（10像素半径）
        self.animate_popup_ball(30, 30, 10, ball_color, outline_color, ball_num)

    def animate_popup_ball(self, center_x, center_y, max_radius, ball_color, outline_color, ball_num):
        """小球弹出动画"""
        duration = 1.5  # 动画持续时间
        steps = 20      # 动画步数
        
        def animate_step(step):
            if step > steps:
                # 动画结束，隐藏弹出层
                Timer(0.3, lambda: self.popup_frame.place_forget()).start()
                return
            
            # 清除上一帧
            self.popup_canvas.delete("ball")
            
            # 计算当前大小（弹性效果）
            progress = step / steps
            
            # 使用弹性函数
            if progress < 0.5:
                # 快速放大阶段
                scale = (progress / 0.5) * 1.5
            else:
                # 回弹阶段
                bounce_progress = (progress - 0.5) / 0.5
                scale = 1.5 - 0.5 * bounce_progress
            
            current_radius = max_radius * scale
            
            # 绘制球体主体
            self.popup_canvas.create_oval(
                center_x - current_radius, center_y - current_radius,
                center_x + current_radius, center_y + current_radius,
                fill=ball_color,
                outline=outline_color,
                width=2,
                tags="ball"
            )
            
            # 添加小光泽效果
            if current_radius > 3:
                highlight_radius = current_radius * 0.3
                highlight_x = center_x - current_radius * 0.3
                highlight_y = center_y - current_radius * 0.3
                
                self.popup_canvas.create_oval(
                    highlight_x - highlight_radius, highlight_y - highlight_radius,
                    highlight_x + highlight_radius, highlight_y + highlight_radius,
                    fill='white',
                    outline='',
                    tags="ball"
                )
            
            # 绘制球号
            font_size = max(8, int(current_radius * 0.8))
            self.popup_canvas.create_text(
                center_x, center_y,
                text=str(ball_num),
                fill='white',
                font=('Arial', font_size, 'bold'),
                tags="ball"
            )
            
            # 继续下一帧
            Timer(duration/steps, lambda: animate_step(step + 1)).start()
        
        # 开始动画
        animate_step(0)

    def finish_selection(self):
        """完成选择"""
        self.is_selecting = False
        self.btn_select.configure(state='normal', text='🎯 开始动画选号')
        
        # 更新显示结果
        blue_nums = sorted(self.selected_blue)
        red_nums = sorted(self.selected_red)
        
        blue_str = " ".join([f"{num:02d}" for num in blue_nums])
        red_str = " ".join([f"{num:02d}" for num in red_nums])
        
        result_text = f"🎊 选号完成！🔵 蓝球 [{blue_str}]  🔴 红球 [{red_str}]  🎊 共7个球"
        self.result_var.set(result_text)
        
        # 更新标题框显示选中数量
        self.blue_frame.configure(text=f"🔵 蓝球池 (已选{len(self.selected_blue)}个)")
        self.red_frame.configure(text=f"🔴 红球池 (已选{len(self.selected_red)}个)")
        
        # 播放完成提示音
        for i in range(3):
            Timer(i * 0.2, lambda: self.root.bell()).start()
    
    def clear_selection(self):
        """清空选择，恢复球的原始状态"""
        # 停止当前动画
        self.is_selecting = False
        self.selection_queue = []
        
        # 隐藏弹出层
        self.popup_frame.place_forget()
        
        # 恢复所有蓝球
        for ball_num, ball_obj in self.blue_ball_objects.items():
            canvas = ball_obj['canvas']
            ball_id = ball_obj['ball']
            text_id = ball_obj['text']
            
            # 恢复颜色和文字
            canvas.itemconfig(ball_id, fill='#2563eb', outline='#1d4ed8', width=2)
            canvas.itemconfig(text_id, fill='white', text=str(ball_num))
            ball_obj['selected'] = False
        
        # 恢复所有红球
        for ball_num, ball_obj in self.red_ball_objects.items():
            canvas = ball_obj['canvas']
            ball_id = ball_obj['ball']
            text_id = ball_obj['text']
            
            # 恢复颜色和文字
            canvas.itemconfig(ball_id, fill='#dc2626', outline='#b91c1c', width=2)
            canvas.itemconfig(text_id, fill='white', text=str(ball_num))
            ball_obj['selected'] = False
        
        # 重置选择状态
        self.selected_blue = []
        self.selected_red = []
        
        # 重置按钮和显示
        self.btn_select.configure(state='normal', text='🎯 开始动画选号')
        self.result_var.set('点击"开始动画选号"按钮进行选择')
        self.blue_frame.configure(text="🔵 蓝球池 (选5个)")
        self.red_frame.configure(text="🔴 红球池 (选2个)")
    
    def __del__(self):
        """清理定时器"""
        for timer in self.decoration_timers:
            if timer.is_alive():
                timer.cancel()

def main():
    # 创建主窗口
    root = tk.Tk()
    
    # 创建应用程序
    app = AnimatedBallSelector(root)
    
    # 窗口居中显示
    root.update_idletasks()
    width = 900
    height = 650
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # 启动程序
    root.mainloop()

if __name__ == "__main__":
    main()
