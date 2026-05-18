"""
app.py
Flask 后端：读取 user_behavior.csv，提供漏斗数据 JSON 接口和前端页面。
路由:
  GET '/'           → 返回 templates/index.html（ECharts 漏斗图）
  GET '/funnel_data' → 返回漏斗阶段用户数 JSON
"""

import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)

CSV_FILE = 'user_behavior.csv'


@app.route('/')
def index():
    """返回前端漏斗图页面"""
    return render_template('index.html')


@app.route('/funnel_data')
def funnel_data():
    """
    返回漏斗数据 JSON
    格式: {
        "stages": ["浏览", "加购", "购买"],
        "counts": [800, 320, 192],
        "rates": {
            "view_to_cart": 40.0,
            "cart_to_purchase": 60.0,
            "overall": 24.0
        }
    }
    """
    df = pd.read_csv(CSV_FILE)

    # 各阶段独立用户数（去重）
    view_users = set(df[df['action'] == 'view']['user_id'].unique())
    cart_users = set(df[df['action'] == 'add_to_cart']['user_id'].unique())
    purchase_users = set(df[df['action'] == 'purchase']['user_id'].unique())

    view_count = len(view_users)
    cart_count = len(cart_users)
    purchase_count = len(purchase_users)

    # 转化率
    rates = {
        'view_to_cart': round(cart_count / view_count * 100, 1) if view_count > 0 else 0,
        'cart_to_purchase': round(purchase_count / cart_count * 100, 1) if cart_count > 0 else 0,
        'overall': round(purchase_count / view_count * 100, 1) if view_count > 0 else 0
    }

    return jsonify({
        'funnel': [
            {'stage': '浏览', 'count': view_count},
            {'stage': '加购', 'count': cart_count},
            {'stage': '购买', 'count': purchase_count}
        ],
        'rates': rates
    })


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
