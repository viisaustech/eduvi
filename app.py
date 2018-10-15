from flask import Flask, render_template, request, jsonify, redirect
import csv
import os
from collections import Counter, OrderedDict
from operator import itemgetter
import pandas as pd
import json

#################### Global Dictionaries #################
Business_Studies = {}
Science_Mathematics = {}
Technology = {}
Humanities = {}
combined_dict = {}

############ functions to create the main dictionaries ##########################


def parse_file():
    global Business_Studies 
    global Science_Mathematics 
    global Technology 
    global Humanities
    global combined_dict
    Dict_Business_Studies = {}
    Dict_Science_Mathematics = {}
    Dict_Technology = {}
    Dict_Humanities = {}
    combined = []
    Business_Studies_subject = ['Computer Studies','Mathematics','Civic Education','Further Mathematics','English Studies','Accounting','Store Management','Office Practice','Insurance','Commerce']
    Science_Mathematics_subject = ['Computer Studies','Mathematics','Civic Education','Further Mathematics','English Studies','Biology','Chemistry','Physics','Further Mathematics','Agriculture','Physical Education','Health Education']
    Technology_subject = ['Computer Studies','Mathematics','Civic Education','Further Mathematics','English Studies','Technical Drawing','General Metalwork','Basic Electricity','Electronics','Auto_Mechanics','Building Construction','Woodwork','Home Management','Food and Nutrition','Clothing and Textiles']
    Humanities_subject = ['Computer Studies','Mathematics','Civic Education','Further Mathematics','English Studies','Edo Language','Yoruba','English Literature','Geography','Government','Christian Religious Knowledge','Islamic Religious Knowledge','History','Visual Arts','Music','French Language','Economics','Arabic']
    trade_csv = 'C:/Flaskproject/flask/trade_csv.csv'
    trade_subject = pd.read_csv(trade_csv)
    result_csv = 'C:/Flaskproject/flask/result.csv'
    result = pd.read_csv(result_csv)
    unique_session = result['session'].unique().tolist()

    #unique_student_id = result['student_id'].unique().tolist() 
    for session in unique_session:
        filtered_session = result[result.session == session]
        unique_student_id = filtered_session['student_id'].unique().tolist()
        for student_id in unique_student_id:
            filtered_student = filtered_session[filtered_session.student_id == student_id]
            count = filtered_student['subject']
            student_classs = filtered_student['student_class']
            school = filtered_student['school_name']
            student_clas = student_classs[0:1].to_string(header=None, index=None)
            student_school = school[0:1].to_string(header=None, index=None)

            #screen out student that didn't offer any trade subject and have number of subject less than 8
            if len(set(count).intersection(trade_subject)) == 0 and len(count) < 8:
                combined.extend(('','failed requirement','',student_clas,session,student_school))
                combined = []
                continue

            #sort the subject result by total score    
            result_score = sorted(filtered_student['total_score'], reverse = True)
            #select top 8 subject
            top_subject = result_score[0:8]
            #sum top 8 subject
            sum_top_subject = sum(top_subject)

            #Assign field of specialisation and top_performer if subject match is >= 7 and total_score falls within 560 to 800 respectively
            if sum_top_subject in range(560,801) and len(set(count).intersection(Business_Studies_subject)) >= 7:
                combined.extend((student_id,'Business_Studies',sum_top_subject,student_clas,session,student_school,'Top performer'))
                
                Dict_Business_Studies.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Business_Studies = Dict_Business_Studies
            elif sum_top_subject in range(560,801) and len(set(count).intersection(Science_Mathematics_subject)) >=7:
                combined.extend((student_id,'Science_Mathematics',sum_top_subject,student_clas,session,student_school,'Top performer'))
                Dict_Science_Mathematics.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Science_Mathematics = Dict_Science_Mathematics
            elif sum_top_subject in range(560,801) and len(set(count).intersection(Technology_subject)) >=7:
                combined.extend((student_id,'Technology',sum_top_subject,student_clas,session,student_school,'Top performer'))
                Dict_Technology.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
            #     Technology = Dict_Technology   
            elif sum_top_subject in range(560,801) and len(set(count).intersection(Humanities_subject)) >=7:
                combined.extend((student_id,'Humanities',sum_top_subject,student_clas,session,student_school,'Top performer'))   
                Dict_Humanities.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Humanities = Dict_Humanities

            #     # Capture under performing student under a field of specialization 
            elif len(set(count).intersection(Business_Studies_subject)) >= 7:
                combined.extend((student_id,'Business_Studies',sum_top_subject,student_clas,session,student_school,'Under performer'))
                Dict_Business_Studies.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Business_Studies = Dict_Business_Studies
            elif len(set(count).intersection(Science_Mathematics_subject)) >=7:
                combined.extend((student_id,'Science_Mathematics',sum_top_subject,student_clas,session,student_school,'Under performer'))
                Dict_Science_Mathematics.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Science_Mathematics = Dict_Science_Mathematics
            elif len(set(count).intersection(Technology_subject)) >=7:
                combined.extend((student_id,'Technology',sum_top_subject,student_clas,session,student_school,'Under performer'))
                Dict_Technology.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6])) 
                Technology = Dict_Technology   
            elif len(set(count).intersection(Humanities_subject)) >=7:
                combined.extend((student_id,'Humanities',sum_top_subject,student_clas,session,student_school,'Under performer'))   
                Dict_Humanities.setdefault(combined[4],
                    {}).setdefault(combined[3],{}).setdefault(combined[5],[]).append((combined[6]))
                Humanities = Dict_Humanities
            else: 
                combined.extend((student_id,'Less than required','under performer',student_clas,session,student_school,'Under performer'))
                Dict_Business_Studies.setdefault(combined[4],{}).setdefault(combined[3],
                    {}).setdefault(combined[5],[]).append((combined[6]))
                Science_Mathematics = Dict_Business_Studies
            
 
            # print(combined_dict)
            #### Empty list ###

            combined=[]
            
            combined_dict =  {
                'Business_Studies':Business_Studies,
                'Science_Mathematics':Science_Mathematics,
                'Technology':Technology,
                'Humanities':Humanities
                }
    
