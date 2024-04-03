from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
uri = "mongodb+srv://ku_clap_src:DN0Gms7bOkAVTHqj@cluster0.hqpxerp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["ku_clap_src"] 
collection = db["info_course"]
login = db["login"]
"เป็นการเชื่อม mongodb ที่เข้าใจง่าย ในอนาคตควรเพิ่ม update and delete "
CORS(app)

@app.route("/")
def greet():
    return "<p>Welcome to Comment Management API</p>"

@app.route("/comments", methods=["GET"])
def get_all_comments():
    comments = list(collection.find({}, {"_id": 0, "user": 1, "course": 1, "comment": 1, "like": 1}))  
    comments_list = []
    
    for comment in comments:
        comments_data = {
            "user" : comment["user"],
            "course" : comment["course"],
            "comment" : comment["comment"],
            "like": comment["like"]
        }
        comments_list.append(comments_data)
    return jsonify({"comments": comments_list})

@app.route("/comments/<string:course_id>", methods=["GET"])
def get_comments_by_course(course_id):
    comments = list(collection.find({"course": course_id}, {"_id": 0}))  
    comments_list = []
    
    for comment in comments:
        comments_data = {
            "user" : comment["user"],
            "course" : comment["course"],
            "comment" : comment["comment"],
            "like": comment["like"]
        }
        comments_list.append(comments_data)
    return jsonify({"comments": comments_list})

@app.route("/comments", methods={"POST"})
def create_comment():
    data = request.get_json()
    last_comment = collection.find_one(sort=[("_id", -1)])
    last_id = last_comment["_id"] if last_comment else 0
    new_id = last_id + 1
    comment = {
        "_id": new_id,
        "user" : data.get("user"),
        "course" : data.get("course"),
        "comment" : data.get("comment"),
        "like" : data.get("like")
    }
    "โค้ดดูเข้าใจง่ายดี เขียนอธิบายสถานะของcomment ไว้ด้วย"
    try:
        collection.insert_one(comment)
        return jsonify({"message": "Comment added successfully"}), 200
    except DuplicateKeyError:
        return jsonify({"error": "Comment already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
