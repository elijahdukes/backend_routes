import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98"
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"
    }
}

post_id_counter = 2

@app.route("/api/posts/")
def get_posts():
    """
    Gets all posts.
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Creates new post.
    """
    global post_id_counter
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if title is None:
        return json.dumps({"error": "Input title!"}), 400
    if link is None:
        return json.dumps({"error": "Input link!"}), 400
    if username is None:
        return json.dumps({"error": "Input username!"}), 400
    post = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username
    }
    posts[post_id_counter] = post
    comments[post_id_counter] = []
    post_id_counter += 1
    return json.dumps(post), 201

@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    """
    Gets specific post by post ID.
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post Not Found!"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Deletes specific post by post ID.
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post Not Found!"}), 404
    del posts[post_id]
    return json.dumps(post), 200

comments = {
    0:[{
        "id": 0,
        "upvotes": 8,
        "text": "Wow, my first Reddit Gold!",
        "username": "alicia98"
    }],
}

comment_id_counter = 1

@app.route("/api/posts/<int:post_id>/comments/")
def get_comments(post_id):
    """
    Gets all comments on a specific post.
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post Not Found!"}), 404
    comment = comments[post_id]
    res = {"comments": comment}
    return json.dumps(res), 200

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def post_comment(post_id):
    """
    Posts a new comment on a specific post.
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post Not Found!"}), 404
    global comment_id_counter
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")
    if text is None:
        return json.dumps({"error": "Input text!"}), 400
    if username is None:
        return json.dumps({"error": "Input username!"}), 400
    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username,
    }
    comments[post_id].append(comment)
    comment_id_counter += 1
    return json.dumps(comment), 201

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id,comment_id):
    """
    Edits existing comment on a specific post
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post Not Found!"}), 404
    if comment_id >= comment_id_counter:
        return json.dumps({"error": "Comment Not Found!"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Input text!"}), 400
    for i in comments[post_id]:
        if i["id"] == comment_id:
            i["text"] = text
            return json.dumps(i), 200
    return json.dumps({"error": "Comment Not Found on Post!"}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
