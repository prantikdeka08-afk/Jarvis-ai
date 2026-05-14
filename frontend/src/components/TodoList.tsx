import React, { useState, useEffect } from 'react';
import '../styles/TodoList.css';

interface Todo {
  id: number;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  completed: boolean;
  created_at: string;
  due_date?: string;
  tags: string[];
}

interface Stats {
  total: number;
  completed: number;
  pending: number;
  completion_rate: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
}

const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sortBy, setSortBy] = useState<'priority' | 'date' | 'status'>('priority');

  const API_URL = 'http://localhost:5000/api/todos';

  // Load todos on component mount
  useEffect(() => {
    loadTodos();
    loadStats();
  }, []);

  // Load todos
  const loadTodos = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_URL);
      const data = await response.json();
      if (data.success) {
        setTodos(data.data);
        setError('');
      }
    } catch (err) {
      setError('Failed to load todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Load stats
  const loadStats = async () => {
    try {
      const response = await fetch(`${API_URL}/stats`);
      const data = await response.json();
      if (data.success) {
        setStats(data.data);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  // Create new todo
  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Please enter a title');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          priority
        })
      });

      const data = await response.json();
      if (data.success) {
        setTitle('');
        setDescription('');
        setPriority('medium');
        setError('');
        await loadTodos();
        await loadStats();
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Failed to create todo');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Toggle todo completion
  const handleToggleTodo = async (id: number, completed: boolean) => {
    try {
      const endpoint = completed ? 'uncomplete' : 'complete';
      const response = await fetch(`${API_URL}/${id}/${endpoint}`, {
        method: 'PUT'
      });

      const data = await response.json();
      if (data.success) {
        await loadTodos();
        await loadStats();
      }
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  // Delete todo
  const handleDeleteTodo = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        const response = await fetch(`${API_URL}/${id}`, {
          method: 'DELETE'
        });

        const data = await response.json();
        if (data.success) {
          await loadTodos();
          await loadStats();
        }
      } catch (err) {
        setError('Failed to delete todo');
        console.error(err);
      }
    }
  };

  // Search todos
  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (!query.trim()) {
      await loadTodos();
      return;
    }

    try {
      const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      if (data.success) {
        setTodos(data.data);
        setError('');
      }
    } catch (err) {
      setError('Failed to search todos');
      console.error(err);
    }
  };

  // Get filtered and sorted todos
  const getFilteredTodos = () => {
    let filtered = todos;

    // Apply status filter
    if (filter === 'completed') {
      filtered = filtered.filter(todo => todo.completed);
    } else if (filter === 'pending') {
      filtered = filtered.filter(todo => !todo.completed);
    }

    // Apply sorting
    const sorted = [...filtered].sort((a, b) => {
      if (sortBy === 'priority') {
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      } else if (sortBy === 'date') {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      } else if (sortBy === 'status') {
        return (a.completed ? 1 : 0) - (b.completed ? 1 : 0);
      }
      return 0;
    });

    return sorted;
  };

  const displayedTodos = getFilteredTodos();
  const completionPercentage = stats ? stats.completion_rate : 0;

  return (
    <div className="todo-container">
      <div className="todo-header">
        <h1>✓ My To-Do List</h1>
        <p className="subtitle">Stay organized and productive</p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.pending}</div>
            <div className="stat-label">Pending</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Completed</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{completionPercentage.toFixed(0)}%</div>
            <div className="stat-label">Completion</div>
          </div>
        </div>
      )}

      {/* Progress Bar */}
      {stats && stats.total > 0 && (
        <div className="progress-section">
          <div className="progress-label">Overall Progress</div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
          <div className="progress-text">
            {stats.completed} of {stats.total} tasks completed
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && <div className="error-message">{error}</div>}

      {/* Add Todo Form */}
      <form onSubmit={handleAddTodo} className="add-todo-form">
        <h2>Add New Task</h2>
        <div className="form-group">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input-field"
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <textarea
            placeholder="Add description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="textarea-field"
            rows={2}
            disabled={loading}
          />
        </div>
        <div className="form-row">
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
            className="select-field"
            disabled={loading}
          >
            <option value="low">🟢 Low Priority</option>
            <option value="medium">🟡 Medium Priority</option>
            <option value="high">🔴 High Priority</option>
          </select>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Adding...' : '➕ Add Task'}
          </button>
        </div>
      </form>

      {/* Search and Filter */}
      <div className="controls-section">
        <input
          type="text"
          placeholder="Search tasks..."
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          className="search-input"
        />
        <div className="filter-controls">
          <div className="filter-group">
            <label>Filter:</label>
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => { setFilter('all'); setSearchQuery(''); }}
            >
              All
            </button>
            <button
              className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
              onClick={() => { setFilter('pending'); setSearchQuery(''); }}
            >
              Pending
            </button>
            <button
              className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
              onClick={() => { setFilter('completed'); setSearchQuery(''); }}
            >
              Completed
            </button>
          </div>
          <div className="sort-group">
            <label>Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'priority' | 'date' | 'status')}
              className="sort-select"
            >
              <option value="priority">Priority</option>
              <option value="date">Date</option>
              <option value="status">Status</option>
            </select>
          </div>
        </div>
      </div>

      {/* Todos List */}
      <div className="todos-section">
        <h2>
          {filter === 'completed'
            ? 'Completed Tasks'
            : filter === 'pending'
            ? 'Pending Tasks'
            : 'All Tasks'}
          <span className="todo-count">({displayedTodos.length})</span>
        </h2>

        {displayedTodos.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <p>No tasks found</p>
            {filter !== 'all' && (
              <button
                className="btn btn-secondary"
                onClick={() => { setFilter('all'); setSearchQuery(''); }}
              >
                Clear Filters
              </button>
            )}
          </div>
        ) : (
          <div className="todos-list">
            {displayedTodos.map((todo) => (
              <div
                key={todo.id}
                className={`todo-item ${todo.completed ? 'completed' : ''} priority-${todo.priority}`}
              >
                <div className="todo-checkbox-wrapper">
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleTodo(todo.id, todo.completed)}
                    className="todo-checkbox"
                  />
                </div>
                <div className="todo-content">
                  <div className="todo-title">{todo.title}</div>
                  {todo.description && <div className="todo-description">{todo.description}</div>}
                  <div className="todo-meta">
                    <span className={`priority-badge priority-${todo.priority}`}>
                      {todo.priority.charAt(0).toUpperCase() + todo.priority.slice(1)}
                    </span>
                    <span className="todo-date">
                      {new Date(todo.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <button
                  className="btn btn-delete"
                  onClick={() => handleDeleteTodo(todo.id)}
                  title="Delete task"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoList;
