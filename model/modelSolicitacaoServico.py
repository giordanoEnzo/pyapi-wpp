from HareInteract.utils.db import db


class Hiss(db.Model):
    __tablename__ = 'hiss'
    id = db.Column(db.Integer, primary_key=True)
    HISSNOME = db.Column(db.String)
    HISSFONE = db.Column(db.String, unique=True, nullable=False)
    HISSERVI = db.Column(db.String)
    HISSOLUC = db.Column(db.String)
    HISSEGUR = db.Column(db.String)

    def __init__(self, HISSNOME, HISSFONE, HISSERVI, HISSOLUC, HISSEGUR):
        self.HISSNOME = HISSNOME
        self.HISSFONE = HISSFONE
        self.HISSERVI = HISSERVI
        self.HISSOLUC = HISSOLUC
        self.HISSEGUR = HISSEGUR

    def gravar_solicitacao(self):
        db.session.add(self)
        db.session.commit()

    def deletar_solicitacao(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def pesquisar_solicitacao(self, telefone):
        return Hiss.query.filter_by(HISSFONE=telefone).first()