from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import random  

app = Flask(__name__)

current_order = []

now = datetime.now()
current_order = [
    {'order_id': random.randint(1, 1000), 'name': '오늘 상품', 'price': 1000, 'image': '/static/today.jpg', 'date': f"{now.month}/{now.day}", 'is_reviewed': False, 'review_content': None, 'review_rating': None},
    {'order_id': random.randint(1, 1000), 'name': '1개월 전 상품', 'price': 2000, 'image': '/static/month.jpg', 'date': f"{(now - timedelta(days=20)).month}/{(now - timedelta(days=20)).day}", 'is_reviewed': False, 'review_content': None, 'review_rating': None},
    {'order_id': random.randint(1, 1000), 'name': '3개월 전 상품', 'price': 3000, 'image': '/static/3month.jpg', 'date': f"{(now - timedelta(days=60)).month}/{(now - timedelta(days=60)).day}", 'is_reviewed': True, 'review_content': '괜찮았어요', 'review_rating': 3},
    {'order_id': random.randint(1, 1000), 'name': '6개월 전 상품', 'price': 4000, 'image': '/static/6month.jpg', 'date': f"{(now - timedelta(days=150)).month}/{(now - timedelta(days=150)).day}", 'is_reviewed': False, 'review_content': None, 'review_rating': None},
    {'order_id': random.randint(1, 1000), 'name': '7개월 전 상품', 'price': 5000, 'image': '/static/old.jpg', 'date': f"{(now - timedelta(days=210)).month}/{(now - timedelta(days=210)).day}", 'is_reviewed': True, 'review_content': '별로였습니다.', 'review_rating': 1},
]

@app.route('/')
def order_history():
    return render_template('주문내역.html', current_order=current_order)

@app.route('/order_food')
def order_food_page():
    return render_template('주문내역실험.html')

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    data = request.get_json()
    if data and 'name' in data and 'price' in data and 'image' in data:
        now = datetime.now()
        formatted_date = f"{now.month}/{now.day}"
        data['date'] = formatted_date
        data['order_id'] = random.randint(1, 1000)
        data['is_reviewed'] = False
        data['review_content'] = None
        data['review_rating'] = None
        current_order.append(data)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid order data'}), 400

@app.route('/filter_orders', methods=['POST'])
def filter_orders():
    data = request.get_json()
    period = data.get('period')
    filtered_orders = []
    now = datetime.now()

    for order in current_order:
        order_date_str = order.get('date')
        if order_date_str:
            try:
                order_month, order_day = map(int, order_date_str.split('/'))
                order_datetime = datetime(now.year, order_month, order_day)

                if period == '전체':
                    filtered_orders.append(order)
                elif period == '1개월':
                    if now - timedelta(days=30) <= order_datetime <= now:
                        filtered_orders.append(order)
                elif period == '3개월':
                    if now - timedelta(days=90) <= order_datetime <= now:
                        filtered_orders.append(order)
                elif period == '6개월':
                    if now - timedelta(days=180) <= order_datetime <= now:
                        filtered_orders.append(order)
            except ValueError:
                print(f"날짜 형식 오류: {order_date_str}")

    return jsonify({'filtered_orders': filtered_orders})



@app.route('/review_write')
def review_write():
    order_id = request.args.get('order_id')
    order = next((item for item in current_order if str(item['order_id']) == order_id), None)
    return render_template('order_write.html', order=order)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    order_id = request.form.get('order_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    for order in current_order:
        if str(order['order_id']) == order_id:
            order['is_reviewed'] = True
            order['review_content'] = comment
            order['review_rating'] = int(rating)
            break
    return "리뷰가 성공적으로 제출되었습니다!"


@app.route('/filter_reviews', methods=['POST'])
def filter_reviews():
    data = request.get_json()
    status = data.get('status') 
    filtered_reviews = []
    if status == '작성 가능':
        filtered_reviews = [order for order in current_order if not order.get('is_reviewed')]
    elif status == '작성 완료':
        filtered_reviews = [order for order in current_order if order.get('is_reviewed')]
    return jsonify({'reviews': filtered_reviews})



if __name__ == '__main__':
    app.run(debug=True)