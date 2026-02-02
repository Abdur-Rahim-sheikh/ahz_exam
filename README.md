## The project is not complete

for last 8 months I have been working on other projects where db was not related.

So I forgot those syntax. During this two whole hour. I googled those params, read docs, fixed bug and Finally
only exposed 3 endpoint two to add to the respective databaes and 1 for filter query.

So i did not had enough to go to the next part for `cron job`.

Though what I did tried to make following the best practices.

Regrads,
Abdur Rahim

## The api docs

The api doc will be found in fastapi documentation
after starting the project via

```bash
uv run fastapi dev
```

open

```bash
localhost:8000/docs
```

And all is there.

**Problem Statement:**

Design and implement a RESTful API service for an online library system. The service must support full CRUD functionality for both books and authors. Key features should include data filtering, background task handling, signal processing, and optimized database queries. Integrate caching mechanisms where applicable to enhance performance.

---

## Requirements:

### 1. REST API Implementation:

- Create two models: **Author** and **Book**.
  - Author model should have a `name` and a `date_of_birth`.
  - Book model should have `title`, `author` (foreign key), `published_date`, and `genre`.
- Implement **Create** and **Read** operations for both models.
- Ensure proper serialization and validation using **Django Rest Framework**.

### 2. Filtering Data:

- Allow filtering of books based on:
  - author name
- Make the filtering available as query parameters in the `GET` request to the books endpoint.

### 3. Background Task:

- Implement a background task that runs periodically (every 30 minutes) and checks for books that have been published for over 10 years.
- For these books, set a new field `is_archived` to `True` in the database.
- Use **Celery** for task scheduling.

---

## Deliverables:

1. A Django/FastAPI project that includes the implementation of the above requirements.

---

## Constraints:

- The task should be completed within **2.0 hours**.
- You may use any third-party libraries that you deem necessary, but be sure to mention them in the **README**.
