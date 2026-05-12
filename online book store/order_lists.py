order_list = [] 
payment_list = []

def add_book_order(book_order): 
    order_list.append(book_order) 
    save_orders()

def add_payment(payment): 
    payment_list.append(payment)

def save_orders():
    with open("data.txt", "a") as file:
        for item in order_list:
            file.write(f"{item}\n")

def view_order_list(): 
    for i, book_order in enumerate(order_list, 1): 
        print(f'{i}. {book_order}') 
         
def delete_book_order(book_order_number): 
    if 0 < book_order_number <= len(order_list): 
        order_list.pop(book_order_number - 1)

def get_total():
    return sum(payment_list)
