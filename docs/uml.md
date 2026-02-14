## UML - Mermaid Class Diagram

```mermaid
classDiagram
    direction TB

    class Owner {
      +string id
      +string name
      +string timezone
      +List~TimeWindow~ availability
      +get_availability(date):List~TimeWindow~
    }

    class Pet {
      +string id
      +string name
      +string species
      +string breed
      +List~Task~ tasks
      +add_task(t:Task)
      +remove_task(taskId:string)
    }

    class Task {
      +string id
      +string title
      +int duration_minutes
      +Priority priority
      +List~TimeWindow~ preferred_windows
      +bool required
    }

    class Scheduler {
      +generate_schedule(owner:Owner, pet:Pet, available_minutes:int):Schedule
      +explain_decision():string
      +score_task(t:Task):float
    }

    %% Relationships
    Owner "1" -- "0..*" Pet : owns
    Pet "1" -- "0..*" Task : has
    Scheduler ..> Task
    Scheduler ..> Owner
    Scheduler ..> Pet

```

Brief roles:
- `Owner`: user identity and availability windows.
- `Pet`: groups tasks for a specific pet.
- `Task`: duration, priority, preferred windows, required flag.
- `Scheduler`: core algorithm that builds a schedule, scores tasks, and explains decisions.

Next steps: convert these classes into Python stubs or add unit tests for scheduling behavior.
