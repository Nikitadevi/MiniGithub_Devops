from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Home Page (Main Website)
@app.route("/")
def home():
    return render_template("index.html")

# 1. Show Commit History
@app.route("/commits")
def commits():
    logs = subprocess.getoutput("git log --oneline")
    return f"<h2 style='font-family:Arial;'>Commit History</h2><pre>{logs}</pre>"

# 2. Show Branches
@app.route("/branches")
def branches():
    branches = subprocess.getoutput("git branch")
    return f"<h2 style='font-family:Arial;'>Branches</h2><pre>{branches}</pre>"

# 3. Show Git Status
@app.route("/status")
def status():
    status = subprocess.getoutput("git status")
    return f"<h2 style='font-family:Arial;'>Git Status</h2><pre>{status}</pre>"

# 4. Run Git Commands from Web
@app.route("/run", methods=["GET", "POST"])
def run_git_command():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("gitcmd")
        output = subprocess.getoutput(cmd)
    return f"""
        <h2 style='font-family:Arial;'>Run Git Command</h2>
        <form method='POST'>
            <input name='gitcmd' placeholder='Enter git command' style='padding:8px;width:250px;'/>
            <button type='submit' style='padding:8px 15px;'>Run</button>
        </form>
        <pre>{output}</pre>
    """

if __name__ == "__main__":
    app.run(debug=True)
