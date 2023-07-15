from flask import Blueprint, render_template, abort

projects_pb = Blueprint('projects_pb', __name__, url_prefix="/projects")

class ProjectsRestApi(Ba):
    
    @projects_pb.route('/', methods = ["GET"])
    def get():
        return "GET /projects"
    
    @projects_pb.route('/', methods = ["POST"])
    def post():
        return "POST /projects"