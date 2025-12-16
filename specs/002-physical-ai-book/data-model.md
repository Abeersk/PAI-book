# Data Model: Physical AI & Humanoid Robotics Book - Modules 1 & 2

## Core Entities

### 1. ROS 2 System
- **Description**: The middleware that enables communication between different parts of a robot system
- **Attributes**:
  - Communication protocol (DDS-based)
  - Architecture type (node-based)
  - Purpose (robotic nervous system)
- **Relationships**: Contains Nodes, Topics, Services

### 2. Node
- **Description**: Independent functional units in the ROS 2 system
- **Attributes**:
  - Name (string)
  - Function (description of role)
  - Communication type (publisher/subscriber/service client/server)
- **Relationships**: Communicates via Topics and Services

### 3. Topic
- **Description**: One-way data streams for communication between nodes
- **Attributes**:
  - Name (string)
  - Message type (data structure)
  - Direction (publisher to subscriber)
- **Relationships**: Used by Publishers and Subscribers

### 4. Service
- **Description**: Request-response interactions between nodes
- **Attributes**:
  - Name (string)
  - Request type (data structure)
  - Response type (data structure)
- **Relationships**: Used by Service Clients and Service Servers

### 5. Digital Twin
- **Description**: Virtual replica of a physical robot system used for simulation
- **Attributes**:
  - Name (string)
  - Simulation environment (Gazebo/Unity)
  - Fidelity level (description)
- **Relationships**: Represents Physical Robot, uses Simulation Environment

### 6. Simulation Environment
- **Description**: Virtual space where robot behaviors and interactions are modeled
- **Attributes**:
  - Type (Gazebo/Unity)
  - Purpose (physics/visualization)
  - Capabilities (list)
- **Relationships**: Contains Robot Models, Physics Properties

### 7. URDF Model
- **Description**: Unified Robot Description Format defining robot structure
- **Attributes**:
  - Name (string)
  - Links (list of body parts)
  - Joints (list of connection points)
  - Materials (visual properties)
- **Relationships**: Defines Robot Structure, used in Simulation

### 8. AI Agent
- **Description**: Software component that makes decisions and controls robot behavior
- **Attributes**:
  - Name (string)
  - Decision-making approach (algorithm type)
  - Interface type (ROS connection method)
- **Relationships**: Connects to ROS 2 System, processes Sensor Data

## Entity Relationships

```
AI Agent --(connects via)--> ROS 2 System <--(contains)--- Node
Node --(communicates via)--> Topic/Service
ROS 2 System --(controls)--> Physical Robot (via Digital Twin)
Digital Twin --(uses)--> Simulation Environment
Simulation Environment --(contains)--> URDF Model
URDF Model --(defines)--> Robot Structure
```

## Validation Rules

1. **ROS 2 System** must contain at least one Node
2. **Node** must use either Topics or Services for communication (or both)
3. **Topic** must have exactly one publisher and may have multiple subscribers
4. **Service** must have exactly one server and may have multiple clients
5. **Digital Twin** must map to exactly one Physical Robot
6. **URDF Model** must define both Links and Joints for complete robot structure
7. **AI Agent** must connect to the ROS 2 System to control the robot