'''
Created on 9 Aug 2018

@author: ostlerr
@author: castells

This code lists the documents / articles in the database: you choose the one you want to process and it saves the Schema json in the relevant 
folder prepared in your staging area. See settings to set the staging area. 
'''
import sys
import pyodbc
import json
import configparser
import settings

def connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    dsn=config['SQL_SERVER']['DSN']
    uid = config['SQL_SERVER']['UID']
    pwd = config['SQL_SERVER']['PWD']
    con = pyodbc.connect('DSN='+dsn+';uid='+uid+';pwd='+pwd)
    #con = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\website development\datacite\DataCite Metadata database.accdb;')
    #con = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\code\access\DataCite Metadata database.accdb;')
    return con


class DocumentInfo:
    
    def __init__(self):
        """
tract 
        """
        self.url = None
        self.mdId = None
        self.data = None
        self.folder = None
        self.sDOI = None

        
        
        
class Person:
    def __init__(self, row):
        self.familyName = row.family_name
        self.givenName = row.given_name 
        self.nameIdentifier = row.name_identifier 
        self.nameIdentifierScheme = row.name_identifier_scheme 
        self.schemeUri = row.scheme_uri 
        self.organisationName = row.organisation_name 
        self.street = row.street_address
        self.locality = row.address_locality 
        self.region = row.address_region 
        self.country = row.address_country 
        self.postalCode = row.postal_code
        self.fullname = self.givenName + " " + self.familyName
        if hasattr(row,'type_value'):
            self.contributorType = row.type_value
        self.nameIdentifiers = None
        if not self.nameIdentifier is None:
            self.nameIdentifiers = [
                {
                    "nameIdentifier": self.nameIdentifier,
                    "nameIdentifierScheme": self.nameIdentifierScheme,
                    "schemeURI": self.schemeUri 
                }
            ]
        self.affiliation = dict(type="Organization", name= self.organisationName,  address= self.formatAddress())
        
        
    def formatAddress(self):
        address = ""
        if not self.street is None:
            address = address + ", " + self.street
        if not self.locality is None:
            address = address + ", " + self.locality
        if not self.region is None:
            address = address + ", " + self.region
        if not self.postalCode is None:
            address = address + ", " + self.postalCode
        if not self.country is None:
            address = address + ", " + self.country
        return address
#        
    def asCreatorJson(self):
        dictaddress = dict(type="PostalAddress", streetAddress= self.organisationName, addressLocality= self.locality, addressRegion = self.region, postalCode= self.postalCode, addressCountry=self.country   )
        creator = dict(type = 'Person', Name = self.fullname,givenName = self.givenName,familyName = self.familyName, sameAs = self.nameIdentifier,address = dictaddress )
      
        creator["affiliation"] = self.affiliation
        return creator
    
    def asContributorJson(self):
        dictaddress = dict(type="PostalAddress", streetAddress= self.organisationName, addressLocality= self.locality, addressRegion = self.region, postalCode= self.postalCode, addressCountry=self.country   )
        contributor = dict(type = 'Person', jobTitle = self.contributorType, name = self.fullname, givenName = self.givenName, familyName = self.familyName, sameAs = self.nameIdentifier, address = dictaddress)
     
        contributor["affiliation"] = self.affiliation
        return contributor


def getCursor():
    con = connect()
    cur = con.cursor()
    return cur

def getDocumentMetadata(mdId):
    """ sql select m.md_id, m.url, m.identifier, m.identifier_type, m.title, p.organisation_name as publisher, publication_year, grt.type_value as grt_value, srt.type_value as srt_value,
        m.language, m.version, f.mime_type, f.extension, m.rights_text, m.rights_licence_uri, m.rights_licence, m.description_abstract,m.description_methods,m.description_toc,m.description_technical_info,m.description_quality,m.description_provenance,m.description_other,
        fl.fieldname, fl.geo_point_latitude, fl.geo_point_longitude
        from (((((metadata_document m
        inner join organisation p on m.publisher = p.organisation_id)
        inner join general_resource_types grt on m.grt_id = grt.grt_id)
        left outer join specific_resource_types srt on m.srt_id = srt.srt_id)
        inner join formats f on m.format_id = f.format_id)
        inner join experiment lte on m.lte_id = lte.experiment_id)
        inner join fields fl on lte.field_id = fl.field_id encapsulted in a view
    
    
    """
    cur = getCursor()
    cur.execute("""select * from viewMetaDocument  where md_id = ?""", mdId)
    return cur

