import random
from faker import Faker
from .. import db
from sqlalchemy.orm import validates
from datetime import datetime

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    deadline = db.Column(db.Date)
    award_amount = db.Column(db.Float, index=True)
    category = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    merit_based = db.Column(db.Boolean, default=False)
    service_based = db.Column(db.Boolean, default=False)
    need_based = db.Column(db.Boolean,default=False)
    minimum_gpa = db.Column(db.Float, index=True)
    interview_required = db.Column(db.Boolean, default=False)
    link = db.Column(db.String, index=True)
    status = db.Column(db.String, index=True)


    @staticmethod
    def get_scholarship_by_name(name):
        return Scholarship.query.filter_by(name=name).first()


    @validates('status')
    def validate_status(self, key, status):
        assert status in [
            'Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done'
        ]
        return status

    @validates('category')
    def validate_category(self, key, category):
        assert category in [
            'African-American', 'Agriculture', 'Arts-related','Asian','Asian Pacific American',
            'Community Service','Construction Related Fields','Disabled','Engineering',
            'Environmental Interest','Female','Filipino','First Generation College Student',
            'Queer','General -- Open to All','Latinx','Immigrant/AB540/DACA','Interest in Journalism',
            'Japanese','Jewish','Indigenous','Open to All Grade Levels','Science/Engineering',
            'Student-Athlete','Teaching','Women in Math/Engineering'
        ]

    @staticmethod
    def insert_scholarships():
        scholarship_names = {
            'Science Scholar', 'Math Achievement Scholarship', 'Music Scholarship',
            'Oldham Scholarship', 'Boatwright Scholarship', 'Bonner Scholarship',
        }
        category = [
            'African-American', 'Agriculture', 'Arts-related','Asian','Asian Pacific American',
            'Community Service','Construction Related Fields','Disabled','Engineering',
            'Environmental Interest','Female','Filipino','First Generation College Student',
            'Queer','General -- Open to All','Latinx','Immigrant/AB540/DACA','Interest in Journalism',
            'Japanese','Jewish','Indigenous','Open to All Grade Levels','Science/Engineering',
            'Student-Athlete','Teaching','Women in Math/Engineering'
        ]

        deadline = [
            datetime(2017, 11, 4),
            datetime(2017, 11, 3),
            datetime(2017, 11, 2)
        ]
        award_amount = [
            50000, 20000, 10000
        ]
        statuses = [
            'Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done'
        ]

        description = [
            'Full Ride Scholarship','Awards for Females Interested in Math',
            'Scholarship Awards Up to $1000'
        ]
        merit_based = [
            'True','False'
        ]
        service_based = [
            'True', 'False'
        ]
        need_based = [
            'True', 'False'
        ]
        minimum_gpa = [
        4.0, 3.5, 3.0, 2.5, 2.0
        ]
        interview_required = [
            'True', 'False'
        ]
        link = [
            'https://google.com'
        ]

        for i in scholarship_names:
            scholarship = Scholarship.get_scholarship_by_name(i)
            if scholarship is None:
                scholarship = Scholarship(
                    name = i,
                    deadline = random.choice(deadline),
                    award_amount = random.choice(award_amount),
                    category = random.choice(category),
                    description = random.choice(description),
                    merit_based = random.choice(merit_based),
                    service_based = random.choice(service_based),
                    need_based = random.choice(need_based),
                    minimum_gpa = random.choice(minimum_gpa),
                    interview_required = random.choice(interview_required),
                    link = random.choice(link),
                    status = random.choice(statuses))
                db.session.add(scholarship)
            db.session.commit()
        

        # return scholarships
    def __repr__(self):
        return '<Scholarship: {}>'.formate(self.name)
