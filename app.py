from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    name = db.Column(db.String(100))
    price = db.Column(db.String(20))
    img = db.Column(db.String(200))
    student_id = db.Column(db.String(30))
    category = db.Column(db.String(30))
    description = db.Column(db.String(300))
    sold = db.Column(db.Boolean, default=False)
    time = db.Column(db.String(30))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    sell_count = sum(1 for i in items if i.type == "sell" and not i.sold)
    buy_count = sum(1 for i in items if i.type == "buy")
    sold_count = sum(1 for i in items if i.sold)
    return render_template('index.html', items=items,
                           sell_count=sell_count,
                           buy_count=buy_count,
                           sold_count=sold_count)

@app.route('/add_sell', methods=['POST'])
def add_sell():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()
    img = request.form.get('img', '').strip()
    student_id = request.form.get('student_id', '').strip()
    category = request.form.get('category', '其他').strip()
    description = request.form.get('description', '').strip()
    if not name or not price or not student_id:
        return redirect('/')
    item = Item(
        type="sell",
        name=name,
        price=price,
        img=img,
        student_id=student_id,
        category=category,
        description=description,
        sold=False,
        time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    db.session.add(item)
    db.session.commit()
    return redirect('/')

@app.route('/add_buy', methods=['POST'])
def add_buy():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()
    student_id = request.form.get('student_id', '').strip()
    description = request.form.get('description', '').strip()
    if not name or not price or not student_id:
        return redirect('/')
    item = Item(
        type="buy",
        name=name,
        price=price,
        student_id=student_id,
        description=description,
        time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    db.session.add(item)
    db.session.commit()
    return redirect('/')

@app.route('/sold/<int:index>')
def sold(index):
    item = Item.query.get(index)
    if item and item.type == "sell":
        item.sold = True
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    item = Item.query.get(index)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)