# get-nie-appointment
A Python script that automates the process of getting an appointment for NIE assignation. It can be modified in order to change the type of appointment.

## Requirements

* Python3
* Selenium
* Firefox installed
* Gecko Driver

### Installing in Debian based distributions

* Install pip3 and geckodriver
```sh
sudo apt-get install pip3 firefox-geckodriver
```

* Install selenium
```sh
pip3 install selenium
```

### Installing in macOS

* Get pip
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

* Install pip
```sh
python3 get-pip.py
```

* Install selenium
```sh
pip3 install selenium
```

* Install
```sh
brew install geckodriver
```

## Running the script

```sh
python3 nie.py
```


## Parameters

For getting the requiered parameters, city and appointment type, visit: https://sede.administracionespublicas.gob.es/icpplustieb/index/ and complete the process one type manually. Then get the appointment type based on your city (which may vary from city to city).

## Settings File
Create a settings.ini file (added to .gitignore)

[settings]
city = Barcelona
;city = Castellón
;appointmentType = POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)
;appointmentType = AUTORIZACIÓN DE REGRESO
;appointmentType = POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN
;appointmentType = POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.
;appointmentType = POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)
;appointmentType = POLICIA-CERTIFICADOS Y ASIGNACION NIE (NO COMUNITARIOS)
;appointmentType = 4010
appointmentType = 4036
doc_type = nie
passport_nie = Y9448941A
passport_nie_expire_date = 03/11/2022
name = MARIA DE LOS MILAGROS YOZZIA
country = ARGENTINA
# Sede
placeAddress = 14
# Oficina de la cita (2da selección)
;oficina_cita = 4
email = jmjacquet@gmail.com
tel = 657274449
birthyear = 1997
max_wanted_date = 1/11/2022
days_after = 0
