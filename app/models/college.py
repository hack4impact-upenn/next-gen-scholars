from . import ScattergramData
from .. import db
    
import os
import random
from datetime import datetime
import urllib.request, json
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
# import plotly.tools as tools
# import plotly.plotly as py
# import plotly.graph_objs as go

# PLOTLY_USERNAME = os.environ.get('PLOTLY_USERNAME')
# PLOTLY_API_KEY = os.environ.get('PLOTLY_API_KEY')

# py.sign_in(PLOTLY_USERNAME, PLOTLY_API_KEY)

# auth = HTTPBasicAuth(PLOTLY_USERNAME, PLOTLY_API_KEY)
# headers = {'Plotly-Client-Platform': 'python'}


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scorecard_id=db.Column(db.Integer,index=True)
    name = db.Column(db.String, index=True)
    institution_type = db.Column(db.String, index=True) #private, public, proprietary
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
    
    median_debt_income_0_30000 = db.Column(db.Integer, index=True)
    median_debt_income_30001_75000 = db.Column(db.Integer, index=True)
    median_debt_income_75001_plus = db.Column(db.Integer, index=True)
    median_debt_first_gen = db.Column(db.Integer, index=True)
    median_debt_non_first_gen = db.Column(db.Integer, index=True)

    net_price_0_30000 = db.Column(db.Integer, index=True)
    net_price_30001_48000 = db.Column(db.Integer, index=True)
    net_price_48001_75000 = db.Column(db.Integer, index=True)
    net_price_75001_110000 = db.Column(db.Integer, index=True)
    net_price_110001_plus = db.Column(db.Integer, index=True)

    image = db.Column(db.String, index=True)
    is_hispanic_serving = db.Column(db.Integer, index=True)
    school_url = db.Column(db.String, index=True)
    price_calculator_url = db.Column(db.String, index=True)
    school_size = db.Column(db.Integer, index=True)
    school_city = db.Column(db.String, index=True)
    school_state = db.Column(db.String, index=True)
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

    # def update_plots(self):
    #     if (self.plot_SAT2400):
    #         plot_num = self.plot_SAT2400[1 + self.plot_SAT2400.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)
    #     if (self.plot_SAT1600):
    #         plot_num = self.plot_SAT1600[1 + self.plot_SAT1600.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)
    #     if (self.plot_ACT):
    #         plot_num = self.plot_ACT[1 + self.plot_ACT.rfind('/')]
    #         requests.post('https://api.plot.ly/v2/files/' +
    #                       PLOTLY_USERNAME + ':' + plot_num + '/trash', auth=auth, headers=headers)
    #         requests.delete('https://api.plot.ly/v2/files/' + username + ':' + plot_num +
    #                         '/permanent_delete', auth=auth, headers=headers)

    #     data = ScattergramData.query.filter_by(college=self.name).all()

    #     college_filename = self.name.replace(' ', '-').lower()

    #     # GPA vs. SAT [2400]
    #     SAT2400_Accepted = []
    #     GPA_SAT2400_Accepted = []
    #     SAT2400_Denied = []
    #     GPA_SAT2400_Denied = []
    #     SAT2400_Waitlisted1 = []
    #     GPA_SAT2400_Waitlisted1 = []
    #     SAT2400_Waitlisted2 = []
    #     GPA_SAT2400_Waitlisted2 = []
    #     SAT2400_Waitlisted3 = []
    #     GPA_SAT2400_Waitlisted3 = []

    #     # GPA vs. SAT [1600]
    #     SAT1600_Accepted = []
    #     GPA_SAT1600_Accepted = []
    #     SAT1600_Denied = []
    #     GPA_SAT1600_Denied = []
    #     SAT1600_Waitlisted1 = []
    #     GPA_SAT1600_Waitlisted1 = []
    #     SAT1600_Waitlisted2 = []
    #     GPA_SAT1600_Waitlisted2 = []
    #     SAT1600_Waitlisted3 = []
    #     GPA_SAT1600_Waitlisted3 = []

    #     # GPA vs. ACT
    #     ACT_Accepted = []
    #     GPA_ACT_Accepted = []
    #     ACT_Denied = []
    #     GPA_ACT_Denied = []
    #     ACT_Waitlisted1 = []
    #     GPA_ACT_Waitlisted1 = []
    #     ACT_Waitlisted2 = []
    #     GPA_ACT_Waitlisted2 = []
    #     ACT_Waitlisted3 = []
    #     GPA_ACT_Waitlisted3 = []

    #     for i in range(len(data)):
    #         if(data[i].SAT2400):
    #             if(data[i].status == 'Accepted'):
    #                 SAT2400_Accepted.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 SAT2400_Denied.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 SAT2400_Waitlisted1.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 SAT2400_Waitlisted2.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 SAT2400_Waitlisted3.append(int(data[i].SAT2400))
    #                 GPA_SAT2400_Waitlisted3.append(data[i].GPA)

    #         if(data[i].SAT1600):
    #             if(data[i].status == 'Accepted'):
    #                 SAT1600_Accepted.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 SAT1600_Denied.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 SAT1600_Waitlisted1.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 SAT1600_Waitlisted2.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 SAT1600_Waitlisted3.append(int(data[i].SAT1600))
    #                 GPA_SAT1600_Waitlisted3.append(data[i].GPA)

    #         if(data[i].ACT):
    #             if(data[i].status == 'Accepted'):
    #                 ACT_Accepted.append(int(data[i].ACT))
    #                 GPA_ACT_Accepted.append(data[i].GPA)
    #             elif(data[i].status == 'Denied'):
    #                 ACT_Denied.append(int(data[i].ACT))
    #                 GPA_ACT_Denied.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Accepted)'):
    #                 ACT_Waitlisted1.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted1.append(data[i].GPA)
    #             elif(data[i].status == 'Waitlisted/Deferred (Denied)'):
    #                 ACT_Waitlisted2.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted2.append(data[i].GPA)
    #             if(data[i].status == 'Waitlisted/Deferred (Withdrew App)'):
    #                 ACT_Waitlisted3.append(int(data[i].ACT))
    #                 GPA_ACT_Waitlisted3.append(data[i].GPA)

    #     # Create a trace
    #     trace0 = go.Scatter(
    #         x=SAT2400_Accepted,
    #         y=GPA_SAT2400_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace1 = go.Scatter(
    #         x=SAT2400_Denied,
    #         y=GPA_SAT2400_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace2 = go.Scatter(
    #         x=SAT2400_Waitlisted1,
    #         y=GPA_SAT2400_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace3 = go.Scatter(
    #         x=SAT2400_Waitlisted2,
    #         y=GPA_SAT2400_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace4 = go.Scatter(
    #         x=SAT2400_Waitlisted3,
    #         y=GPA_SAT2400_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout1 = go.Layout(
    #         title='{}: SAT [2400] vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='SAT [2400]'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig1 = go.Figure(data=[trace0, trace1, trace2,
    #                            trace3, trace4], layout=layout1)
    #     self.plot_SAT2400 = py.plot(
    #         fig1, filename=college_filename + '-sat2400', auto_open=False)

    #     # Create a trace
    #     trace5 = go.Scatter(
    #         x=SAT1600_Accepted,
    #         y=GPA_SAT1600_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace6 = go.Scatter(
    #         x=SAT1600_Denied,
    #         y=GPA_SAT1600_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace7 = go.Scatter(
    #         x=SAT1600_Waitlisted1,
    #         y=GPA_SAT1600_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace8 = go.Scatter(
    #         x=SAT1600_Waitlisted2,
    #         y=GPA_SAT1600_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace9 = go.Scatter(
    #         x=SAT1600_Waitlisted3,
    #         y=GPA_SAT1600_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout2 = go.Layout(
    #         title='{}: SAT [1600] vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='SAT1600'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig2 = go.Figure(data=[trace5, trace6, trace7,
    #                            trace8, trace9], layout=layout2)
    #     self.plot_SAT1600 = py.plot(
    #         fig2, filename=college_filename + '-sat1600', auto_open=False)

    #     # Create a trace
    #     trace10 = go.Scatter(
    #         x=ACT_Accepted,
    #         y=GPA_ACT_Accepted,
    #         mode='markers',
    #         name="Accepted"
    #     )

    #     trace11 = go.Scatter(
    #         x=ACT_Denied,
    #         y=GPA_ACT_Denied,
    #         mode='markers',
    #         name="Denied"
    #     )

    #     trace12 = go.Scatter(
    #         x=ACT_Waitlisted1,
    #         y=GPA_ACT_Waitlisted1,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Accepted)"
    #     )

    #     trace13 = go.Scatter(
    #         x=ACT_Waitlisted2,
    #         y=GPA_ACT_Waitlisted2,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Denied)"
    #     )

    #     trace14 = go.Scatter(
    #         x=ACT_Waitlisted3,
    #         y=GPA_ACT_Waitlisted3,
    #         mode='markers',
    #         name="Waitlisted/Deferred (Withdrew App)"
    #     )

    #     layout3 = go.Layout(
    #         title='{}: ACT vs. GPA'.format(self.name),
    #         xaxis=dict(
    #             title='ACT'
    #         ),
    #         yaxis=dict(
    #             title='GPA',
    #         )
    #     )

    #     fig3 = go.Figure(data=[trace10, trace11, trace12,
    #                            trace13, trace14], layout=layout3)
    #     self.plot_ACT = py.plot(
    #         fig3, filename=college_filename + '-act', auto_open=False)

    @staticmethod
    def get_college_by_name(name):
        return College.query.filter_by(name=name).first()

    @staticmethod
    def search_college_scorecard(college):
        ''' This method uses the College Scorecard Data API to retrieve a dictionary
        of information about colleges that match with our query name
        @param name: name of the college we need to look up
        @return a dictionary of information about colleges that match with our query'''


        if college.scorecard_id is not '':
            nameNewFormat='id=' + str(college.scorecard_id)

        else:
            name = 'school.name=' + college.name
            nameNewFormat = name.replace(' ', '%20')
            
        try:
            data = None
            year='latest'
            urlStr = '' .join(['https://api.data.gov/ed/collegescorecard/v1/schools.json?',
                nameNewFormat, 
                '&_fields=school.name,id,school.city,school.state,school.school_url,school.price_calculator_url,', 
                'school.minority_serving.hispanic,school.ownership_peps,',
                year, '.admissions.admission_rate.overall,',
                year, '.student.size,', 
                year, '.cost.attendance.academic_year,',
                year, '.cost.tuition.in_state,', 
                year, '.cost.tuition.out_of_state,', 
                
                #aid/debt
                year, '.aid.median_debt.income.0_30000,',
                year, '.aid.median_debt.income.30001_75000,',
                year, '.aid.median_debt.income.greater_than_75000,',
                year, '.aid.median_debt.non_first_generation_students,',
                year, '.aid.median_debt.first_generation_students,',

                #costs
                year, '.cost.net_price.public.by_income_level.0-30000,',
                year, '.cost.net_price.public.by_income_level.30001-48000,',
                year, '.cost.net_price.public.by_income_level.48001-75000,',
                year, '.cost.net_price.public.by_income_level.75001-110000,',
                year, '.cost.net_price.public.by_income_level.110001-plus,',
                year, '.cost.net_price.private.by_income_level.0-30000,',
                year, '.cost.net_price.private.by_income_level.30001-48000,',
                year, '.cost.net_price.private.by_income_level.48001-75000,',
                year, '.cost.net_price.private.by_income_level.75001-110000,',
                year, '.cost.net_price.private.by_income_level.110001-plus,',

                year, '.admissions.act_scores.midpoint.cumulative,', 
                year, '.student.share_firstgeneration,', 
                year, '.admissions.sat_scores.average.overall,', 
                year, '.student.demographics.race_ethnicity.white,',
                year, '.student.demographics.race_ethnicity.black,', 
                year, '.student.demographics.race_ethnicity.hispanic,',
                year, '.student.demographics.race_ethnicity.asian,', 
                year, '.student.demographics.race_ethnicity.aian,',
                year, '.student.demographics.race_ethnicity.nhpi,', 
                year, '.student.demographics.race_ethnicity.non_resident_alien',
                '&api_key=jjHzFLWEyba3YYtWiv7jaQN8kGSkMuf55A9sRsxl'])

            r = requests.get(urlStr)
            r.raise_for_status()
            data = r.json()
        except HTTPError:
            print('error')
            
        else:
            college.year_data_collected = year

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

        if data is None:
            return False

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
            if result['school.price_calculator_url'] is not None:
                college.price_calculator_url = result['school.price_calculator_url']
            if result['id'] is not None:
                college.scorecard_id = result['id']
            if result['school.ownership_peps'] is not None:
                ownership_values = { 1 : 'public', 2 : 'private', 3 : 'proprietary'}
                college.institution_type = ownership_values.get(result['school.ownership_peps'])
            if result[y+'.aid.median_debt.income.0_30000'] is not None:
                college.median_debt_income_0_30000 = result[y+'.aid.median_debt.income.0_30000']
            if result[y+'.aid.median_debt.income.30001_75000'] is not None:
                college.median_debt_income_30001_75000 = result[y+'.aid.median_debt.income.30001_75000']
            if result[y+'.aid.median_debt.income.greater_than_75000'] is not None:
                college.median_debt_income_75001_plus = result[y+'.aid.median_debt.income.greater_than_75000']
            if result[y+'.aid.median_debt.first_generation_students'] is not None:
                college.median_debt_first_gen = result[y+'.aid.median_debt.first_generation_students']
            if result[y+'.aid.median_debt.non_first_generation_students'] is not None:
                college.median_debt_non_first_gen = result[y+'.aid.median_debt.non_first_generation_students']
            
            if result[y + '.student.size'] is not None:
                college.school_size = result[y + '.student.size']
            if result['school.city'] is not None:
                college.school_city = result['school.city']
            if result['school.state'] is not None:
                college.school_state = result['school.state']
            if result['school.minority_serving.hispanic'] is not None:
                college.is_hispanic_serving = result['school.minority_serving.hispanic']
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
            

            #will only show in-state net price if instiution is public and in CA
            inst_type_to_get = college.institution_type if college.school_state == 'CA' and result['school.ownership_peps'] == 1\
                else 'private'
            college.net_price_0_30000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.0-30000']
            college.net_price_30001_48000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.30001-48000']
            college.net_price_48001_75000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.48001-75000']
            college.net_price_75001_110000 = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.75001-110000']
            college.net_price_110001_plus = result[y+'.cost.net_price.'+inst_type_to_get+'.by_income_level.110001-plus']



            ivy_leagues = {'Cornell University', 'Dartmouth University', 'Brown University', 'Columbia University',
                'University of Pennsylvania', 'Princeton University', 'Yale University', 'Harvard University'}

            if college.description == '':
                default = (college.institution_type).capitalize() + ' Instiution in ' + college.school_state
                college.description = 'Ivy League Institution' if college.name in ivy_leagues else default   
                
            return True


    @staticmethod
    def insert_colleges():
        college_names = {
            'University of Pennsylvania', 'Columbia University',
            'Stanford University', 'Princeton University',
            'Harvard University', 'Cornell University', 'Yale University',
            'Brown University', 'Dartmouth College', 'New York University',
            'University of California - Berkeley',
            'University of California - Los Angeles', 'University of Michigan-Ann Arbor',
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
                    scorecard_id = '',
                    description='',
                    regular_deadline=None,
                    early_deadline=None,
                    fafsa_deadline=None,
                    acceptance_deadline=None,
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
                    scholarship_deadline=None,
                    image=random.choice(images))
                College.retrieve_college_info(college)
            db.session.add(college)
        db.session.commit()

        #@TODOOOOO: DO THE SAME FOR ADD COLLEGE METHOD IN COUNSELOR:VIEWS.PY

    def __repr__(self):
        return '<College: {}>'.format(self.name)