def prepareCreators_new(mdId):
    cur = getCursor()
    creators = ""
    # First prepare named people
    cur.execute('select p.family_name, p.given_name, p.name_identifier, p.name_identifier_scheme, p.scheme_uri, o.organisation_name, o.street_address, o.address_locality, o.address_region, o.address_country, o.postal_code from (person p inner join person_creator pc on p.person_id = pc.person_id) inner join organisation o on p.affiliation = o.organisation_id where pc.md_id = ?', mdId)
    
    results = cur.fetchall()    
    for row in results: 
        person = Person(row)  
     
        creators.append(person.asCreatorJson())
           
    # second prepare organisations
    cur.execute('select * from organisation o inner join organisation_creator oc on o.organisation_id = oc.organisation_id where oc.md_id = ?',mdId)
    results = cur.fetchall()
    for row in results:
     
        creators.append({"creatorName": row.organisation_name}) 
        
    return creators 
   
def prepareCreators(mdId):
    cur = getCursor()
    creators = []
    # First prepare named people
    cur.execute('select p.family_name, p.given_name, p.name_identifier, p.name_identifier_scheme, p.scheme_uri, o.organisation_name, o.street_address, o.address_locality, o.address_region, o.address_country, o.postal_code from (person p inner join person_creator pc on p.person_id = pc.person_id) inner join organisation o on p.affiliation = o.organisation_id where pc.md_id = ?', mdId)
    
    results = cur.fetchall()    
    for row in results: 
        person = Person(row)  
     
        creators.append(person.asCreatorJson())
           
    # second prepare organisations
    cur.execute('select * from organisation o inner join organisation_creator oc on o.organisation_id = oc.organisation_id where oc.md_id = ?',mdId)
    results = cur.fetchall()
    for row in results:
     
        creators.append({"type": "organization", "name": row.organisation_name}) 
        
    return creators

