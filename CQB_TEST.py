from asyncore import loop
from json import tool
from operator import or_, and_
from random import sample
from re import I
from flask import Flask, redirect, url_for,render_template, request, session, flash, request
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField , BooleanField   
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CQB_DB.db'
app.config["SQLALCHEMY_TRACK_MODDIFICATIONS"] = False


db = SQLAlchemy(app)



#　Create Model 
class data(db.Model):
    loop = db.Column("LOOP",db.String(10), nullable = False)
    rcp_id = db.Column("RCP_ID",db.Integer, primary_key = True)
    aodx_id = db.Column("AODX_ID",db.Integer)
    rcp_part = db.Column("PART",db.String(10), nullable = False)
    rcp_layer = db.Column("LAYER_NAME",db.String(20), nullable = False)
    rcp_name = db.Column("RECIPE_NAME",db.String(100), nullable = False)
    tool = db.Column("Tool",db.String(25), nullable = False)
    owner = db.Column("OWNER",db.String(100), nullable = False)
    sample_id = db.Column("SAMPLE_RULE_NUMBER",db.Integer)
    recipe_id = db.Column("RECIPE_NUMBER",db.Integer)
    date_add = db.Column(db.DateTime, default = datetime.utcnow)
    desc = db.Column("DESCRIPTION",db.String(100), nullable = False)



    def __init__(self, rcp_name, owner, aodx_id, tool, rcp_part, rcp_layer, sample_id, recipe_id, desc, loop):
        self.rcp_name = rcp_name
        self.owner = owner
        self.aodx_id = aodx_id
        self.tool = tool 
        self.rcp_part = rcp_part
        self.rcp_layer = rcp_layer 
        self.recipe_id = recipe_id 
        self.sample_id = sample_id 
        self.desc = desc
        self.loop = loop


               

@app.route('/', methods = ["POST","GET"])
def home():
    # if request.method =="POST":
    #     rcp_name = request.form["rcn"]
    #     owner = request.form["own"]
    #     data_temp= data("rcp_name","owner") 
    #     db.session.add(data_temp)      
    #     db.session.commit()
    return render_template("CQB_index.html")

@app.route('/view')
def view():
    rcp_lists = data.query.order_by(data.date_add)
    return render_template("CQB_view.html",rcp_lists=rcp_lists)

## Create a Form
class UserForm(FlaskForm):
    loop = StringField("Loop", validators=[DataRequired()])
    rcp_part = StringField("Part", validators=[DataRequired()])
    rcp_layer = StringField("Layer Name", validators=[DataRequired()])
    rcp_name = StringField("Recipe Name", validators=[DataRequired()])
    tool =  StringField("Tool", validators=[DataRequired()])
    owner =  StringField("Owner", validators=[DataRequired()])
    desc =  StringField("Description", validators=[DataRequired()])
    submit = SubmitField("submit")
    # check_aodx = BooleanField("AODX ID")
    # check_sample = BooleanField("Sample ID")
    # check_recipe = BooleanField("Recipe ID")

class SearchForm(FlaskForm):
    rcp_name = StringField("Recipe Name", validators=[DataRequired()])
    tool = StringField("Tool", validators=[DataRequired()])
    submit = SubmitField("submit")
    

#Update Database  Record
@app.route('/update/<int:rcp_id>',methods = ["GET","POST"])
def update(rcp_id):
    form = UserForm()
    rcp_to_update = data.query.get_or_404(rcp_id)
    if request.method =="POST":
        #print(int(form.check_aodx.data)) check tpye
        rcp_to_update.rcp_name = request.form["rcp_name"]
        rcp_to_update.owner = request.form["owner"]
        rcp_to_update.desc = request.form["desc"]
        print()
        try:
            db.session.commit()
            flash("Recipe Update Successfully!")
            return render_template("CQB_update.html",form=form, rcp_to_update=rcp_to_update)
            
        except Exception:
            flash("Error~Please check again")
            return render_template("CQB_update.html",form=form, rcp_to_update=rcp_to_update)
        
    else:
        return render_template("CQB_update.html",form=form, rcp_to_update=rcp_to_update)

@app.route('/delete/<int:rcp_id>', methods= ['GET','POST'])
def delete(rcp_id):
    rcp_to_delete = data.query.get_or_404(rcp_id)
    rcp_name = None 
    form = UserForm()
    try:
        db.session.delete(rcp_to_delete)
        db.session.commit()
        flash("Recipe Delete Successfully!!!")
        rcp_lists = data.query.order_by(data.date_add)
        return render_template("CQB_name.html",rcp_name=rcp_name,form=form,rcp_lists=rcp_lists)
    except Exception:
        flash("Some error occurred!!!")
        return render_template("CQB_name.html",rcp_name=rcp_name,form=form,rcp_lists=rcp_lists)


