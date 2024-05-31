from wtforms import Form, DateField, SelectField
from wtforms.validators import InputRequired
from project.db import Naprawa, Przeglad
from datetime import date


class ReportForm(Form):
    type = SelectField(
        "Rodzaj raportu", validators=[InputRequired()], choices=["Naprawy", "Przeglądy"]
    )
    date_start = DateField("Od", validators=[InputRequired()])
    date_end = DateField("Do", validators=[InputRequired()])
