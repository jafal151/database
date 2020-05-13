import sqlite3
from flask import g
import string
import random
from datetime import datetime, date

conn = sqlite3.connect('database.db')
c = conn.cursor()

DATABASE = "database.db"

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_to_database()
	return db

def connect_to_database():
	return sqlite3.connect('database.db')

def disconnect_db():
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def put_message(message,courseTitle):
	try:
		today = date.today()
		today = today.strftime("%Y/%m/%d")
		###### --- SET a specific date for testing --- ######
		#today = datetime.strptime("2020/6/3", '%Y/%m/%d').date()

		today = datetime.strptime(str(today), '%Y/%m/%d').date()
		get_db().execute("INSERT INTO messages (content, noteDate, course) VALUES(?,?,?)", [message,today,courseTitle])
		get_db().commit()
		cursor = get_db().execute("SELECT id FROM messages WHERE content=?", [message])
		messageId = cursor.fetchall()
		cursor.close()
		return  messageId
	except Exception as e:
		print(e)
		return None

def delete_message(noteId):
	try:
		get_db().execute("DELETE FROM messages WHERE id=?", [noteId])
		get_db().commit()
		return True
	except Exception as e:
		print(e)
		return False

def search_course(courseId):
	try:
		cursor = get_db().execute("SELECT content FROM messages WHERE course=?", [courseId])
		messages = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT noteDate FROM messages WHERE course=?", [courseId])
		dates= cursor.fetchall();
		cursor.close()
		cursor = get_db().execute("SELECT id FROM messages WHERE course=?", [courseId])
		noteId= cursor.fetchall()
		cursor.close()

		return {'course' : courseId, 'messages': messages, 'dates': dates, 'id': noteId}
	except Exception as e:
		print(e)
		return None

def search_time(fromDate, toDate ):

	try:
		date1 = datetime.strptime(fromDate, '%Y-%m-%d').date() 
		date2 = datetime.strptime(toDate, '%Y-%m-%d').date()   
		cursor = get_db().execute("SELECT noteDate FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ?",[date1,date2])
		dates = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT content FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ?",[date1,date2])
		messages = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT course FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ?",[date1,date2])
		course = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT id FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ?",[date1,date2])
		noteId = cursor.fetchall()
		cursor.close()


		#print("Dates: ","\n",noteDates, '\n') #for testing
		return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}
	except Exception as e:
		print(e)
		return None

def search_word(word):

	try:
		searchWord= '%'+word+'%'
		cursor = get_db().execute("SELECT noteDate FROM messages WHERE content LIKE ? ",[searchWord])
		dates = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT content FROM messages WHERE content LIKE ? ",[searchWord])
		messages = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT course FROM messages WHERE content LIKE ? ",[searchWord])
		course = cursor.fetchall()
		cursor.close()
		cursor = get_db().execute("SELECT id FROM messages WHERE content LIKE ? ",[searchWord])
		noteId = cursor.fetchall()
		cursor.close()


		print("Dates: ","\n",dates, noteId,'\n') #for testing
		return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}
	except Exception as e:
		print(e)
		return None

def search_all(courseId,word,fromDate,toDate):
	try:
		searchWord= '%'+word+'%'

		if fromDate == "" or toDate=="":
			if courseId=="":
				if word== "":
					return None
				else:
					cursor = get_db().execute("SELECT content FROM messages WHERE content LIKE ?",[searchWord])
					messages = cursor.fetchall()
					cursor.close()
					cursor = get_db().execute("SELECT noteDate FROM messages WHERE content LIKE ?",[searchWord])
					dates = cursor.fetchall()
					cursor.close()
					cursor = get_db().execute("SELECT course FROM messages WHERE content LIKE ?",[searchWord])
					course = cursor.fetchall()
					cursor.close()
					cursor = get_db().execute("SELECT id FROM messages WHERE content LIKE ?",[searchWord])
					noteId = cursor.fetchall()
					cursor.close()	
					print(messages)
					return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}
			else:
				cursor = get_db().execute("SELECT content FROM messages WHERE course = ? AND  content LIKE ?",[courseId,searchWord])
				messages = cursor.fetchall()
				cursor.close()
				cursor = get_db().execute("SELECT noteDate FROM messages WHERE course = ? AND  content LIKE ?",[courseId,searchWord])
				dates = cursor.fetchall()
				cursor.close()
				cursor = get_db().execute("SELECT course FROM messages WHERE course = ? AND  content LIKE ?",[courseId,searchWord])
				course = cursor.fetchall()
				cursor.close()
				cursor = get_db().execute("SELECT id FROM messages WHERE course = ? AND  content LIKE ?",[courseId,searchWord])
				noteId = cursor.fetchall()
				cursor.close()	
				print(messages)
				return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}

		elif courseId == "":
			date1 = datetime.strptime(fromDate, '%Y-%m-%d').date() 
			date2 = datetime.strptime(toDate, '%Y-%m-%d').date() 
			cursor = get_db().execute("SELECT content FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ?  AND  content LIKE ?",[date1,date2,searchWord])
			messages = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT noteDate FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND content LIKE ?",[date1,date2,searchWord])
			dates = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT course FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND  content LIKE ?",[date1,date2,searchWord])
			course = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT id FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND content LIKE ?",[date1,date2,searchWord])
			noteId = cursor.fetchall()
			cursor.close()	
			print(messages)
			return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}
				

		else:
			date1 = datetime.strptime(fromDate, '%Y-%m-%d').date() 
			date2 = datetime.strptime(toDate, '%Y-%m-%d').date() 
			cursor = get_db().execute("SELECT content FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND  course = ? AND  content LIKE ?",[date1,date2,courseId,searchWord])
			messages = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT noteDate FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND  course = ? AND  content LIKE ?",[date1,date2,courseId,searchWord])
			dates = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT course FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND  course = ? AND  content LIKE ?",[date1,date2,courseId,searchWord])
			course = cursor.fetchall()
			cursor.close()
			cursor = get_db().execute("SELECT id FROM messages WHERE strftime('%Y-%m-%d', noteDate) BETWEEN ? AND ? AND  course = ? AND  content LIKE ?",[date1,date2,courseId,searchWord])
			noteId = cursor.fetchall()
			cursor.close()	
			print(messages)
			return {'course' : course, 'dates' : dates, 'messages' : messages, 'id': noteId}
	except Exception as e:
		print(e)
		return None
	