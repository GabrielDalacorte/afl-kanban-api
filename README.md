# afl-kanban-api

## Overview

The `afl-kanban-api` is a RESTful API designed to manage a kanban board system. It is built using Django and Django REST Framework, providing endpoints for managing boards, columns, and cards.

## Models

### Board
- **name**: The name of the board.
- **description**: A text field for additional details about the board.
- **created_at**: Timestamp of when the board was created.
- **owner**: A foreign key linking to the user who owns the board.
- **active**: A boolean indicating if the board is active.

### Column
- **board**: A foreign key linking to the board the column belongs to.
- **name**: The name of the column.
- **order**: An integer representing the order of the column within the board.

### Card
- **column**: A foreign key linking to the column the card belongs to.
- **delivery_date**: The date by which the card should be completed.
- **status**: The current status of the card, with choices including 'on_time', 'late', and 'done'.
- **assignee**: A foreign key linking to the user assigned to the card.
- **created_at**: Timestamp of when the card was created.

## Running the API

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd afl-kanban-api
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Pre-registered User

The system comes with a pre-registered user for testing purposes:
- **Email**: gnunes.servico@gmail.com
- **Password**: 1611

You can use these credentials to authenticate and test the API endpoints.