# @app.route('/cal_num/<int:rcp_id>', methods=["GET","POST"])
# def cal_num(rcp_id):
#     form = UserForm()
#     rcp_lists = db.session.query(data.aodx_id).filter(rcp_id == rcp_id ).first()
#     rcp_name = None
#     if form.validate_on_submit():
#         a = rcp_lists
#         # b = form.check_sample.data
#         # c = form.check_recipe.data  
#         # sum = int(a)+int(b)+int(c)
#         print(a)
#         return render_template("CQB_index.html")
#     else :
#         a = rcp_lists
#         print (a)
#         return render_template("CQB_index.html")
#         # if sum == 3:
#         #     A=rcp_lists["aodx_id"]
#         #     print(A) 
#         #     return render_template("CQB_name.html",rcp_name=rcp_name,form=form,rcp_lists=rcp_lists)
#             # num_aodx = db.session.query(data.aodx_id).filter(data.rcp_name==form.rcp_name.data).scalar()
#             # num_sample = db.session.query(data.sample_id).filter(data.rcp_name==form.rcp_name.data).scalar()
#             # num_recipe = db.session.query(data.recipe_id).filter(data.rcp_name==form.rcp_name.data).scalar()
#             # if num_aodx is None:
#             #     num_aodx=0
#             # else:
#             #     num_aodx=int(num_aodx)
#             # num_sample = db.session.query(func.max(data.sample_id)).filter(data.tool==form.tool.data,data.loop==form.loop.data).scalar()
#             # if num_sample is None:
#             #     num_sample=0
#             # else:
#             #     num_sample=int(num_sample)
#             # num_recipe = db.session.query(func.max(data.recipe_id)).filter(data.tool==form.tool.data,data.loop==form.loop.data).scalar()
#             # if num_recipe is None:
#             #     num_recipe=0
#             # else:
#             #     num_recipe=int(num_recipe)     
#     #         return 1

##html CQB
    #    <p>Choose AODX/SAMPLE/RECIPE you changed</p>
    #     <div class="form-check">
    #       {{ form.check_aodx(class="form-check-input")}}
    #       {{ form.check_aodx.label(class="form-check-label") }}
    #     </div>
    #       <div class="form-check">  
    #       {{ form.check_sample(class="form-check-input")}}
    #       {{ form.check_sample.label(class="form-check-label") }}
    #     </div>
    #       <div class="form-check">
    #       {{ form.check_recipe(class="form-check-input")}}
    #       {{ form.check_recipe.label(class="form-check-label") }}
    #       <a href="{{url_for('cal_num', rcp_id=rcp_to_update.rcp_id)}}" class="btn btn-success">Give New ID</a>
    #     </div>

@app.route('/search', methods=["GET","POST"])
def search():
    form = SearchForm()
    rcp_lists = None
    if form.validate_on_submit():
        rcp_lists = data.query.filter(and_(data.rcp_name==form.rcp_name.data, data.tool==form.tool.data)).all()
        
        
        if len(rcp_lists)== 0 :
            rcp_sim = data.query.filter(data.rcp_name.like('%'+form.rcp_name.data+'%')).all()
            if len(rcp_sim) !=0 :
                rcp_lists = rcp_sim
                flash("No valid recipe, But maybe you are searching for...")
                return render_template("search.html",rcp_lists=rcp_lists,form=form)
            else:
                flash("No valid recipe")
                return render_template("search.html",rcp_lists=rcp_lists,form=form)
        else:
            flash("Here you are!")
            return render_template("search.html",rcp_lists=rcp_lists,form=form)
    
    return render_template("search.html", rcp_lists=rcp_lists,form=form)



@app.route('/rcp_name', methods= ['GET','POST'])
def rcp_name():
    rcp_name = None
    owner = None
    form = UserForm()
    if form.validate_on_submit():
        data_check = data.query.filter_by(rcp_name = form.rcp_name.data).first()
        if data_check is None :
            #num = len(data.query.filter_by(tool=form.tool.data).all())
            num_aodx = db.session.query(func.max(data.aodx_id)).filter(data.tool==form.tool.data,data.loop==form.loop.data).scalar()
            if num_aodx is None:
                num_aodx=0
            else:
                num_aodx=int(num_aodx)
            num_sample = db.session.query(func.max(data.sample_id)).filter(data.tool==form.tool.data,data.loop==form.loop.data).scalar()
            if num_sample is None:
                num_sample=0
            else:
                num_sample=int(num_sample)
            num_recipe = db.session.query(func.max(data.recipe_id)).filter(data.tool==form.tool.data,data.loop==form.loop.data).scalar()
            if num_recipe is None:
                num_recipe=0
            else:
                num_recipe=int(num_recipe)                                                             
            data_check = data(rcp_name= form.rcp_name.data, owner = form.owner.data, tool = form.tool.data,\
                aodx_id =num_aodx, sample_id=num_aodx, recipe_id=num_aodx, rcp_part = form.rcp_part.data, rcp_layer = form.rcp_layer.data,loop=form.loop.data, desc = form.desc.data)
            data_check.aodx_id += 1
            data_check.sample_id += 1
            data_check.recipe_id += 1
            db.session.add(data_check)
            db.session.commit()
            flash("Recipe Save!")
            
        else :
            rcp_name = data.query.filter_by(rcp_name = form.rcp_name.data).first()
            flash("Recipe Exist!")
        
    rcp_lists = data.query.order_by(data.date_add)
    return render_template("CQB_name.html", rcp_name=rcp_name,form=form, rcp_lists=rcp_lists)




if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0',port=3001,debug=True)
   