# Design Choice

## API design

### API used by prospect:

* `create_lead(session, lead_in, resume)`
serves POST request to URL `/leads/`. 

`lead_in` is request body containing info (email, fist_name, last_name) sent from client. `resume` is `File` type parameter 
receiving the resume file uploaded by client. `session` is needed for database write.

This API also sends emails, which can be refactored into an async background task.

### API used by attorney inside the company:

* `login(session, form_data)` serves POST request to URL `/login/`.

`form_data` is request body containing username and password sent from client. `session` is needed for authentication 
against credentials stored in db. This API issues a token good for 8 days after a successful auth.

* `get_leads(session, skip, limit)` serves GET request to URL `/leads/`.

`skip` and `limit` are optional query parameters to help attorney on pagination of lead info.


* `update_lead(session, id, new_state)` serves PUT request to URL `/leads/{id}/`.

Attorney can change a selected lead (associated with path parameter `id`) from PENDING to REACHED_OUT state. 
The query parameter `new_state` is Enum type with predefined values.

### User APIs
No APIs added for `User` entity at this time because there seems no requirements to
create/update/get users. The users (attorneys) can be directly inserted into db by SQL statements, not necessarily
through APIs.

## Database design

### Tables
Choose Relational Database (in particular PostgreSQL which works well with FastAPI) for data persistence (more discussion 
in Tradeoffs section below).

Two tables are defined in SQL database: 

`Lead` table:
* id (primary key)
* email (unique, index)
* first_name
* last_name
* resume
* state (enum: pending, reached_out)

`User` table - stores attorneys inside the company:
* id (primary key)
* email (unique, index)
* hashed_password
* is_active

### Media file
The resume files uploaded by prospects can be stored on local file system of the server. Capacity estimation: suppose 
average resume pdf file has 100KB, for 100K prospects, the required storage is 10GB. A server should have enough disk space.
But consider redundancy and failover, we could choose to store the resume files in Amazon S3. The data will be 
preserved even our server is failed.

## Tradeoffs
For this design, better to use Relational Database than NoSQL Database:
* This scenario doesn't require rapid and vast scalability 
because each prospect may submit one or a few leads - not like e-commerce applications where each user may generate
a lot of transaction records. Even 1M prospects are still well within the capacity of RDB (e.g. PostgreSQL 
[limits](https://www.postgresql.org/docs/current/limits.html)). 
* Data is well-defined and highly structured. Doesn't need NoSQL db for dynamic and flexible data types.
* This design needs to store credential for login. Rational database provides strong consistency.