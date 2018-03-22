import time
import psycopg2
import psycopg2.extras
import conf
from datetime import datetime

import pdb

from flask import Flask, jsonify, request, Blueprint, url_for, redirect
from flask.json import JSONEncoder
from flask.views import View

bp = Blueprint("api", __name__, "api/")
db = psycopg2.connect(conf.db_path)
cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

class CustomJsonEncoder(JSONEncoder):
    """
        This class extends the builtin JSONEncoder class from flask to convert
        python date time objects into unix timestamps for purposes of
        interoperability with javascript
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.timestamp()
        return JSONEncoder.default(self,obj)


class ListView(View):
    '''
        This class provides a generic list view over an sql table providing a
        few predefined fields that records can be used to filter the table for
        the appropriate records
    '''

    methods = ["GET"]
    def records(self, n, p, before, after, search):
        
        raise NotImplementedError()

    def dispatch_request(self, **kwargs):
        n = int(request.args.get("n")) if "n" in request.args else 100
        p = int(request.args.get("p")) if "p" in request.args else 1
        before = request.args.get("before") if "before" in request.args else 0
        after = request.args.get("after") if "after" in request.args else int(time.time())
        search = request.args.get("field") if "field" in request.args else ""
        data = self.records(n, p, before, after, search, **kwargs)
        count = len(data)
        if count == n:
            return jsonify(
                    {
                        "count": len(data),
                        "data": list(data),
                        "next_page": url_for(request.endpoint, n=n, p=p+1, before=before, after=after, field=search, _external=True, **kwargs)
                    })
        else:
            return jsonify(
                    {
                        "count": len(data),
                        "data": list(data),
                    })

class SchoolList(ListView):
    '''
        This class extends the list view and provides a view into the schools table
    '''

    def records(self, n, p, before, after, search, *args):
        print(search)
        cursor.execute(
                "SELECT * FROM schools WHERE lower(establishment_name) like %s limit %s offset %s",
                ["%" + search.lower() + "%",
                n,
                (p-1) * n])
        return [
                {
                    "school_url": url_for(".school_detail", school_id=record["establishment_name"] , _external=True),
                    **record
                }
                for record in cursor.fetchall()]

class PostList(ListView):
    '''
        This class extends the list view and provides a view into the posts of a particular school
    '''

    def records(self, n, p, before, after, search, **kwargs):
        cursor.execute(
                "SELECT post.* FROM post INNER JOIN schools "
                "ON post.school_id = schools.establishment_name "
                "WHERE "
                    "schools.establishment_name = %s and  "
                    "lower(raw_text) like lower(%s) and  "
                    "post.timestamp > to_timestamp(%s) and  "
                    "post.timestamp < to_timestamp(%s) "
                "limit %s offset %s",
                [
                    kwargs["school_id"],
                    search + "%",
                    before,
                    after,
                    n,
                    (p-1) * n])
        return cursor.fetchall()

class TopicList(ListView):
    '''
        This class extends the list view and provides a view into the topics of
        a particular school
    '''
    def records(self, n, p, before, after, search, **kwargs):
        cursor.execute(
                "SELECT topic.* FROM topic INNER JOIN post "
                    "ON post.topic_id = topic.id "
                "INNER JOIN schools "
                    "ON post.school_id = schools.establishment_name "
                "WHERE "
                    "schools.establishment_name = %s and  "
                    "lower(raw_text) like lower(%s) and  "
                    "post.timestamp > to_timestamp(%s) and  "
                    "post.timestamp < to_timestamp(%s) "
                "limit %s offset %s",
                [
                    kwargs["school_id"],
                    search + "%",
                    before,
                    after,
                    n,
                    (p-1) * n])
        return [
                {
                    "topic_url": url_for(".topic_detail", school_id=kwargs["school_id"], topic_id=record["id"], _external=True),
                    **record
                }
                for record in cursor.fetchall()]

class DetailView(View):
    '''
    A generic view class that abstracts over the concept of a single-item view
    '''

    methods = ["GET"]

    def record(self, **kwargs):
        raise NotImplementedError()

    def dispatch_request(self, **kwargs):
        return jsonify(self.record(**kwargs))

class SchoolView(DetailView):
    '''
    A detail view that looks renders a school into json and returns a link to a
    list of that school's topics and posts
    '''

    def record(self, **kwargs):
        id = kwargs["school_id"]
        cursor.execute("SELECT * FROM schools WHERE establishment_name=%s", [id])
        record = cursor.fetchone()
        return {
                "posts": url_for(".posts", school_id=id, _external=True),
                "topics": url_for(".topics", school_id=id, _external=True),
                **record
                }

class TopicView(DetailView):
    '''
    A detail view that looks renders a topic into json and returns a link to a
    list of that topic's posts
    '''

    def record(self, **kwargs):
        id = kwargs["topic_id"]
        cursor.execute("SELECT * FROM topic WHERE id=%s", [id])
        record = cursor.fetchone()
        return {
                "posts": url_for(".posts_by_topic", school_id=kwargs["school_id"], topic_id=id, _external=True),
                **record
                }

class TopicPostList(ListView):
    '''
        This class extends the list view and provides a view into the posts of
        a particular topic
    '''
    def records(self, n, p, before, after, search, **kwargs):
        cursor.execute(
                "SELECT post.* FROM post INNER JOIN schools "
                "ON post.school_id = schools.establishment_name "
                "INNER JOIN topic "
                "ON topic.id = post.topic_id "
                "WHERE "
                    "topic.id = %s and "
                    "schools.establishment_name = %s and  "
                    "lower(raw_text) like lower(%s) and  "
                    "post.timestamp > to_timestamp(%s) and  "
                    "post.timestamp < to_timestamp(%s) "
                "limit %s offset %s",
                [   
                    kwargs["topic_id"],
                    kwargs["school_id"],
                    search + "%",
                    before,
                    after,
                    n,
                    (p-1) * n])
        return cursor.fetchall()



@bp.route('/')
def index():
    '''
    The index redirects to the school search endpoint
    '''
    return redirect(url_for(".schools", _external=True))

bp.add_url_rule("/schools/", view_func=SchoolList.as_view("schools"))
bp.add_url_rule("/schools/<school_id>", view_func=SchoolView.as_view("school_detail"))
bp.add_url_rule("/schools/<school_id>/posts/", view_func=PostList.as_view("posts"))
bp.add_url_rule("/schools/<school_id>/topics/", view_func=TopicList.as_view("topics"))
bp.add_url_rule("/schools/<school_id>/topics/<topic_id>", view_func=TopicView.as_view("topic_detail"))
bp.add_url_rule("/schools/<school_id>/topics/<topic_id>/posts/", view_func=TopicPostList.as_view("posts_by_topic"))

@bp.after_request
def after_request(response):
    '''
    A custom request handler that appends the universal cross domain headers
    onto the response
    '''
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.json_encoder = CustomJsonEncoder
    app.run()
