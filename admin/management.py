class AdminManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminManager, cls).__new__(cls)
        return cls._instance

    def create_course(self, course_factory, course_type, **kwargs):
        return course_factory.create_course(course_type, **kwargs)

    def delete_course(self, catalogue, course_id):
        # Assume catalogue has remove_course(course_id)
        catalogue.remove_course(course_id)

    def override_enrolment(self, enrolment_service, student, course):
        # Directly enrol ignoring validation
        return course.enrol_student(student)
