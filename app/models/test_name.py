from .. import db


class TestName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    @staticmethod
    def get_test_by_name(name):
        return TestName.query.filter_by(name=name).first()

    @staticmethod
    def insert_tests():
        test_names = {
            'SAT', 'ACT', 'AP Computer Science A', 'AP Chemistry',
            'AP Physics 1', 'AP Physics 2', 'SAT Subject Test - Math Level 2',
            'SAT Subject Test - Math Level 1', 'SAT Subject Test - Physics',
            'AP English Language & Composition', 'SAT Subject Test - Chemistry'
        }

        for t in test_names:
            test = TestName.get_test_by_name(t)
            if test is None:
                test = TestName(name=t)
            db.session.add(test)
        db.session.commit()

    def __repr__(self):
        return '<Test Name: {}>'.format(self.name)
