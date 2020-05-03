import bs4
import cfscrape

from Brain.Utils.strings import *


def branch_as_baseurl(branch, course):
    branch_coded = ""  # for courses which doesn't have a branch ['BCOM', 'BAF', 'BBI', 'BFM', 'BMS', 'MCA']
    if course == 'BE':
        if branch == 'Automobile':
            branch_coded = 'Automobile'
        elif branch == 'Biomedical':
            branch_coded = 'Biomedical'
        elif branch == 'Biotechnology':
            branch_coded = 'Biotech'
        elif branch == 'Chemical':
            branch_coded = 'Chemical'
        elif branch == 'Civil':
            branch_coded = 'Civil'
        elif branch == 'Computer':
            branch_coded = 'Comps'
        elif branch == 'Electrical':
            branch_coded = 'Electrical'
        elif branch == 'Electronics':
            branch_coded = 'Etrx'
        elif branch == 'Electronics and Telecommunication':
            branch_coded = 'Extc'
        elif branch == 'Information Technology':
            branch_coded = 'IT'
        elif branch == 'Instrumentation':
            branch_coded = 'Instrumentation'
        elif branch == 'Mechanical':
            branch_coded = 'Mechanical'
        elif branch == 'Mechatronics':
            branch_coded = 'Mechatronics'
        elif branch == 'Production':
            branch_coded = 'Production'
    elif course == 'ME':
        if branch == 'CAD CAM and Robotics':
            branch_coded = 'CAD'
        elif branch == 'Computer Engineering':
            branch_coded = 'Computer'
        elif branch == 'CN & IS':
            branch_coded = 'Cnis'
        elif branch == 'Construction Engineering':
            branch_coded = 'Construction'
        elif branch == 'Electronics Engineering':
            branch_coded = 'Etrc'
        elif branch == 'Electronics & Telecommunication':
            branch_coded = 'Extc'
        elif branch == 'Information Technology':
            branch_coded = 'IT'
        elif branch == 'Machine Design':
            branch_coded = 'MachineDesign'
        elif branch == 'Thermal Engineering':
            branch_coded = 'Thermal'
    elif course == 'BSC':
        if branch == 'Biochemistry':
            branch_coded = 'Biochemistry'
        elif branch == 'Biotechnology':
            branch_coded = 'Biotech'
        elif branch == 'Botany':
            branch_coded = 'Botany'
        elif branch == 'Chemistry':
            branch_coded = 'Chemistry'
        elif branch == 'Computer Science (CS)':
            branch_coded = 'CS'
        elif branch == 'Information Technology':
            branch_coded = 'IT'
        elif branch == 'Mathematics':
            branch_coded = 'Mathematics'
        elif branch == 'Physics':
            branch_coded = 'Physics'
        elif branch == 'Zoology':
            branch_coded = 'Zoology'
    return branch_coded


def generate_uri(course, branch, sem):
    # generates URI for selected course branch and sem
    branch = branch_as_baseurl(branch, course)
    URI = ""
    if course == 'BE':
        sem = 'Sem' + str(sem)
        if sem == 'Sem1' or sem == 'Sem2':
            YR = 'FE'
        else:
            if sem == 'Sem3' or sem == 'Sem4':
                YR = 'SE'
            elif sem == 'Sem5' or sem == 'Sem6':
                YR = 'TE'
            else:
                YR = 'BE'
        URI = YR + branch + sem + '.php'
    elif course == 'ME':
        sem = 'Sem' + str(sem)
        URI = course + branch + sem + '.php'
    elif course == 'BSC':
        sem = "Sem" + str(sem)
        if sem == 'Sem3' or sem == 'Sem4':
            YR = 'SY'
        elif sem == 'Sem5' or sem == 'Sem6':
            YR = 'TY'
        else:
            YR = 'FY'
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


def fetch_links_from_url(uri):
    # scrapes 'BASE_URL + uri' for Subjects and QuestionPapers and returns them
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
