import sys
import xml.etree.ElementTree as ET
import json
import csv
import pandas as pd
from collections import OrderedDict as ordereddict

def interfaces(root):

    jsonContent = "{";

    for block in root:
        if block.tag == "interfaces":

            #jsonContent += "\"" + block.tag + "\": [{"

            countBlock = 0
            for element in block:
                print("")
                print("--" + element.tag + "---")

                jsonContent += "\"" + element.tag + "\" : {"                

                countElement = 0
                for values in element:
                    print("[" + values.tag + "] " + str(values.text)); 
                    jsonContent += "\"" + values.tag + "\" : \"" + str(values.text) + "\""
                    countElement = countElement + 1
                    if countElement != len(element):
                        jsonContent += ","
    
                jsonContent += "}"
                countBlock = countBlock + 1
                if countBlock != len(block):
                    jsonContent += ","
    
            
            #jsonContent += "}]"    
    
    jsonContent += "}"

    interface_parsed = json.loads(jsonContent, object_pairs_hook=ordereddict)

    df = pd.DataFrame(interface_parsed)

    df = df.transpose()
    df.to_csv('interface.csv',sep='\t')
   
    return "Interface ..... OK"

def filters(root):

    jsonContent = "{";

    for block in root:
        if block.tag == "filter":

            #jsonContent += "\"" + block.tag + "\": [{"

            countBlock = 0
            for element in block:
                print("")
                print("--" + element.tag + "_" + str(countBlock) + "---")

                jsonContent += "\"" + element.tag + "_" + str(countBlock) + "\" : {"                

                countElement = 0
                for values in element:
                    countElement = countElement + 1
                    if values.tag ==  "source":
                        jsonContent += "\"" + values.tag + "\" : {"  
                        countValues = 0
                        for subvalues in values:
                            countValues = countValues + 1

                            if subvalues.tag == "network":
                                jsonContent += "\"" + subvalues.tag + "\" : \"" + buscaInterfaces(root,str(subvalues.text)) + "\""
                            else:
                                jsonContent += "\"" + subvalues.tag + "\" : \"" + buscaAliases(root,str(subvalues.text)) + "\""


                            if countValues != len(values):
                                jsonContent += ","

                        jsonContent += "}"
                        if countElement != len(element):
                                jsonContent += ","

                    elif values.tag ==  "destination":
                        jsonContent += "\"" + values.tag + "\" : {"  
                        countValues = 0
                        for subvalues in values:
                            countValues = countValues + 1
                            if subvalues.tag == "network":
                                jsonContent += "\"" + subvalues.tag + "\" : \"" + buscaInterfaces(root,str(subvalues.text)) + "\""
                            else:
                                jsonContent += "\"" + subvalues.tag + "\" : \"" + buscaAliases(root,str(subvalues.text)) + "\""
                            if countValues != len(values):
                                jsonContent += ","

                        jsonContent += "}" 
                        if countElement != len(element):
                                jsonContent += ","   
 
                    #elif values.tag ==  "updated":
                        #jsonContent += "\"" + values.tag + "\" : {"  
                        #countValues = 0
                        #for subvalues in values:
                        #    countValues = countValues + 1
                        #    jsonContent += "\"" + subvalues.tag + "\" : \"" + str(subvalues.text) + "\""
                        #    if countValues != len(values):
                        #        jsonContent += ","

                        #jsonContent += "}"     
           
                    #elif values.tag ==  "created":
                        #jsonContent += "\"" + values.tag + "\" : {"  
                        #countValues = 0
                        #for subvalues in values:
                        #    countValues = countValues + 1
                        #    jsonContent += "\"" + subvalues.tag + "\" : \"" + str(subvalues.text) + "\""
                        #    if countValues != len(values):
                        #        jsonContent += ","

                        #jsonContent += "}"    
       
                    else:
                        if values.tag ==  "interface":
                            print("[" + values.tag + "] " + str(values.text)); 
                            jsonContent += "\"" + values.tag + "\" : \"" + buscaInterfaces(root,str(values.text)) + "\""
                            if countElement != len(element):
                                jsonContent += ","
                        if values.tag ==  "type":
                            print("[" + values.tag + "] " + str(values.text)); 
                            jsonContent += "\"" + values.tag + "\" : \"" + str(values.text) + "\""
                            if countElement != len(element):
                                jsonContent += ","
                        if values.tag ==  "protocol":
                            print("[" + values.tag + "] " + str(values.text)); 
                            jsonContent += "\"" + values.tag + "\" : \"" + str(values.text) + "\""
                            if countElement != len(element):
                                jsonContent += ","
                        if values.tag ==  "descr":
                            print("[" + values.tag + "] " + str(values.text)); 
                            jsonContent += "\"" + values.tag + "\" : \"" + str(values.text) + "\""
                            #if countElement != len(element):
                                #jsonContent += ","
                   
    
                jsonContent += "}"
                countBlock = countBlock + 1
                if countBlock != len(block):
                    jsonContent += ","
    
            
            #jsonContent += "}]"    
    
    jsonContent += "}"

    interface_parsed = json.loads(jsonContent)#, object_pairs_hook=ordereddict)

    df = pd.DataFrame(interface_parsed)

    df = df.transpose()
    df.to_csv('filter.csv',sep=';')
   
    return "filter  ..... OK"

def buscaAliases(root, sBusca):

    for block in root:
        if block.tag == "aliases":

            bEncontrou = False

            for element in block:
                for values in element: 
           
                    if values.tag == "name":
                        if values.text == sBusca:
                            bEncontrou = True
                    
                    if values.tag == "address" and bEncontrou == True:
                        return values.text                           

    return sBusca

def buscaInterfaces(root, sBusca):

    for block in root:
        if block.tag == "interfaces":
            for element in block:
                if element.tag == sBusca:
                    for values in element:            
                        if values.tag == "descr":
                            return values.text                           

    return sBusca


def main(argv):

    try:
        rule = sys.argv[1]
        fileXML = sys.argv[2]
        fileCSV = sys.argv[3]
        
    except :
        print("Defina o arquivo de entrada e saida: PfSense2CSV.py <REGRA> <ENTRADA> <SAIDA>")
        return 0
    
    # Abre o arquivo
    #print("passou")
    tree = ET.parse(fileXML)
    

    #Escolhe o parse de regra:
    root = tree.getroot()

    if rule == "interfaces":
        print(interfaces(root))

    if rule == "filters":
        print(filters(root))
    

    #for child in root:
    #    if child.tag == rule:
             #print( child.tag, child.attrib)
             #method_name = str(child.tag)
             #method = getattr(self, method_name, lambda: "nothing")
             #print(method())

    # Pega as linhas


if __name__ == "__main__":
       main(sys.argv[1:])
