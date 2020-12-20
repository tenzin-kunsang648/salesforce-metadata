'''
Creates package xml file of Salesforce's metadata coverage

Usage: python3 createPackageXML.py

Input: dataset (reference metadataCoverage.csv)
Output: 
    clean dataset -> metadataCoverage_clean.csv
    xml files


'''

from xml.dom import minidom
import os
import pandas as pd
from bs4 import BeautifulSoup
import csv
import sys
import os
from lxml import etree
import xml.etree.ElementTree as ET


def createXML(data):
    '''
    creates an xml file using a csv dataset with two columns - metadata type (first column) 
    and the relevant api (second column - eg: metadata api, unlocked packaging, managed packaging etc.)
    
    might need to alter this based on your dataset
    '''

    package = ET.Element('Package')
    package.set('xmlns', 'http://soap.sforce.com/2006/04/metadata')
    for index, row in data.iterrows():
        types = ET.SubElement(package, 'types')
        members = ET.SubElement(types, 'members')
        members.text = '*'
        name = ET.SubElement(types, 'name')
        name.text = row['metadataType']

    mydata = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
        ET.tostring(package, encoding="unicode")

    xmlfilename = data.columns[1] + ".xml"

    with open(xmlfilename, "w") as f:
        f.write(BeautifulSoup(mydata, "xml").prettify())


def dataCleanup(data):

    '''
    cleans up the dataset. might need to alter this method based on your requirement.
    '''

    df = data
    # drop the irrelevant columns - only need metadata type, metadata API, and unlocked packaging columns
    cols = [2, 4, 5, 6, 7, 8]
    df.drop(df.columns[cols], axis=1, inplace=True)
    # rename column names
    df.columns = ['metadataType', 'metadataAPI', 'unlockedPackaging']
    # save the csv file
    df.to_csv('metadataCoverage_clean.csv')

    # create three different datasets -

    # 1. where metadata type is available in metadata API

    metadataAPI_available_data = df.drop(df.columns[2], axis=1)  # drop unlocked packaging
    metadataAPI_available_data = metadataAPI_available_data.dropna()

    # 2. where metadata type is available in unlocked packaging

    unlockedPackaging_data = df.drop(df.columns[1], axis=1)  # drop metadataAPI
    unlockedPackaging_data_available = unlockedPackaging_data.dropna()

    # 3. where metadata type is not available in unlocked packaging

    unlockedPackaging_data_notAvailable = unlockedPackaging_data[unlockedPackaging_data['unlockedPackaging'].isnull()]
    unlockedPackaging_data_notAvailable.columns = ['metadataType', 'unlockedPackaging_nan']

    return metadataAPI_available_data, unlockedPackaging_data_available, unlockedPackaging_data_notAvailable


def main():
    df = pd.read_csv("metadataCoverage.csv")
    data1, data2, data3 = dataCleanup(df)
    createXML(data1)
    createXML(data2)
    createXML(data3)


if __name__ == "__main__":
    main()
