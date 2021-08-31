import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):
    try:
        notification_id = int(msg.get_body().decode('utf-8'))
        logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)
        
        # TODO: Get connection to database
        m_dbname = "techconfdb"
        m_user = "garima@techconfserver"
        m_password = "Jindagi123?"
        m_host = "techconfserver.postgres.database.azure.com"
        conn = psycopg2.connect(
            dbname= m_dbname, 
            user= m_user,
            password= m_password,
            host= m_host)

        cur = psycopg2.conn.cursor()

    
        # TODO: Get notification message and subject from database using the notification_id
        cur.execute("SELECT message,subject FROM notification WHERE id=%s;",(notification_id,))
        messagePlain, subject = cur.fetchone()
        cur.execute("SELECT email,first_name FROM attendee;")
        attendees = cur.fetchall()
        for attendee in attendees:
          message = Mail(
              from_email='from_email@example.com',
              to_emails=attendee[0],
              subject='{}: {}'.format(attendee[1], subject),
              html_content=messagePlain)
          try:
              sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
              response = sg.send(message)
              print(response.status_code)
              print(response.body)
              print(response.headers)
          except Exception as e:
              print(str(e))
        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        total_attendees = 'Notified {} attendees'.format(len(attendees))
        cur.execute("UPDATE notification SET status = %s WHERE id=%s;", (total_attendees,notification_id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        conn.close()