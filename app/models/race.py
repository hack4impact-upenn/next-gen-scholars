from .. import db


class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    @staticmethod
    def get_race_by_name(name):
        return Race.query.filter_by(name=name.title()).first()

    @staticmethod
    def insert_races():
        race_names = { 'African-American',
       'Agriculture', 'Arts-related', 'Asian', 'Asian Pacific American', 'Community Service',
       'Construction-related Fields', 'Disabled', 'Engineering', 'Enviornmental Interest',
       'Female', 'Filipino', 'First Generation College Student', 'Queer', 'General-open to all',
       'Latinx', 'Immigrant/AB540/DACA', 'Interest in Journalism', 'Japanese', 'Jewish',
       'Indigenous', 'Open to all grade levels', 'Science/Engineering', 'Student-Athlete',
       'Teaching', 'Women in Math/Engineering'
        }
        for r in race_names:
            race = Race.get_race_by_name(r)
            if race is None:
                race = Race(name=r)
            db.session.add(race)
        db.session.commit()

    def __repr__(self):
        return '<Major: {}>'.format(self.name)
