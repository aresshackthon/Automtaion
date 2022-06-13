
import openpyxl 
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from selenium.common.exceptions import StaleElementReferenceException
from datetime import date
import time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
# import os
# from glob import glob
import os, glob
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
import send_email
today = date.today()
#======================================================================================
#Mail Credential

#======================================================================================
ds_usa_url = 'https://www.linkedin.com/login'
chromeoptions = webdriver.ChromeOptions()


chromeoptions.add_argument("--no-sandbox")
chromeoptions.add_argument('--disable-dev-shm-usage')
chromeoptions.add_argument('user-agent=ua.chrome()')

chromeoptions.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')

driver = webdriver.Chrome(ChromeDriverManager().install(),  options=chromeoptions)
driver.maximize_window()
try:
    time.sleep(2)
    ds_usa_url = 'https://www.linkedin.com/login'
    driver.get(ds_usa_url)
    time.sleep(2)
    user = driver.find_element_by_id('username').send_keys('shoebahmed370@gmail.com')
    time.sleep(2)
    pwd = driver.find_element_by_id('password').send_keys('yasmeen1878')
    # user = driver.find_element_by_id('username').send_keys('automatedmailreport@gmail.com')
    # pwd = driver.find_element_by_id('password').send_keys('Aress123!#')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
    time.sleep(2)
except: 
    pass
       

driver.get("https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=artificial%20intelligence&location=United%20States")
time.sleep(5)
# print("Now you can open link: http://localhost:50026/")

# driver.get(ds_usa_url)
# user = driver.find_element_by_id('username').send_keys('automatedmailreport@gmail.com')
# pwd = driver.find_element_by_id('password').send_keys('Aress123!#')
# driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
# time.sleep(2)

# =============================================================================
#               Date Conversion
# =============================================================================
def date_conv(l):
    k = re.findall(r'\d+\s\w+',l)[0].split(' ')
    if k[1] in ['hours','hour']:
        dd_ = datetime.now() - relativedelta(hours=int(k[0]))
    elif k[1] in ['months','month']:
       dd_ = datetime.now() - relativedelta(months=int(k[0]))
    elif k[1] in ['years','year']:
       dd_ = datetime.now() - relativedelta(years=int(k[0]))
    elif k[1] in ['days','day']:
       dd_ = datetime.now() - relativedelta(days=int(k[0]))
    elif k[1] in ['weeks','week']:
       dd_ = datetime.now() - relativedelta(weeks=int(k[0]))
    elif k[1] in ['minutes','minute']:
       dd_ = datetime.now() - relativedelta(minutes=int(k[0]))
    val = dd_.strftime("%d-%m-%Y")
    return val
#===================================================================================
#Mail Setup
#===================================================================================


# =============================================================================
#       Select the filter
# # =============================================================================

# def make_clickable(val):
#     return '<a href="{}">{}</a>'.format(val,val)



def extract_data(domain_name,location,driver,duration):

    wait = WebDriverWait(driver, 25)
    try:
        print("Execution start")

