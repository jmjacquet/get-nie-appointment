# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from time import sleep
import logging

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import alert
from selenium.common.exceptions import NoSuchElementException


from decouple import config
from tabulate import tabulate
from constants import doc_type_id, URL_SEDE, sede_cfg, SECONDS_FOR_RECONNECTION
from exceptions import NoOfficeException
from playsound import playsound

logging.basicConfig(format='%(levelname)s: %(asctime)s || %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)



class AppointmentDriver:
    driver = webdriver.Firefox()

    @classmethod
    def wait(cls, time):
        WebDriverWait(cls.driver, time)

    @classmethod
    def close(cls):
        cls.driver.close()

    @classmethod
    def start(cls):
        # open the nie website
        logger.info("Connecting to {}...".format(URL_SEDE))
        cls.driver.get(URL_SEDE)
        sleep(1)

    @classmethod
    def _scroll_bottom(cls):
        # scroll to bottom of page
        cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @classmethod
    def _click_button(cls, btnid):
        # click button after scrolling to bottom of page
        cls._scroll_bottom()
        cls.driver.find_element_by_id(btnid).click()

    @classmethod
    def _select_option(cls, menu_id, option):
        # select option from a drop down menu
        select = Select(cls.driver.find_element_by_id(menu_id))
        select.select_by_visible_text(option)
        sleep(1)

    @classmethod
    def _select_option_value(cls, menu_id, option):
        # select option from a drop down menu
        select = Select(cls.driver.find_element_by_id(menu_id))
        select.select_by_value(option)
        sleep(1)

    @classmethod
    def _select_choice(cls, menu_id):
        radio = cls.driver.find_element_by_id(menu_id)
        radio.click()
        #sleep(1)

    @classmethod
    def _fill_field(cls, fld_id, text):
        # fill a text field
        field = cls.driver.find_element_by_id(fld_id)
        field.send_keys(text)

    @classmethod
    def _cancel_and_leave(cls):
        # if the date is not correct, exit
        try:
            cls._click_button("btnCancelar")
        except NoSuchElementException:
            pass
        alert = cls.driver.switch_to.alert
        alert.accept()

    @classmethod
    def require_appointment(cls):
        # ask for an appointment
        cls._click_button("btnEnviar")

    @classmethod
    def go_to_conditions_page(cls):
        # conditions page after appointment page
        cls._click_button("btnEntrar")

    @classmethod
    def no_appointment(cls):
        # if there are no offices to choose from, exit
        try:
            cls._click_button("btnSalir")
            return
        except NoSuchElementException as e:
            pass

        try:
            cls._click_button("btnSubmit")
        except NoSuchElementException as e:
            return


class AppointmentApp(AppointmentDriver):

    found_appointments = []

    def __init__(
        self,
        city,
        appointment_type,
        place_address,
        oficina_cita,
        doc_type,
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
        self.doc_type_id = doc_type_id[doc_type]
        self.name = name
        self.country = country
        self.passport_nie_expire_date = passport_nie_expire_date
        self.birthyear = birthyear
        self.cel_tel = (cel_tel,)
        self.email = (email,)
        self.min_wanted_date = min_wanted_date
        self.max_wanted_date = max_wanted_date
        self.oficina_cita = oficina_cita

        self.selected_office = None

    def go_to_city_page(self):
        # fill in and continue on the select city page
        sleep(1)
        self._select_option("form", self.city)
        self._click_button("btnAceptar")

    def go_to_appointment_page(self):
        # choose the correct type of appointment for NIE page
        self._scroll_bottom()
        if self.place_address:
            self._select_option_value("sede", self.place_address)
        if self.appointment_type:
            self._select_option_value("tramiteGrupo[0]", self.appointment_type)
        self._click_button("btnAceptar")

    def go_to_info_page(self):
        # input basic info to ask for appointment
        self._select_choice(self.doc_type_id)
        self._fill_field("txtIdCitado", self.passport_nie)
        try:
            self._fill_field("txtDesCitado", self.name)
        except:
            pass
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

    def too_many_redirects(self):
        # check if we have a 429 and wait
        return "429 Too Many Requests" in self.driver.title

    def go_to_office_page(self):
        """
        Select second office because it could return a single preselected office
        or multiple where you have to make a choice
        """
        try:
            if self.oficina_cita:
                self._select_option_value("idSede", self.oficina_cita)
                self.selected_office = sede_cfg.get(self.oficina_cita)
            else:
                site = AppointmentDriver.driver.find_element_by_id("idSede")
                site.send_keys(Keys.DOWN)
                self.selected_office = site.text
            self._click_button("btnSiguiente")
        except Exception:
            self.selected_office = None
            raise NoOfficeException

    def add_extra_info(self):
        # info to be inputted after office selection - last step
        self._fill_field("txtTelefonoCitado", self.cel_tel)
        self._fill_field("emailUNO", self.email)
        self._fill_field("emailDOS", self.email)
        self._click_button("btnSiguiente")

    @staticmethod
    def get_valid_date(actual_date, min_date, max_date):
        return (actual_date >= min_date) and (actual_date <= max_date)

    @classmethod
    def print_found_appointments(cls):
        print(
            tabulate(
                cls.found_appointments,
                ["#", "Fecha", "Hora", "Oficina"],
                "rst",
                showindex="always",
            )
        )

    def add_appointment(self, app_date, app_time, app_office):
        if app_date not in [c[0] for c in self.__class__.found_appointments]:
            self.__class__.found_appointments.append((app_date, app_time, app_office))
            self.__class__.found_appointments = list(
                set(self.__class__.found_appointments)
            )
            self.__class__.found_appointments.sort(key=lambda x: x[0])
            self.print_found_appointments()

    def find_better_appointment(self):
        """
        Find the best appointments based on the max/min date and the office selected
        """
        result = False
        if (
            "Seleccione una de las siguientes citas disponibles"
            in self.driver.page_source
        ):
            try:
                # if self.appointment_type in ('4010'):
                #     almanaque_header = self.driver.find_elements_by_class_name("ui-datepicker-month")[0]
                #     if almanaque_header.text in ("Agosto",'Septiembre'):
                #         return True
                #     else:
                #         print("Month: {}".format(almanaque_header.text))
                # else:
                    for i, e in enumerate(
                        self.driver.find_elements_by_class_name("tc"), start=1
                    ):
                        app_date = e.find_element_by_xpath(
                            "//label[@id='lCita_" + str(i) + "']/span[2]"
                        ).text
                        app_time = e.find_element_by_xpath(
                            "//label[@id='lCita_" + str(i) + "']/span[4]"
                        ).text
                        app_office = sede_cfg.get(self.place_address, self.place_address) if self.place_address else self.selected_office
                        app_date = datetime.strptime(app_date, "%d/%m/%Y").date()
                        if self.get_valid_date(
                            app_date, self.min_wanted_date, self.max_wanted_date
                        ):
                            print(
                                "Date: {} Time: {} Office: {}".format(
                                    app_date, app_time, app_office
                                )
                            )
                            result = True
                        else:
                            self.add_appointment(app_date, app_time, app_office)
            except Exception as e:
                logger.error(e)
        return result

    def select_appointment(self):
        """Select appointment ir continue the loop"""
        if "no hay citas disponibles" not in AppointmentDriver.driver.page_source:
            if self.find_better_appointment():
                print("FOUND ONE!! in {} offices.".format(self.selected_office))
                return True
            else:
                self._cancel_and_leave()
        else:
            self._click_button("btnSubmit")
        return False


if __name__ == "__main__":
    AppointmentApp.start()
    retry_num = 0
    try:
        city = (
            config("city", default=None) or sys.argv[1]
        )  # as defined in the list of cities that the page has
        passport_nie = config("passport_nie", default=None) or sys.argv[2]
        doc_type = config("doc_type", default="nie") or sys.argv[2]
        name = config("name", default=None) or sys.argv[3]
        country = (
            config("country", default=None) or sys.argv[4]
        )  # as defined in the list of countries that the page has ( in UPPERCASE )
        birthyear = config("birthyear", default=None) or sys.argv[5]
        cel_tel = (
            config("tel", default=None) or sys.argv[6]
        )  # Spanish phone number without country code
        email = config("email", default=None) or sys.argv[7]
        appointment_type = (
            config("appointmentType", default=None) or sys.argv[8]
        )  # as defined in the list of appointment types of the selected city
        place_address = config(
            "placeAddress", default=""
        )  # as defined in the list of appointment types of the selected city
        oficina_cita = config(
            "oficina_cita", default=""
        )  # as defined in the list of appointment types of the selected city
        max_wanted_date = config("max_wanted_date", default=None) or sys.argv[10]
        passport_nie_expire_date = config("passport_nie_expire_date", default=None)
        days_after = int(config("days_after", default=0) or sys.argv[12])
        min_wanted_date = (datetime.now() + timedelta(days=days_after)).date()
        max_wanted_date = datetime.strptime(max_wanted_date, "%d/%m/%Y").date()
        print("Looking for appointment of type: " + appointment_type)
        print("\tCity of appointment: " + city)
        print("\tName: " + name)
        print("\tDoc.Type: " + doc_type)
        print("\tPassport: " + passport_nie)
        print("\tCountry: " + country)
        print("\tYear of birth: " + birthyear)
        print("\tEmail: " + email)
        print("\tTelephone: " + cel_tel)
        print(
            "\tFrom Date: {} to: {}".format(str(min_wanted_date), str(max_wanted_date))
        )
        print("\tOffice: {}".format(sede_cfg.get(place_address, place_address) if place_address else "Cualquiera"))
        appointment = AppointmentApp(
            city=city,
            appointment_type=appointment_type,
            place_address=place_address,
            doc_type=doc_type,
            passport_nie=passport_nie,
            name=name,
            country=country,
            passport_nie_expire_date=passport_nie_expire_date,
            birthyear=birthyear,
            cel_tel=cel_tel,
            email=email,
            min_wanted_date=min_wanted_date,
            max_wanted_date=max_wanted_date,
            oficina_cita=oficina_cita,
        )
        while True:
            if appointment.too_many_redirects():
                retry_num += 1
                logger.info("Reconnecting... waiting {} seconds for retry Nº {}.".format(SECONDS_FOR_RECONNECTION, retry_num))
                sleep(SECONDS_FOR_RECONNECTION)
                AppointmentApp.start()
            try:
                appointment.go_to_city_page()
                appointment.go_to_appointment_page()
                appointment.go_to_conditions_page()
                appointment.go_to_info_page()
                appointment.require_appointment()
                try:
                    appointment.go_to_office_page()
                except NoOfficeException:
                    appointment.no_appointment()
                    continue
                appointment.add_extra_info()
                if appointment.select_appointment():
                    playsound("clock.mp3")
                    break
            except Exception as e:
                appointment.no_appointment()
                continue

    except KeyboardInterrupt:
        AppointmentApp.close()


    # error page URL https://sede.administracionespublicas.gob.es/icpplustieb/acOfertarCita

    # office selection page URL is https://sede.administracionespublicas.gob.es/icpplustieb/acCitar

    # for the info_compl page URL is https://sede.administracionespublicas.gob.es/icpplustieb/acVerFormulario

    # could get generic back page: https://sede.administracionespublicas.gob.es/icpplustieb/infogenerica
    # use click_button("btnSubmit") if so
