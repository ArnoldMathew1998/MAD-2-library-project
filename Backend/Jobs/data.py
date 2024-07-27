from Database.models import UserLog, db, User, Book, BookSection, Feedback
from sqlalchemy import distinct, and_
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors

def get_inactive_users():
    active_user_ids = db.session.query(UserLog.user_id).filter(UserLog.approved.in_([1, 0])).distinct().all()
    active_user_ids = [user_id[0] for user_id in active_user_ids]
    active_user_ids.append(1)

    inactive_users = db.session.query(User).filter(~User.user_id.in_(active_user_ids)).all()
    inactive_users_data = [{'mail_id': user.mail_id, 'name': user.first_name + ' ' + user.last_name} for user in inactive_users]

    return inactive_users_data
    
def get_book_requested(user_id):
    one_month_ago = datetime.now() - timedelta(days=30)
    user_details = db.session.query(
        UserLog.book_id,
        UserLog.borrow_date,
        UserLog.return_date,
        UserLog.approved,
        Book.book_name,
        Book.author_name,
        BookSection.sec_name
    ).join(Book, UserLog.book_id == Book.book_id) \
     .join(BookSection, Book.sec_id == BookSection.sec_id) \
     .filter(
        and_(
            UserLog.user_id == user_id,
            UserLog.borrow_date >= one_month_ago
        )
    ).all()
    
    return user_details
    
def generate_activity_summary_pdf(data, user):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title = Paragraph(f"Monthly Activity Summary for {user.first_name} {user.last_name}", styles['Title'])
    elements.append(title)
    
    # Table header
    table_data = [
        ["Book ID", "Book Name", "Author", "Section", "Borrow Date", "Return Date", "Book Status"]
    ]
    
    # Table data
    for detail in data:
        book_id, borrow_date, return_date, approved, book_name, author_name, sec_name = detail
        table_data.append([
            book_id, 
            book_name, 
            author_name, 
            sec_name, 
            borrow_date.strftime('%Y-%m-%d'),
            return_date.strftime('%Y-%m-%d'), 
            approved
        ])
    
    # Create the table
    table = Table(table_data)
    
    # Table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer


