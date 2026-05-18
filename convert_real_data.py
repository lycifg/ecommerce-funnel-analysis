"""
真实数据转换脚本
功能：将不同来源的电商数据（淘宝、抖店、RetailRocket等）转换为项目所需的 user_behavior.csv
格式：user_id, action, product_id, timestamp
运行：python convert_real_data.py
"""

import pandas as pd

# ========== 配置区域（根据你的数据源修改） ==========
# 选择数据源类型: 'taobao', 'doudian', 'retailrocket', 'custom'
SOURCE_TYPE = 'taobao'   # 改成你实际的数据源

# 文件路径（原始数据文件）
INPUT_FILE = 'UserBehavior.csv'        # 淘宝数据集文件名
# INPUT_FILE = '抖店订单.xlsx'          # 抖店导出文件（支持Excel/CSV）
# INPUT_FILE = 'retailrocket.csv'       # RetailRocket数据集

# 可选：如果原始文件很大，只读取前 N 行（0 表示全部读取）
SAMPLE_ROWS = 100000    # 建议先 10 万行测试，成功后再改为 0 全量

# ========== 各数据源转换逻辑 ==========

def convert_taobao():
    """淘宝天池数据集 UserBehavior.csv 转换"""
    print("正在读取淘宝数据...")
    df = pd.read_csv(INPUT_FILE, header=None,
                     names=['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp'],
                     nrows=SAMPLE_ROWS if SAMPLE_ROWS > 0 else None)
    print(f"原始行数: {len(df)}")
    print(f"behavior_type 唯一值: {df['behavior_type'].unique()}")

    df = df.rename(columns={'item_id': 'product_id'})

    # 行为类型映射：字符串 -> 标准 action
    action_map = {
        'pv': 'view',
        'cart': 'add_to_cart',
        'buy': 'purchase'
    }
    # 过滤出需要的行为（丢弃 'fav' 及其他未知）
    df = df[df['behavior_type'].isin(action_map.keys())]
    print(f"过滤后行数: {len(df)}")
    if len(df) == 0:
        print("警告：未找到 'pv', 'cart', 'buy' 行为，请检查数据格式。")
        return pd.DataFrame(columns=['user_id', 'action', 'product_id', 'timestamp'])

    df['action'] = df['behavior_type'].map(action_map)
    df_out = df[['user_id', 'action', 'product_id', 'timestamp']]
    return df_out

def convert_doudian():
    """抖店导出订单/行为数据转换（示例）"""
    # 根据你导出的文件类型选择读取方式
    if INPUT_FILE.endswith('.xlsx'):
        df = pd.read_excel(INPUT_FILE)
    else:
        df = pd.read_csv(INPUT_FILE)
    
    # 列名映射（根据你实际导出列名修改）
    df = df.rename(columns={
        '买家昵称': 'user_id',
        '商品ID': 'product_id',
        '订单状态': 'action',
        '下单时间': 'timestamp'
    })
    
    # 行为映射（根据实际状态值修改）
    action_map = {
        '已付款': 'purchase',
        '加入购物车': 'add_to_cart',
        '浏览商品': 'view'
    }
    df['action'] = df['action'].map(action_map)
    
    # 删除未映射的行
    df = df.dropna(subset=['action'])
    
    df = df[['user_id', 'action', 'product_id', 'timestamp']]
    return df

def convert_retailrocket():
    """RetailRocket 数据集转换"""
    # RetailRocket 通常包含三列: visitorid, event, itemid, timestamp
    # 注意：它的 event 已经是 view/addtocart/transaction
    df = pd.read_csv(INPUT_FILE, nrows=SAMPLE_ROWS if SAMPLE_ROWS > 0 else None)
    df = df.rename(columns={'visitorid': 'user_id', 'itemid': 'product_id', 'event': 'action'})
    # 将 transaction 统一为 purchase
    df['action'] = df['action'].replace('transaction', 'purchase')
    df = df[['user_id', 'action', 'product_id', 'timestamp']]
    return df

def convert_custom():
    """自定义数据源：用户自己提供 CSV，列名任意"""
    # 假设你有一个 CSV 文件，列名可能是 '用户ID', '行为', '商品编码', '时间'
    # 你需要根据实际列名修改下面的映射
    df = pd.read_csv(INPUT_FILE, nrows=SAMPLE_ROWS if SAMPLE_ROWS > 0 else None)
    df = df.rename(columns={
        '用户ID': 'user_id',
        '行为': 'action',
        '商品编码': 'product_id',
        '时间': 'timestamp'
    })
    # 如果 action 是中文，映射成英文
    action_map = {
        '浏览': 'view',
        '加购': 'add_to_cart',
        '购买': 'purchase'
    }
    df['action'] = df['action'].map(action_map)
    df = df.dropna(subset=['action'])
    df = df[['user_id', 'action', 'product_id', 'timestamp']]
    return df

# ========== 主流程 ==========
if __name__ == '__main__':
    # 根据配置选择转换函数
    if SOURCE_TYPE == 'taobao':
        df_out = convert_taobao()
    elif SOURCE_TYPE == 'doudian':
        df_out = convert_doudian()
    elif SOURCE_TYPE == 'retailrocket':
        df_out = convert_retailrocket()
    elif SOURCE_TYPE == 'custom':
        df_out = convert_custom()
    else:
        raise ValueError("SOURCE_TYPE 只能是 taobao, doudian, retailrocket, custom 之一")
    
    # 保存为 user_behavior.csv
    df_out.to_csv('user_behavior.csv', index=False, encoding='utf-8-sig')
    print(f"转换完成！共 {len(df_out)} 条记录，已保存为 user_behavior.csv")
    print("现在可以运行 python app.py 查看真实数据的漏斗图了。")