class Patient:

    def __init__(self, patient: dict):
        self.patient = self.clean_payload(patient)
        self.name = self.parse_name()
        self.gender = self.parse_gender()
        self.birthdate = self.parse_birthdate()
        self.parents = self.parse_parents()
        self.deceased = self.parse_deceased()
        self.protected_person = self.parse_protected_person()
        self.race = self.parse_race()
        self.indigenous_ethnicity = self.parse_indigenous_ethnicity()
        self.birth_city = self.parse_birth_city()
        self.birth_country = self.parse_birth_country()
        self.nationality = self.parse_nationality()
        self.naturalization = self.parse_naturalization()
        self.identifier = self.parse_identifier()
        self.active = self.parse_active()
        self.telecom = self.parse_telecom()
        self.address = self.parse_address()

    def clean_payload(self, patient):
        return patient['soapEnvelope']['soapBody']['cadresponseConsultar']['usuUsuarioSUS']
    
    def parse_active(self):
        # TODO: validate condition
        if self.patient['usuSituacao'] == 'true':
            return True
        else:
            return False 
    
    def parse_address(self):
        # TODO: handle multiple address
        address = self.patient['usuEnderecos']['usuEndereco']
        address_parsed = {'use': 'home', # FIXME :identify atribute/code. Ref: https://hl7.org/fhir/R4/valueset-address-use.html
                          'type' : 'both', # FIXME :identify atribute/code. Ref: https://hl7.org/fhir/R4/valueset-address-type.html
                          'line' : [
                                    address['endTipoLogradouro']['tipcodigoTipoLogradouro']['#text'],
                                    address['endnomeLogradouro']['#text'],
                                    address['endnumero']['#text'],
                                    address['endcomplemento']['#text'],
                                    address['endBairro']['bairdescricaoBairro']['#text']
                                    ],
                          'city' : address['endMunicipio']['muncodigoMunicipio']['#text'],
                          'state' : address['endMunicipio']['munUF']['ufcodigoUF']['#text'],
                          'postalCode' : address['endCEP']['cepnumeroCEP']['#text']
                          }

        return address_parsed

    def parse_birthdate(self):
        return self.patient['usudataNascimento']
    
    def parse_birth_country(self):
        # TODO: check 'de-para'. Ref: https://rnds-fhir.saude.gov.br/ValueSet-BRPais-1.0.html
        # TODO: save as str without left zero
        return {'code': int(self.patient['usuDadosNacionalidade']['dadPaisNascimento']['paiscodigoPais']['#text']),
                'value': self.patient['usuDadosNacionalidade']['dadPaisNascimento']['paisnomePais']['#text']}
    
    def parse_birth_city(self):
        # TODO: check 'de-para'. Ref: https://rnds-fhir.saude.gov.br/ValueSet-BRMunicipio-1.0.html
        # TODO: save as str without left zero
        return {'code': int(self.patient['usuMunicipioNascimento']['muncodigoMunicipio']['#text']),
                'value': self.patient['usuMunicipioNascimento']['munnomeMunicipio']['#text']}
       
    def parse_deceased(self):
        alive = self.patient['usuvivo']
        if alive == 'true':
            return False
        else:
            return True
   
    def parse_gender(self):
        gender = self.patient['usuSexo']['sexocodigoSexo']['#text']
        match gender:
            case 'M':
                return 'male'
            case 'F':
                return 'female'
            case _:
                return 'unknown'
    
    def parse_identifier(self):
        identifier = {'cpf': self.patient['usuCPF']['cpfnumeroCPF']['#text'],
                      'cns':{'d': '', 'p': []}}

        for cns in self.patient['usuCartoes']['usuCNS']:
            if cns['cnstipoCartao']['#text'] == 'D':
                identifier['cns'].update({'d': cns['cnsnumeroCNS']['#text']})
            else:
                identifier['cns']['p'].append(cns['cnsnumeroCNS']['#text'])

        return identifier

    def parse_indigenous_ethnicity(self):
        # TODO: check 'de-para'. Ref: https://rnds-fhir.saude.gov.br/ValueSet-BREtniaIndigena-1.0.html
        # TODO: check if statement with data
        if '#text' in self.patient['usuEtniaIndigena']['etncodigoEtniaIndigena'].keys():
            return {'code': self.patient['usuEtniaIndigena']['etncodigoEtniaIndigena']['#text']}
        else:
            return None

    def parse_name(self):
        return self.patient['usuNomeCompleto']['nomNome']['#text']
    
    
    def parse_nationality(self):
        # TODO: check 'de-para'. Ref: https://rnds-fhir.saude.gov.br/ValueSet-BRNacionalidade.html
        return {'code': self.patient['usuDadosNacionalidade']['dadnacionalidade']['#text']}
    
    def parse_naturalization(self):
        # TODO: implement parser
        return None
    
    def parse_parents(self):
        parents = {'mother':'', 'father':''}
        
        # TODO: validate condition
        if 'usuMae' in self.patient.keys():
            parents.update({'mother': self.patient['usuMae']['nomNome']['#text']})
        if 'usuPai' in self.patient.keys():
            parents.update({'father': self.patient['usuPai']['nomNome']['#text']})
        return parents

    def parse_protected_person(self):
        vip = self.patient['usuVip']
        witness = self.patient['usuprotecaoTestemunha']
        
        # TODO: validate condition
        if vip == 'true' or witness == 'true':
            return True
        else:
            return False
    
    def parse_race(self):
        # TODO: check 'de-para'. Ref: https://rnds-fhir.saude.gov.br/ValueSet-BRRacaCor-1.0.html
        # TODO: check if missing value is possible (id = 99)
        return {'code': self.patient['usuRacaCor']['raccodigoRacaCor']['#text'],
                'value': self.patient['usuRacaCor']['racdescricaoRacaCor']['#text']}
    
    def parse_telecom(self):
        # TODO: handle multiple telephones

        # FIXME: get 'use' "de-para". Ref: https://hl7.org/fhir/R4/valueset-contact-point-use.html
        use = {'1': 'home'}  

        # TODO: confirm cadsus only have telephones
        phone = self.patient['usuTelefones']['usuTelefone']

        phone_parsed = {'id': phone['telidentificador']['#text'],
                        'system': 'phone', # Ref: https://hl7.org/fhir/R4/valueset-contact-point-system.html
                        'value': f"+{phone['telDDI']['#text']} {phone['telDDD']['#text']} {phone['telnumeroTelefone']['#text']}",
                        'use': use[phone['telTipoTelefone']['tipcodigoTipoTelefone']['#text']]
                        }
        return phone_parsed





