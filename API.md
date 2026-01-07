# API Documentation - Julian Personal Assistant

## Table of Contents
- [Core Components](#core-components)
- [JulianAssistant API](#julianassistant-api)
- [ScheduleManager API](#schedulemanager-api)
- [FinanceManager API](#financemanager-api)
- [DataAdvisor API](#dataadvisor-api)

---

## Core Components

### JulianAssistant

Main orchestrator class for the AI assistant.

#### Initialization

```python
from julian_assistant import JulianAssistant

# Basic initialization
assistant = JulianAssistant()

# With custom session ID
assistant = JulianAssistant(session_id="my_session_123")

# Using context manager (recommended)
with JulianAssistant() as assistant:
    # Use assistant
    pass
```

#### Methods

##### `greet() -> str`
Returns greeting message to user.

```python
greeting = assistant.greet()
print(greeting)
```

##### `process_command(user_input: str) -> str`
Process natural language command and return response.

```python
response = assistant.process_command("jadwal hari ini")
print(response)
```

Supported commands:
- Schedule: `jadwal hari ini`, `jadwal minggu ini`, `statistik jadwal`
- Finance: `saldo`, `ringkasan bulan ini`, `statistik keuangan`
- Data: `tips data`, `kategori tips`, `saran visualisasi`
- Help: `bantuan`, `help`

##### `get_conversation_history() -> List[Dict[str, str]]`
Get conversation history for current session.

```python
history = assistant.get_conversation_history()
for message in history:
    print(f"{message['role']}: {message['content']}")
```

##### `close()`
Close database connection. Automatically called when using context manager.

```python
assistant.close()
```

---

## ScheduleManager API

Manage schedules and calendar events.

### Initialization

```python
from julian_assistant.modules import ScheduleManager
from julian_assistant.core import db

session = db.get_session()
schedule_manager = ScheduleManager(session)
```

### Methods

#### `create_schedule()`

Create a new schedule entry.

**Parameters:**
- `title` (str, required): Title of the event
- `start_time` (datetime, required): Start time
- `description` (str, optional): Event description
- `end_time` (datetime, optional): End time
- `location` (str, optional): Event location
- `priority` (str, optional): Priority level ("low", "medium", "high")

**Returns:** `Schedule` object

**Example:**
```python
from datetime import datetime, timedelta

tomorrow = datetime.now() + timedelta(days=1)
schedule = schedule_manager.create_schedule(
    title="Team Meeting",
    start_time=tomorrow.replace(hour=10, minute=0),
    end_time=tomorrow.replace(hour=11, minute=0),
    description="Weekly team sync",
    location="Conference Room A",
    priority="high"
)
print(f"Created: {schedule.id} - {schedule.title}")
```

#### `get_schedule(schedule_id: int)`

Get schedule by ID.

**Returns:** `Schedule` object or `None`

```python
schedule = schedule_manager.get_schedule(1)
if schedule:
    print(schedule.title)
```

#### `get_today_schedules()`

Get all schedules for today.

**Returns:** `List[Schedule]`

```python
today_schedules = schedule_manager.get_today_schedules()
for schedule in today_schedules:
    print(f"{schedule.start_time.strftime('%H:%M')} - {schedule.title}")
```

#### `get_upcoming_schedules(days: int = 7)`

Get upcoming schedules for next N days.

**Returns:** `List[Schedule]`

```python
upcoming = schedule_manager.get_upcoming_schedules(days=7)
```

#### `update_schedule(schedule_id: int, **kwargs)`

Update schedule fields.

```python
schedule_manager.update_schedule(
    schedule_id=1,
    title="Updated Title",
    status="completed"
)
```

#### `delete_schedule(schedule_id: int)`

Delete a schedule.

**Returns:** `bool` (True if successful)

```python
success = schedule_manager.delete_schedule(1)
```

#### `mark_completed(schedule_id: int)`

Mark schedule as completed.

```python
schedule_manager.mark_completed(1)
```

#### `get_schedule_conflicts(start_time: datetime, end_time: datetime)`

Check for schedule conflicts in time range.

**Returns:** `List[Schedule]`

```python
conflicts = schedule_manager.get_schedule_conflicts(
    start_time=datetime(2026, 1, 15, 10, 0),
    end_time=datetime(2026, 1, 15, 11, 0)
)
```

#### `get_statistics()`

Get schedule statistics.

**Returns:** `Dict[str, Any]` with keys:
- `total`: Total number of schedules
- `completed`: Number of completed schedules
- `pending`: Number of pending schedules
- `completion_rate`: Completion percentage

```python
stats = schedule_manager.get_statistics()
print(f"Completion rate: {stats['completion_rate']:.1f}%")
```

---

## FinanceManager API

Manage financial transactions (income and expenses).

### Initialization

```python
from julian_assistant.modules import FinanceManager
from julian_assistant.core import db

session = db.get_session()
finance_manager = FinanceManager(session)
```

### Methods

#### `add_income()`

Add income transaction.

**Parameters:**
- `amount` (float, required): Amount
- `category` (str, required): Category (e.g., "Gaji", "Bonus")
- `description` (str, optional): Description
- `date` (datetime, optional): Transaction date (default: now)
- `payment_method` (str, optional): Payment method
- `tags` (str, optional): Comma-separated tags

**Returns:** `FinanceTransaction` object

```python
income = finance_manager.add_income(
    amount=5000000,
    category="Gaji",
    description="Salary for January 2026",
    payment_method="bank_transfer",
    tags="work,salary"
)
```

#### `add_expense()`

Add expense transaction. Same parameters as `add_income()`.

```python
expense = finance_manager.add_expense(
    amount=500000,
    category="Makanan",
    description="Monthly groceries",
    payment_method="cash"
)
```

#### `get_transaction(transaction_id: int)`

Get transaction by ID.

```python
transaction = finance_manager.get_transaction(1)
```

#### `get_transactions()`

Get filtered transactions.

**Parameters (all optional):**
- `transaction_type` (str): "income" or "expense"
- `start_date` (datetime): Start date filter
- `end_date` (datetime): End date filter
- `category` (str): Category filter

**Returns:** `List[FinanceTransaction]`

```python
# Get all expenses
expenses = finance_manager.get_transactions(transaction_type="expense")

# Get transactions for January 2026
transactions = finance_manager.get_transactions(
    start_date=datetime(2026, 1, 1),
    end_date=datetime(2026, 2, 1)
)
```

#### `get_monthly_summary(year: int, month: int)`

Get monthly financial summary.

**Returns:** `Dict[str, Any]` with keys:
- `period`: Period string (e.g., "2026-01")
- `total_income`: Total income
- `total_expense`: Total expense
- `balance`: Net balance
- `expense_by_category`: Dict of expenses per category

```python
summary = finance_manager.get_monthly_summary(2026, 1)
print(f"Balance: {summary['balance']}")
for category, amount in summary['expense_by_category'].items():
    print(f"  {category}: {amount}")
```

#### `get_balance()`

Get total balance (income - expense).

```python
balance = finance_manager.get_balance()
print(f"Current balance: IDR {balance:,.2f}")
```

#### `delete_transaction(transaction_id: int)`

Delete a transaction.

```python
finance_manager.delete_transaction(1)
```

#### `get_statistics(days: int = 30)`

Get financial statistics for last N days.

**Returns:** `Dict[str, Any]`

```python
stats = finance_manager.get_statistics(days=30)
print(f"Total income: {stats['total_income']}")
print(f"Total expense: {stats['total_expense']}")
print(f"Average expense: {stats['avg_expense']}")
```

---

## DataAdvisor API

Provide data literacy tips and statistical analysis.

### Initialization

```python
from julian_assistant.modules import DataAdvisor

advisor = DataAdvisor()
```

### Methods

#### `get_random_tip(category: str = None)`

Get random data/statistics tip.

```python
# Random tip from any category
tip = advisor.get_random_tip()
print(tip)

# Random tip from specific category
tip = advisor.get_random_tip(category="python_pandas")
print(tip)
```

#### `get_tips_by_category(category: str)`

Get all tips from a category.

**Available categories:**
- `statistik_dasar`
- `visualisasi_data`
- `analisis_data`
- `data_cleaning`
- `python_pandas`

```python
tips = advisor.get_tips_by_category("statistik_dasar")
for tip in tips:
    print(f"- {tip}")
```

#### `get_all_categories()`

Get list of all available categories.

```python
categories = advisor.get_all_categories()
print(categories)
```

#### `analyze_dataframe(df: pd.DataFrame)`

Analyze pandas DataFrame and provide insights.

**Returns:** `Dict[str, Any]` with:
- `shape`: DataFrame shape
- `columns`: Column names
- `dtypes`: Data types
- `missing_values`: Missing value counts
- `numeric_summary`: Statistics for numeric columns
- `recommendations`: List of recommendations

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, None, 4, 5],
    'B': [10, 20, 30, 40, 50]
})

analysis = advisor.analyze_dataframe(df)
print(f"Shape: {analysis['shape']}")
for rec in analysis['recommendations']:
    print(f"- {rec}")
```

#### `suggest_visualization(data_type: str, num_categories: int = 1)`

Suggest visualization type for data.

**Data types:**
- `numeric`: Numeric data
- `categorical`: Categorical data
- `time_series`: Time series data
- `bivariate`: Two variables

```python
suggestion = advisor.suggest_visualization("numeric")
print(f"Chart: {suggestion['chart_type']}")
print(f"Reason: {suggestion['reason']}")
print(f"Library: {suggestion['library']}")
```

#### `calculate_basic_stats(data: List[float])`

Calculate basic statistics from list of numbers.

**Returns:** `Dict[str, float]` with:
- `count`, `mean`, `median`, `std`, `min`, `max`, `q25`, `q75`

```python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
stats = advisor.calculate_basic_stats(data)
print(f"Mean: {stats['mean']}")
print(f"Median: {stats['median']}")
print(f"Std Dev: {stats['std']}")
```

---

## Data Models

### Schedule Model

```python
class Schedule:
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    priority: str  # "low", "medium", "high"
    status: str    # "pending", "completed", "cancelled"
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime
```

### FinanceTransaction Model

```python
class FinanceTransaction:
    id: int
    transaction_type: str  # "income", "expense"
    category: str
    amount: float
    currency: str
    description: str
    date: datetime
    payment_method: str
    tags: str
    created_at: datetime
    updated_at: datetime
```

---

## Complete Example

```python
from julian_assistant import JulianAssistant
from datetime import datetime, timedelta

# Use assistant with context manager
with JulianAssistant() as assistant:
    # Add schedule
    tomorrow = datetime.now() + timedelta(days=1)
    schedule = assistant.schedule_manager.create_schedule(
        title="Important Meeting",
        start_time=tomorrow.replace(hour=14, minute=0),
        priority="high"
    )
    print(f"Schedule created: {schedule.id}")
    
    # Add financial transactions
    assistant.finance_manager.add_income(
        amount=5000000,
        category="Gaji"
    )
    assistant.finance_manager.add_expense(
        amount=500000,
        category="Makanan"
    )
    
    # Get balance
    balance = assistant.finance_manager.get_balance()
    print(f"Balance: IDR {balance:,.2f}")
    
    # Get data tip
    tip = assistant.data_advisor.get_random_tip()
    print(f"Tip: {tip}")
    
    # Process natural language command
    response = assistant.process_command("jadwal hari ini")
    print(response)
```

---

For more examples, see the `examples/` directory.