def prepareContributors(mdId):
    cur = getCursor()
    contributors = [] 
    # First prepare named people
    cur.execute("""select p.family_name, p.given_name, p.name_identifier, p.name_identifier_scheme, p.scheme_uri, o.organisation_name, o.street_address, o.address_locality, o.address_region, o.address_country, o.postal_code, prt.type_value 
        from ((person p 
        inner join organisation o on p.affiliation = o.organisation_id) 
        inner join person_role pr on p.person_id = pr.person_id)
        inner join person_role_types prt on pr.prt_id = prt.prt_id
        where pr.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        person = Person(row)        
        contributors.append(person.asContributorJson())
    # second prepare organisations
    cur.execute("""select o.organisation_name, ort.type_value 
        from (organisation o 
        inner join organisation_role r on o.organisation_id = r.organisation_id) 
        inner join organisation_role_types ort on r.ort_id = ort.ort_id
        where r.md_id = ?""",mdId)
    results = cur.fetchall()
    for row in results:
        contributors.append({"sourceOrganisation": row.organisation_name}) 
        
    return contributors    
    
def prepareSubjects(mdId):
    cur = getCursor()
    subjects = []
    cur.execute("""select s.subject, s.subject_uri, ss.subject_schema, ss.schema_uri
        from (subjects s
        inner join subject_schemas ss on s.ss_id = ss.ss_id)
        inner join document_subjects ds on s.subject_id = ds.subject_id 
        where ds.md_id = ?""", mdId)
    results = cur.fetchall()    
    for row in results: 
        subjects.append(row.subject)
        
    return subjects
    
def prepareDescriptions(row):
    descriptions = []
    
    descriptions.append({'inLanguage' : row.language, 'descriptionType' : 'Abstract', 'description' : row.description_abstract})
    if not row.description_methods is None:
        descriptions.append({'inLanguage' : row.language, 'descriptionType' : 'Methods', 'description' : row.description_methods})
    if not row.description_toc is None:
        descriptions.append({'inLanguage' : row.language, 'descriptionType' : 'TableOfContents', 'description' : row.description_toc})
    if not row.description_technical_info is None:
        descriptions.append({'inLanguage' : row.language, 'descriptionType' : 'TechnicalInfo', 'description' : row.description_technical_info})
    if not row.description_quality is None or not row.description_provenance is None or not row.description_other is None:
        descriptions.append({'inLanguage' : row.language, 'descriptionType' : 'Other', 'description' : str(row.description_provenance) + " " + str(row.description_quality) + " " + str(row.description_other)})
    
    return descriptions

def prepareDateCreated(mdId):
    cur = getCursor()
    cur.execute("""select dt.type_value, dd.document_date from document_dates dd inner join date_types dt on dd.dt_id = dt.dt_id where dd.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        if row.type_value == 'Created':
            
            return row.document_date.strftime('%Y-%m-%d')

def prepareDateAvailable(mdId):
    cur = getCursor()
    cur.execute("""select dt.type_value, dd.document_date from document_dates dd inner join date_types dt on dd.dt_id = dt.dt_id where dd.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        if row.type_value in ('Available', 'Accepted') :
            return row.document_date.strftime('%Y-%m-%d') 


def prepareDateModified(mdId):
    cur = getCursor()
    cur.execute("""select dt.type_value, dd.document_date from document_dates dd inner join date_types dt on dd.dt_id = dt.dt_id where dd.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        if row.type_value == 'Updated' :
            return row.document_date.strftime('%Y-%m-%d') 

def prepareRelatedIdentifiers(mdId):
    cur = getCursor()
    related_identifiers = []
    cur.execute("""select ri.related_identifier, i.type_value as identifier_type, r.type_value as relation_type
        from (related_identifiers ri
        inner join identifier_types i on ri.it_id = i.it_id)
        inner join relation_types r on ri.rt_id = r.rt_id
        where ri.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        related_identifiers.append({'relatedIdentifier': row.related_identifier,'relatedIdentifierType' : row.identifier_type, 'relationType' : row.relation_type})
        
    return related_identifiers    

def prepareSizes(mdId):
    cur = getCursor()
    sizes = []
    cur.execute("""select u.unit_short_name, ds.size_value
        from document_sizes ds inner join measurement_unit u on ds.unit_id = u.unit_id where ds.md_id = ?""", mdId)
    
    results = cur.fetchall()    
    for row in results: 
        if row.unit_short_name == 'None':
            sizes.append(row.size_value)
        else:
            sizes.append(str(row.size_value) + ' ' + row.unit_short_name)
        
    return sizes

def prepareFundingReferences(mdId):
    cur = getCursor()
    fundingreferences = []
    cur.execute("""select fa.award_number, fa.award_uri, fa.award_title,fb.organisation_name, fb.funder_identifier, fb.funder_identifier_type
        from (document_funding df
        inner join funding_awards fa on df.fa_id = fa.fa_id)
        inner join organisation fb on fa.organisation_id = fb.organisation_id
        where df.md_id = ?""", mdId)

    results = cur.fetchall()
    for row in results:
        fundingreferences.append(
           {
               "type": "organization",
               "name": row.organisation_name,
               "sameAs": row.funder_identifier,
               "award":  row.award_number + ' - ' + row.award_title,
               "identifier": row.award_uri
            }
        )
        
    return fundingreferences

def process(documentInfo):
    mdId = documentInfo.mdId
    mdCursor = getDocumentMetadata(mdId)
    mdRow = mdCursor.fetchone()
    data = None
    print("Document ID is: " + mdId)
    if mdRow:
        mdUrl = mdRow.url
        documentInfo.url = mdUrl        
        print(documentInfo.url)
        mdExpt =  mdRow.experiment_code
        documentInfo.expt = mdExpt
        print(documentInfo.expt)
        folder = ''.join(ch for ch in mdExpt if ch.isalnum()).lower()
        documentInfo.folder = folder
        print(folder)
        sDOI = mdRow.identifier[9::]
        documentInfo.sDOI = sDOI
        print(sDOI)
        data = {
            '@context' : 'https://schema.org/',
            '@type' : 'Article',           
            'identifier' : mdRow.identifier,
            'name' : mdRow.title,
            'url': mdRow.url,
            'description': mdRow.description_abstract,
            'publisher' :{
                "type": "organization",
                "name": mdRow.publisher,
                "logo": "TODO"
                },
            'datePublished' : mdRow.publication_year,
            'dateCreated' : prepareDateCreated(mdId),
            'dateModified' : prepareDateModified(mdId),
            'datePublished' : prepareDateAvailable(mdId),
            'inLanguage' : mdRow.language,  
            'version' : str(mdRow.version), 
            'keywords' : prepareSubjects(mdId),
            'creator' : prepareCreators(mdId),
            'author' : prepareContributors(mdId),
            'encodingFormat' : mdRow.mime_type,
            'copyrightHolder' : {
                "type": "organization",
                "name": mdRow.publisher
                },
            'license':  {
                "type": "CreativeWork",
                "name": "Attribution 4.0 International (CC BY 4.0)",
                "license": mdRow.rights_licence_uri,
                "text": mdRow.rights_licence
                },
            'spatialCoverage': 
                {
                    'type': 'place',
                    'geo' : {
                        'type':'GeoCoordinates',
                        'longitude': float(mdRow.geo_point_longitude),
                        'latitude': float(mdRow.geo_point_latitude)
                    },
                    'name': mdRow.fieldname            
                },
            'funder' : prepareFundingReferences(mdId)
        }
        print(data)
        
    documentInfo.data = data    
    return documentInfo    

def save(documentInfo): 
    xname = settings.STAGE+ "metadata/"+str(documentInfo.folder)+"/"+ str(documentInfo.sDOI) + ".json"
    print (xname)
    fxname = open(xname,'w+')
    strJsDoc =  json.dumps(documentInfo.data, indent=4)
    print (strJsDoc)
    fxname.write(strJsDoc)
    fxname.close()
   
    print('json document saved in '+ xname)
    print('\n done')
    
def getDOCIDs():
    #list 
    DOCIDs = []
    cur = getCursor()
    cur.execute("""select * from viewMetaDocument where grt_value like 'text' """)
    results = cur.fetchall()  
    counter = 0  
    for row in results: 
        
        counter +=1  
        DOCIDs.append(dict(
            nb = counter,
            documentID = row.md_id,
            title = row.title,
            expCode = row.experiment_code))
           
        
    return DOCIDs 


try:
    #-28178770 is a dataset
    #-1140916605 has author
    # 4 is a text 

    
    while True:
        datasetID = 0
        documentInfo = DocumentInfo()   
        DOCIDs = getDOCIDs()
   
        IDs = []     
        tokens = []
        counter = 0
        for items in DOCIDs: 
            counter = counter + 1
            print ("%s -  %s (%s) DOCIDs =  %s" % (counter, items['title'],items['expCode'], items['documentID']))
            IDs.append(str(items['documentID']))
            tokens.append(str(counter))
        print (" ")  
        print(tokens)
    
        token = '0'
        while token == '0':
            token = input('Which document? ')
            print(token)
            if token  not in tokens:
                print("not in the list")
                token = '0'
            else: 
                inToken = int(token)
                inToken = inToken - 1
                datasetID = IDs[inToken]
            print (datasetID)
        documentInfo.mdId = datasetID
        documentInfo = process(documentInfo)    
        save(documentInfo)
        new_game = input("Would you like to do another one? Enter 'y' or 'n' ")
        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print("Thanks for your work!")
            break    
       
      
#     documentInfo.mdId = input('Enter Document ID: ')
#     documentInfo = process(documentInfo)    
#     save(documentInfo)         


        

except:
    print("Unexpected error:", sys.exc_info()[0])        
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    print(sys.exc_info()[2].tb_lineno)
    print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],
                                         sys.exc_info()[1],
                                         sys.exc_info()[2].tb_lineno))
    