parse_file()  

topschoolbysubject = {}
def getperformingschool():
    global topschoolbysubject
    dict_topschoolbysubject = {}
    results_csv = 'C:/Flaskproject/flask/result.csv'
    results = pd.read_csv(results_csv)
    for row in results.itertuples(index=True, name='Pandas'):
        dict_topschoolbysubject.setdefault(getattr(row, "session"),{}).setdefault(getattr(row, "student_class"),
            {}).setdefault(getattr(row, "subject"),{}).setdefault(getattr(row, "school_name"),
                []).append(getattr(row, "total_score"))
    # print(dict_topschoolbysubject)
    topschoolbysubject = dict_topschoolbysubject        
getperformingschool()    

def getsubject(school_subject):
    school_list = list(school_subject.keys())
    for school in school_list:
        school_subject_list = school_subject[school]
        subject_counter = Counter(school_subject_list)
        Total_performer = sum(subject_counter.values())
        how do u select a range pf multiple keys in a dictionary
        how do u use counter to count the number of time a specific value occured



performer_dict = {}
def getschools(School_Perform_Dict): 
    global performer_dict
    performer_dict_medium = {}
    school_names = list(School_Perform_Dict.keys())
    # print(school_names)
    for school_name in school_names:
        school = School_Perform_Dict[school_name] 
        performer_counter = Counter(school)
        Total_performer = sum(performer_counter.values())
        Total_Top_Perform = performer_counter['Top performer']
        if Total_Top_Perform < 0.02*Total_performer:
            continue
        else:
            percentage = round((100*Total_Top_Perform / Total_performer),1)
            performer_dict_medium.setdefault(school_name,(percentage,Total_Top_Perform,Total_performer))
    performer_dict = performer_dict_medium   
    return performer_dict


sorted_dict = {}
def get_sorted_dict(sorted_performer):
    global sorted_dict
    sorted_dict_medium = {}
    for school, Total_Top_Perform in sorted(sorted_performer.items(), key = itemgetter(1), reverse = True):
        sorted_dict_medium.setdefault(school,Total_Top_Perform)
    sorted_dict = sorted_dict_medium
    return sorted_dict

