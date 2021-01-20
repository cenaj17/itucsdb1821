from flask import Flask, request, jsonify, render_template
import dbinit

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/profile")
def profile():
    return render_template("profile.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/profile_student")
def profile_student():
    return render_template("profile_student.html")
    
@app.route("/profile_employer")
def profile_employer():
    return render_template("profile_employer.html")


@app.route('/login_employer',methods=['POST'])
def login_employer():
    email = request.args.get('email')
    password = request.args.get('password')
    res = dbinit.login_employer(email,password)
    ret = {
        "flag":res[0],
        "id":res[1]
    }
    return jsonify(ret)

@app.route('/signup_employer',methods=['POST'])
def signup_employer():
    email = request.args.get('email')
    name = request.args.get('name')
    password = request.args.get('password')
    res = dbinit.signup_employer(email,password)
    ret = {
        "flag":res[0],
        "id":res[1]
    }
    return jsonify(ret)

#student login
@app.route('/student_login',methods=['POST'])
def student_login():
    email = request.args.get('email')
    password = request.args.get('password')
    res = dbinit.student_login(email, password)
    ret = {
        "flag":res[0],
        "id":res[1]
    }
    return jsonify(ret)


#student signup
@app.route('/student_signup',methods=['POST'])
def student_signup():
    email = request.args.get('email')
    password = request.args.get('password')

    res = dbinit.student_signup(email,password)

    ret = {
        "flag":res[0],
        "id":res[1]
    }
    return jsonify(ret)


#student profile
@app.route('/student_profile',methods=['GET'])
def stu_detail():
    stu_id = request.args.get('student_id')
    res = dbinit.student_profile(student_id)
    ret = {
        "id":res[0],
        "name": res[1],
        "university":res[2],
        "skills":res[3]
    }
    return jsonify(ret)


#student add skill
@app.route('/skill_adding',methods=["POST"])
def add_skill():
    name = request.args.get('name')
    desc = request.args.get('desc')
    res = dbinit.add_skill(name,desc)
    ret = {
        "flag":res[0],
        "skill_id":res[1]
    }
    return jsonify(ret)

#job application add
@app.route("/job_app_add",methods=["POST"])
def add_job_listing():
    company_id = request.args.get('company')
    desc = request.args.get('desc')
    
    res = dbinit.add_job_listing(company_id)
    ret = {
        "flag":res[0],
        "job_id":res[1]
    }
    if ret["flag"]:
        dbinit.update_joblisting_location(ret["job_id"])
    return jsonify(ret)

#all jobs page
@app.route("/jobs",methods=["GET"])
def all_jobs():
    res = dbinit.get_all_jobs()
    t = []
    for i in range(len(res)):

        s = {
            "id":res[i][0],
            "company_id": res[i][1],
            "job_desc":res[i][2],  
            "company_name":res[i][3],
            "skill_list":res[i][4],
            "skill_id":res[i][5]
        }
        t.append(s)
    ret = {"jobs":t }
    return (jsonify(ret))


@app.route('/search_byskill',methods=["GET"])
def search_jobs_by_skill():
    term = request.args.get('term')
    res = dbinit.search_jobs_by_skill(term)
    t = []
    for ii in range(len(res)):

        s = {
            "id":res[ii][0],
            "company_id": res[ii][1],
            "skill_list":res[ii][2],
            "skill_id":res[ii][3]
        }
        t.append(s)
    ret = {"students":t }
    return jsonify(ret)

@app.route('/search_byskillids',methods=["GET"])
def search_jobss_by_skill_ids():
    term = request.args.get('term')
    res = dbinit.search_jobs_by_skill_ids(term)
    t = []
    for ii in range(len(res)):

        s = {
            "id":res[ii][0],
            "company_id": res[ii][1],
            "job_desc":res[ii][2],  
            "company_name":res[ii][3],
            "skill_list":res[ii][4],
            "skill_ids":res[ii][5]
        }
        t.append(s)
    ret = {"students":t }
    return jsonify(ret)


@app.route('/jobs',methods=["GET"])
def search_jobs():
    term = request.args.get('term')
    res = dbinit.jobs(term)
    t = []
    for ii in range(len(res)):

        s = {
            "id":res[ii][0],
            "company_id": res[ii][1],
            "job_desc":res[ii][2],  
            "company_name":res[ii][3],
            "skill_list":res[ii][4],
            "skill_ids":res[ii][5]
        }
        t.append(s)
    ret = {"students":t }
    return jsonify(ret)

@app.route("/applications_of_student",methods=["GET"])
def applications_of_student():
    student_id = request.args.get('student_id')
    result = dbinit.get_applications_of_student(student_id)
    t = []
    for ii in range(len(result)):

        s = {
            "job_id":res[ii][0],
            "student_id": res[ii][1],
            "company_id":res[ii][2],
            "description":res[ii][3],
            "company_name":res[ii][4]
        }
        t.append(s)
    ret = {"students":t }
    return jsonify(ret)


if __name__ == "__main__":
    app.run(debug=True,port=9090)