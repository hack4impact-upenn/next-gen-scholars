from .. import db

import random
from datetime import datetime


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    regular_deadline = db.Column(db.Date, index=True)
    early_deadline = db.Column(db.Date, index=True)
    plot_SAT2400 = db.Column(db.String)
    plot_SAT1600 = db.Column(db.String)
    plot_ACT = db.Column(db.String)

    def update_plots(self):
        data = ScattergramData.query.filter_by(college=self.name).all()

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
            print('SAT [2400] ' + str(data[i].SAT2400))
            print('SAT [1600] ' + str(data[i].SAT1600))
            print('ACT ' + str(data[i].ACT))
            if(data[i].SAT2400):
                if(data[i].status == 'Accepted'):
                    SAT2400_Accepted.append(int(data[i].SAT2400))
                    GPA_SAT2400_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    SAT2400_Denied.append(int(data[i].SAT2400))
                    GPA_SAT2400_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Accepted)'):
                    SAT2400_Waitlisted1.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Denied)'):
                    SAT2400_Waitlisted2.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted or Deferred (Withdrew App)'):
                    SAT2400_Waitlisted3.append(int(data[i].SAT2400))
                    GPA_SAT2400_Waitlisted3.append(data[i].GPA)

            if(data[i].SAT1600):
                if(data[i].status == 'Accepted'):
                    SAT1600_Accepted.append(int(data[i].SAT1600))
                    GPA_SAT1600_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    SAT1600_Denied.append(int(data[i].SAT1600))
                    GPA_SAT1600_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Accepted)'):
                    SAT1600_Waitlisted1.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Denied)'):
                    SAT1600_Waitlisted2.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted or Deferred (Withdrew App)'):
                    SAT1600_Waitlisted3.append(int(data[i].SAT1600))
                    GPA_SAT1600_Waitlisted3.append(data[i].GPA)

            if(data[i].ACT):
                if(data[i].status == 'Accepted'):
                    ACT_Accepted.append(int(data[i].ACT))
                    GPA_ACT_Accepted.append(data[i].GPA)
                elif(data[i].status == 'Denied'):
                    ACT_Denied.append(int(data[i].ACT))
                    GPA_ACT_Denied.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Accepted)'):
                    ACT_Waitlisted1.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted1.append(data[i].GPA)
                elif(data[i].status == 'Waitlisted or Deferred (Denied)'):
                    ACT_Waitlisted2.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted2.append(data[i].GPA)
                if(data[i].status == 'Waitlisted or Deferred (Withdrew App)'):
                    ACT_Waitlisted3.append(int(data[i].ACT))
                    GPA_ACT_Waitlisted3.append(data[i].GPA)

        import plotly.tools as tools
        import plotly.plotly as py
        import plotly.graph_objs as go

        # CHANGE THIS LMAO
        tools.set_credentials_file(
            username='ktjx', api_key='xO7VaxjEmJnimiYnhKfS')

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
            name="Waitlisted or Deferred (Accepted)"
        )

        trace3 = go.Scatter(
            x=SAT2400_Waitlisted2,
            y=GPA_SAT2400_Waitlisted2,
            mode='markers',
            name="Waitlisted or Deferred (Denied)"
        )

        trace4 = go.Scatter(
            x=SAT2400_Waitlisted3,
            y=GPA_SAT2400_Waitlisted3,
            mode='markers',
            name="Waitlisted or Deferred (Withdrew App)"
        )

        layout1 = go.Layout(
            title='SAT2400 vs. GPA',
            xaxis=dict(
                title='SAT2400'
            ),
            yaxis=dict(
                title='GPA',
            )
        )

        fig1 = go.Figure(data=[trace0, trace1, trace2,
                               trace3, trace4], layout=layout1)
        self.plot_SAT2400 = py.plot(
            fig1, filename='basic-scatter1', auto_open=False)

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
            name="Waitlisted or Deferred (Accepted)"
        )

        trace8 = go.Scatter(
            x=SAT1600_Waitlisted2,
            y=GPA_SAT1600_Waitlisted2,
            mode='markers',
            name="Waitlisted or Deferred (Denied)"
        )

        trace9 = go.Scatter(
            x=SAT1600_Waitlisted3,
            y=GPA_SAT1600_Waitlisted3,
            mode='markers',
            name="Waitlisted or Deferred (Withdrew App)"
        )

        layout2 = go.Layout(
            title='SAT1600 vs. GPA',
            xaxis=dict(
                title='SAT1600'
            ),
            yaxis=dict(
                title='GPA',
            )
        )

        fig2 = go.Figure(data=[trace5, trace6, trace7,
                               trace8, trace9], layout=layout2)
        plot_SAT1600 = py.plot(
            fig2, filename='basic-scatter2', auto_open=False)

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
            name="Waitlisted or Deferred (Accepted)"
        )

        trace13 = go.Scatter(
            x=ACT_Waitlisted2,
            y=GPA_ACT_Waitlisted2,
            mode='markers',
            name="Waitlisted or Deferred (Denied)"
        )

        trace14 = go.Scatter(
            x=ACT_Waitlisted3,
            y=GPA_ACT_Waitlisted3,
            mode='markers',
            name="Waitlisted or Deferred (Withdrew App)"
        )

        layout3 = go.Layout(
            title='ACT vs. GPA',
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
            fig3, filename='basic-scatter3', auto_open=False)

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
            'Private research university',
            'Ivy League university',
            'Liberal arts college',
            'Public research university',
            'Private doctorate university'
        ]

        for c in college_names:
            college = College.get_college_by_name(c)
            if college is None:
                college = College(name=c, description=random.choice(descriptions),
                                  regular_deadline=random.choice(
                                      regular_deadlines),
                                  early_deadline=random.choice(early_deadlines))
            db.session.add(college)
        db.session.commit()

    def __repr__(self):
        return '<College: {}>'.format(self.name)