# #jobs-search-box-keyword-id-ember354 /html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]
        time.sleep(5)
        # JOB SEARCH INPUT FIELD
        driver.find_element_by_xpath("//input[@aria-label='Search by title, skill, or company']").clear()
        driver.find_element_by_xpath("//input[@aria-label='Search by title, skill, or company']").send_keys(domain_name)#("UiPath")#
        # LOCATION SEARCH INPUT
        driver.find_element_by_xpath("//input[@aria-label='City, state, or zip code']").clear()
        driver.find_element_by_xpath("//input[@aria-label='City, state, or zip code']").send_keys(location)#("India")#
        time.sleep(5)
        #COLLECTION SEARCH BAR WHICH CONTAIN SEARCH BUTTON
        search_box = driver.find_element_by_class_name('jobs-search-box')
        search_box.find_element_by_tag_name('button').click()
        time.sleep(5)
        #COLLECTION OF NAV BAR WHICH CONTAIN DATE POSTED FILTER
        filter_box = driver.find_element_by_xpath("//section[@aria-label='search filters']")
        #COLLECTION OF DATE FILTER STATUS
        time_filter = filter_box.text.split('\n')[2]
        if time_filter == 'Date Posted':
            arial_time = 'Date Posted filter. Clicking this button displays all Date Posted filter options.'
            filter_box.find_element_by_xpath(f"//button[@aria-label='{arial_time}']").click()
        elif time_filter == "Past Month":
            arial_time = 'Date Posted filter. Past Month filter is currently applied. Clicking this button displays all Date Posted filter options.'
            filter_box.find_element_by_xpath(f"//button[@aria-label='{arial_time}']").click()
        elif time_filter == 'Past Week':
            arial_time = "Date Posted filter. Past Week filter is currently applied. Clicking this button displays all Date Posted filter options."
            filter_box.find_element_by_xpath(f"//button[@aria-label='{arial_time}']").click()
        elif time_filter == "Past 24 hours":
            arial_time = "Date Posted filter. Past 24 hours filter is currently applied. Clicking this button displays all Date Posted filter options."
            filter_box.find_element_by_xpath(f"//button[@aria-label='{arial_time}']").click()
        #COLLECTION OF TIME FILTER OPTIONS
        store = driver.find_element_by_id('hoverable-outlet-date-posted-filter-value')
        time.sleep(2)
        # duration =1
        if duration == 0:
            #PAST 24 HOURS
            store.find_element_by_xpath("//*[text()='Past 24 hours']").click()
        elif duration == 1:
            #PAST WEEK
            store.find_element_by_xpath("//*[text()='Past Week']").click()
        elif duration == 2:
            #PAST MONTH
            store.find_element_by_xpath("//*[text()='Past Month']").click()
        
        # TIME FILTER OKAY BUTTON
        store.find_element_by_xpath("//button[@data-control-name='filter_show_results']").click()
        
        

    
        loc_list=[];company_list=[];job_title_list=[];state=[];jobs_desc_list=[];date_time_list=[]
        current_url=[];senior=[];emp_type=[];ind=[]
     # initialize lists
        seniority_level = ['Internship','Entry level','Associate','Mid-Senior level','Director','Executive']
        empl_type =['Full-time','Part-time','Contract','Temporary','Volunteer','Internship','Other']
        
        # wait = WebDriverWait(driver, 25)
        time.sleep(5)
        for i in range(0,10):
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          # to scroll at first position
            
        # try: 
        #     time.sleep(5)
            
        #     # page_num = int(page_num.split('\n')[-1])
        #     # if  page_num>=7:
        #     #     page_num=7
        # except Exception as e:
        #     page_num = 2
        #     # print("page capturing error as ........",e)

    
        list_items = driver.find_elements_by_class_name("occludable-update")
        page_num = 5
        flags = False;flags_2=False
        # move through pages page_num+1
        # for page_num_i in range(2,page_num+1):
        for page_num_i in range(2,page_num+1):
    
            list_items = driver.find_elements_by_class_name("occludable-update")
                    
    
            time.sleep(2)
                        
            for job in list_items:
                
            # to scroll the div into view
         
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", job)
                time.sleep(2)
                job.click()
                time.sleep(2)
                try:
                    link = driver.find_element_by_class_name('jobs-unified-top-card__content--two-pane')
                except:
                    
                    flags = True
                    driver.back()
                    break
     
                try:
                    type_job = link.text.split('\n')[2]
                    type_job = type_job.split(' · ')
                    s = type_job[-1]
                  
                    e = type_job[0]
                    if s in seniority_level: pass
                    else: s= "Not Present"
                    
                    if e in empl_type: pass
                    else: e= "Not Present"
                    
             
                 
                    
                    type_job = link.text.split('\n')[3].split(' · ')
                    ind1 = type_job[-1]
                    if 'employees' not in ind1: pass
                    else:ind1= "Not Present"
                    
                    
                    time.sleep(1)
                    a=link.find_element_by_tag_name('a').get_attribute('href')
                    time.sleep(2)
                    d = job.find_element_by_tag_name('time').get_attribute('datetime')
                   
                    time.sleep(1)
                    details = driver.find_element_by_id("job-details").text
                    time.sleep(1)
                    [position, company, location_temp] = job.text.split('\n')[:3]
                except:
                    driver.back()
                    
                    break
                
                
                senior.append(s)
                emp_type.append(e)
                ind.append(ind1)
                current_url.append(a)
                date_time_list.append(d)            
                
                
             
    
                job_title_list.append(position)
                loc_list.append(location_temp)
                company_list.append(company)
                jobs_desc_list.append(details)
    
            if flags == True: break
            #if flags_2 == True: break
            time.sleep(20)
            try:
                for i in range(0,10):
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # wait.until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Page {page_num_i}"]'))).click()
                driver.find_element_by_xpath(f"//button[@aria-label='Page {page_num_i}']").click()
                print(f"page number {page_num_i} is executed properly")
                # page_num_c = driver.find_element_by_xpath("//section[@aria-label='pagination']").text
                # print("Page number capture sucessfully",page_num_c) 

            except Exception as e:
                print(f"page number {page_num_i} is halted an error")
                print("Error in page number selections as ----->",e)
                break
    
        # extract city frim location list
        
        city = [x.split(',')[0] for x in loc_list]
        
        # extract state from lication list 
        for loc in loc_list:
            try:
                s= loc.split(',')[1]
                state.append(s)
            except:
                state.append("Not Present")
                pass
        
                
        # create dataframe frame
        main_data = pd.DataFrame({"Domain Name": domain_name.title() ,'Job Title':job_title_list,'Page Link':current_url,
                               "Company":company_list,'City':city,'State':state,'Country':location,
                               "Posted Date":date_time_list,'Job Description': jobs_desc_list,
                               'Seniority level':senior,'Employment type':emp_type,
                               'Industries':ind})
         
        #main_data.to_csv("Linkedin_Job_Today.csv", index = False)
        
        date_time=datetime.now()
        time_diff=timedelta(days=15,hours=0,minutes=0)
        req_date_time=date_time-time_diff
        req_date_time=req_date_time.strftime('%Y-%m-%d')
        
        temp_scrap_data = main_data.copy()
        
        filtered_df = temp_scrap_data.loc[(temp_scrap_data['Posted Date'].astype('str') >= req_date_time)]
        filtered_df=filtered_df.sort_values(by='Posted Date',ascending=False)
       
        
        #filtered_df.to_csv("Linkedin_Job_Today_temp.csv", index = False)
        return filtered_df
    except Exception as e:
        print(f"NO DATA IS FOUND FOR domain_name-> {domain_name} and locations-> {location}")
        columns_name = ['Job Title','Page Link',"Company",'City','State','Country',"Posted Date",'Job Description',
        'Seniority level','Employment type','Industries']
        main_data = pd.DataFrame(columns= columns_name)
        print("The Error is --->>", e)
        pass                    
    
        return main_data

