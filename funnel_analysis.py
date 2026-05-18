"""
funnel_analysis.py
读取 user_behavior.csv，计算转化漏斗数据并打印结果。
可独立运行，不依赖 Flask。
"""

import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# ---- 读取数据 ----
INPUT_FILE = 'user_behavior.csv'

df = pd.read_csv(INPUT_FILE)

print("=" * 50)
print("📊 电商用户行为转化漏斗分析")
print("=" * 50)

# ---- 计算各阶段独立用户数 ----
# view：浏览过任意商品的用户
view_users = set(df[df['action'] == 'view']['user_id'].unique())
view_count = len(view_users)

# add_to_cart：加购过任意商品的用户
cart_users = set(df[df['action'] == 'add_to_cart']['user_id'].unique())
cart_count = len(cart_users)

# purchase：购买过任意商品的用户
purchase_users = set(df[df['action'] == 'purchase']['user_id'].unique())
purchase_count = len(purchase_users)

# ---- 计算转化率 ----
view_to_cart_rate = (cart_count / view_count * 100) if view_count > 0 else 0
cart_to_purchase_rate = (purchase_count / cart_count * 100) if cart_count > 0 else 0
overall_rate = (purchase_count / view_count * 100) if view_count > 0 else 0

# ---- 打印结果 ----
print(f"\n阶段               | 用户数")
print(f"-------------------|--------")
print(f"浏览 (view)        | {view_count:>6}")
print(f"加购 (add_to_cart) | {cart_count:>6}")
print(f"购买 (purchase)    | {purchase_count:>6}")

print(f"\n转化路径              | 转化率")
print(f"----------------------|--------")
print(f"浏览 → 加购           | {view_to_cart_rate:.2f}%")
print(f"加购 → 购买           | {cart_to_purchase_rate:.2f}%")
print(f"浏览 → 购买 (整体)     | {overall_rate:.2f}%")

print(f"\n共 {len(df)} 条行为记录")
print(f"总用户数：{df['user_id'].nunique()}")
