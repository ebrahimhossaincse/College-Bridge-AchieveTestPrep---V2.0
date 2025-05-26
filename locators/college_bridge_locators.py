class LandingPageLocators:
    PROGRAM_OF_INTEREST = "//select[@id='poi']"
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
    NEXT_BUTTON_INFO = "(//button[contains(text(),'Next')])[1]"
    ENTER_YOUR_ANSWER = "//textarea[@placeholder='Enter your answer here...']"
    I_WOULD_NOT_CARE = "//div[contains(text(),'Somewhat excited.')]//preceding::div[1]"
    SOME_WHAT_EXCITED = "//div[contains(text(),'Somewhat excited.')]"
    VERY_EXCITED = "//div[contains(text(),'Very excited.')]"

class BridgeStartPageLocators:
    NEXT_BUTTON = "(//button[contains(text(),'Next')])[1]"

class GeneralEducationPageLocators:
    NEXT_BUTTON = "(//button[contains(text(),'Next')])[1]"
    I_HAVE_PASSED_ALL_MY_GEN_ED_COURSES = "//div[contains(text(),\"I've passed all of my Gen Ed Courses.\")]"
    I_HAVE_PASSED_SOME_BUT_NOT_ALL_OF_THEM = "//div[contains(text(),\"I've passed some, but not all of them.\")]"
    I_HAVE_NOT_PASSED_ANY_GEN_EDS_YET = "//div[contains(text(),\"I haven't passed any Gen Eds yet.\")]"
    NOT_IMPORTANT = "//div[contains(text(),'Not important.')]"
    SOME_WHAT_IMPORTANT = "//div[contains(text(),'Somewhat important.')]"
    VERY_IMPORTANT = "//div[contains(text(),'Very important.')]"

class EntranceExamPageLocators:
    NEXT_BUTTON = "(//button[contains(text(),'Next')])[1]"
    I_HAVE_PASSED_MY_RN_ENTRANCE_EXAM = "//div[contains(text(),'I’ve passed my RN entrance exam.')]"
    I_TOOK_THE_EXAM_BUT_DID_NOT_PASS = '//div[contains(text(),"I took the exam, but didn\'t pass.")]'
    I_HAVE_NOT_TAKEN_MY_RN_ENTRANCE_EXAM = "//div[contains(text(),'I haven’t taken my RN entrance exam.')]"
    NOT_CONCERNED = "//div[contains(text(),'Not concerned.')]"
    SOMEWHAT_CONCERNED = "//div[contains(text(),'Somewhat concerned.')]"
    VERY_CONCERNED = "//div[contains(text(),'Very concerned.')]"

class CoreNursingPageLocators:
    NEXT_BUTTON = "//footer//button[1]"
    I_HAVE_PASSED_MY_CORE_RN_COURSES = "//div[contains(text(), 'I’ve passed my core RN courses.')]"
    I_HAVE_PASSED_SOME_BUT_NOT_ALL_OF_THEM = "//div[contains(text(), 'I’ve passed some, but not all of them.')]"
    I_HAVE_NOT_TAKEN_MY_CORE_RN_COURSES = "//div[contains(text(), 'I haven’t taken my core RN courses.')]"
    NOT_CONCERNED = "//div[contains(text(), 'Not concerned.')]"
    SOMEWHAT_CONCERNED = "//div[contains(text(), 'Somewhat concerned.')]"
    VERY_CONCERNED = "//div[contains(text(), 'Very concerned.')]"

class ExitExamPageLocators:
    NEXT_BUTTON = "//footer/button[1]"
    I_HAVE_PASSED_THE_NCLEX_RN = "//div[contains(text(),'I’ve passed the NCLEX-RN.')]"
    I_TOOK_THE_NCLEX_RN_BUT_DID_NOT_PASS_IT = "//div[contains(text(),'I took the NCLEX-RN, but didn’t pass it.')]"
    I_HAVE_NOT_TAKEN_THE_NCLEX_RN_YET = "//div[contains(text(),'I haven’t taken the NCLEX-RN yet.')]"
    NOT_CONCERNED = "//div[contains(text(),'Not concerned.')]"
    SOMEWHAT_CONCERNED = "//div[contains(text(),'Somewhat concerned.')]"
    VERY_CONCERNED = "//div[contains(text(),'Very concerned.')]"

class ConfirmContactPageLocators:
    NEXT_BUTTON = "(//button[contains(text(),'Next')])[2]"
    EMAIL_ADDRESS = "//input[@name='email']"
    PHONE_NUMBER = "//input[@name='phone']"

class ResultsPageLocators:
    NEXT_BUTTON = "//footer/button[1]"

class CollegePlanPageLocators:
    NEXT_BUTTON = "(//button[contains(text(), 'Next')])[1]"
    PLEASE_WAIT = "//button[contains(text(),'Please wait...')]"

class PreBuyOrNotPreBuyOptionsPageLocators:
    START_MY_PLAN = "(//button[contains(text(), 'Start My Plan')])[1]"
    CONTINUE_WITH_OUT_A_PLAN = "//button[contains(text(),'Continue without a plan')]"

class PreBuyCheckoutPageLocators:
    NAME_ON_CARD = "//input[@name='name']"
    CARD_NUMBER = "//input[@name='card_number']"
    EXPIRY = "//input[@name='expiry']"
    CVV = "//input[@name='cvv']"
    POSTAL_CODE = "//input[@name='postal_code']"
    EMAIL_ADDRESS = "//input[@name='email']"
    CHECKBOX = "//input[@type='checkbox']"
    PAY_NOW = "//button[@type='submit']"

class PreBuyPurchasedPageLocators:
    NEXT_BUTTON = "//footer/button[1]"
    CONGRATULATIONS_TEXT= "//span[contains(.,'You’ve taken the first step toward building an RN Bridge P')]"

class PreBuyResPageLocators:
    NEXT_BUTTON = "//footer/button[1]"
    CHAT_NOW = "(//button[contains(text(), 'Chat now')])[1]"
    SCHEDULE_A_TIME = "//button[contains(text(),'Schedule a time')]"


class ReadinessPageLocators:
    IMMEDIATELY = "//div[.=\"Immediately. I'm ready to select a plan.\"]"
    SOON = "//div[.=\"Soon. I’m ready to discuss my RN goals.\"]"
    NOT_YET = "//div[.=\"Not yet. I'd like more information.\"]"
    NEXT_BUTTON = "//footer/button[1]"

class ReadyImmediateInfoPageLocators:
    SCHEDULE_NOW = "(//button[contains(text(), 'Schedule Now')])[1]"
    HOW_OUR_STUDENTS_SUCCEED = "//button[contains(text(),'How our students succeed')]"

class ReadySoonThanksPageLocators:
    BLOG = "//a[contains(text(),'blog')]"
    FAQS = "//a[contains(text(),'FAQs')]"
    NURSING_CARRIER_PATHWAY = "//a[contains(text(),'Nursing Career Pathway')]"

class ReadyNotYetVideoPageLocators:
    NEXT_BUTTON = "//footer/button[1]"

class ReadyNotYetThanksPageLocators:
    BLOG = "//a[contains(text(),'blog')]"
    FAQS = "//a[contains(text(),'FAQs')]"
    NURSING_CARRIER_PATHWAY = "//a[contains(text(),'Nursing Career Pathway')]"
