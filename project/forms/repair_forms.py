from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    IntegerField,
    TextAreaField,
    DateField,
    DecimalField,
    SelectField,
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
from datetime import date


class RepairReasonForm(Form):
    inspection_id = SelectField("Id przeglądu", validators=[Optional()])
    repair_need_report_id = SelectField(
        "Id zgłoszenia potrzeby naprawy", validators=[Optional()]
    )
    priority = IntegerField(
        "Priorytet",
        validators=[
            NumberRange(min=0, max=5, message="Priorytet musi być z zakresu <1,5>"),
            InputRequired(),
        ],
    )
    remarks = TextAreaField(
        "Uwagi",
        validators=[
            Length(
                min=0, max=1024, message="Uwagi mogą zawierać maksymalnie 1024 znaków"
            ),
            Optional(),
        ],
    )

    def validate_inspection_id(form, self):
        if self.data is not None:
            if not db.session.query(Przeglad).filter_by(id=self.data).first():
                self.errors.append("Nie istnieje przegląd o podanym id")
                return False
        return True

    def validate_repair_need_report_id(form, self):
        if self.data is not None:
            if not db.session.query(ZgloszenieNaprawy).filter_by(id=self.data).first():
                self.errors.append(
                    "Nie istnieje zgłoszenie potrzeby naprawy o podanym id"
                )
                return False
            if (
                db.session.query(PowodNaprawy)
                .filter_by(zgloszenie_id=self.data)
                .first()
            ):
                self.errors.append(
                    "Zgłoszenie potrzeby naprawy o podanym id zostało już przypisane do istniejącej naprawy"
                )
                return False
        return True

    def validate(self):
        super_succes = super().validate()
        success = True
        self.inspection_id.data = (
            None if self.inspection_id.data == "" else self.inspection_id.data
        )
        self.repair_need_report_id.data = (
            None
            if self.repair_need_report_id.data == ""
            else self.repair_need_report_id.data
        )
        if (
            self.inspection_id.data is not None
            and self.repair_need_report_id.data is not None
        ) or (
            self.inspection_id.data is None and self.repair_need_report_id.data is None
        ):
            success = False
            self.form_errors.append(
                "Musisz wybrać id zgłoszenia potrzeby naprawy lub id przeglądu, nie możesz wybrać obu na raz"
            )
        return success and super_succes


class RepairNeedReportForm(Form):
    element_id = SelectField(
        "Id elementu infrastruktury, który wymaga naprawy", validators=[InputRequired()]
    )
    date = DateField("Data zgłoszenia potrzeby naprawy", validators=[InputRequired()])
    reporting_person = StringField(
        "Osoba zgłaszająca",
        validators=[
            InputRequired(),
            Length(
                min=0,
                max=1024,
                message="Osoba zgłaszająca może zawierać maksymalnie 64 znaków",
            ),
        ],
    )
    remarks = TextAreaField(
        "Uwagi",
        validators=[
            Length(
                min=0, max=128, message="Uwagi mogą zawierać maksymalnie 128 znaków"
            ),
            Optional(),
        ],
    )

    def validate_element_id(form, self):
        if not db.session.query(ElementInfrastruktury).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje element infrastruktury o podanym id")
            return False
        else:
            return True

    def validate_date(form, self):
        if self.data is not None:
            today_date = date.today()
            if today_date < self.data:
                self.errors.append("Data zgłoszenia nie może być w przyszłości")
                return False
        return True


class RepairForm(Form):
    reason_id = SelectField(
        "Id powodu naprawy", validators=[InputRequired()], coerce=int
    )
    maintainer_id = SelectField("Id serwisanta", validators=[InputRequired()])
    element_id = SelectField(
        "Id elementu infrastruktury poddawanego naprawie", validators=[InputRequired()]
    )
    date_start = DateField("Data rozpoczęcia naprawy", validators=[InputRequired()])
    date_end = DateField("Data zakończenia naprawy", validators=[Optional()])
    cost = DecimalField("Koszt naprawy", places=2, validators=[InputRequired()])

    def validate(self):
        super_succes = super().validate()
        success = True
        if self.date_end.data is not None and self.date_start.data is not None:
            if self.date_end.data < self.date_start.data:
                self.form_errors.append(
                    "Data zakończenia musi być poźniejsza od daty rozpoczęcia"
                )
                success = False
        return super_succes and success

    def validate_date_end(form, self):
        if self.data is not None:
            today_date = date.today()
            if today_date < self.data:
                self.errors.append("Data zakończenia nie może być w przyszłości")
                return False
        return True

    def validate_reason_id(form, self):
        if not db.session.query(PowodNaprawy).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje podód naprawy o podanym id")
            return False
        else:
            return True

    def validate_maintainer_id(form, self):
        if not db.session.query(Serwisant).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje serwisant o podanym id")
            return False
        else:
            return True

    def validate_element_id(form, self):
        if not db.session.query(ElementInfrastruktury).filter_by(id=self.data).first():
            self.errors.append("Nie istnieje element infrastruktury o podanym id")
            return False
        else:
            return True
