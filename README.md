# TutorHub

## Description

TutorHub is a tutoring website that connects students in need with tutors for one-on-one sessions in specific subjects. This platform aims to bridge the gap between tutors and students, catering to college students looking to tutor and earn AICTE points.

## Installation & Setup

To run the project locally, follow these steps:

1. Clone the repository to your local machine.
2. Set up your Django environment.
3. Run the Django development server with `python manage.py runserver`.

## Features

- User authentication and registration.
- Session scheduling for tutors.
- Session booking for students.
- Review and rating system for completed sessions.
- Subject selection and profile customization for users.

## Usage

1. Visit the homepage to view available sessions or scheduled sessions based on your user type.
2. Students can book sessions, and tutors can view and manage their scheduled sessions.
3. After a session, both students and tutors can provide reviews and ratings.
4. Users can customize their subjects and profile information.

## Main Files

- `models.py`: Defines the database models for subjects, user profiles, sessions, and reviews.
- `views.py`: Contains the logic for handling user requests, session bookings, and reviews.
- `forms.py`: Includes forms for user registration, login, session creation, and reviews.

## Database

The project uses Django's default database (SQLite) with tables for subjects, user profiles, sessions, reviews, and more.

## Contribution Guidelines

If you wish to contribute to TutorHub, follow these guidelines:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and ensure they are properly tested.
4. Commit and push your changes to your forked repository.
5. Submit a pull request to the main repository, clearly explaining your contributions.

Your contributions are valuable!

## Contact

For questions, feedback, or suggestions, please reach out:

- Name: Yashas Donthi
- Email: 2yashas2@gmail.com

## Release Notes

**Version 1.0**
- Initial release

**Next Release:**

1. More test cases to ensure comprehensive coverage.
2. Students cannot book additional sessions unless they have reviewed a finished class.
3. Tutors cannot create more sessions unless they have confirmed the status of previously 'booked' classes ('finished' or 'missed') by the student.
4. Enforce reviews for both students and tutors.
