import streamlit as st, sqlite3, datetime#, os ; os.remove('chats.db')
con=sqlite3.connect('chats.db')
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS db(messages TEXT)')

col1, col2=st.columns([2,3])
with col2:
  msg=cur.execute('SELECT messages FROM db').fetchone()
  if msg==None:
    cur.execute('INSERT INTO db(messages) VALUES ("")')
    con.commit()
  st.text_area('msg', msg[0], height=350, label_visibility='collapsed')
with col1:
  with st.form('New Message', clear_on_submit=True):
    name=st.text_input('Name')
    message=st.text_area('Message') 
    timestamp=datetime.datetime.now()
    if st.form_submit_button('Add Message'):
      newmsg=f'---  {name}   {timestamp}\n\n{message}\n\n{msg[0]}'
      cur.execute(
        'UPDATE db SET messages=? WHERE rowid=?;', 
        (newmsg, 1)
      )
      con.commit()
      st.experimental_rerun()
