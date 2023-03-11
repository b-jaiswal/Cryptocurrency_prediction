import streamlit as st
import pandas as pd
import pickle
import numpy as np


pickle_in = open("model.pkl","rb")
classifier=pickle.load(pickle_in)

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Cryptocurrency Price Prediction App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
#			hashed_pswd = make_hashes(password)

			result = login_user(username,password)
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Graphs","Analytics","Profiles"])
				if task == "Graphs":
					st.subheader("Add Your Post")
					st.title('Crypto Close v/s Date')

					DATE_COLUMN = 'Date'
					DATA_URL = pd.read_csv('btc.csv', index_col=0, parse_dates=True)

					data =DATA_URL 

					st.line_chart(data["Close"])
				elif task == "Analytics":
					st.subheader("Analytics")
					num1 = st.number_input('Insert a number')
					#num2 = st.number_input("Insert second number")
					#arr = np.array([[num1],[num2]])
					#print(arr)
					#prediction=classifier.predict(arr)
					#print(prediction)
					arr = np.array([[num1]])
					# print(arr)
					prediction=classifier.predict(arr)
					st.write(prediction[0])
    # return prediction
					#st.success('sucessful')
					
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,new_password)
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
