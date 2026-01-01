from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# ------------------- SHOW COMMITS AS TABLE ---------------------
@app.route("/commits")
def show_commits():
    logs = subprocess.getoutput("git log --pretty=format:'%h - %s - %an - %ad' --date=short")
    logs_list = logs.split("\n")

    html = "<h2 style='font-family:Arial;'>Commit History</h2>"
    html += "<table border='1' cellpadding='8' style='border-collapse:collapse;font-family:Arial;'>"
    html += "<tr><th>Hash</th><th>Message</th><th>Author</th><th>Date</th></tr>"

    for log in logs_list:
        parts = log.split(" - ")
        if len(parts) == 4:
            html += f"<tr><td>{parts[0]}</td><td>{parts[1]}</td><td>{parts[2]}</td><td>{parts[3]}</td></tr>"

    html += "</table>"
    return html


# ------------------- SHOW BRANCHES LIST ---------------------
@app.route("/branches")
def show_branches():
    branches = subprocess.getoutput("git branch")
    branches_list = branches.split("\n")

    html = "<h2 style='font-family:Arial;'>Available Branches</h2><ul style='font-size:20px;'>"
    for b in branches_list:
        html += f"<li>{b}</li>"
    html += "</ul>"

    return html

# ------------------- SHOW GIT STATUS ---------------------
@app.route("/status")
def git_status():
    status = subprocess.getoutput("git status")
    return f"<h2 style='font-family:Arial;'>Git Status</h2><pre>{status}</pre>"


# Run Git Command through UI
@app.route("/run", methods=["GET", "POST"])
def run_git_command():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("gitcmd")
        output = subprocess.getoutput(cmd)

    return f"""
    <h2>Run Git Command</h2>
    <form method='POST'>
        <input name='gitcmd' placeholder='Enter git command' style='width:300px;padding:8px;'/>
        <button type='submit' style='padding:8px 16px;'>Run</button>
    </form>
    <pre>{output}</pre>
    """


if __name__ == "__main__":
    app.run(debug=True)
