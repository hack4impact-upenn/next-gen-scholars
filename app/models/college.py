from . import ScattergramData
from .. import db
    
import os
import random
from datetime import datetime
import urllib.request, json
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import plotly.tools as tools
import plotly.plotly as py
import plotly.graph_objs as go

PLOTLY_USERNAME = os.environ.get('PLOTLY_USERNAME')
PLOTLY_API_KEY = os.environ.get('PLOTLY_API_KEY')

py.sign_in(PLOTLY_USERNAME, PLOTLY_API_KEY)

auth = HTTPBasicAuth(PLOTLY_USERNAME, PLOTLY_API_KEY)
headers = {'Plotly-Client-Platform': 'python'}


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    cost_of_attendance = db.Column(db.Integer, index=True)
    image = db.Column(db.String, index=True)
    regular_deadline = db.Column(db.Date, index=True)
    admission_rate = db.Column(db.Float, index=True)
    early_deadline = db.Column(db.Date, index=True)
    fafsa_deadline = db.Column(db.Date, index=True)
    scholarship_deadline = db.Column(db.Date, index=True)    
    acceptance_deadline = db.Column(db.Date, index=True)
    plot_SAT2400 = db.Column(db.String)
    plot_SAT1600 = db.Column(db.String)
    plot_ACT = db.Column(db.String)
    image = db.Column(db.String, index=True)
    school_url = db.Column(db.String, index=True)
    school_size = db.Column(db.Integer, index=True)
    school_city = db.Column(db.String, index=True)
    tuition_in_state = db.Column(db.Float, index=True)
    tuition_out_of_state = db.Column(db.Float, index=True)
    cost_of_attendance_in_state = db.Column(db.Float, index=True)
    cost_of_attendance_out_of_state = db.Column(db.Float, index=True)
    room_and_board = db.Column(db.Float, index=True)
    sat_score_average_overall = db.Column(db.Float, index=True)
    act_score_average_overall = db.Column(db.Float, index=True)
    first_generation_percentage = db.Column(db.Float, index=True)
    year_data_collected = db.Column(db.String, index=True)
    race_white = db.Column(db.Float, index=True)
    race_black = db.Column(db.Float, index=True)
    race_hispanic = db.Column(db.Float, index=True)
    race_asian = db.Column(db.Float, index=True)
    race_american_indian = db.Column(db.Float, index=True)
    race_native_hawaiian = db.Column(db.Float, index=True)
    race_international = db.Column(db.Float, index=True)
    # TODO: Add college dates

    def update_plots(self):
        if (self.plot_SAT2400):
            plot_num = self.plot_SAT2400[1 + self.plot_SAT2400.rfind('/')]
            requests.post('https://api.plot.ly/v2/files/' +
                          PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
            requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
                            '/permanent_delete', auth=auth, headers=headers)
        if (self.plot_SAT1600):
            plot_num = self.plot_SAT1600[1 + self.plot_SAT1600.rfind('/')]
            requests.post('https://api.plot.ly/v2/files/' +
                          PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
            requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
                            '/permanent_delete', auth=auth, headers=headers)
        if (self.plot_ACT):
            plot_num = self.plot_ACT[1 + self.plot_ACT.rfind('/')]
            requests.post('https://api.plot.ly/v2/files/' +
                          PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
            requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
                            '/permanent_delete', auth=auth, headers=headers)

        data = ScattergramData.query.filter_by(college=self.name).all()

        college_filename = self.name.replace(' ', '-').lower()

        # GPA vs. SAT [2400]
        SAT2400_Accepted = []
        GPA_SAT2400_Accepted = []
        SAT2400_Denied = []
        GPA_SAT2400_Denied = []
        SAT2400_Waitlisted1 = []
        GPA_SAT2400_Waitlisted1 = []
        SAT2400_Waitlisted2 = []
        GPA_SAT2400_Waitlisted2 = []
        SAT2400_Waitlisted3 = []
        GPA_SAT2400_Waitlisted3 = []

        # GPA vs. SAT [1600]
        SAT1600_Accepted = []
        GPA_SAT1600_Accepted = []
        SAT1600_Denied = []
        GPA_SAT1600_Denied = []
        SAT1600_Waitlisted1 = []
        GPA_SAT1600_Waitlisted1 = []
        SAT1600_Waitlisted2 = []
        GPA_SAT1600_Waitlisted2 = []
        SAT1600_Waitlisted3 = []
        GPA_SAT1600_Waitlisted3 = []

        # GPA vs. ACT
        ACT_Accepted = []
        GPA_ACT_Accepted = []
        ACT_Denied = []
        GPA_ACT_Denied = []
        ACT_Waitlisted1 = []
        GPA_ACT_Waitlisted1 = []
        ACT_Waitlisted2 = []
        GPA_ACT_Waitlisted2 = []
        ACT_Waitlisted3 = []
        GPA_ACT_Waitlisted3 = []

        for i in range(len(data)):
            if(data[i].SAT2400):
                if(data[i].status == 'Accepted'):
                    SAT2400_Accepted.append(int(data[i].SAT2400))
                    GPA_SAT2400_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    SAT2400_Denied.append(int(data[i].SAT2400))
                    GPA_SAT2400_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
                    SAT2400_Waitlisted1.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
                    SAT2400_Waitlisted2.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
                    SAT2400_Waitlisted3.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted3.append(data[i].GPA)

            if(data[i].SAT1600):
                if(data[i].status == 'Accepted'):
                    SAT1600_Accepted.append(int(data[i].SAT1600))
                    GPA_SAT1600_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    SAT1600_Denied.append(int(data[i].SAT1600))
                    GPA_SAT1600_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
                    SAT1600_Waitlisted1.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
                    SAT1600_Waitlisted2.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
                    SAT1600_Waitlisted3.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted3.append(data[i].GPA)

            if(data[i].ACT):
                if(data[i].status == 'Accepted'):
                    ACT_Accepted.append(int(data[i].ACT))
                    GPA_ACT_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    ACT_Denied.append(int(data[i].ACT))
                    GPA_ACT_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
                    ACT_Waitlisted1.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
                    ACT_Waitlisted2.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
                    ACT_Waitlisted3.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted3.append(data[i].GPA)

        # Create a trace
        trace0 = go.Scatter(
            x=SAT2400_Accepted,
            y=GPA_SAT2400_Accepted,
            mode='markers',
            name="Accepted"
        )

        trace1 = go.Scatter(
            x=SAT2400_Denied,
            y=GPA_SAT2400_Denied,
            mode='markers',
            name="Denied"
        )

        trace2 = go.Scatter(
            x=SAT2400_Waitlisted1,
            y=GPA_SAT2400_Waitlisted1,
            mode='markers',
            name="Waitlisted/Deferred (Accepted)"
        )

        trace3 = go.Scatter(
            x=SAT2400_Waitlisted2,
            y=GPA_SAT2400_Waitlisted2,
            mode='markers',
            name="Waitlisted/Deferred (Denied)"
        )

        trace4 = go.Scatter(
            x=SAT2400_Waitlisted3,
            y=GPA_SAT2400_Waitlisted3,
            mode='markers',
            name="Waitlisted/Deferred (Withdrew App)"
        )

        layout1 = go.Layout(
            title='{}: SAT [2400] vs. GPA'.format(self.name),
            xaxis=dict(
                title='SAT [2400]'
            ),
            yaxis=dict(
                title='GPA',
            )
        )

        fig1 = go.Figure(data=[trace0, trace1, trace2,
                               trace3, trace4], layout=layout1)
        self.plot_SAT2400 = py.plot(
            fig1, filename=college_filename + '-sat2400', auto_open=False)

        # Create a trace
        trace5 = go.Scatter(
            x=SAT1600_Accepted,
            y=GPA_SAT1600_Accepted,
            mode='markers',
            name="Accepted"
        )

        trace6 = go.Scatter(
            x=SAT1600_Denied,
            y=GPA_SAT1600_Denied,
            mode='markers',
            name="Denied"
        )

        trace7 = go.Scatter(
            x=SAT1600_Waitlisted1,
            y=GPA_SAT1600_Waitlisted1,
            mode='markers',
            name="Waitlisted/Deferred (Accepted)"
        )

        trace8 = go.Scatter(
            x=SAT1600_Waitlisted2,
            y=GPA_SAT1600_Waitlisted2,
            mode='markers',
            name="Waitlisted/Deferred (Denied)"
        )

        trace9 = go.Scatter(
            x=SAT1600_Waitlisted3,
            y=GPA_SAT1600_Waitlisted3,
            mode='markers',
            name="Waitlisted/Deferred (Withdrew App)"
        )

        layout2 = go.Layout(
            title='{}: SAT [1600] vs. GPA'.format(self.name),
            xaxis=dict(
                title='SAT1600'
            ),
            yaxis=dict(
                title='GPA',
            )
        )

        fig2 = go.Figure(data=[trace5, trace6, trace7,
                               trace8, trace9], layout=layout2)
        self.plot_SAT1600 = py.plot(
            fig2, filename=college_filename + '-sat1600', auto_open=False)

        # Create a trace
        trace10 = go.Scatter(
            x=ACT_Accepted,
            y=GPA_ACT_Accepted,
            mode='markers',
            name="Accepted"
        )

        trace11 = go.Scatter(
            x=ACT_Denied,
            y=GPA_ACT_Denied,
            mode='markers',
            name="Denied"
        )

        trace12 = go.Scatter(
            x=ACT_Waitlisted1,
            y=GPA_ACT_Waitlisted1,
            mode='markers',
            name="Waitlisted/Deferred (Accepted)"
        )

        trace13 = go.Scatter(
            x=ACT_Waitlisted2,
            y=GPA_ACT_Waitlisted2,
            mode='markers',
            name="Waitlisted/Deferred (Denied)"
        )

        trace14 = go.Scatter(
            x=ACT_Waitlisted3,
            y=GPA_ACT_Waitlisted3,
            mode='markers',
            name="Waitlisted/Deferred (Withdrew App)"
        )

        layout3 = go.Layout(
            title='{}: ACT vs. GPA'.format(self.name),
            xaxis=dict(
                title='ACT'
            ),
            yaxis=dict(
                title='GPA',
            )
        )

        fig3 = go.Figure(data=[trace10, trace11, trace12,
                               trace13, trace14], layout=layout3)
        self.plot_ACT = py.plot(
            fig3, filename=college_filename + '-act', auto_open=False)

    @staticmethod
    def get_college_by_name(name):
        return College.query.filter_by(name=name).first()

    @staticmethod
    def search_college_scorecard(college):
        ''' This method uses the College Scorecard Data API to retrieve a dictionary
        of information about colleges that match with our query name
        @param name: name of the college we need to look up
        @return a dictionary of information about colleges that match with our query'''
        # Split name by white space, add %20 as the encoding for the space chacracter in query
        name = college.name
        tokens = name.split()
        nameNewFormat = ''
        for token in tokens:
            nameNewFormat = nameNewFormat + token + "%20"
        nameNewFormat = nameNewFormat[:-3]
        nameNewFormat  = nameNewFormat.replace(',', '')

        # Get current year and keep decrementing the year to get the valid most recent data
        now = datetime.now()
        yearNum = now.year
        while(True):
            try:
                year = str(yearNum)
                urlStr = '' .join(['https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=',
                    nameNewFormat, '&_fields=school.name,school.city,', year, '.admissions.admission_rate.overall,',
                    year, '.student.size,school.school_url,', year, '.cost.attendance.academic_year,',
                    year, '.cost.tuition.in_state,', year, '.cost.tuition.out_of_state,', year,
                    '.admissions.act_scores.midpoint.cumulative,', year, '.student.share_firstgeneration,', year,
                    '.admissions.sat_scores.average.overall,', year, '.student.demographics.race_ethnicity.white,',
                    year, '.student.demographics.race_ethnicity.black,', year, '.student.demographics.race_ethnicity.hispanic,',
                    year, '.student.demographics.race_ethnicity.asian,', year, '.student.demographics.race_ethnicity.aian,',
                    year, '.student.demographics.race_ethnicity.nhpi,', year, '.student.demographics.race_ethnicity.non_resident_alien',
                    '&api_key=jjHzFLWEyba3YYtWiv7jaQN8kGSkMuf55A9sRsxl'])
                r = requests.get(urlStr)
                r.raise_for_status()
                data = r.json()
            except HTTPError:
                yearNum = yearNum - 1
            else:
                college.year_data_collected = year
                break
        return(data)

    @staticmethod
    def retrieve_college_info(college):
        ''' This method takes in a College, attempts to find the college that best matches
        with our query, and fill in the variables of the college accordingly.
        Always called after college.name has been initialized
        @param name: name of the college we need to look up
        @return a dictionary of information about the college'''
        if(college.name == ''):
            return
        data = College.search_college_scorecard(college)

        # If there are some colleges that match with the query
        if(len(data['results']) > 0):
            # Default to the first search result returned
            result = data['results'][0]
            firstFoundIdx = float("inf")
            # Prioritize colleges whose name contain the query name, and of those who do, prioritize
            # those wherein the query name appears earlier in the college's name
            for r in data['results']:
                idx = r['school.name'].find(college.name)
                if idx != -1:
                    if(firstFoundIdx > idx):
                        firstFoundIdx = idx
                        result = r
            y = college.year_data_collected
            if result[y + '.admissions.admission_rate.overall'] is not None:
                college.admission_rate = round(result[y + '.admissions.admission_rate.overall']*100,2)
            if result['school.school_url'] is not None:
                college.school_url = result['school.school_url']
            if result[y + '.student.size'] is not None:
                college.school_size = result[y + '.student.size']
            if result['school.city'] is not None:
                college.school_city = result['school.city']
            if result[y + '.cost.tuition.in_state'] is not None:
                college.tuition_in_state = result[y + '.cost.tuition.in_state']
            if result[y + '.cost.tuition.out_of_state'] is not None:
                college.tuition_out_of_state = result[y + '.cost.tuition.out_of_state']
            if result[y + '.cost.attendance.academic_year'] is not None:
                college.cost_of_attendance_in_state = result[y + '.cost.attendance.academic_year']
            if result[y + '.cost.attendance.academic_year'] is not None and result[y + '.cost.tuition.in_state'] is not None:
                college.room_and_board = result[y + '.cost.attendance.academic_year'] - result[y + '.cost.tuition.in_state']
            if result[y + '.cost.tuition.out_of_state'] is not None:
                college.cost_of_attendance_out_of_state = college.tuition_out_of_state + college.room_and_board
            if result[y + '.admissions.sat_scores.average.overall'] is not None:
                college.sat_score_average_overall = result[y + '.admissions.sat_scores.average.overall']
            if result[y + '.admissions.act_scores.midpoint.cumulative'] is not None:
                college.act_score_average_overall = result[y + '.admissions.act_scores.midpoint.cumulative']
            if result[y + '.student.share_firstgeneration'] is not None:
                college.first_generation_percentage = round(result[y + '.student.share_firstgeneration']*100,2)
            if result[y + '.student.demographics.race_ethnicity.white'] is not None:
                college.race_white = round(result[y + '.student.demographics.race_ethnicity.white']*100,2)
            if result[y + '.student.demographics.race_ethnicity.black'] is not None:
                college.race_black = round(result[y + '.student.demographics.race_ethnicity.black']*100,2)
            if result[y + '.student.demographics.race_ethnicity.hispanic'] is not None:
                college.race_hispanic = round(result[y + '.student.demographics.race_ethnicity.hispanic']*100,2)
            if result[y + '.student.demographics.race_ethnicity.asian'] is not None:
                college.race_asian= round(result[y + '.student.demographics.race_ethnicity.asian']*100,2)
            if result[y + '.student.demographics.race_ethnicity.aian'] is not None:
                college.race_american_indian = round(result[y + '.student.demographics.race_ethnicity.aian']*100,2)
            if result[y + '.student.demographics.race_ethnicity.nhpi'] is not None:
                college.race_native_hawaiian = round(result[y + '.student.demographics.race_ethnicity.nhpi']*100,2)
            if result[y + '.student.demographics.race_ethnicity.non_resident_alien'] is not None:
                college.race_international = round(result[y + '.student.demographics.race_ethnicity.non_resident_alien']*100,2)

    @staticmethod
    def insert_colleges():
        college_names = {
            'University of Pennsylvania', 'Columbia University',
            'Stanford University', 'Princeton University',
            'Harvard University', 'Cornell University', 'Yale University',
            'Brown University', 'Dartmouth College', 'New York University',
            'University of California, Berkeley',
            'University of California, Los Angeles', 'University of Michigan-Ann Arbor',
            'Carnegie Mellon University', 'John Hopkins University',
            'University of Chicago', 'Amherst College', 'Williams College',
            'Massachusetts Institute of Technology',
            'Georgia Institute of Technology',
            'California Institute of Technology', 'Duke University'
        }
        early_deadlines = [
            datetime(2017, 11, 4),
            datetime(2017, 11, 3),
            datetime(2017, 10, 26),
            datetime(2017, 11, 1),
            datetime(2017, 11, 11),
            datetime(2017, 11, 13),
            datetime(2017, 10, 29)
        ]
        regular_deadlines = [
            datetime(2017, 12, 31),
            datetime(2017, 1, 1),
            datetime(2017, 1, 2),
            datetime(2017, 1, 3),
            datetime(2017, 1, 5),
            datetime(2017, 2, 1),
            datetime(2017, 1, 14)
        ]
        fafsa_deadline = [
            datetime(2017, 12, 31),
            datetime(2017, 1, 1),
            datetime(2017, 1, 2),
            datetime(2017, 1, 3),
            datetime(2017, 1, 5),
            datetime(2017, 2, 1),
            datetime(2017, 1, 14)
        ]
        acceptance_deadline = [
            datetime(2017, 12, 31),
            datetime(2017, 1, 1),
            datetime(2017, 1, 2),
            datetime(2017, 1, 3),
            datetime(2017, 1, 5),
            datetime(2017, 2, 1),
            datetime(2017, 1, 14)
        ]
        scholarship_deadlines = [
            datetime(2017, 12, 31),
            datetime(2017, 1, 1),
            datetime(2017, 1, 2),
            datetime(2017, 1, 3),
            datetime(2017, 1, 5),
            datetime(2017, 2, 1),
            datetime(2017, 1, 14)
        ]
        descriptions = [
            'Private research university', 'Ivy League university',
            'Liberal arts college', 'Public research university',
            'Private doctorate university'
        ]

        images = [
            'http://www.collegerank.net/wp-content/uploads/2015/08/morehouse-college-quad.jpg',
            'https://static1.squarespace.com/static/52f11228e4b0a96c7b51a92d/t/55e705bee4b03fc234f02b5e/1441203647587/'
        ]

        for c in college_names:
            college = College.get_college_by_name(c)
            if college is None:
                college = College(
                    name=c,
                    admission_rate = 0,
                    description=random.choice(descriptions),
                    regular_deadline=random.choice(regular_deadlines),
                    early_deadline=random.choice(early_deadlines),
                    fafsa_deadline=random.choice(fafsa_deadline),
                    acceptance_deadline=random.choice(acceptance_deadline),
                    school_url = "",
                    school_size = 0,
                    school_city = "",
                    tuition_in_state = 0,
                    tuition_out_of_state = 0,
                    cost_of_attendance_in_state = 0,
                    cost_of_attendance_out_of_state = 0,
                    room_and_board = 0,
                    sat_score_average_overall = 0,
                    act_score_average_overall = 0,
                    first_generation_percentage = 0,
                    year_data_collected = "",
                    race_white = 0,
                    race_black = 0,
                    race_hispanic = 0,
                    race_asian = 0,
                    race_american_indian = 0,
                    race_native_hawaiian = 0,
                    race_international = 0,
                    scholarship_deadline=random.choice(scholarship_deadlines),
                    image=random.choice(images))
                College.retrieve_college_info(college)
            db.session.add(college)
        db.session.commit()

        #@TODOOOOO: DO THE SAME FOR ADD COLLEGE METHOD IN COUNSELOR:VIEWS.PY

    def __repr__(self):
        return '<College: {}>'.format(self.name)
