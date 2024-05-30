from wtforms import Form, StringField, PasswordField, IntegerField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Optional
from project.db import db, Rola, Uzytkownik


class UzytkownikForm(Form):
    rola_fk = IntegerField("Id roli", validators=[InputRequired()])
    imie = StringField("Imię", validators=[InputRequired(), Length(max=32)])
    nazwisko = StringField("Nazwisko", validators=[Optional(), Length(max=32)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=32)])
    password = PasswordField(
        "Hasło", validators=[InputRequired(), Length(min=8, max=128)]
    )
    numer_tel = StringField("Numer telefonu", validators=[Optional(), Length(max=32)])

    def validate_rola_fk(self, field):
        if not db.session.query(Rola).filter_by(id=field.data).first():
            raise ValidationError("Nie istnieje rola o podanym id")

    def validate_email(self, field):
        if db.session.query(Uzytkownik).filter_by(email=field.data).first():
            raise ValidationError("Email już istnieje w bazie danych")


class RolaForm(Form):
    rola = StringField("Rola", validators=[InputRequired(), Length(max=32)])

    def validate_rola(self, field):
        if db.session.query(Rola).filter_by(rola=field.data).first():
            raise ValidationError("Rola już istnieje w bazie danych")
