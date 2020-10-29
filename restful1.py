from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  #we are using sqlite db in db.sqlite3 file

api = Api(app)   #for restful
db = SQLAlchemy(app)  #for sqlalchemy -- to access any sql db easily (ie. without sql)
ma = Marshmallow(app)  #for marshmallow

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)  
#after this, create db in python shell 
#from restful1 import db (ie. restful1 is this file name)
#db.create_all()  #then db.sqlite3 is created 

class PostsResource(Resource):
    def get(self):
        #return 'jijo'
        return jsonify({'jijo':'hihi'})
        #return Post.query.all()
        #return posts_schema.dump(Post.query.all())  #posts_schema.dump  to JSON-serialize the data, ie when many=True
   
    def post(self):
        data = request.json
        #print(data)
        #return data
        
        post = Post(title=data['title'], content=data['content'])
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post) #posts_schema.dump  to JSON-serialize the data

#get,patch and delete using primary key
class PostResource(Resource): 
    def get(self, pk):
        return post_schema.dump(Post.query.get_or_404(pk))
         

    def patch(self, pk):     #PUT needs all data(columns) and updates all, PATCH needs only few data, and updates those few 
        data = request.json
        post = Post.query.get_or_404(pk)

        if 'title' in data:
            post.title = data['title']
        
        if 'content' in data:
            post.content = data['content']
        
        db.session.commit()
        return post_schema.dump(post)

    def delete(self, pk):
        post = Post.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()
        return '', 204   #ie to return nothing and no error 204

api.add_resource(PostResource, '/posts/<int:pk>')
api.add_resource(PostsResource, '/posts')


if __name__ == "__main__": 
    #app.run(debug=True)     #with this we can just like any python code
    app.run(debug=False)     #debug True is to save this and refresh page, no need to run
 