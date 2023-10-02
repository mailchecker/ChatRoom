import streamlit as st, sqlite3, datetime #, os ; os.remove('forum.db')
con=sqlite3.connect('forum.db')
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS db(topic TEXT, messages TEXT)')

# st.set_page_config(layout="wide", page_title="Forum")

for row in cur.execute('SELECT rowid, topic, messages FROM db'):
  st.subheader(row[1])
  with st.expander(''):
    col1, col2=st.columns([3,2])
    with col1:
      st.text_area('topic', row[2], height=350, label_visibility='collapsed')
    with col2:
      with st.form(f'ID{row[0]}', clear_on_submit=True):
        name=st.text_input('Name')
        timestamp=datetime.datetime.now()
        message=st.text_area('Message')
        if st.form_submit_button('Submit'):
          messages=f'{name} - {timestamp}:\n\n{message}\n\n{row[2]}\n\n'
          cur.execute(
            'UPDATE db SET topic=?, messages=? WHERE rowid=?;', 
            (row[1], messages, str(row[0]))
          )
          con.commit() ; st.experimental_rerun()

st.header('Add New Topic')
with st.form('New Topic', clear_on_submit=True):
  topic=st.text_input('New Topic')
  name=st.text_input('Name')
  messages=st.text_area('Initial Mesage')
  timestamp=datetime.datetime.now()
  if st.form_submit_button('Add New Topic'):
    cur.execute('INSERT INTO db(topic, messages) VALUES(?,?)', (
      topic, f'{name} - {timestamp}:\n\n{messages}\n\n'
    ))
    con.commit() ; st.experimental_rerun()
