import project_one.src.models as models
import project_one.src.db as db
import project_one.src.adapters as adapters
from project_one.src.adapters import school_loc_details,attn_pop_details,score_details
import psycopg2
import json
import pdb


class ParentBuilder:

    def school_run(self,school_details=school_loc_details,conn=db.conn_dev):
        cursor = conn.cursor()
        schools = SchoolBuilder().run(school_details, conn, cursor)
        return schools

    def attn_run(self,school_details=attn_pop_details,conn=db.conn_dev):
        cursor = conn.cursor()
        attendance = AttendanceBuilder().run(school_details, conn, cursor)
        return attendance

    def pop_run(self,school_details=attn_pop_details,conn=db.conn_dev):
        cursor = conn.cursor()
        population = PopulationBuilder().run(school_details, conn, cursor)
        return population

    def scores_run(self,school_details=score_details,conn=db.conn_dev):
        cursor = conn.cursor()
        scores = ScoresBuilder().run(school_details, conn, cursor)
        return scores
        
class SchoolBuilder:
 
    attributes = ['nyc_id', 'name','address',
        'zipcode','lat_lon','borough']

    def select_attributes(self, school_data):
          schools = []
          for d in school_data:
            if d.get('location_category_description') == 'High school':
              nyc_id,name,address = d.get('ats_system_code','').strip(),d.get('location_name',''),d.get('primary_address_line_1','').strip()
              zipcode = json.loads(d.get('location_1','')['human_address'])['zip']
              borough = json.loads(d.get('location_1','')['human_address'])['city']
              lat_lon = d.get('location_1','')['latitude'] + ',' +  d.get('location_1','')['longitude']
              schools.append(dict(zip(self.attributes,[nyc_id, name, address, zipcode,lat_lon,borough])))
          return schools
    
    def run(self, school_data, conn, cursor):
        selected = self.select_attributes(school_data)
        schools_written = []
        for select in selected:
            nyc_id = select['nyc_id'] 
            schools = models.Schools.find_by_id(nyc_id, cursor)
            if schools:
                schools.exists = True
            else:
                schools = db.save(models.Schools(**select), conn, cursor)
                schools.exists = False
                schools_written.append(schools)
        return schools_written

class PopulationBuilder:

    population_attributes = ['school_id','english_language_learners','percent_students_disabilities','economic_needs_idx'] 
                
    def select_attributes(self, school_data, cursor):
        schools = []
        for d in school_data:
            dbn=d.get('dbn','')
            school_reference_id = models.Schools.reference_by_id(dbn,cursor)
            school_id = school_reference_id
            if school_reference_id:
                english_language_learners=d.get('percent_english_language',' ')
                percent_students_disabilities=d.get('percent_students_with','')
                economic_needs_idx=d.get('economic_need_index','')
                schools.append(dict(zip(self.population_attributes,[school_id, english_language_learners, percent_students_disabilities, economic_needs_idx])))
        return schools

    def run(self, school_data, conn, cursor):
        selected = self.select_attributes(school_data,cursor)
        schools_written = []
        for select in selected:
            school_id = select['school_id'] 
            population = models.Population.find_by_id(school_id, cursor)
            if population:
                population.exists = True
            else:
                population = db.save(models.Population(**select), conn, cursor)
                population.exists = False
                schools_written.append(population)
        return schools_written

class AttendanceBuilder:

    attendance_attributes = ['school_id','enrollment', 'student_attendance', 
                'teacher_attendance','year'] 
                
    def select_attributes(self, school_data,cursor):
        schools = []
        for d in school_data:
            dbn=d.get('dbn','')
            school_reference_id = models.Schools.reference_by_id(dbn,cursor)
            if school_reference_id:
                school_id = school_reference_id
                enrollment=d.get('enrollment',' ')
                student_attendance=d.get('student_attendance_rate','')
                teacher_attendance=d.get('teacher_attendance_rate','')
                schools.append(dict(zip(self.attendance_attributes,[school_id, enrollment, student_attendance, teacher_attendance])))
        return schools

    def run(self, school_data, conn, cursor):
        selected = self.select_attributes(school_data,cursor)
        schools_written = []
        for select in selected:
            school_id = select['school_id'] 
            attendance = models.Attendance.find_by_id(school_id, cursor)
            if attendance:
                attendance.exists = True
            else:
                attendance = db.save(models.Attendance(**select), conn, cursor)
                attendance.exists = False
                schools_written.append(attendance)
        return schools_written


class ScoresBuilder:

    scores_attributes = ['school_id','avg_score_sat_math', 'avg_score_sat_reading_writing', 'tot_sat_score',
                'graduation_rate','ars_english','ars_algebra'] 
    
                
    def select_attributes(self, school_data, cursor):
        schools = []
        for d in school_data:
            dbn=d.get('DBN','')
            school_reference_id = models.Schools.reference_by_id(dbn,cursor)
            if school_reference_id:
                school_id = school_reference_id
                avg_score_sat_math=d.get(' Average Score SAT Math','')
                avg_score_sat_reading_writing=d.get('Average Score SAT Reading and Writing','')
                tot_sat_score = avg_score_sat_math+avg_score_sat_reading_writing
                tot_sat_score=round(tot_sat_score,2)
                graduation_rate=d.get('4-Year Graduation Rate','')               
                ars_english=d.get('Average Regents Score - English ','')
                ars_algebra=d.get(' Average Regents Score - Algebra I ','')
                schools.append(dict(zip(self.scores_attributes,[school_id,avg_score_sat_math, avg_score_sat_reading_writing,tot_sat_score,graduation_rate,ars_english,ars_algebra])))
        return schools

    def run(self, school_data, conn, cursor):
        selected = self.select_attributes(school_data,cursor)
        schools_written = []
        for select in selected:
            school_id = select['school_id'] 
            scores = models.Scores.find_by_id(school_id, cursor)
            if scores:
                scores.exists = True
            else:
                scores = db.save(models.Scores(**select), conn, cursor)
                scores.exists = False
                schools_written.append(scores)
        return schools_written