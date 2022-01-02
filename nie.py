# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from decouple import config
from tabulate import tabulate

class AppointmentApp:

    driver = webdriver.Firefox()

    def __init__(self,
        city,
        appointment_type,
        place_address,
        passport_nie,
        name,
        country,
        passport_nie_expire_date,
        birthyear,
        cel_tel,
        email,
        min_wanted_date,
        max_wanted_date,
    ):
        self.city = city
        self.appointment_type = appointment_type
        self.place_address = place_address
        self.passport_nie = passport_nie
        self.name = name
        self.country = country
        self.passport_nie_expire_date = passport_nie_expire_date
        self.birthyear = birthyear
        self.cel_tel = (cel_tel,)
        self.email = (email,)
        self.min_wanted_date = min_wanted_date
        self.max_wanted_date = max_wanted_date

        self.selected_office = None

    @classmethod
    def wait(cls, time):
        WebDriverWait(cls.driver, time)

    @classmethod
    def start(cls):
        # open the nie website
        cls.driver.get("https://sede.administracionespublicas.gob.es/icpplustieb/index/")

    def _scroll(self):
        # scroll to bottom of page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _click_button(self, btnid):
        # click button after scrolling to bottom of page
        self._scroll()
        self.driver.find_element_by_id(btnid).click()

    def _select_option(self, menu_id, option):
        # select option from a drop down menu
        select = Select(self.driver.find_element_by_id(menu_id))
        select.select_by_visible_text(option)

    def _fill_field(self, fld_id, text):
        # fill a text field
        field = self.driver.find_element_by_id(fld_id)
        field.send_keys(text)



    def go_to_city_page(self):
        # fill in and continue on the select city page
        self._select_option("form", self.city)
        self._click_button("btnAceptar")

    def go_to_appointment_page(self):
        # choose the correct type of appointment for NIE page
        self._scroll()
        if self.place_address:
            self._select_option("sede", self.place_address)
        if self.appointment_type:
            self._select_option("tramiteGrupo[0]", self.appointment_type)
        self._click_button("btnAceptar")

    def go_to_conditions_page(self):
        # conditions page after appointment page
        self._click_button("btnEntrar")

    def go_to_info_page(self):
        # input basic info to ask for appointment
        self._fill_field("txtIdCitado", self.passport_nie)
        self._fill_field("txtDesCitado", self.name)
        try:
            self._select_option("txtPaisNac", self.country)
        except:
            pass
        try:
            self._fill_field("txtAnnoCitado", self.birthyear)
        except:
            pass
        try:
            if self.passport_nie_expire_date:
                self._fill_field("txtFecha", self.passport_nie_expire_date)
        except:
            pass
        self._click_button("btnEnviar")

    def require_appointment(self):
        # ask for an appointment
        self._click_button("btnEnviar")

    def go_to_office_page(self):
        """
        Select second office because it could return a single preselected office
        or multiple where you have to make a choice
        """
        try:
            site = self.driver.find_element_by_id("idSede")
            site.send_keys(Keys.DOWN)
            self.selected_office = site.text
            self._click_button("btnSiguiente")
        except:
            self.selected_office = None
            pass

    def no_appointment(self):
        # if there are no offices to choose from, exit
        try:
            self._click_button("btnSalir")
        except NoSuchElementException:
            pass
        try:
            self._click_button("btnSubmit")
        except NoSuchElementException:
            pass

    def cancel_and_leave(self):
        # if the date is not correct, exit
        try:
            self._click_button("btnCancelar")
        except NoSuchElementException:
            pass
        self.driver.switch_to_alert()
        self.driver.find_element_by_id("YesBtn").click()

    def add_extra_info(self):
        # info to be inputted after office selection - last step
        self._fill_field("txtTelefonoCitado", self.cel_tel)
        self._fill_field("emailUNO", self.email)
        self._fill_field("emailDOS", self.email)
        self._click_button("btnSiguiente")

    @staticmethod
    def get_valid_date(actual_date, min_date, max_date):
        return (actual_date >= min_date) and (actual_date <= max_date)

    @staticmethod
    def print_found_appointments(found_appointments):
        print(tabulate(found_appointments, ['#', 'Fecha', 'Hora', 'Oficina'], 'rst', showindex="always"))

    def add_appointment(self, app_date, app_time, app_office, found_appointments):
        if app_date not in [c[0] for c in found_appointments]:
            found_appointments.append((app_date, app_time, app_office))
            found_appointments = list(set(found_appointments))
            found_appointments.sort(key=lambda x: x[0])
            self.print_found_appointments(found_appointments)
        return found_appointments

    def find_better_appointment(self):
        """
        Find the best appointments based on the max/min date and the office selected
        """
        result = False
        if "Seleccione una de las siguientes citas disponibles" in self.driver.page_source:
            try:
                for i, e in enumerate(self.driver.find_elements_by_class_name("tc"), start=1):
                    app_date = e.find_element_by_xpath("//label[@id='lCita_"+str(i)+"']/span[2]").text
                    app_time = e.find_element_by_xpath("//label[@id='lCita_"+str(i)+"']/span[4]").text
                    app_office = self.selected_office or self.place_address
                    app_date = datetime.strptime(app_date, '%d/%m/%Y').date()
                    if self.get_valid_date(app_date, self.min_wanted_date, self.max_wanted_date):
                        print("Date: {} Time: {}".format(app_date, app_time))
                        result = True
                    else:
                        self.add_appointment(app_date, app_time, app_office)
            except Exception as e:
                print(e)
        return result

    def select_appointment(self):
        """Select appointment ir continue the loop"""
        if not "no hay citas disponibles" in self.driver.page_source:
            if self.find_better_appointment():
                print("FOUND ONE!! in {} offices.".format(self.selected_office))
                return True
            self.wait(1000)
            # cancel_and_leave()
            self.start()
        else:
            self._click_button("btnSubmit")
        return False



