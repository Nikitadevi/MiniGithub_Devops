from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# ------------------- Home Page -------------------
@app.route("/")
def home():
    return render_template("index.html")   # must be inside /templates folder

# ------------------- Show Git Commits -------------------
@app.route("/commits")
def commits():
    logs = subprocess.getoutput("git log --oneline")
    return f"<h2>Commit History</h2><pre>{logs}</pre>"

# ------------------- Show Branches -------------------
@app.route("/branches")
def branches():
    branches = subprocess.getoutput("git branch")
    return f"<h2>Branches</h2><pre>{branches}</pre>"

# ------------------- Git Status -------------------
@app.route("/status")
def status():
    status = subprocess.getoutput("git status")
    return f"<h2>Git Status</h2><pre>{status}</pre>"

# ------------------- Run Custom Git Command -------------------
@app.route("/run", methods=["GET", "POST"])
def run_git():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("gitcmd")
        output = subprocess.getoutput(cmd)
    return f"""
        <h2>Run Git Command</h2>
        <form method='POST'>
            <input name='gitcmd' placeholder='Enter git command'/>
            <button type='submit'>Run</button>
        </form>
        <pre>{output}</pre>
    """

if __name__ == "__main__":
    app.run(debug=True)
