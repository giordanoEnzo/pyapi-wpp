from utils.db import db


class Hico(db.Model):
    __tablename__ = 'hico'
    id = db.Column(db.Integer, primary_key=True)
    HICONOME = db.Column(db.String)
    HICOFONE = db.Column(db.String)
    HICOMAIL = db.Column(db.String)
    HICOCLIE = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, HICONOME, HICOFONE, HICOMAIL, HICOCLIE):
        self.HICONOME = HICONOME
        self.HICOFONE = HICOFONE
        self.HICOMAIL = HICOMAIL
        self.HICOCLIE = HICOCLIE

    def gravar_registro(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def listar_registros(self):
        return Hico.query.all()

    @classmethod
    def pesquisar_registro(self, telefone):
        return Hico.query.filter_by(HICOFONE=telefone).first()

