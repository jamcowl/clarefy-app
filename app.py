from flask import Flask, render_template, request
import clarefyUtils
app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

docInfo = ""
@app.route('/signUp', methods=['GET','POST'])
def signUp():
	if request.method == 'POST':
		print "\n================================================================\n > Button clicked to submit document!\n================================================================\n"
		global docInfo
		docInfo = request.form['inputName']
		print "\n================================================================\n > Got info: "+docInfo+"\n================================================================\n"
		return clarefyUtils.getFullPageHTML(docInfo)
	elif request.method == 'GET':
		global docInfo
		if docInfo != "":
			return clarefyUtils.getFullPageHTML(docInfo)

if __name__ == "__main__":
	app.debug = True
	app.run()


