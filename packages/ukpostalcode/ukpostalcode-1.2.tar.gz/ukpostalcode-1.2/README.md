Quickstart Usage:

UK Postalcode format and validation.
regex from https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom


INSTALL:

$ pip install https://git.jquiterio.eu/jquiterio/ukpostalcode.git
>>>import ukpostalcode as ukpc


VALIDATION

`>>>ukpc.isvalid("OX1 2JD")
>>>True`


FORMAT

`>>>ukpc.format_postalcode("OX12JD")
>>>'OX1 2JD'`


or:


`>>>ukpc.format_postalcode("O X 12J D")
>>>'OX1 2JD'`

GETTING MORE DETAILS(json)

>>>ukpc.detailed('OX1 2JD')

this will get information from http://api.getthedata.com/postcode



