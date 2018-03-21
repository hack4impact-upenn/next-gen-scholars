from . import ScattergramData
from .. import db

import os
import random
from datetime import datetime
import json
import requests
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
    # TODO image addition
    image = db.Column(db.String, index=True)
    # TODO cost of attendance
    regular_deadline = db.Column(db.Date, index=True)
    early_deadline = db.Column(db.Date, index=True)
    plot_SAT2400 = db.Column(db.String)
    plot_SAT1600 = db.Column(db.String)
    plot_ACT = db.Column(db.String)

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
    def insert_colleges():
        college_names = {
            'University of Pennsylvania', 'Columbia University',
            'Stanford University', 'Princeton University',
            'Harvard University', 'Cornell University', 'Yale University',
            'Brown University', 'Dartmouth College', 'New York University',
            'University of California, Berkeley',
            'University of California, Los Angelos', 'University of Michigan',
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
                    description=random.choice(descriptions),
                    regular_deadline=random.choice(regular_deadlines),
                    early_deadline=random.choice(early_deadlines),
                    image=random.choice(images))
            db.session.add(college)
        db.session.commit()

    def __repr__(self):
        return '<College: {}>'.format(self.name)