def linkedin_output():
    domain_name_list = []
    with open('domain.txt') as f:
        for dom in f:
            if dom:
                dom = dom[:-1].replace(',','')
                domain_name_list.append(dom)
    location_list = []
    with open('locations_list.txt') as f:
        for loc in f:
            if loc:
                loc = loc[:-1].replace(',','')
            location_list.append(loc)
    locations = location_list;all_dd = pd.DataFrame()
#     column_names = ["'Job Title'", "Page Link", "Company","City","State","Country","Posted Date","Job Description","Seniority level","Employment type","Industries"]
#     all_dd = pd.DataFrame(columns = column_names)
    all_dd = pd.DataFrame()
    duration =1
    for location in locations:
        for domain_name in domain_name_list:
            dd = extract_data(domain_name,location,driver,duration)
            all_dd = all_dd.append(dd,ignore_index = True)
    curr = os.getcwd()
    
     
    dir_data = curr+'\\Linked_in_job_output'
    filelist = glob.glob(os.path.join(dir_data, "*"))
    for f in filelist:
        os.remove(f)
        
        # all_dd.to_excel(os.getcwd()+"//Linkedin_data//"+f"""Output//Linked_in_{domain_name.replace(" ","_")}_{location.replace(" ","_")}.xlsx""",encoding='utf-8-sig',index=False)
    #ff_data = pd.DataFrame()
    #print(all_dd.head())
    # for i in all_dd:
        # ff_data = ff_data.append(i,sort=False)
    curr = os.getcwd()
    if not os.path.exists(curr+'\\Linked_in_job_output'):
        # os.chdir(curr)
        os.makedirs(curr+'\\Linked_in_job_output')
    save_dir = curr+'\\Linked_in_job_output'
    os.chdir(save_dir)
    save_file_name =  'Linkedin_Job_'+today.strftime("%d_%m_%Y")+'.csv'
    all_dd.to_csv(save_file_name,index=False)
    # filename = save_dir+'\\'+save_file_name
    os.chdir(curr)
    sender_list = []
    with open('sender_list.txt') as f:
        for s_l in f:
            if s_l:
                s_l = s_l.replace(',','')
                sender_list.append(s_l.strip())
    receiver_email=''
    receiver_email = ','.join(sender_list)
    #=======================MAIL_CONTENT======
    dom_str = ""
    for ind,i in enumerate(domain_name_list):
        dom_str +=str(ind+1)+". "+i+"\n"
    
        loc_str = ""
    for ind,i in enumerate(locations):
        loc_str +=str(ind+1)+". "+i+"\n"

    mail_content = f"""Hi, \nPlease find the attachment.\n\nAttached excel data contains following Technologies:\n{dom_str.title()}
    \n and Location/s are :\n {loc_str.title()}\n\n
    Thanks and Regards
    Data Analytics Team
    """
    send_email.send_the_data(receiver_email,save_dir,save_file_name,curr,mail_content)
    driver.close()
