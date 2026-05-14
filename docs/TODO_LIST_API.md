# To-Do List API Documentation

## Overview

The To-Do List API provides endpoints to manage todo items with persistent local storage. All data is saved to a JSON file and persists across sessions.

## Base URL

```
http://localhost:5000/api/todos
```

## Authentication

No authentication required (local application).

## Endpoints

### 1. Get All Todos

**Endpoint:** `GET /api/todos`

**Description:** Retrieve all todo items

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1715721600000,
      "title": "Complete project",
      "description": "Finish the todo list feature",
      "priority": "high",
      "completed": false,
      "created_at": "2026-05-14T10:00:00",
      "due_date": null,
      "tags": []
    }
  ],
  "count": 1
}
```

### 2. Get Specific Todo

**Endpoint:** `GET /api/todos/<todo_id>`

**Description:** Retrieve a specific todo by ID

**Parameters:**
- `todo_id` (int, required): The ID of the todo item

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1715721600000,
    "title": "Complete project",
    "description": "Finish the todo list feature",
    "priority": "high",
    "completed": false,
    "created_at": "2026-05-14T10:00:00",
    "due_date": null,
    "tags": []
  }
}
```

### 3. Create Todo

**Endpoint:** `POST /api/todos`

**Description:** Create a new todo item

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium"
}
```

**Parameters:**
- `title` (string, required): Todo title
- `description` (string, optional): Todo description
- `priority` (string, optional): Priority level - 'low', 'medium', 'high' (default: 'medium')

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1715721600000,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium",
    "completed": false,
    "created_at": "2026-05-14T10:00:00",
    "due_date": null,
    "tags": []
  },
  "message": "Todo created successfully"
}
```

### 4. Update Todo

**Endpoint:** `PUT /api/todos/<todo_id>`

**Description:** Update a todo item

**Request Body:**
```json
{
  "title": "Buy groceries and cook dinner",
  "priority": "high",
  "due_date": "2026-05-15"
}
```

**Parameters:**
- `title` (string): Updated title
- `description` (string): Updated description
- `priority` (string): Updated priority
- `due_date` (string): Due date
- `tags` (array): Tags for the todo
- `completed` (boolean): Completion status

**Response:**
```json
{
  "success": true,
  "data": { /* updated todo */ },
  "message": "Todo updated successfully"
}
```

### 5. Complete Todo

**Endpoint:** `PUT /api/todos/<todo_id>/complete`

**Description:** Mark a todo as completed

**Response:**
```json
{
  "success": true,
  "data": { /* completed todo with completed: true */ },
  "message": "Todo marked as completed"
}
```

### 6. Uncomplete Todo

**Endpoint:** `PUT /api/todos/<todo_id>/uncomplete`

**Description:** Mark a todo as incomplete

**Response:**
```json
{
  "success": true,
  "data": { /* uncompleted todo with completed: false */ },
  "message": "Todo marked as incomplete"
}
```

### 7. Delete Todo

**Endpoint:** `DELETE /api/todos/<todo_id>`

**Description:** Delete a specific todo item

**Response:**
```json
{
  "success": true,
  "message": "Todo deleted successfully"
}
```

### 8. Delete All Todos

**Endpoint:** `DELETE /api/todos/clear/all`

**Description:** Delete all todo items

**Response:**
```json
{
  "success": true,
  "message": "Deleted 5 todos",
  "deleted_count": 5
}
```

### 9. Get Todos by Priority

**Endpoint:** `GET /api/todos/priority/<priority>`

**Description:** Get todos filtered by priority

**Parameters:**
- `priority` (string, required): 'low', 'medium', or 'high'

**Response:**
```json
{
  "success": true,
  "data": [ /* todos with specified priority */ ],
  "count": 3,
  "priority": "high"
}
```

### 10. Get Completed Todos

**Endpoint:** `GET /api/todos/status/completed`

**Description:** Get all completed todo items

**Response:**
```json
{
  "success": true,
  "data": [ /* completed todos */ ],
  "count": 2
}
```

### 11. Get Pending Todos

**Endpoint:** `GET /api/todos/status/pending`

**Description:** Get all pending (incomplete) todo items

**Response:**
```json
{
  "success": true,
  "data": [ /* pending todos */ ],
  "count": 3
}
```

### 12. Get Statistics

**Endpoint:** `GET /api/todos/stats`

**Description:** Get todo statistics

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 5,
    "completed": 2,
    "pending": 3,
    "completion_rate": 40.0,
    "high_priority": 1,
    "medium_priority": 2,
    "low_priority": 2
  }
}
```

### 13. Search Todos

**Endpoint:** `GET /api/todos/search?q=<query>`

**Description:** Search todos by title or description

**Parameters:**
- `q` (string, required): Search query

**Response:**
```json
{
  "success": true,
  "data": [ /* matching todos */ ],
  "count": 2,
  "query": "buy"
}
```

### 14. Health Check

**Endpoint:** `GET /api/todos/health`

**Description:** Check todo service health

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "stats": { /* current statistics */ }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Title is required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Todo not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error message"
}
```

## Data Model

```typescript
interface Todo {
  id: number;                    // Unique identifier (timestamp-based)
  title: string;                 // Todo title
  description: string;           // Todo description
  priority: 'low' | 'medium' | 'high';  // Priority level
  completed: boolean;            // Completion status
  created_at: string;            // Creation timestamp (ISO format)
  updated_at?: string;           // Last update timestamp
  due_date?: string;             // Due date
  tags: string[];               // Tags for categorization
}
```

## Usage Examples

### Create a high priority todo
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the todo list feature",
    "priority": "high"
  }'
```

### Get pending todos
```bash
curl http://localhost:5000/api/todos/status/pending
```

### Mark todo as completed
```bash
curl -X PUT http://localhost:5000/api/todos/1715721600000/complete
```

### Search todos
```bash
curl "http://localhost:5000/api/todos/search?q=buy"
```

### Get statistics
```bash
curl http://localhost:5000/api/todos/stats
```

## Local Storage

- All todos are stored in `backend/data/todos.json`
- Data persists across server restarts
- File is automatically created if it doesn't exist
- Human-readable JSON format for easy inspection

## Best Practices

1. **Always use meaningful titles** for todos
2. **Set appropriate priorities** for better organization
3. **Use descriptions** for complex tasks
4. **Search before creating** to avoid duplicates
5. **Regularly archive** completed todos

## Rate Limiting

No rate limiting for local storage (unlimited requests)

## Version

API Version: 1.0  
Last Updated: 2026-05-14
