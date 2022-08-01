from flask import Flask, render_template, request
from bounding_box import BoundingBox
from pointcloud import PointCloud
from tracker import Tracker
from pcd2bin import pcd2bin_GUI, bin_directory_GUI

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def root():
	return render_template("index.html")

@app.route("/initTracker", methods=["POST"])
def init_tracker():
	json_request = request.get_json()
	pointcloud = PointCloud.parse_json(json_request["pointcloud"])
	tracker = Tracker(pointcloud)
	print(str(tracker))
	return "success"

@app.route("/trackBoundingBoxes", methods=['POST'])
def trackBoundingBox():
	json_request = request.get_json()
	pointcloud = PointCloud.parse_json(json_request["pointcloud"], json_request["intensities"])
	filtered_indices = tracker.filter_pointcloud(pointcloud)
	next_bounding_boxes = tracker.predict_bounding_boxes(pointcloud)
	print(next_bounding_boxes)
	return str([filtered_indices, next_bounding_boxes])

@app.route("/updateBoundingBoxes", methods=['POST'])
def updateBoundingBoxes():
	print(request.get_json())
	json_request = request.get_json()
	bounding_boxes = BoundingBox.parse_json(json_request["bounding_boxes"])
	tracker.set_bounding_boxes(bounding_boxes)
	return str(bounding_boxes)

@app.route("/predictLabel", methods=['POST'])
def predictLabel():
	return str('Car')

if __name__ == "__main__":
	while True:
		user_input =  input ('Do you want to convert your .pcd files to .bin files? [Y/N] \n')
		if user_input in ['Y', 'y', 'N', 'n'] :
			break
		print('Please enter an appropriate answer.')
	if user_input in ['Y', 'y']:
		pcd2bin_GUI()
	tracker = Tracker()
	app.run()
