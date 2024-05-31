from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    IntegerField,
    TextAreaField,
    DateField,
    DecimalField,
    EmailField,
)
from wtforms.validators import NumberRange, InputRequired, Length, Optional
from project.db import (
    db,
    Rola,
    Uzytkownik,
    ZgloszenieNaprawy,
    Przeglad,
    PowodNaprawy,
    ElementInfrastruktury,
    Serwisant,
)
from re import fullmatch


class ServiceForm(Form):
    name = TextAreaField(
        "Nazwa",
        validators=[
            Length(min=0, max=128, message="Nazwa może mieć maksymalnie 128 znaków"),
            InputRequired(),
        ],
    )

    phone_number = TextAreaField(
        "Nr telefonu",
        validators=[
            Length(
                min=9, max=32, message="Nr telefonu musi mieć przynajmniej 9 znaków."
            ),
            InputRequired(),
        ],
    )
    mail = EmailField(
        "Adres e-mail",
        validators=[
            Length(min=0, max=128, message="E-mail może mieć maksymalnie 128 znaków"),
            InputRequired(),
        ],
    )
    __phone_number_regex = r"(?:([+]\d{1,4})[-.\s]?)?(?:[(](\d{1,3})[)][-.\s]?)?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})"

    def validate_phone_number(form, self):
        if fullmatch(form.__phone_number_regex, self.data):
            return True
        self.errors.append("Zły format nr. telefonu.")
        return False
