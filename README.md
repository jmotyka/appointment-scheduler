# appointment-scheduler
API for allowing providers to specify which times they are available and for clients to schedule appointments.

## Setup
1. Must have python>=3.10 installed.
2. Run `python3.10 -m venv .VENV && source .VENV/bin/activate && pip install -r requirements.txt`.
3. Start server using `cd app && fastapi dev main.py`.

## Requirements
1. Clients can register themselves using `http://localhost:8000/api/clients`.
2. Providers can register themselves using `http://localhost:8000/api/providers`.
3. Providers can submit their availability in 15 minute windows using `http://localhost:8000/api/appoinments/availability`.
4. Clients can find available appointments using `http://localhost:8000/api/appointments`. Clients will only see appointments they can reserve that are 24 hours in the future.
5. Clients can reserve an appointment using `http://localhost:8000/api/appointments/reserve`.
6. Clients can confirm an appointment using `http://localhost:8000/api/appointments/confirm`.
7. Every 5 seconds, a background process runs to remove client reservations that have not been confirmed in over 30 minutes.

## Database
I used an in-memory SQLite database for this exercise. A more robust application should use a persistent database solution such as PostgresSQL.

The schema consists of 3 tables:
1. providers:
    - id: int
    - first_name: str
    - last_name: str
2. clients:
    - id: int
    - first_name: str
    - last_name: str
3. appointments:
    - id: int
    - appointment_time: datetime
    - created_time: datetime
    - booked_time: datetime
    - reservation_confirmed: boolean
    - client_id = foreign key to clients table
    - provider_id = foreign key to providers table

I thought about using a singular table for providers and clients, but keeping them separate allows us to expand the schema to fit provider/client metadata where applicable.

## Remaining work
1. The codebase does not contain docstrings. This can make it challenging for the next person to understand some pieces of logic.

2. While I was able to write some unit tests, more should be added. Especially views as there is zero test coverage with respect to endpoints.

3. I initally thought to use asynchronous functionality for a more performant web server, but worried that may be a rabbit hole. Instead I opted for a more constrainted MVP.

4. I wanted to containerize the application using Docker but ran out of time before I could piece that together. The skeleton (`Dockerfile` and `Makefile`) is present though.

5. I'm not fond of provider and client endpoints requiring `first_name`/`last_name` as lookup keys, rather than `id`. In a full-stack application we could use `id` instead as that state would be persistent through something like authentication layers.