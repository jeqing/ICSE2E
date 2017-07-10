

import os
import sys
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from simple_salesforce import Salesforce

sys.path.append('C:\\Python_Lib\\pypyodbc\\')
import pypyodbc


class Logger:
    def __init__(self,logPrefix,logFolder):
    
        self.folder = logFolder
        self.filename = logPrefix + "_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
        self.fileHandle = open(self.folder + self.filename,'w')
        self.errors = []
        self.numErrors = 0
        
    def writeToLog(self, text):
        currTime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.fileHandle.write(currTime + " " + text + "\n")

        textUpper = text.upper()
        if (textUpper[0:5] == "ERROR"):
            self.errors.append(text)
            self.numErrors += 1

    def closeLog(self):
        if (self.numErrors == 0):
            self.writeToLog("\n###################\nSUCCESS: No errors in log")
        else:
            self.writeToLog("\n###################\n" + str(self.numErrors).strip() + " errors found in log:\n###################\n")
            for error in self.errors:
                self.writeToLog(error)
        self.fileHandle.close()
        

class WebEntry:
    def __init__(self, log):
        self.browser = webdriver.Firefox()
        self.log = log

    def navigate(self, site):
        try:
            self.log.writeToLog("Navigating to site: " + str(site))
            self.browser.get(site)
        except Exception as e:
            self.log.writeToLog("Exception navigating to site: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def isFieldHidden(self, id):

        try:
            result = self.browser.find_element_by_id(id).get_attribute("data-hidden")
            if (result == "false"):
                return False
            else:
                return True
        except Exception as e:
            self.log.writeToLog("Exception checking data hidden attribute of element: " + str(e))
            #self.log.closeLog()
            #sys.exit(9)

    # Function to check page has loaded through presence of page element
    # Has a timeout also
    def pageLoad(self, sleepTimeSec, timeOutSec, xpathcommand):

        self.log.writeToLog("Waiting for xpath command: " + str(xpathcommand))
        i = 0
        time.sleep(1)
        while True:
            try:
                check = self.browser.find_elements_by_xpath(xpathcommand)
            except:
                check = []
            if (len(check) > 0):
                return 0
            i += 1
            time.sleep(sleepTimeSec)
            if (i > (timeOutSec/sleepTimeSec)):
                return 9

    # Function to add a person to the dwelling summary form
    def addPerson(self, personNo, firstNameStr, surnameStr, ageStr, relationshipStr):

        try:
            self.log.writeToLog("Adding person to summary: " + str(firstNameStr) + ", " + str(surnameStr))
            if (personNo > 1):
                
                addperson = self.browser.find_element_by_xpath('//button[text() = "Add Person"]')
                addperson.click()
                time.sleep(2)
            
            firstname = self.browser.find_elements_by_xpath('//label/span[text() = "first names"]/../input')[personNo-1]
            firstname.send_keys(firstNameStr)

            surname = self.browser.find_elements_by_xpath('//label/span[text() = "family name"]/../input')[personNo-1]
            surname.send_keys(surnameStr)

            age = self.browser.find_elements_by_xpath('//numeric-age-field/fieldset[@id="fieldwrapper-age"]/div/input')[personNo-1]
            age.send_keys(ageStr)

            if (personNo > 1):
                relationship = Select(self.browser.find_elements_by_xpath('//dropdown-field/fieldset[@id = "fieldwrapper-relationship"]/div/select')[personNo-1])
                relationship.select_by_visible_text(relationshipStr)
        except Exception as e:
            self.log.writeToLog("Exception adding persion " + str(e))
            self.log.closeLog()
            sys.exit(9)
            

    def clickElement(self, fieldsetId, exactMatch, text):

        try:
            self.log.writeToLog("Click element with fieldset id: " + str(id) + ", Exact match text: " + str(exactMatch) + " Text: " + text)
            xpathStr = "//fieldset[@id = \"" + fieldsetId + "\"]/div/label/span"
            if (exactMatch):
                xpathStr = xpathStr + "[text()=\"" + text + "\"]/../input"
            else:
                xpathStr = xpathStr + "[contains(text(),\"" + text + "\")]/../input"
            
            control = self.browser.find_element_by_xpath(xpathStr)
            control.click()
        except Exception as e:
            self.log.writeToLog("Exception clicking element: " + str(e))
            #self.log.closeLog()
            #sys.exit(9)


    def clickElementByValue(self, fieldsetId, text):
        try:
            self.log.writeToLog("Click element with fieldset id: " + str(id) + ", with value of: " + text)
            xpathStr = "//fieldset[@id = \"" + fieldsetId + "\"]/div/div/label/input[@value=\"" + text + "\"]"
        
            control = self.browser.find_element_by_xpath(xpathStr)
            control.click()
        except Exception as e:
            self.log.writeToLog("Exception clicking element with value field: " + str(e))
            #self.log.closeLog()
            #sys.exit(9)


    def clickButtonText(self, text):

        try:
            self.log.writeToLog("Clicking Button with text: " + text)
            xpathStr = "//button[text() = \"" + text + "\"]"
            control = self.browser.find_element_by_xpath(xpathStr)
            control.click()
        except Exception as e:
            self.log.writeToLog("Exception clicking button text: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def clickButtonId(self, id):

        try:
            self.log.writeToLog("Clicking Button with id: " + id)
            control = self.browser.find_element_by_id(id)
            control.click()
        except Exception as e:
            self.log.writeToLog("Exception clicking button id: " + str(e))
            self.log.closeLog()
            sys.exit(9)


    def clickDwellBtn(self, id, text):

        try:    
            self.log.writeToLog("Clicking dwelling button fieldset id: " + str(id) + ", Text: " + text)
            xpathStr = "//fieldset[@id = \"" + id + "\"]/div/button[text() = \"" + text + "\"]"
            control = self.browser.find_element_by_xpath(xpathStr)
            control.click()
        except Exception as e:
            self.log.writeToLog("Exception clicking dwelling button: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def sendText(self, id, text):

        try:
            self.log.writeToLog("Sending text to fieldset id: " + str(id) + ", Text: " + text)
            xpathStr = "//fieldset[@id = \"" + id + "\"]/div/input"
            control = self.browser.find_element_by_xpath(xpathStr)
            control.send_keys(text)
        except Exception as e:
            self.log.writeToLog("Exception sending text to field: " + str(e))
            #self.log.closeLog()
            #sys.exit(9)
        

    def sendTextToElement(self,id,text):

        try:
            self.log.writeToLog("Sending text to element id: " + str(id) + ", Text: " + text)
            self.browser.find_element_by_id(id).send_keys(text)
        except Exception as e:
            self.log.writeToLog("Exception sending text to element: " + str(e))
            #self.log.closeLog()
            #sys.exit(9)

    def enterAccessCode(self, accessCode):

        # Wait for access code page to be present
        ret = self.pageLoad(5,30,'//div/label[contains(text(),"Enter your access code")]')

        if (ret == 9):
            self.log.writeToLog("Error: Enter access code screen not present")
            self.log.closeLog()
            sys.exit(9)

        self.log.writeToLog("Entering access code: " + str(accessCode))
        self.sendTextToElement("Form_UniqueCodeForm_uniqueCode_0",accessCode[0:3])
        self.sendTextToElement("Form_UniqueCodeForm_uniqueCode_1",accessCode[3:6])
        self.sendTextToElement("Form_UniqueCodeForm_uniqueCode_2",accessCode[6:9])
        self.sendTextToElement("Form_UniqueCodeForm_uniqueCode_3",accessCode[9:12])
        time.sleep(1)

        # Click Start button
        self.clickButtonId("Form_UniqueCodeForm_action_doValidateCode")

    def checkCleanResponse(self):
        
        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//div/h1[contains(text(),"Set up your household")]')
        if (ret == 9):
            self.log.writeToLog("Note: Set-up household screen not present - trying next access Code")
        else:
            checkAddressAssignHidden = self.isFieldHidden("fieldwrapper-census_night_address_confirm")
            if (checkAddressAssignHidden == True):
                log.writeToLog("Note: Pre-allocated address not present - trying next access code")
                return False
            else:
                return True

    def enterHouseholdSummary(self):

        self.clickElement("fieldwrapper-census_night_address_confirm",True,"yes")

        # Add person
        self.addPerson(1, "John Norman", "Smith", 37, "")
        self.addPerson(2, "Sarah Kim", "Smith", 37, "wife, husband, partner or de facto")
        self.addPerson(3, "Katie Mackenzie", "Smith", 9, "son or daughter")
        self.addPerson(4, "Hannah Sophie", "Smith", 6, "son or daughter")
        self.addPerson(5, "Michael Flynn", "Smith", 3, "son or daughter")
        self.clickElement("fieldwrapper-any_visitors",True,"no")
        self.clickElement("fieldwrapper-any_away",True,"no")
        self.clickButtonText("Continue")


        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//div/p[contains(text(),"Please double check everything is correct")]')
        if (ret == 9):
            self.log.writeToLog("Error: Confirmation screen not present")
            self.log.closeLog()
            sys.exit(9)

        self.clickButtonText("Submit")

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//div/h2[contains(text(),"Household Summary for")]')

        if (ret == 9):
            self.log.writeToLog("Error: Household summary screen not present")
            self.log.closeLog()
            sys.exit(9)

    def startDwellingForm(self):
        
        dwellingBtn = self.browser.find_element_by_xpath('//tr[@class = "dwelling"]/td/button[text() = "Start Form"]')
        dwellingBtn.click()

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-dwelling_description"]')
        if (ret == 9):
            self.log.writeToLog("Error: Dwelling Section 1 Form not present")
            self.log.closeLog()
            sys.exit(9)

    def enterDwellFormPage1(self):
                
        self.clickElement("fieldwrapper-dwelling_description_predefined", True, "house")
        self.clickElement("fieldwrapper-joined", True, "no")
        self.clickElement("fieldwrapper-storeys", False, "one storey")
        self.clickElement("fieldwrapper-own_dwelling", False, "own or partly own this dwelling")
        self.clickElement("fieldwrapper-mortgage_payments", True, "no")
        self.clickButtonText("Continue")
                
        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-rooms"]')
        if (ret == 9):
            self.log.writeToLog("Error: Dwelling Section 2 Form not present")
            self.log.closeLog()
            sys.exit(9)

    def enterDwellFormPage2(self):
        self.clickDwellBtn("fieldwrapper-room_kitchen","+")
        self.clickDwellBtn("fieldwrapper-room_living","+")
        self.clickDwellBtn("fieldwrapper-room_dining","+")
        self.clickDwellBtn("fieldwrapper-room_bedroom","+")
        self.clickDwellBtn("fieldwrapper-room_conservatory","+")
        self.clickDwellBtn("fieldwrapper-room_study","+")
        self.clickElement("fieldwrapper-heating_predefined",False,"fixed gas heater")
        self.clickElement("fieldwrapper-telecommunications",False,"Internet access")
        self.clickElement("fieldwrapper-vehicle_num",True,"two")
        self.clickElement("fieldwrapper-dwelling_damp",True,"no")
        self.clickElement("fieldwrapper-mould",True,"yes - sometimes")
        self.clickElement("fieldwrapper-amenities",False,"kitchen sink")
        self.clickElement("fieldwrapper-declaration",False,"Yes, I declare")
        self.clickButtonText("Submit")
                
        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//div/h2[contains(text(),"Household Summary for")]')

        if (ret == 9):
            self.log.writeToLog("Error: Household summary screen not present")
            self.log.closeLog()
            sys.exit(9)


    def startPersonForm(self):
        
        personBtn = self.browser.find_element_by_xpath('//tr[@class = "person person-type-Resident"]/td/button[text() = "Start Form"]')
        personBtn.click()
                
        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-hsp_confirm_name"]')
        if (ret == 9):
            self.log.writeToLog("Error: Person Section 1 Form not present")
            self.log.closeLog()
            sys.exit(9)

    def enterPersonFormPage1(self):
        
        self.clickElement("fieldwrapper-hsp_confirm_name",True,"yes")
        self.sendText("fieldwrapper-dob_day","01")
        self.sendText("fieldwrapper-dob_month","01")
        self.sendText("fieldwrapper-dob_year","1978")
        self.clickElement("fieldwrapper-sex",True,"male")
        self.clickElement("fieldwrapper-ur_confirm_address",True,"yes")
        self.sendText("fieldwrapper-years_at_ur_address_text","2")
        self.clickElement("fieldwrapper-ethnicity_predefined",False,"New Zealand")
        self.clickElement("fieldwrapper-country_birth_predefined",True,"New Zealand")
        self.clickButtonText("Continue")

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-maori_descent"]')
        if (ret == 9):
            self.log.writeToLog("Error: Person Section 2 Form not present")
            self.log.closeLog()
            sys.exit(9)


    def enterPersonFormPage2(self):

        self.clickElement("fieldwrapper-maori_descent",True,"no")
        #Special case
        self.clickElementByValue("fieldwrapper-address_predefined","ur_address")
        self.clickElement("fieldwrapper-languages",True,"English")
        self.clickElement("fieldwrapper-religion_predefined",True,"Christianity")
        self.sendText("fieldwrapper-religion_denomination","Catholic")
        self.clickElement("fieldwrapper-live_with_predefined",False,"my wife or husband")
        self.clickElement("fieldwrapper-study",False,"no")
        self.clickElement("fieldwrapper-difficulty_seeing",False,"no")
        self.clickElement("fieldwrapper-difficulty_hearing",False,"no")
        self.clickElement("fieldwrapper-difficulty_walking",False,"no")
        self.clickElement("fieldwrapper-difficulty_remembering",False,"no")
        self.clickElement("fieldwrapper-difficulty_washing",False,"no")
        self.clickElement("fieldwrapper-difficulty_communicating",False,"no")
        self.clickButtonText("Continue")

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-smoking"]')
        if (ret == 9):
            self.log.writeToLog("Error: Person Section 3 Form not present")
            self.log.closeLog()
            sys.exit(9)


    def enterPersonFormPage3(self):

        self.clickElement("fieldwrapper-smoking",True,"no")
        self.clickElement("fieldwrapper-used_to_smoke",True,"no")
        self.clickElement("fieldwrapper-legal_marital_status",False,"I am legally married")
        self.clickElement("fieldwrapper-own_dwelling",False,"own or partly own it")
        self.clickElement("fieldwrapper-highest_school_qualification_predefined",False,"NZ Higher School Certificate")
        self.clickElement("fieldwrapper-other_completed_qualification",True,"yes")
        self.clickElement("fieldwrapper-highest_qualification_predefined",False,"Bachelor Degree")
        self.sendText("fieldwrapper-highest_qualification_subject","Statistics")
        self.clickElement("fieldwrapper-highest_qualification_location",True,"New Zealand")
        self.clickElement("fieldwrapper-income_source",False,"wages")
        self.clickElement("fieldwrapper-total_personal_income",False,"$70,001")
        self.clickButtonText("Continue")

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//fieldset[@id = "fieldwrapper-work_in_ref_week"]')
        if (ret == 9):
            self.log.writeToLog("Error: Person Section 4 Form not present")
            self.log.closeLog()
            sys.exit(9)


    def enterPersonFormPage4(self):

        self.clickElement("fieldwrapper-work_in_ref_week",False,"I worked for pay")
        self.sendText("fieldwrapper-hours_worked","40")
        self.clickElement("fieldwrapper-employment_status",False,"a paid employee")
        self.sendText("fieldwrapper-occupation","Labourer")
        self.sendText("fieldwrapper-business_name","Jo's labourers")
        self.sendText("fieldwrapper-business_main_activity","Labour Hire")
        self.clickElement("fieldwrapper-work_place_address",False,"work away from home")
        self.sendText("fieldwrapper-work_place_address_text","120 Hereford St, Christchurch")
        self.clickElement("fieldwrapper-travel_to_work",False,"drive a private car")
        self.clickElement("fieldwrapper-unpaid_activities",False,"looked after a child who is a member")
        self.sendText("fieldwrapper-phone_number","0271234567")
        self.clickElement("fieldwrapper-declaration",False,"Yes, I declare")
        self.clickButtonText("Submit")

        # Wait for next page to be present
        ret = self.pageLoad(5,30,'//div/h2[contains(text(),"Household Summary for")]')

        if (ret == 9):
            self.log.writeToLog("Error: Household summary screen not present")
            self.log.closeLog()
            sys.exit(9)
    

    def closeBrowser(self):
        self.browser.quit()

class SalesForceAPI:
    def __init__(self, log):
        self.log = log
        self.sf = Salesforce(username='ben.schluter@stats.govt.nz.regression', password='sophie22',
                security_token='XFBTDkhKpVxNXBZ4na81RHxS', sandbox=True)


    def getDacRecords(self):
        #'Id','Name','Access_Code__c','Allocation_Status__c','Document_ID__c','For_Print__c','Is_Non_Private_Dwelling__c','Response__c'
        dacQuery = self.sf.query("\
            SELECT id, Name, access_code__c, allocation_status__c, document_id__c, for_print__c,\
                is_non_private_dwelling__c, response__c \
            FROM DAC_store__c \
            WHERE allocation_status__c = 'Allocated' \
            AND is_non_private_dwelling__c = False" \
            )

        return (dacQuery['records'])


    def getResponse(self, responseId):
        respQuery = self.sf.query_all("\
        SELECT id, name, access_code__c, address__c, address_id__c, collection_code__c, \
            collection_instance__c, collection_mode__c, document_number__c, \
            number_of_dwelling_forms_received__c, number_of_individual_forms_received__c, \
            number_of_occupants__c, Number_of_Individual_Responses_Expected__c,\
            Number_of_Outstanding_Individual_Forms__c, Number_of_Paper_Dwelling_Forms__c, \
            Number_of_Paper_Individual_Forms__c, Mark_In__c \
        FROM Response__c \
        WHERE id = '" + responseId + "'")

        return (respQuery['records'])


    def getResponseFromAccessCode(self, accessCode):
        
        respQuery = self.sf.query_all("\
        SELECT id, name, access_code__c, address__c, address_id__c, collection_code__c, \
            collection_instance__c, collection_mode__c, document_number__c, \
            number_of_dwelling_forms_received__c, number_of_individual_forms_received__c, \
            number_of_occupants__c, Number_of_Individual_Responses_Expected__c,\
            Number_of_Outstanding_Individual_Forms__c, Number_of_Paper_Dwelling_Forms__c, \
            Number_of_Paper_Individual_Forms__c, Mark_In__c \
        FROM Response__c \
        WHERE access_code__c = '" + accessCode + "'")

        return (respQuery['records'])
    

    def checkValidResponse(self, respRecords):

        noRespRecords = len(respRecords)

        if (noRespRecords != 1):
            self.log.writeToLog("More than one response store record found - moving onto next record")
            return False    

        noDwellForms = respRecords[0]['Number_of_Dwelling_Forms_Received__c']
        noIndForms = respRecords[0]['Number_of_Individual_Forms_Received__c']
        noOccs = respRecords[0]['Number_of_Occupants__c']
        noIndExpect = respRecords[0]['Number_of_Individual_Responses_Expected__c']
        noOutstandInd = respRecords[0]['Number_of_Outstanding_Individual_Forms__c']
        noPaperDwell = respRecords[0]['Number_of_Paper_Dwelling_Forms__c']
        noPaperInd = respRecords[0]['Number_of_Paper_Individual_Forms__c']
        markIn = respRecords[0]['Mark_In__c']
        accessCode = respRecords[0]['Access_Code__c']
        collectionInstance = respRecords[0]['Collection_Instance__c']

        self.log.writeToLog("Response Store, noDwellForms: " + str(noDwellForms) + ", noIndForms: " + str(noIndForms) + ", noOccs: " + str(noOccs) +
                    ", noIndExpect: " + str(noIndExpect) + ", noOutstandInd: " + str(noOutstandInd) + ", noPaperDwell: " + str(noPaperDwell) +
                    ", noPaperInd: " + str(noPaperInd) + ", markIn: " + str(markIn) + ", accessCode: " + str(accessCode) + ", collectionInstance: " + str(collectionInstance))

        # Check it has not been used
        if (accessCode == dacAccessCode and collectionInstance == "a03P0000004VCiAIAW" and markIn == False
            and (noDwellForms is None or noDwellForms == 0)
            and (noIndForms is None or noIndForms == 0)
            and (noOccs is None or noOccs == 0)
            and (noIndExpect is None or noIndExpect == 0)
            and (noOutstandInd is None or noOutstandInd == 0)
            and (noPaperDwell is None or noPaperDwell == 0)
            and (noPaperInd is None or noPaperInd == 0)):

            return True
        else:
            return False

    def convertInt(self, str):
        value = 0
        try:
            value = int(str)
        except:
            value = 0
        return value
            

    def performSFChecks(self, respRecords):

        self.log.writeToLog("Checking Sales Force Reponse")

        totalForms = len(respRecords)
        if (totalForms != 1):
            self.log.writeToLog("Error - Expected ones SF response record for access code, have: " + str(totalForms) + "\n" + str(respRecords))

        noDwellForms = self.convertInt(respRecords[0]['Number_of_Dwelling_Forms_Received__c'])
        if (noDwellForms != 1):
            self.log.writeToLog("Error - SF: Do not have 1 dwelling form received as expected, have: " + str(noDwellForms) + "\n" + str(respRecords))

        noIndForms = self.convertInt(respRecords[0]['Number_of_Individual_Forms_Received__c'])            
        if (noIndForms != 1):
            self.log.writeToLog("Error - SF: Do not have 1 individual form received as expected, have: " + str(noIndForms) + "\n" + str(respRecords))

        noOccs = self.convertInt(respRecords[0]['Number_of_Occupants__c'])
        if (noOccs != 5):
            self.log.writeToLog("Error - SF: Do not have 5 occupants as expected, have: " + str(noOccs) + "\n" + str(respRecords))
               
        noOutstandInd = self.convertInt(respRecords[0]['Number_of_Outstanding_Individual_Forms__c'])
        if (noOutstandInd != 4):
            self.log.writeToLog("Error - SF: Do not have 4 individual responses expected, have: " + str(noOutstandInd) + "\n" + str(respRecords))

        noPaperDwell = self.convertInt(respRecords[0]['Number_of_Paper_Dwelling_Forms__c'])
        if (noPaperDwell != 0):
            self.log.writeToLog("Error - SF: Unexpectedly have paper dwelling form: " + str(noPaperDwell) + "\n" + str(respRecords))

        noPaperInd = self.convertInt(respRecords[0]['Number_of_Paper_Individual_Forms__c'])
        if (noPaperInd != 0):
            self.log.writeToLog("Error - SF: Unexpectedly have paper individual form: " + str(noPaperInd) + "\n" + str(respRecords))

        markIn = respRecords[0]['Mark_In__c']
        if (markIn != True):
            self.log.writeToLog("Error - SF: Not markedin, stats is: " + str(markIn) + "\n" + str(respRecords))


class Database:
    def __init__(self, log):
        self.log = log
        self.con = None
        self.cur = None

    def connect(self, database):

        try:
            connectString = "DRIVER={SQL Server};SERVER=wuatclsqlcorp10.stats.govt.nz;DATABASE=" + database + ";"
            self.log.writeToLog("Connecting to DB: " + connectString)
            self.con = pypyodbc.connect(connectString)
        except Exception as e:
            self.log.writeToLog("Exception connecting to DB: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def query(self, sql):

        try:
            self.cur = self.con.cursor()
            self.cur.execute(sql)

            self.columns = [column[0] for column in self.cur.description]
            self.results = []
            for row in self.cur.fetchall():
                self.results.append(dict(zip(self.columns, row)))

            self.cur.close()
        except Exception as e:
            self.log.writeToLog("Exception querying DB:, SQL = " + sql + "\nError: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def performMarkinChecks(self):

        self.log.writeToLog("Checking Markin table")

        totalForms = len(self.results)
        if (totalForms != 5):
            self.log.writeToLog("Error - Markin: Expecting 5 entries in markin database, have: " + str(totalForms) + "\n" + str(self.results))

        noHouseholdForms = 0
        noDwellingForms = 0
        noIndForms = 0

        for iter in range(len(self.results)):
            formType = self.results[iter]['formtypecode']
            markedIn = self.results[iter]['salesforcemarkinstatuscode']
            noOccs = self.results[iter]['numberofoccupants'] 

            if (formType == "household"):
                noHouseholdForms += 1
            elif (formType == "dwl"):
                noDwellingForms += 1
            elif (formType == "ind"):
                noIndForms += 1

            if (markedIn != "markedIn"):
                self.log.writeToLog("Error - Markin: Record is not marked in, status is: " + markedIn + "\n" + str(self.results[iter]))

            if (formType == "household" and noOccs != 5):
                self.log.writeToLog("Error - Markin: Household is not set to 5 occupants, is set to: " + str(noOccs) + "\n" + str(self.results[iter]))
                               
        if (noHouseholdForms != 3):
            self.log.writeToLog("Error - Markin: Do not have 3 household form markin records as expected, have: " + str(noHouseholdForms) + "\n" + str(self.results))
                     
        if (noDwellingForms != 1):
            self.log.writeToLog("Error - Markin: Do not have 1 dwelling form markin record as expected, have: " + str(noDwellingForms) + "\n" + str(self.results))

        if (noIndForms != 1):
            self.log.writeToLog("Error - Markin: Do not have 1 individual form markin record as expected, have: " + str(noIndForms) + "\n" + str(self.results))


    def performResponseStoreChecks(self):

        self.log.writeToLog("Checking Response Store Table")
        totalForms = len(self.results)
        if (totalForms != 5):
            self.log.writeToLog("Error - Reponse Store: Expecting 5 entries in reponse store, have: " + str(totalForms) + "\n" + str(self.results))

        noHouseholdForms = 0
        noDwellingForms = 0
        noIndForms = 0

        for iter in range(len(self.results)):
            instrumentCode = self.results[iter]['instrument_code']
            
            if (instrumentCode == "CEN2018CT2017_Online_Household"):
                noHouseholdForms += 1
            elif (instrumentCode == "CEN2018CT2017_Online_Dwelling"):
                noDwellingForms += 1
            elif (instrumentCode == "CEN2018CT2017_Online_Individual"):
                noIndForms += 1

                               
        if (noHouseholdForms != 3):
            self.log.writeToLog("Error - Response Store: Do not have 3 household form records as expected, have: " + str(noHouseholdForms) + "\n" + str(self.results))
                     
        if (noDwellingForms != 1):
            self.log.writeToLog("Error - Response Store: Do not have 1 dwelling form record as expected, have: " + str(noDwellingForms) + "\n" + str(self.results))

        if (noIndForms != 1):
            self.log.writeToLog("Error - Response Store: Do not have 1 individual form record as expected, have: " + str(noIndForms) + "\n" + str(self.results))


    def disconnect(self):
        self.con.close()



###################
# Main class
###################

if __name__ == "__main__":

    currUser = os.getlogin()
    outputLog = "C:\\Users\\" + currUser + "\\"

    log = Logger("ICS_selenium_log",outputLog)
    sf = SalesForceAPI(log)
    webEntry = WebEntry(log)

    # Retrieve 2000 records from the DAC store for Access codes
    dacRecords = sf.getDacRecords()
    iter = 0
    dacAccessCode = ""

    # Go through the DAC codes randomly, finding one which has not been used for ICS or scanning
    while (True):
        iter = iter + 1
        log.writeToLog("Using DAC store entry number: " + str(iter))
        # Give up if we haven't found one within the first 2000
        if (iter > 2000):
            log.writeToLog("Can't find a valid access code - giving up")
            log.closeLog()
            sys.exit(9)
        # Select a random code
        i = random.randint(0, len(dacRecords) - 1)

        responseId = dacRecords[i]['Response__c']
        dacAccessCode = dacRecords[i]['Access_Code__c']
        log.writeToLog("DAC Store - Response Id: " + str(responseId) + ", Access Code: " + str(dacAccessCode))
        
        # Retrieve the response data from SF for this access code
        respRecords = sf.getResponse(responseId)

        isValidResponse = sf.checkValidResponse(respRecords)
        # Check it has not been used
        if (isValidResponse):

            log.writeToLog("Opening ICS site")
            # Open up browser
            webEntry.navigate("https://onlinecensus-uat.cwp.govt.nz/census-test/landing/")
            webEntry.enterAccessCode(dacAccessCode)

            isCleanResponse = webEntry.checkCleanResponse()

            if (isCleanResponse):
                log.writeToLog("Access Code is a valid free one to use - proceeding")
                break
            
    webEntry.enterHouseholdSummary()
    webEntry.startDwellingForm()
    webEntry.enterDwellFormPage1()
    webEntry.enterDwellFormPage2()
    webEntry.startPersonForm()
    webEntry.enterPersonFormPage1()
    webEntry.enterPersonFormPage2()
    webEntry.enterPersonFormPage3()
    webEntry.enterPersonFormPage4()

    # Sleep for 6 mins
    #time.sleep(360)


    db1 = Database(log)
    db1.connect("StatsNZ_ECP_Markin")
    db1.query("select * from StatsNZ_ECP_Markin.dbo.CensusMarkinStatus where accessCode = '" + dacAccessCode + "'")
    db1.performMarkinChecks()
    db1.disconnect()

    db2 = Database(log)
    db2.connect("StatsNZ_Epl_ResponseStore")
    db2.query("select * from StatsNZ_Epl_ResponseStore.data.response_data where questionnaire_id = '" + dacAccessCode + "'")
    db2.performResponseStoreChecks()
    db2.disconnect()

    respRecords = sf.getResponseFromAccessCode(dacAccessCode)
    sf.performSFChecks(respRecords)

    log.closeLog()
    #webEntry.closeBrowser()

    sys.exit(0)
