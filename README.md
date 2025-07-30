## Medblocks

Aarthy Medblocks-ErpNext integration
### FHIR PATIENT
```
{
  "id": "c5c3dcbb-6e45-4bfe-9127-7f74f524ee4b",
  "resourceType": "Patient",
  "meta": {
    "versionId": "7286efb0-c226-4b87-a806-8e22ec2e3884",
    "lastUpdated": "2025-03-19T15:42:08.978Z"
  },
   "address": [
    {
      "text": "Somur",
      "postalCode": ""
    }
  ],
  "birthDate": "2024-12-05",
  "gender": "male",
  "identifier": [
    {
      "system": "https://medblocks.com/fhir/aarthy_uid",
      "value": "AEHMB189077"
    }
  ],
  "name": [
    {
      "text": "test Abhinand",
      "prefix": [
        "mr"
      ]
    }
  ],
  "photo": [],
  "telecom": [
    {
      "system": "phone",
      "value": "9787161565"
    }
  ],
  "active": true,
  "contact": [
    {
      "relationship": [
        {
          "coding": [
            {
              "system": "relationSystem",
              "code": "Son"
            }
          ],
          "text": ""
        }
      ]
    }
  ]
}
```

### OPPORTUNITY BODY
```
{
"mrn_no" : "AEHMB189077"
}
```
#### License

mit
