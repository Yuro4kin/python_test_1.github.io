# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# БД -- Таблицы -- Записи
# Таблица
# id    title   price   isActive
# 1     Some    100     True
# 2     Some2   200     False
# 3     Some3   40      True

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def catalog():
    items = Item.query.order_by(Item.price).all()
    return render_template('catalog.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item =Item.query.get(id)

    api = Api(merchant_id=1396424,
          secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:

        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