if __name__=="__main__":
    linkedin_output()
    print("The code has been executed properly please press Ctrl+C ...............")


    # return dom,locations
   
  
    
  
    # driver.find_element_by_xpath("//button[@type='button']").click()
    
    # try:
    #     wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]'))).clear()
    #     time.sleep(2)
    #     wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]'))).send_keys(domain_name)
    # except:
    #     try:
    #         wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]'))).clear()
    #         wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]'))).send_keys(domain_name)
    #     except:
    #         try:
    #             driver.find_element_by_xpath("/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]").clear()
    #             driver.find_element_by_xpath("/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]").send_keys(domain_name)
    #         #/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]
    #         except:
    #             driver.find_element_by_xpath('/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div/input[1]').clear()
    #             driver.find_element_by_xpath('/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div/input[1]').send_keys(domain_name)
                
    # try:
    #     wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]'))).clear()
    #     time.sleep(2)
    #     wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]'))).send_keys(location)
    # except:
    #     try:
    #         wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]'))).clear()
    #         wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]'))).send_keys(location)
    #     except:
    #         try:
    #             driver.find_element_by_xpath("/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]").clear()
    #             driver.find_element_by_xpath("/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]").send_keys(location)
    #         except:
    #             driver.find_element_by_xpath("/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]").clear()
    #             driver.find_element_by_xpath("/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]").send_keys(location)                    

    
        # extract last page number from web page
       #  try:
       #      page_num=int(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-two-pane__pagination'))).text.split('\n')[-1])
       #  except Exception as e: 
       #      print("Page number error as -------->>",e)
       #      page_num=2
       # # to scroll down