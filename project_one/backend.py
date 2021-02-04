from flask import Flask
import simplejson as json
from flask import request
import project_one.src.models as models
import project_one.src.db as db
import pandas as pd
from collections import defaultdict

def create_app(database='project_one', testing = False, debug = True):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=database,
        DEBUG = debug,
        TESTING = testing
    )

    @app.route('/')
    def root_url():
        return 'Welcome to Schoolsy - always find the best school!'

    @app.route('/schools')
    def schools():
        conn = db.get_db()
        cursor = conn.cursor()
        
        schools = db.find_all(models.Schools, cursor)
        school_dict = [school.__dict__ for school in schools]
        
        scores = db.find_all(models.Scores, cursor)
        scores_dict = [score.__dict__ for score in scores]
        for score in scores_dict:
                score['id'] = score.pop('school_id')

        attendances = db.find_all(models.Attendance, cursor)
        attendance_dict = [attendance.__dict__ for attendance in attendances]
        for attendance in attendance_dict:
                attendance['id'] = attendance.pop('school_id')

        populations = db.find_all(models.Population, cursor)
        population_dict = [population.__dict__ for population in populations]
        for population in population_dict:
                population['id'] = population.pop('school_id')

        merged = defaultdict(dict)
        for l in (scores_dict,attendance_dict,population_dict,school_dict):
            for elem in l:
                merged[elem['id']].update(elem)
        
        return json.dumps(merged,default= str)


    @app.route('/schools/<id>')
    def attendance_id(id):
        conn = db.get_db()
        cursor = conn.cursor()
        school_obj = db.find(models.Schools, id, cursor)
        school =  json.dumps(school_obj.__dict__, default = str)
        return school

    return app



app = create_app()
app.run(debug = True)
