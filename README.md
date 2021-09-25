# Simple Learning Management System API

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

[Report Bug][project-issues-link]
·
[Request Feature][project-issues-link]


## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the project locally](#running-the-project-locally)
  - [Running the project with Docker](#running-the-project-locally-with-docker)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)



## Getting Started

### Prerequisites

[![Python Version][python-shield]][python-url]
[![Poetry Version][poetry-shield]][poetry-url]
[![Docker Version][docker-shield]][docker-url]
[![Django Version][django-shield]][django-url]
[![Django REST Version][djangorest-shield]][djangorest-url]


### Running the project locally
[(Back to top)](#table-of-contents)

1. Clone the repo
   ```sh
   git clone https://github.com/relidaar/lms-api.git
   ```
2. Change your directory
   ```sh
   cd lms-api
   ```
3. Initialize Poetry shell 
   ```sh
   poetry shell
   ``` 
4. Install Poetry dependencies
   ```sh
   poetry install
   ```
5. Apply project migrations
   ```sh
   python manage.py migrate
   ```
6. Run the development server 
   ```sh
   python manage.py runserver
   ```


### Running the project locally with Docker
[(Back to top)](#table-of-contents)

1. Clone the repo
   ```sh
   git clone https://github.com/relidaar/lms-api.git
   ```
2. Change your directory
   ```sh
   cd lms-api
   ```
3. Create Docker images with docker-compose
   ```sh
   docker-compose build
   ```
5. Run created Docker images
   ```sh
   docker-compose up
   ```



### Running the project in production with Docker
[(Back to top)](#table-of-contents)

1. Clone the repo
   ```sh
   git clone https://github.com/relidaar/lms-api.git
   ```
2. Change your directory
   ```sh
   cd lms-api
   ```
3. Create .env file
   ```sh
   SECRET_KEY=<YOUR_SECRET_KEY>
   DEBUG=False
   DOMAIN_NAME=<YOUR_DOMAIN>
   ALLOWED_HOSTS=<YOUR_DOMAIN>

   POSTGRES_DB=<YOUR_DB>
   POSTGRES_USER=<YOUR_POSTGRES_USER>
   POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD>
   DATABASE_URL=psql://[user]:[password]@[host]:[port]/[db_name]
   ```
3. Create Docker images with docker-compose
   ```sh
   docker-compose -f docker-compose.prod.yml build
   ```
5. Run created Docker images
   ```sh
   docker-compose -f docker-compose.prod.yml up -d
   ```



## Roadmap
[(Back to top)](#table-of-contents)

See the [open issues][project-issues-link] for a list of proposed features (and known issues).



## Contributing
[(Back to top)](#table-of-contents)

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License
[(Back to top)](#table-of-contents)

Distributed under the MIT License. See  [`LICENSE`][license-url] for more information.



## Contact
[(Back to top)](#table-of-contents)

Oleksandr Sviatetskyi - alex.sviatetskyi@outlook.com

Project Link: [https://github.com/relidaar/lms-api][project-link]

[![LinkedIn][linkedin-shield]][linkedin-url]



[project-link]: https://github.com/relidaar/lms-api
[project-issues-link]: https://github.com/relidaar/lms-api/issues

[contributors-shield]: https://img.shields.io/github/contributors/relidaar/lms-api?style=for-the-badge
[contributors-url]: https://github.com/relidaar/lms-api/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/relidaar/lms-api?style=for-the-badge
[forks-url]: https://github.com/relidaar/lms-api/network/members

[issues-shield]: https://img.shields.io/github/issues/relidaar/lms-api?style=for-the-badge
[issues-url]: https://github.com/relidaar/lms-api/issues

[license-shield]: https://img.shields.io/github/license/relidaar/lms-api?style=for-the-badge
[license-url]: https://github.com/relidaar/lms-api/blob/main/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/oleksandr-sviatetskyi-45424b143/

[python-shield]: https://img.shields.io/badge/python-3.9-brightgreen.svg?style=flat-square
[python-url]: https://python.org

[poetry-shield]:  https://img.shields.io/badge/poetry-1.1.6-brightgreen.svg?style=flat-square
[poetry-url]: https://python-poetry.org/

[docker-shield]:  https://img.shields.io/badge/docker--brightgreen.svg?style=flat-square
[docker-url]: https://www.docker.com/

[django-shield]: https://img.shields.io/badge/django-3.1.8-brightgreen.svg?style=flat-square
[django-url]: https://djangoproject.com

[djangorest-shield]: https://img.shields.io/badge/django_rest-3.12.4-brightgreen.svg?style=flat-square
[djangorest-url]: https://www.django-rest-framework.org/
