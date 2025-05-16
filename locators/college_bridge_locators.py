class LandingPageLocators:
    PROGRAM_OF_INTEREST = "#poi"
    FIRST_NAME = "input[placeholder='First Name']"
    LAST_NAME = "input[placeholder='Last Name']"
    PHONE_NUMBER = "input[placeholder='Phone Number']"
    EMAIL_ADDRESS = "input[placeholder='Email Address']"
    ZIP_CODE = "input[placeholder='Zip Code']"
    GET_STARTED = "button#customSubmit"

class StartQualifyPageLocators:
    NEXT_BUTTON = "//button[@type='button'][1]"

class MindsetQualifyPageLocators:
    NOT_IMPORTANT = "//div[contains(text(),'Not important.')]"
    SOME_WHAT_IMPORTANT = "//div[contains(text(),'Somewhat important.')]"
    VERY_IMPORTANT = "//div[contains(text(),'Very important.')]"
    NEXT_BUTTON = "//footer/button[1]"
    NEXT_BUTTON_INFO = "//body/div[@id='root']/article[1]/footer[1]/button[1]"
    ENTER_YOUR_ANSWER = "//textarea[@placeholder='Enter your answer here...']"
    I_WOULD_NOT_CARE = "//div[contains(text(),'Somewhat excited.')]//preceding::div[1]"
    SOME_WHAT_EXCITED = "//div[contains(text(),'Somewhat excited.')]"
    VERY_EXCITED = "//div[contains(text(),'Very excited.')]"

class BridgeStartPageLocators:
    NEXT_BUTTON = "//footer/button[1]"

class GeneralEducationPageLocators:
    I_HAVE_PASSED_ALL_MY_GEN_ED_COURSES = "//div[contains(text(),\"I've passed all of my Gen Ed Courses.\")]"
    I_HAVE_PASSED_SOME_BUT_NOT_ALL_OF_THEM = "//div[contains(text(),\"I've passed some, but not all of them.\")]"
    I_HAVE_NOT_PASSED_ANY_GEN_EDS_YET = "//div[contains(text(),\"I haven't passed any Gen Eds yet.\")]"
    NOT_IMPORTANT = "//div[contains(text(),'Not important.')]"
    SOME_WHAT_IMPORTANT = "//div[contains(text(),'Somewhat important.')]"
    VERY_IMPORTANT = "//div[contains(text(),'Very important.')]"

class EntranceExamPageLocators:
    NEXT_BUTTON = "//footer/button[1]"
    I_HAVE_PASSED_MY_RN_ENTRANCE_EXAM = "//div[contains(text(),'I’ve passed my RN entrance exam.')]"
    I_TOOK_THE_EXAM_BUT_DID_NOT_PASS = '//div[contains(text(),"I took the exam, but didn\'t pass.")]'
    I_HAVE_NOT_TAKEN_MY_RN_ENTRANCE_EXAM = "//div[contains(text(),'I haven’t taken my RN entrance exam.')]"
    NOT_CONCERNED = "//div[contains(text(),'Not concerned.')]"
    SOMEWHAT_CONCERNED = "//div[contains(text(),'Somewhat concerned.')]"
    VERY_CONCERNED = "//div[contains(text(),'Very concerned.')]"

# class CoreNursingPageLocators:






