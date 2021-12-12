"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""


"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""


from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, Field, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user
from py4web.utils.form import Form, FormStyleBulma

url_signer = URLSigner(session)

#index is the main page.
@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    print("User:", get_user_email())
    students = db((db.student.student_id == get_user())).select()
    for student in students:
        if student.is_admin:
            redirect(URL('indexAdmin', signer=url_signer))
            return
    rowsFresh = []
    rowsSoph = []
    rowsJunior = []
    rowsSenior = []
    rowsExtra = []
    rowsSuggest = []
    season = "None"
    theRows= db(db.studentCourse.student_id == get_user()).select()
    total_units = ""
    for i in range(0, 4):
        rowsFresh.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsSoph.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsJunior.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsSenior.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsExtra.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})

    for row in theRows:
        if row.year == "Freshman":
            rowsFresh[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Sophomore":
            rowsSoph[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Junior":
            rowsJunior[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Senior":
            rowsSenior[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Extra":
            rowsExtra[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"

    units = 0
    for row in theRows:
        try:
            nextUnitValue=int((db(db.course.id == row.course_id).select())[0].unit)
        except:
            nextUnitValue = 0

        units+=nextUnitValue
    total_units = "Total Units: " + str(units)

    return dict(rowsFresh = rowsFresh, rowsSoph = rowsSoph, rowsJunior=rowsJunior, rowsSenior= rowsSenior, rowsExtra= rowsExtra, rowsSuggest = rowsSuggest,season=season, total_units = total_units, url_signer=url_signer)


#edit_course is for when a user presses one of the edit buttons on main page.
@action('edit_course/<period:int>/<season>/<year>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit_course.html', url_signer.verify())
def edit_course(period=None, season=None, year=None):
    assert period is not None
    assert season is not None
    assert year is not None

    courses = db(db.course).select()

    for course in courses:
        warning = ""
        if db((db.studentCourse.student_id == get_user()) & (db.studentCourse.course_id == course.id)).count() > 0:
            warning+="Already taken.  "
        if (season == "Fall" and not course.offered_fall) or (season == "Winter" and not course.offered_winter) or (season == "Spring" and not course.offered_spring) or(season == "Summer" and not course.offered_summer):
            warning+="  Not available this quarter."
        course["warning"] = warning

    return dict(year=year, season=season, period=period, courses=courses, url_signer=url_signer)

#add course is for when a user adds a course on the main page.
@action('add_course/<course_id:int>/<period:int>/<season>/<year>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def add_course(course_id=None, period=None, season=None, year=None):
    assert period is not None
    assert season is not None
    assert year is not None
    assert course_id is not None

    student_id = get_user()
    db((db.studentCourse.student_id == student_id) & (db.studentCourse.season == season) & (db.studentCourse.year == year) & (db.studentCourse.period == period)).delete()
    db.studentCourse.insert(student_id=get_user(), course_id=course_id, season=season, year=year, period=period)

    redirect(URL('index', signer=url_signer))

#delete course is for when a student deletes course on the main page.
@action('delete_course/<period:int>/<season>/<year>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(period=None, season=None, year=None):
    assert period is not None
    assert season is not None
    assert year is not None
    db((db.studentCourse.student_id == get_user()) & (db.studentCourse.season == season) & (db.studentCourse.year == year) & (db.studentCourse.period == period)).delete()
    redirect(URL('index', signer=url_signer))


#Suggest Course Functionality
@action('suggest_courses')
@action.uses(db, auth.user, 'index.html')
def suggest_courses():
    print("User:", get_user_email())
    students = db((db.student.student_id == get_user())).select()
    for student in students:
        if student.is_admin:
            redirect(URL('indexAdmin', signer=url_signer))
            return
    rowsFresh = []
    rowsSoph = []
    rowsJunior = []
    rowsSenior = []
    rowsExtra = []
    rowsSuggest = []
    theRows= db(db.studentCourse.student_id == get_user()).select()
    allCourses = db(db.course).select()
    total_units = ""
    for i in range(0, 4):
        rowsFresh.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsSoph.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsJunior.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsSenior.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})
        rowsExtra.append({ 'period': i, 'Fall': '', 'Winter': '', 'Spring': '', 'Summer': ''})


    for row in theRows:
        if row.year == "Freshman":
            rowsFresh[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Sophomore":
            rowsSoph[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Junior":
            rowsJunior[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Senior":
            rowsSenior[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"
        elif row.year == "Extra":
            rowsExtra[row.period][row.season]= db.course[row.course_id].name + "   (" + db.course[row.course_id].unit + ")"


    print(db(db.course.id == 2).select().first().name)
    season, a, b, c = suggestCourses(db)
    rowsSuggest.append({'period': 0, 'Value': a})
    rowsSuggest.append({'period': 1, 'Value': b})
    rowsSuggest.append({'period': 2, 'Value': c})

    units = 0
    for row in theRows:
        try:
            nextUnitValue=int((db(db.course.id == row.course_id).select())[0].unit)
        except:
            nextUnitValue = 0

        units+=nextUnitValue

    total_units = "Total Units: " + str(units)


    return dict(rowsFresh = rowsFresh, rowsSoph = rowsSoph, rowsJunior=rowsJunior, rowsSenior= rowsSenior, rowsExtra= rowsExtra, rowsSuggest=rowsSuggest, season=season, total_units = total_units, url_signer=url_signer)

#about page
@action('about', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'about.html', url_signer.verify())
def about():
    return dict(url_signer=url_signer)

#requirements page
@action('requirements', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'requirements.html', url_signer.verify())
def requirements():
    return dict(url_signer=url_signer)

####################
#Admin Functionality
####################

#Course Modification

#Index of admin page.
@action('indexAdmin')
@action.uses(db, auth.user, 'indexAdmin.html')
def indexAdmin():
    print("User:", get_user_email())
    courses = db(db.course).select()
    requirements = db(db.requirement).select()
    for course in courses:
        offered = ""
        if course.offered_fall:
            offered = offered + "Fall "
        if course.offered_winter:
            offered = offered + "Winter "
        if course.offered_spring:
            offered = offered + "Spring "
        if course.offered_summer:
            offered = offered + "Summer "
        course["offered"] = offered
    for requirement in requirements:
        course_or_requirement = ""
        if requirement.course_or_requirement:
            course_or_requirement = "Course"
        elif not requirement.course_or_requirement:
            course_or_requirement = "Requirement"
        requirement["course_or_requirement"] = course_or_requirement
    return dict(courses=courses, requirements=requirements, url_signer=url_signer)

#Add course function for admin page, so that admins can add new courses.
@action('addCourse', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'addCourse.html')
def addCourse():
    form = Form(db.course, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('indexAdmin'))
    return dict(form=form)

#Edit course function for admin page, so that admins can edit the information of courses.
@action('editCourse/<course_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'editCourse.html')
def edit(course_id=None):
    assert course_id is not None
    # p = db(db.bird.id == bird_id).select().first()
    p = db.course[course_id]
    if p is None:
        redirect(URL('indexAdmin'))
    form = Form(db.course, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('indexAdmin'))
    return dict(form=form)

#Delete course function for admin page, so that admins can delete courses.
@action('deleteCourse/<course_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(course_id=None):
    assert course_id is not None
    db(db.course.id == course_id).delete()
    redirect(URL('indexAdmin'))

#Requirement Modification
#Add requirement functions for admins.
@action('addRequirement', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'addRequirement.html')
def addCourse():
    form = Form(db.requirement, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('indexAdmin'))
    return dict(form=form)

#Edit requirement functions for the admin page.
@action('editRequirement/<requirement_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'editRequirement.html')
def edit(requirement_id=None):
    assert requirement_id is not None
    # p = db(db.bird.id == bird_id).select().first()
    p = db.requirement[requirement_id]
    if p is None:
        redirect(URL('indexAdmin'))
    form = Form(db.requirement, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('indexAdmin'))
    return dict(form=form)

#Delete function for the admin page, so that admins can delete requirements.
@action('deleteRequirement/<requirement_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(requirement_id=None):
    assert requirement_id is not None
    db(db.requirement.id == requirement_id).delete()
    redirect(URL('indexAdmin'))

#Helper functions
def next_season(season):
    if season == "Fall":
        return "Winter"
    elif season == "Winter":
        return "Spring"
    elif season == "Spring":
        return "Fall"
    elif season == "Summer":
        return "Fall"
    
#An algorithm to suggest potential courses for the next quarter.
def suggestCourses(db):
    years=["Extra", "Senior", "Junior", "Sophomore", "Freshman"]
    seasons=["Summer", "Spring","Winter","Fall"]
    nextSeason = "Fall"
    recommendations= []
    found = False
    for year in years:
        for season in seasons:
            if(db((db.studentCourse.student_id == get_user()) & (db.studentCourse.year == year) & (db.studentCourse.season == season)).count() != 0):
                nextSeason = next_season(season)
                found = True
                break
        if found:
            break

    allSuggestions = ["CSE 20", "CSE 30", "MATH 19A", "CSE 12", "MATH 19B", "CSE 13S", "AM 10", "AM 30", "CSE 16", "CSE 101", "CSE 107", "ECE 30", "CSE 102", "Elective", "CSE 103", "Elective", "CSE 120", "DC Elective", "CSE 116", "Elective", "CSE 130", "Capstone Elective"]

    allCourses = db(db.course).select()
    for course in allCourses:
        if(db((db.studentCourse.student_id == get_user()) & (db.studentCourse.course_id == course.id)).count() == 0):
            if nextSeason == "Fall" and course.offered_fall:
                recommendations.append(course.name)
            elif nextSeason == "Winter" and course.offered_winter:
                recommendations.append(course.name)
            elif nextSeason == "Spring" and course.offered_spring:
                recommendations.append(course.name)
        if len(recommendations) ==2:
            break

    if len(recommendations) == 1:
        return nextSeason, recommendations[0], "GE", "Elective"
    if len(recommendations) == 0:
        return nextSeason, "GE", "GE", "Elective"

    return nextSeason, recommendations[0], recommendations[1], "Elective"


