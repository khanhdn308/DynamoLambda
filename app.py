from flask import Flask
from flask import render_template, request, redirect
import boto3
import json
from flask_caching import Cache


app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/')
# @cache.cached(timeout=50)
def index():
    client = boto3.client('lambda')
    respond = client.invoke(
        FunctionName='movieTest',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "action": "read"
        }).encode('utf-8')
    )
    result = json.loads(respond['Payload'].read())
    return render_template('index.html', resource=result)


@app.route('/movie/<movieDetail>')
def getMovieByKeys(movieDetail):
    client = boto3.client('lambda')
    details = movieDetail.split("+")
    response = client.invoke(
        FunctionName='movieTest',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "action": "read",
            "key": {
                "year": int(float(details[1])),
                "title": details[0]
            }
        })
    )
    result = json.loads(response['Payload'].read())
    print(result)
    return render_template('movieDetail.html', resource=result)

@app.route("/addMovie", methods=['GET', 'POST'])
def addMovie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        print(title, year)

        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName='movieTest',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "create",
                "item": {
                    "year": int(year),
                    "title": title
                }
            })
        )
        result = json.loads(response['Payload'].read())
        print(result)
        return redirect('/')
    return render_template('addMovie.html')

@app.route("/deleteMovie/<movieDetail>")
def deleteMovie(movieDetail):
    client = boto3.client('lambda')
    details = movieDetail.split("+")

    response = client.invoke(
        FunctionName='movieTest',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "action": "delete",
            "key": {
                "year": int(float(details[1])),
                "title": details[0]
            }
        })
    )

    result = json.loads(response['Payload'].read())
    print(result)
    return redirect('/')

@app.route("/editMovie",  methods=['GET', 'POST'])
def editMovie():
    if request.method == 'POST':
        print(request.form)
        client = boto3.client('lambda')
        title = request.form['title']
        year = int(float(request.form['year']))

        response = client.invoke(
            FunctionName='movieTest',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action":"update",
                "key":{
                    "year": year,
                    "title": title
                },
                'updateExpression' : "set info.rating = :r, info.plot=:p",
                'expressionAttributeValues' : {
                    ':r': request.form["rating"],
                    ':p': request.form["plot"],
                }            
            })
        )
        result = json.loads(response['Payload'].read())
        print(result)
        return redirect('/movie/' + title + '+' + str(year))
    
    #redirect to edit form
    if request.method == 'GET':

        print(request.args, 'ooooooo')
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName='movieTest',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "read",
                "key": {
                    "year": int(float(request.args['year'])),
                    "title": request.args['title']
                }
            })
        )
    result = json.loads(response['Payload'].read())
    return render_template('editMovie.html', resource=result)