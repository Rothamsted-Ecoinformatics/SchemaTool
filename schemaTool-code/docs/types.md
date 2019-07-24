# Defining types
The file passed-1140916605.json has been made by correcting manually the errors. It is a start of what we could aim at. 


## Person

### A person can be a type of the following
  - **author**: The author of this content or rating
  - **contributor** : A secondary contributor to the CreativeWork
  - **copyrightHolder**: The party holding the legal copyright to the CreativeWorkc
  - **creator**: The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork.
  - **editor**: Specifies the Person who edited the CreativeWork.
  - **funder**: A person or organisation that supports (sponsors) something through some kind of financial contribution.
  - **sdPublisher**: Indicates the party responsible for generating and publishing the current structured data markup, typically in cases where the structured data is derived automatically from existing published content but published on a different site. For example, student projects and open data initiatives often re-publish existing content with more explicitly structured metadata. 
  
### A person will have the following attributes: 
  - **familyName**: Family name. In the U.S., the last name of an Person. This can be used along with givenName instead of the name property
  - **givenName**: Given name. In the U.S., the first name of a Person. This can be used along with familyName instead of the name property
  - **contactPoint**: (type contactpoint) or **email**
  - **name**: 
  - **sameAs**: (type URL) will have the URL to orcid ID 
  - **affiliation**: (type organization)
  - **PostalAddress**
  
  
     "creator": [
        {
            "type": "Person",
            "name": "Margaret Glendining",
            "givenName": "Margaret",
            "familyName": "Glendining",
            "sameAs": "https://orcid.org/0000-0002-6466-4629",
            "address": {
            		"@type": "PostalAddress",
        			"streetAddress": "1400 VFW Parkway",
       	 		"addressLocality": "West Roxbury",
       	 		"addressRegion": "MA",
        			"postalCode": "02132",
        			"addressCountry": "GBR"
            }
        },
        {
           "@type": "Organization",
        	"sameAs": "https://ror.org/0347fy350",
        	"name": "Rothamsted Research"
        }
    ]
 
  
  "creator": [
    {
        "@type": "Person",
        "sameAs": "http://orcid.org/0000-0000-0000-0000",
        "givenName": "Jane",
        "familyName": "Foo",
        "name": "Jane Foo"
        "address": {
        	"@type": "PostalAddress",
        	"streetAddress": "1400 VFW Parkway",
       	 	"addressLocality": "West Roxbury",
       	 	"addressRegion": "MA",
        	"postalCode": "02132"
        	"addressCountry": "GBR"
      }
    },
    {
        "@type": "Person",
        "sameAs": "http://orcid.org/0000-0000-0000-0001",
        "givenName": "Jo",
        "familyName": "Bar",
        "name": "Jo Bar"
    },
    {
        "@type": "Organization",
        "sameAs": "http://ror.org/xxxxxxxxx",
        "name": "Fictitious Research Consortium"
    }
]