if __name__ == '__main__':
    AppointmentApp.start()
    try:
        found_appointments = []
        city = config("city", default=None) or sys.argv[1] # as defined in the list of cities that the page has
        passport_nie = config("passport_nie", default=None) or sys.argv[2]
        name = config("name", default=None) or sys.argv[3]
        country = config("country", default=None) or sys.argv[4]   # as defined in the list of countries that the page has ( in UPPERCASE )
        birthyear = config("birthyear", default=None) or sys.argv[5]
        cel_tel = config("tel", default=None) or sys.argv[6] # Spanish phone number without country code
        email = config("email", default=None) or sys.argv[7]
        appointment_type = config("appointmentType", default=None) or sys.argv[8] # as defined in the list of appointment types of the selected city
        place_address = config("placeAddress", default=None)# as defined in the list of appointment types of the selected city
        max_wanted_date = config("max_fecha_deseada", default=None) or sys.argv[10]
        passport_nie_expire_date = config("passport_nie_expire_date", default=None)
        days_after = int(config("days_after", default=0) or sys.argv[12])
        min_wanted_date = (datetime.now() + timedelta(days=days_after)).date()
        max_wanted_date = datetime.strptime(max_wanted_date, '%d/%m/%Y').date()
        print ("Looking for appointment of type: " + appointment_type)
        print ("\tCity of appointment: " + city)
        print ("\tName: " + name)
        print ("\tPassport: " + passport_nie)
        print ("\tCountry: " + country)
        print ("\tYear of birth: " + birthyear)
        print ("\tEmail: " + email)
        print ("\tTelephone: " + cel_tel)
        print ("\tFrom Date: {} to: {}".format(str(min_wanted_date) ,str(max_wanted_date)))
        print ("\tOffice: " + place_address)
        appointment = AppointmentApp(
            city = city,
            appointment_type = appointment_type,
            place_address = place_address,
            passport_nie = passport_nie,
            name = name,
            country = country,
            passport_nie_expire_date = passport_nie_expire_date,
            birthyear = birthyear,
            cel_tel = cel_tel,
            email = email,
            min_wanted_date = min_wanted_date,
            max_wanted_date = max_wanted_date,
        )
        while True:
            appointment.go_to_city_page()
            appointment.go_to_appointment_page()
            appointment.go_to_conditions_page()
            appointment.go_to_info_page()
            appointment.require_appointment()
            try:
                appointment.go_to_office_page()
                AppointmentApp.wait(100)
                appointment.add_extra_info()
                if appointment.select_appointment():
                    break
            except Exception as e:
                # print(e)
                appointment.no_appointment()

    except KeyboardInterrupt:
        AppointmentApp.wait(100)

    #error page URL https://sede.administracionespublicas.gob.es/icpplustieb/acOfertarCita

    #office selection page URL is https://sede.administracionespublicas.gob.es/icpplustieb/acCitar

    #for the info_compl page URL is https://sede.administracionespublicas.gob.es/icpplustieb/acVerFormulario

    #could get generic back page: https://sede.administracionespublicas.gob.es/icpplustieb/infogenerica
    #use click_button("btnSubmit") if so