# # get_sorted_dict(getschools(combined_dict['Science_Mathematics']['2011/2012']['SS 1']))




app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/topschoolsformpage")
def performer():
	# return render_template('TopSchools2.html')dict
    fieldOFSpecialisation = ['Science_Mathematics','Business_Studies','Humanities','Technology']
    fieldOFSpecialisation.sort()
    return render_template("topschoolsformpage.html", fieldOFSpecialisation=fieldOFSpecialisation)

@app.route("/topperformerbysubject")
def performerbysubject():
    sessions = list(topschoolbysubject.keys())
    sessions.sort()
    return render_template("topschoolsbysubjectformpage.html", data_sessions=sessions)

# # # # # global combined_dict 
# # # # # Business_Studies = {
# # # # #                     'fruit':['orange','apple','grape'],
# # # # #                     'color':['red','blue','green']
# # # # #                     }
# # # # # Humanities = {
# # # # #                     'make': {'toyota':['avensis','camry']},
# # # # #                     'species': {'animate':['man','wildanimal']}
# # # # #                     }
# # # # # combined_dict = {
# # # # #                  'Business_Studies':Business_Studies,
# # # # #                  'Humanities':Humanities
# # # # #                 } 
                   
### accepting Json value from top performing school
@app.route('/school_session', methods=['GET', 'POST'])
def getschoolsession():
    fieldkey = request.json['fieldspecialisationtext']
    school_session = list(combined_dict[fieldkey].keys())
    school_sessio = json.dumps(school_session)
    return school_sessio

@app.route('/school_class', methods=['GET', 'POST'])
def getschoolclass():
    fieldkey = request.json['fieldspecialisationtext']
    sessionkey = request.json['fieldschoolsessiontext']
    school_class = list(combined_dict[fieldkey][sessionkey].keys())
    school_clas = json.dumps(school_class)
    return school_clas

### accepting Json value from top performing school by subject 

@app.route('/school_class_bysub', methods=['GET', 'POST'])
def getschoolclass():
    sessionkey = request.json['session']
    school_session = list(topschoolbysubject[sessionkey].keys())
    school_clas = json.dumps(school_session)
    return school_clas

@app.route('/school_class', methods=['GET', 'POST'])
def getschoolclass():
    fieldkey = request.json['fieldspecialisationtext']
    sessionkey = request.json['fieldschoolsessiontext']
    school_class = list(combined_dict[fieldkey][sessionkey].keys())
    school_clas = json.dumps(school_class)
    return school_clas  



@app.route('/', methods=['POST'])
def navigate():
    # fieldinput = request.form['fieldOFSpecialisation']
    # sessioninput = request.form['session']
    # classinput = request.form['htclass']
    if request.form['submit_input'] == 'Display Results':
        return redirect("/GENERATE/{}/{}/{}".format(request.form['fieldOFSpecialisation'],
            request.form['session'], request.form['htclass']))
    else: request.form['submit_input'] == 'Result':
            return redirect("/GENERATE_Result/{}/{}/{}".format(request.form['session'],
                request.form['htclass'], request.form['subject']))

    # selectbutton = request.form['submit']



@app.route('/GENERATE/<fieldOFSpecialisation>/<session>/<htclass>')
def getcountschool_sessiones(fieldOFSpecialisation, session, htclass):
    Top_Performing_Schools = get_sorted_dict(getschools(combined_dict[fieldOFSpecialisation][session][htclass]))
    error = ''
    if not Top_Performing_Schools:
        error = 'There is no data'
        return render_template("error.html", error=error)
    else:
        # print(Top_Performing_Schools)
        return render_template("Top_Performing_Schools.html", Performing_School_Result=Top_Performing_Schools)


@app.route('/GENERATE_Result/<fieldOFSpecialisation>/<session>/<htclass>')
def getcountschool_sessiones(session, htclass, subject):        






    # return render_template('resultlevel.html',school=school_name,Total_Top_Perform=Total_Top_Perform)





if __name__ == "__main__":
	app.run(debug=True)	