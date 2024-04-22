from utils.db import db


class Hist(db.Model):
    __tablename__ = 'hist'
    id = db.Column(db.Integer, primary_key=True)
    HISTFONE = db.Column(db.String)
    HISTSTAT = db.Column(db.String)
    HISTTIME = db.Column(db.String)

    def __init__(self, HISTFONE, HISTSTAT, HISTTIME):
        self.HISTFONE = HISTFONE
        self.HISTSTAT = HISTSTAT
        self.HISTTIME = HISTTIME

    def gravar_status(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def deletar_status(self):
        db.session.delete()
        db.session.commit()

    @classmethod
    def pesquisar_status(self, telefone):
        return Hist.query.filter_by(HISTFONE=telefone).first()