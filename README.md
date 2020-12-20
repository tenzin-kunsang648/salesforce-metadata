# salesforce-metadata
creates xml files using dataset of the newest version of Salesforce's metadata coverage(includes metadata api and unlocked packaging)

https://developer.salesforce.com/docs/metadata-coverage/51

Usage:

    python3 createPackageXML.py
    
OR run createPackageXML.ipynb

Input: dataset (reference metadataCoverage.csv)

Output: 

clean dataset -> metadataCoverage_clean.csv

xml files


Challenge: 

    Final xml file includes colon in the Package tag 
        
         <Package xmlns:="http://soap.sforce.com/2006/04/metadata">
    
    Remove colon like so 
         <Package xmlns="http://soap.sforce.com/2006/04/metadata">

Would appreciate help to remove it during the creation. couldn't figure it out yet.

