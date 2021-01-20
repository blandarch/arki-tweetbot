from configs import db

class Store_Word(db.Model):
    __tablename__ = 'words'
    print(__tablename__)
    word_id = db.Column(db.Integer, primary_key=True)
    print(word_id)
    every_word = db.Column(db.String(32), index=True)
    print(every_word)

