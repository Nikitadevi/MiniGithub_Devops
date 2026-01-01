from flask import Flask, render_template, request
import requests
import subprocess

app = Flask(__name__)

# ------------------- HOME PAGE -------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------- FULL COMMIT HISTORY FROM GITHUB API -------------------
@app.route("/commits")
def show_commits():
    repo_owner = "Nikitadevi"   # your GitHub username
    repo_name = "MiniGithub_DevopsProject"  # your GitHub repo name

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    response = requests.get(url)
    data = response.json()

    html = """
    <h1 style='font-family:Arial;'>Commit History</h1>
    <table border='1' cellpadding='8' style='border-collapse:collapse;font-family:Arial;width:90%;'>
    <tr><th>Hash</th><th>Message</th><th>Author</th><th>Date</th></tr>
    """

    for commit in data:
        sha = commit['sha'][:7]
        message = commit['commit']['message']
        author = commit['commit']['author']['name']
        date = commit['commit']['author']['date'][:10]

        html += f"<tr><td>{sha}</td><td>{message}</td><td>{author}</td><td>{date}</td></tr>"

    html += "</table>"
    return html


# ------------------- BRANCH LIST -------------------
@app.route("/branches")
def show_branches():
    branches = subprocess.getoutput("git branch -a")
    branches_list = branches.split("\n")

    html = "<h1 style='font-family:Arial;'>Available Branches</h1>"
    html += "<ul style='font-size:20px;font-family:Arial;'>"

    for b in branches_list:
        html += f"<li>{b}</li>"
    html += "</ul>"
    return html


# ------------------- GIT STATUS -------------------
@app.route("/status")
def git_status():
    status = subprocess.getoutput("git status")
    return f"<h1 style='font-family:Arial;'>Git Status</h1><pre>{status}</pre>"


# ------------------- RUN GIT COMMANDS THROUGH UI -------------------
@app.route("/run", methods=["GET", "POST"])
def run_git_command():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("gitcmd")
        output = subprocess.getoutput(cmd)

    return f"""
    <h2 style='font-family:Arial;'>Run Git Command</h2>
    <form method='POST'>
        <input name='gitcmd' placeholder='Enter git command' style='width:300px;padding:8px;'>
        <button type='submit' style='padding:8px 16px;'>Run</button>
    </form>
    <pre>{output}</pre>
    """


# ------------------- RUN FLASK -------------------
if __name__ == "__main__":
    app.run(debug=True)
