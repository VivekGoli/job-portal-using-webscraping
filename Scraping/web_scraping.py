from typing import Any
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from threading import *
import mysql.connector
import threading

class JobThread(threading.Thread):
    def __init__(self, target, *args):
        super().__init__(target, *args)
        self.result = None

    def run(self):
        self.result = super().run()

def cisco_parser(url):
    print("Cisco started")
    response = requests.get(url)
    #read the url and create a BeautifulSoap instance
    soup = BeautifulSoup(response.content, "html.parser")
    jobs_table = soup.find("table", class_="table_basic-1") #gets the table of jobs

    links = [] # get the link for each job in cisco
    for row in jobs_table.find_all("tr"):
        anchor = row.find("a")
        if anchor:
            links.append(anchor["href"])

    jobs_list = []
    for i in range(len(links)):
        try:
            link_response = requests.get(links[i])
            link_soup = BeautifulSoup(link_response.content, "html.parser")
            job_title = link_soup.find("div", class_="section_header").find("h2", class_="title_page-1").text # gets the job title
            job_description = link_soup.find("div", class_="job_description")

            seperators = r"\||\(|,|\/"
            details = ["Cisco"]
            details.append(re.split(seperators, job_title)[0].strip())
            location = link_soup.find("li", class_="fields-data_item").text.split(":")[1].strip() # gets list of job details

            details.append(location)
            details.append(job_description.prettify())
            details.append(links[i])
            if len(details) == 5:
                jobs_list.append(details)
        except:
            pass
    jobs_dataframe = pd.DataFrame(jobs_list, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\cisco_new.csv")
    print("Cisco ended")
    return jobs_dataframe

def google_parser(url):
    print("Google started")
    def google_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        for anchor in soup.find_all("a", class_="WpHeLc"):
            links.append("https://www.google.com/about/careers/applications/" + anchor["href"])

        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")
                details = ["Google"]
                details.append(link_soup.find("h2", class_="p1N2lc").text)
                details.append(link_soup.find("span", class_="r0wTof").text)
                
                skills = link_soup.find("div", class_="KwJkGe")
                responsibilities = link_soup.find("div", class_="BDNOWe")
                description = '<div>' + skills.prettify() + responsibilities.prettify() + '</div>'
                details.append(description)
                details.append(links[i])
                jobs_list.append(details)
            except:
                pass
        return jobs_list
    
    threads = []
    jobs = []

    for i in range(1, 11):
        thread = MyThread(target=google_inner_parser, args=(url + str(i),))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        jobs = jobs + thread.result
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\google_new.csv")
    print("Google ended")
    return jobs_dataframe

def deloitte_parser(url):
    print("Deloitte started")
    def deloitte_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find(name="table")
        links = [] # get the link for each job in hp
        for item in table.find_all(name="td"):
            anchor = item.find(name="a")
            if anchor:
                links.append("https://jobsindia.deloitte.com" + anchor["href"])

        jobs_list = []
        for i in range(1, len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                details = ["Deloitte"]
                details.append(link_soup.find(name="span", attrs={"class":"rtltextaligneligible", "data-careersite-propertyid":"title"}).text.strip())
                details.append(link_soup.find(name="span", attrs={"class":"rtltextaligneligible", "data-careersite-propertyid":"city"}).text.strip())
                desc_span = link_soup.find(name="span", attrs={"class":"jobdescription"})
                description = '<div>' + desc_span.prettify() + '</div>'

                details.append(description)
                details.append(links[i])
                jobs_list.append(details)
            except:
                pass
        return jobs_list
    
    jobs = []
    for i in range(0, 200, 25):
        link = url + str(i)
        jobs = jobs + deloitte_inner_parser(link)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\deloitte_new.csv")
    print("Deloitte ended")
    return jobs_dataframe

def ey_parser(url):
    print("EY started")
    def ey_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        spans = soup.find_all("span", class_="jobTitle hidden-phone")
        for span in spans:
            anchor = span.find("a")
            links.append("https://careers.ey.com/" + anchor["href"])

        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")
                
                details = ["Ernest & Young"]
                job_title = link_soup.find("h1").text.strip()
                details.append(job_title)
                location = link_soup.find("span", attrs={"data-careersite-propertyid":"city"}).text.strip()
                details.append(location)

                span = link_soup.find("span", class_="jobdescription")
                job_description = '<div>' + span.prettify() + '</div>'
                details.append(job_description)
                details.append(links[i])
                jobs_list.append(details)
            except:
                pass
        return jobs_list
    jobs = []
    for i in range(0, 100, 25):
        link = url + str(i)
        jobs = jobs + ey_inner_parser(link)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\ey_new.csv")
    print("EY ended")
    return jobs_dataframe

def sap_parser(urls):
    print("SAP started")
    def sap_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        divs = soup.find_all("div", class_="jobdetail-phone")
        for div in divs:
            anchor = div.find("a", class_="jobTitle-link")
            if anchor:
                links.append("https://jobs.sap.com/" + anchor["href"])

        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")
                
                details = ["SAP"]
                job_title = link_soup.find("h1").text.strip()
                details.append(job_title)
                location = link_soup.find("span", class_="jobGeoLocation").text.split(",")[0].strip()
                details.append(location)

                span = link_soup.find("span", class_="jobdescription")
                job_description = '<div>' + span.prettify() + '</div>'

                details.append(job_description)
                details.append(links[i])
                jobs_list.append(details)

            except:
                pass
        return jobs_list
    
    jobs = []
    url1 = urls[0]
    url2 = urls[1]
    for i in range(0, 101, 25):
        link = url1 + str(i) + url2
        jobs = jobs + sap_inner_parser(link)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\sap_new.csv")
    print("SAP ended")
    return jobs_dataframe

def hsbc_parser(url):
    print("HSBC started")
    def hsbc_inner_parser(url):
        response = requests.get(url) #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        divs = soup.find_all("div", class_="article__header__title")
        for div in divs:
            anchor = div.find("a")
            if anchor:
                links.append(anchor["href"])

        try:
            jobs_list = []
            for i in range(len(links)):
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                details = ["HSBC"]
                job_title = link_soup.find("h2", class_="banner__text__title").text.strip()
                details.append(job_title)
                location_div = link_soup.find("div", class_="view-icon--location").find("div", class_="article__content__view__field__value")
                details.append(location_div.text.strip())
                
                div = link_soup.find("div", class_="article__content__view__field__value")
                jobdescription = div.prettify()
                details.append(jobdescription)
                details.append(links[i])           
                jobs_list.append(details)
        except:
            pass
        return jobs_list
    
    jobs = []
    for i in range(0, 50, 10):
        link = url + str(i)
        jobs = jobs + hsbc_inner_parser(link)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\hsbc_new.csv")
    print("HSBC ended")
    return jobs_dataframe

def electronicarts_parser(url):
    print("EA started")
    response = requests.get(url)
    #read the url and create a BeautifulSoap instance
    soup = BeautifulSoup(response.content, "html.parser")

    links = [] # get the link for each job in google
    table = soup.find("tbody")
    for row in table.find_all("tr"):
        anchor = row.find("a")
        links.append(anchor["href"])

    jobs_list = []
    for i in range(len(links)):
        try:
            link_response = requests.get(links[i])
            link_soup = BeautifulSoup(link_response.content, "html.parser")

            details = ["Electronic Arts"]
            title = link_soup.find("h1", class_="job-title").text.strip()
            location = re.split(":|,", link_soup.find("h3", class_="job-locations").text)[1].strip()
            details.append(title)
            details.append(location)

            jobdescription = '<div>'
            div = soup.find("div", class_="job-details")
            for list in div.find_all("ul"):
                jobdescription += list.prettify()
            jobdescription += '</div>'
            
            details.append(jobdescription)
            details.append(links[i])
            jobs_list.append(details)
        except:
            pass
    jobs_dataframe = pd.DataFrame(jobs_list, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\electronic_arts_new.csv")
    print("EA ended")
    return jobs_dataframe

def bank_of_america_parser(urls):
    print("Bank of America started")
    def bankofamerica_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        heads = soup.find_all("h3", class_="job-search-tile__title")
        for head in heads:
            anchor = head.find("a")
            links.append("https://careers.bankofamerica.com" + anchor["href"])
        
        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                details = ["Bank of America"]
                title = link_soup.find("h1", class_="job-description-body__title").text
                location = link_soup.find("span", class_="js-primary-location").text
                details.append(title)
                details.append(location)

                div = link_soup.find("div", class_="job-description-body__internal")
                jobdescription = div.prettify()
                details.append(jobdescription)
                details.append(links[i])

                jobs_list.append(details)
            except:
                pass
        return jobs_list
    url1 = urls[0]
    url2 = urls[1]
    jobs = bankofamerica_inner_parser(url1)
    jobs += bankofamerica_inner_parser(url2)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\\bank_of_america_new.csv")
    print("Bank of America ended")
    return jobs_dataframe

def massmutual_parser(urls):
    print("MassMutual started")
    def massmutual_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        heads = soup.find_all("h2", class_="headline headline__medium headline--no-spacing")
        for head in heads:
            anchor = head.find("a")
            links.append("https://careers.massmutualindia.com" + anchor["href"])
        
        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                details = ["Mass Mutual"]
                title = link_soup.find("h1", class_="headline headline__medium font-color--blue-3").text.strip()
                location = link_soup.find("span", class_="job-location job-info").text.strip()
                details.append(title)
                details.append(location)

                div = link_soup.find("div", class_="ats-description")
                jobdescription = div.prettify()
                
                details.append(jobdescription)
                details.append(links[i])

                jobs_list.append(details)
            except:
                pass
        return jobs_list

    url1 = urls[0]
    url2 = urls[1]
    jobs = massmutual_inner_parser(url1)
    jobs += massmutual_inner_parser(url2)
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\massmutual_new.csv")
    print("Mass Mutual ended")
    return jobs_dataframe

def hitachi_parser(url):
    print("Hitachi started")
    def hitachi_inner_parser(url):
        response = requests.get(url)
        #read the url and create a BeautifulSoap instance
        soup = BeautifulSoup(response.content, "html.parser")

        links = [] # get the link for each job in google
        locations = []
        divs = soup.find_all("div", class_="jobs-section__item page-section-1")
        for div in divs:
            anchor = div.find("a")
            if anchor:
                links.append(anchor["href"])
                location_div = div.find("div", class_="large-4 columns")
                text = location_div.find_all(str=True, recursive=False)
                location = 'Remote'
                for t in text:
                    if t.strip() != '':
                        location = t.split()[0].strip()
                locations.append(location)

        jobs_list = []
        for i in range(len(links)):
            try:
                link_response = requests.get(links[i])
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                details = ["Hitachi"]
                title = link_soup.find("h1").text.strip()
                details.append(title)
                details.append(locations[i])

                div = link_soup.find("div", class_="page-section-2 space-2 job-description")
                jobdescription = div.prettify()

                details.append(jobdescription)
                details.append(links[i])

                jobs_list.append(details)
            except:
                pass
        return jobs_list
    
    threads = []
    jobs = []

    for i in range(1, 6):
        thread = MyThread(target=hitachi_inner_parser, args=(url + str(i) + "#",))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        jobs = jobs + thread.result
    jobs_dataframe = pd.DataFrame(jobs, columns=["company", "title", "location", "description", "link"])
    #jobs_dataframe.to_csv("Scraping\hitachi_new.csv")
    print("Hitachi ended")
    return jobs_dataframe

class MyThread(threading.Thread):
    def __init__(self, target, args):
        super().__init__()
        self.target = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.target(*self.args)

if __name__=="__main__":
    urls = ["https://jobs.cisco.com/jobs/SearchJobs/?21178=%5B207928%5D&21178_format=6020&21180=%5B164%2C165%2C163%2C162%5D&21180_format=6022&21181=%5B183%2C186%2C194%2C187%2C190%2C191%2C185%5D&21181_format=6023&listFilterMode=1&projectOffset=0",
            "https://www.google.com/about/careers/applications/jobs/results/?location=India&target_level=MID&target_level=EARLY&target_level=INTERN_AND_APPRENTICE&page=",
            "https://jobsindia.deloitte.com/search/?q=&locationsearch=india&startrow=",
            "https://careers.ey.com/ey/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=IN&optionsFacetsDD_customfield1=Consulting&startrow=",
            ["https://jobs.sap.com/go/SAP-Jobs-in-India/851201/", "/?q=&sortColumn=referencedate&sortDirection=desc&scrollToTable=true"],
            "https://mycareer.hsbc.com/en_GB/external/SearchJobs/?1017=%5B67213%5D&1017_format=812&listFilterMode=1&pipelineRecordsPerPage=10&pipelineOffset=",
            "https://ea.gr8people.com/jobs?page=1&geo_location=ChIJx9Lr6tqZyzsRwvu6koO3k64",
            ["https://careers.bankofamerica.com/en-us/job-search/india", "https://careers.bankofamerica.com/en-us/job-search/india?ref=search&country=India&search=jobsByCountry&start=20&rows=40"],
            ["https://careers.massmutualindia.com/search-jobs/India/724/2/1269750/22/79/50/2", "https://careers.massmutualindia.com/search-jobs/India/724/2/1269750/22/79/50/2&p=2"],
            "https://careers.hitachi.com/search/digital-system-and-service/jobs/in/country/india?page="
            ]
    functions = [cisco_parser, 
                 google_parser,
                 deloitte_parser,
                 ey_parser,
                 sap_parser,
                 hsbc_parser,
                 electronicarts_parser,
                 bank_of_america_parser,
                 massmutual_parser,
                 hitachi_parser
                 ]
    n = len(urls)
    threads = []
    dataframe = pd.DataFrame([], columns=["company", "title", "location", "description", "link"])
    for i in range(n):
        thread = MyThread(target=functions[i], args=(urls[i], ))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
        dataframe = pd.concat([dataframe, thread.result])

    dataframe.to_csv("Scraping\\alljobs_new.csv", index=False)
    db_connection = mysql.connector.connect(
        host='localhost',
        user='VIVEK',
        password='Vivek@SQL16',
        database='project'
    )

    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM `jobstable`")
    cols = "`,`".join([str(i) for i in dataframe.columns.tolist()])
    for i, row in dataframe.iterrows():
        sql = "INSERT INTO `jobstable` (`" + cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        db_connection.commit()
    db_connection.close()
