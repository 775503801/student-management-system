from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, select
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)

# SQLite in-file DB (students.db will be created automatically)
engine = create_engine('sqlite:///students.db', echo=False, future=True)
metadata = MetaData()

students = Table(
    'students', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=True),
    Column('major', String, nullable=True)
)

# Create table if not exists
metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

# API: list students (optional search query ?q=)
@app.route('/api/students', methods=['GET'])
def list_students():
    q = request.args.get('q', '').strip()
    with engine.connect() as conn:
        if q:
            stmt = select(students).where(
                (students.c.name.ilike(f"%{q}%")) | (students.c.email.ilike(f"%{q}%"))
            )
        else:
            stmt = select(students)
        result = conn.execute(stmt).mappings().all()
        return jsonify(result)

# API: add student
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    major = data.get('major', '').strip()
    if not name:
        return jsonify({'error':'name is required'}), 400
    with engine.connect() as conn:
        stmt = students.insert().values(name=name, email=email, major=major)
        res = conn.execute(stmt)
        conn.commit()
        return jsonify({'id': res.inserted_primary_key[0], 'name': name, 'email': email, 'major': major})

# API: update student
@app.route('/api/students/<int:sid>', methods=['PUT'])
def update_student(sid):
    data = request.json or {}
    with engine.connect() as conn:
        stmt = select(students).where(students.c.id == sid)
        found = conn.execute(stmt).first()
        if not found:
            return jsonify({'error':'not found'}), 404
        upd = students.update().where(students.c.id == sid).values(
            name=data.get('name', found.name),
            email=data.get('email', found.email),
            major=data.get('major', found.major)
        )
        conn.execute(upd)
        conn.commit()
        return jsonify({'ok': True})

# API: delete student
@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    with engine.connect() as conn:
        stmt = select(students).where(students.c.id == sid)
        found = conn.execute(stmt).first()
        if not found:
            return jsonify({'error':'not found'}), 404
        d = students.delete().where(students.c.id == sid)
        conn.execute(d)
        conn.commit()
        return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
