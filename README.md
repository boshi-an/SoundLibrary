# SoundLib: A Music Recording Library

SoundLib (abbreviation of sound library), provides a site for users to upload their own music recordings.

![image](https://github.com/totorato/SoundLib/blob/main/Static/screenshot/1.png)

## Todo List

- [x] Better "User" view: need to added ways to modify user information.
- [x] Forget password: send email to reset password.
- [x] Database: need to add Recording and Composer database.
- [x] Search: search entries from databases and show the result.
- [x] Detailed view: detailed view of recordings, composers and users when clicking on entries.
- [x] About page: add an about page.
- [ ] Admin page: have access to anything.
- [x] Translations: support Chinse and English.

## Installation Guide

### Dependencies

This project requires the following dependencies:

- postgresql
- django
- psycopg2
- uwsgi

Please manually install the dependencies above. Future versions will contain a dependence list.

### Preparation

Before running, you need to config the postgresql database to a proper state. This project by default uses 'postgres' 

## Project Introduction

Clone the project, install all dependencies (django) manually, and run the server using command `python manage.py runserver` to start. For production use, please run via uwsgi (see uwsgi.ini), which automatically configures the website to non-debug mode and runs silently in the background.

### Upload Recordings

Django supports upload files, so this is not a big deal.

### Searching

Django also supports advanced searching, considering similar vocabulary, weighted words and so on:

https://docs.djangoproject.com/en/4.0/topics/db/search/

## User Guide

### Login

SoundLib only provides username-password registration. We will encrypt your password to sha256 hash values, so no one (even the developer of SoundLib) can spy on your private information.

### Browse Recordings

Soundlib provides 4 different views.

- Time Line: this view lists recordings on a timeline in ascending order of upload time.
- Members: in this view, recordings are grouped by their uploader, a filter can be further adapted to find a specific user.
- Composers: recordings can also be classified by copmosers of the piece.
- Search: searching for anything you are interested in, including recordings, members and composers.

### Upload Recordings

When an authenticated user want to upload a new recording, he or she can choose the "upload" tab and include required information in the form.

### Manage Recordings

To be determined.