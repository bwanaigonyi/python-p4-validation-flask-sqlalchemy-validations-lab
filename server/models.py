from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        
        if Author.query.filter(Author.name == name).first() is not None:
            raise ValueError("Author name exists. Please enter another name")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if not number:
            raise ValueError("Phone number cannot be empty")

        if len(number) != 10 or not number.isdigit():
            raise ValueError("Invalid phone number. Phone number must be ten digits.")    

        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")

        return content    

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Maximum characters exceedeed. Summary should be 250 character max.")    

        return summary

    @validates('category')
    def validate_category(self, key, category):
        values = ['Fiction', 'Non-Fiction']

        if category not in values:
            raise ValueError("Post category is either'Fiction', 'Non-Fiction'")

        return category  

    @validates('title')
    def validate_title(self, key, title):
        clickbait_titles = ["Won't Believe", "Secret", "Top", "Guess"] 

        if not any (phrase in title for phrase in clickbait_titles):
                raise ValueError("Title must contain at least one of these clickbait- y: 'won't', 'Believe', 'Secret', 'Top', 'Guess'")

        return title        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'