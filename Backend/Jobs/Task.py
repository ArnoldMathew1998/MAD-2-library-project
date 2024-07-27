from Database.models import UserLog, db, User, Book, BookSection, Feedback
from Jobs.data import get_inactive_users,get_book_requested,generate_activity_summary_pdf
from Jobs.mailing import send_email,send_activity_summary_email
from celery import shared_task 
from celery import Celery
import matplotlib.pyplot as plt
import pandas as pd
import csv
from io import StringIO

celery_app = Celery('tasks', result_backend='redis://localhost:6379/2', broker_url='redis://localhost:6379/1')


@shared_task()
def generate_chart():
    # Fetching data
    user_logs = UserLog.query.join(Book, UserLog.book_id == Book.book_id).all()
    feedbacks = Feedback.query.all()

    # 1. Total Revenue Chart (Line Chart)
    if user_logs:
        logs_data = [{'borrow_date': log.borrow_date, 'price': log.book.price} for log in user_logs if log.approved == 1 or log.approved == -2]
        df_logs = pd.DataFrame(logs_data)
        df_logs['borrow_date'] = pd.to_datetime(df_logs['borrow_date'])
        df_logs = df_logs.sort_values('borrow_date')
        df_logs['cumulative_sum'] = df_logs['price'].cumsum()

        plt.figure(figsize=(10, 6))
        plt.plot(df_logs['borrow_date'], df_logs['cumulative_sum'], marker='o')
        plt.title('Total Revenue Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Revenue')
        plt.grid(True)
        plt.savefig('../Frontend/src/assets/admin/total_revenue.png')  # Save the chart as an image
        plt.close()
    else:
        # Create an empty chart if no user logs
        plt.figure(figsize=(10, 6))
        plt.plot([], [])
        plt.title('Total Revenue Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Revenue')
        plt.grid(True)
        plt.savefig('../Frontend/src/assets/admin/total_revenue.png')  # Save the chart as an image
        plt.close()

    # 2. Customer Satisfaction Chart
    if feedbacks:
        feedback_data = [{'book_id': feedback.book_id, 'rating': feedback.feedback_rating} for feedback in feedbacks]
        df_feedback = pd.DataFrame(feedback_data)
        avg_feedback = df_feedback.groupby('book_id').mean().reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(avg_feedback['book_id'], avg_feedback['rating'])
        plt.title('Customer Satisfaction')
        plt.xlabel('Book ID')
        plt.ylabel('Average Rating')
        plt.savefig('../Frontend/src/assets/admin/customer_satisfaction.png')  # Save the chart as an image
        plt.close()

        # 3. Top-Rated Book Chart
        top_rated_books = avg_feedback.sort_values(by='rating', ascending=False).head(10)
        plt.figure(figsize=(10, 6))
        plt.bar(top_rated_books['book_id'], top_rated_books['rating'])
        plt.title('Top Rated Books')
        plt.xlabel('Book ID')
        plt.ylabel('Average Rating')
        plt.savefig('../Frontend/src/assets/admin/top_rated_books.png')  # Save the chart as an image
        plt.close()
    else:
        # Create empty charts if no feedback
        plt.figure(figsize=(10, 6))
        plt.bar([], [])
        plt.title('Customer Satisfaction')
        plt.xlabel('Book ID')
        plt.ylabel('Average Rating')
        plt.savefig('../Frontend/src/assets/admin/customer_satisfaction.png')  # Save the chart as an image
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.bar([], [])
        plt.title('Top Rated Books')
        plt.xlabel('Book ID')
        plt.ylabel('Average Rating')
        plt.savefig('../Frontend/src/assets/admin/top_rated_books.png')  # Save the chart as an image
        plt.close()

    # 4. Active and Non-Active Users Chart
    active_user_ids = db.session.query(UserLog.user_id).filter(UserLog.approved.in_([1, 0])).distinct().all()
    active_users = [user_id[0] for user_id in active_user_ids]
    
    non_active_users = db.session.query(User).filter(~User.user_id.in_(active_users)).all()
    non_active_users = [user.user_id for user in non_active_users]
    
    num_active_users = len(active_users)
    num_non_active_users = len(non_active_users)-1

    plt.figure(figsize=(6, 4))
    plt.bar(['Active Users', 'Non-Active Users'], [num_active_users, num_non_active_users])
    plt.title('Active vs Non-Active Users')
    plt.ylabel('Number of Users')
    plt.savefig('../Frontend/src/assets/admin/active_non_active_users.png')  # Save the chart as an image
    plt.close()

@celery_app.task
def generate_csv():
    # Query the database to gather the necessary information
    results = db.session.query(
        User.user_id,
        User.first_name,
        User.last_name,
        UserLog.log_id.label('Approval_ID'),
        UserLog.approved.label('Approval_Status'),
        UserLog.borrow_date.label('Date'),
        Book.book_id.label('Book_ID'),
        Book.book_name.label('Book_Name'),
        Book.author_name.label('Author_Name'),
        Feedback.feedback_rating.label('Feedback_Rating'),
        Feedback.feedback_text.label('Feedback_Text')
    ).join(UserLog, User.user_id == UserLog.user_id, isouter=True) \
     .join(Book, UserLog.book_id == Book.book_id, isouter=True) \
     .join(Feedback, (User.user_id == Feedback.user_id) & (Book.book_id == Feedback.book_id), isouter=True) \
     .order_by(User.user_id).all()

    # Create a list of dictionaries for the CSV
    data = []
    i = 1
    for row in results:
        if row.Date is not None:
            data.append({
                'S.No.': i,
                'Date': row.Date.strftime('%Y-%m-%d'),  # Format the date to 'YYYY-MM-DD'
                'User ID': row.user_id,
                'User Name': f"{row.first_name} {row.last_name}",
                'Approval ID': row.Approval_ID,
                'Approval Status': row.Approval_Status,
                'Book ID': row.Book_ID,
                'Book Name': row.Book_Name,
                'Author Name': row.Author_Name,
                'Feedback Rating': row.Feedback_Rating,
                'Feedback Text': row.Feedback_Text,
            })
            i += 1

    # Create a CSV file
    output = StringIO()
    column_names = ['S.No.', 'Date', 'User ID', 'User Name', 'Approval ID', 'Approval Status', 'Book ID', 'Book Name', 'Author Name', 'Feedback Rating', 'Feedback Text']
    
    writer = csv.DictWriter(output, fieldnames=column_names)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    filename = 'report.csv'
    with open(filename, 'w') as f:
        f.write(output.getvalue())

    return filename

@shared_task()
def reminder_email():
    inactive_users = get_inactive_users()
    for user in inactive_users:
        send_email(user['mail_id'], "We Miss You!", "It looks like you haven't read any books recently. Come back for more knowledge!", user['name'])

@shared_task()
def monthly_activity_summary():
    users = User.query.all()
    for user in users:
        user_id = user.user_id
        if user.role != 'admin': 
            user_details = get_book_requested(user_id)
            pdf_file = generate_activity_summary_pdf(user_details, user)
            send_activity_summary_email(user.mail_id, "Your Monthly Book Activity Summary", pdf_file, user)  
