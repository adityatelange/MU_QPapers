import bs4
import cfscrape
from requests import get

from Brain.Utils.strings import *


def brancher(branch, course):
    uri = ""  # for courses which doesn't have a branch ['BCOM', 'BAF', 'BBI', 'BFM', 'BMS', 'MCA']
    if course == 'BE':
        if branch == 'Automobile':
            uri = 'Automobile'
        elif branch == 'Biomedical':
            uri = 'Biomedical'
        elif branch == 'Biotechnology':
            uri = 'Biotech'
        elif branch == 'Chemical':
            uri = 'Chemical'
        elif branch == 'Civil':
            uri = 'Civil'
        elif branch == 'Computer':
            uri = 'Comps'
        elif branch == 'Electrical':
            uri = 'Electrical'
        elif branch == 'Electronics':
            uri = 'Etrx'
        elif branch == 'Electronics and Telecommunication':
            uri = 'Extc'
        elif branch == 'Information Technology':
            uri = 'IT'
        elif branch == 'Instrumentation':
            uri = 'Instrumentation'
        elif branch == 'Mechanical':
            uri = 'Mechanical'
        elif branch == 'Mechatronics':
            uri = 'Mechatronics'
        elif branch == 'Production':
            uri = 'Production'
    elif course == 'ME':
        if branch == 'CAD CAM and Robotics':
            uri = 'CAD'
        elif branch == 'Computer Engineering':
            uri = 'Computer'
        elif branch == 'CN & IS':
            uri = 'Cnis'
        elif branch == 'Construction Engineering':
            uri = 'Construction'
        elif branch == 'Electronics Engineering':
            uri = 'Etrc'
        elif branch == 'Electronics & Telecommunication':
            uri = 'Extc'
        elif branch == 'Information Technology':
            uri = 'IT'
        elif branch == 'Machine Design':
            uri = 'MachineDesign'
        elif branch == 'Thermal Engineering':
            uri = 'Thermal'
    elif course == 'BSC':
        if branch == 'Biochemistry':
            uri = 'Biochemistry'
        elif branch == 'Biotechnology':
            uri = 'Biotech'
        elif branch == 'Botany':
            uri = 'Botany'
        elif branch == 'Chemistry':
            uri = 'Chemistry'
        elif branch == 'Computer Science (CS)':
            uri = 'CS'
        elif branch == 'Information Technology':
            uri = 'IT'
        elif branch == 'Mathematics':
            uri = 'Mathematics'
        elif branch == 'Physics':
            uri = 'Physics'
        elif branch == 'Zoology':
            uri = 'Zoology'
    return uri


def get_subs_links(uri):
    scraper = cfscrape.create_scraper()
    page = scraper.get(BASE_URL + uri)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    subjects_all = []
    papers_all = []
    for some in soup.find_all('table', attrs={'class': 't1'}):

        subject = some.find('thead').find('tr').find('th').text
        subjects_all.append(subject)

        papers = {}
        for x in some.find('tbody').find_all('tr'):
            for paper in x.find_all('th'):
                name = paper.text
                try:
                    lenk = paper.find('a').get('href')
                    papers[name] = lenk
                except AttributeError:
                    pass  # for blank table cells
        papers_all.append(papers)

    return subjects_all, papers_all


def link_getter(course, branch, sem):
    URI = ""
    if course == 'BE':
        sem = 'Sem' + str(sem)
        if sem == 'Sem1' or sem == 'Sem2':
            YR = 'FE'
            branch = ''
        else:
            if sem == 'Sem3' or sem == 'Sem4':
                YR = 'SE'
            elif sem == 'Sem5' or sem == 'Sem6':
                YR = 'TE'
            else:
                YR = 'BE'
            branch = brancher(branch, course)
        URI = YR + branch + sem + '.php'
    elif course == 'ME':
        sem = 'Sem' + str(sem)
        branch = brancher(branch, course)
        URI = course + branch + sem + '.php'
    elif course == 'BSC':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'

        branch = brancher(branch, course)
        URI = YR + "Bsc" + branch + sem + '.php'
    elif course == 'BCOM':
        sem = "Semester" + str(sem)
        if sem == 'Semester3' or sem == 'Semester4':
            YR = 'SY'
        elif sem == 'Semester5' or sem == 'Semester6':
            YR = 'TY'
        else:
            YR = 'FY'
        URI = YR + "BCOM" + sem + '.php'
    elif course == 'BAF':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'
        URI = YR + "BAF" + sem + '.php'
    elif course == 'BBI':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'
        URI = YR + "BBI" + sem + '.php'
    elif course == 'BFM':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'
        URI = YR + "BFM" + sem + '.php'
    elif course == 'BMS':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'
        URI = YR + "BMS" + sem + '.php'
    elif course == "MCA":
        sem = "Semester" + str(sem)
        URI = course + sem + '.php'
    return URI
