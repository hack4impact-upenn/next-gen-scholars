from .. import db

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_url = db.Column(db.String, index=True)
    title = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    image_url = db.Column(db.String, index=True)

    @staticmethod
    def insert_resources():
        resources = (
           ('https://www.princetonreview.com/college-advice/college-essay',
            'Writing a Personal Essay', 
            'Tips and tricks on how to write a personal essay from the UC System!',
            'https://clipartstation.com/wp-content/uploads/2018/09/essay-clipart-4.jpg'), 

           ('https://www.youtube.com/watch?time_continue=3&v=LK0bbu0y5AM',
            'Completing the FAFSA', 
            'Having trouble with the FAFSA? Want to learn more about the process? Here is a useful guide on what to do.',
            'https://moneydotcomvip.files.wordpress.com/2017/03/170310_fafsa.jpg'), 

           ('https://www.collegeessayguy.com/blog/college-interview',
            'Interviews', 
            'Nervous about an upcoming college interview? Here are some useful tricks on how to ace your next interview.',
            'http://images.clipartpanda.com/interview-clipart-Interview.png'),

           ('https://bigfuture.collegeboard.org/find-colleges/how-find-your-college-fit',
            'Choosing the Right Schools', 
            'Find your perfect school with some tips from Collegeboard.',
            'http://www.cnf.cornell.edu/image/cornell_fall_sunset.jpg')
        )

        for r in resources:
            r_url = r[0]
            r_title = r[1]
            r_description = r[2]
            r_image_url = r[3]

            resource = Resource (
                resource_url=r_url, 
                title=r_title,
                description=r_description,
                image_url=r_image_url
            )
            
            db.session.add(resource)
        db.session.commit()

    @staticmethod
    def add_resource():
        #TODO: Me
        db.add('resource')
        db.session.commit()

    def __repr__(self):
        return '<Resource: {}>'.format(self.resource_url)
