"""To-Do List API Routes."""
from flask import Blueprint, request, jsonify
from services.todo_service import TodoService

todos_bp = Blueprint('todos', __name__, url_prefix='/api/todos')
todo_service = TodoService()


@todos_bp.route('', methods=['GET'])
def get_all_todos():
    """Get all todo items."""
    try:
        todos = todo_service.get_all_todos()
        return jsonify({
            'success': True,
            'data': todos,
            'count': len(todos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID."""
    try:
        todo = todo_service.get_todo(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        return jsonify({
            'success': True,
            'data': todo
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('', methods=['POST'])
def create_todo():
    """Create a new todo item."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        title = data.get('title')
        description = data.get('description', '')
        priority = data.get('priority', 'medium')
        
        if not title:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        todo = todo_service.create_todo(title, description, priority)
        return jsonify({
            'success': True,
            'data': todo,
            'message': 'Todo created successfully'
        }), 201
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo item."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        updated_todo = todo_service.update_todo(todo_id, **data)
        if not updated_todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': updated_todo,
            'message': 'Todo updated successfully'
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    """Mark a todo as completed."""
    try:
        completed_todo = todo_service.complete_todo(todo_id)
        if not completed_todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': completed_todo,
            'message': 'Todo marked as completed'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/<int:todo_id>/uncomplete', methods=['PUT'])
def uncomplete_todo(todo_id):
    """Mark a todo as incomplete."""
    try:
        uncompleted_todo = todo_service.uncomplete_todo(todo_id)
        if not uncompleted_todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': uncompleted_todo,
            'message': 'Todo marked as incomplete'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item."""
    try:
        deleted = todo_service.delete_todo(todo_id)
        if not deleted:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/clear/all', methods=['DELETE'])
def delete_all_todos():
    """Delete all todo items."""
    try:
        count = todo_service.delete_all_todos()
        return jsonify({
            'success': True,
            'message': f'Deleted {count} todos',
            'deleted_count': count
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/priority/<priority>', methods=['GET'])
def get_todos_by_priority(priority):
    """Get todos filtered by priority."""
    try:
        if priority not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': 'Invalid priority. Must be low, medium, or high'
            }), 400
        
        todos = todo_service.get_todos_by_priority(priority)
        return jsonify({
            'success': True,
            'data': todos,
            'count': len(todos),
            'priority': priority
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/status/completed', methods=['GET'])
def get_completed_todos():
    """Get all completed todos."""
    try:
        todos = todo_service.get_completed_todos()
        return jsonify({
            'success': True,
            'data': todos,
            'count': len(todos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/status/pending', methods=['GET'])
def get_pending_todos():
    """Get all pending todos."""
    try:
        todos = todo_service.get_pending_todos()
        return jsonify({
            'success': True,
            'data': todos,
            'count': len(todos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get todo statistics."""
    try:
        stats = todo_service.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/search', methods=['GET'])
def search_todos():
    """Search todos by query."""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        todos = todo_service.search_todos(query)
        return jsonify({
            'success': True,
            'data': todos,
            'count': len(todos),
            'query': query
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@todos_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for todo service."""
    try:
        stats = todo_service.get_stats()
        return jsonify({
            'success': True,
            'status': 'healthy',
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500
