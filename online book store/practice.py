import streamlit as st
from order_lists import add_book_order, add_payment, view_order_list, delete_book_order, get_total

st.title("📚 Online Book Store")

# Customer info
name = st.text_input("Enter your name")
contact = st.text_input("Enter your contact number")
address = st.text_area("Enter your address")

if st.button("Save Customer Info"):
    with open("data.txt", "a") as file:
        file.write(f"Customer Name: {name}\n")
        file.write(f"Contact: {contact}\n")
        file.write(f"Address: {address}\n")
        file.write("Orders:\n")
    st.success("Customer info saved!")

# Book sections
section = st.selectbox("Choose a section", [
    "Schools Books Section",
    "Poetry Section",
    "Novels",
    "View Ordered Books",
    "Delete Order",
    "Exit"
])

if section == "Schools Books Section":
    book_choice = st.radio("Select a book pack", [
        "Class 9th Book Pack (5000 PKR)",
        "Class 10th Book Pack (5500 PKR)"
    ])
    if st.button("Order"):
        if "9th" in book_choice:
            payment = 5000
        else:
            payment = 5500
        add_book_order(book_choice)
        add_payment(payment)
        with open("data.txt", "a") as file:
            file.write(f"Order: {book_choice}, Payment: {payment}\n")
        st.success(f"Ordered {book_choice}!")

elif section == "Poetry Section":   # ✅ Match exact string
    book_choice = st.radio("Select a book pack", [
        "POETRY BOOKS PACK OF 5 (ALLAMA IQBAL)",
        "POETRY BOOKS PACK OF 5 (WILLIAM SHAKESPEARE)"
    ])
    if st.button("Order"):
        payment = 5500
        add_book_order(book_choice)
        add_payment(payment)
        with open("data.txt", "a") as file:
            file.write(f"Order: {book_choice}, Payment: {payment}\n")
        st.success(f"Ordered {book_choice}!")

elif section == "Novels":   # ✅ Match exact string
    book_choice = st.radio("Select a book pack", [
        "AB-E-HAYAT BY NIMRA AHMED",
        "PEER-E-KAMIL BY NIMRA AHMED",
        "AMAR BAIL BY NIMRA AHMED",
        "HASIL BY UMERA AHMED",
        "LA-HASIL BY UMERA AHMED"
    ])
    if st.button("Order"):
        payment = 5500
        add_book_order(book_choice)
        add_payment(payment)
        with open("data.txt", "a") as file:
            file.write(f"Order: {book_choice}, Payment: {payment}\n")
        st.success(f"Ordered {book_choice}!")


elif section == "View Ordered Books":
    view_order_list()

elif section == "Delete Order":
    order_no = st.number_input("Enter order number to discard", min_value=1)
    if st.button("Delete"):
        delete_book_order(order_no)
        st.success(f"Deleted order {order_no}")

elif section == "Exit":
    total = get_total()
    st.info(f"Your total amount to pay is {total} PKR. You can JazzCash or EasyPaisa on phone no# 3702139375")
    with open("data.txt", "a") as file:
        file.write(f"Total Payment: {total} PKR\n")
        
        file.write("----- End of Order -----\n\n")
