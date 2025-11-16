import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Group, Teacher, Subject, Grade
from database import engine


Session = sessionmaker(bind=engine)
session = Session()


def create_teacher(args):
    teacher = Teacher(fullname=args.name)
    session.add(teacher)
    session.commit()
    print(f"Teacher created: id={teacher.id}, name={teacher.fullname}")


def create_group(args):
    group = Group(name=args.name)
    session.add(group)
    session.commit()
    print(f"Group created: id={group.id}, name={group.name}")


def create_student(args):
    student = Student(fullname=args.name, group_id=args.group_id)
    session.add(student)
    session.commit()
    print(f"Student created: id={student.id}, name={student.fullname}")


def create_subject(args):
    subject = Subject(name=args.name, teacher_id=args.teacher_id)
    session.add(subject)
    session.commit()
    print(f"Subject created: id={subject.id}, name={subject.name}")


def create_grade(args):
    grade = Grade(grade=args.grade, student_id=args.student_id, subject_id=args.subject_id)
    session.add(grade)
    session.commit()
    print(f"Grade created id={grade.id}")




def list_items(model):
    items = session.query(model).all()
    for item in items:
        print(item.__dict__)




def update_item(model, args):
    item = session.query(model).filter(model.id == args.id).first()
    if not item:
        print("Item not found")
        return

    if args.name:
        item.fullname = args.name if hasattr(item, "fullname") else args.name
        if hasattr(item, "name"):
            item.name = args.name

    if args.group_id and hasattr(item, "group_id"):
        item.group_id = args.group_id

    if args.teacher_id and hasattr(item, "teacher_id"):
        item.teacher_id = args.teacher_id

    session.commit()
    print("Updated:", item.__dict__)




def remove_item(model, item_id):
    item = session.query(model).filter(model.id == item_id).first()
    if not item:
        print("Item not found")
        return
    session.delete(item)
    session.commit()
    print(f"Removed id={item_id}")




models_map = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}

def main():
    parser = argparse.ArgumentParser(description="CLI tool for DB CRUD operations")

    parser.add_argument("-a", "--action", required=True, help="CRUD action: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, help="Model: Teacher, Group, Student, Subject, Grade")

    parser.add_argument("-n", "--name", help="Name for create/update")
    parser.add_argument("--id", type=int, help="ID for update/remove")

    parser.add_argument("--group_id", type=int)
    parser.add_argument("--teacher_id", type=int)
    parser.add_argument("--student_id", type=int)
    parser.add_argument("--subject_id", type=int)
    parser.add_argument("--grade", type=int)

    args = parser.parse_args()
    model = models_map.get(args.model)

    if not model:
        print("Unknown model")
        return

    # CREATE
    if args.action == "create":
        if model == Teacher:
            create_teacher(args)
        elif model == Group:
            create_group(args)
        elif model == Student:
            if not args.group_id:
                print("Student requires --group_id")
                return
            create_student(args)
        elif model == Subject:
            if not args.teacher_id:
                print("Subject requires --teacher_id")
                return
            create_subject(args)
        elif model == Grade:
            if not (args.student_id and args.subject_id and args.grade):
                print("Grade requires --student_id, --subject_id, --grade")
                return
            create_grade(args)

  
    elif args.action == "list":
        list_items(model)

    
    elif args.action == "update":
        if not args.id:
            print("Update requires --id")
            return
        update_item(model, args)

  
    elif args.action == "remove":
        if not args.id:
            print("Remove requires --id")
            return
        remove_item(model, args.id)

    else:
        print("Unknown action")


if __name__ == "__main__":
    main()
