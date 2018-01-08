from app import db


class BillBook(db.Model):

    __tablename__ = "bill_book"

    id = db.column(db.Integer, primary_key=True)
    bill_keeper = db.column(db.String(255))
    bill_amount = db.column(db.Float)
    bill_description = db.column(db.String(255))
    is_valid = db.column(db.Integer(255))
    create_time = db.column(db.DateTime())
    updated_time = db.column(db.DateTime())

    def __init__(self, bill_keeper, bill_amount, bill_description, is_valid, create_time, updated_time):
        self.bill_keeper = bill_keeper
        self.bill_amount = bill_amount
        self.bill_description = bill_description
        self.is_valid = is_valid
        self.create_time = create_time
        self.updated_time = updated_time
