# Task Management API Documentation

## Overview

The Task Management API provides endpoints to manage tasks. Users can perform operations such as creating, retrieving, updating, and deleting tasks. Each task is associated with a user who owns it, and only the owner can modify or delete their tasks.

## Base URL

The base URL for the API is `/api/`.

## Authentication

The API uses Token-based authentication. Users need to include their authentication token in the header of each request.

### Authentication Header Example

```plaintext
Authorization: Token <user_token>
```

## Endpoints

### 1. List and Create Tasks

#### `GET /api/tasks/`

##### Description

Retrieves a list of all tasks.

##### Request

No request parameters required.

##### Response

Returns a list of tasks with their details.

#### `POST /api/tasks/`

##### Description

Creates a new task.

##### Request

Include task details in the request body as JSON.

##### Example Request Body

```json
{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2024-02-28",
  "status": "Pending"
}
```

##### Response

Returns the details of the newly created task.

### 2. Retrieve, Update, and Delete a Task

#### `GET /api/tasks/<int:pk>/`

##### Description

Retrieves details of a specific task.

##### Request

No request parameters required.

##### Response

Returns the details of the requested task.

#### `PATCH /api/tasks/<int:pk>/`

##### Description

Updates details of a specific task.

##### Request

Include the updated task details in the request body as JSON.

##### Example Request Body

```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "due_date": "2024-03-05",
  "status": "In Progress"
}
```

##### Response

Returns the updated details of the task.

#### `DELETE /api/tasks/<int:pk>/`

##### Description

Deletes a specific task.

##### Request

No request parameters required.

##### Response

Returns no content upon successful deletion.

### 3. Permissions

- Users must be authenticated to access any task-related endpoint.
- Users can only retrieve, update, or delete tasks they own.

### 4. Examples

#### Retrieve Task List

```http
GET /api/tasks/
```

#### Create a Task

```http
POST /api/tasks/
Content-Type: application/json
Authorization: Token <user_token>

{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2024-02-28",
  "status": "Pending"
}
```

#### Retrieve a Task

```http
GET /api/tasks/<task_id>/
Authorization: Token <user_token>
```

#### Update a Task

```http
PATCH /api/tasks/<task_id>/
Content-Type: application/json
Authorization: Token <user_token>

{
  "title": "Updated Task",
  "description": "Updated description",
  "due_date": "2024-03-05",
  "status": "In Progress"
}
```

#### Delete a Task

```http
DELETE /api/tasks/<task_id>/
Authorization: Token <user_token>
```

## Error Handling

In case of errors, the API will return appropriate HTTP status codes along with error messages in the response body.

- `400 Bad Request`: Invalid request.
- `401 Unauthorized`: Authentication failure.
- `403 Forbidden`: User does not have permission for the requested action.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Server-side error.

## Additional Information

- Task ownership middleware is enforced to ensure users can only manipulate tasks they own.
- Each task includes details such as title, description, due date, and status.
- The API follows RESTful principles for CRUD operations on tasks.
- Token-based authentication provides secure access to the API endpoints.