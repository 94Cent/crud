import re,random,os
from flask import render_template,request,flash,redirect,make_response,session,url_for
from sqlalchemy.sql import text
from vapp import app,csrf
from vapp.forms import ContactForm,PostForm, SignupForm
from vapp.models import db,Post,Category,User

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register",methods=["POST","GET"])
def register():
    signupform=SignupForm()
    if request.method=="GET":
        return render_template("register.html",signupform=signupform)
    else:
        if signupform.validate_on_submit():
            #retrieve form data and save in database
            
            u=User(user_fullname=request.form.get('fullname'),
                   user_email=request.form.get('email'),
                   user_pwd=request.form.get("password"))
            db.session.add(u)
            db.session.commit()
            #log the user in and redirect to dashboard
            session['userid']=u.user_id
            session["user_loggedin"]=True
            flash("Account created successfully",)
            return redirect("/dashboard")
        else:
            return render_template("register.html",signupform=signupform)
        


@app.route("/login",methods=["POST","GET"])
@csrf.exempt
def f_login():
    if request.method=="GET":

         return render_template("login.html")
    else:
        username=request.form['username']
        password=request.form['password']
        if password=="1234":
           flash("Login Successful", category="success")
           session["loggedin"]= username
           return redirect("/profile")
        else:
            flash("login incorrect" ,category="error")
            return redirect("/login")
        
@app.route("/logout")
def f_logout():
    if session.get("loggedin") != None:
        session.pop("loggedin",None)
    flash("you are logged out")
    return redirect("/login")

  

@app.route("/profile")
def f_profile():
    if session.get("loggedin") != None:
        
         return render_template("profile.html")
    
    else:
        flash("you must be logged in in order to view this page")
        return redirect("/login")

@app.route("/dashboard")
def f_dashboard():
    
    return  render_template("dashboard.html")
@app.route("/news",methods=['GET','POST'])
def newsletter():
    if request.method=='GET':
         return render_template("news.html")
    else:
        email=request.form.get("email")
        check=re.match("^[a-z|A-Z]([a-z|A-Z|0-9]+)@[a-z|A-Z]+(.)[a-z|A-Z]+",email)

        if check:

            db.session.execute(text(f"INSERT INTO newsletter SET email='{email}'"))

            db.session.commit()
            flash("Thank you for your subscription")
        else:
            flash("invalid email format")
        return redirect("/profile")
    

        

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=="GET":
        return  render_template("fileupload.html")
    else:
        #retrive the file from the form
        fileobj=request.files['pix']
        original_name=fileobj.filename

        #to get the file extension
        file,ext=os.path.splitext(original_name)
        
        #To upload
        newname=int(random.random()*1000000)
        destination=str(newname)+ext
        allow=[".png",".jpg",".jpeg"]
        if ext.lower() not in allow:
            return f"invalid Format {ext}" 
        else:
            fileobj.save("fapp/static/profile/"+destination)
            return f"file has been submitted here  {original_name}"
        


@app.route('/comments')
def allcomments():
    #query the database
    #data=db.session.query(Post).all() #or use
    #data=Post.query.all()
    data=db.session.query(Post,Category).join(Category).all()
    # data=db.session.query(Post,Category).join(Category).filter((Post.post_cat_id=="1")).all()
    data=db.session.query(Post,Category).join(Category).order_by((Category.cat_name)).all()
    # data=Post.query.join(Category).add_columns(Category).all()
    # data=db.session.query(Post.post_content,Post.post_title,Category.cat_id).join(Category).all()
    return render_template("allcomment.html",data=data)

@app.route('/delete/post/<postid>')
def delete_post(postid):
    #delete post from orm
    d=Post.query.get(postid)
    db.session.delete(d)
    db.session.commit()
    return redirect("/comments") 

@app.route('/edit/post/<postid>',methods=['POST',"GET"])
def edit_post(postid):
    if request.method=="GET":
        #fetch the post with id postid
        e=Post.query.get(postid)
        cats=db.session.query(Category).all()#a list of all categories
        return render_template("edit_post.html",e=e,c=cats)
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        author=request.form.get('author')
        pp=db.session.query(Post).get(postid)
        pp.post_title=title
        pp.post_content=content
        pp.post_author=author
        db.session.commit()
        flash("Post updated successfully")
        return redirect("/comments")
    

@app.route('/post',methods=['GET','POST'])
def postcomment():
    pform=PostForm()
    if request.method=="GET":
        cats=db.session.query(Category).all()#a list of all categories
        return render_template("comment.html",pform=pform,c=cats)
    else:
         if pform.validate_on_submit():
            title=request.form.get('title')
            content=request.form.get('content')
            category=request.form.get('category')
            author=request.form.get('author')
            #insert into database without writing query
            p=Post(post_title=title,post_content=content,post_cat_id=category,post_author=author)
            db.session.add(p)
            db.session.commit()
            flash("Comment Sent")
            return redirect('/comments') #by get request
         else:
             return render_template("comment.html",pform=pform)

        