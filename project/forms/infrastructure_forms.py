from wtforms import Form, TextAreaField, FloatField, StringField, IntegerField, BooleanField, validators, \
    ValidationError

from project.db import db, Lokalizacja, TypInfrastruktury, Obiekt, StatusElementu


class LocationForm(Form):
    szerokosc_geo = FloatField("Szerokość geograficzna", validators=[validators.InputRequired()])
    dlugosc_geo = FloatField("Długość geograficzna", validators=[validators.InputRequired()])
    nazwa_miejsca = StringField("Nazwa miejsca", validators=[validators.Optional(), validators.Length(max=32)])

    def validate_szerokosc_geo(form, field):
        if field.data is not None and not (-90 <= field.data <= 90):
            raise ValidationError("Szerokość geograficzna musi być w zakresie -90 do 90 stopni.")

    def validate_dlugosc_geo(form, field):
        if field.data is not None and not (-180 <= field.data <= 180):
            raise ValidationError("Długość geograficzna musi być w zakresie -180 do 180 stopni.")


class ObjectForm(Form):
    typ = StringField("Typ", validators=[validators.InputRequired(), validators.Length(max=32)])
    do_uzytku = BooleanField("Do użytku")


class TypeForm(Form):
    typ = StringField("Typ", validators=[validators.InputRequired(), validators.Length(max=32)])


class StatusForm(Form):
    status = StringField("Status", validators=[validators.InputRequired(), validators.Length(max=32)])


class ElementForm(Form):
    typ = IntegerField("Id typu", validators=[validators.InputRequired()])
    lokalizacja = IntegerField("Id lokalizacji", validators=[validators.InputRequired()])
    obiekt = IntegerField("Id obiektu", validators=[validators.InputRequired()])
    status = IntegerField("Id statusu", validators=[validators.InputRequired()])
    max_interwal = IntegerField("Maksymalny interwał",
                                validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    opis = TextAreaField("Opis",
                         validators=[
                             validators.Length(min=0, max=1024, message="Opis może zawierać maksymalnie 1024 znaków"),
                             validators.Optional()])

    def validate_lokalizacja(form, self):
        print("validating")
        if not db.session.query(Lokalizacja).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje lokalizacja o podanym id")
            return False
        else:
            return True

    def validate_typ(form, self):
        if not db.session.query(TypInfrastruktury).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje typ infrastruktury o podanym id")
            return False
        else:
            return True

    def validate_obiekt(form, self):
        if not db.session.query(Obiekt).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje obiekt o podanym id")
            return False
        else:
            return True

    def validate_status(form, self):
        if not db.session.query(StatusElementu).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje status o podanym id")
            return False
        else:
            return True

