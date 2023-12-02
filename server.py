from flask import Flask, request, render_template, redirect
from json import load
import get_schedule

app = Flask(__name__)


@app.route("/")
@app.route("/faculties")
def post_faculties():
    with open("groups.json", encoding='utf-8') as f:
        data = load(f)

    faculties = {}
    for faculty, groups in data.items():
        faculties[faculty] = groups['id']

    return render_template('faculties.html', faculties=faculties)


@app.route("/faculties/<int:facultyId>/groups")
def post_groups(facultyId):
    with open("groups.json", encoding='utf-8') as f:
        data = load(f)

    for faculty, grouplist in data.items():
        if int(grouplist['id']) == facultyId:
            return render_template('groups.html', groups=grouplist['groups'])

    return redirect(f"/faculties/{facultyId}", 404)

@app.route("/schedule/groups")
def post_schedule():
    groupId = request.args.get('groupId', type=str)
    week = request.args.get('week', type=int)
    if week is None:
        url = f"https://ssau.ru/rasp?groupId={groupId}"
    else:
        url = f"https://ssau.ru/rasp?groupId={groupId}&selectedWeek={str(week)}&selectedWeekday=1"
    get_schedule.parser(url)
    with open("schedule.json", encoding='utf-8') as f:
        schedule = load(f)

    return render_template('schedule.html', groupId=groupId, title=schedule['title'], weeks=schedule['weeks'],
                           dates=schedule['dates'], rows=schedule['rows'])


@app.route("/schedule/staff")
def post_staff():
    print(123)
    staffId = request.args.get('staffId', type=str)
    week = request.args.get('week', type=int)

    if week is None:
        url = f"https://ssau.ru/rasp?staffId={staffId}"
    else:
        url = f"https://ssau.ru/rasp?staffId={staffId}&selectedWeek={str(week)}&selectedWeekday=1"

    get_schedule.parser(url)
    with open("schedule.json", encoding='utf-8') as f:
        schedule = load(f)

    return render_template('staff_schedule.html', staffId=staffId, title=schedule['title'], weeks=schedule['weeks'],
                           dates=schedule['dates'], rows=schedule['rows'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
