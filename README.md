# NexusEnroll - University Course Enrollment System

## Software Architecture Assignment (SCS 2303)

### Project Overview
This project implements a modern university course enrollment system called "NexusEnroll" to replace the legacy "LegacyEnroll" system. The solution demonstrates the application of software design principles, design patterns, and architectural patterns.

### Architecture Choice: 3-Tier Architecture
**Justification:**
- **Scalability**: Each tier can be scaled independently based on demand
- **Maintainability**: Clear separation of concerns makes the system easier to maintain
- **Flexibility**: Easy to modify individual tiers without affecting others
- **Integration**: Well-suited for future integration with external systems (financial aid, etc.)
- **Performance**: Optimized for handling high-volume concurrent users during enrollment periods

### Design Patterns Implemented
1. **Observer Pattern**: For notification system (email notifications, waitlist updates)
2. **Factory Method Pattern**: For creating different types of users and courses
3. **Strategy Pattern**: For different enrollment validation strategies
4. **Command Pattern**: For enrollment operations (add/drop courses)
5. **Singleton Pattern**: For system configuration and logging

### Project Structure
```
nexus_enroll/
├── models/           # Business entities and data models
├── services/         # Business logic layer
├── patterns/         # Design pattern implementations
├── validators/       # Validation strategies
├── notifications/    # Observer pattern implementation
├── commands/         # Command pattern implementation
├── tests/           # Test cases and demonstrations
└── main.py          # Main application entry point
```

### Running the Application
```bash
python main.py
```

### Key Features
- Student self-service enrollment
- Faculty grade management
- Administrator system control
- Real-time notifications
- Transaction management
- Comprehensive validation
