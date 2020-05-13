from flask import Flask, request, jsonify, json, render_template
import re, os
import database_helper

if 'NAMESPACE' in os.environ and os.environ['NAMESPACE'] == 'heroku':
    db_uri = os.environ['DATABASE_URL']
    debug_flag = False
else: # when running locally: use sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    debug_flag = True


app = Flask(__name__, static_url_path='')
#app = Flask(__name__)

app.debug = True

@app.route('/')
def home():
    return  app.send_static_file('index.html')


@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()




@app.route('/put_message', methods = ['POST'])
def post_message():
    data = request.get_json()
    message = data['message']
    courseTitle= data['course']

    if message == None:
        res = jsonify({'success' : False, 'message' : 'No message'})
        return res

    result = database_helper.put_message(message, courseTitle)
    if result != None:
        res = jsonify({'success' : True, 'message' : 'Message posted'})
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res


@app.route('/delete_message', methods = ['POST'])
def delete_message():
    data = request.get_json()
    noteId = data['id']

    if noteId == None:
        res = jsonify({'success' : False, 'message' : 'No message to delete'})
        return res

    result = database_helper.delete_message(noteId)
    if result:
        res = jsonify({'success' : True, 'message' : 'Message deleted'})
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res

###########################

@app.route('/search_course', methods = ['GET'])
def search_course_message():
    courseId = request.headers.get('courseTitle')

    if courseId == None:
        res = jsonify({'success' : False, 'message' : 'Nothing to find :('})
        return res

    result = database_helper.search_course(courseId)
    if result != None:
        print(result)
        res = jsonify({'success' : True,'course': result['course'] , 'messages' : result['messages'], 'dates': result['dates'], 'id':result['id']})
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res

############################################################
@app.route('/search_all', methods = ['GET'])
def search_all_messages():
    #data = request.get_json()
    course = request.headers.get('course')
    word = request.headers.get('word')
    fromDate = request.headers.get('from')
    toDate = request.headers.get('to')

    result = database_helper.search_all(course,word,fromDate,toDate)
    
    if result != None:
        print(result)
        res = jsonify({'success' : True, 'course':result['course'], 'dates':result['dates'], 'messages':result['messages'], 'id':result['id'] })
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res

############################################################
@app.route('/search_date', methods = ['GET'])
def search_date_message():
    #data = request.get_json()
    fromDate = request.headers.get('from')
    toDate = request.headers.get('to')

    if (fromDate == None or toDate == None):
        res = jsonify({'success' : False, 'message' : 'Nothing to find :('})
        return res

    result = database_helper.search_time(fromDate,toDate)
    if result != None:
        print(result)
        res = jsonify({'success' : True, 'course':result['course'], 'dates':result['dates'], 'messages':result['messages'], 'id':result['id'] })
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res

    #####################################################
@app.route('/search_word', methods = ['GET'])
def search_word_message():
    word = request.headers.get('word')
    print("word= ",word)

    if (word == None or word==""):
        res = jsonify({'success' : False, 'message' : 'Nothing to find :('})
        return res

    result = database_helper.search_word(word)
    if result != None:
        print(result)
        res = jsonify({'success' : True, 'course':result['course'], 'dates':result['dates'], 'messages':result['messages'], 'id':result['id'] })
        return res
    res = jsonify({'success' : False, 'message' : 'Something went wrong'})
    return res



    ################################################################

if __name__ == "__main__":
    app.run()
