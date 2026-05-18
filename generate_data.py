"""
generate_data.py
生成模拟电商用户行为数据，输出 user_behavior.csv
字段: user_id, action, product_id, timestamp
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# ---- 参数配置 ----
np.random.seed(42)          # 固定随机种子，保证每次运行结果一致
NUM_USERS = 1000            # 用户总数
NUM_PRODUCTS = 100          # 商品总数
DAYS = 30                   # 时间跨度（天）
OUTPUT_FILE = 'user_behavior.csv'

end_date = datetime.now()
start_date = end_date - timedelta(days=DAYS)

records = []

for user_id in range(1, NUM_USERS + 1):
    # 80% 的用户为活跃用户（至少有一次浏览）
    if np.random.random() > 0.2:
        num_viewed = np.random.randint(1, 6)  # 浏览 1-5 个商品
        viewed_products = np.random.choice(
            range(1, NUM_PRODUCTS + 1),
            size=num_viewed,
            replace=False
        )

        for product_id in viewed_products:
            # 生成浏览时间
            view_time = start_date + timedelta(
                days=np.random.randint(0, DAYS),
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            records.append({
                'user_id': user_id,
                'action': 'view',
                'product_id': int(product_id),
                'timestamp': view_time.strftime('%Y-%m-%d %H:%M:%S')
            })

            # 40% 概率加购
            if np.random.random() < 0.4:
                cart_time = view_time + timedelta(minutes=np.random.randint(1, 30))
                records.append({
                    'user_id': user_id,
                    'action': 'add_to_cart',
                    'product_id': int(product_id),
                    'timestamp': cart_time.strftime('%Y-%m-%d %H:%M:%S')
                })

                # 加购用户中 60% 概率购买
                if np.random.random() < 0.6:
                    purchase_time = cart_time + timedelta(minutes=np.random.randint(1, 120))
                    records.append({
                        'user_id': user_id,
                        'action': 'purchase',
                        'product_id': int(product_id),
                        'timestamp': purchase_time.strftime('%Y-%m-%d %H:%M:%S')
                    })

# 创建 DataFrame 并打乱顺序（模拟真实日志的时间交错）
df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# 保存 CSV
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')

# 输出统计摘要
print(f"✅ 数据已生成：{len(df)} 条记录 → {OUTPUT_FILE}")
print(f"   用户数：{df['user_id'].nunique()}")
print(f"   商品数：{df['product_id'].nunique()}")
print(f"   浏览记录：{(df['action'] == 'view').sum()}")
print(f"   加购记录：{(df['action'] == 'add_to_cart').sum()}")
print(f"   购买记录：{(df['action'] == 'purchase').sum()}")
