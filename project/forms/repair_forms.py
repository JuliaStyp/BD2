from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, TextAreaField,\
                    DateField
from wtforms.validators import NumberRange, InputRequired, Length, Optional
from db import db, Rola, Uzytkownik, ZgloszenieNaprawy, Przeglad, PowodNaprawy, ElementInfrastruktury

class RepairReasonForm(Form):
    inspection_id = IntegerField("Id przeglądu", validators=[Optional()])
    repair_need_report_id = IntegerField("Id zgłoszenia potrzeby naprawy", validators=[Optional()])
    priority = IntegerField("Priorytet",
                            validators=[NumberRange(min=0, max=5, message="Priorytet musi być z zakresu <1,5>"),
                                        InputRequired()])
    remarks = TextAreaField("Uwagi",
                            validators=[Length(min=0, max=1024, message="Uwagi mogą zawierać maksymalnie 1024 znaków")])


    def validate_inspection_id(form, self):
        if self.data is not None:
            if not db.session.query(Przeglad).filter_by(id=self.data).exists():
                self.errors.append("Nie istnieje przegląd o podanym id")
                return False
        return True


    def validate_repair_need_report_id(form, self):
        if self.data is not None:
            if not db.session.query(ZgloszenieNaprawy).filter_by(id=self.data).exists():
                self.errors.append("Nie istnieje zgłoszenie potrzeby naprawy o podanym id")
                return False
            if db.session.query(PowodNaprawy).filter_by(zgloszenie_id=self.data).exists():
                self.errors.append(
                    "Zgłoszenie potrzeby naprawy o podanym id zostało już przypisane do istniejącej naprawy")
                return False
        return True


    def validate(self):
        super_succes = super().validate()
        success = True
        if ((self.inspection_id.data is not None and self.repair_need_report_id.data is not None) or
            (self.inspection_id.data is None and self.repair_need_report_id.data is None)):
            success = False
            self.form_errors.append
            ("Musisz wybrać id zgłoszenia potrzeby naprawy lub id przeglądu, nie możesz wybrać obu na raz")
        return success and super_succes


class RepairNeedReportForm(Form):
    element_id = IntegerField("Id elementu infrastruktury, który potrzebuje naprawy",
                              validators=[InputRequired()])
    date = DateField("Data zgłoszenia potrzeby naprawy",
                     validators=[InputRequired()])
    reporting_person = StringField("Osoba zgłaszająca",
                                   validators=
                                   [InputRequired(),
                                    Length(min=0, max=1024,
                                           message="Osoba zgłaszająca może zawierać maksymalnie 64 znaków")])
    remarks = TextAreaField("Uwagi",
                            validators=
                            [Length(min=0, max=128, message="Uwagi mogą zawierać maksymalnie 128 znaków")])


    def validate_element_id(form, self):
        if not db.session.query(ElementInfrastruktury).filter_by(id=self.data).exists():
            self.errors.append("Nie istnieje element infrastruktury o podanym id")
            return False
        else:
            return True





