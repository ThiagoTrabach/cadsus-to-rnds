from cadsus_to_rnds.utils import xml_to_dict, save_to_json
from cadsus_to_rnds.cadsus import Patient
import pprint

def main():
    cadsus_patient = xml_to_dict('./data/patient.xml')
    patient = Patient(cadsus_patient)
    print(f'NOME: {patient.name}')
    print(f'GENDER: {patient.gender}')
    print(f'BIRTH_DATE: {patient.birthdate}')
    print(f'IDENTIFIER: {patient.identifier}')
    print(f'PARENTS: {patient.parents}')
    print(f'NATIONALTY: {patient.nationality}')
    print(f'BIRTH_CITY: {patient.birth_city}')    
    print(f'BIRTH_COUNTRY: {patient.birth_country}')
    print(f'NATURALIZATION: {patient.naturalization}')
    print(f'RACE: {patient.race}')
    print(f'ETHNICITY: {patient.indigenous_ethnicity}')
    print(f'DECEASED: {patient.deceased}')
    print(f'PROTECTED_PERSON: {patient.protected_person}')
    print(f'ACTIVE: {patient.active}')
    print(f'ADDRESS: {patient.address}')
    print(f'TELECOM: {patient.telecom}')


if __name__ == '__main__':
    main()