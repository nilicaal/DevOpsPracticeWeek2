import json
import logging
import os
import tempfile

import pymongo
from functools import reduce
import uuid

from swagger_server.models import Student

client = pymongo.MongoClient('mongodb://example_db:27017/')
db = client["studentsdb"]
student_db = db["students"]

def add_student(student):
    if (student.first_name is None or student.last_name is None):
        return 'unable to add user, provide all details.', 405

    res = student_db.find({"first_name" : student.first_name,
                         "last_name" : student.last_name })

    if res.count() > 0:
        return 'already exists', 409

    newStudent = student.to_dict()
    # newStudent["_id"] = student.student_id
    res = student_db.insert_one(newStudent)
    return int(student.student_id), 200

# Returns a student by their ID.
def get_student_by_id(student_id, subject):
    student = student_db.find({"_id": int(student_id)})

    if student.count() < 1:
        return 'no students found', 404

    student = Student.from_dict(student)
    if not subject or subject in student.grades:
        return student
    else:
        return 'no students found', 404


def get_student_by_last_name(last_name):
    student = student_db.find({"last_name": student.last_name})

    if student.count() < 1:
        return "no students found", 404

    student = Student.from_dict(student)

    return student, 200


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id
