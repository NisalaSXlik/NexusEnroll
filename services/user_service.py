"""
User Service - Business logic for user management operations.
Handles user creation, authentication, and profile management.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from models.user import User, Student, Faculty, Administrator, UserType
from patterns.factory import UserFactoryProducer, UserType as FactoryUserType
from patterns.observer import Subject


class UserService(Subject):
    """
    Service for managing users in the system.
    Implements the Observer pattern for user-related notifications.
    """
    
    def __init__(self):
        super().__init__()
        self._users: Dict[str, User] = {}
        self._user_sessions: Dict[str, Dict] = {}  # session_id -> user_info
        self._login_attempts: Dict[str, List[datetime]] = {}  # user_id -> list of login attempts
    
    def create_user(self, user_data: Dict) -> Tuple[bool, Optional[User], str]:
        """
        Create a new user using the Factory pattern.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Tuple of (success, user_object, message)
        """
        try:
            # Validate required fields
            if 'user_type' not in user_data:
                return False, None, "User type is required"
            
            # Convert string to UserType enum
            try:
                user_type = UserType(user_data['user_type'].lower())
            except ValueError:
                return False, None, f"Invalid user type: {user_data['user_type']}"
            
            # Check if user already exists
            if user_data['user_id'] in self._users:
                return False, None, "User ID already exists"
            
            # Create user using factory
            factory = UserFactoryProducer.get_factory(user_type)
            user = factory.create_user(user_data)
            
            # Store user
            self._users[user.user_id] = user
            
            # Notify observers
            self.notify("user_created", {
                'user_id': user.user_id,
                'user_type': user.user_type.value,
                'name': user.name,
                'timestamp': datetime.now()
            })
            
            return True, user, "User created successfully"
            
        except Exception as e:
            return False, None, f"User creation failed: {str(e)}"
    
    def authenticate_user(self, user_id: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate a user (simplified implementation).
        In a real system, this would verify against a secure password store.
        """
        try:
            # Check if user exists
            if user_id not in self._users:
                return False, None, "User not found"
            
            user = self._users[user_id]
            
            # Check if user is active
            if not user.is_active:
                return False, None, "User account is deactivated"
            
            # Simple password check (in real system, use proper hashing)
            # For demo purposes, we'll accept any non-empty password
            if not password or len(password) < 1:
                return False, None, "Invalid password"
            
            # Record login attempt
            if user_id not in self._login_attempts:
                self._login_attempts[user_id] = []
            self._login_attempts[user_id].append(datetime.now())
            
            # Create session
            session_id = f"session_{user_id}_{datetime.now().timestamp()}"
            self._user_sessions[session_id] = {
                'user_id': user_id,
                'user_type': user.user_type.value,
                'login_time': datetime.now(),
                'last_activity': datetime.now()
            }
            
            # Notify observers
            self.notify("user_login", {
                'user_id': user_id,
                'user_type': user.user_type.value,
                'session_id': session_id,
                'timestamp': datetime.now()
            })
            
            return True, user, f"Login successful. Session: {session_id}"
            
        except Exception as e:
            return False, None, f"Authentication failed: {str(e)}"
    
    def logout_user(self, session_id: str) -> bool:
        """Logout a user and invalidate their session."""
        if session_id in self._user_sessions:
            user_info = self._user_sessions[session_id]
            user_id = user_info['user_id']
            
            # Notify observers
            self.notify("user_logout", {
                'user_id': user_id,
                'session_id': session_id,
                'timestamp': datetime.now()
            })
            
            # Remove session
            del self._user_sessions[session_id]
            return True
        
        return False
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID."""
        return self._users.get(user_id)
    
    def get_user_by_session(self, session_id: str) -> Optional[User]:
        """Get a user by their session ID."""
        if session_id in self._user_sessions:
            user_id = self._user_sessions[session_id]['user_id']
            return self._users.get(user_id)
        return None
    
    def update_user_profile(self, user_id: str, updates: Dict) -> Tuple[bool, str]:
        """Update user profile information."""
        if user_id not in self._users:
            return False, "User not found"
        
        user = self._users[user_id]
        
        try:
            # Update allowed fields
            if 'name' in updates:
                user._name = updates['name']
            if 'email' in updates:
                user._email = updates['email']
            
            # Type-specific updates
            if isinstance(user, Student) and 'major' in updates:
                user._major = updates['major']
            elif isinstance(user, Faculty) and 'department' in updates:
                user._department = updates['department']
            elif isinstance(user, Administrator) and 'department' in updates:
                user._department = updates['department']
            
            # Notify observers
            self.notify("user_updated", {
                'user_id': user_id,
                'updates': updates,
                'timestamp': datetime.now()
            })
            
            return True, "Profile updated successfully"
            
        except Exception as e:
            return False, f"Profile update failed: {str(e)}"
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account."""
        if user_id not in self._users:
            return False
        
        user = self._users[user_id]
        user.deactivate()
        
        # Notify observers
        self.notify("user_deactivated", {
            'user_id': user_id,
            'user_type': user.user_type.value,
            'timestamp': datetime.now()
        })
        
        return True
    
    def activate_user(self, user_id: str) -> bool:
        """Activate a user account."""
        if user_id not in self._users:
            return False
        
        user = self._users[user_id]
        user.activate()
        
        # Notify observers
        self.notify("user_activated", {
            'user_id': user_id,
            'user_type': user.user_type.value,
            'timestamp': datetime.now()
        })
        
        return True
    
    def get_all_users(self, user_type: Optional[UserType] = None) -> List[User]:
        """Get all users, optionally filtered by type."""
        users = list(self._users.values())
        
        if user_type:
            users = [user for user in users if user.user_type == user_type]
        
        return users
    
    def get_user_statistics(self) -> Dict:
        """Get user statistics for the system."""
        total_users = len(self._users)
        active_users = len([user for user in self._users.values() if user.is_active])
        inactive_users = total_users - active_users
        
        # Count by type
        type_counts = {}
        for user in self._users.values():
            user_type = user.user_type.value
            type_counts[user_type] = type_counts.get(user_type, 0) + 1
        
        # Active sessions
        active_sessions = len(self._user_sessions)
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'user_type_distribution': type_counts,
            'active_sessions': active_sessions
        }
    
    def get_login_attempts(self, user_id: str, hours: int = 24) -> List[datetime]:
        """Get login attempts for a user within the specified hours."""
        if user_id not in self._login_attempts:
            return []
        
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        attempts = self._login_attempts[user_id]
        
        return [attempt for attempt in attempts if attempt.timestamp() > cutoff_time]
    
    def is_user_locked(self, user_id: str, max_attempts: int = 5, hours: int = 1) -> bool:
        """Check if a user account is locked due to too many login attempts."""
        recent_attempts = self.get_login_attempts(user_id, hours)
        return len(recent_attempts) >= max_attempts
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """Get permissions for a user."""
        if user_id not in self._users:
            return []
        
        user = self._users[user_id]
        return user.get_permissions()
    
    def validate_user_access(self, user_id: str, required_permission: str) -> bool:
        """Validate if a user has a specific permission."""
        permissions = self.get_user_permissions(user_id)
        return required_permission in permissions
    
    def search_users(self, query: str, user_type: Optional[UserType] = None) -> List[User]:
        """Search for users by name or email."""
        results = []
        query_lower = query.lower()
        
        for user in self._users.values():
            if user_type and user.user_type != user_type:
                continue
            
            if (query_lower in user.name.lower() or 
                query_lower in user.email.lower() or 
                query_lower in user.user_id.lower()):
                results.append(user)
        
        return results
