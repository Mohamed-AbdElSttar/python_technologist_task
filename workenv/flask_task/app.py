from flask import Flask, request, jsonify
from markupsafe import string
import csv

my_novles = []
with open("workenv/webscrap_task/novels.csv", "r") as my_file:
    my_file = csv.reader(my_file)
    for row in my_file:
        my_novles.append(row)
        
app = Flask(__name__)

@app.route("/novel", methods=["POST"])
def add_novel():
    title = request.json['title']
    novel_link = request.json['novel_link']
    auther = request.json['auther']
    auther_link = request.json['auther_link']
    country = request.json['country']
    country_link = request.json['country_link']
    
    row = [len(my_novles), title, novel_link, auther, auther_link, country, country_link]
    my_novles.append(row)
    
    with open("workenv/webscrap_task/novels.csv", "w") as my_file:
        my_file = csv.writer(my_file)
        for i in range(len(my_novles)):
            my_file.writerow(my_novles[i])
    
    return jsonify(row[1:])
    
@app.route("/novel", methods=["GET"])
def get_all_novels():
    return jsonify(my_novles[1:])

@app.route("/novel/<id>", methods=["GET"])
def get_novel(id):
    return jsonify(my_novles[int(id)])

@app.route("/novel/<id>", methods=["PUT"])
def update_novel(id):
    id = int(id)
    title = request.json['title']
    novel_link = request.json['novel_link']
    auther = request.json['auther']
    auther_link = request.json['auther_link']
    country = request.json['country']
    country_link = request.json['country_link']
    
    row = [id, title, novel_link, auther, auther_link, country, country_link]
    my_novles[id] = row
    
    with open("workenv/webscrap_task/novels.csv", "w") as my_file:
        my_file = csv.writer(my_file)
        for i in range(len(my_novles)):
            my_file.writerow(my_novles[i])
    
    return jsonify(row[1:])
    
@app.route("/novel/<id>", methods=["DELETE"])
def del_novel(id):
    id = int(id)
    row = my_novles[id]
    my_novles.pop(id)
    
    with open("workenv/webscrap_task/novels.csv", "w") as my_file:
        my_file = csv.writer(my_file)
        for i in range(len(my_novles)):
            my_file.writerow(my_novles[i])
            
    return jsonify(row)
    

if __name__ == "__main__":
    app.run(debug=True)