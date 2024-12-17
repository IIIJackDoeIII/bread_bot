from database.models import Session, User, CartItem

# Добавление товара в корзину
def add_to_cart(telegram_id, bread_type):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    print(f"Found User: {user}")
    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()

    cart_item = session.query(CartItem).filter_by(user_id=user.id, bread_type=bread_type).first()
    if cart_item:
        cart_item.quantity += 1
        print(f"Quantity updated: {cart_item.bread_type}, {cart_item.quantity}")
    else:
        cart_item = CartItem(user_id=user.id, bread_type=bread_type, quantity=1)
        session.add(cart_item)
        print(f"New item added to cart: {cart_item.bread_type}")

    session.commit()
    session.close()
    print(f"Item {bread_type} added to cart for user {telegram_id}.")

# Получение корзины пользователя
def get_cart(telegram_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if not user:
        session.close()
        return []  # Возвращаем пустой список, если пользователь не найден

    # Получаем все записи из корзины, связанные с этим пользователем
    cart_items = session.query(CartItem).filter_by(user_id=user.id).all()
    session.close()
    print(f"Cart items fetched: {cart_items}")
    return cart_items


# Очистка корзины
def clear_cart(telegram_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        session.query(CartItem).filter_by(user_id=user.id).delete()
        session.commit()

    session.close()
