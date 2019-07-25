# Defining types and classes

The file passed-1140916605.json has been made by correcting manually the errors. It is a start of what we could aim at. 
## dataset itself
  - ** **: 
  - **distribution**: A downloadable form of this dataset, at a specific location, in a specific format. expected type: DataDownload
  - **contactPoint**: (type contactpoint) or **email**: I note that contact point will need a URL, or a telephone  number.
  
## Person

### A person can be a type of the following
  - **author**: The author of this content or rating
  - **contributor** : A secondary contributor to the CreativeWork: and in contact point type we can put curator. 
  - **copyrightHolder**: The party holding the legal copyright to the CreativeWorkc
  - **creator**: The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork.
  - **editor**: Specifies the Person who edited the CreativeWork. Could this be the curator?
  - **funder**: A person or organisation that supports (sponsors) something through some kind of financial contribution.
  - **sdPublisher**: Indicates the party responsible for generating and publishing the current structured data markup, typically in cases where the structured data is derived automatically from existing published content but published on a different site. For example, student projects and open data initiatives often re-publish existing content with more explicitly structured metadata. 
  
### A person will have the following attributes: 
  - **familyName**: Family name. In the U.S., the last name of an Person. This can be used along with givenName instead of the name property
  - **givenName**: Given name. In the U.S., the first name of a Person. This can be used along with familyName instead of the name property  
  - **name**: First + last name: it fails if there is no name. 
  - **sameAs**: (type URL) will have the URL to orcid ID 
  - **affiliation**: (type organization)
  - **address** : type PostalAddress 

```
  
    "creator": {
		"type": "Person",
		"name": "Margaret Glendining",
		"givenName": "Margaret",
		"familyName": "Glendining",
		"sameAs": "https://orcid.org/0000-0002-6466-4629",
		"address": {
			"@type": "PostalAddress",
			"streetAddress": "Rothamsted Research",
			"addressLocality": "Harpenden",
			"addressRegion": "Hertfordshire",
			"postalCode": "AL5 2JQ",
			"addressCountry": "GBR"
		},
		"contactPoint": {
			"type": "ContactPoint",
			"email": "era@rothamsted.ac.uk",
			"contactType": "curator",
			"url": "<root>/contact.php"
		},
		"affiliation": {
			"@type": "organization",
			"name": "Rothamsted Research",
			"sameAs": "https://ror.org/0347fy350"
		}
	}
	
```
	

