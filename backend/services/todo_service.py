"""To-Do List Service - Manages todo items with persistence."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class TodoService:
    """Service for managing to-do items with file-based storage."""

    def __init__(self, storage_path: str = "data/todos.json"):
        """Initialize TodoService with storage path.
        
        Args:
            storage_path: Path to store todo items JSON file
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self.todos = self._load_todos()

    def _ensure_storage_exists(self) -> None:
        """Create storage directory and file if they don't exist."""
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir and not os.path.exists(storage_dir):
            os.makedirs(storage_dir, exist_ok=True)
        
        if not os.path.exists(self.storage_path):
            self._save_todos([])

    def _load_todos(self) -> List[Dict]:
        """Load todos from JSON file.
        
        Returns:
            List of todo items
        """
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_todos(self, todos: List[Dict]) -> None:
        """Save todos to JSON file.
        
        Args:
            todos: List of todo items to save
        """
        with open(self.storage_path, 'w') as f:
            json.dump(todos, f, indent=2)

    def create_todo(self, title: str, description: str = "", priority: str = "medium") -> Dict:
        """Create a new todo item.
        
        Args:
            title: Todo title
            description: Todo description (optional)
            priority: Priority level - 'low', 'medium', 'high' (default: 'medium')
            
        Returns:
            Created todo item
        """
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty")
        
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        
        todo = {
            'id': int(datetime.now().timestamp() * 1000),
            'title': title.strip(),
            'description': description.strip(),
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'due_date': None,
            'tags': []
        }
        
        self.todos.append(todo)
        self._save_todos(self.todos)
        return todo

    def get_all_todos(self) -> List[Dict]:
        """Get all todo items.
        
        Returns:
            List of all todos
        """
        return self.todos

    def get_todo(self, todo_id: int) -> Optional[Dict]:
        """Get a specific todo by ID.
        
        Args:
            todo_id: ID of the todo to retrieve
            
        Returns:
            Todo item or None if not found
        """
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """Update a todo item.
        
        Args:
            todo_id: ID of the todo to update
            **kwargs: Fields to update (title, description, priority, due_date, tags, etc.)
            
        Returns:
            Updated todo item or None if not found
        """
        for todo in self.todos:
            if todo['id'] == todo_id:
                # Update allowed fields
                allowed_fields = ['title', 'description', 'priority', 'due_date', 'tags', 'completed']
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        if key == 'title' and (not value or not str(value).strip()):
                            raise ValueError("Todo title cannot be empty")
                        todo[key] = value
                
                todo['updated_at'] = datetime.now().isoformat()
                self._save_todos(self.todos)
                return todo
        return None

    def complete_todo(self, todo_id: int) -> Optional[Dict]:
        """Mark a todo as completed.
        
        Args:
            todo_id: ID of the todo to complete
            
        Returns:
            Updated todo item or None if not found
        """
        return self.update_todo(todo_id, completed=True)

    def uncomplete_todo(self, todo_id: int) -> Optional[Dict]:
        """Mark a todo as incomplete.
        
        Args:
            todo_id: ID of the todo to uncomplete
            
        Returns:
            Updated todo item or None if not found
        """
        return self.update_todo(todo_id, completed=False)

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item.
        
        Args:
            todo_id: ID of the todo to delete
            
        Returns:
            True if deleted, False if not found
        """
        original_length = len(self.todos)
        self.todos = [todo for todo in self.todos if todo['id'] != todo_id]
        
        if len(self.todos) < original_length:
            self._save_todos(self.todos)
            return True
        return False

    def delete_all_todos(self) -> int:
        """Delete all todo items.
        
        Returns:
            Number of todos deleted
        """
        count = len(self.todos)
        self.todos = []
        self._save_todos(self.todos)
        return count

    def get_todos_by_priority(self, priority: str) -> List[Dict]:
        """Get todos filtered by priority.
        
        Args:
            priority: Priority level ('low', 'medium', 'high')
            
        Returns:
            List of todos with specified priority
        """
        return [todo for todo in self.todos if todo['priority'] == priority]

    def get_completed_todos(self) -> List[Dict]:
        """Get all completed todos.
        
        Returns:
            List of completed todos
        """
        return [todo for todo in self.todos if todo['completed']]

    def get_pending_todos(self) -> List[Dict]:
        """Get all pending (incomplete) todos.
        
        Returns:
            List of pending todos
        """
        return [todo for todo in self.todos if not todo['completed']]

    def get_stats(self) -> Dict:
        """Get statistics about todos.
        
        Returns:
            Dictionary with todo statistics
        """
        total = len(self.todos)
        completed = len(self.get_completed_todos())
        pending = len(self.get_pending_todos())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'high_priority': len(self.get_todos_by_priority('high')),
            'medium_priority': len(self.get_todos_by_priority('medium')),
            'low_priority': len(self.get_todos_by_priority('low'))
        }

    def search_todos(self, query: str) -> List[Dict]:
        """Search todos by title or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching todos
        """
        query = query.lower()
        return [
            todo for todo in self.todos
            if query in todo['title'].lower() or query in todo['description'].lower()
        ]
