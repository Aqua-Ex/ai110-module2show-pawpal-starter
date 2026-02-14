# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I only added four classes (Owner, Pet, Task, Scheduler). The relations inlcude Owner owning pets and pets having a task, while schulder passes down information to every other class. As for responsibilites: Owner class stores information about the owner and sets their avaliable times; Pets stores infomation about the pets and links to their tasks; Tasks store information about specific tasks and sets priority and preferred times; Scheduler generates schedules, explains reasoning behind such schedlues and scores tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    Yes, I added a Recurrence Pattern which tracks how often a task repeats(Daily, weekly, etc). The way it was done before had no way to determine if a task was overdue. Adding recurrence patterns enables the is_overdue() method to properly prioritize tasks
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers constraints in time, priority, status, recency and dependencies. I decided which constraints mattered most in
the order of Time>Status>Priority>Preferences as this order made the most logical sense. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Tradeoff: Greedy scheduling vs. optimal global scheduling**

My scheduler uses a greedy algorithm, it scores and schedules tasks one at a time in priority order, rather than trying every possible combination to find the mathematically optimal schedule. Once a task is placed, it doesn't backtrack or rearrange earlier decisions. If the scheduler used a backtracking algorithim, the run time would drastically go up to the point where the better scheduling is not worth the time constraints.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

For brainstorming I would describe my ideas and tasks to claude and ask for implemntation ideas and from there decide the best options. Debugging
was a mix of manual searching and using claude to search through the codebase for errors. Refactoring worked similarly to how i did brainstorming.

These were the most helpful prompts 
- Specific feature requests: "Add logic so daily/weekly tasks auto-create new instances when completed"
- Constraint-based requests: "If they already exist, don't change any code" - prevented unnecessary modifications
- Quality requirements: "Use Streamlit components like st.warning to make conflict warnings helpful to pet owners"
- Performance-focused: "Suggest small algorithms that make the scheduler more efficient"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

 When I asked AI to implement the original uml diagram, it added extra classes that I felt were unecessary at the time. I told it to stick to four major classes and to create the uml based on that. As for how I evaluated it, I just read the relationships of the uml diagram and realised it was way to convuluted for what I was trying to achieve.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?


**TEST 1: Out-of-order task addition** - Verifies that tasks added in random order still get scheduled chronologically
- *Why important*: Ensures `sort_by_time()` and binary insertion work correctly

**TEST 2: Filtering by completion status** - Tests `get_completed_tasks()` and `get_incomplete_tasks()`
- *Why important*: Pet owners need to see what's done vs. what's pending

**TEST 3: Filtering by pet name** - Tests cross-pet task filtering for multi-pet owners
- *Why important*: Owners with multiple pets need to manage tasks separately

**TEST 4: Sorting by time attribute** - Validates chronological sorting with explicit time windows
- *Why important*: Schedule display must show tasks in the order they'll occur

**TEST 5: Recurring task auto-creation (6 sub-tests)** - Tests all 5 recurrence patterns (DAILY, WEEKLY, BIWEEKLY, MONTHLY, AS_NEEDED)
- *Why important*: Core feature - failing here would break task continuity

**TEST 6: Conflict detection (3 scenarios)** - Tests overlapping tasks, same-time conflicts, and warning reporting
- *Why important*: Ensures scheduler doesn't silently fail on conflicts but provides helpful feedback

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am around 90% confident that it works as intended. When I did my manual testing there was not any specfic
issue or bug that caught my attention to much. The app worked how i envisoned it for the most part. As for edge cases
I would like to test how it would deal with different time zones or a large number of tasks and time windows to stress test.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with the loading times for generating scheduling. The schedule is generated almost instantly and if I was a customer, I would appreciate that.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Would add some sort of machine learning to the algorithim so it could learn from the users choices and the time that they complete certain tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned how detailed you have to be when designing systems, even if you're prompt engineering. As for AI, I learned not to trust the AI blindly,
it frequently goes off the rails if you leave it to its own judgements.