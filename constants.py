# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List
import enum


URL_SEDE = "https://icp.administracionelectronica.gob.es/icpplus/"
# URL_SEDE = "https://sede.administracionespublicas.gob.es/icpplus/"


SECONDS_FOR_RECONNECTION = 300


@dataclass
class AppointmentType:
    id: int
    description: str = ""


@dataclass
class AppointmentsTypes:
    appointments_types: List[AppointmentType]


@dataclass
class DocumentType:
    id: int
    description: str = ""


appointmentType = {
    "20": "POLICIA-AUTORIZACIÓN DE REGRESO",
    "4010": "POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN",
    "4036": "POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)",
    "4037": "POLICIA-CARTA DE INVITACIÓN",
    "4038": "POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.",
    "4049": "POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)",
    "4067": "POLICIA- EXPEDICIÓN/RENOVACIÓN DE DOCUMENTOS DE SOLICITANTES DE ASILO",
    "4078": "POLICIA- SOLICITUD ASILO",
    "4079": "POLICIA-CERTIFICADOS Y ASIGNACION NIE (NO COMUNITARIOS)",
    "4092": "POLICIA - TÍTULOS DE VIAJE",
    "4094": "POLICÍA-EXP.TARJETA ASOCIADA AL ACUERDO DE RETIRADA CIUDADANOS BRITÁNICOS Y SUS FAMILIARES (BREXIT)",
    "4096": "POLICIA-CERTIFICADOS Y ASIGNACION NIE",
}


doc_type_id = {"nie": "rdbTipoDocNie", "dni": "rdbTipoDocDni", "pas": "rdbTipoDocPas"}

sede_cfg = {
    "5": "OUE BCN-C/MURCIA, 42, MURCIA, 42",
    "6": "PASSEIG DE SANT JOAN, PASSEIG DE SANT JOAN, 189",
    "14": "CNP MALLORCA GRANADOS, MALLORCA, 213",
    "16": "CNP RAMBLA GUIPUSCOA 74, RAMBLA GUIPUSCOA, 74",
    "17": "CNP COMISARIA LHOSPITALET DE LLOBREGAT, Rbla. Just Oliveres, 43",
    "18": "CNP COMISARIA BADALONA, AVDA. DELS VENTS, 9",
    "19": "CNP COMISARIA CASTELLDEFELS, PLAÇA DE L`ESPERANTO, 4",
    "20": "CNP COMISARIA CERDANYOLA DEL VALLES, VERGE DE LES FEIXES, 4",
    "21": "CNP COMISARIA CORNELLA DE LLOBREGAT, AV. SANT ILDEFONS, S/N",
    "22": "CNP COMISARIA SANT FELIU DE LLOBREGAT, CARRERETES, 9",
    "23": "CNP COMISARIA EL PRAT DE LLOBREGAT, CENTRE, 4",
    "24": "CNP COMISARIA SANT BOI DE LLOBREGAT, RIERA BASTÉ, 43",
    "25": "CNP COMISARIA VILADECANS, AVDA. BALLESTER, 2",
    "26": "CNP COMISARIA IGUALADA, PRAT DE LA RIBA, 13",
    "27": "CNP COMISARIA MATARO, AV. GATASSA, 15",
    "28": "CNP COMISARIA GRANOLLERS, RICOMA, 65",
    "29": "CNP COMISARIA RUBI, TERRASSA, 16",
    "30": "CNP COMISARIA SABADELL, BATLLEVELL, 115",
    "31": "CNP COMISARIA MONTCADA I REIXAC, MAJOR, 38",
    "32": "CNP COMISARIA RIPOLLET, TAMARIT, 78",
    "33": "CNP COMISARIA SANT ADRIA DEL BESOS, AV. JOAN XXIII, 2",
    "34": "CNP COMISARIA SANT CUGAT DEL VALLES, VALLES, 1",
    "35": "CNP COMISARIA SANTA COLOMA DE GRAMENET, IRLANDA, 67",
    "36": "CNP COMISARIA TERRASSA, BALDRICH, 13",
    "37": "CNP COMISARIA VIC, BISBE MORGADES, 4",
    "38": "CNP COMISARIA MANRESA, SOLER I MARCH, 5",
    "39": "CNP COMISARIA VILANOVA I LA GELTRU ODE, VAPOR, 19",
    "43": "CNP PSJ PLANTA BAJA, PASSEIG SANT JOAN, 189",
    "46": "CNP COMISARIA VILAFRANCA DEL PENEDES, Avinguda Ronda del Mar, 109",
    "48": "CNP CARTAS DE INVITACION, CALLE GUADALAJARA , 1",
    "49": "CNP COMISARIA VILANOVA I LA GELTRU, PLAÇA COTXES, 5",
    "50": "VILADECANS 2, AVDA. BALLESTER, 2",
    "51": "VILADECANS, AVDA. BALLESTER, 2",
}

"""
<select id="idSede" data-live-search="true" title="Oficina" data-size="10" class="mf-input__xl" name="idSede">
<option value="">Seleccionar ...</option>
<option value="16">CNP RAMBLA GUIPUSCOA 74, RAMBLA GUIPUSCOA, 74</option>
<option value="19">CNP COMISARIA CASTELLDEFELS, PLAÇA DE L`ESPERANTO, 4</option>
<option value="20">CNP COMISARIA CERDANYOLA DEL VALLES, VERGE DE LES FEIXES, 4</option>
<option value="26">CNP COMISARIA IGUALADA, PRAT DE LA RIBA, 13</option>
<option value="27">CNP COMISARIA MATARO, AV. GATASSA, 15</option>
<option value="30">CNP COMISARIA SABADELL, BATLLEVELL, 115</option>
<option value="34">CNP COMISARIA SANT CUGAT DEL VALLES, VALLES, 1</option>
<option value="35">CNP COMISARIA SANTA COLOMA DE GRAMENET, IRLANDA, 67</option>
<option value="36">CNP COMISARIA TERRASSA, BALDRICH, 13</option>
<option value="38">CNP COMISARIA MANRESA, SOLER I MARCH, 5</option>
<option value="39">CNP COMISARIA VILANOVA I LA GELTRU ODE, VAPOR, 19</option>
</select>
"""
