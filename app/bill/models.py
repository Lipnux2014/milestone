from app import db


class BillBook(db.Model):

    __tablename__ = "bill_book"

    id = db.Column("id", db.Integer, primary_key=True)
    bill_keeper = db.Column("bill_keeper", db.String(255))
    bill_amount = db.Column("bill_amount", db.Float)
    bill_description = db.Column("bill_description", db.String(255))
    is_valid = db.Column("is_valid", db.Integer)
    created_time = db.Column("created_time", db.DateTime())
    updated_time = db.Column("updated_time", db.DateTime())

    def __init__(self, bill_keeper, bill_amount, bill_description, is_valid, create_time, updated_time):
        self.bill_keeper = bill_keeper
        self.bill_amount = bill_amount
        self.bill_description = bill_description
        self.is_valid = is_valid
        self.created_time = create_time
        self.updated_time = updated_time
