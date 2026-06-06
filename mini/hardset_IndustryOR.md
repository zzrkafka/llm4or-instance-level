# Both-fail instance set (IndustryOR)

59 instances where BOTH 3B and ORLM-8B are wrong. 3B modes: {'WRONG_FORMULATION': 16, 'SOLVE_FAILED': 34, 'CODE_BUG': 9}


## Case 1  [WRONG_FORMULATION]

**GT:** -99999  |  **3B:** 18.4 (Optimal)  |  **8B:** 8.7

### Question
A strategic bomber squadron has been ordered to destroy enemy military targets. It is known that there are four key areas, and destroying any one of them will achieve the objective. To complete this mission, the limits are set at $48000 \mathrm{~L}$ of gasoline, 48 heavy bombs, and 32 light bombs. When the aircraft carries heavy bombs, it can fly $2 \mathrm{~km}$ per liter of gasoline, and when it carries light bombs, it can fly $3 \mathrm{~km}$ per liter of gasoline. It is also known that each aircraft can only carry one bomb at a time, and each bombing mission consumes gasoline for the round trip (when empty, it can fly $4 \mathrm{~km}$ per liter of gasoline), as well as $100 \mathrm{~L}$ for takeoff and landing each time. The relevant data is shown in Table 1-17.

Table 1-17
\begin{tabular}{c|c|c|c}
\hline \multirow{2}{*}{ Key Area } & \multirow{2}{*}{ Distance from Base $/ \mathrm{km}$} & \multicolumn{2}{|c}{ Probability of Destruction } \\
\cline { 3 - 4 } & 450 & Per Heavy Bomb & Per Light Bomb \\
\hline 1 & 480 & 0.10 & 0.08 \\
2 & 540 & 0.20 & 0.16 \\
3 & 600 & 0.15 & 0.12 \\
4 & 0.25 & 0.20 \\
\hline
\end{tabular}

To maximize the probability of destroying enemy military targets, how should the bombing plan be determined? Establish a linear programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Define the probabilities and distances from base
probabilities = {
    1: {'heavy': 0.10, 'light': 0.08},
    2: {'heavy': 0.20, 'light': 0.16},
    3: {'heavy': 0.15, 'light': 0.12},
    4: {'heavy': 0.25, 'light': 0.20}
}

distances = {
    1: 480,
    2: 540,
    3: 600,
    4: 250
}

# Define the problem
prob = LpProblem("BomberMission", LpMaximize)

# Decision variables: x[i] is the number of heavy bombs for area i, y[i] is the number of light bombs for area i
x = {i: LpVariable(f"x_{i}", lowBound=0) for i in probabilities.keys()}
y = {i: LpVariable(f"y_{i}", lowBound=0) for i in probabilities.keys()}

# Objective function: maximize probability of destroying all key areas
prob += lpSum([probabilities[i]['heavy'] * x[i] + probabilities[i]['light'] * y[i] for i in probabilities])

# Constraints:
# 1. Total number of heavy bombs and light bombs cannot exceed the limit
prob += lpSum([x[i] for i in probabilities]) <= 48, "HeavyBombsLimit"
prob += lpSum([y[i] for i in probabilities]) <= 32, "LightBombsLimit"

# 2. Total distance flown by all aircrafts must be within the limit
total_distance = lpSum([
    (distances[i] + 4) * x[i] / 100 + distances[i] * y[i] / 100 for i in probabilities
])
prob += total_distance <= 48000, "GasolineLimit"

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Objective: {prob.objective.value()}")
```

This code sets up and solves a linear programming model to determine how many heavy and light bombs should be used for each key area to maximize the probability of destroying all four key areas while adhering to the constraints on gasoline, heavy bombs, and light bombs.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem for the strategic bomber squadron, we will establish a linear programming model to maximize the probability of destroying enemy military targets while considering the limits of gasoline and bombs. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): The number of times the \(i\)th aircraft carries the \(j\)th type of bomb to the \(k\)th key area, where \(i\) represents the aircraft number, \(j\) represents the bomb type (heavy or light), and \(k\) represents the key area.

### Objective Function:
- Maximize the probability of destruction: \[Z = \sum_{i=1}^{16} \sum_{j \in \{heavy, light\}} \sum_{k=1}^{4} p_{jk} \cdot x_{ijk}\]
  - This function calculates the total probability of destruction based on the number of times each aircraft carries each type of bomb to each key area and the probability of destruction per bomb.

### Constraints:
1. Gasoline limit: \[\sum_{i=1}^{16} \sum_{k=1}^{4} (2 \cdot d_k + 100) \cdot x_{iheavyk} + \sum_{i=1}^{16} \sum_{k=1}^{4} (3 \cdot d_k + 100) \cdot x_{ilightk} \leq 48000\]
   - This ensures that the total amount of gasoline used for all bombing missions does not exceed the limit.
2. Heavy bomb limit: \[\sum_{i=1}^{16} \sum_{k=1}^{4} x_{iheavyk} \leq 48\]
   - This ensures that the total number of heavy bombs used for all bombing missions does not exceed the limit.
3. Light bomb limit: \[\sum_{i=1}^{16} \sum_{k=1}^{4} x_{ilightk} \leq 32\]
   - This ensures that the total number of light bombs used for all bombing missions does not exceed the limit.
4. Each aircraft can only carry one bomb at a time: \[x_{iheavyk} + x_{ilightk} \leq 1, \forall i, k\]
   - This ensures that each aircraft can only carry one bomb at a time.

### Non-negativity and Integer Constraints:
- \(x_{ijk} \geq 0\) and must be integers, as the number of bombing missions must be integers.

Using this model, we can apply linear programming techniques to find the optimal number of bombing missions for each aircraft to carry each type of bomb to each key area, maximizing the probability of destruction while satisfying the limits of gasoline and bombs. This will provide the strategic bomber squadron with an optimized bombing plan.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for the strategic bomber squadron:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("StrategicBomberOptimization")

# Define parameters
num_planes = 16
bomb_types = ['heavy', 'light']
target_areas = range(1, 5)
gasoline_limit = 48000
heavy_bomb_limit = 48
light_bomb_limit = 32
distance = {1: 480, 2: 540, 3: 600, 4: 450}
prob_heavy = {1: 0.10, 2: 0.20, 3: 0.15, 4: 0.25}
prob_light = {1: 0.08, 2: 0.16, 3: 0.12, 4: 0.20}

# Add decision variables
x = {(i, j, k): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}_{k}") for i in range(1, num_planes+1) for j in bomb_types for k in target_areas}

# Objective function: Maximize the probability of destruction
objective = cp.quicksum(prob_heavy[k] * x[i, 'heavy', k] + prob_light[k] * x[i, 'light', k] for i in range(1, num_planes+1) for k in target_areas)
model.setObjective(objective, sense=COPT.MAXIMIZE)

# Constraints
# Gasoline limit
model.addConstr(cp.quicksum((2 * distance[k] + 100) * x[i, 'heavy', k] for i in range(1, num_planes+1) for k in target_areas) +
                cp.quicksum((3 * distance[k] + 100) * x[i, 'light', k] for i in range(1, num_planes+1) for k in target_areas) <= gasoline_limit, name="GasolineLimit")

# Heavy bomb limit
model.addConstr(cp.quicksum(x[i, 'heavy', k] for i in range(1, num_planes+1) for k in target_areas) <= heavy_bomb_limit, name="HeavyBombLimit")

# Light bomb limit
model.addConstr(cp.quicksum(x[i, 'light', k] for i in range(1, num_planes+1) for k in target_areas) <= light_bomb_limit, name="LightBombLimit")

# Each aircraft can only carry one bomb at a time
for i in range(1, num_planes+1):
    for k in target_areas:
        model.addConstr(x[i, 'heavy', k] + x[i, 'light', k] <= 1, name=f"PlaneBombLimit_{i}_{k}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized probability of destruction: {:.2f}".format(model.objval))
    for i in range(1, num_planes+1):
        for j in bomb_types:
            for k in target_areas:
                if x[i, j, k].x > 0:
                    print(f"Aircraft {i} carries {j} bomb to key area {k} {int(x[i, j, k].x)} times")
else:
    print("No optimal solution found.")
```

This script defines the parameters of the problem, including the number of aircraft, bomb types, key areas, limits of gasoline and bombs, distances, and probabilities of destruction. Then, it creates decision variables `x` representing the number of times each aircraft carries each type of bomb to each key area.

The objective function is to maximize the probability of destruction, calculated by summing the probabilities of destruction for each aircraft carrying each type of bomb to each key area.

The constraints include the gasoline limit, heavy bomb limit, light bomb limit, and the constraint that each aircraft can only carry one bomb at a time.

Finally, the script solves the model and outputs the maximized probability of destruction and the optimal bombing plan (if an optimal solution is found).

Note that this script assumes you have installed the `coptpy` library and have a valid license. If you do not have a license, you can consider using other optimization libraries such as `PuLP` or `OR-Tools`.

---

## Case 2  [SOLVE_FAILED]

**GT:** 16.0  |  **3B:** 1620.0 (Infeasible)  |  **8B:** No Best Solution

### Question
Mary is planning her dinner for tonight. Each 100 grams of okra contains 3.2 grams of fiber, each 100 grams of carrots contains 2.7 grams of fiber, each 100 grams of celery contains 1.6 grams of fiber, and each 100 grams of cabbage contains 2 grams of fiber. How many grams of each food should Mary purchase to maximize her fiber intake?

She is considering choosing either salmon, beef, or pork as her protein source.

She is also considering selecting at least two vegetables from okra, carrots, celery, and cabbage.

Salmon is priced at $4 per 100 grams, beef at $3.6, and pork at $1.8. Okra is priced at $2.6 per 100 grams, carrots at $1.2, celery at $1.6, and cabbage at $2.3. Mary has a budget of $15 for this meal.

The total intake of food is 600 grams.

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Mary's Dinner", LpMaximize)

# Decision variables: amount of each food in grams
okra = LpVariable('Okra', lowBound=0)
carrots = LpVariable('Carrots', lowBound=0)
celery = LpVariable('Celery', lowBound=0)
cabbage = LpVariable('Cabbage', lowBound=0)
salmon = LpVariable('Salmon', lowBound=0, upBound=None)
beef = LpVariable('Beef', lowBound=0, upBound=None)
pork = LpVariable('Pork', lowBound=0, upBound=None)

# Objective function: maximize fiber intake
prob += 3.2*okra + 2.7*carrots + 1.6*celery + 2*cabbage + salmon + beef + pork

# Constraints:
# Total food amount is 600 grams
prob += okra + carrots + celery + cabbage + salmon + beef + pork == 600

# At least two vegetables (okra, carrots, celery, cabbage)
prob += okra + carrots + celery + cabbage >= 2

# Budget constraint: total cost <= $15
cost = 2.6*okra + 1.2*carrots + 1.6*celery + 2.3*cabbage + 4*salmon + 3.6*beef + 1.8*pork
prob += cost <= 15

# Solve the problem
prob.solve()

# Display results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total fiber intake: {value(prob.objective)} grams")
```

This code sets up and solves a linear programming problem to maximize Mary's fiber intake while adhering to her constraints. The objective is to find the optimal amount of each food item she should purchase within her budget and total food quantity requirements.

### ORLM-8B formulation
## Mathematical Model:
To help Mary maximize her fiber intake while staying within her budget, we can construct a linear programming model. Here is the detailed formulation of the model:

### Decision Variables:
- \(x_1\): Grams of salmon purchased (100 grams as the unit).
- \(x_2\): Grams of beef purchased (100 grams as the unit).
- \(x_3\): Grams of pork purchased (100 grams as the unit).
- \(x_4\): Grams of okra purchased (100 grams as the unit).
- \(x_5\): Grams of carrots purchased (100 grams as the unit).
- \(x_6\): Grams of celery purchased (100 grams as the unit).
- \(x_7\): Grams of cabbage purchased (100 grams as the unit).

### Objective Function:
- Maximize fiber intake: \(Z = 3.2x_4 + 2.7x_5 + 1.6x_6 + 2x_7\)

### Constraints:
1. Budget constraint: \(4x_1 + 3.6x_2 + 1.8x_3 + 2.6x_4 + 1.2x_5 + 1.6x_6 + 2.3x_7 \leq 15\)
2. Total intake constraint: \(x_1 + x_2 + x_3 + x_4 + x_5 + x_6 + x_7 = 600\)
3. At least two vegetables constraint:
   - \(x_4 \geq 1\) (At least 100 grams of okra)
   - \(x_5 \geq 1\) (At least 100 grams of carrots)
   - \(x_6 \geq 1\) (At least 100 grams of celery)
   - \(x_7 \geq 1\) (At least 100 grams of cabbage)
4. Non-negativity constraint:
   - \(x_1, x_2, x_3, x_4, x_5, x_6, x_7 \geq 0\)

Using this model, we can apply linear programming techniques to find the optimal quantities of each food to purchase, maximizing fiber intake while staying within the budget and meeting the total intake and vegetable requirements. This will provide Mary with an optimal dinner plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("DinnerPlanning")

# Add decision variables
x1 = model.addVar(lb=0, name="Salmon")  # Grams of salmon
x2 = model.addVar(lb=0, name="Beef")    # Grams of beef
x3 = model.addVar(lb=0, name="Pork")    # Grams of pork
x4 = model.addVar(lb=0, name="Okra")    # Grams of okra
x5 = model.addVar(lb=0, name="Carrot")  # Grams of carrots
x6 = model.addVar(lb=0, name="Celery")  # Grams of celery
x7 = model.addVar(lb=0, name="Cabbage") # Grams of cabbage

# Set the objective function: Maximize fiber intake
model.setObjective(3.2*x4 + 2.7*x5 + 1.6*x6 + 2*x7, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(4*x1 + 3.6*x2 + 1.8*x3 + 2.6*x4 + 1.2*x5 + 1.6*x6 + 2.3*x7 <= 15, name="BudgetConstraint")
model.addConstr(x1 + x2 + x3 + x4 + x5 + x6 + x7 == 600, name="TotalIntakeConstraint")
model.addConstr(x4 >= 1, name="MinOkraConstraint")
model.addConstr(x5 >= 1, name="MinCarrotConstraint")
model.addConstr(x6 >= 1, name="MinCeleryConstraint")
model.addConstr(x7 >= 1, name="MinCabbageConstraint")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized fiber intake: {:.2f} grams".format(model.objval))
    print("Grams of salmon: {:.2f}".format(x1.x))
    print("Grams of beef: {:.2f}".format(x2.x))
    print("Grams of pork: {:.2f}".format(x3.x))
    print("Grams of okra: {:.2f}".format(x4.x))
    print("Grams of carrots: {:.2f}".format(x5.x))
    print("Grams of celery: {:.2f}".format(x6.x))
    print("Grams of cabbage: {:.2f}".format(x7.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the maximized fiber intake and the optimal quantities of each food.

This script provides a complete example of using the `coptpy` library to solve Mary's dinner planning problem while satisfying all the constraints mentioned in the problem.

---

## Case 3  [CODE_BUG]

**GT:** 16.0  |  **3B:** None (?)  |  **8B:** No Best Solution

### Question
A new company is opening in a small town and needs to decide how to deliver its products to customers in surrounding cities. The company can choose from three modes of transportation: cars, trucks, and buses. Each car trip generates 100 units of pollution, each truck trip generates 80 units of pollution, and each bus trip generates 110 units of pollution. The company needs to minimize the total amount of pollution.

The company can only choose a maximum of two out of the three modes of transportation.

Due to restrictions on road transportation, the number of truck trips cannot exceed 10.

Each car trip can transport 25 units of products, each truck trip can transport 30 units of products, and each bus trip can transport 40 units of products. The company needs to transport at least 500 units of products.

The number of bus trips should not exceed one-fifth of the total number of trips.

The total number of trips must be less than or equal to 15.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpInteger

# Create a problem
prob = LpProblem("Transportation_Pollution_Minimization", LpMinimize)

# Decision variables: number of trips for each mode of transportation
x1 = LpVariable('Cars', 0, None, LpInteger)
x2 = LpVariable('Trucks', 0, None, LpInteger)
x3 = LpVariable('Buses', 0, None, LpInteger)

# Objective function: minimize total pollution
prob += lpSum([100*x1 + 80*x2 + 110*x3]), "Total_Pollution"

# Constraints
# Maximum of two out of three modes of transportation
prob += x1 + x2 + x3 <= 2, "Max_Two_Trips"
# Truck trips cannot exceed 10
prob += x2 <= 10, "Trucks_Max_10"
# At least 500 units of products need to be transported
prob += lpSum([25*x1 + 30*x2 + 40*x3]) >= 500, "Products_Transported"
# Bus trips should not exceed one-fifth of the total number of trips
prob += x3 <= (x1 + x2 + x3) / 5, "Buses_Max_Fifth_Trips"
# Total number of trips must be less than or equal to 15
prob += x1 + x2 + x3 <= 15, "Total_Trips_Less_Or_Equal_To_15"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Pollution: {value(prob.objective))}")
```

Please note that there are a few issues with the formulation of the constraints and objective function. Specifically, the constraint for "Products_Transported" should be formulated as an equality since we need to transport exactly 500 units. Also, the objective function is currently set up to minimize total pollution, but it might not make sense in this context if there are other objectives or constraints that should influence the solution.

Here's a corrected version of the code:

```python
from pulp import LpProblem, LpVariable, lpSum, LpInteger

# Create a problem
prob = LpProblem("Transportation_Pollution_Minimization", LpMinimize)

# Decision variables: number of trips for each mode of transportation
x1 = LpVariable('Cars', 0, None, LpInteger)
x2 = LpVariable('Trucks', 0, None, LpInteger)
x3 = LpVariable('Buses', 0, None, LpInteger)

# Objective function: minimize total pollution
prob += lpSum([100*x1 + 80*x2 + 110*x3]), "Total_Pollution"

# Constraints
# Maximum of two out of three modes of transportation
prob += x1 + x2 + x3 <= 2, "Max_Two_Trips"
# Truck trips cannot exceed 10
prob += x2 <= 10, "Trucks_Max_10"
# At least 500 units of products need to be transported (equality constraint)
prob += lpSum([25*x1 + 30*x2 + 40*x3]) == 500, "Products_Transported"
# Bus trips should not exceed one-fifth of the total number of trips
prob += x3 <= (x1 + x2 + x3) / 5, "Buses_Max_Fifth_Trips"
# Total number of trips must be less than or equal to 15
prob += x1 + x2 + x3 <= 15, "Total_Trips_Less_Or_Equal_To_15"

# Solve the problem
status = prob.solve()

if status == LpStatusOptimal:
    print(f"Total Pollution: {value(prob.objective))}")
else:
    print("No solution found")

for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
```

This code should now correctly formulate and solve the problem.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_C \): Number of car trips
- \( x_T \): Number of truck trips
- \( x_B \): Number of bus trips
- \( y_C \): 1 if car trips are chosen, 0 otherwise
- \( y_T \): 1 if truck trips are chosen, 0 otherwise
- \( y_B \): 1 if bus trips are chosen, 0 otherwise

### Objective Function:
- Minimize total pollution: \[ \min Z = 100x_C + 80x_T + 110x_B \]

### Constraints:
1. Maximum of two modes of transportation can be chosen:
   - \( y_C + y_T + y_B \leq 2 \)
2. Number of truck trips cannot exceed 10:
   - \( x_T \leq 10 \)
3. At least 500 units of products need to be transported:
   - \( 25x_C + 30x_T + 40x_B \geq 500 \)
4. Number of bus trips should not exceed one-fifth of the total number of trips:
   - \( x_B \leq \frac{1}{5}(x_C + x_T + x_B) \)
5. Total number of trips must be less than or equal to 15:
   - \( x_C + x_T + x_B \leq 15 \)
6. If car trips are chosen, the number of car trips must be at least 1:
   - \( x_C \geq y_C \)
7. If truck trips are chosen, the number of truck trips must be at least 1:
   - \( x_T \geq y_T \)
8. If bus trips are chosen, the number of bus trips must be at least 1:
   - \( x_B \geq y_B \)

## Python Code Solution Using `coptpy`:
```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("TransportationOptimization")

# Add decision variables
x_C = model.addVar(vtype=COPT.INTEGER, name="x_C")  # Number of car trips
x_T = model.addVar(vtype=COPT.INTEGER, name="x_T")  # Number of truck trips
x_B = model.addVar(vtype=COPT.INTEGER, name="x_B")  # Number of bus trips
y_C = model.addVar(vtype=COPT.BINARY, name="y_C")   # 1 if car trips are chosen, 0 otherwise
y_T = model.addVar(vtype=COPT.BINARY, name="y_T")   # 1 if truck trips are chosen, 0 otherwise
y_B = model.addVar(vtype=COPT.BINARY, name="y_B")   # 1 if bus trips are chosen, 0 otherwise

# Objective function: Minimize total pollution
model.setObjective(100 * x_C + 80 * x_T + 110 * x_B, sense=COPT.MINIMIZE)

# Constraints
model.addConstr(y_C + y_T + y_B <= 2, name="MaxTwoTypes")
model.addConstr(x_T <= 10, name="MaxTrucks")
model.addConstr(25 * x_C + 30 * x_T + 40 * x_B >= 500, name="MinTransport")
model.addConstr(x_B <= (1/5) * (x_C + x_T + x_B), name="MaxBuses")
model.addConstr(x_C + x_T + x_B <= 15, name="MaxTrips")
model.addConstr(x_C >= y_C, name="CarLogic")
model.addConstr(x_T >= y_T, name="TruckLogic")
model.addConstr(x_B >= y_B, name="BusLogic")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total pollution: {:.2f} units".format(model.objval))
    print("Number of car trips: {:.2f}".format(x_C.x))
    print("Number of truck trips: {:.2f}".format(x_T.x))
    print("Number of bus trips: {:.2f}".format(x_B.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total pollution and the number of trips for each mode of transportation.

---

## Case 4  [SOLVE_FAILED]

**GT:** 4685100  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
An Italian transportation company needs to transport some empty containers from its 6 warehouses (located in Verona, Perugia, Rome, Pescara, Taranto, and La Spezia) to major national ports (Genoa, Venice, Ancona, Naples, Bari). The inventory of containers in each warehouse is as follows:

|  | Empty Containers |
| :---: | :---: |
| Verona | 10 |
| Perugia | 12 |
| Rome | 20 |
| Pescara | 24 |
| Taranto | 18 |
| La Spezia | 40 |

The demand at the ports is as follows:

|  | Container Demand |
| :---: | :---: |
| Genoa | 20 |
| Venice | 15 |
| Ancona | 25 |
| Naples | 33 |
| Bari | 21 |

The transportation will be done by a fleet of trucks. The transportation cost for each container is directly proportional to the distance traveled by the truck, at a rate of 30 euros per kilometer. Each truck can transport a maximum of 2 containers. The distances are as follows:

|  | Genoa | Venice | Ancona | Naples | Bari |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Verona | $290 \mathrm{~km}$ | $115 \mathrm{~km}$ | $355 \mathrm{~km}$ | $715 \mathrm{~km}$ | $810 \mathrm{~km}$ |
| Perugia | $380 \mathrm{~km}$ | $340 \mathrm{~km}$ | $165 \mathrm{~km}$ | $380 \mathrm{~km}$ | $610 \mathrm{~km}$ |
| Rome | $505 \mathrm{~km}$ | $530 \mathrm{~km}$ | $285 \mathrm{~km}$ | $220 \mathrm{~km}$ | $450 \mathrm{~km}$ |
| Pescara | $655 \mathrm{~km}$ | $450 \mathrm{~km}$ | $155 \mathrm{~km}$ | $240 \mathrm{~km}$ | $315 \mathrm{~km}$ |
| Taranto | $1010 \mathrm{~km}$ | $840 \mathrm{~km}$ | $550 \mathrm{~km}$ | $305 \mathrm{~km}$ | $95 \mathrm{~km}$ |
| La Spezia | $1072 \mathrm{~km}$ | $1097 \mathrm{~km}$ | $747 \mathrm{~km}$ | $372 \mathrm{~km}$ | $333 \mathrm{~km}$ |

Write a mathematical program to find the transportation policy that minimizes cost and solve it using COPTPY.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Container_Transportation_Problem", LpMinimize)

# Define decision variables: x[i][j] is 1 if a truck departs from warehouse i to port j, else 0
x = {(i, j): LpVariable(f"x_{i}_{j}", lowBound=0, cat='Binary') for i in range(6) for j in range(5)}

# Objective function: minimize total transportation cost
prob += lpSum([30 * distances[i][j] * x[(i, j)] for i in range(6) for j in range(5)])

# Constraints: demand satisfaction at each port
for j in range(5):
    prob += lpSum([x[(i, j)] for i in range(6)]) == demands[j]

# Constraints: supply limit from each warehouse
for i in range(6):
    prob += lpSum([x[(i, j)] for j in range(5)]) <= supplies[i]

# Solve the problem
prob.solve()

# Print the solution
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Cost = ", value(prob.objective))
```

To run this code, you need to define the `distances` and `demands` lists based on the provided distances table. Also, create a list `supplies` with the inventory of containers in each warehouse.

Here is an example for the initial setup:

```python
# Distances from warehouses to ports (in km)
distances = [
    [290, 115, 505, 655, 1010],
    [380, 340, 530, 450, 840],
    [20, 12, 20, 24, 18],
    [240, 380, 220, 240, 315],
    [95, 550, 305, 305, 95],
    [372, 1097, 747, 372, 333]
]

# Demands at ports
demands = [20, 15, 25, 33, 21]

# Supplies from warehouses (containers)
supplies = [10, 12, 20, 24, 18, 40]
```

Please replace the `distances`, `demands`, and `supplies` with actual data.

### ORLM-8B formulation
## Mathematical Model:
To solve the transportation problem for the Italian transportation company, we need to construct a mathematical model to minimize the total transportation cost while satisfying the container demand at the ports and the container supply at the warehouses. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): The number of containers transported from warehouse \(i\) to port \(j\), where \(i\) represents the warehouses (Verona, Perugia, Rome, Pescara, Taranto, La Spezia) and \(j\) represents the ports (Genoa, Venice, Ancona, Naples, Bari).

### Objective Function:
- Minimize the total transportation cost: \[Z = \sum_{i \in \text{Warehouses}} \sum_{j \in \text{Ports}} (30 \times \text{Distance}_{ij} \times x_{ij})\]
  - This function calculates the total transportation cost based on the transportation cost per kilometer, the distance, and the number of containers.

### Constraints:
1. Container demand at the ports: \[\sum_{i \in \text{Warehouses}} x_{ij} = \text{Demand}_j, \forall j \in \text{Ports}\]
   - This ensures that the container demand at each port is met by the number of containers sent from the warehouses.
2. Container supply at the warehouses: \[\sum_{j \in \text{Ports}} x_{ij} \leq \text{Supply}_i, \forall i \in \text{Warehouses}\]
   - This ensures that the total number of containers shipped from each warehouse does not exceed the container supply at that warehouse.
3. Truck capacity constraint: \[x_{ij} \leq 2, \forall i \in \text{Warehouses}, \forall j \in \text{Ports}\]
   - This ensures that the number of containers transported from each warehouse to each port does not exceed the maximum capacity of a truck.

### Non-negativity and Integer Constraints:
- \(x_{ij} \geq 0\) and must be integers, as the number of containers must be integers.

Using this model, we can apply integer linear programming techniques to find the optimal number of containers to be transported from each warehouse to each port, minimizing the total transportation cost while satisfying the container demand at the ports and the container supply at the warehouses. This will provide the transportation company with an economically efficient transportation strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the transportation problem for the Italian transportation company:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ContainerTransportation")

# Define warehouses and ports
warehouses = ["Verona", "Perugia", "Rome", "Pescara", "Taranto", "La Spezia"]
ports = ["Genoa", "Venice", "Ancona", "Naples", "Bari"]

# Define container supply at warehouses
supply = {"Verona": 10, "Perugia": 12, "Rome": 20, "Pescara": 24, "Taranto": 18, "La Spezia": 40}

# Define container demand at ports
demand = {"Genoa": 20, "Venice": 15, "Ancona": 25, "Naples": 33, "Bari": 21}

# Define transportation distances
distances = {
    "Verona": {"Genoa": 290, "Venice": 115, "Ancona": 355, "Naples": 715, "Bari": 810},
    "Perugia": {"Genoa": 380, "Venice": 340, "Ancona": 165, "Naples": 380, "Bari": 610},
    "Rome": {"Genoa": 505, "Venice": 530, "Ancona": 285, "Naples": 220, "Bari": 450},
    "Pescara": {"Genoa": 655, "Venice": 450, "Ancona": 155, "Naples": 240, "Bari": 315},
    "Taranto": {"Genoa": 1010, "Venice": 840, "Ancona": 550, "Naples": 305, "Bari": 95},
    "La Spezia": {"Genoa": 1072, "Venice": 1097, "Ancona": 747, "Naples": 372, "Bari": 333}
}

# Define decision variables
x = {}
for i in warehouses:
    for j in ports:
        x[i, j] = model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}")

# Set the objective function
model.setObjective(cp.quicksum(30 * distances[i][j] * x[i, j] for i in warehouses for j in ports), sense=COPT.MINIMIZE)

# Add constraints
# Container demand at ports
for j in ports:
    model.addConstr(cp.quicksum(x[i, j] for i in warehouses) == demand[j], name=f"Demand_{j}")

# Container supply at warehouses
for i in warehouses:
    model.addConstr(cp.quicksum(x[i, j] for j in ports) <= supply[i], name=f"Supply_{i}")

# Truck capacity constraint
for i in warehouses:
    for j in ports:
        model.addConstr(x[i, j] <= 2, name=f"TruckCapacity_{i}_{j}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total transportation cost: {:.2f} euros".format(model.objval))
    print("Transportation plan:")
    for i in warehouses:
        for j in ports:
            if x[i, j].x > 0:
                print(f"Transport {int(x[i, j].x)} containers from {i} to {j}")
else:
    print("No optimal solution found.")
```

This script first defines the warehouses, ports, container supply, container demand, and transportation distances. Then, it creates decision variables `x[i, j]` representing the number of containers transported from warehouse `i` to port `j`.

Next, the script sets the objective function, which is to minimize the total transportation cost. It also adds three types of constraints: container demand at the ports, container supply at the warehouses, and truck capacity constraint.

Finally, the script solves the model and outputs the minimum total transportation cost and the specific transportation plan (if an optimal solution is found).

Note that this script assumes you have installed the `coptpy` library and have a valid COPT license. If you are using a different solver, you may need to make appropriate modifications to the script.

---

## Case 5  [WRONG_FORMULATION]

**GT:** 5004  |  **3B:** 7000.0 (Optimal)  |  **8B:** No Best Solution

### Question
A project consists of the following 7 activities, with their durations (in days) as follows: $A(4), B(3), C(5), D(2), E(10), F(10), G(1)$. The following priorities are also given: $A \\rightarrow G, D ; E, G \\rightarrow F; D, F \\rightarrow C ; F \\rightarrow B$. The daily cost of work is 1000 euros; in addition, a special machinery must be rented from the start of activity $A$ to the end of activity $B$, with a daily cost of 5000 euros. Formulate this problem as a linear programming problem and solve it using COPTPY.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the model
prob = LpProblem("Project_Scheduling", LpMinimize)

# Activities
activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Decision variables: binary variables indicating whether an activity is started (1) or not (0)
start_activities = {act: LpVariable(f'start_{act}', 0, None, LpInteger) for act in activities}

# Objective function
prob += lpSum([1000 * start_activities[act] for act in activities])

# Constraints

# A -> G, D; E, G -> F; D, F -> C; F -> B
for i in range(len(activities)):
    prob += (start_activities[activities[i]] <= sum(start_activities[j] for j in activities if (activities.index(j) + 1) % len(activities) == activities.index(activities[i])), f'Constraint_{i}')

# Machinery constraint: A to B
prob += lpSum([start_activities[act] for act in activities]) >= 1, 'Machinery_Constraint'

# Solve the problem
status = prob.solve()

# Print the results
for v in prob.variables():
    print(f'{v.name} = {v.varValue}')

print(f'Objective: {prob.objective.value()}')
```

This code sets up a linear programming model to solve the project scheduling problem with given activities, their durations, priorities, and constraints. The objective is to minimize the total cost of starting activities while respecting the precedence relationships and machinery rental constraint.

### ORLM-8B formulation
## Mathematical Model:
To solve the project scheduling problem, we need to construct a linear programming model to minimize the total cost while satisfying the given activity priorities and duration constraints. Here is the model formulation:

### Decision Variables:
- \( t_i \): Start time of activity \( i \), where \( i \) represents the activities \( A, B, C, D, E, F, G \).

### Objective Function:
- Minimize the total cost: \[ Z = 1000(t_7 - t_1) + 5000(t_4 - t_2) \]
  - This function calculates the total cost based on the start and end times of each activity and their respective costs.

### Constraints:
1. Activity priorities and duration constraints:
   - \( t_A + 4 \leq t_G \)
   - \( t_A + 4 \leq t_D \)
   - \( t_E + 10 \leq t_F \)
   - \( t_G + 1 \leq t_F \)
   - \( t_D + 2 \leq t_C \)
   - \( t_F + 10 \leq t_C \)
   - \( t_F + 10 \leq t_B \)
2. Non-negativity constraints:
   - \( t_i \geq 0 \) for all activities \( i \).

Using this model, we can apply linear programming techniques to find the optimal start times for each activity, minimizing the total cost while satisfying all activity priorities and duration constraints. This will provide an economically efficient project scheduling strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProjectScheduling")

# Add decision variables
activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
durations = {'A': 4, 'B': 3, 'C': 5, 'D': 2, 'E': 10, 'F': 10, 'G': 1}
start_times = {act: model.addVar(name=f"t_{act}") for act in activities}

# Objective function: Minimize total cost
total_cost = 1000 * (start_times['G'] - start_times['A']) + 5000 * (start_times['D'] - start_times['B'])
model.setObjective(total_cost, sense=COPT.MINIMIZE)

# Constraints
model.addConstr(start_times['A'] + durations['A'] <= start_times['G'], name="AG")
model.addConstr(start_times['A'] + durations['A'] <= start_times['D'], name="AD")
model.addConstr(start_times['E'] + durations['E'] <= start_times['F'], name="EF")
model.addConstr(start_times['G'] + durations['G'] <= start_times['F'], name="GF")
model.addConstr(start_times['D'] + durations['D'] <= start_times['C'], name="DC")
model.addConstr(start_times['F'] + durations['F'] <= start_times['C'], name="FC")
model.addConstr(start_times['F'] + durations['F'] <= start_times['B'], name="FB")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} euros".format(model.objval))
    for act in activities:
        print(f"Start time of activity {act}: {start_times[act].x:.2f} days")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables to represent the start times of each activity and set the objective function to minimize the total cost. Next, we add constraints based on the activity priorities and duration constraints. Finally, we solve the model and output the results, including the minimum total cost and the start times of each activity.

This script provides a complete example of using the `coptpy` library to solve the project scheduling problem, while satisfying all the constraints mentioned in the problem.

---

## Case 6  [SOLVE_FAILED]

**GT:** 42.1  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
On Danzig Street, vehicles can park on both sides of the street. Mr. Edmunds, who lives at number 1, is organizing a party with about 30 attendees who will arrive in 15 cars. The length of the i-th car, denoted as $\lambda_i$, is given in meters as follows:
i 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
$\lambda_i$ 4 4.5 5 4.1 2.4 5.2 3.7 3.5 3.2 4.5 2.3 3.3 3.8 4.6 3

To avoid disturbing the neighbors, Mr. Edmunds wants to arrange the parking on both sides of the street in such a way that the total length of the street occupied by his friends' cars is minimized. Please provide a mathematical programming formulation and solve this problem using AMPL.
If the vehicles on one side of the street cannot occupy more than 15 meters exactly, how would the program change?

### 3B formulation
To address Mr. Edmunds' parking arrangement problem, we can formulate it as a Mixed-Integer Linear Programming (MILP) problem using PuLP. The goal is to minimize the total length of the street occupied by the cars while ensuring that no side exceeds 15 meters.

Here's how we can set up and solve this problem using Python with the `PuLP` library:

```python
from pulp import LpProblem, LpMinimize, LpVariable

# Initialize the LP problem
prob = LpProblem("Danzig_Street_Parking", LpMinimize)

# Define decision variables
parking_positions = {i: LpVariable(f'position_{i}', lowBound=0) for i in range(15)}

# Objective function to minimize total length occupied by cars
prob += sum([4 + 0.6 * (i > 0) if i % 2 == 0 else 3.5 + 0.6 * (i > 0) for i in parking_positions.values()]), "Total_occupied_length"

# Constraints: no side exceeds 15 meters
prob += sum([parking_positions[i] for i in range(0, 15, 2)]) <= 15, "Side_A_max"
prob += sum([parking_positions[i] for i in range(1, 15, 2)]) <= 15, "Side_B_max"

# Solve the problem
status = prob.solve()

# Print the solution status and total length occupied
print(f"Status: {LpStatus[prob.status]}")
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total length occupied =", value(prob.objective))
```

### Explanation:
- **Decision Variables**: We define a variable `parking_positions[i]` for each car position. The index `i` ranges from 0 to 14 (since there are 15 cars).
  
- **Objective Function**: The objective is to minimize the total length occupied by the cars. For even indices, we use a base length of 4 meters and add 0.6 for each car parked on that side. For odd indices, we use a base length of 3.5 meters and add 0.6 for each car parked on that side.

- **Constraints**: We ensure that no side exceeds 15 meters by summing the positions of cars on one side (even indices) and comparing it to 15, and similarly for the other side (odd indices).

### Running the Code:
When you run this code, PuLP will solve the problem and print out the solution status, variable values, and total length occupied. The `value(prob.objective)` function is used to get the value of the objective function after solving.

This formulation assumes that cars can be parked on either side of the street (even or odd indices). If we need to enforce a specific arrangement where all cars must park on one side only, additional constraints would be needed.

### ORLM-8B formulation
## Mathematical Model:
To solve Mr. Edmunds' parking problem, we need to construct a linear programming model to minimize the total length of the street occupied by the cars on both sides. Here is the model formulation:

### Decision Variables:
- $x_{ij}$: If the i-th car parks on the j-th side of the street, then $x_{ij} = 1$; otherwise, $x_{ij} = 0$. Here, $i = 1, \ldots, 15$ represents the car number, and $j = 1, 2$ represents the two sides of the street.

### Objective Function:
- Minimize the total length of the street occupied by the cars on both sides: $Z = \sum_{i=1}^{15} \sum_{j=1}^{2} \lambda_i x_{ij}$

### Constraints:
1. Each car can only park on one side of the street: $\sum_{j=1}^{2} x_{ij} = 1, \quad \forall i = 1, \ldots, 15$
2. The total length of the cars on one side of the street cannot exceed 15 meters: $\sum_{i=1}^{15} \lambda_i x_{ij} \leq 15, \quad \forall j = 1, 2$

### Non-negativity and Binary Constraints:
- $x_{ij} \in \{0, 1\}, \quad \forall i = 1, \ldots, 15; \quad \forall j = 1, 2$

If the vehicles on one side of the street cannot occupy more than 15 meters exactly, we need to modify the second constraint to:
2. The total length of the cars on one side of the street cannot exceed 15 meters: $\sum_{i=1}^{15} \lambda_i x_{ij} \leq 15, \quad \forall j = 1, 2$

This model can be solved using linear programming techniques to find the optimal parking arrangement that minimizes the total length of the street occupied by the cars on both sides.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve Mr. Edmunds' parking problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ParkingOptimization")

# Car length data
car_lengths = [4, 4.5, 5, 4.1, 2.4, 5.2, 3.7, 3.5, 3.2, 4.5, 2.3, 3.3, 3.8, 4.6, 3]

# Add decision variables
x = {}
for i in range(15):
    for j in range(2):
        x[i, j] = model.addVar(vtype=COPT.BINARY, name=f"x_{i+1}_{j+1}")

# Set the objective function
model.setObjective(cp.quicksum(car_lengths[i] * x[i, j] for i in range(15) for j in range(2)), sense=COPT.MINIMIZE)

# Add constraints
# Each car can only park on one side of the street
for i in range(15):
    model.addConstr(cp.quicksum(x[i, j] for j in range(2)) == 1, name=f"Car_{i+1}")

# The total length of the cars on one side of the street cannot exceed 15 meters
for j in range(2):
    model.addConstr(cp.quicksum(car_lengths[i] * x[i, j] for i in range(15)) <= 15, name=f"Side_{j+1}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total length of the street occupied by the cars on both sides: {:.2f} meters".format(model.objval))
    for i in range(15):
        for j in range(2):
            if x[i, j].x > 0.5:
                print(f"Car {i+1} parks on Side {j+1}")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we define the car length data and add binary decision variables `x[i, j]`, representing whether the i-th car parks on the j-th side of the street.

Next, we set the objective function to minimize the total length of the street occupied by the cars on both sides. We also add two sets of constraints: each car can only park on one side of the street, and the total length of the cars on one side of the street cannot exceed 15 meters.

Finally, we solve the model and output the optimal solution (if it exists). The output includes the minimum total length of the street occupied by the cars on both sides and the parking positions of each car.

This script provides a complete example of using the `coptpy` library to solve Mr. Edmunds' parking problem, considering all the necessary constraints and the objective function.

---

## Case 7  [SOLVE_FAILED]

**GT:** 8800  |  **3B:** 1134.0 (Not Solved)  |  **8B:** No Best Solution

### Question
A certain store has formulated a purchasing and selling plan for a certain product from July to December. It is known that the store's warehouse capacity cannot exceed 500 units. By the end of June, there are already 200 units in stock. From then on, the store will purchase once at the beginning of each month. Assuming the purchase and selling prices of the product for each month are as shown in Table 1-21, how many units should be purchased and sold each month to maximize total revenue?

Table 1-21
\begin{tabular}{c|cccccc}
\hline Month & 7 & 8 & 9 & 10 & 11 & 12 \\
\hline Purchase & 28 & 24 & 25 & 27 & 23 & 23 \\
\hline Sale & 29 & 24 & 26 & 28 & 22 & 25 \\
\hline Sale & 29 & 24 & 26 & 28 & 22 & 25 \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Product_Purchasing_Selling", LpMaximize)

# Define decision variables
purchase_vars = LpVariable.dicts('Purchase', range(1, 7), lowBound=0, cat='Continuous')
sell_vars = LpVariable.dicts('Sell', range(1, 7), lowBound=0, cat='Continuous')

# Objective function: Maximize total revenue
prob += lpSum([29*p for p in purchase_vars] + [25*s for s in sell_vars]), "Total Revenue"

# Constraints:
# Warehouse capacity constraint (excluding initial stock)
for month in range(1, 7):
    prob += purchase_vars[month-1] - sell_vars[month-1] <= 500 - 200, f"Stock Constraint at the end of Month {month}"

# Purchase and sale constraints for each month
prob += purchase_vars[0] == 200, "Initial Stock"
for month in range(1, 6):
    prob += purchase_vars[month-1] >= purchase_vars[month], "Purchase Non-Decreasing Constraint"

# Solve the problem
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for var in prob.variables():
    print(f"{var.name} = {var.varValue}")
print("Total Revenue: ", value(prob.objective))
```

This code sets up a linear programming model to determine how many units should be purchased and sold each month from July to December, with the goal of maximizing total revenue. The constraints ensure that the warehouse capacity does not exceed 500 units (excluding initial stock), and purchases are non-decreasing throughout the period.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem of the store's purchasing and selling plan, we need to construct a linear programming model to maximize total revenue while satisfying the warehouse capacity constraint. Here is the model formulation:

### Decision Variables:
- \(x_j\): The number of units purchased in the \(j\)th month, where \(j = 1, \ldots, 6\) corresponds to the months from July to December.
- \(y_j\): The number of units sold in the \(j\)th month, where \(j = 1, \ldots, 6\) corresponds to the months from July to December.

### Objective Function:
- Maximize total revenue: \[Z = \sum_{j=1}^{6} (s_j y_j - c_j x_j)\]
  - where \(s_j\) is the selling price in the \(j\)th month, and \(c_j\) is the purchase price in the \(j\)th month.

### Constraints:
1. Warehouse capacity constraint: \[200 + \sum_{j=1}^{i} x_j - \sum_{j=1}^{i} y_j \leq 500, \quad \forall i = 1, \ldots, 6\]
   - This ensures that the total quantity of products in the warehouse at any time does not exceed 500 units.
2. Non-negativity constraint: \[x_j, y_j \geq 0, \quad \forall j = 1, \ldots, 6\]
   - This ensures that the quantities purchased and sold are non-negative.

Using this model, we can apply linear programming techniques to find the optimal quantities to purchase and sell each month, maximizing total revenue while satisfying the warehouse capacity constraint. This will provide the store with an optimized purchasing and selling strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the optimization problem of the store's purchasing and selling plan:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("InventoryOptimization")

# Define parameters
months = range(1, 7)  # Months from July to December
purchase_prices = [28, 24, 25, 27, 23, 23]  # Purchase prices for each month
sale_prices = [29, 24, 26, 28, 22, 25]  # Sale prices for each month
initial_inventory = 200  # Initial inventory
max_inventory = 500  # Maximum warehouse capacity

# Add decision variables
x = [model.addVar(lb=0, vtype=COPT.CONTINUOUS, name=f"x_{j}") for j in months]  # Number of units purchased each month
y = [model.addVar(lb=0, vtype=COPT.CONTINUOUS, name=f"y_{j}") for j in months]  # Number of units sold each month

# Objective function: Maximize total revenue
model.setObjective(cp.quicksum(sale_prices[j-1] * y[j-1] - purchase_prices[j-1] * x[j-1] for j in months), sense=COPT.MAXIMIZE)

# Constraints
# Warehouse capacity constraint
for i in range(1, 7):
    model.addConstr(initial_inventory + cp.quicksum(x[j-1] for j in range(1, i+1)) - cp.quicksum(y[j-1] for j in range(1, i+1)) <= max_inventory, name=f"InventoryConstraint_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total revenue: {:.2f}".format(model.objval))
    for j in months:
        print(f"Number of units purchased in month {j+6}: {x[j-1].x:.2f}")
        print(f"Number of units sold in month {j+6}: {y[j-1].x:.2f}")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we define the parameters of the problem, including the months, purchase and sale prices, initial inventory, and maximum warehouse capacity.

Next, we add decision variables `x` and `y`, representing the number of units purchased and sold each month, respectively. The objective function is set to maximize total revenue, which is the sum of the sale revenue minus the purchase cost for each month.

The constraints include the warehouse capacity constraint, which ensures that the total quantity of products in the warehouse at any time does not exceed the maximum capacity.

Finally, we solve the model and output the maximized total revenue as well as the optimal quantities purchased and sold each month.

Please note that this script assumes you have installed the `coptpy` library and have a valid COPT license. If you do not have a COPT license, you can consider using other linear programming solvers such as `PuLP` or `scipy.optimize`.

---

## Case 8  [SOLVE_FAILED]

**GT:** 1360  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
A trading company specializes in wholesale business of a certain kind of miscellaneous grain. The company has a warehouse with a capacity of 5000 units. On January 1st, the company has a stock of 1000 units of miscellaneous grain and a capital of 20000 yuan. The estimated prices of the grain for the first quarter are shown in Table 1-8.
Table $1-8$
\begin{tabular}{c|c|c}
\hline Month & Purchase Price/(yuan/unit) & Selling Price $/$ (yuan $/$ unit) \\
\hline 1 & 2.85 & 3.10 \\
2 & 3.05 & 3.25 \\
3 & 2.90 & 2.95 \\
\hline
\end{tabular}

The purchased grain arrives in the same month but can only be sold in the following month, and it is required to be paid upon delivery. The company wants to have a stock of 2000 units at the end of the quarter. What buying and selling strategies should be adopted to maximize the total profit over the three months?

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Create a problem
prob = LpProblem("GrainTrading", LpMaximize)

# Define decision variables
buy1 = LpVariable('BuyMonth1', lowBound=0, cat='Continuous')
sell1 = LpVariable('SellMonth1', lowBound=0, cat='Continuous')
buy2 = LpVariable('BuyMonth2', lowBound=0, cat='Continuous')
sell2 = LpVariable('SellMonth2', lowBound=0, cat='Continuous')
buy3 = LpVariable('BuyMonth3', lowBound=0, cat='Continuous')
stock_end = LpVariable('StockEnd', lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
profit = (3.10 - 2.85) * buy1 + (3.25 - 3.05) * buy2 + (2.95 - 2.90) * buy3 - \
          (2.85 * sell1 + 3.05 * sell2 + 2.90 * sell3)
prob += profit, "Total Profit"

# Constraints
prob += buy1 + buy2 + buy3 <= 5000, "Warehouse Capacity"
prob += stock_end == 1000 + buy1 - sell1 + buy2 - sell2 + buy3 - sell3, "Stock Constraint"
prob += stock_end >= 2000, "End Stock Requirement"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Profit: {value(prob.objective)}")
```

Note: There is a typo in the question where `sell3` appears. Assuming there was an error and it should be `sell2`, I have adjusted the code accordingly. If `sell3` is intended, please provide further instructions or correct me.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem for the trading company, we will establish a linear programming model to maximize the total profit over the three months while considering the warehouse capacity, capital constraints, and the time difference between purchase and sale. The model can be formulated as follows:

### Decision Variables:
- \(x_i\): The quantity of grain purchased in month \(i\).
- \(y_i\): The quantity of grain sold in month \(i\).

### Objective Function:
- Maximize total profit: \[Z = 3.10y_1 + 3.25y_2 + 2.95y_3 - 2.85x_1 - 3.05x_2 - 2.90x_3\]

### Constraints:
1. Warehouse capacity constraint: \[x_1 - y_1 + x_2 - y_2 + x_3 - y_3 \leq 5000\]
2. Capital constraint: \[2.85x_1 \leq 20000\]
3. Stock constraint: \[x_1 - y_1 + x_2 - y_2 + x_3 - y_3 = 2000\]
4. Non-negativity constraint: \[x_i, y_i \geq 0, \forall i\]

### Integer Constraint:
- \(x_i, y_i\) must be integers, as the quantity of grain cannot be fractional.

Using this model, we can use linear programming techniques to find the optimal quantities of grain to purchase and sell each month, maximizing the total profit over the three months while satisfying the warehouse capacity, capital constraints, and the time difference between purchase and sale. This will provide the trading company with an optimized buying and selling strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for the trading company:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("GrainTradingOptimization")

# Define decision variables
x = [model.addVar(vtype=COPT.INTEGER, name=f"x_{i}") for i in range(1, 4)]
y = [model.addVar(vtype=COPT.INTEGER, name=f"y_{i}") for i in range(1, 4)]

# Define the objective function
model.setObjective(3.10*y[0] + 3.25*y[1] + 2.95*y[2] - 2.85*x[0] - 3.05*x[1] - 2.90*x[2], sense=COPT.MAXIMIZE)

# Add constraints
# Warehouse capacity constraint
model.addConstr(x[0] - y[0] + x[1] - y[1] + x[2] - y[2] <= 5000, name="WarehouseCapacity")

# Capital constraint
model.addConstr(2.85*x[0] <= 20000, name="CapitalConstraint")

# Stock constraint
model.addConstr(x[0] - y[0] + x[1] - y[1] + x[2] - y[2] == 2000, name="InventoryConstraint")

# Non-negativity constraint
for i in range(3):
    model.addConstr(x[i] >= 0, name=f"NonNegativity_x_{i}")
    model.addConstr(y[i] >= 0, name=f"NonNegativity_y_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: {:.2f} yuan".format(model.objval))
    for i in range(3):
        print(f"Quantity of grain purchased in month {i+1}: {x[i].x} units")
        print(f"Quantity of grain sold in month {i+1}: {y[i].x} units")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we define the decision variables `x` and `y`, representing the quantities of grain purchased and sold each month.

Next, we set the objective function, which is to maximize the total profit. The objective function includes the selling revenue and purchase cost for each month.

Then, we add constraints, including the warehouse capacity constraint, capital constraint, stock constraint, and non-negativity constraint. These constraints ensure that the model satisfies the conditions mentioned in the problem description.

Finally, we solve the model and output the results. If an optimal solution is found, we print the maximized total profit and the quantities of grain purchased and sold each month. If no optimal solution is found, we output the corresponding message.

This script provides a complete example of using the `coptpy` library to solve the optimization problem for the trading company, considering all the constraints and objectives mentioned in the problem description.

---

## Case 9  [SOLVE_FAILED]

**GT:** 770.0  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
There are 8 villages in Tuanjie Township, with their respective coordinates and the number of elementary school students shown in Table 5-14.

Table 5-14
\begin{tabular}{c|c|c|c}
\hline Village Code & \multicolumn{2}{|c|}{Coordinate Position} & \multirow{2}{*}{Number of Elementary School Students} \
\cline {2-4} 1 & $x$ & $y$ & 60 \
2 & 10 & 0 & 80 \
3 & 12 & 3 & 100 \
4 & 14 & 15 & 120 \
5 & 16 & 13 & 80 \
6 & 18 & 9 & 60 \
7 & 8 & 6 & 40 \
8 & 6 & 12 & 80 \
\hline
\end{tabular}

Considering the economies of scale for the schools, it is planned to build one elementary school in each of the two villages. Where should the two schools be built to minimize the walking distance for the elementary school students? (The walking distance for the students is calculated based on the Euclidean distance between the two villages.)

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem
prob = LpProblem("School_Placement", LpMinimize)

# Initialize variables: x[i] and y[i] for village i, where i is a code of villages
village_vars = {}
for i in range(1, 9):
    x = LpVariable(f"x_{i}", lowBound=0)
    y = LpVariable(f"y_{i}", lowBound=0)
    village_vars[i] = (x, y)

# Objective function: minimize total walking distance
objective_function = lpSum([village_vars[v][0]*village_vars[v][1] + village_vars[v][1]*village_vars[v][0] for v in village_vars])
prob += objective_function

# Constraints: each school can only be built once and must serve the students of its respective villages
for i in range(1, 9):
    prob += village_vars[i][0] + village_vars[i][1] <= 1

# Solve the problem
prob.solve()

# Print which schools should be built based on the solution
print("Schools to be built:")
for v in village_vars:
    if village_vars[v].varValue == 1:
        print(f"Village {v} with coordinates ({village_vars[v][0].varValue}, {village_vars[v][1].varValue})")
```

This code sets up a linear programming problem to minimize the total walking distance for elementary school students by placing two schools in Tuanjie Township. The solution will indicate which villages should have an elementary school built based on the optimal placement that minimizes the sum of Euclidean distances from each village's student population.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of where to build the two elementary schools in Tuanjie Township, we need to construct a mathematical model to minimize the total walking distance for the students. The model can be formulated as follows:

### Decision Variables:
- \(z_{ij}\): If the students from village \(i\) go to village \(j\) for school, then \(z_{ij} = 1\); otherwise, \(z_{ij} = 0\). Here, \(i, j\) represent the village code.

### Objective Function:
- Minimize the total walking distance: \[Z = \sum_{i=1}^{8}\sum_{j=1}^{8} d_{ij} \cdot n_i \cdot z_{ij}\]
  - Here, \(d_{ij}\) represents the Euclidean distance between village \(i\) and village \(j\), and \(n_i\) represents the number of elementary school students in village \(i\).

### Constraints:
1. Each village's students can only go to one school: \[\sum_{j=1}^{8} z_{ij} = 1, \forall i\]
2. Each village can have at most one school: \[\sum_{i=1}^{8} z_{ij} \leq 1, \forall j\]
3. Two schools must be built: \[\sum_{i=1}^{8}\sum_{j=1}^{8} z_{ij} = 2\]

### Non-negativity and Integer Constraints:
- \(z_{ij} \in \{0, 1\}\), for all \(i, j\), ensuring that the solution is discrete and follows the logic of "either select completely or not at all".

Using this model, we can apply integer programming techniques (specifically 0-1 integer programming) to find out where to build the two schools to minimize the total walking distance for the students. This will provide Tuanjie Township with an optimal school construction plan to improve the efficiency of student commuting.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the problem of where to build the two elementary schools in Tuanjie Township:

```python
import coptpy as cp
from coptpy import COPT
import math

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("SchoolLocationOptimization")

# Village coordinates and number of elementary school students
village_coords = [(1, 60), (2, 80), (3, 100), (4, 120), (5, 80), (6, 60), (7, 40), (8, 80)]
num_villages = len(village_coords)
num_schools = 2

# Calculate the Euclidean distance between villages
def euclidean_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

village_distances = [[euclidean_distance(coord1, coord2) for coord2 in village_coords] for coord1 in village_coords]

# Add decision variables
z = {(i, j): model.addVar(vtype=COPT.BINARY, name=f"z_{i}_{j}") for i in range(num_villages) for j in range(num_villages)}

# Objective function: Minimize the total walking distance
model.setObjective(cp.quicksum(village_distances[i][j] * village_coords[i][1] * z[(i, j)] for i in range(num_villages) for j in range(num_villages)), sense=COPT.MINIMIZE)

# Constraints
# Each village's students can only go to one school
for i in range(num_villages):
    model.addConstr(cp.quicksum(z[(i, j)] for j in range(num_villages)) == 1, name=f"StudentAssignment_{i}")

# Each village can have at most one school
for j in range(num_villages):
    model.addConstr(cp.quicksum(z[(i, j)] for i in range(num_villages)) <= 1, name=f"SchoolCapacity_{j}")

# Two schools must be built
model.addConstr(cp.quicksum(z[(i, j)] for i in range(num_villages) for j in range(num_villages)) == num_schools, name="TotalSchools")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total walking distance: {:.2f}".format(model.objval))
    for i in range(num_villages):
        for j in range(num_villages):
            if z[(i, j)].x > 0.5:
                print(f"Village {i+1} students go to village {j+1} for school")
else:
    print("No optimal solution found.")
```

This script first defines the village coordinates and the number of elementary school students, and then calculates the Euclidean distance between villages. Next, it creates decision variables `z` to represent whether the students from village `i` go to village `j` for school.

The objective function is to minimize the total walking distance, calculated by multiplying the Euclidean distance between villages, the number of elementary school students in each village, and the corresponding decision variables.

The constraints ensure that each village's students can only go to one school, each village can have at most one school, and two schools must be built.

Finally, the script solves the model and outputs the minimum total walking distance and the school assignment for each village's students.

---

## Case 10  [SOLVE_FAILED]

**GT:** 14  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
Now we need to determine 4 out of 5 workers to each complete one of the four tasks. Since each worker has different skill sets, the amount of time required for each worker to complete each task is also different. The time required for each worker to complete each task is shown in Table 5-2.
Table 5-2
\begin{tabular}{|c|c|c|c|c|}
\hline Task Time Required & $A$ & $B$ & $C$ & $D$ \\
\hline Worker & & & & \\
\hline I & 9 & 4 & 3 & 7 \\
\hline II & 4 & 6 & 5 & 6 \\
\hline III & 5 & 4 & 7 & 5 \\
\hline IV & 7 & 5 & 2 & 3 \\
\hline V & 10 & 6 & 7 & 4 \\
\hline
\end{tabular}

Try to find a work assignment plan that minimizes the total working hours.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Worker_Task_Assignment", LpMinimize)

# Define decision variables
workers = ['I', 'II', 'III', 'IV', 'V']
tasks = [1, 2, 3, 4]
assignment = {worker: {task: LpVariable(f'{worker}_{task}', lowBound=0) for task in tasks} for worker in workers}

# Objective function (minimize total working hours)
prob += lpSum([assignment[worker][task] * time_required[worker - 'I'][task - 1] for worker, task in assignment])

# Constraints: each task is assigned to exactly one worker
for task in tasks:
    prob += lpSum([assignment[worker][task] for worker in workers]) == 1

# Each worker can only be assigned to one task
for worker in workers:
    prob += lpSum([assignment[worker][task] for task in tasks]) == 1

# Time required for each worker to complete each task (in hours)
time_required = {
    'I': [9, 4, 3, 7],
    'II': [4, 6, 5, 6],
    'III': [5, 4, 7, 5],
    'IV': [7, 5, 2, 3],
    'V': [10, 6, 7, 4]
}

# Solve the problem
prob.solve()

# Print the solution
for task in tasks:
    print(f"Task {task}:")
    for worker in workers:
        if assignment[worker][task].varValue > 0:
            print(f"Worker {worker} assigned to Task {task}")
```

This code sets up a linear programming problem where we minimize the total working hours by assigning each of the four tasks to one of the five workers. The constraints ensure that each task is completed by exactly one worker and each worker completes only one task. The solution will provide an optimal assignment plan with minimized total working hours.

### ORLM-8B formulation
## Mathematical Model:
To solve this problem, we can construct a linear programming model to minimize the total working hours while satisfying the constraints of task completion and worker assignment. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): If worker \(i\) is assigned to task \(j\), then \(x_{ij} = 1\), otherwise \(x_{ij} = 0\). Here, \(i\) represents the workers (I, II, III, IV, V), and \(j\) represents the tasks (A, B, C, D).

### Objective Function:
- Minimize the total working hours: \[Z = \sum_{i \in \{I, II, III, IV, V\}}\sum_{j \in \{A, B, C, D\}} (time_{ij} \times x_{ij})\]
  - This function calculates the total working hours based on the time required for each worker to complete each task and the assignment of workers to tasks.

### Constraints:
1. Each task can only be completed by one worker: \[\sum_{i \in \{I, II, III, IV, V\}} x_{ij} = 1, \forall j\]
2. Each worker can only be assigned to one task: \[\sum_{j \in \{A, B, C, D\}} x_{ij} = 1, \forall i\]
3. Binary constraints: \[x_{ij} \in \{0, 1\}, \forall i, j\]

Using this model, we can apply integer linear programming techniques to find the optimal assignment of workers to tasks that minimizes the total working hours while satisfying the constraints of task completion and worker assignment. This will provide the company with an optimized work assignment strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve this problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("WorkAssignmentOptimization")

# Define workers and tasks
workers = ['I', 'II', 'III', 'IV', 'V']
tasks = ['A', 'B', 'C', 'D']

# Define task time required for each worker
time_required = {
    ('I', 'A'): 9, ('I', 'B'): 4, ('I', 'C'): 3, ('I', 'D'): 7,
    ('II', 'A'): 4, ('II', 'B'): 6, ('II', 'C'): 5, ('II', 'D'): 6,
    ('III', 'A'): 5, ('III', 'B'): 4, ('III', 'C'): 7, ('III', 'D'): 5,
    ('IV', 'A'): 7, ('IV', 'B'): 5, ('IV', 'C'): 2, ('IV', 'D'): 3,
    ('V', 'A'): 10, ('V', 'B'): 6, ('V', 'C'): 7, ('V', 'D'): 4
}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.BINARY, name=f"x_{i}_{j}") for i in workers for j in tasks}

# Objective function: Minimize total working hours
objective = cp.quicksum(time_required[i, j] * x[i, j] for i in workers for j in tasks)
model.setObjective(objective, sense=COPT.MINIMIZE)

# Constraints
# Each task can only be completed by one worker
for j in tasks:
    model.addConstr(cp.quicksum(x[i, j] for i in workers) == 1, name=f"Task_{j}")

# Each worker can only be assigned to one task
for i in workers:
    model.addConstr(cp.quicksum(x[i, j] for j in tasks) == 1, name=f"Worker_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total working hours:", model.objval)
    for i in workers:
        for j in tasks:
            if x[i, j].x == 1:
                print(f"Worker {i} assigned to Task {j}")
else:
    print("No optimal solution found.")
```

In this script, we first define the workers, tasks, and the time required for each worker to complete each task. Then, it creates a binary decision variable `x[i, j]` to represent whether worker `i` is assigned to task `j`.

The objective function is to minimize the total working hours, which is the sum of the time required for each worker to complete their assigned task.

The constraints ensure that each task is completed by only one worker and each worker is assigned to only one task.

Finally, the script solves the model and outputs the minimum total working hours and the assignment of each worker to a task (if an optimal solution is found).

---

## Case 11  [SOLVE_FAILED]

**GT:** 246  |  **3B:** 7400.0 (Infeasible)  |  **8B:** No Best Solution

### Question
A company produces two products, microwaves and water heaters, which are manufactured in two workshops, Workshop A and Workshop B. It is known that, excluding purchased components, producing one microwave requires 2 hours of processing in Workshop A and 1 hour of assembly in Workshop B. Producing one water heater requires 1 hour of processing in Workshop A and 3 hours of assembly in Workshop B. After being produced, both products need to go through inspection and sales processes. It is known that the inspection and sales cost for each microwave is $30, and for each water heater is $50. Workshop A has 120 hours of available production time per month, with a cost of $80 per hour. Workshop B has 150 hours of available production time per month, with a cost of $20 per hour. It is estimated that an average of 80 microwaves and 50 water heaters can be sold per month in the next year. Based on these facts, the company has set the following monthly planning objectives:

First priority: Inspection and sales costs should not exceed $4500 per month.
Second priority: Sell no less than 80 microwaves per month.
Third priority: Ensure full utilization of production hours in Workshop A and Workshop B (weighting factor determined by the hourly cost ratio of each workshop).
Fourth priority: Workshop A overtime should not exceed 20 hours per month.
Fifth priority: Sell no less than 50 water heaters per month.

Please determine the monthly production plan that the company should establish in order to achieve the above objectives.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Monthly_Planning", LpMinimize)

# Decision variables: number of microwaves and water heaters to produce
x1 = LpVariable('Microwaves', lowBound=0, cat='Continuous')
x2 = LpVariable('WaterHeaters', lowBound=0, cat='Continuous')

# Objective function (minimize production cost)
prob += 80*x1 + 20*x2

# Constraints
# Inspection and sales costs constraint
prob += x1*30 + x2*50 <= 4500

# Minimum number of microwaves to sell
prob += x1 >= 80

# Full utilization of production hours in Workshop A (weighting factor: 80/120)
prob += x1*2 + x2*1 - 120 >= 0

# Full utilization of production hours in Workshop B (weighting factor: 20/150)
prob += x1*2 + x2*3 - 150 >= 0

# Minimum number of water heaters to sell
prob += x2 >= 50

# Overtime constraint for Workshop A
prob += x1 <= 80 + 20

# Solve the problem
prob.solve()

# Print results
print(f"Status: {LpStatus[prob.status]}")
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total cost: ${value(prob.objective)}")
```

This code sets up a linear programming model to address the given objectives. The `PuLP` library is used to define and solve the problem, with constraints for inspection/sales costs, minimum sales targets, production hours utilization, and an overtime constraint for Workshop A. The objective function aims to minimize production cost while satisfying all constraints.

### ORLM-8B formulation
## Mathematical Model:
To solve this production planning problem, we need to construct a mathematical model that aims to achieve the company's planning objectives while considering all given constraints. The model can be formulated as follows:

### Decision Variables:
- \(x\): Number of microwaves produced per month.
- \(y\): Number of water heaters produced per month.

### Objective Function:
- Minimize total cost: \[Z = 80 \times (2x + y) + 20 \times (x + 3y)\]
  - This function calculates the total cost of producing microwaves and water heaters, including the cost of Workshop A and Workshop B.

### Constraints:
1. Inspection and sales cost constraint: \[30x + 50y \leq 4500\]
2. Microwave sales quantity constraint: \[x \geq 80\]
3. Workshop A production time constraint: \[2x + y \leq 120\]
4. Workshop B production time constraint: \[x + 3y \leq 150\]
5. Workshop A overtime constraint: \[2x + y - 120 \leq 20\]
6. Water heater sales quantity constraint: \[y \geq 50\]

### Non-negativity Constraints:
- \(x, y \geq 0\)

Using this model, we can apply linear programming techniques to find out how to plan the production of microwaves and water heaters to minimize total cost while satisfying all constraints. This will provide the company with an optimal production strategy to improve production efficiency and reduce costs.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve this production planning problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ProductionPlanning")

# Add decision variables
x = model.addVar(lb=0, vtype=COPT.CONTINUOUS, name="Microwave")
y = model.addVar(lb=0, vtype=COPT.CONTINUOUS, name="Heater")

# Set the objective function
model.setObjective(80 * (2*x + y) + 20 * (x + 3*y), sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(30*x + 50*y <= 4500, name="InspectionAndSalesCost")
model.addConstr(x >= 80, name="MicrowaveSales")
model.addConstr(2*x + y <= 120, name="WorkshopATime")
model.addConstr(x + 3*y <= 150, name="WorkshopBTime")
model.addConstr(2*x + y - 120 <= 20, name="WorkshopAOvertime")
model.addConstr(y >= 50, name="HeaterSales")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f}".format(model.objval))
    print("Monthly production plan:")
    print("Microwave: {:.2f}".format(x.x))
    print("Heater: {:.2f}".format(y.x))
else:
    print("No optimal solution found.")
```

In this script:

1. We first import the `coptpy` library and create a COPT environment and model.

2. Then, we add two decision variables `x` and `y`, representing the number of microwaves and water heaters produced per month, respectively.

3. Next, we set the objective function, which is to minimize the total cost. The objective function includes the cost of Workshop A and Workshop B.

4. Then, we add all the constraints, including the inspection and sales cost constraint, microwave sales quantity constraint, Workshop A and Workshop B production time constraints, Workshop A overtime constraint, and water heater sales quantity constraint.

5. Finally, we solve the model and output the results. If an optimal solution is found, we print the minimum total cost and the monthly production plan (number of microwaves and water heaters). If no optimal solution is found, we print the corresponding message.

This script provides a complete example of using the `coptpy` library to solve a production planning problem, considering all given constraints and objectives.

---

## Case 12  [SOLVE_FAILED]

**GT:** 165  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
A company has three factories that produce the same product, and now they need to transport the products from the three factories to four customers. The supply capacity of the factories, the demand of the customers, and the unit transportation cost from the three factories to the four customers are shown in Table 3.4 (the number in the top right corner of the table is the unit transportation cost).

Table 3.4
| Factory |  |  |  |  | Customer |  |  |  | Supply |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|  | 1 |  | 2 |  | 3 |  | 4 |  |  |
| 1 |  | 5 |  | 2 |  | 6 |  | 7 | 30 |
| 2 |  | 3 |  | 5 |  | 4 |  | 10 | 20 |
| 3 |  | 4 |  | 3 |  | 2 |  | 13 | $\Delta 0$ |
| Demand | 20 |  | 10 |  | 45 |  | 25 |  | 100 |

Now, a transportation plan needs to be made to meet the following requirements:

$p_{1}$: The order quantity of Customer 4 must be fully satisfied first.

$p_{2}$: The degree of satisfaction of the order quantity for the remaining customers should not be less than 80%.

$p_{3}$: The quantity of products transported from Factory 3 to Customer 1 should be at least 15 units.

$p_{4}$: Due to route restrictions, Factory 2 should preferably not be allocated to Customer 4.

$p_{5}$: The degree of satisfaction of the demands of Customer 1 and Customer 3 should be balanced as much as possible.

$p_{6}$: Minimize the total transportation cost.

Try to establish a goal programming model for the above problem.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Transportation_Problem", LpMinimize)

# Decision variables: x[i][j] represents the quantity shipped from factory i to customer j
x = {(i, j): LpVariable(f"x{i}{j}", lowBound=0) for i in range(1, 4) for j in range(1, 5)}

# Objective function (total transportation cost)
prob += lpSum([cost[i][j] * x[(i, j)] for i in range(1, 4) for j in range(1, 5)])

# Constraints
# Supply constraints from each factory
for i in range(1, 4):
    prob += lpSum([x[(i, j)] for j in range(1, 5)]) <= supply[i]

# Demand constraints at each customer
for j in range(1, 5):
    prob += lpSum([x[(i, j)] for i in range(1, 4)]) >= demand[j] * 0.8

# Constraint p3: Quantity of products transported from Factory 3 to Customer 1 should be at least 15 units
prob += x[(3, 1)] >= 15

# Constraint p4: Factory 2 should preferably not be allocated to Customer 4
prob += x[(2, 4)] <= 0.9 * demand[4]

# Constraint p5: The degree of satisfaction of the demands of Customer 1 and Customer 3 should be balanced as much as possible.
prob += lpSum([x[(i, j)] for i in range(1, 4) if j == 1]) - lpSum([x[(i, j)] for i in range(1, 4) if j == 3]) <= 0

# Constraint p6: The order quantity of Customer 4 must be fully satisfied first.
prob += x[(1, 4)] >= demand[4]

# Solve the problem
status = prob.solve()

# Print the solution
for i in range(1, 4):
    for j in range(1, 5):
        print(f"x[{i},{j}]: {x[i,j].varValue}")
print("Total transportation cost: ", value(prob.objective))
```

Please note that the above code assumes that `cost` and `supply` are defined as dictionaries. In this example, I will not define these dictionaries explicitly because they were not provided in your question. You would need to replace the placeholders with actual values for those dictionaries based on Table 3.4.

To run this code successfully, you should have PuLP installed and properly configured in your Python environment. If it's not already installed, you can install it using `pip install pulp`.

### ORLM-8B formulation
## Mathematical Model:
To solve the company's product transportation problem, we need to construct a goal programming model to minimize the total transportation cost while satisfying the supply capacity of the factories, the demand of the customers, and other specific transportation requirements. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The quantity of products transported from Factory \(i\) to Customer \(j\), where \(i = 1, 2, 3\) represents the factory number, and \(j = 1, 2, 3, 4\) represents the customer number.

### Objective Function:
- Minimize the total transportation cost: \[Z = p_6 \left( 5x_{11} + 2x_{12} + 6x_{13} + 7x_{14} + 3x_{21} + 5x_{22} + 4x_{23} + 10x_{24} + 4x_{31} + 3x_{32} + 2x_{33} + 13x_{34} \right)\]

### Constraints:
1. Factory supply capacity constraints:
   - \(x_{11} + x_{12} + x_{13} + x_{14} \leq 30\)
   - \(x_{21} + x_{22} + x_{23} + x_{24} \leq 20\)
   - \(x_{31} + x_{32} + x_{33} + x_{34} \leq 0\) (Note: Factory 3 has no supply capacity)
2. Customer demand satisfaction constraints:
   - \(x_{11} + x_{21} + x_{31} \geq 0.8 \times 20\) (Customer 1)
   - \(x_{12} + x_{22} + x_{32} \geq 0.8 \times 10\) (Customer 2)
   - \(x_{13} + x_{23} + x_{33} \geq 0.8 \times 45\) (Customer 3)
   - \(x_{14} + x_{24} + x_{34} = 25\) (Customer 4)
3. Specific transportation requirements constraints:
   - \(x_{31} \geq 15\) (Factory 3 to Customer 1)
   - \(x_{24} = 0\) (Factory 2 to Customer 4)
4. Non-negativity constraints:
   - \(x_{ij} \geq 0\), for all \(i, j\).

### Integer Constraints:
- \(x_{ij}\) must be integers, as the quantity of products cannot be fractional.

Using this model, we can apply goal programming techniques to find the optimal transportation plan that minimizes the total transportation cost while satisfying the supply capacity of the factories, the demand of the customers, and other specific transportation requirements. This will provide the company with an economically efficient product transportation strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("TransportationProblem")

# Define the factories and customers
factories = [1, 2, 3]
customers = [1, 2, 3, 4]

# Define the unit transportation costs
unit_costs = {
    (1, 1): 5, (1, 2): 2, (1, 3): 6, (1, 4): 7,
    (2, 1): 3, (2, 2): 5, (2, 3): 4, (2, 4): 10,
    (3, 1): 4, (3, 2): 3, (3, 3): 2, (3, 4): 13
}

# Define the supply capacity of the factories
supply = {1: 30, 2: 20, 3: 0}

# Define the demand of the customers
demand = {1: 20, 2: 10, 3: 45, 4: 25}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for i in factories for j in customers}

# Objective function: Minimize the total transportation cost
model.setObjective(cp.quicksum(unit_costs[i, j] * x[i, j] for i in factories for j in customers), sense=COPT.MINIMIZE)

# Constraints
# Factory supply capacity constraints
for i in factories:
    model.addConstr(cp.quicksum(x[i, j] for j in customers) <= supply[i], name=f"Supply_{i}")

# Customer demand satisfaction constraints
for j in customers:
    if j != 4:  # Customer 4's demand must be fully satisfied
        model.addConstr(cp.quicksum(x[i, j] for i in factories) >= 0.8 * demand[j], name=f"Demand_{j}")
    else:
        model.addConstr(cp.quicksum(x[i, j] for i in factories) == demand[j], name=f"Demand_{j}")

# Specific transportation requirements constraints
model.addConstr(x[3, 1] >= 15, name="SpecificDemand_31")
model.addConstr(x[2, 4] == 0, name="SpecificDemand_24")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total transportation cost: {:.2f}".format(model.objval))
    for i in factories:
        for j in customers:
            if x[i, j].x > 0:
                print(f"Quantity of products transported from Factory {i} to Customer {j}: {x[i, j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the factories, customers, unit transportation costs, supply capacity of the factories, and demand of the customers. Next, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total transportation cost and the quantity of products transported from each factory to each customer (if greater than 0).

This script provides a complete example of using the `coptpy` library to solve the company's product transportation problem while satisfying all the constraints mentioned in the problem.

---

## Case 13  [SOLVE_FAILED]

**GT:** 16  |  **3B:** None (Not Solved)  |  **8B:** No Best Solution

### Question
The planning of the operation and use of arrival and departure lines at large passenger railway stations in our country is mainly carried out by dispatchers, and the adjustment of the operation plan is not flexible. In the case of a fixed scale of arrival and departure lines at the station, optimizing and improving the technical operations of trains can help improve the throughput capacity of railway stations. In order to adapt to the characteristics of railway operation and improve the efficiency of station technical operations, the feasibility and real-time performance of adjusting and optimizing station operation plans need to be continuously improved. The allocation and use of approach tracks and arrival and departure lines in the throat area of the station are key links in the preparation and adjustment of operation plans, which need to be continuously studied to meet the needs of on-site operations. The arrival and departure line of a railway refers to the route where trains stop at the station, pick up and drop off passengers, and perform dispatch operations. The arrival and departure line is usually a line or multiple lines parallel or connected to the main line, used for train entry and exit, as well as train stopping and dispatching. The allocation and preparation of arrival and departure lines for railway trains refers to the reasonable arrangement of the operation plan and stopping tracks of railway trains on different arrival and departure lines based on the needs of train operation and the conditions of arrival and departure lines.

### Question Description

There are multiple optimization objectives for the allocation of railway train arrival and departure lines, such as:
- Minimizing the dwell time of trains, reducing the waiting time for trains to park, and improving the efficiency of train operation;
- Maximizing the speed of trains, reducing the travel time of trains, and improving the efficiency of train operation;
- Maximizing the throughput capacity of the station, allowing the station to accommodate and dispatch more trains at the same time, and meet the travel needs of more passengers;
- Minimizing the delay rate of trains, reducing train delays, and improving the punctuality and reliability of trains;
- Maximizing passenger satisfaction and providing a convenient travel experience for passengers;
- Other optimization objectives.

Please model the medium-term arrangement of approach tracks in the train station based on the job shop model. Use the COPT (Cardinal Optimizer) solver to solve this problem. Output the train timetable for each train, as well as the arrival and departure timetable for each station.

### Data Introduction

We assume that a total of 16 trains are operated, and model the approach tracks and track selection in Station A. A track refers to a lane in the station where trains can stop. Each station has a certain number of tracks depending on its size, used to park different trains. The station boundary refers to the boundary of the station area, which is the dividing point between entering and leaving the station. An approach track refers to the path a train takes when entering the station and reaching a track. Generally, there are multiple approach tracks connecting different tracks in the station. Trains choose different approach tracks before entering the station, and then stop on the corresponding tracks.

### Train Data
We consider 16 trains on the line, each with different speeds and stopping information. Each column in the table represents: train number, train speed, train stop status. "1" indicates that the train stops at the station, "0" indicates that the train does not stop at the station.
| trainNO | speed | A | B | C | D | E | F | G |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| G1 | 350 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| G3 | 350 | 1 | 1 | 1 | 0 | 1 | 0 | 1 |
| G5 | 350 | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| G7 | 350 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| G9 | 350 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| G11 | 350 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| G13 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G15 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G17 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G19 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G21 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G23 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G25 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G27 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G29 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| G31 | 300 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

### Station Data

There are 5 tracks in Station A, among which tracks I, II, and III take 4 minutes to reach the station boundary, and tracks IV and V take 5 minutes to reach the station boundary. The time to the station boundary refers to the time it takes for a train to start from a track and pass through the station boundary, including the entire process.

|track|time to boundary (min)|
|:---:|:---:|
|I|4|
|II|4|
|III|4|
|IV|5|
|V|5|

The optional approach tracks and conflict relationships within Station A are as follows. Approach track conflict refers to the occurrence of collisions or operational impacts if two trains choose the same or intersecting approach tracks. To avoid conflicts, at any time, each approach track or any pair of intersecting approach tracks should only allow one train to use them.
|path|from|conflict|
|:---:|:---:|:---|
|1|I|2, 3, 4, 5, 6, 7|
|2|I|1, 3, 4, 5, 6, 7|
|3|II|1, 2, 4, 5, 6, 7|
|4|III|1, 2, 3, 5, 6, 7|
|5|IV|1, 2, 3, 4, 6, 7|
|6|IV|1, 2, 3, 4, 5, 7|
|7|V|1, 2, 3, 4, 5, 6|

Here we assume that the approach tracks conflict with each other pairwise, and at a more detailed level of approach track arrangement, approach tracks to the same boundary may not conflict.

### Other Data
- Since Station A is the starting station, the minimum dwell time is 20 minutes.
- The safe interval between any two trains is 3 minutes.

### 3B formulation
```python
from pulp import *

# Define the problem
prob = LpProblem("Train_Scheduling", LpMinimize)

# Decision variables: binary variable to indicate if a train uses an approach track
track_vars = {}
for i in range(1, 8):
    for j in [1, 2, 3, 4, 5]:
        track_vars[i, j] = LpVariable(f'track_{i}_{j}', cat='Binary')

# Objective function: minimize the total dwell time
objective_function = lpSum([trainNO[trainNO.index(i)] * (track_vars[1, i] + track_vars[2, i] + track_vars[3, i]) for i in range(1, 6)])
prob += objective_function

# Constraints:
# Each train can only use one approach track
for i in range(1, 8):
    prob += lpSum([track_vars[i, j] for j in [1, 2, 3, 4, 5]]) == 1

# No conflict between any two trains on the same or intersecting tracks
for path in [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]:
    for i in range(1, 8):
        prob += lpSum([track_vars[i, j] for j in path]) <= 1

# Safe interval constraint: at least 3 minutes between any two trains
for i in range(1, 6):
    for j in [1, 2, 3, 4, 5]:
        prob += track_vars[1, j] + track_vars[2, j] + track_vars[3, j] <= 1

# Minimum dwell time constraint: at least 20 minutes
prob += lpSum([trainNO[trainNO.index(i)] * (track_vars[1, i] + track_vars[2, i] + track_vars[3, i]) for i in range(1, 6)]) >= 20

# Solve the problem
status = prob.solve(PULP_CBC_CMD(msg=False))

# Output the train timetable and arrival/departure timetables for each station
print("Train Timetable:")
for i in range(1, 8):
    print(f"Approach Track {i}:")
    for j in [1, 2, 3, 4, 5]:
        if value(track_vars[i, j]) == 1:
            trainNO_index = next(trainNO.index(i) for i in trainNO if value(track_vars[i, j]) == 1)
            print(f"Train {trainNO[trainNO_index]} uses Approach Track {j}")

print("\nStation A Arrival and Departure Timetables:")
for i in range(1, 6):
    print(f"Track {i} Boundary: {value(prob.objective) * (4 if i == 1 else 5)} minutes")
```

This code sets up a linear programming problem to minimize the total dwell time of trains at Station A. It includes constraints for avoiding conflicts between approach tracks and ensuring that each train uses exactly one track, while also considering safe intervals and minimum dwell times. The solution provides the optimal allocation of trains to tracks and their corresponding arrival/departure timetables.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{ijk} \): Binary variable indicating whether train \( i \) chooses approach track \( j \) and stops at track \( k \).
- \( t_{i}^{arr} \): Continuous variable representing the arrival time of train \( i \) at the station.
- \( t_{i}^{dep} \): Continuous variable representing the departure time of train \( i \) from the station.
- \( \Delta t_{ij} \): Continuous variable representing the time interval between train \( i \) and train \( j \).

### Constraints:
1. **Single Approach Track Selection Constraint**:
   \[
   \sum_{j \in J} \sum_{k \in K} x_{ijk} = 1, \quad \forall i \in I
   \]
   Each train can only choose one approach track and one track.

2. **Time Interval Constraint**:
   \[
   t_{i}^{dep} \geq t_{i}^{arr} + \text{min\_stay}_i, \quad \forall i \in I
   \]
   The departure time of each train must be at least the minimum dwell time after arrival.

3. **Safe Interval Constraint**:
   \[
   t_{i}^{dep} + \Delta t_{ij} \leq t_{j}^{arr}, \quad \forall i, j \in I, i \neq j
   \]
   The departure time of one train must be later than the arrival time of the next train, ensuring a safe interval.

4. **Approach Track Conflict Constraint**:
   \[
   x_{ijk} + x_{j'k'} \leq 1, \quad \forall (j, j') \in \text{conflicts}, \forall k \in K
   \]
   If two approach tracks conflict, they cannot be chosen simultaneously.

### Optimization Objective:
Minimize the total dwell time of trains:
\[
\min \sum_{i \in I} (t_{i}^{dep} - t_{i}^{arr})
\]

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("TrainScheduling")

# Data definition
trains = range(16)
paths = range(7)
tracks = range(5)
conflicts = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
min_stay = 20
safe_interval = 3

# Decision variables
x = model.addVars(trains, paths, tracks, vtype=COPT.BINARY, nameprefix = "x")
t_arr = model.addVars(trains, vtype=COPT.CONTINUOUS, nameprefix = "t_arr")
t_dep = model.addVars(trains, vtype=COPT.CONTINUOUS, nameprefix = "t_dep")
delta_t = model.addVars(trains, trains, vtype=COPT.CONTINUOUS, nameprefix = "delta_t")

# Constraints
# Single approach track selection constraint
model.addConstrs((x.sum(i, '*', '*') == 1 for i in trains), "PathSelection")

# Time interval constraint
model.addConstrs((t_dep[i] >= t_arr[i] + min_stay for i in trains), "MinStay")

# Safe interval constraint
model.addConstrs((t_dep[i] + safe_interval <= t_arr[j] for i in trains for j in trains if i != j), "SafetyInterval")

# Approach track conflict constraint
for i, j in conflicts:
    for k in tracks:
        model.addConstr(x.sum('*', i, k) + x.sum('*', j, k) <= 1, f"Conflict_{i}_{j}_{k}")

# Optimization objective
model.setObjective(t_dep.sum() - t_arr.sum(), COPT.MINIMIZE)

# Solve the model
model.solve()

# Output the results
if model.Status == COPT.OPTIMAL:
    print("Optimal solution found!")
    for i in trains:
        print(f"Train {i}: Arrival at {t_arr[i].x}, Departure at {t_dep[i].x}")
else:
    print("No optimal solution found.")
```
This script defines the decision variables, constraints, and optimization objective, and uses the COPT solver to find the optimal train scheduling plan.

---

## Case 14  [SOLVE_FAILED]

**GT:** 146.0  |  **3B:** 184.0 (Infeasible)  |  **8B:** None

### Question
Mary is planning tonight's dinner and wants to choose either chicken, salmon, or tofu as a source of protein in addition to the vegetables she had previously considered. Chicken contains 23 grams of protein per 100 grams, salmon contains 20 grams of protein per 100 grams, and tofu contains 8 grams of protein per 100 grams. Chicken is priced at $3 per 100 grams, salmon is priced at $5 per 100 grams, and tofu is priced at $1.5 per 100 grams. Considering Mary's budget of $20, how should she choose the ingredients to maximize her protein intake? Additionally, the total weight of the food should not exceed 800 grams, and she needs to choose at least three types of vegetables and one source of protein.

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Protein_Selection", LpMaximize)

# Decision variables: binary variables indicating whether each food is chosen (1) or not (0)
chicken = LpVariable('Chicken', 0, None, LpInteger)
salmon = LpVariable('Salmon', 0, None, LpInteger)
tofu = LpVariable('Tofu', 0, None, LpInteger)

# Objective function: maximize protein intake
prob += chicken*23 + salmon*20 + tofu*8

# Constraints:
# Budget constraint: total cost of food should not exceed $20
prob += chicken*0.1 + salmon*0.5 + tofu*0.15 <= 20, "Budget Constraint"

# Protein intake constraint: total protein intake should be maximized
prob += chicken + salmon + tofu >= 30, "Protein Intake Constraint"

# Weight constraint: total weight of food should not exceed 800 grams
prob += (chicken*100 + salmon*100 + tofu*100) <= 800, "Weight Constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Protein Intake: {value(prob.objective)} grams")
```

This code sets up a linear programming model to maximize protein intake while adhering to budget and weight constraints. The decision variables are binary, indicating whether each food is chosen (1) or not (0). The objective function aims to maximize the total protein intake from chicken, salmon, and tofu. Constraints ensure that the total cost does not exceed $20, at least three types of vegetables are selected, and the total weight does not exceed 800 grams.

### ORLM-8B formulation
## Mathematical Model:
To help Mary maximize her protein intake within the budget, we can construct a linear programming model to determine the optimal combination of ingredients. Here is the detailed formulation of the model:

### Decision Variables:
- \(x_1\): Weight of chicken (in 100 grams)
- \(x_2\): Weight of salmon (in 100 grams)
- \(x_3\): Weight of tofu (in 100 grams)
- \(y_i\): Binary variable indicating whether vegetable \(i\) is chosen (1 if chosen, 0 otherwise)

### Objective Function:
- Maximize protein intake: \[Z = 23x_1 + 20x_2 + 8x_3\]

### Constraints:
1. Budget constraint: \[3x_1 + 5x_2 + 1.5x_3 \leq 20\]
2. Total weight constraint: \[x_1 + x_2 + x_3 \leq 8\]
3. At least three types of vegetables chosen: \[\sum_{i} y_i \geq 3\]
4. At least one source of protein chosen: \[x_1 + x_2 + x_3 \geq 1\]
5. Non-negativity constraints: \[x_1, x_2, x_3 \geq 0\]
6. Binary constraints: \[y_i \in \{0, 1\}\]

Using this model, we can apply linear programming techniques to find the optimal combination of ingredients that maximizes protein intake while satisfying the budget, total weight, and ingredient selection constraints. This will provide Mary with an optimal dinner plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("DinnerPlanning")

# Add decision variables
x1 = model.addVar(lb=0, name="x1")  # Weight of chicken (in 100 grams)
x2 = model.addVar(lb=0, name="x2")  # Weight of salmon (in 100 grams)
x3 = model.addVar(lb=0, name="x3")  # Weight of tofu (in 100 grams)
y = model.addVars(3, vtype=COPT.BINARY, name="y")  # Whether vegetable i is chosen

# Set the objective function: Maximize protein intake
model.setObjective(23*x1 + 20*x2 + 8*x3, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(3*x1 + 5*x2 + 1.5*x3 <= 20, name="BudgetConstraint")
model.addConstr(x1 + x2 + x3 <= 8, name="TotalWeightConstraint")
model.addConstr(cp.quicksum(y[i] for i in range(3)) >= 3, name="VegetableConstraint")
model.addConstr(x1 + x2 + x3 >= 1, name="ProteinConstraint")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized protein intake: {:.2f} grams".format(model.objval))
    print("Weight of chicken: {:.2f} grams".format(x1.x))
    print("Weight of salmon: {:.2f} grams".format(x2.x))
    print("Weight of tofu: {:.2f} grams".format(x3.x))
    print("Chosen vegetables:")
    for i in range(3):
        if y[i].x > 0.5:
            print(f"Vegetable {i+1}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables, including the weights of chicken, salmon, and tofu, as well as binary variables indicating whether each vegetable is chosen. We set the objective function to maximize protein intake and add constraints for the budget, total weight, vegetable selection, and protein source selection.

Finally, we solve the model and output the results of the optimal solution, including the maximized protein intake and the weights of each ingredient. This script provides Mary with an optimal dinner plan that maximizes protein intake within the budget.

---

## Case 15  [WRONG_FORMULATION]

**GT:** 1000.0  |  **3B:** 1185.0 (Optimal)  |  **8B:** None

### Question
A manufacturing company needs to transport 1800 units of products from the warehouse to three different sales points. The company has four transportation options to choose from: trucks, vans, motorcycles, and electric vehicles. Due to the high energy consumption of vans and electric vehicles, the company wants to choose only one of these two transportation options. Trucks generate 100 units of pollution per trip, vans generate 50 units of pollution, motorcycles generate 10 units of pollution, and electric vehicles generate 0 units of pollution. The total pollution generated by all trips must not exceed 2000 units. Trucks must be used at least 10 times. Trucks, vans, motorcycles, and electric vehicles can carry 100 units, 80 units, 40 units, and 60 units of products per trip, respectively. The company needs to ensure that the total quantity of products transported is at least 1800 units.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpInteger

# Create problem
prob = LpProblem("Product_Transportation", LpMinimize)

# Decision variables
truck_trips = LpVariable('Truck_Trips', lowBound=10, cat='Continuous')
van_trips = LpVariable('Van_Trips', cat='Binary')
motorcycle_trips = LpVariable('Motorcycle_Trips', lowBound=0, upBound=22.5, cat='Continuous')  # 1800/40
electric_vehicle_trips = LpVariable('Electric_Vehicle_Trips', lowBound=0, upBound=30, cat='Binary')

# Objective function: minimize pollution
prob += lpSum([truck_trips * 100 + van_trips * 50 + motorcycle_trips * 10 + electric_vehicle_trips * 0]), "Total_Pollution"

# Constraints
# Total quantity of products transported must be at least 1800 units
prob += lpSum([truck_trips * 100, van_trips * 80, motorcycle_trips * 40, electric_vehicle_trips * 60]) >= 1800

# Trucks must be used at least 10 times
prob += truck_trips >= 10

# Total pollution generated by all trips must not exceed 2000 units
prob += lpSum([truck_trips * 100, van_trips * 50, motorcycle_trips * 10, electric_vehicle_trips * 0]) <= 2000

# Solve the problem
status = prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Pollution Generated =", value(prob.objective))
```

Please note that the variable `motorcycle_trips` is defined as a continuous variable with an upper bound of 22.5 (since 1800/40 = 45), and it's also constrained to be binary (`van_trips`) since only one type of vehicle can be used at most. The total pollution constraint ensures that the sum of all trips' pollution does not exceed 2000 units, which is a logical error as electric vehicles do not generate any pollution. This should be corrected by removing the `electric_vehicle_trips` variable and its associated constraints if we want to ensure only trucks, vans, or motorcycles are used.

### ORLM-8B formulation
## Mathematical Model:
To solve the transportation problem for the manufacturing company, we need to construct a linear programming model to minimize the total pollution while satisfying the transportation requirements and constraints. Here is the model formulation:

### Decision Variables:
- \(x_1\): Number of truck trips
- \(x_2\): Number of van trips
- \(x_3\): Number of motorcycle trips
- \(x_4\): Number of electric vehicle trips
- \(y_2\): Whether to choose van (1 = yes, 0 = no)
- \(y_4\): Whether to choose electric vehicle (1 = yes, 0 = no)

### Objective Function:
- Minimize total pollution: \[Z = 100x_1 + 50y_2x_2 + 10x_3 + 0y_4x_4\]

### Constraints:
1. Total pollution does not exceed 2000 units: \[100x_1 + 50y_2x_2 + 10x_3 + 0y_4x_4 \leq 2000\]
2. Trucks must be used at least 10 times: \[x_1 \geq 10\]
3. Total quantity of products transported is at least 1800 units: \[100x_1 + 80y_2x_2 + 40x_3 + 60y_4x_4 \geq 1800\]
4. Only one of vans or electric vehicles can be chosen: \[y_2 + y_4 \leq 1\]

### Non-negativity Constraints:
- \(x_1, x_2, x_3, x_4 \geq 0\)
- \(y_2, y_4 \in \{0, 1\}\)

Using this model, we can apply linear programming techniques to find the optimal number of trips for each transportation option, minimizing the total pollution while satisfying the transportation requirements and constraints. This will provide the manufacturing company with an economically efficient transportation strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("TransportationOptimization")

# Add decision variables
x1 = model.addVar(vtype=COPT.INTEGER, name="x1")  # Number of truck trips
x2 = model.addVar(vtype=COPT.INTEGER, name="x2")  # Number of van trips
x3 = model.addVar(vtype=COPT.INTEGER, name="x3")  # Number of motorcycle trips
x4 = model.addVar(vtype=COPT.INTEGER, name="x4")  # Number of electric vehicle trips
y2 = model.addVar(vtype=COPT.BINARY, name="y2")   # Whether to choose van
y4 = model.addVar(vtype=COPT.BINARY, name="y4")   # Whether to choose electric vehicle

# Objective function: Minimize total pollution
model.setObjective(100 * x1 + 50 * y2 * x2 + 10 * x3 + 0 * y4 * x4, sense=COPT.MINIMIZE)

# Constraints
model.addConstr(100 * x1 + 50 * y2 * x2 + 10 * x3 + 0 * y4 * x4 <= 2000, name="PollutionLimit")
model.addConstr(x1 >= 10, name="MinTruckTrips")
model.addConstr(100 * x1 + 80 * y2 * x2 + 40 * x3 + 60 * y4 * x4 >= 1800, name="TotalTransport")
model.addConstr(y2 + y4 <= 1, name="VehicleChoice")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total pollution: {:.2f} units".format(model.objval))
    print("Number of truck trips: {:.2f}".format(x1.x))
    print("Number of van trips: {:.2f}".format(x2.x))
    print("Number of motorcycle trips: {:.2f}".format(x3.x))
    print("Number of electric vehicle trips: {:.2f}".format(x4.x))
    print("Whether to choose van: {}".format(int(y2.x)))
    print("Whether to choose electric vehicle: {}".format(int(y4.x)))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total pollution and the number of trips for each transportation option.

This script provides a complete example of using the `coptpy` library to solve the transportation problem for the manufacturing company, while satisfying all the constraints mentioned in the problem.

---

## Case 16  [SOLVE_FAILED]

**GT:** 1581550  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A company plans to produce three products, $A_{1}, A_{2}, A_{3}$, within a four-month timeframe (January to April). The demand for the products is shown in the table below:

| Demand | January | February | March | April |
| :---: | :---: | :---: | :---: | :---: |
| $A_{1}$ | 5300 | 1200 | 7400 | 5300 |
| $A_{2}$ | 4500 | 5400 | 6500 | 7200 |
| $A_{3}$ | 4400 | 6700 | 12500 | 13200 |

The prices, production costs, production quotas, activation costs, and minimum batch sizes (refer to the definitions in Exercise 4.3) are as follows:

| Product | $A_{1}$ | $A_{2}$ | $A_{3}$ |
| :---: | :---: | :---: | :---: |
| Unit Price | $\\$ 124$ | $\\$ 109$ | $\\$ 115$ |
| Activation Cost | $\\$ 150000$ | $\\$ 150000$ | $\\$ 100000$ |
| Production Cost | $\\$ 73.30$ | $\\$ 52.90$ | $\\$ 65.40$ |
| Production Quota | 500 | 450 | 550 |
| Minimum Batch Size | 20 | 20 | 16 |

January has 23 production days, February has 20, March has 23, and April has 22. The activation status of the production lines can be changed each month. The minimum batch size is calculated on a monthly basis.

In addition, storage space can be rented monthly at a cost of $\\$ 3.50$ for $A_{1}$, $\\$ 4.00$ for $A_{2}$, and $\\$ 3.00$ for $A_{3}$. Each product takes up the same amount of storage space. The total available capacity is 800 units.

Write a mathematical program to maximize revenue.

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Product_Planning_Problem", LpMaximize)

# Define decision variables
A1 = [LpVariable(f'A1_{i}', lowBound=0) for i in range(4)]
A2 = [LpVariable(f'A2_{i}', lowBound=0) for i in range(4)]
A3 = [LpVariable(f'A3_{i}', lowBound=0) for i in range(4)]

# Objective function: Maximize total revenue
prob += sum([124 * A1[i] + 109 * A2[i] + 115 * A3[i] for i in range(4)])

# Constraints

# Demand constraints
demand_constraints = [
    LpConstraint(A1[0] + A1[1] + A1[2] + A1[3], sense=LpEqual, rhs=5300),
    LpConstraint(A2[0] + A2[1] + A2[2] + A2[3], sense=LpEqual, rhs=4500),
    LpConstraint(A3[0] + A3[1] + A3[2] + A3[3], sense=LpEqual, rhs=4400)
]

# Production quota constraints
quota_constraints = [
    LpConstraint(A1[i], sense=LpLessThan, rhs=500) for i in range(4)
] + [
    LpConstraint(A2[i], sense=LpLessThan, rhs=450) for i in range(4)
] + [
    LpConstraint(A3[i], sense=LpLessThan, rhs=550) for i in range(4)
]

# Activation cost constraints
activation_cost_constraints = [
    LpConstraint(A1[0], sense=LpLessThan, rhs=150000),
    LpConstraint(A2[0], sense=LpLessThan, rhs=150000),
    LpConstraint(A3[0], sense=LpLessThan, rhs=100000)
]

# Minimum batch size constraints
min_batch_size_constraints = [
    LpConstraint(A1[i], sense=LpGreaterEqual, rhs=20) for i in range(4)
] + [
    LpConstraint(A2[i], sense=LpGreaterEqual, rhs=20) for i in range(4)
] + [
    LpConstraint(A3[i], sense=LpGreaterEqual, rhs=16) for i in range(4)
]

# Storage space constraints
storage_space_constraints = [
    LpConstraint(A1[i], sense=LpLessThan, rhs=800) for i in range(4)
] + [
    LpConstraint(A2[i], sense=LpLessThan, rhs=800) for i in range(4)
] + [
    LpConstraint(A3[i], sense=LpLessThan, rhs=800) for i in range(4)
]

# Add constraints to the problem
prob += demand_constraints[0]
prob += demand_constraints[1]
prob += demand_constraints[2]
prob += quota_constraints[0]
prob += quota_constraints[1]
prob += quota_constraints[2]
prob += quota_constraints[3]
prob += activation_cost_constraints[0]
prob += activation_cost_constraints[1]
prob += activation_cost_constraints[2]
prob += min_batch_size_constraints[0]
prob += min_batch_size_constraints[1]
prob += min_batch_size_constraints[2]
prob += min_batch_size_constraints[3]
prob += storage_space_constraints[0]
prob += storage_space_constraints[1]
prob += storage_space_constraints[2]
prob += storage_space_constraints[3]

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print("Total Revenue: ", value(prob.objective))
```

This code sets up a PuLP model to maximize revenue for producing products A1, A2, and A3 over four months. It includes constraints for demand, production quotas, activation costs, minimum batch sizes, and storage space. The solution will provide the optimal production quantities for each product in each month that maximizes total revenue while adhering to all given constraints.

### ORLM-8B formulation
## Mathematical Model:
To solve the company's production planning problem, we need to construct a linear programming model to maximize revenue while satisfying the demand, production capacity, and storage space constraints. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The quantity of product \(i\) produced in month \(j\).
- \(y_{ij}\): The quantity of product \(i\) stored in month \(j\).
- \(z_{ij}\): The activation status of product \(i\) in month \(j\), where \(z_{ij} = 1\) if activated, and \(z_{ij} = 0\) otherwise.

### Objective Function:
- Maximize revenue: \[Z = \sum_{i=1}^{3} \sum_{j=1}^{4} (P_{i} - C_{i} - S_{i} - A_{i} \cdot z_{ij}) \cdot x_{ij} - \sum_{i=1}^{3} \sum_{j=1}^{4} M_{i} \cdot y_{ij}\]
  - where \(P_{i}\) is the unit price of product \(i\), \(C_{i}\) is the production cost, \(S_{i}\) is the storage cost, \(A_{i}\) is the activation cost, and \(M_{i}\) is the monthly storage cost.

### Constraints:
1. Demand satisfaction: \[x_{ij} + y_{i,j-1} \geq D_{ij}, \quad \forall i, \forall j\]
   - where \(D_{ij}\) is the demand for product \(i\) in month \(j\), and \(y_{i0}\) is the initial inventory, which can be set to 0 if there is no initial inventory.
2. Production capacity: \[\sum_{i=1}^{3} \frac{x_{ij}}{Q_{i}} \leq T_{j}, \quad \forall j\]
   - where \(Q_{i}\) is the production quota for product \(i\), and \(T_{j}\) is the total available production time in month \(j\).
3. Storage space: \[\sum_{i=1}^{3} y_{ij} \leq 800, \quad \forall j\]
4. Minimum batch size: \[x_{ij} \geq L_{i} \cdot z_{ij}, \quad \forall i, \forall j\]
   - where \(L_{i}\) is the minimum batch size for product \(i\).
5. Activation status: \[z_{ij} \in \{0, 1\}, \quad \forall i, \forall j\]

### Non-negativity Constraints:
- \(x_{ij}, y_{ij} \geq 0, \quad \forall i, \forall j\)

Using this model, we can apply linear programming techniques to find the optimal production and storage quantities for each product in each month, while satisfying all production and storage constraints, in order to maximize revenue. This will provide the company with an optimized production and storage strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionPlanning")

# Define parameters
products = ['A1', 'A2', 'A3']
months = ['Jan', 'Feb', 'Mar', 'Apr']
demand = {
    'A1': [5300, 1200, 7400, 5300],
    'A2': [4500, 5400, 6500, 7200],
    'A3': [4400, 6700, 12500, 13200]
}
price = {'A1': 124, 'A2': 109, 'A3': 115}
activation_cost = {'A1': 150000, 'A2': 150000, 'A3': 100000}
production_cost = {'A1': 73.30, 'A2': 52.90, 'A3': 65.40}
quota = {'A1': 500, 'A2': 450, 'A3': 550}
min_batch = {'A1': 20, 'A2': 20, 'A3': 16}
storage_cost = {'A1': 3.50, 'A2': 4.00, 'A3': 3.00}
production_days = [23, 20, 23, 22]
storage_capacity = 800

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.CONTINUOUS, name=f"x_{i}_{j}") for i in products for j in months}
y = {(i, j): model.addVar(vtype=COPT.CONTINUOUS, name=f"y_{i}_{j}") for i in products for j in months}
z = {(i, j): model.addVar(vtype=COPT.BINARY, name=f"z_{i}_{j}") for i in products for j in months}

# Objective function: Maximize revenue
model.setObjective(
    cp.quicksum((price[i] - production_cost[i] - storage_cost[i] - activation_cost[i] * z[i, j]) * x[i, j] for i in products for j in months) -
    cp.quicksum(storage_cost[i] * y[i, j] for i in products for j in months),
    sense=COPT.MAXIMIZE
)

# Constraints
# Demand satisfaction
for i in products:
    model.addConstr(cp.quicksum(x[i, j] + (y[i, months[months.index(j)-1]] if j != 'Jan' else 0) for j in months) >= demand[i][months.index(j)]) for j in months)

# Production capacity
for j in months:
    model.addConstr(cp.quicksum(x[i, j] / quota[i] for i in products) <= production_days[months.index(j)])

# Storage space
for j in months:
    model.addConstr(cp.quicksum(y[i, j] for i in products) <= storage_capacity)

# Minimum batch size
for i in products:
    for j in months:
        model.addConstr(x[i, j] >= min_batch[i] * z[i, j])

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized revenue: ${:.2f}".format(model.objval))
    for i in products:
        for j in months:
            print(f"Quantity of product {i} produced in {j}: {x[i, j].x:.2f}")
            print(f"Quantity of product {i} stored in {j}: {y[i, j].x:.2f}")
            print(f"Activation status of product {i} in {j}: {int(z[i, j].x)}")
else:
    print("No optimal solution found.")
```

In this script, we first define the parameters of the problem, including the products, months, demand, prices, activation costs, production costs, production quotas, minimum batch sizes, storage costs, and production days. Then, we add the decision variables `x`, `y`, and `z`, representing the production quantities, storage quantities, and activation statuses, respectively.

Next, we set the objective function to maximize revenue and add the constraints, including demand satisfaction, production capacity, storage space, and minimum batch size. Finally, we solve the model and output the results of the optimal solution, including the maximized revenue and the production and storage quantities for each product in each month.

This script provides a complete example of using the `coptpy` library to solve the company's production planning problem while satisfying all the constraints mentioned in the problem statement.

---

## Case 17  [WRONG_FORMULATION]

**GT:** 2.78195  |  **3B:** 6.2e-08 (Optimal)  |  **8B:** None

### Question
There are 10 tasks that must be run on 3 CPUs, with frequencies of 1.33, 2, and $2.66 \mathrm{GHz}$ respectively (each processor can only run one task at a time). The basic instructions (in billions of instructions, BI) for each task are as follows:

| Process | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| BI | 1.1 | 2.1 | 3 | 1 | 0.7 | 5 | 3 |

Arrange the tasks onto the processors to minimize the completion time of the last task. Use COPTPY to solve the problem.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the model
prob = LpProblem("Task_Scheduling", LpMinimize)

# Define decision variables
tasks_on_cpu1 = [LpVariable(f'task_{i}_on_CPU1', 0, None) for i in range(7)]
tasks_on_cpu2 = [LpVariable(f'task_{i}_on_CPU2', 0, None) for i in range(7)]
tasks_on_cpu3 = [LpVariable(f'task_{i}_on_CPU3', 0, None) for i in range(7)]

# Objective function: minimize the completion time of the last task
prob += lpSum([1.1*tasks_on_cpu1[i] + 2.1*tasks_on_cpu2[i] + 3.0*tasks_on_cpu3[i] for i in range(7)]) / 1e9

# Constraints: tasks must be assigned to CPUs and total number of tasks is 10
prob += lpSum(tasks_on_cpu1) == 10
prob += lpSum(tasks_on_cpu2) == 10
prob += lpSum(tasks_on_cpu3) == 10

# Solve the problem
prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Output the results
for task, cpu in zip([tasks_on_cpu1, tasks_on_cpu2, tasks_on_cpu3], ['CPU1', 'CPU2', 'CPU3']):
    print(f"Tasks assigned to {cpu}: {[task.varValue for task in task]}")
```

This code sets up a linear programming problem where the objective is to minimize the completion time of the last task by assigning each task to one of three CPUs. The constraints ensure that exactly 10 tasks are assigned to each CPU, and the decision variables represent whether a given task is assigned to a specific CPU.

### ORLM-8B formulation
## Mathematical Model:
To solve the task scheduling problem, we need to construct a mathematical model to minimize the completion time of the last task. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): If task \(i\) is assigned to processor \(j\), then \(x_{ij} = 1\); otherwise, \(x_{ij} = 0\). Here, \(i\) represents the tasks (1 to 7), and \(j\) represents the processors (1 to 3).

### Objective Function:
- Minimize the completion time of the last task: \[Z = \max_{i,j} (x_{ij} \times \frac{\text{BI}_i}{\text{frequency}_j})\]
  - This function calculates the completion time of each task on each processor and selects the maximum value as the completion time of the last task.

### Constraints:
1. Each task can only be assigned to one processor: \[\sum_{j=1}^{3} x_{ij} = 1, \forall i\]
2. Each processor can only run one task at a time: \[\sum_{i=1}^{7} x_{ij} = 1, \forall j\]

### Binary Constraints:
- \(x_{ij} \in \{0, 1\}\), for all \(i, j\).

Using this model, we can apply integer linear programming techniques to find the optimal assignment of tasks to processors that minimizes the completion time of the last task. This will provide an optimized task scheduling strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the task scheduling problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("TaskScheduling")

# Define the number of tasks and processors
num_tasks = 7
num_processors = 3

# Define the basic instructions (BI) for each task
task_BIs = [1.1, 2.1, 3, 1, 0.7, 5, 3]

# Define the frequencies of the processors (GHz)
processor_frequencies = [1.33, 2, 2.66]

# Create decision variables
x = {}
for i in range(num_tasks):
    for j in range(num_processors):
        x[i, j] = model.addVar(vtype=COPT.BINARY, name=f"x_{i}_{j}")

# Add constraints
# Each task can only be assigned to one processor
for i in range(num_tasks):
    model.addConstr(cp.quicksum(x[i, j] for j in range(num_processors)) == 1, name=f"TaskAssignment_{i}")

# Each processor can only run one task at a time
for j in range(num_processors):
    model.addConstr(cp.quicksum(x[i, j] for i in range(num_tasks)) == 1, name=f"ProcessorAssignment_{j}")

# Define the objective function
completion_times = {}
for i in range(num_tasks):
    for j in range(num_processors):
        completion_times[i, j] = x[i, j] * task_BIs[i] / processor_frequencies[j]

model.setObjective(cp.max_(completion_times[i, j) for i in range(num_tasks) for j in range(num_processors)), sense=COPT.MINIMIZE)

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print(f"Minimum completion time of the last task: {model.objval:.2f} GHz")
    for i in range(num_tasks):
        for j in range(num_processors):
            if x[i, j].x == 1:
                print(f"Task {i+1} assigned to Processor {j+1}")
else:
    print("No optimal solution found.")
```

In this script, we first define the number of tasks, the number of processors, the basic instructions for each task, and the frequencies of the processors. Then, we create binary decision variables `x[i, j]` to represent whether task `i` is assigned to processor `j`.

Next, the script adds two sets of constraints:
1. Each task can only be assigned to one processor.
2. Each processor can only run one task at a time.

The objective function is to minimize the completion time of the last task, which is calculated by multiplying the basic instructions of each task by the reciprocal of the processor frequency and selecting the maximum value.

Finally, the script solves the model and outputs the minimum completion time of the last task and the assignment of each task to a processor.

This script provides a complete example of using the `coptpy` library to solve the task scheduling problem, including creating the model, defining variables and constraints, setting the objective function, and solving the model.

---

## Case 18  [SOLVE_FAILED]

**GT:** 10000  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A company that produces only one product has 40 workers. Each worker produces 20 units per month. The demand for the semester changes according to the following table:

| Month | 1 | 2 | 3 | 4 | 5 | 6 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Demand (units) | 700 | 600 | 500 | 800 | 900 | 800 |

To adjust production based on demand, the company can offer some (paid) additional working hours (each worker can produce a maximum of 6 extra units per month, with a unit cost of 5 euros), use warehouse space (10 euros per unit per month), and hire or lay off employees (the number of employees can vary by a maximum of $\\pm 5$ per month, with a hiring cost of 500 euros per person and a layoff cost of 700 euros per person).

Initially, the warehouse space is empty, and we require it to be empty at the end of the semester as well. Develop a mathematical program to maximize revenue and solve it using COPTPY. How does the objective function change when all variables are relaxed to continuous?

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Production_Planning_Problem", LpMaximize)

# Define decision variables
workers = LpVariable('Workers', 0, None, LpInteger)
additional_hours = [LpVariable(f'Additional_Hours_{i+1}', 0, None, LpContinuous) for i in range(6)]
warehouse_space = LpVariable('Warehouse_Space', -float('inf'), float('inf'), LpContinuous)

# Objective function
prob += workers * 20 + sum(hours * 5 for hours in additional_hours), "Total_Revenue"

# Constraints
for month in range(1, 7):
    demand = 600 if month == 3 else 800 if month > 3 and month < 6 else 900 if month == 6 else 700 if month == 4 or month == 5 else 800
    prob += workers * 20 + sum(hours for hours in additional_hours[:month-1]) - demand <= warehouse_space, f'Demand_Constraint_{month}'

prob += warehouse_space >= 0, "Warehouse_Space_Constraint"

# Hiring and laying off constraints
for month in range(1, 7):
    prob += workers * 20 + sum(hours for hours in additional_hours[:month-1]) <= 45 - 5, f'Hiring_Limit_{month}'
    prob += workers * 20 + sum(hours for hours in additional_hours[:month-1]) >= -5 + 5, f'Laying_Off_Limit_{month}'

# Solve the problem
prob.solve()

# Print results
print(f"Status: {LpStatus[prob.status]}")
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")
print(f"Total Revenue: {value(prob.objective)}")
```

This code sets up a mathematical program using PuLP to maximize the total revenue for producing and selling products based on given constraints. The objective function aims to maximize the revenue from regular production, additional hours, and warehouse space usage. Constraints ensure that demand is met within the semester, warehouse space remains empty at the end of the period, and hiring or laying off employees does not exceed allowed limits.

To relax all variables to continuous, you can replace `LpVariable` with `LpContinuous`. However, this might lead to numerical instability if used in a mixed-integer context.

### ORLM-8B formulation
## Mathematical Model:
To solve the production planning problem for the company, we need to construct a linear programming model to maximize revenue while satisfying the demand for each month and the constraints on production capacity. Here is the model formulation:

### Decision Variables:
- \(x_i\): Number of workers in month \(i\).
- \(y_i\): Number of additional units produced in month \(i\).
- \(z_i\): Number of units stored in the warehouse in month \(i\).
- \(w_i\): Number of units used from the warehouse in month \(i\).
- \(h_i\): Number of units hired in month \(i\).
- \(f_i\): Number of units laid off in month \(i\).

### Objective Function:
- Maximize revenue: \[Z = \sum_{i=1}^{6} (20x_i + 6y_i - 5y_i - 10z_i + 10w_i - 500h_i - 700f_i)\]

### Constraints:
1. Demand satisfaction: \[20x_i + y_i + z_{i-1} - w_i = \text{demand}_i + h_i - f_i, \forall i \in \{1,2,3,4,5,6\}\]
2. Warehouse space: \[z_i + w_i = z_{i-1}, \forall i \in \{1,2,3,4,5,6\}\]
3. Worker number variation: \[|x_i - x_{i-1}| \leq 5, \forall i \in \{1,2,3,4,5,6\}\]
4. Additional production limit: \[0 \leq y_i \leq 6x_i, \forall i \in \{1,2,3,4,5,6\}\]
5. Non-negativity: \[x_i, y_i, z_i, w_i, h_i, f_i \geq 0, \forall i \in \{1,2,3,4,5,6\}\]

### Initial and Final Conditions:
- \(z_0 = 0\) (Initial warehouse space is empty)
- \(z_6 = 0\) (Final warehouse space should be empty)

Using this model, we can apply linear programming techniques to find the optimal production and storage strategies that maximize revenue while satisfying the demand for each month and the constraints on production capacity. This will provide the company with an economically efficient production and inventory management plan.

For the continuous variable case, we only need to relax the integer constraints on the decision variables and solve the resulting continuous linear programming problem. This will provide a more flexible production and inventory management strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the production planning problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ProductionPlanning")

# Define parameters
months = range(1, 7)
demand = {1: 700, 2: 600, 3: 500, 4: 800, 5: 900, 6: 800}
initial_workers = 40
max_extra_units = 6
unit_cost = 5
storage_cost = 10
hiring_cost = 500
firing_cost = 700
initial_storage = 0
final_storage = 0

# Add decision variables
x = {i: model.addVar(vtype=COPT.INTEGER, name=f"x_{i}") for i in months}
y = {i: model.addVar(vtype=COPT.INTEGER, name=f"y_{i}") for i in months}
z = {i: model.addVar(vtype=COPT.INTEGER, name=f"z_{i}") for i in months}
w = {i: model.addVar(vtype=COPT.INTEGER, name=f"w_{i}") for i in months}
h = {i: model.addVar(vtype=COPT.INTEGER, name=f"h_{i}") for i in months}
f = {i: model.addVar(vtype=COPT.INTEGER, name=f"f_{i}") for i in months}

# Set the objective function
model.setObjective(cp.quicksum(20*x[i] + 6*y[i] - unit_cost*y[i] - storage_cost*z[i] + 10*w[i] - hiring_cost*h[i] - firing_cost*f[i] for i in months), sense=COPT.MAXIMIZE)

# Add constraints
for i in months:
    if i == 1:
        model.addConstr(20*initial_workers + y[i] - w[i] == demand[i] + h[i] - f[i], name=f"Demand_{i}")
    else:
        model.addConstr(20*x[i] + y[i] + z[i-1] - w[i] == demand[i] + h[i] - f[i], name=f"Demand_{i}")
    
    model.addConstr(z[i] + w[i] == z[i-1], name=f"Storage_{i}")
    
    if i > 1:
        model.addConstr(x[i] - x[i-1] <= 5, name=f"Hiring_{i}")
        model.addConstr(x[i-1] - x[i] <= 5, name=f"Firing_{i}")
    
    model.addConstr(y[i] <= max_extra_units*x[i], name=f"ExtraProduction_{i}")

# Set initial and final storage conditions
model.addConstr(z[0] == initial_storage, name="InitialStorage")
model.addConstr(z[6] == final_storage, name="FinalStorage")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized revenue: {:.2f} euros".format(model.objval))
    for i in months:
        print(f"Month {i}:")
        print(f"  Number of workers: {x[i].x}")
        print(f"  Additional units produced: {y[i].x}")
        print(f"  Units stored in the warehouse: {z[i].x}")
        print(f"  Units used from the warehouse: {w[i].x}")
        print(f"  Units hired: {h[i].x}")
        print(f"  Units laid off: {f[i].x}")
else:
    print("No optimal solution found.")
```

This script first defines the parameters of the problem, then creates the decision variables and sets the objective function and constraints. Finally, it solves the model and outputs the results, including the maximized revenue and the values of each decision variable for each month.

Note that this script assumes all variables are integers. If you want to allow all variables to be continuous, you can change the `vtype` parameter of the variables to `COPT.CONTINUOUS`.

---

## Case 19  [SOLVE_FAILED]

**GT:** 153  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A traveling salesman must visit 7 customers at 7 different locations, and the (symmetric) distance matrix is as follows:

|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | - | 86 | 49 | 57 | 31 | 69 | 50 |
| 2 |  | - | 68 | 79 | 93 | 24 | 5 |
| 3 |  |  | - | 16 | 7 | 72 | 67 |
| 4 |  |  |  | - | 90 | 69 | 1 |
| 5 |  |  |  |  | - | 86 | 59 |
| 6 |  |  |  |  |  | - | 81 |

Develop a mathematical program to determine the visiting order starting from location 1 and ending at location 1, in order to minimize the traveling distance, and solve it using COPTPY.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Distance matrix
distance_matrix = [
    [0, 86, 49, 57, 31, 69, 50],
    [86, 0, 68, 79, 93, 24, 5],
    [49, 68, 0, 16, 7, 72, 67],
    [57, 79, 16, 0, 90, 69, 1],
    [31, 93, 7, 90, 0, 86, 59],
    [69, 24, 72, 69, 86, 0, 81],
    [50, 5, 67, 1, 59, 81, 0]
]

# Create the LP problem
prob = LpProblem("Traveling_Salesman", LpMinimize)

# Variables: binary variables indicating if there is an edge between two nodes
variables = []
for i in range(1, len(distance_matrix) + 1):
    for j in range(1, len(distance_matrix[0]) + 1):
        if i != j:
            variables.append(LpVariable(f"x_{i}_{j}", cat='Binary'))

# Objective function: minimize total distance
objective = lpSum([distance_matrix[i-1][j-1] * variables[k] for k, (i, j) in enumerate(variables)])

prob += objective

# Constraints: each node must be visited exactly once
for i in range(1, len(distance_matrix) + 1):
    prob += lpSum([variables[k] for k in range(len(variables)) if distance_matrix[i-1][j-1] != 0 and variables[k].varValue == 1]) == 1

# Solve the problem
prob.solve()

# Print the solution
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Distance: {value(prob.objective)}")
```

Note: The COPTPY library is not a standard Python library and does not exist. Therefore, I have omitted any reference to it in this code snippet. If you intended to use PuLP for solving the problem as specified, then no changes are needed beyond ensuring that `PuLP` is installed (`pip install pulp`).

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \(x_{ij}\): Binary variable that is 1 if the salesman travels directly from location \(i\) to location \(j\), and 0 otherwise.

### Constraints:
1. **Visit each location exactly once**:
   \[
   \sum_{j=1, j \neq i}^{7} x_{ij} = 1 \quad \forall i \in \{1, \dots, 7\}
   \]
   \[
   \sum_{i=1, i \neq j}^{7} x_{ij} = 1 \quad \forall j \in \{1, \dots, 7\}
   \]

2. **Avoid sub-tours** (using MTZ sub-tour elimination constraints):
   \[
   u_i - u_j + 7x_{ij} \leq 6 \quad \forall i, j \in \{2, \dots, 7\}, i \neq j
   \]
   where \(u_i\) is a continuous variable representing the position of location \(i\) in the tour.

### Objective:
Minimize the total traveling distance:
\[
\min \sum_{i=1}^{7} \sum_{j=1, j \neq i}^{7} d_{ij} x_{ij}
\]
where \(d_{ij}\) is the distance from location \(i\) to location \(j\).

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("TSP")

# Distance matrix
distances = {
    (1, 2): 86, (1, 3): 49, (1, 4): 57, (1, 5): 31, (1, 6): 69, (1, 7): 50,
    (2, 3): 68, (2, 4): 79, (2, 5): 93, (2, 6): 24, (2, 7): 5,
    (3, 4): 16, (3, 5): 7,  (3, 6): 72, (3, 7): 67,
    (4, 5): 90, (4, 6): 69, (4, 7): 1,
    (5, 6): 86, (5, 7): 59,
    (6, 7): 81
}

# Add decision variables
x = model.addVars([(i, j) for i in range(1, 8) for j in range(1, 8) if i != j], vtype=COPT.BINARY, nameprefix = "x")
u = model.addVars(range(1, 8), vtype=COPT.CONTINUOUS, nameprefix = "u")

# Set objective function
model.setObjective(sum(distances[i, j] * x[i, j] for i in range(1, 8) for j in range(1, 8) if i != j), sense=COPT.MINIMIZE)

# Add constraints
for i in range(1, 8):
    model.addConstr(sum(x[i, j] for j in range(1, 8) if i != j) == 1)
    model.addConstr(sum(x[j, i] for j in range(1, 8) if i != j) == 1)

for i in range(2, 8):
    for j in range(2, 8):
        if i != j:
            model.addConstr(u[i] - u[j] + 7 * x[i, j] <= 6)

# Solve the model
model.solve()

# Output the results
print("Optimal solution found with total distance:", model.objval)
for i in range(1, 8):
    for j in range(1, 8):
        if i != j and x[i, j].x > 0.5:
            print(f"Travel from {i} to {j}")
```

This script uses the COPTPY library to build and solve the traveling salesman problem (TSP) model, ensuring that the salesman visits each location exactly once and returns to the starting point, minimizing the total traveling distance.

---

## Case 20  [WRONG_FORMULATION]

**GT:** 103801  |  **3B:** 600000.0 (Optimal)  |  **8B:** None

### Question
The mass of a rocket is $m$, and it must reach a height of $H$ within time $T$ when launched at sea level. Let $y(t)$ be the height of the rocket at time $t$, and let $u(t)$ be the force acting on the rocket in the vertical direction at time $t$. Assuming $u(t)$ cannot exceed a given value $b$, the mass of the rocket $m$ remains constant throughout the process, and the gravitational acceleration $g$ remains constant in the interval $[0, H]$. Discretize the time $t \in [0, T]$ into $n$ intervals and propose a linear program to determine the force $u(t_k)$ at each moment $k \leq n$ to minimize the total energy consumption. Solve this problem using the following data: $m=2140~\mathrm{kg}$, $H=23~\mathrm{km}$, $T=1~\mathrm{min}$, $b=10000~\mathrm{N}$, $n=20$.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpStatus

# Define the problem
prob = LpProblem("RocketLaunch", LpMinimize)

# Parameters
m = 2140  # mass of the rocket in kg
H = 23000  # target height in meters
T = 60  # total time in seconds
b = 10000  # maximum force in Newtons
n = 20  # number of intervals

# Decision variables: u(t_k) for k=0, ..., n-1
u_vars = [LpVariable(f'u_{k}', lowBound=0, upBound=b) for k in range(n)]

# Objective function (total energy consumption)
energy_consumption = lpSum([u_vars[k] * T / n for k in range(n)])
prob += energy_consumption

# Constraints
for k in range(1, n):
    # Force equation: m * a_k = u(k) - m * g
    acceleration = (u_vars[k] - u_vars[k-1]) / (T / n)
    prob += m * acceleration >= 0, f'Acceleration constraint at time {k}'

# Initial and final conditions
prob += u_vars[0] == b, 'Initial force condition'
prob += u_vars[-1] <= b, 'Final force condition'

# Solve the problem
status = prob.solve()

# Check if the problem was solved successfully
if LpStatus[prob.status] != "Optimal":
    print("No solution found.")
else:
    # Print the optimal forces at each time interval
    for k in range(n):
        print(f'u_{k} = {u_vars[k].value()} N')
```

This code sets up and solves a linear program to determine the force $u(t_k)$ that minimizes total energy consumption while ensuring the rocket reaches height $H$ within time $T$. The problem is discretized into $n=20$ intervals, with each interval's force constrained by the maximum allowable force $b$.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- $u_k$: Continuous variable representing the force acting on the rocket in the vertical direction at time $t_k$.
- $y_k$: Continuous variable representing the height of the rocket at time $t_k$.
- $v_k$: Continuous variable representing the velocity of the rocket at time $t_k$.

### Constraints:
1. **Dynamics Constraints**:
   - For each $k \leq n$:
     $$
     y_{k+1} - y_k = v_k \Delta t
     $$
     $$
     v_{k+1} - v_k = \left(\frac{u_k}{m} - g\right) \Delta t
     $$
   where $\Delta t = T/n$.

2. **Initial and Terminal Conditions**:
   - $y_1 = 0$ (Initial height is sea level)
   - $y_{n+1} = H$ (Final height is $H$)
   - $v_1 = 0$ (Initial velocity is zero)

3. **Force Limit**:
   - For each $k \leq n+1$:
     $$
     -b \leq u_k \leq b
     $$

4. **Height and Velocity Bounds**:
   - For each $k \leq n+1$:
     $$
     0 \leq y_k \leq H
     $$
     $$
     v_k \geq 0
     $$

### Objective:
$$
\min \sum_{k=1}^{n} |u_k|
$$
This objective function aims to minimize the total energy consumption, which is the sum of the absolute values of the forces.

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("RocketTrajectoryOptimization")

# Parameters
m = 2140  # Rocket mass (kg)
H = 23000  # Target height (m)
T = 60  # Total time (s)
b = 10000  # Maximum force (N)
n = 20  # Number of time intervals
g = 9.81  # Gravitational acceleration (m/s^2)
delta_t = T / n  # Time interval

# Decision variables
u = model.addVars(n, lb=-b, ub=b, nameprefix = "u")
y = model.addVars(n + 1, lb=0, ub=H, nameprefix = "y")
v = model.addVars(n + 1, lb=0, nameprefix = "v")

# Initial and terminal conditions
model.addConstr(y[1] == 0, "InitialHeight")
model.addConstr(y[n + 1] == H, "FinalHeight")
model.addConstr(v[1] == 0, "InitialVelocity")

# Dynamics constraints
for k in range(1, n):
    model.addConstr(y[k + 1] - y[k] == v[k] * delta_t, "HeightDynamics")
    model.addConstr(v[k + 1] - v[k] == (u[k] / m - g) * delta_t, "VelocityDynamics")

# Objective: Minimize total energy consumption
model.setObjective(sum(abs(u[k]) for k in range(1, n + 1)), sense=COPT.MINIMIZE)

# Solve the model
model.solve()

# Output results
if model.Status == COPT.OPTIMAL:
    print("Optimal solution found:")
    for k in range(1, n + 1):
        print(f"Time {k}: Force = {u[k].x}, Height = {y[k].x}, Velocity = {v[k].x}")
else:
    print("Optimal solution not found.")
```
This script sets up and solves the optimization problem using the COPT Python API, aiming to minimize the total energy consumption of the rocket while satisfying all the constraints.

---

## Case 21  [SOLVE_FAILED]

**GT:** 8505  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A company has three types of products, I, II, and III. The contract orders for each quarter of the next year are shown in Table 1-23. At the beginning of the first quarter, there is no inventory, and it is required to have 150 units of each product in inventory at the end of the fourth quarter. It is known that the company has 15,000 hours of production time per quarter, and it takes 2 hours, 4 hours, and 3 hours to produce one unit of products I, II, and III, respectively. Due to the replacement of production equipment, product I cannot be produced in the second quarter. It is specified that if the products cannot be delivered on time, a compensation of $20 per unit per quarter is required for products I and II, and $10 for product III. If the produced products are not delivered in the same quarter, a storage fee of $5 per unit per quarter is incurred. How should the company arrange production to minimize the total compensation and storage fee?

Table 1-23
\begin{tabular}{c|c|c|c|c}
\hline \multirow{2}{*}{Product} & \multicolumn{4}{|c}{Contract Orders for Each Quarter} \\
\cline { 2 - 5 } & 1 & 2 & 3 & 4 \\
\hline I & 1500 & 1000 & 2000 & 1200 \\
II & 1500 & 1500 & 1200 & 1500 \\
III & 1000 & 2000 & 1500 & 2500 \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Create the LP problem
prob = LpProblem("Production_Planning", LpMinimize)

# Define decision variables
prod_I_1 = LpVariable('Prod_I_1', lowBound=0)
prod_I_2 = LpVariable('Prod_I_2', lowBound=0, cat='Continuous')
prod_I_3 = LpVariable('Prod_I_3', lowBound=0, cat='Continuous')

prod_II_1 = LpVariable('Prod_II_1', lowBound=0)
prod_II_2 = LpVariable('Prod_II_2', lowBound=0, cat='Continuous')
prod_II_3 = LpVariable('Prod_II_3', lowBound=0, cat='Continuous')

prod_III_1 = LpVariable('Prod_III_1', lowBound=0)
prod_III_2 = LpVariable('Prod_III_2', lowBound=0, cat='Continuous')
prod_III_3 = LpVariable('Prod_III_3', lowBound=0, cat='Continuous')

# Objective function
prob += lpSum([
    5 * prod_I_1 + 10 * prod_I_2 + 15 * prod_I_3,
    5 * prod_II_1 + 10 * prod_II_2 + 15 * prod_II_3,
    5 * prod_III_1 + 10 * prod_III_2 + 15 * prod_III_3
])

# Constraints
# Initial inventory and final inventory constraints for each product
prob += lpSum([prod_I_1, prod_II_1, prod_III_1]) == 150
prob += lpSum([prod_I_2, prod_II_2, prod_III_2]) + lpSum([prod_I_3, prod_II_3, prod_III_3]) == 450

# Production time constraint for each quarter
prob += 2 * prod_I_1 + 4 * prod_I_2 + 3 * prod_I_3 <= 15000 / 4
prob += 2 * prod_II_1 + 4 * prod_II_2 + 3 * prod_II_3 <= 15000 / 4
prob += 2 * prod_III_1 + 4 * prod_III_2 + 3 * prod_III_3 <= 15000 / 4

# Constraints for product I in the second quarter
prob += prod_I_2 == 0

# Compensation and storage fee constraints
prob += (prod_I_1 - 150) * 20 if prod_I_1 > 150 else 0, "Compensation_I"
prob += (prod_I_2 - 100) * 20 + (prod_I_3 - 200) * 20 if prod_I_2 > 100 or prod_I_3 > 200 else 0, "Compensation_I_2"
prob += (prod_II_1 - 150) * 20 + (prod_II_2 - 150) * 20 if prod_II_1 > 150 or prod_II_2 > 150 else 0, "Compensation_II"
prob += (prod_II_3 - 120) * 20 + (prod_III_1 - 100) * 20 if prod_II_3 > 120 or prod_III_1 > 100 else 0, "Compensation_II_2"
prob += (prod_III_2 - 200) * 20 + (prod_III_3 - 1500) * 20 if prod_III_2 > 200 or prod_III_3 > 1500 else 0, "Compensation_III"
prob += lpSum([prod_I_1, prod_I_2, prod_I_3]) * 5 + lpSum([prod_II_1, prod_II_2, prod_II_3]) * 5 + lpSum([prod_III_1, prod_III_2, prod_III_3]) * 5 <= 0

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Cost: ${value(prob.objective):.2f}")
```
```python
from pulp import LpProblem, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Production_Planning", LpMinimize)

# Define decision variables
prod_I_1 = LpVariable('Prod_I_1', lowBound=0)
prod_I_2 = LpVariable('Prod_I_2', lowBound=0, cat='Continuous')
prod_I_3 = LpVariable('Prod_I_3', lowBound=0, cat='Continuous')

prod_II_1 = LpVariable('Prod_II_1', lowBound=0)
prod_II_2 = LpVariable('Prod_II_2', lowBound=0, cat='Continuous')
prod_II_3 = LpVariable('Prod_II_3', lowBound=0, cat='Continuous')

prod_III_1 = LpVariable('Prod_III_1', lowBound=0)
prod_III_2 = LpVariable('Prod_III_2', lowBound=0, cat='Continuous')
prod_III_3 = LpVariable('Prod_III_3', lowBound=0, cat='Continuous')

# Objective function
prob += lpSum([
    5 * prod_I_1 + 10 * prod_I_2 + 15 * prod_I_3,
    5 * prod_II_1 + 10 * prod_II_2 + 15 * prod_II_3,
    5 * prod_III_1 + 10 * prod_III_2 + 15 * prod_III_3
])

# Constraints
# Initial inventory and final inventory constraints for each product
prob += lpSum([prod_I_1, prod_II_1, prod_III_1]) == 150
prob += lpSum([prod_I_2, prod_II_2, prod_III_2]) + lpSum([prod_I_3, prod_II_3, prod_III_3]) == 450

# Production time constraint for each quarter
prob += 2 * prod_I_1 + 4 * prod_I_2 + 3 * prod_I_3 <= 15000 / 4
prob += 2 * prod_II_1 + 4 * prod_II_2 + 3 * prod_II_3 <= 15000 / 4
prob += 2 * prod_III_1 + 4 * prod_III_2 + 3 * prod_III_3 <= 15000 / 4

# Constraints for product I in the second quarter
prob += prod_I_2 == 0

# Compensation and storage fee constraints
prob += (prod_I_1 - 150) * 20 if prod_I_1 > 150 else 0, "Compensation_I"
prob += (prod_I_2 - 100) * 20 + (prod_I_3 - 200) * 20 if prod_I_2 > 100 or prod_I_3 > 200 else 0, "Compensation_I_2"
prob += (prod_II_1 - 150) * 20 + (prod_II_2 - 150) * 20 if prod_II_1 > 150 or prod_II_2 > 150 else 0, "Compensation_II"
prob += (prod_II_3 - 120) * 20 + (prod_III_1 - 100) * 20 if prod_II_3 > 120 or prod_III_1 > 100 else 0, "Compensation_II_2"
prob += (prod_III_2 - 200) * 20 + (prod_III_3 - 1500) * 20 if prod_III_2 > 200 or prod_III_3 > 1500 else 0, "Compensation_III"
prob += lpSum([prod_I_1, prod_I_2, prod_I_3]) * 5 + lpSum([prod_II_1, prod_II_2, prod_II_3]) * 5 + lpSum([prod_III_1, prod_III_2, prod_III_3]) * 5 <= 0

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Cost: ${value(prob.objective):.2f}")
```
```python
from pulp import L

### ORLM-8B formulation
## Mathematical Model:
To solve the company's production planning problem, we need to construct a linear programming model to minimize the total compensation and storage fee while satisfying the contract orders, production time constraints, and inventory requirements. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The quantity of product \(i\) produced in quarter \(j\).
- \(s_{ij}\): The quantity of product \(i\) stored at the end of quarter \(j\).
- \(F_{ij}\): The quantity of product \(i\) delivered in quarter \(j\).
- \(R_{ij}\): The quantity of product \(i\) ordered in quarter \(j\).
- \(C_{ij}\): The compensation for product \(i\) in quarter \(j\).

### Objective Function:
- Minimize the total compensation and storage fee: \[Z = \sum_{j=1}^4 (20F_{1j} + 20F_{2j} + 10F_{3j}) + 5\sum_{i=1}^3 \sum_{j=1}^4 s_{ij}\]

### Constraints:
1. Production time constraint: \[2x_{1j} + 4x_{2j} + 3x_{3j} \leq 15000, \quad \forall j = 1, 2, 3, 4\]
2. Product I cannot be produced in the second quarter: \[x_{12} = 0\]
3. Contract order fulfillment: \[F_{ij} = R_{ij}, \quad \forall i = 1, 2, 3; \quad \forall j = 1, 2, 3, 4\]
4. Inventory balance: \[s_{i,j-1} + x_{ij} - F_{ij} = s_{ij}, \quad \forall i = 1, 2, 3; \quad \forall j = 1, 2, 3, 4\]
5. Initial inventory is zero: \[s_{i0} = 0, \quad \forall i = 1, 2, 3\]
6. End-of-year inventory requirement: \[s_{i3} + x_{i4} - F_{i4} = 150, \quad \forall i = 1, 2, 3\]

### Non-negativity Constraints:
- \(x_{ij}, s_{ij}, F_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply linear programming techniques to find the optimal production and delivery quantities for each product in each quarter, minimizing the total compensation and storage fee while satisfying all contract orders, production time constraints, and inventory requirements. This will provide the company with an economically efficient production and delivery plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionPlanning")

# Contract orders
orders = {
    1: [1500, 1000, 2000, 1200],
    2: [1500, 1500, 1200, 1500],
    3: [1000, 2000, 1500, 2500]
}

# Production time
production_time = {1: 2, 2: 4, 3: 3}
total_time = 15000

# Compensation and storage fee
compensation = {1: 20, 2: 20, 3: 10}
storage_cost = 5

# Add decision variables
x = model.addVars(3, 4, lb=0, vtype=COPT.INTEGER, nameprefix="x")
s = model.addVars(3, 4, lb=0, vtype=COPT.INTEGER, nameprefix="s")
F = model.addVars(3, 4, lb=0, vtype=COPT.INTEGER, nameprefix="F")

# Objective function: Minimize total compensation and storage fee
model.setObjective(
    cp.quicksum(compensation[i] * F[i, j] for i in range(1, 4) for j in range(1, 5)) +
    cp.quicksum(storage_cost * s[i, j] for i in range(1, 4) for j in range(1, 5)),
    sense=COPT.MINIMIZE
)

# Constraints
# Production time constraint
for j in range(1, 5):
    model.addConstr(cp.quicksum(production_time[i] * x[i, j] for i in range(1, 4)) <= total_time)

# Product I cannot be produced in the second quarter
model.addConstr(x[1, 2] == 0)

# Contract order fulfillment
for i in range(1, 4):
    for j in range(1, 5):
        model.addConstr(F[i, j] == orders[i][j-1])

# Inventory balance
for i in range(1, 4):
    for j in range(1, 5):
        if j == 1:
            model.addConstr(s[i, j-1] + x[i, j] - F[i, j] == s[i, j])
        else:
            model.addConstr(s[i, j-1] + x[i, j] - F[i, j] == s[i, j])

# Initial inventory is zero
for i in range(1, 4):
    model.addConstr(s[i, 0] == 0)

# End-of-year inventory requirement
for i in range(1, 4):
    model.addConstr(s[i, 3] + x[i, 4] - F[i, 4] == 150)

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total compensation and storage fee: {:.2f} dollars".format(model.objval))
    for i in range(1, 4):
        for j in range(1, 5):
            print(f"Quantity of product {i} produced in quarter {j}: {x[i, j].x}")
            print(f"Quantity of product {i} stored at the end of quarter {j}: {s[i, j].x}")
            print(f"Quantity of product {i} delivered in quarter {j}: {F[i, j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the contract orders, production time, compensation, and storage fee. Next, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total compensation and storage fee, as well as the production, storage, and delivery quantities for each product in each quarter.

This script provides a complete example of using the `coptpy` library to solve the company's production planning problem while satisfying all the constraints mentioned in the problem.

---

## Case 22  [CODE_BUG]

**GT:** 5069500  |  **3B:** None (?)  |  **8B:** None

### Question
The market demand for products I and II is as follows: Product I requires 10,000 units per month from January to April, 30,000 units per month from May to September, and 100,000 units per month from October to December. Product II requires 15,000 units per month from March to September and 50,000 units per month for the other months. The production cost for these two products is as follows: Product I costs $5 per unit to produce from January to May and $4.50 per unit to produce from June to December. Product II costs $8 per unit to produce from January to May and $7 per unit to produce from June to December. The total production capacity for both products should not exceed 120,000 units per month. Product I occupies 0.2 cubic meters per unit, while Product II occupies 0.4 cubic meters per unit. The warehouse capacity of the factory is 15,000 cubic meters. If the warehouse is not sufficient, the factory can rent additional space from an external facility. If occupying 1 cubic meter of the factory's storage space incurs a cost of $1 per month, and renting storage space from an external facility incurs an additional cost of $1.5 per month, how should the factory arrange its production to minimize the total production cost including storage fees while meeting market demand?

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Create a problem
prob = LpProblem("Production_Planning", LpMinimize)

# Define decision variables
x1 = LpVariable('Product_I_Units_Jan', lowBound=0, cat='Continuous')
x2 = LpVariable('Product_I_Units_Feb', lowBound=0, cat='Continuous')
x3 = LpVariable('Product_I_Units_Mar', lowBound=0, cat='Continuous')
x4 = LpVariable('Product_I_Units_Apr', lowBound=0, cat='Continuous')
x5 = LpVariable('Product_I_Units_May', lowBound=0, cat='Continuous')
x6 = LpVariable('Product_I_Units_Jun', lowBound=0, cat='Continuous')
x7 = LpVariable('Product_I_Units_Jul', lowBound=0, cat='Continuous')
x8 = LpVariable('Product_I_Units_Aug', lowBound=0, cat='Continuous')
x9 = LpVariable('Product_I_Units_Sep', lowBound=0, cat='Continuous')
x10 = LpVariable('Product_I_Units_Oct', lowBound=0, cat='Continuous')
x11 = LpVariable('Product_I_Units_Nov', lowBound=0, cat='Continuous')
x12 = LpVariable('Product_I_Units_Dec', lowBound=0, cat='Continuous')

y1 = LpVariable('Product_II_Units_Jan', lowBound=0, cat='Continuous')
y2 = LpVariable('Product_II_Units_Feb', lowBound=0, cat='Continuous')
y3 = LpVariable('Product_II_Units_Mar', lowBound=0, cat='Continuous')
y4 = LpVariable('Product_II_Units_Apr', lowBound=0, cat='Continuous')
y5 = LpVariable('Product_II_Units_May', lowBound=0, cat='Continuous')
y6 = LpVariable('Product_II_Units_Jun', lowBound=0, cat='Continuous')
y7 = LpVariable('Product_II_Units_Jul', lowBound=0, cat='Continuous')
y8 = LpVariable('Product_II_Units_Aug', lowBound=0, cat='Continuous')
y9 = LpVariable('Product_II_Units_Sep', lowBound=0, cat='Continuous')
y10 = LpVariable('Product_II_Units_Oct', lowBound=0, cat='Continuous')
y11 = LpVariable('Product_II_Units_Nov', lowBound=0, cat='Continuous')
y12 = LpVariable('Product_II_Units_Dec', lowBound=0, cat='Continuous')

# Define the objective function
prob += lpSum([
    5 * x1 + 4.5 * x6 + 4.5 * x7 + 4.5 * x8 + 4.5 * x9 + 4.5 * x10 + 4.5 * x11 + 4.5 * x12,
    8 * y1 + 7 * y6 + 7 * y7 + 7 * y8 + 7 * y9 + 7 * y10 + 7 * y11
] + [
    0.2 * x1 + 0.4 * y1,
    0.2 * x2 + 0.4 * y2,
    0.2 * x3 + 0.4 * y3,
    0.2 * x4 + 0.4 * y4,
    0.2 * x5 + 0.4 * y5,
    0.2 * x6 + 0.4 * y6,
    0.2 * x7 + 0.4 * y7,
    0.2 * x8 + 0.4 * y8,
    0.2 * x9 + 0.4 * y9,
    0.2 * x10 + 0.4 * y10,
    0.2 * x11 + 0.4 * y11
] - lpSum([
    15000 * (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12),
    15000 * (y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11)
] - lpSum([
    min(1, (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12) / 120000) * 1.5,
    min(1, (y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11) / 120000) * 1.5
]) == 0)

# Define constraints for market demand and production capacity
prob += lpSum([
    x1, x2, x3, x4, x5,
    x6, x7, x8, x9, x10, x11, x12,
    y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11
]) >= 10000 * (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12) + 30000 * (x6 + x7 + x8 + x9 + x10 + x11) + 100000 * (x12)

prob += lpSum([
    x1, x2, x3, x4, x5,
    x6, x7, x8, x9, x10, x11, x12,
    y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11
]) <= 120000

prob += lpSum([
    0.2 * x1 + 0.4 * y1,
    0.2 * x2 + 0.4 * y2,
    0.2 * x3 + 0.4 * y3,
    0.2 * x4 + 0.4 * y4,
    0.2 * x5 + 0.4 * y5,
    0.2 * x6 + 0.4 * y6,
    0.2 * x7 + 0.4 * y7,
    0.2 * x8 + 0.4 * y8,
    0.2 * x9 + 0.4 * y9,
    0.2 * x10 + 0.4 * y10,
    0.2 * x11 + 0.4 * y11
]) <= 15000

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Cost: ${value(prob.objective):.2f}")
```

This code sets up and solves a linear programming model to minimize production costs while meeting market demand for products I and II, considering both the internal storage capacity of the factory and external rental space if needed.

### ORLM-8B formulation
## Mathematical Model:
To solve the factory's production and storage problem, we need to construct a linear programming model to minimize the total production cost including storage fees while meeting market demand and warehouse capacity constraints. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The quantity of Product I produced in month \(i\), where \(i = 1, \ldots, 12\).
- \(y_{ij}\): The quantity of Product II produced in month \(i\), where \(i = 1, \ldots, 12\).
- \(s_{ij}\): The storage quantity of Product I in month \(i\), where \(i = 1, \ldots, 12\).
- \(t_{ij}\): The storage quantity of Product II in month \(i\), where \(i = 1, \ldots, 12\).
- \(S\): The additional storage space rented from an external facility (in cubic meters).

### Objective Function:
- Minimize the total cost: \[Z = \sum_{i=1}^{12} (5x_{i1} + 8y_{i1} + 4.5x_{i6} + 7y_{i6}) + \sum_{i=1}^{5} (5x_{i2} + 8y_{i2}) + \sum_{i=6}^{12} (4.5x_{i3} + 7y_{i3}) + S + 1.5S\]

### Constraints:
1. Market demand satisfaction:
   - \(x_{11} + x_{12} + x_{13} + x_{14} = 40000\)
   - \(x_{15} + x_{16} + x_{17} + x_{18} + x_{19} + x_{110} + x_{111} + x_{112} = 90000\)
   - \(x_{113} + x_{114} + x_{115} + x_{116} + x_{117} + x_{118} + x_{119} + x_{120} = 100000\)
   - \(y_{11} + y_{12} + y_{13} + y_{14} + y_{15} + y_{16} + y_{17} + y_{18} + y_{19} + y_{110} + y_{111} + y_{112} + y_{113} + y_{114} + y_{115} + y_{116} + y_{117} + y_{118} + y_{119} + y_{120} + y_{121} + y_{122} + y_{123} + y_{124} = 50000\)
   - \(y_{125} + y_{126} + y_{127} + y_{128} + y_{129} + y_{210} + y_{211} + y_{212} + y_{213} + y_{214} + y_{215} + y_{216} + y_{217} + y_{218} + y_{219} + y_{310} + y_{311} + y_{312} + y_{313} + y_{314} + y_{315} + y_{316} + y_{317} + y_{318} + y_{319} + y_{410} + y_{411} + y_{412} + y_{413} + y_{414} + y_{415} + y_{416} + y_{417} + y_{418} + y_{419} = 15000\)
2. Warehouse capacity constraint:
   - \(\sum_{i=1}^{12} (0.2x_{i} + 0.4y_{i}) + S \leq 15000\)
3. Production capacity constraint:
   - \(\sum_{i=1}^{12} (x_{i} + y_{i}) \leq 120000\)
4. Non-negativity constraints:
   - \(x_{ij}, y_{ij}, s_{ij}, t_{ij} \geq 0\), for all \(i, j\)
   - \(S \geq 0\)

Using this model, we can apply linear programming techniques to find the optimal production and storage plan that minimizes the total cost while meeting market demand and warehouse capacity constraints. This will provide the factory with an economically efficient production and storage strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionStorageOptimization")

# Add decision variables
x = model.addVars(12, 2, lb=0, vtype=COPT.INTEGER, nameprefix="x")  # Production quantity of Product I
y = model.addVars(12, 2, lb=0, vtype=COPT.INTEGER, nameprefix="y")  # Production quantity of Product II
s = model.addVars(12, 2, lb=0, vtype=COPT.INTEGER, nameprefix="s")  # Storage quantity of Product I
t = model.addVars(12, 2, lb=0, vtype=COPT.INTEGER, nameprefix="t")  # Storage quantity of Product II
S = model.addVar(lb=0, name="S")  # Additional storage space rented from an external facility

# Objective function: Minimize total cost
model.setObjective(
    cp.quicksum(5*x[i,0] + 8*y[i,0] for i in range(1, 6)) +
    cp.quicksum(4.5*x[i,1] + 7*y[i,1] for i in range(6, 13)) +
    S + 1.5*S,
    sense=COPT.MINIMIZE
)

# Constraints
# Market demand satisfaction
model.addConstr(cp.quicksum(x[i,0] for i in range(1, 5)) == 40000, name="DemandI_1_4")
model.addConstr(cp.quicksum(x[i,1] for i in range(5, 13)) == 90000, name="DemandI_5_12")
model.addConstr(cp.quicksum(y[i,0] for i in range(1, 13)) == 50000, name="DemandII_1_12")
model.addConstr(cp.quicksum(y[i,1] for i in range(3, 13)) == 15000, name="DemandII_4_12")

# Warehouse capacity constraint
model.addConstr(cp.quicksum(0.2*x[i,j] + 0.4*y[i,j] for i in range(1, 13) for j in range(2)) + S <= 15000, name="StorageCapacity")

# Production capacity constraint
model.addConstr(cp.quicksum(x[i,j] + y[i,j] for i in range(1, 13) for j in range(2)) <= 120000, name="ProductionCapacity")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} dollars".format(model.objval))
    for i in range(1, 13):
        for j in range(2):
            if x[i,j].x > 0:
                print(f"Quantity of Product I produced in month {i}: {x[i,j].x}")
            if y[i,j].x > 0:
                print(f"Quantity of Product II produced in month {i}: {y[i,j].x}")
    print(f"Additional storage space rented from an external facility: {S.x:.2f} cubic meters")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables, set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total cost and the production and storage quantities for each month.

This script provides a complete example of using the `coptpy` library to solve the factory's production and storage problem while satisfying all the constraints mentioned in the problem.

---

## Case 23  [CODE_BUG]

**GT:** 105.52  |  **3B:** None (?)  |  **8B:** None

### Question
A factory produces two types of food, I and II. There are currently 50 skilled workers. It is known that one skilled worker can produce food I at a rate of 10 kg/h or food II at a rate of 6 kg/h. According to the contract, the demand for these two types of food will sharply increase each week, as shown in Table 1-11. To meet this demand, the factory plans to train 50 new workers by the end of the 8th week, with production in two shifts. It is known that one worker works 40 hours per week, and a skilled worker can train no more than three new workers in two weeks (during the training period, skilled workers and trainees do not participate in production). Skilled workers earn a weekly salary of 360 yuan, trainees earn a weekly salary of 120 yuan during the training period, and a weekly salary of 240 yuan after training is completed. Their production efficiency is the same as that of skilled workers. During the training transition period, many skilled workers are willing to work overtime. The factory decides to arrange for some workers to work 60 hours per week at a salary of 540 yuan per week. If the ordered food cannot be delivered on time, there is a compensation fee of 0.50 yuan per kg for food I and 0.60 yuan per kg for food II. Under the above conditions, how should the factory make comprehensive arrangements to minimize the total cost?

Table 1-11
\begin{tabular}{|c|c|c|c|c|c|c|c|c|}
\hline Food Week & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 \\
\hline I & 10 & 10 & 12 & 12 & 16 & 16 & 20 & 20 \\
\hline II & 6 & 7. 2 & 8.4 & 10.8 & 10.8 & 12 & 12 & 12 \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Initialize the problem as a maximization problem
prob = LpProblem("FoodProduction", LpMaximize)

# Define decision variables
skilled_workers_week1_to_8 = {}
for week in range(1, 9):
    for shift in ['day', 'night']:
        skilled_workers_week1_to_8[shift] = LpVariable(f'SkilledWorkers_{week}_{shift}', lowBound=0)

new_trainees_week2_to_4 = []
for week in range(2, 5):
    new_trainees_week2_to_4.append(LpVariable(f'Trainees_{week}_1', lowBound=0))
    new_trainees_week2_to_4.append(LpVariable(f'Trainees_{week}_2', lowBound=0))

new_trainees_week5_to_8 = []
for week in range(5, 9):
    new_trainees_week5_to_8.append(LpVariable(f'Trainees_{week}_1', lowBound=0))
    new_trainees_week5_to_8.append(LpVariable(f'Trainees_{week}_2', lowBound=0))

# Define the objective function
objective = lpSum([
    360 * skilled_workers_week1_to_8['day'] + 360 * skilled_workers_week1_to_8['night'],
    120 * new_trainees_week2_to_4[0] + 120 * new_trainees_week2_to_4[1],
    120 * new_trainees_week5_to_8[0] + 120 * new_trainees_week5_to_8[1],
    240 * (new_trainees_week2_to_4[0] + new_trainees_week2_to_4[1] + 
           new_trainees_week5_to_8[0] + new_trainees_week5_to_8[1])
])

prob += objective

# Define constraints
# Constraint for skilled workers' production capacity
for week in range(1, 9):
    prob += lpSum([
        skilled_workers_week1_to_8['day'] * 40,
        skilled_workers_week1_to_8['night'] * 40
    ]) >= lpSum([
        new_trainees_week2_to_4[0] + new_trainees_week2_to_4[1],
        new_trainees_week5_to_8[0] + new_trainees_week5_to_8[1]
    ]), f'SkilledWorkers_{week}_production'

# Constraint for skilled workers' training capacity
for week in range(2, 9):
    prob += lpSum([
        new_trainees_week2_to_4[0],
        new_trainees_week2_to_4[1]
    ]) <= 3 * (skilled_workers_week1_to_8[f'day_{week-1}'] + skilled_workers_week1_to_8[f'night_{week-1}']), f'Trainees_{week}_training'

# Constraint for total number of workers
prob += lpSum([
    skilled_workers_week1_to_8['day'],
    skilled_workers_week1_to_8['night']
]) + lpSum([
    new_trainees_week2_to_4[0],
    new_trainees_week2_to_4[1]
] + 
lpSum([
    new_trainees_week5_to_8[0],
    new_trainees_week5_to_8[1]
]) <= 50, 'TotalWorkers'

# Constraint for overtime workers
prob += lpSum([
    skilled_workers_week1_to_8[f'day_{week}'] * 20,
    skilled_workers_week1_to_8[f'night_{week}'] * 20
]) >= lpSum([
    new_trainees_week2_to_4[0],
    new_trainees_week2_to_4[1]
] + 
lpSum([
    new_trainees_week5_to_8[0],
    new_trainees_week5_to_8[1]
]), 'OvertimeWorkers'

# Constraint for production of food I
prob += lpSum([
    skilled_workers_week1_to_8['day'] * 10,
    skilled_workers_week1_to_8['night'] * 10,
    new_trainees_week2_to_4[0] * 6,
    new_trainees_week2_to_4[1] * 6,
    new_trainees_week5_to_8[0] * 6,
    new_trainees_week5_to_8[1] * 6
]) >= lpSum([
    food_I_demand[week]
    for week in range(1, 9)
]), 'FoodIProduction'

# Constraint for production of food II
prob += lpSum([
    skilled_workers_week1_to_8['day'] * 6,
    skilled_workers_week1_to_8['night'] * 6,
    new_trainees_week2_to_4[0] * 7.2,
    new_trainees_week2_to_4[1] * 7.2,
    new_trainees_week5_to_8[0] * 8.4,
    new_trainees_week5_to_8[1] * 8.4
]) >= lpSum([
    food_II_demand[week]
    for week in range(1, 9)
]), 'FoodIIProduction'

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Cost: {value(prob.objective)}")
```

Please note that this code assumes there are variables `food_I_demand` and `food_II_demand` which represent the demand for food I and II respectively. These should be defined based on Table 1-11, but as they are not provided in the question, they have been omitted from the code above.

### ORLM-8B formulation
## Mathematical Model:
To solve the factory's production and cost minimization problem, we need to construct a linear programming model to determine the optimal production and training plan. Here is the model formulation:

### Decision Variables:
- \(x_i\): Number of skilled workers working overtime in week \(i\).
- \(y_i\): Number of skilled workers working in two shifts in week \(i\).
- \(z_i\): Number of skilled workers training new workers in week \(i\).
- \(w_i\): Number of new workers starting training in week \(i\).
- \(F_{1i}\): Quantity of food I produced in week \(i\).
- \(F_{2i}\): Quantity of food II produced in week \(i\).
- \(R_{1i}\): Quantity of food I not delivered on time in week \(i\).
- \(R_{2i}\): Quantity of food II not delivered on time in week \(i\).

### Objective Function:
- Minimize the total cost, including wages, training costs, and compensation fees:
\[ \min Z = \sum_{i=1}^8 \left[ 540x_i + 360y_i + 540z_i + 120w_i + 0.5R_{1i} + 0.6R_{2i} \right] \]

### Constraints:
1. Production constraints to meet the demand for each week:
   - \( F_{1i} + R_{1i} = D_{1i}, \quad \forall i \)
   - \( F_{2i} + R_{2i} = D_{2i}, \quad \forall i \)
2. Worker allocation constraints to ensure sufficient workers for production and training:
   - \( x_i + y_i + z_i \leq 50, \quad \forall i \leq 6 \)
   - \( x_i + y_i + z_i + w_i \leq 50, \quad \forall i \leq 7 \)
3. Training constraints to ensure the training of new workers:
   - \( \sum_{i=1}^7 w_i = 50 \)
4. Overtime constraints to ensure overtime work does not exceed the total number of workers:
   - \( \sum_{i=1}^8 x_i \leq 50 \)
5. Production efficiency constraints to ensure the production efficiency of skilled workers and trainees:
   - \( F_{1i} + F_{2i} \leq 10y_i + 6z_i + 6w_i, \quad \forall i \)
6. Non-negativity constraints:
   - \( x_i, y_i, z_i, w_i, F_{1i}, F_{2i}, R_{1i}, R_{2i} \geq 0, \quad \forall i \)

Using this model, we can apply linear programming techniques to find the optimal production and training plan that minimizes the total cost while meeting the demand for each week and the constraints on worker allocation.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("FactoryProductionOptimization")

# Define the number of weeks
weeks = list(range(1, 9))

# Define the demand for food I and II
demand_1 = {1: 10, 2: 10, 3: 12, 4: 12, 5: 16, 6: 16, 7: 20, 8: 20}
demand_2 = {1: 6, 2: 7.2, 3: 8.4, 4: 10.8, 5: 10.8, 6: 12, 7: 12, 8: 12}

# Add decision variables
x = model.addVars(weeks, vtype=COPT.INTEGER, name="x")  # Overtime workers
y = model.addVars(weeks, vtype=COPT.INTEGER, name="y")  # Workers in two shifts
z = model.addVars(weeks, vtype=COPT.INTEGER, name="z")  # Workers training new workers
w = model.addVars(weeks, vtype=COPT.INTEGER, name="w")  # New workers starting training
F1 = model.addVars(weeks, vtype=COPT.CONTINUOUS, name="F1")  # Quantity of food I produced
F2 = model.addVars(weeks, vtype=COPT.CONTINUOUS, name="F2")  # Quantity of food II produced
R1 = model.addVars(weeks, vtype=COPT.CONTINUOUS, name="R1")  # Quantity of food I not delivered on time
R2 = model.addVars(weeks, vtype=COPT.CONTINUOUS, name="R2")  # Quantity of food II not delivered on time

# Objective function: Minimize the total cost
model.setObjective(
    cp.quicksum(540 * x[i] + 360 * y[i] + 540 * z[i] + 120 * w[i] + 0.5 * R1[i] + 0.6 * R2[i] for i in weeks),
    sense=COPT.MINIMIZE
)

# Constraints
# Production constraints
for i in weeks:
    model.addConstr(F1[i] + R1[i] == demand_1[i], name=f"ProdDemand1_{i}")
    model.addConstr(F2[i] + R2[i] == demand_2[i], name=f"ProdDemand2_{i}")

# Worker allocation constraints
for i in weeks[:7]:
    model.addConstr(x[i] + y[i] + z[i] <= 50, name=f"WorkerLimit_{i}")
for i in weeks[:8]:
    model.addConstr(x[i] + y[i] + z[i] + w[i] <= 50, name=f"WorkerLimitWithTrainees_{i}")

# Training constraints
model.addConstr(cp.quicksum(w[i] for i in weeks[:7]) == 50, name="TrainingLimit")

# Overtime constraints
model.addConstr(cp.quicksum(x[i] for i in weeks) <= 50, name="OvertimeLimit")

# Production efficiency constraints
for i in weeks:
    model.addConstr(F1[i] + F2[i] <= 10 * y[i] + 6 * z[i] + 6 * w[i], name=f"Efficiency_{i}")

# Non-negativity constraints
for var in [x, y, z, w, F1, F2, R1, R2]:
    for i in weeks:
        model.addConstr(var[i] >= 0, name=f"NonNegativity_{var.name}_{i}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} yuan".format(model.objval))
    for i in weeks:
        print(f"Week {i}: Overtime workers {x[i].x}, Workers in two shifts {y[i].x}, Workers training new workers {z[i].x}, New workers starting training {w[i].x}, Quantity of food I produced {F1[i].x:.2f}, Quantity of food II produced {F2[i].x:.2f}, Quantity of food I not delivered on time {R1[i].x:.2f}, Quantity of food II not delivered on time {R2[i].x:.2f}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the number of weeks, the demand for food I and II, and add the decision variables. Next, we set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total cost and the specific production and training plan for each week.

This script provides a complete example of using the `coptpy` library to solve the factory's production and cost minimization problem while satisfying all the constraints mentioned in the problem.

---

## Case 24  [SOLVE_FAILED]

**GT:** -99999  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A large paper manufacturing company has 10 paper mills and supplies 1000 customers. These paper mills use three interchangeable machines and four different raw materials to produce five types of paper. The company wants to develop a plan to determine the quantity of each type of paper produced on each machine in each mill, and to determine which type of paper is supplied to which customers and in what quantity, in order to minimize total transportation costs. The following information is known:

$D_{j k}$ - Customer j requires k units of paper each month;
$r_{k l m}$ - The amount of raw material m required to produce one unit of paper of type k on machine l;
$R_{i m}$ - The amount of raw material m available each month at mill i;
$c_{k l}$ - The machine time required to produce one unit of paper of type k on machine l;
$c_{i l}$ - The machine time available each month at mill i for machine type l;
$P_{i k l}$ - The cost of producing one unit of paper of type k on machine type l at mill i;
$T_{i j k}$ - The cost of transporting one unit of paper of type k from mill i to customer j.

Develop a linear programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Paper_Manufacturing_Planning", LpMinimize)

# Decision variables
for i in range(10):  # Number of mills (1 to 10)
    for k in range(5):  # Types of paper (1 to 5)
        for l in range(3):  # Machines (1 to 3)
            x = LpVariable(f"x{i}{k}{l}", lowBound=0, cat='Continuous')
            prob += x

for i in range(10):  # Number of mills (1 to 10)
    for j in range(1000):  # Customers (1 to 1000)
        y = LpVariable(f"y{i}{j}", lowBound=0, cat='Continuous')
        prob += y

# Objective function
for i in range(10):
    for k in range(5):
        for l in range(3):
            prob += x[i][k][l] <= c[i][k][l] * R[i]

prob += lpSum(P[i][k][l] * x[i][k][l] for i in range(10) for k in range(5) for l in range(3))

# Constraints
for j in range(1000):
    prob += lpSum(T[i][j][k] * y[i][j] for i in range(10)) >= D[j]

for i in range(10):
    for k in range(5):
        prob += lpSum(r[k][l][i] * x[i][k][l] for l in range(3)) <= R[i]

# Solve the problem
prob.solve()
```

Note: The above code is a template and needs to be filled with actual data. In this example, I used placeholders like `c`, `R`, `P`, and `T` which should be replaced by the specific values for each mill, machine type, paper type, customer, etc.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{i k l} \): The quantity of paper of type \( k \) produced on machine type \( l \) at mill \( i \).
- \( y_{i j k} \): The quantity of paper of type \( k \) supplied from mill \( i \) to customer \( j \).

### Constraints:
1. **Demand Satisfaction Constraint**:
   \[
   \sum_{i=1}^{10} y_{i j k} = D_{j k}, \quad \forall j \in \{1, \ldots, 1000\}, k \in \{1, \ldots, 5\}
   \]
   The demand for each type of paper from each customer must be satisfied.

2. **Raw Material Usage Constraint**:
   \[
   \sum_{k=1}^{5} \sum_{l=1}^{3} r_{k l m} x_{i k l} \leq R_{i m}, \quad \forall i \in \{1, \ldots, 10\}, m \in \{1, \ldots, 4\}
   \]
   The usage of each type of raw material at each mill must not exceed the available quantity.

3. **Machine Time Usage Constraint**:
   \[
   \sum_{k=1}^{5} c_{k l} x_{i k l} \leq c_{i l}, \quad \forall i \in \{1, \ldots, 10\}, l \in \{1, 2, 3\}
   \]
   The usage of each machine type at each mill must not exceed the available machine time.

4. **Production and Supply Balance Constraint**:
   \[
   \sum_{l=1}^{3} x_{i k l} = \sum_{j=1}^{1000} y_{i j k}, \quad \forall i \in \{1, \ldots, 10\}, k \in \{1, \ldots, 5\}
   \]
   The total quantity of each type of paper produced at each mill must equal the total quantity supplied to customers.

5. **Non-Negativity Constraint**:
   \[
   x_{i k l} \geq 0, \quad y_{i j k} \geq 0, \quad \forall i, j, k, l
   \]
   All decision variables must be non-negative.

### Objective:
Minimize total cost, including production cost and transportation cost:
\[
\min Z = \sum_{i=1}^{10} \sum_{k=1}^{5} \sum_{l=1}^{3} P_{i k l} x_{i k l} + \sum_{i=1}^{10} \sum_{j=1}^{1000} \sum_{k=1}^{5} T_{i j k} y_{i j k}
\]

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("PaperProduction")

# Define decision variables
x = model.addVars(10, 5, 3, vtype=COPT.CONTINUOUS, nameprefix = "x")
y = model.addVars(10, 1000, 5, vtype=COPT.CONTINUOUS, nameprefix = "y")

# Define parameters (example, actual data should be provided)
D = {(j, k): 100 for j in range(1, 1001) for k in range(1, 6)}  # Customer demand
r = {(k, l, m): 1 for k in range(1, 6) for l in range(1, 4) for m in range(1, 5)}  # Raw material requirement
R = {(i, m): 1000 for i in range(1, 11) for m in range(1, 5)}  # Raw material supply
c_kl = {k: 1 for k in range(1, 6)}  # Machine time requirement
c_il = {(i, l): 100 for i in range(1, 11) for l in range(1, 4)}  # Machine time supply
P = {(i, k, l): 1 for i in range(1, 11) for k in range(1, 6) for l in range(1, 4)}  # Production cost
T = {(i, j, k): 1 for i in range(1, 11) for j in range(1, 1001) for k in range(1, 6)}  # Transportation cost

# Add constraints
for j in range(1, 1001):
    for k in range(1, 6):
        model.addConstr(sum(y[i, j, k] for i in range(1, 11)) == D[j, k])

for i in range(1, 11):
    for m in range(1, 5):
        model.addConstr(sum(r[k, l, m] * x[i, k, l] for k in range(1, 6) for l in range(1, 4)) <= R[i, m])

for i in range(1, 11):
    for l in range(1, 4):
        model.addConstr(sum(c_kl[k] * x[i, k, l] for k in range(1, 6)) <= c_il[i, l])

for i in range(1, 11):
    for k in range(1, 6):
        model.addConstr(sum(x[i, k, l] for l in range(1, 4)) == sum(y[i, j, k] for j in range(1, 1001)))

# Set objective function
model.setObjective(sum(P[i, k, l] * x[i, k, l] for i in range(1, 11) for k in range(1, 6) for l in range(1, 4)) +
                   sum(T[i, j, k] * y[i, j, k] for i in range(1, 11) for j in range(1, 1001) for k in range(1, 6)), COPT.MINIMIZE)

# Solve the model
model.solve()

# Output the results
if model.Status == COPT.OPTIMAL:
    print("Optimal solution found with total cost:", model.objval)
    for i in range(1, 11):
        for k in range(1, 6):
            for l in range(1, 4):
                if x[i, k, l].x > 0:
                    print(f"Mill {i} produces {x[i, k, l].x} units of paper type {k} on machine {l}")
    for i in range(1, 11):
        for j in range(1, 1001):
            for k in range(1, 6):
                if y[i, j, k].x > 0:
                    print(f"Mill {i} supplies {y[i, j, k].x} units of paper type {k} to customer {j}")
```
This script sets up the model, defines variables and constraints, and solves the problem to minimize the total cost of production and transportation. Adjustments may be necessary based on actual data and specific constraints.

---

## Case 25  [CODE_BUG]

**GT:** 76  |  **3B:** None (?)  |  **8B:** None

### Question
A certain factory needs a special tool in $n$ planning stages. In the $j$-th stage, $r_j$ specialized tools are required. At the end of each stage, the tools used in that stage must be sent for repair before they can be used again. There are two types of repairs: slow repair, which is cheaper (costs $b$ dollars per repair) but takes longer (requires $p$ stages to retrieve the tool), and fast repair, which is more expensive (costs $c$ dollars per repair, where $c>b$) but faster (requires $q$ stages to retrieve the tool, where $q<p$). If the repaired tools cannot meet the requirements, new tools need to be purchased at a cost of $a$ dollars per tool ($a>c$). Furthermore, these specialized tools will not be used after $n$ stages. Determine an optimal plan for purchasing and repairing tools to minimize the cost spent on tools during the planning period.

n = 10  # number of stages
r = [0] + [3, 5, 2, 4, 6, 5, 4, 3, 2, 1]  # tool requirements per stage, indexing starts at 1
a = 10  # cost of buying a new tool
b = 1   # cost of slow repair
c = 3   # cost of fast repair
p = 3   # slow repair duration
q = 1   # fast repair duration

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, minimize, PULP_CBC_CMD

n = 10  # number of stages
r = [0] + [3, 5, 2, 4, 6, 5, 4, 3, 2, 1]  # tool requirements per stage, indexing starts at 1
a = 10  # cost of buying a new tool
b = 1   # cost of slow repair
c = 3   # cost of fast repair
p = 3   # slow repair duration
q = 1   # fast repair duration

# Create the LP problem
prob = LpProblem("Tool_Repair_Problem", LpMinimize)

# Decision variables
repair_slow = [LpVariable(f'repair_slow_{j}', lowBound=0, cat='Continuous') for j in range(1, n+1)]
repair_fast = [LpVariable(f'repair_fast_{j}', lowBound=0, cat='Continuous')]

# Objective function: minimize total cost
prob += lpSum([r[j] * a + r[j-1] * b if r[j-1] > 0 else r[j] * a for j in range(1, n+1)] +
              [repair_slow[j] * b / p + repair_fast[j] * c / q for j in range(n)])

# Constraints
for j in range(1, n+1):
    if r[j-1] > 0:
        prob += repair_slow[j] >= r[j-1]
        prob += repair_fast[j] >= r[j-1]

# Solve the problem
solver = PULP_CBC_CMD()
prob.solve(solver)

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print("Total Cost: ", value(prob.objective))
```

This code sets up and solves a linear programming (LP) model to minimize the cost of purchasing and repairing specialized tools over $n$ planning stages. The `PuLP` library is used to define the problem, including decision variables for each stage's repair choices, an objective function that minimizes total costs, and constraints ensuring sufficient tools are available at each stage.

### ORLM-8B formulation
## Mathematical Model:
To solve the factory's tool purchasing and repair problem, we need to construct a dynamic programming model to minimize the total cost spent on tools during the planning period. Here is the model formulation:

### Decision Variables:
- $x_j$: Number of new tools purchased in stage $j$.
- $y_j$: Number of tools sent for slow repair in stage $j$.
- $z_j$: Number of tools sent for fast repair in stage $j$.
- $s_j$: Number of tools available for use in stage $j$.

### Objective Function:
- Minimize the total cost: $Z = \sum_{j=1}^{n} (a x_j + b y_j + c z_j)$

### Constraints:
1. Tool requirements are met: $x_j + y_j + z_j - s_j = r_j, \quad \forall j \in \{1, \ldots, n\}$
2. Slowly repaired tools are available after $p$ stages: $y_j = y_{j+p}, \quad \forall j \in \{1, \ldots, n-p+1\}$
3. Fast repaired tools are available after $q$ stages: $z_j = z_{j+q}, \quad \forall j \in \{1, \ldots, n-q+1\}$
4. Tools are not used after $n$ stages: $s_j = 0, \quad \forall j \in \{n+1, \ldots, n+r_n\}$
5. Non-negativity constraints: $x_j, y_j, z_j, s_j \geq 0, \quad \forall j \in \{1, \ldots, n+r_n\}$

### Integer Constraints:
- $x_j, y_j, z_j, s_j$ must be integers, as the number of tools cannot be fractional.

Using this model, we can apply dynamic programming techniques to find the optimal purchasing and repair plan for tools, minimizing the total cost spent on tools during the planning period. This will provide the factory with an economically efficient tool management strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ToolManagement")

# Define parameters
n = 10  # number of stages
r = [0] + [3, 5, 2, 4, 6, 5, 4, 3, 2, 1]  # tool requirements per stage
a = 10  # cost of buying a new tool
b = 1   # cost of slow repair
c = 3   # cost of fast repair
p = 3   # slow repair duration
q = 1   # fast repair duration

# Add decision variables
x = model.addVars(n+max(r), vtype=COPT.INTEGER, name="x")  # number of new tools purchased
y = model.addVars(n+max(r), vtype=COPT.INTEGER, name="y")  # number of tools sent for slow repair
z = model.addVars(n+max(r), vtype=COPT.INTEGER, name="z")  # number of tools sent for fast repair
s = model.addVars(n+max(r), vtype=COPT.INTEGER, name="s")  # number of tools available for use

# Objective function: minimize total cost
model.setObjective(cp.quicksum(a * x[j] + b * y[j] + c * z[j] for j in range(1, n+1)), sense=COPT.MINIMIZE)

# Constraints
for j in range(1, n+1):
    model.addConstr(x[j] + y[j] + z[j] - s[j] == r[j], name=f"Demand_{j}")

for j in range(n-p+1, n+1):
    model.addConstr(y[j] == y[j-p], name=f"SlowRepair_{j}")

for j in range(n-q+1, n+1):
    model.addConstr(z[j] == z[j-q], name=f"FastRepair_{j}")

for j in range(n+1, n+r[n]+1):
    model.addConstr(s[j] == 0, name=f"EndUse_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} dollars".format(model.objval))
    for j in range(1, n+1):
        print(f"Number of new tools purchased in stage {j}: {x[j].x}")
        print(f"Number of tools sent for slow repair in stage {j}: {y[j].x}")
        print(f"Number of tools sent for fast repair in stage {j}: {z[j].x}")
        print(f"Number of tools available for use in stage {j}: {s[j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the parameters and add the decision variables. Next, we set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the number of new tools purchased, tools sent for slow repair, tools sent for fast repair, and tools available for use in each stage.

This script provides a complete example of using the `coptpy` library to solve the factory's tool purchasing and repair problem, while satisfying all the constraints mentioned in the problem.

---

## Case 26  [WRONG_FORMULATION]

**GT:** 44480.0  |  **3B:** 12801600.0 (Optimal)  |  **8B:** None

### Question
A company has three tasks that require the recruitment of skilled workers and laborers. The first task can be completed by a skilled worker alone or by a team consisting of one skilled worker and two laborers. The second task can be completed by either a skilled worker or a laborer alone. The third task can be completed by a team of five laborers or by a skilled worker leading three laborers. It is known that the weekly wages for skilled workers and laborers are 100 yuan and 80 yuan, respectively. They work 48 hours per week, but their actual effective working time is 42 hours and 36 hours, respectively. To complete these three tasks, the company needs a total effective working time of 10,000 hours for the first task, 20,000 hours for the second task, and 30,000 hours for the third task. The number of workers that can be recruited is limited to a maximum of 400 skilled workers and 800 laborers. Establish a mathematical model to determine the number of skilled workers and laborers to recruit in order to minimize the total wage expenditure.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Create problem
prob = LpProblem("WorkerRecruitment", LpMinimize)

# Define decision variables
skilled_workers = LpVariable('SkilledWorkers', 0, None, LpInteger)
laborers = LpVariable('Laborers', 0, None, LpInteger)

# Objective function: minimize total wage expenditure
prob += lpSum([100*42*skilled_workers + 80*36*laborers]), "TotalWageExpenditure"

# Constraints for each task
task1_constraint = lpSum([skilled_workers/42, skilled_workers/42 + laborers/72]) >= 10000 / (42 * 4.5)
task2_constraint = lpSum([skilled_workers/42, laborers/36]) >= 20000 / (36 * 4.5)
task3_constraint = lpSum([laborers/36, skilled_workers/42 + laborers/72]) >= 30000 / (36 * 4.5)

# Add constraints
prob += task1_constraint
prob += task2_constraint
prob += task3_constraint

# Solve the problem
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("TotalWageExpenditure = ", value(prob.objective))
```

Note: The above code assumes that the effective working time for skilled workers is 42 hours per week and for laborers is 36 hours per week. It also assumes a total of 45 workdays in a month (48 hours/week * 4.5 weeks/month). Adjustments may be needed based on actual conditions or different assumptions.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{11} \): Number of skilled workers completing the first task alone.
- \( x_{12} \): Number of teams consisting of one skilled worker and two laborers completing the first task.
- \( x_{21} \): Number of skilled workers completing the second task.
- \( x_{22} \): Number of laborers completing the second task.
- \( x_{31} \): Number of teams of five laborers completing the third task.
- \( x_{32} \): Number of teams consisting of one skilled worker and three laborers completing the third task.

### Constraints:
1. **Task Completion Time Constraints**:
   - First task: \( 42x_{11} + (42 + 2 \times 36)x_{12} \geq 10000 \)
   - Second task: \( 42x_{21} + 36x_{22} \geq 20000 \)
   - Third task: \( 5 \times 36x_{31} + (42 + 3 \times 36)x_{32} \geq 30000 \)

2. **Worker Quantity Constraints**:
   - Skilled workers: \( x_{11} + x_{12} + x_{21} + x_{32} \leq 400 \)
   - Laborers: \( 2x_{12} + x_{22} + 5x_{31} + 3x_{32} \leq 800 \)

3. **Non-Negativity Constraints**:
   - All decision variables must be non-negative: \( x_{ij} \geq 0 \) for all \( i \) and \( j \).

### Objective:
Minimize the total wage expenditure:
$$
\min Z = 100(x_{11} + x_{12} + x_{21} + x_{32}) + 80(2x_{12} + x_{22} + 5x_{31} + 3x_{32})
$$

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create a COPT environment
env = Envr()

# Create a model
model = env.createModel("WorkerAllocation")

# Add decision variables
x11 = model.addVar(vtype=COPT.INTEGER, name='x11')
x12 = model.addVar(vtype=COPT.INTEGER, name='x12')
x21 = model.addVar(vtype=COPT.INTEGER, name='x21')
x22 = model.addVar(vtype=COPT.INTEGER, name='x22')
x31 = model.addVar(vtype=COPT.INTEGER, name='x31')
x32 = model.addVar(vtype=COPT.INTEGER, name='x32')

# Set the objective function
model.setObjective(100 * (x11 + x12 + x21 + x32) + 80 * (2 * x12 + x22 + 5 * x31 + 3 * x32), COPT.MINIMIZE)

# Add constraints
model.addConstr(42 * x11 + (42 + 2 * 36) * x12 >= 10000, "Task1")
model.addConstr(42 * x21 + 36 * x22 >= 20000, "Task2")
model.addConstr(5 * 36 * x31 + (42 + 3 * 36) * x32 >= 30000, "Task3")
model.addConstr(x11 + x12 + x21 + x32 <= 400, "SkilledWorkers")
model.addConstr(2 * x12 + x22 + 5 * x31 + 3 * x32 <= 800, "Laborers")

# Solve the model
model.solve()

# Output the results
print('Optimal Total Wage Cost: {}'.format(model.ObjVal))
print('x11 = {}'.format(x11.x))
print('x12 = {}'.format(x12.x))
print('x21 = {}'.format(x21.x))
print('x22 = {}'.format(x22.x))
print('x31 = {}'.format(x31.x))
print('x32 = {}'.format(x32.x))
```

This script uses the COPTPY library to define and solve the above linear programming problem, outputting the optimal total wage cost and the values of each decision variable.

---

## Case 27  [SOLVE_FAILED]

**GT:** 13400  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
Xuri Company has signed delivery contracts for 5 products $(i=1, \cdots, 5)$ for the next year from January to June. It is known that the order quantity (in units), unit selling price (in yuan), unit cost (in yuan), and production hours required for each product are $D_i, S_i, C_i, a_i$, respectively. The normal production hours and maximum allowable overtime hours for each month from January to June are shown in Table 1-19.
Table 1-19
\begin{tabular}{c|r|r|r|r|r|r}
\hline Month & \multicolumn{1}{|c|}{1} & \multicolumn{1}{|c|}{2} & \multicolumn{1}{|c}{3} & \multicolumn{1}{|c}{4} & \multicolumn{1}{c}{5} & \multicolumn{1}{c}{6} \\
\hline Normal Production Hours $/ \mathrm{h}$ & 12000 & 11000 & 13000 & 13500 & 13500 & 14000 \\
\hline Maximum Allowable Overtime Hours $/ \mathrm{h}$ & 3000 & 2500 & 3300 & 3500 & 3500 & 3800 \\
\hline
\end{tabular}

However, the cost of each product produced during overtime hours increases by $C_i^{\prime}$ yuan. Due to production preparation and delivery requirements, product 1 is scheduled to start production in March, product 3 needs to be delivered by the end of April, and product 4 can be produced starting from February and must be fully delivered by the end of May. If products 3 and 4 are delayed in delivery, a penalty of $p_3$ yuan and $p_4$ yuan per month of delay will be imposed, respectively. All products must be delivered by the end of June. Please design a production plan for the company that guarantees completion of the contracts and maximizes profit, and establish a mathematical model.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMaximize

# Define the problem
prob = LpProblem("Xuri_Company_Profit_Maximization", LpMaximize)

# Decision variables: production quantities for each product in each month
x1_1 = LpVariable('x1_1', lowBound=0)
x2_1 = LpVariable('x2_1', lowBound=0)
x3_1 = LpVariable('x3_1', lowBound=0)
x4_1 = LpVariable('x4_1', lowBound=0)
x5_1 = LpVariable('x5_1', lowBound=0)

x1_2 = LpVariable('x1_2', lowBound=0)
x2_2 = LpVariable('x2_2', lowBound=0)
x3_2 = LpVariable('x3_2', lowBound=0)
x4_2 = LpVariable('x4_2', lowBound=0)
x5_2 = LpVariable('x5_2', lowBound=0)

x1_3 = LpVariable('x1_3', lowBound=0)
x2_3 = LpVariable('x2_3', lowBound=0)
x3_3 = LpVariable('x3_3', lowBound=0)
x4_3 = LpVariable('x4_3', lowBound=0)
x5_3 = LpVariable('x5_3', lowBound=0)

x1_4 = LpVariable('x1_4', lowBound=0)
x2_4 = LpVariable('x2_4', lowBound=0)
x3_4 = LpVariable('x3_4', lowBound=0)
x4_4 = LpVariable('x4_4', lowBound=0)
x5_4 = LpVariable('x5_4', lowBound=0)

x1_5 = LpVariable('x1_5', lowBound=0)
x2_5 = LpVariable('x2_5', lowBound=0)
x3_5 = LpVariable('x3_5', lowBound=0)
x4_5 = LpVariable('x4_5', lowBound=0)
x5_5 = LpVariable('x5_5', lowBound=0)

# Objective function: maximize profit
profit_function = lpSum([
    (S_i - C_i) * x1_j + 
    (S_i - C_i_prime) * x1_j if j == 1 else 
    (S_i - C_i) * x2_j + 
    (S_i - C_i_prime) * x2_j if j == 2 else 
    (S_i - C_i) * x3_j + 
    (S_i - C_i_prime) * x3_j if j == 3 else 
    (S_i - C_i) * x4_j + 
    (S_i - C_i_prime) * x4_j if j == 4 else 
    (S_i - C_i) * x5_j + 
    (S_i - C_i_prime) * x5_j
    for i, S_i in enumerate(S, start=1)
    for j in range(1, 6)
])
prob += profit_function

# Constraints: production hours and overtime constraints
for month in range(1, 7):
    normal_hours = Normal_Production_Hours[month-1]
    max_overtime_hours = Max_Allowable_Overtime_Hours[month-1]
    
    # Regular production constraint
    regular_production_constraint = lpSum([
        x_i_j for i, x_i_j in enumerate(x, start=1)
        if j == month and not (i == 1 and month == 3) and not (i == 2 and month == 2) and not (i == 4 and month == 5) and not (i == 5 and month == 6)
    ]) <= normal_hours
    
    # Overtime production constraint
    overtime_production_constraint = lpSum([
        x_i_j for i, x_i_j in enumerate(x, start=1)
        if j == month and (i == 1 or i == 2) and not (month == 3 and i == 1) and not (month == 4 and i == 2)
    ]) <= max_overtime_hours
    
    prob += regular_production_constraint
    prob += overtime_production_constraint

# Constraints: delivery deadlines
prob += x1_5 >= D_1 - lpSum([x_i_j for i, x_i_j in enumerate(x, start=1) if i == 1 and j == 6])
prob += x3_4 >= D_3 - lpSum([x_i_j for i, x_i_j in enumerate(x, start=1) if i == 3 and j == 4])
prob += x4_5 >= D_4 - lpSum([x_i_j for i, x_i_j in enumerate(x, start=1) if i == 4 and j == 6])

# Constraints: penalty for delayed delivery
prob += x3_2 <= D_3 - p_3 * (6 - month)
prob += x4_2 <= D_4 - p_4 * (5 - month)

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Profit: {value(prob.objective)}")
```

Please note that this code is a template and requires the following data to be filled in:
- `S`: List of unit selling prices for each product.
- `C`: List of unit costs for each product.
- `C_prime`: List of overtime cost increases for each product.
- `D`: List of order quantities for each product.
- `Normal_Production_Hours`: Normal production hours per month.
- `Max_Allowable_Overtime_Hours`: Maximum allowable overtime hours per month.
- `p_3`, `p_4`: Penalties for delayed delivery for products 3 and 4, respectively.

The code is set up to handle the constraints and objective function based on these variables.

### ORLM-8B formulation
## Mathematical Model:
To solve the production planning problem for Xuri Company, we need to construct a linear programming model to maximize profit while satisfying the constraints of production hours, delivery deadlines, and penalties. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The quantity of product \(i\) produced in month \(j\), where \(i = 1, \cdots, 5\) and \(j = 1, \cdots, 6\).
- \(d_k\): The quantity of product \(k\) delayed in delivery, where \(k = 3, 4\).

### Objective Function:
- Maximize total profit: \[Z = \sum_{i=1}^{5} \sum_{j=1}^{6} \left[ (S_i - C_i) x_{ij} - C_i' \max(0, a_i x_{ij} - \text{normal hours}_j) \right] - p_3 d_3 - 2 p_4 d_4\]

### Constraints:
1. Order fulfillment: \[\sum_{j=1}^{6} x_{ij} = D_i, \quad \forall i = 1, \cdots, 5\]
2. Production hours: \[a_i x_{ij} \leq \text{normal hours}_j + \max(0, \text{normal hours}_j + \text{overtime hours}_j - a_i x_{ij}), \quad \forall i = 1, \cdots, 5, \forall j = 1, \cdots, 6\]
3. Delivery deadline for product 1: \[x_{11} = x_{12} = 0, \quad x_{13} \geq D_1\]
4. Delivery deadline for product 3: \[x_{31} + x_{32} + x_{33} + x_{34} + x_{35} + x_{36} = D_3\]
5. Delivery deadline for product 4: \[x_{41} + x_{42} + x_{43} + x_{44} + x_{45} = D_4\]
6. Delivery deadline for product 5: \[x_{51} + x_{52} + x_{53} + x_{54} + x_{55} + x_{56} = D_5\]
7. Delivery deadline for product 4: \[x_{41} + x_{42} + x_{43} + x_{44} + x_{45} = D_4\]
8. Delivery deadline for product 3: \[x_{31} + x_{32} + x_{33} + x_{34} + x_{35} + x_{36} = D_3\]
9. Delivery deadline for product 1: \[x_{11} = x_{12} = 0, \quad x_{13} \geq D_1\]
10. Non-negativity constraints: \[x_{ij} \geq 0, \quad \forall i = 1, \cdots, 5, \forall j = 1, \cdots, 6\]
11. Non-negativity constraints: \[d_k \geq 0, \quad \forall k = 3, 4\]

### Integer Constraints:
- \(x_{ij}\) and \(d_k\) must be integers, as the quantities of products cannot be fractions.

Using this model, we can apply linear programming techniques to find the optimal production quantities for each product in each month, while satisfying all production and delivery constraints, in order to maximize total profit. This will provide Xuri Company with an economically efficient production and delivery strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the production planning problem for Xuri Company:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("XuriCompanyProduction")

# Define parameters
num_products = 5
num_months = 6
D = [0, 0, 0, 0, 0]  # Order quantity, replace with actual values
S = [0, 0, 0, 0, 0]  # Unit selling price, replace with actual values
C = [0, 0, 0, 0, 0]  # Unit cost, replace with actual values
C_prime = [0, 0, 0, 0, 0]  # Overtime cost, replace with actual values
a = [0, 0, 0, 0, 0]  # Production hours required, replace with actual values
normal_hours = [0, 0, 0, 0, 0, 0]  # Normal production hours, replace with actual values
overtime_hours = [0, 0, 0, 0, 0, 0]  # Maximum allowable overtime hours, replace with actual values
p = [0, 0]  # Penalty, replace with actual values

# Define decision variables
x = [[model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for j in range(num_months)] for i in range(num_products)]
d = [model.addVar(vtype=COPT.INTEGER, name=f"d_{k}") for k in range(2)]

# Define objective function
profit = cp.quicksum((S[i] - C[i]) * x[i][j] - C_prime[i] * cp.max(0, a[i] * x[i][j] - normal_hours[j]) for i in range(num_products) for j in range(num_months))
penalty = p[0] * d[0] + 2 * p[1] * d[1]
model.setObjective(profit - penalty, sense=COPT.MAXIMIZE)

# Add constraints
# Order fulfillment
for i in range(num_products):
    model.addConstr(cp.quicksum(x[i][j] for j in range(num_months)) == D[i], name=f"Demand_{i}")

# Production hours
for i in range(num_products):
    for j in range(num_months):
        model.addConstr(a[i] * x[i][j] <= normal_hours[j] + cp.max(0, normal_hours[j] + overtime_hours[j] - a[i] * x[i][j]), name=f"ProductionHours_{i}_{j}")

# Delivery deadline for product 1
model.addConstr(x[0][0] == 0)
model.addConstr(x[0][1] == 0)
model.addConstr(x[0][2] >= D[0])

# Delivery deadline for product 3
model.addConstr(cp.quicksum(x[2][j] for j in range(num_months)) == D[2])

# Delivery deadline for product 4
model.addConstr(cp.quicksum(x[3][j] for j in range(num_months)) == D[3])

# Delivery deadline for product 5
model.addConstr(cp.quicksum(x[4][j] for j in range(num_months)) == D[4])

# Non-negativity constraints
for i in range(num_products):
    for j in range(num_months):
        model.addConstr(x[i][j] >= 0, name=f"NonNegativity_x_{i}_{j}")
for k in range(2):
    model.addConstr(d[k] >= 0, name=f"NonNegativity_d_{k}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized profit: {:.2f}".format(model.objval))
    for i in range(num_products):
        for j in range(num_months):
            print(f"Quantity of product {i+1} produced in month {j+1}: {x[i][j].x}")
    for k in range(2):
        print(f"Quantity of product {k+3} delayed in delivery: {d[k].x}")
else:
    print("No optimal solution found.")
```

In this script, we first define the parameters of the problem, such as order quantities, unit selling prices, unit costs, overtime costs, production hours required, normal production hours, maximum allowable overtime hours, and penalties. Then, we create decision variables `x` and `d` to represent the production quantities of each product in each month and the quantity of delayed delivery for products 3 and 4.

Next, we define the objective function, which is to maximize total profit minus penalties. We add constraints to ensure order fulfillment, production hours, and delivery deadlines. Finally, we solve the model and output the results, including the maximized profit and the production quantities of each product in each month, as well as the quantity of delayed delivery for products 3 and 4.

Please note that before running this script, you need to replace the `0` values in the parameter lists with actual values. Additionally, you need to install the `coptpy` library and ensure that it is working properly.

---

## Case 28  [WRONG_FORMULATION]

**GT:** 527.9999999999999  |  **3B:** 1463.636372 (Optimal)  |  **8B:** None

### Question
Hongsheng Factory produces three types of products, I, II, and III, which all undergo processing in two steps, A and B. Step A has two machines, A1 and A2, while step B has three machines, B1, B2, and B3. It is known that product I can be processed on either type of A machine, product II can be processed on any type of A machine but can only be processed on machine B2 in step B, and product III can only be processed on machine B2 in step B. Products II and III can only be processed on machines A2 and B2 in step A and B, respectively. The processing time per unit product and other relevant data are shown in Table 1-20. How should the production plan be arranged to maximize profit for the factory?

Table 1-20
\begin{tabular}{|c|c|c|c|c|c|}
\hline \multirow{2}{*}{ Machine } & \multicolumn{3}{|c|}{ Products } & \multirow{2}{*}{ Effective Machine Hours } & \multirow{2}{*}{\begin{tabular}{c} 
Machine Processing Fee \\
/(元/h)
\end{tabular}} \\
\hline & I & II & III & & \\
\hline A1 & 5 & 10 & $2+4$ & 6000 & 0.05 \\
\hline A2 & 7 & 9 & 12 & 10000 & 0.03 \\
\hline B1 & 6 & 8 & & 4000 & 0.06 \\
\hline B2 & 4 & & 11 & 7000 & 0.11 \\
\hline B3 & 7 & & & 4000 & 0.05 \\
\hline Raw Material Cost/(元/件) & 0.25 & 0.35 & 0.50 & & \\
\hline Selling Price/(元/件) & 1.25 & 2.00 & 2.80 & & \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Hongsheng_Factory_Profit_Maximization", LpMaximize)

# Define decision variables
x1 = LpVariable('Product_I', lowBound=0, cat='Continuous')
x2 = LpVariable('Product_II', lowBound=0, cat='Continuous')
x3 = LpVariable('Product_III', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
prob += x1 * 1.25 + x2 * 2.00 + x3 * 2.80 - (x1 * 0.25 + x2 * 0.35 + x3 * 0.50)

# Constraints for machine hours and types of machines
prob += x1 * 7 + x2 * 9 + x3 * 12 <= 10000, "Machine_A2_Hours"
prob += x1 * 6 + x2 * 8 + x3 * 11 <= 7000, "Machine_B2_Hours"
prob += x1 * 5 + x2 * 10 + x3 * (4+2*1) <= 6000, "Machine_A1_Hours"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {prob.objective.value()}")
```

Note that there was a mistake in defining the constraint for `Product_III`'s processing time on machine B2. The correct value should be `1 + 4*1`, as per Table 1-20, which is `5`. I have corrected this and provided the full Python code to solve the problem using PuLP library.

### ORLM-8B formulation
## Mathematical Model:
To solve the production planning problem for Hongsheng Factory, we need to construct a linear programming model to maximize profit while satisfying the constraints of machine processing time and product processing requirements. Here is the model formulation:

### Decision Variables:
- \(x_1, x_2, x_3\): Represent the production quantities of products I, II, and III, respectively.

### Objective Function:
- Maximize total profit: \[Z = (1.25 - 0.25) x_1 + (2.00 - 0.35) x_2 + (2.80 - 0.50) x_3 - \left(0.05 \cdot 5 x_1 + 0.03 \cdot 7 x_2 + 0.11 \cdot 4 x_3\right) - \left(0.06 \cdot 6 x_2 + 0.05 \cdot 7 x_1 + 0.05 \cdot 7 x_3\right)\]

### Constraints:
1. Machine A1 processing time constraint: \[5 x_1 + 10 x_2 + 2 x_3 + 4 x_3 \leq 6000\]
2. Machine A2 processing time constraint: \[7 x_2 + 9 x_3 + 12 x_3 \leq 10000\]
3. Machine B1 processing time constraint: \[6 x_2 \leq 4000\]
4. Machine B2 processing time constraint: \[4 x_1 + 4 x_3 \leq 7000\]
5. Machine B3 processing time constraint: \[7 x_1 \leq 4000\]
6. Non-negativity constraints: \[x_1, x_2, x_3 \geq 0\]

Using this model, we can apply linear programming techniques to find the optimal production quantities for each product, maximizing total profit while satisfying the constraints of machine processing time and product processing requirements. This will provide Hongsheng Factory with an economically efficient production plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("HongshengFactoryOptimization")

# Add decision variables
x1 = model.addVar(vtype=COPT.CONTINUOUS, name="x1")  # Production quantity of product I
x2 = model.addVar(vtype=COPT.CONTINUOUS, name="x2")  # Production quantity of product II
x3 = model.addVar(vtype=COPT.CONTINUOUS, name="x3")  # Production quantity of product III

# Objective function: Maximize total profit
model.setObjective((1.00, 1.65, 2.30)[[1, 2, 3]] - (0.25, 0.35, 0.50)[[1, 2, 3]] * [x1, x2, x3]
                   - (0.05 * 5, 0.03 * 7, 0.11 * 4)[[1, 2, 3]] * [x1, x2, x3]
                   - (0.06 * 6, 0.05 * 7, 0.05 * 7)[[1, 2, 3]] * [x2, x1, x3], sense=COPT.MAXIMIZE)

# Constraints
model.addConstr(5 * x1 + 10 * x2 + 2 * x3 + 4 * x3 <= 6000, name="A1_time")
model.addConstr(7 * x2 + 9 * x3 + 12 * x3 <= 10000, name="A2_time")
model.addConstr(6 * x2 <= 4000, name="B1_time")
model.addConstr(4 * x1 + 4 * x3 <= 7000, name="B2_time")
model.addConstr(7 * x1 <= 4000, name="B3_time")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximum total profit: {:.2f} yuan".format(model.objval))
    print("Production quantity of product I: {:.2f}".format(x1.x))
    print("Production quantity of product II: {:.2f}".format(x2.x))
    print("Production quantity of product III: {:.2f}".format(x3.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables `x1`, `x2`, and `x3`, representing the production quantities of products I, II, and III, respectively. The objective function is to maximize total profit, considering the selling price, raw material cost, and machine processing fees. We add five constraints to ensure that the machine processing time limits are not exceeded. Finally, we solve the model and output the results of the optimal solution, including the maximum total profit and the production quantities of each product.

This script provides a complete example of using the `coptpy` library to solve the production planning problem for Hongsheng Factory, while satisfying all the constraints mentioned in the problem.

---

## Case 29  [WRONG_FORMULATION]

**GT:** -99999  |  **3B:** 16001.0 (Optimal)  |  **8B:** None

### Question
Jiali Company needs to recruit personnel from three different majors to work in the branch offices located in Donghai City and Nanjiang City. The demand for personnel from different majors in these two branch offices is shown in Table 4-3. After statistical analysis of the applicants, the company divides them into 6 categories, and Table 4-4 lists the majors that each category of personnel is competent in, the majors they prefer to prioritize, and the cities they prefer to work in. The company considers personnel arrangements based on the following three priorities:
$p_1$: All three types of required personnel are satisfied;
$p_2$: Among the recruited personnel, 8000 people satisfy their preferred majors;
$p_3$: Among the recruited personnel, 8000 people satisfy their preferred cities.
Based on this, establish a mathematical model for goal programming.

Table 4-3
\begin{tabular}{c|c|c}
\hline Branch Location & Major & Demand \\
\hline \multirow{3}{*}{Donghai City} & 1 & 1000 \\
& 2 & 2000 \\
\hline \multirow{4}{*}{Nanjiang City} & 3 & 1500 \\
& 1 & 2000 \\
& 2 & 1000 \\
& 3 & 1000 \\
\hline
\end{tabular}

Table 4-4
\begin{tabular}{c|c|c|c|c}
\hline Category & Personnel & Competent Majors & Preferred Majors & Preferred Cities \\
\hline 1 & 1500 & 1,2 & 1 & Donghai \\
2 & 1500 & 2,3 & 2 & Donghai \\
3 & 1500 & 1,3 & 1 & Nanjiang \\
4 & 1500 & 1,3 & 3 & Nanjiang \\
5 & 1500 & 2,3 & 3 & Donghai \\
6 & 1500 & 3 & 3 & Nanjiang \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import *

# Define the problem and variables
prob = LpProblem("Jiali_Company_Personnel_Renewal", LpMinimize)

# Decision Variables
x123 = LpVariable('x123', lowBound=0, cat='Continuous')  # Category 1 to Major 1 & 2 & 3
x456 = LpVariable('x456', lowBound=0, cat='Continuous')  # Category 4 to Major 1 & 3 & 3

# Objective Function (Minimization)
prob += (
    8000 * x123 + 8000 * x456,
    "Objective_Function"
)

# Constraints
prob += x123 >= 1000, "Donghai_Major_1_2_Constraint"
prob += x123 <= 2000, "Donghai_Major_1_2_Limitation"

prob += x456 >= 1500, "Nanjiang_Major_1_3_Constraint"
prob += x456 <= 2000, "Nanjiang_Major_1_3_Limitation"

# Priority Programming Constraints
priority1 = LpVariable('Priority1', lowBound=0, cat='Continuous')
priority2 = LpVariable('Priority2', lowBound=0, cat='Continuous')
priority3 = LpVariable('Priority3', lowBound=0, cat='Continuous')

prob += priority1 >= 1, "All_three_types_of_required_personnel_satisfied"
prob += priority2 == 8000, "8000_people_satisfy_preferred_majors"
prob += priority3 == 8000, "8000_people_satisfy_preferred_cities"

# Priority Programming Objective
prob += priority1 + priority2 + priority3

# Solve the problem
status = prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Print the values of the decision variables
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Print the objective function value
print("Objective Function Value =", value(prob.objective))
```

This code sets up a goal programming model using PuLP to address the personnel recruitment problem for Jiali Company. The model aims to satisfy all three priority goals: ensuring that all required types of personnel are satisfied, 8000 people prefer their preferred majors, and 8000 people prefer their preferred cities.

### ORLM-8B formulation
## Mathematical Model:
To solve the personnel recruitment problem for Jiali Company, we need to construct a goal programming model to minimize the total deviation of the three priorities. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The number of personnel from category \(i\) assigned to major \(j\), where \(i = 1, \ldots, 6\) and \(j = 1, 2, 3\).

### Objective Function:
- Minimize the total deviation: \[Z = p_1 d_1^- + p_2 d_2^- + p_3 d_3^- + s_1^- + s_2^- + s_3^-\]

### Constraints:
1. Personnel demand satisfaction:
   - \(x_{11} + x_{21} + x_{31} + x_{41} + x_{51} + x_{61} \geq 1000\) (Donghai City Major 1)
   - \(x_{12} + x_{22} + x_{32} + x_{42} + x_{52} + x_{62} \geq 2000\) (Donghai City Major 2)
   - \(x_{13} + x_{23} + x_{33} + x_{43} + x_{53} + x_{63} \geq 1500\) (Nanjiang City Major 3)
   - \(x_{11} + x_{12} + x_{13} \geq 2000\) (Nanjiang City Major 1)
   - \(x_{21} + x_{22} + x_{23} \geq 1000\) (Nanjiang City Major 2)
   - \(x_{31} + x_{32} + x_{33} \geq 1000\) (Nanjiang City Major 3)
2. Personnel category limits:
   - \(x_{11} + x_{12} + x_{13} \leq 1500\) (Category 1)
   - \(x_{21} + x_{22} + x_{23} \leq 1500\) (Category 2)
   - \(x_{31} + x_{32} + x_{33} \leq 1500\) (Category 3)
   - \(x_{41} + x_{42} + x_{43} \leq 1500\) (Category 4)
   - \(x_{51} + x_{52} + x_{53} \leq 1500\) (Category 5)
   - \(x_{61} + x_{62} + x_{63} \leq 1500\) (Category 6)
3. Personnel preferred major satisfaction:
   - \(x_{11} + x_{21} + x_{31} + x_{41} + x_{51} + x_{61} \geq 8000\) (Preferred Major 1)
   - \(x_{12} + x_{22} + x_{32} + x_{42} + x_{52} + x_{62} \geq 8000\) (Preferred Major 2)
   - \(x_{13} + x_{23} + x_{33} + x_{43} + x_{53} + x_{63} \geq 8000\) (Preferred Major 3)
4. Personnel preferred city satisfaction:
   - \(x_{11} + x_{21} + x_{41} + x_{51} + x_{61} \geq 8000\) (Donghai City)
   - \(x_{13} + x_{23} + x_{33} + x_{43} + x_{53} + x_{63} \geq 8000\) (Nanjiang City)

### Non-negativity Constraints:
- \(x_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply goal programming techniques to find the optimal personnel allocation that minimizes the total deviation while satisfying the demand for personnel from different majors in the branch offices and the preferences of the personnel.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("StaffAllocation")

# Define decision variables
x = model.addVars(6, 3, lb=0, vtype=COPT.INTEGER, nameprefix="x")

# Define the objective function
p1, p2, p3 = 1, 1, 1  # Priority weights, can be adjusted based on actual requirements
d1_neg, d2_neg, d3_neg = model.addVars(3, lb=0, nameprefix="d_neg")
s1_neg, s2_neg, s3_neg = model.addVars(3, lb=0, nameprefix="s_neg")
model.setObjective(p1 * d1_neg[0] + p2 * d2_neg[0] + p3 * d3_neg[0] + s1_neg[0] + s2_neg[0] + s3_neg[0], sense=COPT.MINIMIZE)

# Add constraints
# Personnel demand satisfaction
model.addConstrs((cp.quicksum(x[i, j] for i in range(6)) >= demand for j, demand in enumerate([1000, 2000, 1500, 2000, 1000, 1000])), name="DemandSatisfaction")
# Personnel category limits
model.addConstrs((cp.quicksum(x[i, j] for j in range(3)) <= 1500 for i in range(6)), name="CategoryLimits")
# Personnel preferred major satisfaction
model.addConstrs((cp.quicksum(x[i, j] for i in range(6)) >= 8000 for j in range(3)), name="PreferredMajorSatisfaction")
# Personnel preferred city satisfaction
model.addConstrs((cp.quicksum(x[i, j] for i in [0, 1, 4, 5]) >= 8000, cp.quicksum(x[i, j] for i in [2, 3, 5]) >= 8000), name="PreferredCitySatisfaction")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total deviation: {:.2f}".format(model.objval))
    for i in range(6):
        for j in range(3):
            if x[i, j].x > 0:
                print(f"Number of personnel from category {i+1} assigned to major {j+1}: {x[i, j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the decision variables `x` and set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total deviation and the number of personnel assigned to each major.

This script provides a complete example of solving the personnel recruitment problem for Jiali Company using the `coptpy` library, while satisfying all the constraints mentioned in the problem.

---

## Case 30  [SOLVE_FAILED]

**GT:** 21  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
There are $m$ production points for a certain commodity, where the output of the $i$th point $(i=1, \cdots, m)$ is $a_i$. The commodity is sold to $n$ demand points, where the required quantity at the $j$th demand point is $b_j$ $(j=1, \cdots, n)$. It is known that $\sum_i a_i \geqslant \sum_j b_j$. It is also known that when transporting from each production point to a demand point, it must go through one of the $p$ intermediate transfer stations, and if the $k$th intermediate transfer station is used, regardless of the amount of transfer, a fixed cost of $f_k$ is incurred, and the maximum capacity limit for the $k$th intermediate transfer station is $q_k$ $(k=1, \cdots, p)$. Let $c_{i k}$ and $c_{k j}$ represent the transportation costs per unit of commodity from $i$ to $k$ and from $k$ to $j$, respectively. Determine a transportation plan for the commodity that minimizes the total cost.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum

# Define problem
prob = LpProblem("Commodity_Transportation_Problem", LpMinimize)

# Parameters
m = 3  # Number of production points
n = 4  # Number of demand points
p = 2  # Number of intermediate transfer stations
f = [10, 15]  # Fixed costs for each intermediate station
q = [100, 80]  # Maximum capacities for each intermediate station
c_ij = [[3, 4], [2, 5], [1, 6]]  # Transportation cost from i to j
a = [100, 150, 200]  # Output at each production point
b = [80, 90, 70, 100]  # Demand at each demand point

# Decision variables
x_ik = [[LpVariable(f"x_{i}_{k}", lowBound=0) for k in range(p)] for i in range(m)]
y_kj = [[LpVariable(f"y_{k}_{j}", lowBound=0) for j in range(n)] for k in range(p)]

# Objective function
prob += lpSum([c_ij[i][k] * x_ik[i][k] + c_kj[k][j] * y_kj[k][j] 
               for i in range(m) for k in range(p) for j in range(n)])

# Constraints
for i in range(m):
    prob += lpSum([a[i] * x_ik[i][k] for k in range(p)] == lpSum(y_kj[k][j] for j in range(n)))

for k in range(p):
    prob += lpSum([x_ik[i][k] for i in range(m)] + lpSum(y_kj[k][j] for j in range(n)) <= q[k])

# Fixed costs
prob += lpSum(f[k] * y_kj[k][j] for k in range(p) for j in range(n))

# Solve the problem
prob.solve()
```

This code sets up a PuLP model to solve the given commodity transportation problem. The objective is to minimize the total cost of transporting the commodity from production points to demand points through intermediate transfer stations, considering fixed costs and capacity constraints.

### ORLM-8B formulation
## Mathematical Model:
To solve this transportation problem, we need to construct a mathematical model to minimize the total cost while satisfying the constraints of production point output, demand point requirements, and intermediate transfer station capacity. The model can be formulated as follows:

### Decision Variables:
- \(x_{i k}\): The amount of commodity transported from production point \(i\) to intermediate transfer station \(k\).
- \(x_{k j}\): The amount of commodity transported from intermediate transfer station \(k\) to demand point \(j\).

### Objective Function:
- Minimize the total cost: \[Z = \sum_{i=1}^{m} \sum_{k=1}^{p} c_{i k} x_{i k} + \sum_{k=1}^{p} \sum_{j=1}^{n} c_{k j} x_{k j} + \sum_{k=1}^{p} f_k\]
  - This function calculates the total cost based on the transportation costs from each production point to each intermediate transfer station, from each intermediate transfer station to each demand point, and the fixed costs of each intermediate transfer station.

### Constraints:
1. Production point output constraint: \[\sum_{k=1}^{p} x_{i k} = a_i, \forall i\]
2. Demand point requirement constraint: \[\sum_{k=1}^{p} x_{k j} = b_j, \forall j\]
3. Intermediate transfer station capacity constraint: \[\sum_{i=1}^{m} x_{i k} \leq q_k, \forall k\]
4. Total output of production points is not less than the total demand of demand points: \[\sum_{i=1}^{m} a_i \geq \sum_{j=1}^{n} b_j\]

### Non-negativity Constraints:
- \(x_{i k}, x_{k j} \geq 0, \forall i, j, k\)

Using this model, we can apply linear programming techniques to find the optimal transportation plan for the commodity that minimizes the total cost while satisfying the constraints of production point output, demand point requirements, and intermediate transfer station capacity. This will provide an economically efficient transportation strategy for the commodity.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve this transportation problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("TransportationProblem")

# Define parameters
m = ...  # Number of production points
n = ...  # Number of demand points
p = ...  # Number of intermediate transfer stations
a = [...]  # Output of each production point
b = [...]  # Required quantity at each demand point
f = [...]  # Fixed costs of each intermediate transfer station
q = [...]  # Maximum capacity of each intermediate transfer station
c_ik = [...]  # Transportation costs from each production point to each intermediate transfer station
c_kj = [...]  # Transportation costs from each intermediate transfer station to each demand point

# Add decision variables
x_ik = model.addVars(m, p, lb=0, nameprefix="x_ik")
x_kj = model.addVars(p, n, lb=0, nameprefix="x_kj")

# Objective function: Minimize total cost
objective = cp.quicksum(c_ik[i][k] * x_ik[i, k] for i in range(m) for k in range(p)) + \
            cp.quicksum(c_kj[k][j] * x_kj[k, j] for k in range(p) for j in range(n)) + \
            cp.quicksum(f[k] for k in range(p))
model.setObjective(objective, sense=COPT.MINIMIZE)

# Constraints
# Production point output constraint
for i in range(m):
    model.addConstr(cp.quicksum(x_ik[i, k] for k in range(p)) == a[i], name=f"Production_{i}")

# Demand point requirement constraint
for j in range(n):
    model.addConstr(cp.quicksum(x_kj[k, j] for k in range(p)) == b[j], name=f"Demand_{j}")

# Intermediate transfer station capacity constraint
for k in range(p):
    model.addConstr(cp.quicksum(x_ik[i, k] for i in range(m)) <= q[k], name=f"Capacity_{k}")

# Total output of production points is not less than the total demand of demand points
model.addConstr(cp.quicksum(a[i] for i in range(m)) >= cp.quicksum(b[j] for j in range(n)), name="TotalBalance")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f}".format(model.objval))
    for i in range(m):
        for k in range(p):
            if x_ik[i, k].x > 0:
                print(f"Amount of commodity transported from production point {i} to intermediate transfer station {k}: {x_ik[i, k].x}")
    for k in range(p):
        for j in range(n):
            if x_kj[k, j].x > 0:
                print(f"Amount of commodity transported from intermediate transfer station {k} to demand point {j}: {x_kj[k, j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first define the parameters of the problem, including the number of production points, demand points, intermediate transfer stations, output of each production point, required quantity at each demand point, fixed costs of each intermediate transfer station, maximum capacity of each intermediate transfer station, and transportation costs.

Then, we add decision variables `x_ik` and `x_kj`, representing the amount of commodity transported from each production point to each intermediate transfer station and from each intermediate transfer station to each demand point, respectively.

Next, we define the objective function, which is to minimize the total cost, including transportation costs and fixed costs.

We also add constraints, including production point output constraints, demand point requirement constraints, intermediate transfer station capacity constraints, and the constraint that the total output of production points is not less than the total demand of demand points.

Finally, we solve the model and output the results, including the minimum total cost and the specific transportation plan.

Please note that in the script, you need to replace `...` with specific values and fill in the `a`, `b`, `f`, `q`, `c_ik`, and `c_kj` lists with specific data.

---

## Case 31  [SOLVE_FAILED]

**GT:** 1000.0  |  **3B:** 0.0 (Unbounded)  |  **8B:** None

### Question
There are 10 different parts that can be processed on equipment A, equipment B, or equipment C, with the processing costs per unit shown in Table 5-6. Furthermore, as long as parts are processed on the mentioned equipment, regardless of processing one or multiple parts, the one-time setup costs are $d_A$, $d_B$, and $d_C$ respectively. If the following requirements are to be met:
(1) Each of the 10 parts should be processed once.
(2) If the first part is processed on equipment A, then the second part should be processed on equipment B or C. Conversely, if the first part is processed on equipment B or C, then the second part should be processed on equipment A.
(3) Parts 3, 4, and 5 must be processed on equipment A, B, and C respectively.
(4) The number of parts processed on equipment C should not exceed 3.
Please establish an integer programming mathematical model for this problem, with the objective of minimizing the total cost.

Table 5-6
\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|}
\hline Equipment $\quad$ Part & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 \\
\hline A & $a_1$ & $a_2$ & $a_3$ & $a_4$ & $a_5$ & $a_6$ & $a_7$ & $a_8$ & $a_9$ & $a_{10}$ \\
\hline B & $b_1$ & $b_2$ & $b_3$ & $b_4$ & $b_5$ & $b_6$ & $b_7$ & $b_8$ & $b_9$ & $b_{10}$ \\
\hline C & $c_1$ & $c_2$ & $c_3$ & $c_4$ & $c_5$ & $c_6$ & $c_7$ & $c_8$ & $c_9$ & $c_{10}$ \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Define the problem
prob = LpProblem("Part_Processing_Model", LpMinimize)

# Parameters
a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 = 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = 15, 25, 35, 45, 55, 65, 75, 85, 95, 105
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = 20, 30, 40, 50, 60, 70, 80, 90, 100, 110
d_A, d_B, d_C = 100, 150, 200

# Decision variables
x = {i: LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(1, 11)}

# Constraints
prob += x[3] == 1, "Part_3_on_A"
prob += x[4] == 1, "Part_4_on_B"
prob += x[5] == 1, "Part_5_on_C"
prob += lpSum([x[i] for i in range(1, 11) if i != 2 and i != 3]) <= 3, "Max_parts_C"

# Objective function
for part in range(1, 11):
    prob += x[part] * (a1 if part == 1 else b1 if part == 2 else c1), f"Part_{part}_on_A"
prob += lpSum([x[i] * (b2 if i == 3 else a2 if i == 4 else c2) for i in range(5, 8)]) + \
        lpSum([x[j] * (c3 if j == 9 else b3 if j == 10 else a3) for j in range(8, 11)]) - \
        lpSum([x[k] * (d_A if k < 2 or k > 4 else d_B if k >= 5 and k <= 7 else d_C) for k in range(1, 11)])

# Solve the problem
prob.solve()

# Print the results
for part in x:
    print(f"x[{part}] = {x[part].varValue}")
print("Total Cost:", value(prob.objective))
```

This code sets up and solves an integer programming model using PuLP to minimize the total cost of processing 10 parts on equipment A, B, or C. The constraints ensure that each part is processed exactly once, certain parts are assigned to specific machines based on their sequence, and the number of parts processed on machine C does not exceed a specified limit.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of part processing on equipment, we need to construct an integer programming model to minimize the total cost while satisfying the processing requirements and equipment constraints. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): If part \(j\) is processed on equipment \(i\), then \(x_{ij} = 1\); otherwise, \(x_{ij} = 0\). Here, \(i \in \{A, B, C\}\) and \(j \in \{1, 2, ..., 10\}\).

### Objective Function:
- Minimize the total cost: \[Z = \sum_{i \in \{A, B, C\}} \sum_{j=1}^{10} c_{ij} x_{ij} + d_A \delta_A + d_B \delta_B + d_C \delta_C\]
  where \(c_{ij}\) is the cost of processing part \(j\) on equipment \(i\), and \(\delta_i\) is a binary variable indicating whether equipment \(i\) is used.

### Constraints:
1. Each part can only be processed on one equipment:
   - \(\sum_{i \in \{A, B, C\}} x_{ij} = 1, \forall j \in \{1, 2, ..., 10\}\)
2. If the first part is processed on equipment A, then the second part should be processed on equipment B or C, and vice versa:
   - \(x_{A1} + x_{B2} + x_{C2} = 1\)
   - \(x_{B1} + x_{C1} + x_{A2} = 1\)
3. Parts 3, 4, and 5 must be processed on equipment A, B, and C respectively:
   - \(x_{A3} = 1\)
   - \(x_{B4} = 1\)
   - \(x_{C5} = 1\)
4. The number of parts processed on equipment C should not exceed 3:
   - \(\sum_{j=1}^{10} x_{Cj} \leq 3\)
5. Binary variable constraints:
   - \(\delta_i = \sum_{j=1}^{10} x_{ij}, \forall i \in \{A, B, C\}\)
   - \(\delta_i \leq 1, \forall i \in \{A, B, C\}\)

### Non-negativity and Integer Constraints:
- \(x_{ij} \in \{0, 1\}\), for all \(i \in \{A, B, C\}\) and \(j \in \{1, 2, ..., 10\}\).

Using this model, we can apply integer programming techniques to find the optimal solution for processing each part on the corresponding equipment, minimizing the total cost while satisfying all the processing requirements and equipment constraints. This will provide the company with an economically efficient part processing strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("PartProcessingOptimization")

# Define the processing costs and setup costs
processing_costs = {
    'A': [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10],
    'B': [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10],
    'C': [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
}
setup_costs = {'A': d_A, 'B': d_B, 'C': d_C}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.BINARY, name=f"x_{i}{j}") for i in processing_costs for j in range(1, 11)}
delta = {i: model.addVar(vtype=COPT.BINARY, name=f"delta_{i}") for i in setup_costs}

# Objective function: Minimize the total cost
model.setObjective(cp.quicksum(processing_costs[i][j-1] * x[i, j] for i in processing_costs for j in range(1, 11)) +
                   cp.quicksum(setup_costs[i] * delta[i] for i in setup_costs), sense=COPT.MINIMIZE)

# Constraints
# Each part can only be processed on one equipment
for j in range(1, 11):
    model.addConstr(cp.quicksum(x[i, j] for i in processing_costs) == 1, name=f"Part_{j}")

# If the first part is processed on equipment A, then the second part should be processed on equipment B or C, and vice versa
model.addConstr(x['A', 1] + x['B', 2] + x['C', 2] == 1, name="Equipment_A")
model.addConstr(x['B', 1] + x['C', 1] + x['A', 2] == 1, name="Equipment_B")

# Parts 3, 4, and 5 must be processed on equipment A, B, and C respectively
model.addConstr(x['A', 3] == 1, name="Part_3_on_A")
model.addConstr(x['B', 4] == 1, name="Part_4_on_B")
model.addConstr(x['C', 5] == 1, name="Part_5_on_C")

# The number of parts processed on equipment C should not exceed 3
model.addConstr(cp.quicksum(x['C', j] for j in range(1, 11)) <= 3, name="Limit_C")

# Binary variable constraints
for i in setup_costs:
    model.addConstr(delta[i] == cp.quicksum(x[i, j] for j in range(1, 11)), name=f"Delta_{i}_def")
    model.addConstr(delta[i] <= 1, name=f"Delta_{i}_ub")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f}".format(model.objval))
    for i in processing_costs:
        for j in range(1, 11):
            if x[i, j].x > 0.5:
                print(f"Part {j} processed on Equipment {i}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the processing costs and setup costs, and add the decision variables `x` and `delta`. Next, we set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total cost and the processing of each part on the corresponding equipment.

This script provides a complete example of using the `coptpy` library to solve the part processing problem, while satisfying all the constraints mentioned in the problem.

---

## Case 32  [SOLVE_FAILED]

**GT:** 770.0  |  **3B:** 140.0 (Infeasible)  |  **8B:** None

### Question
Changjiang Comprehensive Shopping Mall has an area of $5000 \mathrm{~m}^2$ for rent and plans to attract tenants from the following 5 types of stores. It is known the area occupied by each store, the minimum and maximum number of stores to be opened in the mall, and the annual expected profit (in ten thousand yuan) for each store at different numbers of stores opened, as shown in Table 5-12. Each store is required to pay the mall 20% of their annual profit as rent. What is the optimal number of each type of store the mall should rent in order to maximize the total rental income?

Table 5-12:
\begin{tabular}{c|c|c|c|c|c|c|c}
\hline 
\multirow{2}{*}{Code} & \multirow{2}{*}{Store Type} & Store Area $/ \mathrm{m}^2$ & \multicolumn{2}{|c|}{Number of Stores} & \multicolumn{3}{|c}{Profit per Store at Different Numbers} \\
\cline{3-8} 
& & & Minimum & Maximum & 1 & 2 & 3 \\
\hline 
1 & Jewelry & 250 & 1 & 3 & 9 & 8 & 7 \\
2 & Shoes and Hats & 350 & 1 & 2 & 10 & 9 & - \\
3 & Department Store & 800 & 1 & 3 & 27 & 21 & 20 \\
4 & Bookstore & 400 & 0 & -2 & 16 & 10 & - \\
5 & Restaurant & 500 & 1 & 3 & 17 & 15 & 12 \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Changjiang_Mall_Rental_Problem", LpMaximize)

# Define decision variables
x1, x2, x3, x4, x5 = LpVariable('Jewelry', lowBound=0, cat='Continuous'), \
                      LpVariable('Shoes_and_Hats', lowBound=0, cat='Continuous'), \
                      LpVariable('Department_Store', lowBound=0, cat='Continuous'), \
                      LpVariable('Bookstore', lowBound=0, cat='Continuous'), \
                      LpVariable('Restaurant', lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
objective = 9*x1 + 8*x2 + 27*x3 + 16*x4 + 17*x5 - (0.2*(9*x1 + 8*x2 + 27*x3 + 16*x4 + 17*x5))
prob += objective

# Constraints
constraints = [
    x1 >= 1, x1 <= 3,
    x2 >= 1, x2 <= 2,
    x3 >= 1, x3 <= 3,
    x4 >= 0, x4 <= -2,
    x5 >= 1, x5 <= 3
]

for constraint in constraints:
    prob += constraint

# Solve the problem
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Profit = ", value(prob.objective))
```

Please note that the formulation of this model is somewhat unconventional due to the presence of a negative number for `Bookstore` (x4) and the constraint x4 >= 0, x4 <= -2 which seems contradictory. In practical terms, it might be more appropriate to exclude or modify such constraints if they are not feasible in real-world scenarios.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem of renting stores in the Changjiang Comprehensive Shopping Mall, we need to construct a mathematical model to maximize the total rental income while satisfying the constraints of store area and number. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The number of stores of type \(i\) opened, where \(i\) represents the store type (1 to 5) and \(j\) represents the number of stores opened (1, 2, or 3).

### Objective Function:
- Maximize the total rental income: \[Z = \sum_{i=1}^{5} \sum_{j=1}^{3} (x_{ij} \cdot \text{Profit}_{ij} \cdot 0.2)\]
  - This function calculates the total rental income based on the number of stores opened for each store type and their respective annual profits.

### Constraints:
1. Store area constraint: \[\sum_{i=1}^{5} \sum_{j=1}^{3} (x_{ij} \cdot \text{Area}_i) \leq 5000\]
   - This ensures that the total area occupied by all stores does not exceed the area of the mall.
2. Store number constraint: \[\text{Minimum}_i \leq \sum_{j=1}^{3} x_{ij} \leq \text{Maximum}_i, \quad \forall i\]
   - This ensures that the number of stores opened for each store type is between the minimum and maximum values.

### Non-negativity and Integer Constraints:
- \(x_{ij} \geq 0\) and must be integers, as the number of stores must be integers.

Using this model, we can apply integer linear programming techniques to find the optimal number of each store type to rent, maximizing the total rental income while satisfying the constraints of store area and number. This will provide the Changjiang Comprehensive Shopping Mall with an optimized store rental strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the optimization problem of renting stores in the Changjiang Comprehensive Shopping Mall:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ChangjiangMallRentalOptimization")

# Store types and related parameters
store_types = {
    1: {'area': 250, 'min': 1, 'max': 3, 'profits': [9, 8, 7]},
    2: {'area': 350, 'min': 1, 'max': 2, 'profits': [10, 9, -]},
    3: {'area': 800, 'min': 1, 'max': 3, 'profits': [27, 21, 20]},
    4: {'area': 400, 'min': 0, 'max': -2, 'profits': [16, 10, -]},
    5: {'area': 500, 'min': 1, 'max': 3, 'profits': [17, 15, 12]}
}

# Mall area
mall_area = 5000

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for i in store_types for j in range(1, len(store_types[i]['profits']) + 1)}

# Objective function: Maximize total rental income
model.setObjective(cp.quicksum(x[(i, j)] * store_types[i]['profits'][j-1] * 0.2 for i in store_types for j in range(1, len(store_types[i]['profits']) + 1)), sense=COPT.MAXIMIZE)

# Constraints
# Store area constraint
model.addConstr(cp.quicksum(x[(i, j)] * store_types[i]['area'] for i in store_types for j in range(1, len(store_types[i]['profits']) + 1)) <= mall_area, name="AreaConstraint")

# Store number constraint
for i in store_types:
    model.addConstr(cp.quicksum(x[(i, j)] for j in range(1, len(store_types[i]['profits']) + 1)) >= store_types[i]['min'], name=f"MinConstraint_{i}")
    model.addConstr(cp.quicksum(x[(i, j)] for j in range(1, len(store_types[i]['profits']) + 1)) <= store_types[i]['max'], name=f"MaxConstraint_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total rental income: {:.2f} ten thousand yuan".format(model.objval))
    for i in store_types:
        for j in range(1, len(store_types[i]['profits']) + 1):
            if x[(i, j)].x > 0:
                print(f"Number of stores of type {i} opened: {x[(i, j)].x}")
else:
    print("No optimal solution found.")
```

In this script, we first define the store types and their related parameters, including the store area, minimum and maximum number of stores, and the annual expected profit for each store at different numbers of stores opened. Then, it creates decision variables `x` representing the number of stores opened for each store type.

The objective function is to maximize the total rental income, which is the sum of the number of stores opened for each store type multiplied by their respective annual profits and 20% rent.

The constraints include the store area constraint and the store number constraint. The store area constraint ensures that the total area occupied by all stores does not exceed the area of the mall, and the store number constraint ensures that the number of stores opened for each store type is between the minimum and maximum values.

Finally, the script solves the model and outputs the maximized total rental income and the optimal number of stores opened for each store type.

---

## Case 33  [WRONG_FORMULATION]

**GT:** 32.436  |  **3B:** 25.511363699999997 (Optimal)  |  **8B:** None

### Question
Suppose an animal needs at least $700 \mathrm{~g}$ of protein, $30 \mathrm{~g}$ of minerals, and $100 \mathrm{mg}$ of vitamins per day. There are 5 types of feed to choose from, and the contents of each nutrient per gram and the unit price of each feed are shown in Table 1-5. Try to establish a linear programming model that not only meets the animal's growth needs but also minimizes the cost of selecting feed.

Table 1-6
\begin{tabular}{|c|c|c|c|c||c|c|c|c|c|}
\hline Feed & \begin{tabular}{c} 
Protein \\
$/ \mathrm{g}$
\end{tabular} & \begin{tabular}{c} 
Minerals \\
$/ \mathrm{g}$
\end{tabular} & \begin{tabular}{c} 
Vitamins \\
$/ \mathrm{mg}$
\end{tabular} & \begin{tabular}{c} 
Price \\
$/$ (yuan $/ \mathrm{kg})$
\end{tabular} & Feed & \begin{tabular}{c} 
Protein \\
$/ \mathrm{g}$
\end{tabular} & \begin{tabular}{c} 
Minerals \\
$/ \mathrm{g}$
\end{tabular} & \begin{tabular}{c} 
Vitamins \\
$/ \mathrm{mg}$
\end{tabular} & \begin{tabular}{c} 
Price \\
$/($ yuan $/ \mathrm{kg})$
\end{tabular} \\
\hline 1 & 3 & 1 & 0.5 & 0.2 & 4 & 6 & 2 & 2 & 0.3 \\
\hline 2 & 2 & 0.5 & 1 & 0.7 & 5 & 18 & 0.5 & 0.8 & 0.8 \\
\hline 3 & 1 & 0.2 & 0.2 & 0.4 & & & & & \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Define the problem as a minimization problem
prob = LpProblem("Feed_Selection_Problem", LpMinimize)

# Define decision variables (amount of each feed to use)
x1, x2, x3, x4, x5 = LpVariable('x1', lowBound=0), LpVariable('x2', lowBound=0), LpVariable('x3', lowBound=0), LpVariable('x4', lowBound=0), LpVariable('x5', lowBound=0)

# Define the objective function (minimize cost)
prob += lpSum([0.2*x1 + 0.7*x2 + 0.4*x4 + 0.3*x5]), "Total_Cost"

# Constraints for protein, minerals, and vitamins
prob += 3*x1 + 6*x2 + 18*x4 + 4*x5 >= 700, "Protein_Constraint"
prob += x1 + 2*x2 + 0.5*x4 + 2*x5 >= 30, "Minerals_Constraint"
prob += 0.5*x2 + 0.2*x4 + 2*x5 >= 100, "Vitamins_Constraint"

# Solve the problem
prob.solve()

# Print the results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Cost = ", value(prob.objective))
```

This code sets up a linear programming model to minimize the cost of selecting feed while ensuring that the animal meets its daily requirements for protein, minerals, and vitamins. The decision variables represent the amount of each type of feed used, and constraints ensure that these amounts meet the nutritional needs.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
Let \(x_i\) be the number of kilograms of feed \(i\) chosen, where \(i = 1, 2, \ldots, 5\).

### Objective Function:
Minimize the total cost: \(\min z = 0.2x_1 + 0.7x_2 + 0.4x_3 + 0.3x_4 + 0.8x_5\)

### Constraints:
1. Protein requirement: \(3x_1 + 2x_2 + x_3 + 6x_4 + 18x_5 \geq 700\)
2. Mineral requirement: \(x_1 + 0.5x_2 + 0.2x_3 + 2x_4 + 0.5x_5 \geq 30\)
3. Vitamin requirement: \(0.5x_1 + x_2 + 0.2x_3 + 2x_4 + 0.8x_5 \geq 100\)
4. Non-negativity constraint: \(x_i \geq 0, \quad i = 1, 2, \ldots, 5\)

## Python Code Solution Using `coptpy`:
```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("FeedOptimization")

# Add decision variables
x = model.addVars(5, lb=0, name="x")

# Objective function: Minimize total cost
model.setObjective(0.2 * x[0] + 0.7 * x[1] + 0.4 * x[2] + 0.3 * x[3] + 0.8 * x[4], sense=COPT.MINIMIZE)

# Constraints
model.addConstr(3 * x[0] + 2 * x[1] + x[2] + 6 * x[3] + 18 * x[4] >= 700, name="ProteinRequirement")
model.addConstr(x[0] + 0.5 * x[1] + 0.2 * x[2] + 2 * x[3] + 0.5 * x[4] >= 30, name="MineralRequirement")
model.addConstr(0.5 * x[0] + x[1] + 0.2 * x[2] + 2 * x[3] + 0.8 * x[4] >= 100, name="VitaminRequirement")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} yuan".format(model.objval))
    for i in range(5):
        print(f"Feed {i+1} chosen: {x[i].x:.2f} kg")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables `x` to represent the number of kilograms of each feed chosen. The objective function is to minimize the total cost, calculated by multiplying the unit price of each feed by the corresponding decision variable and summing them.

We add three constraints to ensure that the animal's protein, mineral, and vitamin requirements are met. Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the number of kilograms of each feed chosen.

This script provides a complete example of using the `coptpy` library to solve the feed selection problem, while satisfying all the constraints mentioned in the problem.

---

## Case 34  [WRONG_FORMULATION]

**GT:** 1146.6  |  **3B:** 766.6666589999999 (Optimal)  |  **8B:** None

### Question
A factory produces three types of products: I, II, and III. Each product requires two processing steps, A and B. The factory has two types of equipment for step A, represented by A1 and A2, and three types of equipment for step B, represented by B1, B2, and B3. Product I can be processed on any type of A equipment and any type of B equipment. Product II can be processed on any type of A equipment, but for step B, it can only be processed on B1 equipment. Product III can only be processed on A2 and B2 equipment. The unit processing time, raw material cost, selling price, equipment available time, and equipment cost at full load for each type of equipment are shown in Table 1-18. Determine the optimal production plan to maximize the profit for the factory.

Table 1-18
\begin{tabular}{c|c|c|c|c|c}
\hline \multirow{2}{*}{ Equipment } & \multicolumn{3}{|c|}{ Product } & \multirow{2}{*}{ Equipment Available Time } & \multirow{2}{*}{\begin{tabular}{c} 
Equipment Cost at \\
Full Load (CNY)
\end{tabular}} \\
\cline { 2 - 4 } & I & II & III & 6000 & 300 \\
$A_1$ & 5 & 10 & & 10000 & 321 \\
$A_2$ & 7 & 9 & 12 & 4000 & 250 \\
$B_1$ & 6 & 8 & & 7000 & 783 \\
$B_2$ & 4 & & 11 & 4000 & 200 \\
$B_3$ & 7 & & & & \\
\hline Raw Material Cost (CNY / unit) & 0.25 & 0.35 & 0.50 & & \\
Unit Price (CNY / unit) & 1.25 & 2.00 & 2.80 & & \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Factory_Optimization_Problem", LpMaximize)

# Decision variables: x1, x2, x3 for products I, II, III respectively
x1 = LpVariable('Product_I', lowBound=0, cat='Continuous')
x2 = LpVariable('Product_II', lowBound=0, cat='Continuous')
x3 = LpVariable('Product_III', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
prob += x1*1.25 + x2*2.00 + x3*2.80 - x1*0.25 - x2*0.35 - x3*0.50

# Constraints for equipment A1, A2, B1, B2, and B3
prob += 5*x1 + 7*x2 + 4*x3 <= 10000, "A1_Constraint"
prob += 10*x1 + 9*x2 + 6*x3 <= 10000, "A2_Constraint"
prob += 6*x1 + 8*x2 + 7*x3 <= 7000, "B1_Constraint"
prob += 4*x1 + x2 + 11*x3 <= 4000, "B2_Constraint"
prob += 7*x1 + 9*x2 + 12*x3 <= 4000, "B3_Constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Optimal Profit: {prob.objective.value()}")
```

This code sets up a linear programming model to maximize profit for the factory given the constraints of available equipment and raw material costs. The decision variables represent the number of units produced for each product, and the objective function calculates the total profit by subtracting the raw material cost from the selling price. Constraints are set based on the processing requirements for each type of equipment.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
Let \(x_{ij}\) represent the production quantity of product \(i\) on equipment \(j\), where \(i = 1, 2, 3\) corresponds to products I, II, and III, and \(j = 1, 2, 3, 4, 5\) corresponds to equipment \(A_1, A_2, B_1, B_2, B_3\).

### Objective Function:
Maximize the total profit:
\[
\max Z = \sum_{i=1}^3 \sum_{j=1}^5 \left( (v_i - c_i) x_{ij} - t_{ij} x_{ij} \right) - \sum_{j=1}^2 C_j
\]
where \(v_i\) is the selling price of product \(i\), \(c_i\) is the raw material cost of product \(i\), \(t_{ij}\) is the unit processing time of product \(i\) on equipment \(j\), and \(C_j\) is the equipment cost at full load for equipment \(j\).

### Constraints:
1. Equipment available time constraints:
   \[
   \sum_{i=1}^3 t_{ij} x_{ij} \leq T_j, \quad j = 1, 2, 3, 4, 5
   \]
   where \(T_j\) is the equipment available time for equipment \(j\).

2. Product production constraints:
   \[
   \sum_{j=1}^5 x_{ij} \geq P_i, \quad i = 1, 2, 3
   \]
   where \(P_i\) is the minimum production quantity for product \(i\).

3. Non-negativity constraints:
   \[
   x_{ij} \geq 0, \quad \forall i, \forall j
   \]

## Python Code Solution Using `coptpy`:
```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionOptimization")

# Define the data
products = ['I', 'II', 'III']
machines = ['A1', 'A2', 'B1', 'B2', 'B3']
processing_times = {
    'I': [5, 7, 6, 4, 7],
    'II': [10, 9, 8, None, None],
    'III': [None, 12, None, 11, None]
}
available_times = [10000, 4000, 7000, 4000, None]
equipment_costs = [321, 250, 783, 200, None]
min_production = {'I': 100, 'II': 50, 'III': 75}
unit_price = {'I': 1.25, 'II': 2.00, 'III': 2.80}
material_cost = {'I': 0.25, 'II': 0.35, 'III': 0.50}

# Add decision variables
x = model.addVars(products, machines, lb=0, nameprefix="x")

# Objective function: Maximize total profit
model.setObjective(
    cp.quicksum((unit_price[i] - material_cost[i]) * x[i, j] - processing_times[i][machines.index(j)] * x[i, j]
                for i in products for j in machines if processing_times[i][machines.index(j)] is not None)
    - cp.quicksum(equipment_costs[machines.index(j)] for j in [machines[i] for i in range(len(machines)) if i < len(equipment_costs)]),
    sense=COPT.MAXIMIZE
)

# Constraints
# Equipment available time constraints
for j in range(len(machines)):
    model.addConstr(
        cp.quicksum(processing_times[i][j] * x[i, machines[j]] for i in products if processing_times[i][j] is not None)
        <= available_times[j],
        name=f"MachineTime_{machines[j]}"
    )

# Product production constraints
for i in products:
    model.addConstr(
        cp.quicksum(x[i, j] for j in machines if processing_times[i][machines.index(j)] is not None)
        >= min_production[i],
        name=f"Production_{i}"
    )

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximum total profit: {:.2f} CNY".format(model.objval))
    for i in products:
        for j in machines:
            if x[i, j].x > 0:
                print(f"Production quantity of product {i} on equipment {j}: {x[i, j].x:.2f} units")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the data for the problem, including the products, machines, processing times, available times, equipment costs, minimum production quantities, unit prices, and material costs. Next, we add the decision variables `x` and set the objective function to maximize the total profit. We also add constraints for the equipment available times and product production quantities. Finally, we solve the model and output the results of the optimal solution, including the maximum total profit and the production quantities of each product on each equipment.

---

## Case 35  [SOLVE_FAILED]

**GT:** 4500  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A certain brand of wine is made by blending three grades of wine. The daily supply and unit cost of these three grades of wine are shown in Table 4-8.
Table 4-8
\begin{tabular}{c|c|c}
\hline Grade & Daily Supply (kg) & Cost (元/kg) \\
\hline I & 1500 & 6 \\
I & 2000 & 4.5 \\
II & 1000 & 3 \\
\hline
\end{tabular}

Assume that there are three brands (red, yellow, blue) for this type of wine, and the blending ratios and selling prices for each brand are shown in Table 4-9. The decision maker specifies that the wines for each brand must be blended strictly according to the specified ratios, followed by maximizing profit, and ensuring that the red brand produces at least 2000 kg per day. Formulate the mathematical model.
Table 4-9
\begin{tabular}{c|c|c}
\hline Brand & Blending Requirements & Selling Price (元/kg) \\
\hline Red & \begin{tabular}{l} 
I less than 10\% \\
I more than 50\%
\end{tabular} & 5.5 \\
\hline Yellow & \begin{tabular}{l} 
II less than 70\% \\
I more than 20\%
\end{tabular} & 5.0 \\
\hline Blue & \begin{tabular}{l} 
I less than 50\% \\
I more than 10\%
\end{tabular} & 4.8 \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpMaximize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Wine_Blending_Problem", LpMaximize)

# Define decision variables
x1_red = LpVariable('Red_I', lowBound=0)
x2_red = LpVariable('Red_II', lowBound=0)
x3_red = LpVariable('Red_III', lowBound=0)

x1_yellow = LpVariable('Yellow_I', lowBound=0)
x2_yellow = LpVariable('Yellow_II', lowBound=0)
x3_yellow = LpVariable('Yellow_III', lowBound=0)

x1_blue = LpVariable('Blue_I', lowBound=0)
x2_blue = LpVariable('Blue_II', lowBound=0)
x3_blue = LpVariable('Blue_III', lowBound=0)

# Objective function: Maximize profit
prob += lpSum([5.5*x1_red + 5.0*x1_yellow + 4.8*x1_blue,
               5.5*x2_red + 5.0*x2_yellow + 4.8*x2_blue,
               5.5*x3_red + 5.0*x3_yellow + 4.8*x3_blue])

# Constraints
prob += x1_red >= 0.1 * (x1_red + x2_red + x3_red), "Red_I_constraint"
prob += x1_red <= 0.5 * (x1_red + x2_red + x3_red), "Red_I_more_than_50_constraint"

prob += x1_yellow >= 0.7 * (x1_yellow + x2_yellow + x3_yellow), "Yellow_II_constraint"
prob += x1_yellow > 0.2 * (x1_yellow + x2_yellow + x3_yellow), "Yellow_I_more_than_20_constraint"

prob += x1_blue <= 0.5 * (x1_blue + x2_blue + x3_blue), "Blue_I_constraint_less_than_50"
prob += x1_blue > 0.1 * (x1_blue + x2_blue + x3_blue), "Blue_I_more_than_10_constraint"

# Daily supply constraints
prob += x1_red + x2_red + x3_red <= 1500, "Red_supply_constraint"
prob += x1_yellow + x2_yellow + x3_yellow <= 1000, "Yellow_supply_constraint"
prob += x1_blue + x2_blue + x3_blue <= 2000, "Blue_supply_constraint"

# Red brand production constraint
prob += x1_red + x2_red + x3_red >= 2000, "Red_production_constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {value(prob.objective)}")
```

This code sets up and solves a linear programming model using PuLP to maximize profit for blending three grades of wine into three different brands (Red, Yellow, Blue) while adhering to specified constraints.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of maximizing profit for the brand of wine, we need to construct a linear programming model to determine the optimal blending ratios for each brand of wine. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The amount of grade \(j\) wine used for brand \(i\) (in kg), where \(i\) represents the brand (red, yellow, blue) and \(j\) represents the grade (I, I, II).

### Objective Function:
- Maximize total profit: \[Z = \sum_{i \in \{red, yellow, blue\}} \left( \text{selling price}_i \times \sum_{j \in \{I, I, II\}} x_{ij} - \sum_{j \in \{I, I, II\}} (\text{cost}_j \times x_{ij}) \right)\]

### Constraints:
1. Supply constraints for each grade of wine:
   - \(\sum_{i \in \{red, yellow, blue\}} x_{iI} \leq 1500\)
   - \(\sum_{i \in \{red, yellow, blue\}} x_{iI} \leq 2000\)
   - \(\sum_{i \in \{red, yellow, blue\}} x_{iII} \leq 1000\)
2. Blending ratio constraints for each brand of wine:
   - Red brand: \(x_{I, \text{red}} \leq 0.1 \times \sum_{j \in \{I, I, II\}} x_{j, \text{red}}\), \(x_{I, \text{red}} \geq 0.5 \times \sum_{j \in \{I, I, II\}} x_{j, \text{red}}\)
   - Yellow brand: \(x_{II, \text{yellow}} \leq 0.7 \times \sum_{j \in \{I, I, II\}} x_{j, \text{yellow}}\), \(x_{I, \text{yellow}} \geq 0.2 \times \sum_{j \in \{I, I, II\}} x_{j, \text{yellow}}\)
   - Blue brand: \(x_{I, \text{blue}} \leq 0.5 \times \sum_{j \in \{I, I, II\}} x_{j, \text{blue}}\), \(x_{I, \text{blue}} \geq 0.1 \times \sum_{j \in \{I, I, II\}} x_{j, \text{blue}}\)
3. Minimum production requirement for the red brand:
   - \(\sum_{j \in \{I, I, II\}} x_{j, \text{red}} \geq 2000\)

### Non-negativity constraints:
- \(x_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply linear programming techniques to find the optimal blending ratios for each brand of wine, maximizing total profit while satisfying the supply constraints for each grade of wine and the blending ratio constraints for each brand. This will provide the brand of wine with an economically efficient production and sales strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("WineBlendingOptimization")

# Define the brands and grades
brands = ['red', 'yellow', 'blue']
grades = ['I', 'I', 'II']

# Define the supply and cost
supply = {'I': 1500, 'I': 2000, 'II': 1000}
cost = {'I': 6, 'I': 4.5, 'II': 3}

# Define the selling price
price = {'red': 5.5, 'yellow': 5.0, 'blue': 4.8}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.CONTINUOUS, name=f"x_{i}_{j}") for i in brands for j in grades}

# Objective function: Maximize total profit
model.setObjective(cp.quicksum(price[i] * cp.quicksum(x[i, j] for j in grades) - 
                               cp.quicksum(cost[j] * x[i, j] for j in grades) for i in brands), 
                   sense=COPT.MAXIMIZE)

# Constraints
# Supply constraints for each grade of wine
for j in grades:
    model.addConstr(cp.quicksum(x[i, j] for i in brands) <= supply[j], name=f"Supply_{j}")

# Blending ratio constraints for each brand of wine
model.addConstr(x['I', 'red'] <= 0.1 * cp.quicksum(x['red', j] for j in grades), name="Blend_Red_I_Lower")
model.addConstr(x['I', 'red'] >= 0.5 * cp.quicksum(x['red', j] for j in grades), name="Blend_Red_I_Upper")
model.addConstr(x['II', 'yellow'] <= 0.7 * cp.quicksum(x['yellow', j] for j in grades), name="Blend_Yellow_II_Lower")
model.addConstr(x['I', 'yellow'] >= 0.2 * cp.quicksum(x['yellow', j] for j in grades), name="Blend_Yellow_I_Upper")
model.addConstr(x['I', 'blue'] <= 0.5 * cp.quicksum(x['blue', j] for j in grades), name="Blend_Blue_I_Lower")
model.addConstr(x['I', 'blue'] >= 0.1 * cp.quicksum(x['blue', j] for j in grades), name="Blend_Blue_I_Upper")

# Minimum production requirement for the red brand
model.addConstr(cp.quicksum(x['red', j] for j in grades) >= 2000, name="Min_Red")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: {:.2f} yuan".format(model.objval))
    for i in brands:
        print(f"Blending ratios for brand {i}:")
        for j in grades:
            print(f"  Grade {j}: {x[i, j].x:.2f} kg")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the brands, grades, supply, cost, and selling price. Next, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results, including the maximized total profit and the optimal blending ratios for each brand of wine.

This script provides a complete example of using the `coptpy` library to solve the problem of maximizing profit for a brand of wine, while satisfying all the constraints mentioned in the problem.

---

## Case 36  [SOLVE_FAILED]

**GT:** 2924  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
A product consists of three components, which are produced by four workshops. The total number of production hours available for each workshop is limited. Table 1.4 shows the productivity of the three components. The objective is to determine how many hours should be allocated to each component in each workshop in order to maximize the number of completed products. Represent this problem as a linear programming problem.

Table 1.4

| Workshop | Production Capacity <br> (hours) | Productivity (units/hour) |  |  |
| :---: | :---: | :---: | :---: | :---: |
|  |  | Component 1 | Component 2 | Component 3 |
| A | 100 | 10 | 15 | 5 |
| B | 150 | 15 | 10 | 5 |
| C | 80 | 20 | 5 | 10 |
| D | 200 | 10 | 15 | 20 |

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Productivity_Maximization", LpMaximize)

# Define decision variables
x11, x12, x13, x21, x22, x23, x31, x32, x33, x41, x42, x43 = [
    LpVariable(f"x_{i}_{j}", lowBound=0) for i in range(1, 5) for j in range(1, 4)
]

# Define the objective function
prob += sum([
    x11*10 + x12*15 + x13*20,
    x21*10 + x22*10 + x23*5,
    x31*20 + x32*5 + x33*10,
    x41*5 + x42*15 + x43*20
], "Total_Productivity")

# Define the constraints based on production capacities of each workshop
prob += 10*x11 + 15*x12 + 20*x13 <= 100, "Workshop_A"
prob += 15*x21 + 10*x22 + 5*x23 <= 150, "Workshop_B"
prob += 20*x31 + 5*x32 + 10*x33 <= 80, "Workshop_C"
prob += 5*x41 + 15*x42 + 20*x43 <= 200, "Workshop_D"

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Productivity: {prob.objective.value()}")
```

This code sets up and solves a linear programming problem to maximize the total productivity of components across four workshops, given their production capacities.

### ORLM-8B formulation
## Mathematical Model:
To solve the product assembly problem, we need to construct a linear programming model to maximize the number of completed products while satisfying the production capacity constraints of each workshop. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The number of hours allocated to component \(j\) in workshop \(i\), where \(i \in \{A, B, C, D\}\) represents the workshop and \(j \in \{1, 2, 3\}\) represents the component.

### Objective Function:
- Maximize the number of completed products: \[Z = \min \left\{10x_{A1} + 15x_{A2} + 5x_{A3}, 15x_{B1} + 10x_{B2} + 5x_{B3}, 20x_{C1} + 5x_{C2} + 10x_{C3}, 10x_{D1} + 15x_{D2} + 20x_{D3}\right\}\]

### Constraints:
- Production capacity constraints for each workshop:
  - \(x_{A1} + x_{A2} + x_{A3} \leq 100\)
  - \(x_{B1} + x_{B2} + x_{B3} \leq 150\)
  - \(x_{C1} + x_{C2} + x_{C3} \leq 80\)
  - \(x_{D1} + x_{D2} + x_{D3} \leq 200\)

### Non-negativity Constraints:
- \(x_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply linear programming techniques to find the optimal number of hours allocated to each component in each workshop, maximizing the number of completed products while satisfying the production capacity constraints of each workshop. This will provide an optimized production strategy for the product assembly problem.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductAssemblyOptimization")

# Add decision variables
x = model.addVars(['A', 'B', 'C', 'D'], [1, 2, 3], lb=0, nameprefix="x")

# Objective function: Maximize the number of completed products
model.setObjective(cp.minimize(cp.quicksum([
    10 * x['A', 1] + 15 * x['A', 2] + 5 * x['A', 3],
    15 * x['B', 1] + 10 * x['B', 2] + 5 * x['B', 3],
    20 * x['C', 1] + 5 * x['C', 2] + 10 * x['C', 3],
    10 * x['D', 1] + 15 * x['D', 2] + 20 * x['D', 3]
])), sense=COPT.MAXIMIZE)

# Constraints: Production capacity constraints for each workshop
model.addConstr(x['A', 1] + x['A', 2] + x['A', 3] <= 100, name="CapacityA")
model.addConstr(x['B', 1] + x['B', 2] + x['B', 3] <= 150, name="CapacityB")
model.addConstr(x['C', 1] + x['C', 2] + x['C', 3] <= 80, name="CapacityC")
model.addConstr(x['D', 1] + x['D', 2] + x['D', 3] <= 200, name="CapacityD")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized number of completed products: {:.2f}".format(model.objval))
    for i in ['A', 'B', 'C', 'D']:
        for j in [1, 2, 3]:
            print(f"Number of hours allocated to component {j} in workshop {i}: {x[i, j].x:.2f}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables `x` representing the number of hours allocated to each component in each workshop. The objective function is to maximize the number of completed products, calculated using the `cp.minimize` function to select the minimum productivity value among the four workshops.

We add four constraints to ensure that the total number of hours allocated to each workshop does not exceed its production capacity. Finally, we solve the model and output the results of the optimal solution, including the maximized number of completed products and the number of hours allocated to each component in each workshop.

This script provides a complete example of solving the product assembly problem using the `coptpy` library, while satisfying all the constraints mentioned in the problem.

---

## Case 37  [SOLVE_FAILED]

**GT:** 1250  |  **3B:** 23250.0 (Infeasible)  |  **8B:** None

### Question
A factory produces two models of microcomputers, A and B. Each model requires two identical processes. The processing time, sales profit, and maximum processing capacity per week for each microcomputer are shown in Table 3.1.

Table 3.1

| Process | Model A | Model B | Maximum Processing Capacity |
| :---: | :---: | :---: | :---: |
| I (hours per unit) | 4 | 6 | 150 |
| II (hours per unit) | 3 | 2 | 70 |
| Profit (RMB per unit) | 300 | 450 |  |

If the factory's desired objectives and priority levels are as follows:

$p_{1}$: The total weekly profit should not be less than 10,000 RMB.

$p_{2}$: Due to contractual requirements, at least 10 units of model A and 15 units of model B should be produced per week.

$p_{3}$: It is desired that the weekly production time for process I is exactly 150 hours, and the production time for process II is maximized, even with overtime if necessary.

If the products produced during overtime in process II result in a decrease of 20 RMB in profit per unit for model A and 25 RMB for model B, and the maximum overtime for process II is 30 hours per week, with this objective as level $p_{4}$, establish an objective programming model for this problem.

### 3B formulation
```python
from pulp import LpMaximize, LpProblem, LpVariable

# Define the decision variables
x1 = LpVariable('Model_A_quantity', lowBound=0, cat='Continuous')
x2 = LpVariable('Model_B_quantity', lowBound=0, cat='Continuous')

# Create the LP problem
prob = LpProblem("Microcomputer_Profit_Model", LpMaximize)

# Define the objective function
profit_function = 300*x1 + 450*x2
prob += profit_function

# Add constraints based on given conditions
# Constraint for total weekly profit not less than 10,000 RMB
prob += 300*x1 + 450*x2 >= 10000

# Constraint for at least 10 units of model A and 15 units of model B per week
prob += x1 >= 10
prob += x2 >= 15

# Constraint for exactly 150 hours in process I
process_I_hours = 4*x1 + 6*x2 <= 150

# Constraint for maximizing the production time in process II, with overtime if necessary
process_II_hours = 3*x1 + 2*x2 <= 70
prob += 3*x1 + 2*x2 <= 70 - (x1 >= 10) * 4 - (x2 >= 15) * 2

# Constraint for maximum overtime in process II, with a decrease of profit per unit
overtime_process_II_hours = 3*x1 + 2*x2 <= 70 - (x1 >= 10) * 4 - (x2 >= 15) * 2 + 30

# Constraint for the weekly production time for process II being exactly 150 hours
prob += 3*x1 + 2*x2 == 150 - (x1 >= 10) * 4 - (x2 >= 15) * 2 + 30

# Solve the problem
prob.solve()

# Print the results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Profit = ", value(prob.objective))
```

Please note that this code is a simplified version of what you might need to implement based on your specific requirements and constraints. The overtime constraint handling may require additional adjustments depending on the exact conditions provided in the problem statement.

### ORLM-8B formulation
## Mathematical Model:
To solve the factory's production planning problem, we need to construct an objective programming model to minimize the deviation of the total profit from the desired objective while satisfying the production requirements and time constraints. Here is the model formulation:

### Decision Variables:
- \(x_{1}\): Number of units of model A produced during regular time.
- \(x_{2}\): Number of units of model A produced during overtime.
- \(x_{3}\): Number of units of model B produced during regular time.
- \(x_{4}\): Number of units of model B produced during overtime.
- \(d_{1}^{-}\): Negative deviation of total profit from the desired objective.
- \(d_{1}^{+}\): Positive deviation of total profit from the desired objective.
- \(d_{2}^{-}\): Negative deviation of model A production from the desired minimum.
- \(d_{3}^{-}\): Negative deviation of model B production from the desired minimum.
- \(d_{4}^{-}\): Negative deviation of process I time from the desired maximum.
- \(d_{5}^{-}\): Negative deviation of process II time from the desired maximum.
- \(d_{6}^{-}\): Negative deviation of process II overtime time from the desired maximum.

### Objective Function:
- Minimize the total deviation: \[Z = p_{1} d_{1}^{-} + p_{2} d_{2}^{-} + p_{3} d_{4}^{-} + p_{3} d_{5}^{-} + p_{4} d_{6}^{-}\]

### Constraints:
1. Total profit constraint: \[300x_{1} + 280x_{2} + 450x_{3} + 425x_{4} + d_{1}^{-} - d_{1}^{+} = 10000\]
2. Model A production constraint: \[x_{1} + x_{2} + d_{2}^{-} - d_{2}^{+} = 10\]
3. Model B production constraint: \[x_{3} + x_{4} + d_{3}^{-} - d_{3}^{+} = 15\]
4. Process I time constraint: \[4x_{1} + 6x_{3} + d_{4}^{-} - d_{4}^{+} = 150\]
5. Process II time constraint: \[3x_{1} + 3x_{2} + 2x_{3} + 2x_{4} + d_{5}^{-} - d_{5}^{+} = 70\]
6. Process II overtime time constraint: \[d_{5}^{+} + d_{6}^{-} - d_{6}^{+} = 30\]
7. Non-negativity constraints: \[x_{1}, x_{2}, x_{3}, x_{4}, d_{i}^{-}, d_{i}^{+} \geq 0, \forall i\]

Using this model, we can apply objective programming techniques to find the optimal production plan that minimizes the deviation of the total profit from the desired objective while satisfying all production requirements and time constraints. This will provide the factory with an economically efficient production strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionOptimization")

# Add decision variables
x1 = model.addVar(vtype=COPT.INTEGER, name="x1")  # Number of units of model A produced during regular time
x2 = model.addVar(vtype=COPT.INTEGER, name="x2")  # Number of units of model A produced during overtime
x3 = model.addVar(vtype=COPT.INTEGER, name="x3")  # Number of units of model B produced during regular time
x4 = model.addVar(vtype=COPT.INTEGER, name="x4")  # Number of units of model B produced during overtime

# Add deviation variables
d1_minus = model.addVar(name="d1_minus")  # Negative deviation of total profit from the desired objective
d1_plus = model.addVar(name="d1_plus")    # Positive deviation of total profit from the desired objective
d2_minus = model.addVar(name="d2_minus")  # Negative deviation of model A production from the desired minimum
d3_minus = model.addVar(name="d3_minus")  # Negative deviation of model B production from the desired minimum
d4_minus = model.addVar(name="d4_minus")  # Negative deviation of process I time from the desired maximum
d5_minus = model.addVar(name="d5_minus")  # Negative deviation of process II time from the desired maximum
d6_minus = model.addVar(name="d6_minus")  # Negative deviation of process II overtime time from the desired maximum

# Set the objective function
model.setObjective(p1 * d1_minus + p2 * d2_minus + p3 * d4_minus + p3 * d5_minus + p4 * d6_minus, sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(300 * x1 + 280 * x2 + 450 * x3 + 425 * x4 + d1_minus - d1_plus == 10000, name="ProfitConstraint")
model.addConstr(x1 + x2 + d2_minus - d2_plus == 10, name="ModelAConstraint")
model.addConstr(x3 + x4 + d3_minus - d3_plus == 15, name="ModelBConstraint")
model.addConstr(4 * x1 + 6 * x3 + d4_minus - d4_plus == 150, name="ProcessIConstraint")
model.addConstr(3 * x1 + 3 * x2 + 2 * x3 + 2 * x4 + d5_minus - d5_plus == 70, name="ProcessIIConstraint")
model.addConstr(d5_plus + d6_minus - d6_plus == 30, name="ProcessIIOTConstraint")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Optimal solution found.")
    print(f"Number of units of model A produced during regular time: {x1.x}")
    print(f"Number of units of model A produced during overtime: {x2.x}")
    print(f"Number of units of model B produced during regular time: {x3.x}")
    print(f"Number of units of model B produced during overtime: {x4.x}")
    print(f"Total profit: {300 * x1.x + 280 * x2.x + 450 * x3.x + 425 * x4.x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and deviation variables, set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the number of units produced during regular and overtime, and the total profit.

This script provides a complete example of using the `coptpy` library to solve the factory's production planning problem while satisfying all the constraints mentioned in the problem.

---

## Case 38  [SOLVE_FAILED]

**GT:** 6105  |  **3B:** 2309.0 (Infeasible)  |  **8B:** None

### Question
A company produces two types of small motorcycles, with Type A being completely manufactured by the company and Type B being assembled from imported parts. The manufacturing, assembly, and inspection times required for these two products are shown in Table 3.2.
Table 3.2

| Type | Manufacturing | Assembly | Inspection | Selling Price <br> (yuan per unit) |
| :---: | :---: | :---: | :---: | :---: |
|  |  |  |  |  |
| Type A (hours per unit) | 20 | 5 | 3 | 650 |
| Type B (hours per unit) | 0 | 7 | 6 | 725 |
| Maximum weekly production capacity (hours) | 120 | 80 | 40 |  |
| Hourly production cost (yuan) | 12 | 8 | 10 |  |

If the company's expected goals and priority levels are as follows:

$p_{1}$: Total weekly profit is at least 3000 yuan;

$p_{2}$: At least 5 units of Type A motorcycles are produced weekly;

$p_{3}$: Minimize the idle time of each process, with the coefficients of the three processes being proportional to their hourly costs, and no overtime is allowed.

Formulate an objective programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable

# Define the problem as a maximization problem
prob = LpProblem("Motorcycle_Profit_Model", LpMaximize)

# Decision variables: number of Type A and Type B motorcycles produced weekly
x1 = LpVariable('Type_A_units', lowBound=0, cat='Continuous')
x2 = LpVariable('Type_B_units', lowBound=0, cat='Continuous')

# Objective function: total profit
prob += 650 * x1 + 725 * x2 - (12 * 20 * x1 + 8 * 5 * x1 + 10 * 3 * x1 +
                                   8 * 7 * x2 + 10 * 6 * x2), "Total_Profit"

# Constraints: production capacity and priority levels
prob += 20 * x1 + 7 * x2 <= 120, 'Manufacturing_Capacity'
prob += 5 * x1 + 6 * x2 <= 80, 'Assembly_Capacity'
prob += 3 * x1 + 6 * x2 <= 40, 'Inspection_Capacity'

# Priority level constraints
prob += x1 >= 5, "Priority_Level_Type_A"
prob += (12 * 20 - 12 * 20 * x1) / 80 >= 0, "Idle_Manufacturing_Time"
prob += (8 * 7 - 8 * 7 * x2) / 40 >= 0, "Idle_Assembly_Time"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {prob.objective.value()}")
```

This code formulates and solves a linear programming model for the motorcycle production problem using PuLP. The objective is to maximize profit while adhering to constraints related to production capacity, priority levels, and idle time.

### ORLM-8B formulation
## Mathematical Model:
To solve the company's production planning problem, we need to construct an objective programming model to maximize the total profit while satisfying the constraints of production capacity and priority goals. Here is the model formulation:

### Decision Variables:
- \(x_{1}\): Number of Type A motorcycles produced.
- \(x_{2}\): Number of Type B motorcycles produced.

### Objective Function:
- Minimize the deviation function: \[Z = p_{1}d_{1}^{-} + p_{2}d_{2}^{-} + p_{3}(6d_{3}^{-} + 4d_{4}^{-} + 5d_{5}^{-})\]

### Constraints:
1. Profit constraint: \[650x_{1} + 725x_{2} - 20 \cdot 12 x_{1} - 5 \cdot 8 x_{1} - 3 \cdot 10 x_{1} - 7 \cdot 8 x_{2} - 6 \cdot 10 x_{2} \geq 3000 + d_{1}^{-}\]
2. Type A production constraint: \[x_{1} \geq 5 + d_{2}^{-}\]
3. Manufacturing time constraint: \[20x_{1} \leq 120 + d_{3}^{-}\]
4. Assembly time constraint: \[5x_{1} + 7x_{2} \leq 80 + d_{4}^{-}\]
5. Inspection time constraint: \[3x_{1} + 6x_{2} \leq 40 + d_{5}^{-}\]

### Non-negativity Constraints:
- \(x_{1}, x_{2}, d_{i}^{-} \geq 0, \forall i \in \{1, 2, 3, 4, 5\}\)

Using this model, we can apply objective programming techniques to find the optimal production quantities for each type of motorcycle, while satisfying all production capacity constraints and priority goals, in order to maximize the total profit. This will provide the company with an optimized production plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("MotorcycleProduction")

# Add decision variables
x1 = model.addVar(vtype=COPT.INTEGER, name="x1")  # Number of Type A motorcycles produced
x2 = model.addVar(vtype=COPT.INTEGER, name="x2")  # Number of Type B motorcycles produced
d1_neg = model.addVar(name="d1_neg")  # Negative deviation for profit
d2_neg = model.addVar(name="d2_neg")  # Negative deviation for Type A production
d3_neg = model.addVar(name="d3_neg")  # Negative deviation for manufacturing time
d4_neg = model.addVar(name="d4_neg")  # Negative deviation for assembly time
d5_neg = model.addVar(name="d5_neg")  # Negative deviation for inspection time

# Set the objective function
model.setObjective(p1 * d1_neg + p2 * d2_neg + p3 * (6 * d3_neg + 4 * d4_neg + 5 * d5_neg), sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(650 * x1 + 725 * x2 - 20 * 12 * x1 - 5 * 8 * x1 - 3 * 10 * x1 - 7 * 8 * x2 - 6 * 10 * x2 >= 3000 + d1_neg, name="ProfitConstraint")
model.addConstr(x1 >= 5 + d2_neg, name="TypeAProductionConstraint")
model.addConstr(20 * x1 <= 120 + d3_neg, name="ManufacturingTimeConstraint")
model.addConstr(5 * x1 + 7 * x2 <= 80 + d4_neg, name="AssemblyTimeConstraint")
model.addConstr(3 * x1 + 6 * x2 <= 40 + d5_neg, name="InspectionTimeConstraint")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Optimal solution found.")
    print(f"Number of Type A motorcycles produced: {x1.x}")
    print(f"Number of Type B motorcycles produced: {x2.x}")
    print(f"Total profit: {650 * x1.x + 725 * x2.x - 20 * 12 * x1.x - 5 * 8 * x1.x - 3 * 10 * x1.x - 7 * 8 * x2.x - 6 * 10 * x2.x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and negative deviation variables, set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the production quantities for each type of motorcycle and the total profit.

This script provides a complete example of using the `coptpy` library to solve the company's production planning problem, while satisfying all the constraints and priority goals mentioned in the problem.

---

## Case 39  [SOLVE_FAILED]

**GT:** 58  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
Consider the task of delivering goods from a central warehouse to $m$ different sales locations. In each delivery, each sales location receives its order. Feasible routes have been specified for each delivery person, and each delivery person can transport up to $r$ types of orders. Assume there are $n$ feasible routes, and each route specifies the sales locations to deliver goods to. Let $c_{j}$ be the cost of the $j$th route. It is possible to have duplicates, so that more than one delivery person can arrive at the same sales location. Represent this problem as an integer model.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the number of variables and constants
m = 3  # Number of sales locations (can be replaced with actual value)
n = 5  # Number of feasible routes (can be replaced with actual value)
r = 2  # Maximum types of orders per delivery person (can be replaced with actual value)

# Initialize the problem as a minimization problem
prob = LpProblem("Delivery_Problem", LpMinimize)

# Define decision variables
delivery_persons = [LpVariable(f'delivery_{i}', lowBound=0, cat='Integer') for i in range(n)]

# Objective function: Minimize total cost of deliveries
objective_function = lpSum([c_j * delivery_person for c_j, delivery_person in zip(range(1, n+1), delivery_persons)])
prob += objective_function

# Constraints
for sales_location in range(m):
    # Sum of deliveries to each sales location should be less than or equal to the maximum types of orders per person
    constraint = lpSum([delivery_person * route[sales_location] for delivery_person, route in zip(delivery_persons, [range(1, n+1) if i == sales_location else [] for i in range(n)])]) <= r
    prob += constraint

# Solve the problem
prob.solve()

# Print the solution
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Cost: {prob.objective.value()}")
```

This code sets up a model where each delivery person can deliver to multiple sales locations, and there is an upper limit on how many types of orders they can handle. The objective is to minimize the total cost of deliveries while respecting these constraints. Please replace `m`, `n`, and `r` with actual values as needed for your specific problem.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of delivering goods from a central warehouse to different sales locations, we need to build an integer programming model to minimize the total cost of the delivery routes while satisfying the constraints of the delivery person's route selection and the order type limit. Here is the model formulation:

### Decision Variables:
- $x_{j}$: If the $j$th route is chosen, then $x_{j} = 1$; otherwise, $x_{j} = 0$.

### Objective Function:
- Minimize the total cost: $Z = \sum_{j=1}^{n} c_{j} x_{j}$

### Constraints:
1. Each sales location can be reached by at least one route: $\sum_{j=1}^{n} a_{ij} x_{j} \geq 1, \quad \forall i \in \{1, 2, \ldots, m\}$
2. Each delivery person can transport up to $r$ types of orders: $\sum_{i=1}^{m} a_{ij} x_{j} \leq r, \quad \forall j \in \{1, 2, \ldots, n\}$
3. Binary constraints: $x_{j} \in \{0, 1\}, \quad \forall j \in \{1, 2, \ldots, n\}$

### Non-negativity Constraints:
- $x_{j} \geq 0, \quad \forall j \in \{1, 2, \ldots, n\}$

Using this model, we can apply integer programming techniques to find the optimal combination of delivery routes that minimizes the total cost while satisfying the constraints of each sales location being reached by at least one route and the order type limit for each delivery person. This will provide the company with an economically efficient delivery strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("DeliveryRouteOptimization")

# Assume there are m sales locations, n routes, and each delivery person can transport r types of orders
m = ...  # Number of sales locations
n = ...  # Number of routes
r = ...  # Maximum number of order types each delivery person can transport
c = [...]  # Costs of each route
a = [...]  # Matrix indicating whether each route reaches each sales location

# Add decision variables
x = model.addVars(n, vtype=COPT.BINARY, name="x")

# Objective function: Minimize total cost
model.setObjective(cp.quicksum(c[j] * x[j] for j in range(n)), sense=COPT.MINIMIZE)

# Constraints
# Each sales location can be reached by at least one route
for i in range(m):
    model.addConstr(cp.quicksum(a[i][j] * x[j] for j in range(n)) >= 1, name=f"ReachSalesPoint_{i}")

# Each delivery person can transport up to r types of orders
for j in range(n):
    model.addConstr(cp.quicksum(a[i][j] * x[j] for i in range(m)) <= r, name=f"DeliveryLimit_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f}".format(model.objval))
    for j in range(n):
        if x[j].x > 0:
            print(f"Choose route {j+1}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the number of sales locations, routes, and the maximum number of order types each delivery person can transport, as well as the costs of each route and the matrix indicating whether each route reaches each sales location.

Next, we add binary decision variables `x` to represent whether each route is chosen. The objective function is to minimize the total cost, calculated using the `cp.quicksum` function.

We add two sets of constraints:
1. Each sales location can be reached by at least one route, using the `cp.quicksum` function to calculate the sum of the routes reaching each sales location.
2. Each delivery person can transport up to `r` types of orders, also using the `cp.quicksum` function to calculate the sum of the orders transported by each delivery person.

Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the chosen routes.

This script provides a complete example of using the `coptpy` library to solve the delivery route optimization problem while satisfying all the constraints mentioned in the problem.

---

## Case 40  [CODE_BUG]

**GT:** 770.0  |  **3B:** None (?)  |  **8B:** None

### Question
Consider the allocation of $n$ factories to $n$ locations, where the transportation quantity between factory $i$ and factory $j$ is $d_{ij}$, and the unit transportation cost from location $p$ to location $q$ is $c_{pq}$. To minimize the total transportation cost, represent this problem as an integer model.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

def solve_factory_allocation(n, d, c):
    # Initialize the LP problem
    prob = LpProblem("Factory_Allocation", LpMinimize)

    # Create variables for allocation decisions
    x = {i: {j: LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') 
              for j in range(n)} 
         for i in range(n)}

    # Objective function: Minimize total transportation cost
    prob += lpSum[c[i][j] * x[i][j] for i in range(n) for j in range(n)], "Total_Cost"

    # Constraints: Allocation to each factory and location
    for i in range(n):
        prob += lpSum[x[i][j] for j in range(n)] == 1, f"Allocate_Factory_{i}"
    
    for j in range(n):
        prob += lpSum[x[i][j] for i in range(n)] == 1, f"Allocate_Location_{j}"

    # Solve the problem
    status = prob.solve()

    return prob, x

# Example usage:
n = 3  # Number of factories and locations
d = {(0, 0): 5, (0, 1): 8, (0, 2): 7,
      (1, 0): 6, (1, 1): 4, (1, 2): 9,
      (2, 0): 3, (2, 1): 5, (2, 2): 2}

c = {(0, 0): 1, (0, 1): 2, (0, 2): 3,
     (1, 0): 4, (1, 1): 6, (1, 2): 7,
     (2, 0): 8, (2, 1): 9, (2, 2): 5}

prob, x = solve_factory_allocation(n, d, c)

# Print the solution
for i in range(n):
    for j in range(n):
        print(f"x[{i}, {j}] = {x[i][j].varValue}")
```

In this code, we define a function `solve_factory_allocation` that sets up and solves an integer linear programming problem to minimize total transportation cost. The example usage section demonstrates how to call the function with a simple 3-factory, 3-location setup.

### ORLM-8B formulation
## Mathematical Model:
To solve the factory allocation problem, we need to construct an integer programming model to minimize the total transportation cost. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): If factory \(i\) is allocated to location \(j\), then \(x_{ij} = 1\); otherwise, \(x_{ij} = 0\).

### Objective Function:
- Minimize the total transportation cost: \[Z = \sum_{i=1}^{n} \sum_{j=1}^{n} \sum_{p=1}^{n} \sum_{q=1}^{n} d_{ij} c_{pq} x_{ip} x_{jq}\]

### Constraints:
1. Each factory can only be allocated to one location:
   - \(\sum_{j=1}^{n} x_{ij} = 1, \quad \forall i \in \{1, \ldots, n\}\)
2. Each location can only have one factory:
   - \(\sum_{i=1}^{n} x_{ij} = 1, \quad \forall j \in \{1, \ldots, n\}\)

### Non-negativity and Integer Constraints:
- \(x_{ij} \in \{0, 1\}\), for all \(i, j \in \{1, \ldots, n\}\).

This model will help us find the optimal allocation of factories to locations, minimizing the total transportation cost.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("FactoryAllocation")

# Assume there are n factories and n locations
n = 5  # Example: 5 factories and 5 locations
# Transportation quantities d_ij and unit transportation costs c_pq need to be provided based on the actual situation

# Transportation quantities d_ij
d = {
    (i, j): ... for i in range(1, n+1) for j in range(1, n+1)
}

# Unit transportation costs c_pq
c = {
    (p, q): ... for p in range(1, n+1) for q in range(1, n+1)
}

# Add decision variables
x = model.addVars([(i, j) for i in range(1, n+1) for j in range(1, n+1)], vtype=COPT.BINARY, name="x")

# Objective function: Minimize total transportation cost
model.setObjective(cp.quicksum(d[i, j] * c[p, q] * x[i, p] * x[j, q] for i in range(1, n+1) for j in range(1, n+1) for p in range(1, n+1) for q in range(1, n+1)), sense=COPT.MINIMIZE)

# Constraints
# Each factory can only be allocated to one location
for i in range(1, n+1):
    model.addConstr(cp.quicksum(x[i, j] for j in range(1, n+1)) == 1, name=f"Factory_{i}")

# Each location can only have one factory
for j in range(1, n+1):
    model.addConstr(cp.quicksum(x[i, j] for i in range(1, n+1)) == 1, name=f"Location_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total transportation cost: {:.2f}".format(model.objval))
    for i in range(1, n+1):
        for j in range(1, n+1):
            if x[i, j].x > 0.5:  # Since x is a binary variable, we use 0.5 as the threshold
                print(f"Factory {i} allocated to Location {j}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the number of factories and locations, as well as the transportation quantities and unit transportation costs. We add decision variables, set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total transportation cost and the allocation of each factory to a location.

This script provides a complete example of solving the factory allocation problem using the `coptpy` library, while satisfying all the constraints mentioned in the problem.

---

## Case 41  [SOLVE_FAILED]

**GT:** 9337440  |  **3B:** None (Not Solved)  |  **8B:** None

### Question
For manufacturing companies, it is important to develop appropriate production plans and human resource management strategies to reduce operating costs, inventory costs, stockout costs, and labor costs. In particular, for products with high demand fluctuations, companies need to accurately forecast demand and develop corresponding production plans. A company produces a folding table, with a raw material cost of 90 yuan per unit and 5 labor hours. The unit price of the product is 300 yuan. At the beginning of January, the company has 1000 workers and holds 15,000 units of inventory. The normal wage for workers is 30 yuan per hour, and the normal working hours per worker per day is 8 hours. Overtime hours are paid at an hourly rate of 40 yuan. The number of working days per month is calculated as 20 days. Assuming the company has sufficient available production machines and its production capacity is not limited by machine hours. The overtime hours per worker per month do not exceed 20 hours. Holding inventory incurs corresponding inventory costs. If there is a stockout due to insufficient capacity, there will be certain stockout costs. In addition, the company can make up for the shortage through outsourcing. The outsourcing cost per unit, monthly inventory cost, and monthly stockout cost are 200 yuan, 15 yuan, and 35 yuan, respectively. The company's employees are all temporary workers, and the company can flexibly decide the number of employees to hire and dismiss each month. The cost of hiring and dismissing a single employee is 5000 yuan and 8000 yuan, respectively. Assuming the company has used existing forecasting models to predict the demand from month 1 to month 6, as shown in Table 4.1.

Table 4.1: Demand Forecast

| Month | 1 | 2 | 3 | 4 | 5 | 6 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Demand Forecast | 20000 | 40000 | 42000 | 35000 | 19000 | 18500 |

Please develop a production plan, worker schedule, and plan for hiring and dismissing employees for the company to maximize its total net profit over 6 months, while ensuring that the company holds at least 10,000 units of product by the end of June.

### 3B formulation
```python
from pulp import LpMaximize, LpProblem, LpVariable

# Initialize the problem as a maximization problem
prob = LpProblem("FoldingTableProduction", LpMaximize)

# Define decision variables
production = {}
for month in range(1, 7):
    production[month] = LpVariable(f"production_{month}", lowBound=0, cat='Continuous')

workers = {}
for day in range(20):  # Assuming a month has 20 working days
    for week in range(4):  # Assuming a month has 4 weeks
        workers[(day, week)] = LpVariable(f"worker_{day}_{week}", lowBound=0, cat='Continuous')

# Define the objective function (total net profit)
objective_function = sum((300 - 90 - 5 * production[month]) * min(production[month], demand) 
                          + workers[(day, week)] * 30
                          for month in range(1, 7) 
                          for day in range(20) 
                          for week in range(4)
                          for demand in [20000, 40000, 42000, 35000, 19000, 18500])
prob += objective_function

# Define constraints
# Inventory constraint at the end of June
inventory_constraint = LpVariable("inventory", lowBound=0)
prob += inventory_constraint >= 10000

# Demand satisfaction constraint for each month
for month in range(1, 7):
    demand_constraint = sum(demand * min(production[month], production[month] // (4 * 20)) 
                             for demand in [20000, 40000, 42000, 35000, 19000, 18500])
    prob += workers[(day, week)] >= demand_constraint - production[month] * (4 * 20)
    
# Overtime hours constraint for each worker
overtime_hours = sum(workers[(day, week)] * 4 for day in range(20) for week in range(4))
prob += overtime_hours <= 160

# Inventory holding cost constraint
inventory_cost_constraint = LpVariable("inventory_cost", lowBound=0)
for month in range(1, 7):
    inventory_cost_constraint += sum(demand * (min(production[month], production[month] // (4 * 20)) - demand) 
                                      for demand in [20000, 40000, 42000, 35000, 19000, 18500])
prob += inventory_cost_constraint <= 60

# Stockout cost constraint
stockout_cost_constraint = LpVariable("stockout_cost", lowBound=0)
for month in range(1, 7):
    stockout_cost_constraint += sum(demand * (min(production[month], production[month] // (4 * 20)) - demand) 
                                     for demand in [20000, 40000, 42000, 35000, 19000, 18500])
prob += stockout_cost_constraint <= 60

# Hiring and dismissing employees cost constraint
hiring_dismissing_cost = LpVariable("hiring_dismissing_cost", lowBound=0)
for month in range(1, 7):
    hiring_dismissing_cost += sum(hiring * 5000 + dismissal * 8000 
                                   for hiring in workers[(day, week)] if hiring > 0
                                   for dismissal in workers[(day, week)] if dismissal < 0)
prob += hiring_dismissing_cost <= 12000

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Net Profit: {value(prob.objective)}")
```

Please note that this model assumes a fixed number of working days per month and weeks per month, which might not be accurate for real-world scenarios. Adjustments may be needed based on the actual work schedule and production capacity constraints.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_i \): Production quantity in month \( i \).
- \( y_i \): Number of workers in month \( i \).
- \( z_i \): Number of workers hired in month \( i \).
- \( w_i \): Number of workers dismissed in month \( i \).
- \( s_i \): Inventory quantity at the end of month \( i \).
- \( d_i \): Stockout quantity in month \( i \).
- \( o_i \): Overtime hours in month \( i \).

### Constraints:
1. **Production Capacity Constraint**:
   \[ x_i \leq y_i \times 160, \quad \forall i \]
   The production quantity in each month cannot exceed the total working hours of all workers in that month (8 hours per worker per day, 20 working days per month).

2. **Inventory Balance Constraint**:
   \[ s_i = s_{i-1} + x_i - d_i, \quad \forall i \]
   The inventory quantity at the end of each month is equal to the inventory quantity at the end of the previous month plus the production quantity minus the stockout quantity.

3. **Inventory Target Constraint**:
   \[ s_6 \geq 10000 \]
   The inventory quantity at the end of June must be at least 10,000 units.

4. **Demand Satisfaction Constraint**:
   \[ x_i + d_i \geq \text{Demand Forecast}_i, \quad \forall i \]
   The production quantity plus the stockout quantity in each month must satisfy the demand forecast.

5. **Worker Number Constraint**:
   \[ y_i = y_{i-1} + z_i - w_i, \quad \forall i \]
   The number of workers in each month is equal to the number of workers in the previous month plus the number of workers hired minus the number of workers dismissed.

6. **Overtime Constraint**:
   \[ o_i \leq y_i \times 20, \quad \forall i \]
   The overtime hours in each month cannot exceed the total overtime hours of all workers in that month (20 hours per worker).

7. **Non-Negativity Constraint**:
   \[ x_i, y_i, z_i, w_i, s_i, d_i, o_i \geq 0, \quad \forall i \]
   All decision variables must be non-negative.

### Objective:
Maximize the total net profit over 6 months:
\[ \max Z = \sum_{i=1}^{6} \left( (300 - 90) x_i - 30 y_i \times 160 - 15 s_i - 35 d_i - 5000 z_i - 8000 w_i - 40 o_i \right) \]

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("ProductionPlanning")

# Define decision variables
x = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Production")
y = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Workers")
z = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Hires")
w = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Fires")
s = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Inventory")
d = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Shortage")
o = model.addVars(6, vtype=COPT.CONTINUOUS, nameprefix = "Overtime")

# Demand forecast
demand = [20000, 40000, 42000, 35000, 19000, 18500]

# Objective function
model.setObjective(sum((210 * x[i] - 30 * y[i] * 160 - 15 * s[i] - 35 * d[i] - 5000 * z[i] - 8000 * w[i] - 40 * o[i]) for i in range(6)), sense=COPT.MAXIMIZE)

# Constraints
for i in range(6):
    model.addConstr(x[i] <= y[i] * 160, name=f"Capacity_{i}")
    model.addConstr(s[i] == (s[i-1] if i > 0 else 15000) + x[i] - d[i], name=f"StockBalance_{i}")
    model.addConstr(y[i] == (y[i-1] if i > 0 else 1000) + z[i] - w[i], name=f"WorkersBalance_{i}")
    model.addConstr(o[i] <= y[i] * 20, name=f"Overtime_{i}")
    model.addConstr(x[i] + d[i] >= demand[i], name=f"Demand_{i}")

# Inventory target constraint
model.addConstr(s[5] >= 10000, name="EndInventory")

# Solve the model
model.solve()

# Output the results
print("Optimal Total Net Profit: ", model.objval)
for i in range(6):
    print(f"Month {i+1}: Production = {x[i].x}, Workers = {y[i].x}, Hires = {z[i].x}, Fires = {w[i].x}, Inventory = {s[i].x}, Shortage = {d[i].x}, Overtime = {o[i].x}")
```
This script sets up the model, defines the decision variables, adds the constraints, and solves the model to maximize the total net profit over 6 months. It also prints out the optimal values for each decision variable for each month.

---

## Case 42  [CODE_BUG]

**GT:** 1644.63  |  **3B:** None (?)  |  **8B:** None

### Question
The Vehicle Routing Problem (VRP) was first proposed by Dantzig in 1959 (Dantzig and Ramser 1959). It is a very classic combinatorial optimization problem. The basic VRP can usually be described as follows: in a certain area, there are a certain number of customers and a distribution center or warehouse. The customers are generally distributed in different locations, and each customer has a certain amount of goods delivery demand. The distribution center or warehouse needs to dispatch a fleet of vehicles and design a suitable delivery plan to fulfill all customer's goods delivery demands. The objective of VRP is to maximize efficiency while meeting all customer demands. The measurement of efficiency is usually presented in the form of an objective function. The objective function varies with the company's requirements, and common objective functions include minimizing the total distance traveled by vehicles, minimizing the total delivery time, and minimizing the number of vehicles used, etc. In addition to meeting customer delivery demands, VRP generally needs to consider various other constraints, resulting in various variants. For example, if the vehicle's load cannot exceed its maximum capacity (capacity constraint), the problem becomes the Capacitated Vehicle Routing Problem (CVRP). If the delivery demand of each customer must be delivered within a specific time window, the problem becomes the Vehicle Routing Problem with Time Windows (VRPTW).

The Vehicle Routing Problem with Time Windows (VRPTW) is a classic problem developed from VRP. There are many applications of VRPTW in reality, and each customer point generally has a service time window. For example, some logistics centers need to deliver packages during low-traffic hours, some large supermarkets need to restock during non-business hours, and real-time delivery methods such as food delivery require specific delivery time windows. Time windows can be classified as hard time windows and soft time windows. Hard Time Windows (HTW) means that vehicles must arrive at or before the time window, and cannot delay their arrival. If they arrive early, they must wait until the time window starts to provide service, such as restocking supermarkets and delivering goods from logistics centers, etc. Soft Time Windows (STW) means that vehicles are not required to arrive within the original hard time window, but they should try to arrive within the hard time window. If the vehicle arrives early, a penalty value will be deducted, and if it arrives late, a certain penalty value will be imposed, such as food delivery, school bus pick-up and drop-off, industrial distribution, etc.

The Vehicle Routing Problem with Hard Time Windows (VRPHTW) can be described as follows: there are a certain number of customer points and a distribution center in the region. Vehicles need to depart from the distribution center and return to the distribution center. The route should be continuous, and each customer should be served by one and only one vehicle. The vehicles also have a capacity. Each customer has a specific service time window and can only be served within the time window. Vehicles can arrive at the customer point ahead of time and wait for the time window to open, then provide service to the customer. They can also arrive at the customer point within the time window to provide service. Vehicles can only start serving customers within the time window, and the service time is known. The distribution center needs to arrange a reasonable delivery plan to both complete the delivery tasks and minimize travel costs. VRPHTW, like VRP, mainly emphasizes the travel costs on the routes because delays are not allowed. Now, please model the VRPHTW in operations research.

### Example
r101.txt = r\"""
    0          35      35           0       0         230           0
    1          41      49          10     161         171          10
    2          35      17           7      50          60          10
    3          55      45          13     116         126          10
    4          55      20          19     149         159          10
    5          15      30          26      34          44          10
    6          25      30           3      99         109          10
    7          20      50           5      81          91          10
    8          10      43           9      95         105          10
    9          55      60          16      97         107          10
   10          30      60          16     124         134          10
   11          20      65          12      67          77          10
   12          50      35          19      63          73          10
   13          30      25          23     159         169          10
   14          15      10          20      32          42          10
   15          30       5           8      61          71          10
   16          10      20          19      75          85          10
   17           5      30           2     157         167          10
   18          20      40          12      87          97          10
   19          15      60          17      76          86          10
   20          45      65           9     126         136          10
   21          45      20          11      62          72          10
   22          45      10          18      97         107          10
   23          55       5          29      68          78          10
   24          65      35           3     153         163          10
   25          65      20           6     172         182          10
   26          45      30          17     132         142          10
   27          35      40          16      37          47          10
   28          41      37          16      39          49          10
   29          64      42           9      63          73          10
   30          40      60          21      71          81          10
   31          31      52          27      50          60          10
   32          35      69          23     141         151          10
   33          53      52          11      37          47          10
   34          65      55          14     117         127          10
   35          63      65           8     143         153          10
   36           2      60           5      41          51          10
   37          20      20           8     134         144          10
   38           5       5          16      83          93          10
   39          60      12          31      44          54          10
   40          40      25           9      85          95          10
   41          42       7           5      97         107          10
   42          24      12           5      31          41          10
   43          23       3           7     132         142          10
   44          11      14          18      69          79          10
   45           6      38          16      32          42          10
   46           2      48           1     117         127          10
   47           8      56          27      51          61          10
   48          13      52          36     165         175          10
   49           6      68          30     108         118          10
   50          47      47          13     124         134          10
   51          49      58          10      88          98          10
   52          27      43           9      52          62          10
   53          37      31          14      95         105          10
   54          57      29          18     140         150          10
   55          63      23           2     136         146          10
   56          53      12           6     130         140          10
   57          32      12           7     101         111          10
   58          36      26          18     200         210          10
   59          21      24          28      18          28          10
   60          17      34           3     162         172          10
   61          12      24          13      76          86          10
   62          24      58          19      58          68          10
   63          27      69          10      34          44          10
   64          15      77           9      73          83          10
   65          62      77          20      51          61          10
   66          49      73          25     127         137          10
   67          67       5          25      83          93          10
   68          56      39          36     142         152          10
   69          37      47           6      50          60          10
   70          37      56           5     182         192          10
   71          57      68          15      77          87          10
   72          47      16          25      35          45          10
   73          44      17           9      78          88          10
   74          46      13           8     149         159          10
   75          49      11          18      69          79          10
   76          49      42          13      73          83          10
   77          53      43          14     179         189          10
   78          61      52           3      96         106          10
   79          57      48          23      92         102          10
   80          56      37           6     182         192          10
   81          55      54          26      94         104          10
   82          15      47          16      55          65          10
   83          14      37          11      44          54          10
   84          11      31           7     101         111          10
   85          16      22          41      91         101          10
   86           4      18          35      94         104          10
   87          28      18          26      93         103          10
   88          26      52           9      74          84          10
   89          26      35          15     176         186          10
   90          31      67           3      95         105          10
   91          15      19           1     160         170          10
   92          22      22           2      18          28          10
   93          18      24          22     188         198          10
   94          26      27          27     100         110          10
   95          25      24          20      39          49          10
   96          22      27          11     135         145          10
   97          25      21          12     133         143          10
   98          19      21          10      58          68          10
   99          20      26           9      83          93          10
  100          18      18          17     185         195          10


\"""

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Load the data from r101.txt (assuming it's a CSV file with distances)
import pandas as pd

data = """
0          35      35           0       0         230           0
1          41      49          10     161         171          10
2          35      17           7      50          60          10
3          55      45          13     116         126          10
4          55      20          19     149         159          10
5          15      30          26      34          44          10
6          25      30           3      99         109          10
7          20      50           5      81          91          10
8          10      43           9      95         105          10
9          11      14          18      69          79          10
...
"""

df = pd.read_csv(pd.compat.StringIO(data), delim_whitespace=True, index_col=0)

# Define the problem
prob = LpProblem("R101_Distances", LpMinimize)

# Number of nodes (excluding depot)
num_nodes = len(df.columns) - 1

# Variables: x[i][j] indicates if edge (i,j) is used in the solution
x = {i: {j: LpVariable(f"x_{i}_{j}", lowBound=0, cat='Binary') for j in range(num_nodes)} for i in range(num_nodes)}

# Objective function: minimize total distance traveled
prob += lpSum([df.iloc[i][j] * x[i][j] for i in range(num_nodes) for j in range(num_nodes)])

# Constraints: each node must be visited exactly once (except depot)
for v in range(1, num_nodes):
    prob += lpSum(x[i][v] for i in range(num_nodes)) == 1

# Depot constraints
prob += lpSum(x[0][i] for i in range(1, num_nodes)) == 1
prob += lpSum(x[i][0] for i in range(1, num_nodes)) == 1

# Solve the problem
prob.solve()

# Print the solution
for v in prob.variables():
    if v.varValue > 0:
        print(f"{v.name}: {v.varValue}")

print(f"Status: {LpStatus[prob.status]}")
```

This code snippet defines a linear programming (LP) model to solve the vehicle routing problem with time windows using PuLP, a Python library for defining and solving LP models. The data is loaded from an assumed CSV file format (`r101.txt`), and the solution attempts to minimize the total distance traveled while ensuring each node is visited exactly once except the depot (node 0). Please note that you need to have `pulp` and `pandas` installed in your Python environment. The data should be formatted as a CSV file with distances between nodes, where the first row/column represents the depot. Adjustments may be needed based on actual data format or additional constraints specific to your problem.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{ijk} \): Binary variable indicating whether vehicle \( k \) travels directly from customer \( i \) to customer \( j \).
- \( s_{ik} \): Continuous variable representing the start time of service at customer \( i \) by vehicle \( k \).
- \( u_k \): Continuous variable representing the load of vehicle \( k \).

### Objective Function:
Minimize the total travel cost:
\[ \min \sum_{i=0}^{n} \sum_{j=0}^{n} \sum_{k=1}^{m} c_{ij} x_{ijk} \]
where \( c_{ij} \) is the travel cost from customer \( i \) to customer \( j \).

### Constraints:
1. Each customer is visited exactly once:
   \[ \sum_{i=0}^{n} \sum_{k=1}^{m} x_{ijk} = 1 \quad \forall j \]
2. Each vehicle departs from the distribution center and returns to the distribution center:
   \[ \sum_{i=0}^{n} x_{0ik} = \sum_{j=0}^{n} x_{j0k} = 1 \quad \forall k \]
3. Vehicle load constraint:
   \[ \sum_{i=0}^{n} \sum_{j=0}^{n} q_j x_{ijk} \leq Q_k \quad \forall k \]
   where \( q_j \) is the demand of customer \( j \) and \( Q_k \) is the maximum load of vehicle \( k \).
4. Time window constraint:
   \[ a_i \leq s_{ik} + t_i \leq b_i \quad \forall i, \forall k \]
   where \( a_i \) and \( b_i \) are the start and end time windows of customer \( i \), and \( t_i \) is the service time at customer \( i \).
5. Continuity constraint:
   \[ \sum_{i=0}^{n} x_{ijk} - \sum_{j=0}^{n} x_{jik} = 0 \quad \forall k \]
6. Subtour elimination constraint (using Miller-Tucker-Zemlin constraints):
   \[ u_k - n \cdot x_{ijk} \leq n - 1 \quad \forall i, \forall j, \forall k \]
   where \( u_k \) is a continuous variable representing the position of vehicle \( k \) in the route.

## Python Code Solution Using `coptpy`:
```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("VRPHTW")

# Define the number of customers, vehicles, and other parameters
n = ...  # Number of customers
m = ...  # Number of vehicles
c = ...  # Travel cost matrix
q = ...  # Customer demands
Q = ...  # Vehicle maximum loads
a = ...  # Customer start time windows
b = ...  # Customer end time windows
t = ...  # Customer service times

# Add decision variables
x = model.addVars(n+1, n+1, m, vtype=COPT.BINARY, nameprefix="x")
s = model.addVars(n+1, m, vtype=COPT.CONTINUOUS, nameprefix="s")
u = model.addVars(m, vtype=COPT.CONTINUOUS, nameprefix="u")

# Objective function: Minimize total travel cost
model.setObjective(cp.quicksum(c[i][j] * x[i, j, k] for i in range(n+1) for j in range(n+1) for k in range(m)), sense=COPT.MINIMIZE)

# Constraints
# Each customer is visited exactly once
for j in range(1, n+1):
    model.addConstr(cp.quicksum(x[i, j, k] for i in range(n+1) for k in range(m)) == 1)

# Each vehicle departs from the distribution center and returns to the distribution center
for k in range(m):
    model.addConstr(cp.quicksum(x[0, i, k] for i in range(1, n+1)) == 1)
    model.addConstr(cp.quicksum(x[j, 0, k] for j in range(1, n+1)) == 1)

# Vehicle load constraint
for k in range(m):
    model.addConstr(cp.quicksum(q[j] * x[i, j, k] for i in range(n+1) for j in range(1, n+1)) <= Q[k])

# Time window constraint
for i in range(1, n+1):
    for k in range(m):
        model.addConstr(s[i, k] + t[i] >= a[i])
        model.addConstr(s[i, k] + t[i] <= b[i])

# Continuity constraint
for k in range(m):
    for i in range(n+1):
        model.addConstr(cp.quicksum(x[i, j, k] for j in range(n+1)) - cp.quicksum(x[j, i, k] for j in range(n+1)) == 0)

# Subtour elimination constraint (using Miller-Tucker-Zemlin constraints)
for i in range(1, n+1):
    for j in range(1, n+1):
        for k in range(m):
            model.addConstr(u[k] - n * x[i, j, k] <= n - 1)

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total travel cost: {:.2f}".format(model.objval))
    for k in range(m):
        print(f"Route for Vehicle {k+1}:")
        for i in range(n+1):
            for j in range(n+1):
                if x[i, j, k].x > 0.5:  # Since it's a binary variable, we use 0.5 as the threshold
                    print(f"From Customer {i} to Customer {j}")
        print(f"Vehicle {k+1} load: {u[k].x:.2f}")
        for i in range(1, n+1):
            print(f"Service start time for Customer {i} by Vehicle {k+1}: {s[i, k].x:.2f}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the number of customers, vehicles, and other parameters, and add decision variables. Next, we set the objective function and constraints. Finally, we solve the model and output the results, including the minimum total travel cost and the routes for each vehicle.

This script provides a complete example of solving the Vehicle Routing Problem with Hard Time Windows (VRPHTW) using the `coptpy` library, while satisfying all the constraints mentioned in the problem.

---

## Case 43  [CODE_BUG]

**GT:** 40  |  **3B:** None (?)  |  **8B:** None

### Question
As one of the main arteries of urban transportation, the city subway carries a huge passenger flow and its operation and management are very complex. Among them, crew scheduling is one of the key links in subway operation management and also the starting point and difficulty of crew management. The subway transportation volume is large, with complex and changing routes, and frequent operation intervals. Crew drivers face huge, continuous, and high-intensity transportation tasks. It is important to arrange the driver's shift and duty mode reasonably and achieve the optimal allocation of personnel to ensure the efficient and stable operation of the subway. Due to the increasing complexity of the subway operation network, traditional manual scheduling methods can no longer meet the high standard operation requirements. Automated and intelligent crew scheduling has become an inevitable trend.

The general process of crew scheduling for subway operating companies is as follows: export train operation section and time information tables based on the current operation chart, manually divide the crew duty roster based on these information tables, compile the crew scheduling master table based on the duty roster, and finally allocate the crew groups based on the scheduling master table to form the final scheduling table. The entire process relies on manual compilation and mainly has the following three major problems:

1. Low scheduling efficiency: Crew scheduling business rules are complex, and the workload is large. The efficiency of manual compilation is very low, requiring at least one week. The manpower and time costs are high.

2. Difficulty in adjustment: When encountering unexpected situations such as train failures and temporary leave of crew members, it is difficult to quickly adjust the scheduling plan based on manual methods, affecting the efficiency of operation management.

3. Uneven task assignment: Manual scheduling has subjective limitations and strong dependence on human experience. If the scheduling is unreasonable, it may lead to uneven task assignment, unfair scheduling, and low crew satisfaction.

This subway line includes 40 platforms, among which A, M, and Z platforms are available for driver transfers and handovers. Please consider 200 driving tasks and their attributes such as time, location, and mileage, and consider classic constraints in crew scheduling scenarios, such as maximum continuous driving time constraint, mileage limit constraint, attendance location constraint, etc. Compare different mixed integer modeling methods to minimize the number of drivers as the goal and output the optimal task chain combination (i.e. the allocation and connection relationship of all tasks) for all tasks.

### Example
Mileage Information Table.csv = \"""
Departure Station,Arrival Station,Mileage
A,M,17.1
Z,M,26.4
\"""

Task Information Table.csv = \"""
Train Number,Train ID,Pickup Time,Pickup Location,Drop-off Time,Drop-off Location
331,M16,10:03:11,M,10:57:43,Z
1,L06,10:03:43,Z,10:58:32,M
163,N23,10:04:10,A,10:39:11,M
332,N27,10:04:32,M,10:40:10,A
333,N20,10:09:11,M,11:03:43,Z
2,L07,10:09:43,Z,11:04:32,M
164,L11,10:10:10,A,10:45:11,M
334,L01,10:10:32,M,10:46:10,A
335,M17,10:15:11,M,11:09:43,Z
3,M13,10:15:43,Z,11:10:32,M
165,N24,10:16:10,A,10:51:11,M
336,N28,10:16:32,M,10:52:10,A
337,N21,10:21:11,M,11:15:43,Z
4,L08,10:21:43,Z,11:16:32,M
166,N25,10:22:10,A,10:57:11,M
338,L02,10:22:32,M,10:58:10,A
339,M18,10:27:11,M,11:21:43,Z
5,M14,10:27:43,Z,11:22:32,M
167,N26,10:28:10,A,11:03:11,M
340,L03,10:28:32,M,11:04:10,A
341,N22,10:33:11,M,11:27:43,Z
6,L09,10:33:43,Z,11:28:32,M
168,L12,10:34:10,A,11:09:11,M
342,N29,10:34:32,M,11:10:10,A
343,N23,10:39:11,M,11:33:43,Z
7,M15,10:39:43,Z,11:34:32,M
169,N27,10:40:10,A,11:15:11,M
344,L04,10:40:32,M,11:16:10,A
345,L11,10:45:11,M,11:39:43,Z
8,N19,10:45:43,Z,11:40:32,M
170,L01,10:46:10,A,11:21:11,M
346,L05,10:46:32,M,11:22:10,A
347,N24,10:51:11,M,11:45:43,Z
9,L10,10:51:43,Z,11:46:32,M
171,N28,10:52:10,A,11:27:11,M
348,N30,10:52:32,M,11:28:10,A
349,N25,10:57:11,M,11:51:43,Z
10,M16,10:57:43,Z,11:52:32,M
172,L02,10:58:10,A,11:33:11,M
350,L06,10:58:32,M,11:34:10,A
351,N26,11:03:11,M,11:57:43,Z
11,N20,11:03:43,Z,11:58:32,M
173,L03,11:04:10,A,11:39:11,M
352,L07,11:04:32,M,11:40:10,A
353,L12,11:09:11,M,12:03:43,Z
12,M17,11:09:43,Z,12:04:32,M
174,N29,11:10:10,A,11:45:11,M
354,M13,11:10:32,M,11:46:10,A
355,N27,11:15:11,M,12:09:43,Z
13,N21,11:15:43,Z,12:10:32,M
175,L04,11:16:10,A,11:51:11,M
356,L08,11:16:32,M,11:52:10,A
357,L01,11:21:11,M,12:15:43,Z
14,M18,11:21:43,Z,12:16:32,M
176,L05,11:22:10,A,11:57:11,M
358,M14,11:22:32,M,11:58:10,A
359,N28,11:27:11,M,12:21:43,Z
15,N22,11:27:43,Z,12:22:32,M
177,N30,11:28:10,A,12:03:11,M
360,L09,11:28:32,M,12:04:10,A
361,L02,11:33:11,M,12:27:43,Z
16,N23,11:33:43,Z,12:28:32,M
178,L06,11:34:10,A,12:09:11,M
362,M15,11:34:32,M,12:10:10,A
363,L03,11:39:11,M,12:33:43,Z
17,L11,11:39:43,Z,12:34:32,M
179,L07,11:40:10,A,12:15:11,M
364,N19,11:40:32,M,12:16:10,A
365,N29,11:45:11,M,12:39:43,Z
18,N24,11:45:43,Z,12:40:32,M
180,M13,11:46:10,A,12:21:11,M
366,L10,11:46:32,M,12:22:10,A
367,L04,11:51:11,M,12:45:43,Z
19,N25,11:51:43,Z,12:46:32,M
181,L08,11:52:10,A,12:27:11,M
368,M16,11:52:32,M,12:28:10,A
369,L05,11:57:11,M,12:51:43,Z
20,N26,11:57:43,Z,12:52:32,M
182,M14,11:58:10,A,12:33:11,M
370,N20,11:58:32,M,12:34:10,A
371,N30,12:03:11,M,12:57:43,Z
21,L12,12:03:43,Z,12:58:32,M
183,L09,12:04:10,A,12:39:11,M
372,M17,12:04:32,M,12:40:10,A
373,L06,12:09:11,M,13:03:43,Z
22,N27,12:09:43,Z,13:04:32,M
184,M15,12:10:10,A,12:45:11,M
374,N21,12:10:32,M,12:46:10,A
375,L07,12:15:11,M,13:09:43,Z
23,L01,12:15:43,Z,13:10:32,M
185,N19,12:16:10,A,12:51:11,M
376,M18,12:16:32,M,12:52:10,A
377,M13,12:21:11,M,13:15:43,Z
24,N28,12:21:43,Z,13:16:32,M
186,L10,12:22:10,A,12:57:11,M
378,N22,12:22:32,M,12:58:10,A
379,L08,12:27:11,M,13:21:43,Z
25,L02,12:27:43,Z,13:22:32,M
187,M16,12:28:10,A,13:03:11,M
380,N23,12:28:32,M,13:04:10,A
381,M14,12:33:11,M,13:27:43,Z
26,L03,12:33:43,Z,13:28:32,M
188,N20,12:34:10,A,13:09:11,M
382,L11,12:34:32,M,13:10:10,A
383,L09,12:39:11,M,13:33:43,Z
27,N29,12:39:43,Z,13:34:32,M
189,M17,12:40:10,A,13:15:11,M
384,N24,12:40:32,M,13:16:10,A
385,M15,12:45:11,M,13:39:43,Z
28,L04,12:45:43,Z,13:40:32,M
190,N21,12:46:10,A,13:21:11,M
386,N25,12:46:32,M,13:22:10,A
387,N19,12:51:11,M,13:45:43,Z
29,L05,12:51:43,Z,13:46:32,M
191,M18,12:52:10,A,13:27:11,M
388,N26,12:52:32,M,13:28:10,A
389,L10,12:57:11,M,13:51:43,Z
30,N30,12:57:43,Z,13:52:32,M
192,N22,12:58:10,A,13:33:11,M
390,L12,12:58:32,M,13:34:10,A
391,M16,13:03:11,M,13:57:43,Z
31,L06,13:03:43,Z,13:58:32,M
193,N23,13:04:10,A,13:39:11,M
392,N27,13:04:32,M,13:40:10,A
393,N20,13:09:11,M,14:03:43,Z
32,L07,13:09:43,Z,14:04:32,M
194,L11,13:10:10,A,13:45:11,M
394,L01,13:10:32,M,13:46:10,A
395,M17,13:15:11,M,14:09:43,Z
33,M13,13:15:43,Z,14:10:32,M
195,N24,13:16:10,A,13:51:11,M
396,N28,13:16:32,M,13:52:10,A
397,N21,13:21:11,M,14:15:43,Z
34,L08,13:21:43,Z,14:16:32,M
196,N25,13:22:10,A,13:57:11,M
398,L02,13:22:32,M,13:58:10,A
399,M18,13:27:11,M,14:21:43,Z
35,M14,13:27:43,Z,14:22:32,M
197,N26,13:28:10,A,14:03:11,M
400,L03,13:28:32,M,14:04:10,A
401,N22,13:33:11,M,14:27:43,Z
36,L09,13:33:43,Z,14:28:32,M
198,L12,13:34:10,A,14:09:11,M
402,N29,13:34:32,M,14:10:10,A
403,N23,13:39:11,M,14:33:43,Z
37,M15,13:39:43,Z,14:34:32,M
199,N27,13:40:10,A,14:15:11,M
404,L04,13:40:32,M,14:16:10,A
405,L11,13:45:11,M,14:39:43,Z
38,N19,13:45:43,Z,14:40:32,M
200,L01,13:46:10,A,14:21:11,M
406,L05,13:46:32,M,14:22:10,A
407,N24,13:51:11,M,14:45:43,Z
39,L10,13:51:43,Z,14:46:32,M
201,N28,13:52:10,A,14:27:11,M
408,N30,13:52:32,M,14:28:10,A
409,N25,13:57:11,M,14:51:43,Z
40,M16,13:57:43,Z,14:52:32,M
202,L02,13:58:10,A,14:33:11,M
410,L06,13:58:32,M,14:34:10,A
411,N26,14:03:11,M,14:57:43,Z
41,N20,14:03:43,Z,14:58:32,M
203,L03,14:04:10,A,14:39:11,M
412,L07,14:04:32,M,14:40:10,A
413,L12,14:09:11,M,15:03:43,Z
42,M17,14:09:43,Z,15:04:32,M
204,N29,14:10:10,A,14:45:11,M
414,M13,14:10:32,M,14:46:10,A
415,N27,14:15:11,M,15:09:43,Z
43,N21,14:15:43,Z,15:10:32,M
205,L04,14:16:10,A,14:51:11,M
416,L08,14:16:32,M,14:52:10,A
417,L01,14:21:11,M,15:15:43,Z
44,M18,14:21:43,Z,15:16:32,M
206,L05,14:22:10,A,14:57:11,M
418,M14,14:22:32,M,14:58:10,A
419,N28,14:27:11,M,15:21:43,Z
45,N22,14:27:43,Z,15:22:32,M
207,N30,14:28:10,A,15:03:11,M
420,L09,14:28:32,M,15:04:10,A
421,L02,14:33:11,M,15:27:43,Z
46,N23,14:33:43,Z,15:28:32,M
208,L06,14:34:10,A,15:09:11,M
422,M15,14:34:32,M,15:10:10,A
423,L03,14:39:11,M,15:33:43,Z
47,L11,14:39:43,Z,15:34:32,M
209,L07,14:40:10,A,15:15:11,M
424,N19,14:40:32,M,15:16:10,A
425,N29,14:45:11,M,15:39:43,Z
48,N24,14:45:43,Z,15:40:32,M
210,M13,14:46:10,A,15:21:11,M
426,L10,14:46:32,M,15:22:10,A
427,L04,14:51:11,M,15:45:43,Z
49,N25,14:51:43,Z,15:46:32,M
211,L08,14:52:10,A,15:27:11,M
428,M16,14:52:32,M,15:28:10,A
429,L05,14:57:11,M,15:51:43,Z
50,N26,14:57:43,Z,15:52:32,M
212,M14,14:58:10,A,15:33:11,M
430,N20,14:58:32,M,15:34:10,A

\"""

### 3B formulation
Based on the data provided in the schedule, here are some key observations and potential insights:

### General Observations:
- The schedule appears to be for a series of flights or train trips.
- Each entry includes a departure time, arrival time, flight/train number, and sometimes additional information like origin/destination.

### Key Points:
1. **Frequency**: There seems to be a consistent frequency in the times, with many entries occurring every hour or half-hour.
2. **Time Ranges**: The schedule covers a wide range of hours from 03:46 AM to 15:58 PM (or later).
3. **Diverse Destinations/Origins**: There are multiple origin and destination pairs listed, indicating a diverse network.

### Specific Observations:
- **Flight/Night Train Schedule**:
  - Many entries show flights or night trains departing at times like 03:46 AM, 04:15 PM, etc.
  - Some specific examples include flights/trains leaving from and arriving at places like "LAX" (Los Angeles International Airport), "JFK" (John F. Kennedy Airport), and various cities in the US.

- **Train Schedule**:
  - There are entries for night trains that operate between different cities, such as New York City to other eastern US cities.
  
### Potential Insights:
1. **Travel Patterns**: The consistent frequency of departures suggests a high volume of travelers during certain times of day or week.
2. **Network Coverage**: The wide range of destinations and the presence of multiple origin/destination pairs indicate a comprehensive network covering major metropolitan areas in the United States.
3. **Operational Scheduling**: The detailed schedule might be useful for operational planning, such as crew scheduling, maintenance schedules, and passenger flow management.

### Summary:
The provided data represents a comprehensive travel schedule that covers both domestic and international flights/trains, operating from various airports and cities across the US. This type of schedule is crucial for ensuring smooth operations in transportation networks.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{ij} \): Binary variable indicating whether task \( i \) is assigned to driver \( j \) (1 if assigned, 0 otherwise).
- \( t_{ij} \): Continuous variable representing the start time of task \( i \) for driver \( j \).
- \( d_{ij} \): Continuous variable representing the end time of task \( i \) for driver \( j \).

### Constraints:
1. **Task Assignment Constraint**: Each task can only be assigned to one driver.
   $$
   \sum_{j=1}^{J} x_{ij} = 1, \quad \forall i
   $$
2. **Driver Task Time Constraint**: The start and end times of a task must be within the driver's working hours.
   $$
   t_{ij} \geq \text{Start Time of Task } i, \quad \forall i, j
   $$
   $$
   d_{ij} \leq \text{End Time of Task } i, \quad \forall i, j
   $$
3. **Driver Working Time Constraint**: The working time of a driver must not exceed the maximum working time.
   $$
   \sum_{i=1}^{I} (d_{ij} - t_{ij}) \leq \text{Maximum Working Time}, \quad \forall j
   $$
4. **Driver Task Continuity Constraint**: Ensure that the tasks of a driver are continuous.
   $$
   t_{ij} \geq d_{i-1,j} + \text{Minimum Rest Time}, \quad \forall i > 1, j
   $$
5. **Driver Task Location Constraint**: Ensure that the tasks of a driver are within the specified location range.
   $$
   \text{Location of Task } i \text{ is within the specified range}, \quad \forall i, j
   $$

### Objective:
Minimize the number of drivers:
$$
\min \sum_{j=1}^{J} \left( \sum_{i=1}^{I} x_{ij} \right)
$$

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("SubwayScheduling")

# Data
tasks = pd.read_csv("TaskInformationTable.csv")
stations = pd.read_csv("MileageInformationTable.csv")
max_work_time = 8 * 60  # Maximum working time in minutes
min_rest_time = 15  # Minimum rest time in minutes

# Decision variables
I = len(tasks)  # Number of tasks
J = 40  # Assume there are 40 drivers
x = model.addVars(I, J, vtype=COPT.BINARY, nameprefix = "x")
t = model.addVars(I, J, vtype=COPT.CONTINUOUS, nameprefix = "t")
d = model.addVars(I, J, vtype=COPT.CONTINUOUS, nameprefix = "d")

# Constraints
# Task assignment constraint
for i in range(I):
    model.addConstr(sum(x[i, j] for j in range(J)) == 1)

# Driver task time constraint
for i in range(I):
    for j in range(J):
        model.addConstr(t[i, j] >= tasks.loc[i, "Pickup Time"])
        model.addConstr(d[i, j] <= tasks.loc[i, "Drop-off Time"])

# Driver working time constraint
for j in range(J):
    model.addConstr(sum(d[i, j] - t[i, j] for i in range(I)) <= max_work_time)

# Driver task continuity constraint
for j in range(J):
    for i in range(1, I):
        model.addConstr(t[i, j] >= d[i-1, j] + min_rest_time)

# Objective
model.setObjective(sum(x[i, j] for i in range(I) for j in range(J)), sense=COPT.MINIMIZE)

# Solve the model
model.solve()

# Output the results
if model.Status == COPT.OPTIMAL:
    print("Optimal number of drivers:", model.objval)
    for j in range(J):
        if sum(x[i, j].x for i in range(I)) > 0:
            print(f"Driver {j+1} tasks:")
            for i in range(I):
                if x[i, j].x > 0.5:
                    print(f"  Task {i+1} from {tasks.loc[i, 'Pickup Time']} to {tasks.loc[i, 'Drop-off Time']}")
```
This script sets up the decision variables, constraints, and objective function, and solves the model to find the optimal number of drivers and their task assignments.

---

## Case 44  [WRONG_FORMULATION]

**GT:** 240000.0  |  **3B:** 3220.0 (Optimal)  |  **8B:** 268000.0

### Question
Vicky and David just bought a farm in the Yarra Valley and are considering using it to grow apples, pears, oranges, and lemons. The profit from growing one acre of apples is $2000, of pears is $1800, of oranges is $2200, and of lemons is $3000. In order to maximize profit, how many acres of land should they use to grow each fruit?
Vicky and David just bought a farm in the Yarra Valley and are considering using it to grow apples, pears, oranges, and lemons. The total land area is 120 acres.

The land area for growing apples should be at least twice the land area for growing pears.

The land area for growing apples should be at least three times the land area for growing lemons.

The land area for growing oranges must be twice the land area for growing lemons.

Vicky and David are not willing to grow more than two types of fruit.

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Fruit_Growing_Problem", LpMaximize)

# Decision variables: acres for each type of fruit
acres_apples = LpVariable('apples', lowBound=0, cat='Continuous')
acres_pears = LpVariable('pears', lowBound=0, cat='Continuous')
acres_oranges = LpVariable('oranges', lowBound=0, cat='Continuous')
acres_lemons = LpVariable('lemons', lowBound=0, cat='Continuous')

# Objective function: maximize total profit
prob += 2000*acres_apples + 1800*acres_pears + 2200*acres_oranges + 3000*acres_lemons

# Constraints:
# Total land area constraint
prob += acres_apples + acres_pears + acres_oranges + acres_lemons <= 120

# Apples and pears constraint: at least twice the land area for pears
prob += acres_apples >= 2*acres_pears

# Apples and lemons constraint: at least three times the land area for lemons
prob += acres_apples >= 3*acres_lemons

# Oranges and lemons constraint: twice the land area for lemons
prob += acres_oranges == 2*acres_lemons

# Limit to two types of fruit
prob += (acres_apples + acres_pears) <= 1
prob += (acres_apples + acres_oranges) <= 1
prob += (acres_apples + acres_lemons) <= 1
prob += (acres_pears + acres_oranges) <= 1
prob += (acres_pears + acres_lemons) <= 1
prob += (acres_oranges + acres_lemons) <= 1

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: ${value(prob.objective)}")
```

This code sets up and solves a linear programming problem using PuLP to determine how many acres of land Vicky and David should use for each type of fruit (apples, pears, oranges, lemons) to maximize their profit while adhering to the constraints provided.

### ORLM-8B formulation
## Mathematical Model:
To help Vicky and David maximize the profit from their farm, we can construct a linear programming model to determine the optimal land area for growing each fruit. Here is the detailed formulation of the model:

### Decision Variables:
- \(a\): Land area for growing apples (in acres).
- \(p\): Land area for growing pears (in acres).
- \(o\): Land area for growing oranges (in acres).
- \(l\): Land area for growing lemons (in acres).

### Objective Function:
- Maximize total profit: \(Z = 2000a + 1800p + 2200o + 3000l\)

### Constraints:
1. Total land area constraint: \(a + p + o + l \leq 120\)
2. Land area for growing apples should be at least twice the land area for growing pears: \(a \geq 2p\)
3. Land area for growing apples should be at least three times the land area for growing lemons: \(a \geq 3l\)
4. Land area for growing oranges must be twice the land area for growing lemons: \(o = 2l\)
5. Vicky and David are not willing to grow more than two types of fruit, which means we need to select two fruits to grow. This can be achieved by introducing binary variables and additional constraints, but for simplicity, we assume they will grow all four types of fruit.

### Non-negativity Constraints:
- \(a, p, o, l \geq 0\)

### Integer Constraints:
- \(a, p, o, l\) must be integers, as land area cannot be divided into fractions.

Using this model, we can apply linear programming techniques to find the optimal land area for growing each fruit, subject to the given constraints, in order to maximize the total profit. This will provide Vicky and David with an optimal planting strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the farm planting problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("FarmPlantingOptimization")

# Add decision variables
a = model.addVar(vtype=COPT.INTEGER, name="Apples")
p = model.addVar(vtype=COPT.INTEGER, name="Pears")
o = model.addVar(vtype=COPT.INTEGER, name="Oranges")
l = model.addVar(vtype=COPT.INTEGER, name="Lemons")

# Set the objective function
model.setObjective(2000*a + 1800*p + 2200*o + 3000*l, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(a + p + o + l <= 120, name="TotalLandArea")
model.addConstr(a >= 2*p, name="ApplePearRatio")
model.addConstr(a >= 3*l, name="AppleLemonRatio")
model.addConstr(o == 2*l, name="OrangeLemonRatio")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: ${:.2f}".format(model.objval))
    print("Land area for growing apples: {:.2f} acres".format(a.x))
    print("Land area for growing pears: {:.2f} acres".format(p.x))
    print("Land area for growing oranges: {:.2f} acres".format(o.x))
    print("Land area for growing lemons: {:.2f} acres".format(l.x))
else:
    print("No optimal solution found.")
```

This script first creates a COPT environment and model. Then, it adds four decision variables `a`, `p`, `o`, and `l`, representing the land area for growing apples, pears, oranges, and lemons, respectively.

Next, the script sets the objective function, which is to maximize the total profit. The objective function is the sum of the profit from each fruit multiplied by its corresponding land area.

Then, the script adds four constraints:
1. Total land area should not exceed 120 acres.
2. Land area for growing apples should be at least twice the land area for growing pears.
3. Land area for growing apples should be at least three times the land area for growing lemons.
4. Land area for growing oranges must be twice the land area for growing lemons.

Finally, the script solves the model and outputs the results. If an optimal solution is found, it prints the maximized total profit and the optimal land area for growing each fruit. If no optimal solution is found, it outputs the corresponding message.

This script provides Vicky and David with an optimal planting strategy to maximize the total profit from their farm, subject to the given constraints.

---

## Case 45  [WRONG_FORMULATION]

**GT:** 21.0  |  **3B:** 1362.0 (Optimal)  |  **8B:** 640.0

### Question
A farmer needs to transport 1000 units of fresh agricultural products from the farm to a nearby market. The farmer has three transportation options: horses, bicycles, and hand carts. Due to the physical exertion required for bicycles and hand carts, the farmer only wants to choose one of these two transportation methods. Horses produce 80 units of pollution per trip, bicycles produce 0 units of pollution, and hand carts produce 0 units of pollution. The total pollution generated by all trips must not exceed 1000 units. The farmer needs to use horses for at least 8 trips. Horses, bicycles, and hand carts can each carry 55 units, 30 units, and 40 units of products per trip, respectively. The farmer needs to ensure that the total quantity of transported products is at least 1000 units.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpInteger

# Create a problem
prob = LpProblem("FarmerTransportation", LpMinimize)

# Decision variables: number of trips for each mode of transportation
horses_trips = LpVariable('HorsesTrips', lowBound=8, cat=LpInteger)
bicycles_trips = LpVariable('BicyclesTrips', 0, 1, cat=LpInteger) # Limited to 1 trip at most
hand_carts_trips = LpVariable('HandCartsTrips', 0, 1, cat=LpInteger) # Limited to 1 trip at most

# Objective function: minimize pollution (since the problem doesn't specify a cost for trips)
prob += lpSum([80 * horses_trips + bicycles_trips + hand_carts_trips]), "Total_Pollution"

# Constraints
# Total quantity of transported products must be at least 1000 units
prob += lpSum([55 * horses_trips, 30 * bicycles_trips, 40 * hand_carts_trips]) >= 1000, "Product_Quantity_Constraint"

# Solve the problem
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Pollution Generated =", value(prob.objective))
```

Please note that this model assumes minimizing pollution as the objective function. If you intended to maximize profit or minimize cost (which is not specified), please clarify and adjust accordingly. The constraints ensure at least 1000 units of products are transported, with a minimum of 8 trips using horses, and limits on bicycles and hand carts to one trip each.

### ORLM-8B formulation
## Mathematical Model:
To solve the farmer's transportation problem, we need to construct a linear programming model to minimize the total pollution while satisfying the transportation demand and constraints. Here is the model formulation:

### Decision Variables:
- \(x_1\): Number of trips using horses.
- \(x_2\): Number of trips using bicycles.
- \(x_3\): Number of trips using hand carts.
- \(y_2\): Binary variable indicating whether bicycles are chosen (1) or not (0).
- \(y_3\): Binary variable indicating whether hand carts are chosen (1) or not (0).

### Objective Function:
- Minimize total pollution: \[Z = 80x_1\]

### Constraints:
1. Pollution constraint: \[80x_1 + 0x_2 + 0x_3 \leq 1000\]
2. Minimum trips using horses: \[x_1 \geq 8\]
3. At least one of bicycles or hand carts must be chosen: \[y_2 + y_3 \geq 1\]
4. If bicycles are chosen, the number of trips using bicycles must be at least 1: \[x_2 \geq y_2\]
5. If hand carts are chosen, the number of trips using hand carts must be at least 1: \[x_3 \geq y_3\]
6. Total quantity of transported products: \[55x_1 + 30x_2 + 40x_3 \geq 1000\]

### Non-negativity Constraints:
- \(x_1, x_2, x_3 \geq 0\)
- \(y_2, y_3 \in \{0, 1\}\)

Using this model, we can apply linear programming techniques to find the optimal number of trips using horses, bicycles, and hand carts that minimize the total pollution while satisfying the transportation demand and constraints. This will provide the farmer with an economically efficient transportation strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("FarmTransportation")

# Add decision variables
x1 = model.addVar(vtype=COPT.INTEGER, name="x1")  # Number of trips using horses
x2 = model.addVar(vtype=COPT.INTEGER, name="x2")  # Number of trips using bicycles
x3 = model.addVar(vtype=COPT.INTEGER, name="x3")  # Number of trips using hand carts
y2 = model.addVar(vtype=COPT.BINARY, name="y2")   # Whether bicycles are chosen
y3 = model.addVar(vtype=COPT.BINARY, name="y3")   # Whether hand carts are chosen

# Objective function: Minimize total pollution
model.setObjective(80 * x1, sense=COPT.MINIMIZE)

# Constraints
model.addConstr(80 * x1 + 0 * x2 + 0 * x3 <= 1000, name="PollutionLimit")
model.addConstr(x1 >= 8, name="MinHorseTrips")
model.addConstr(y2 + y3 >= 1, name="AtLeastOneNonPolluting")
model.addConstr(x2 >= y2, name="BikeLogic")
model.addConstr(x3 >= y3, name="CartLogic")
model.addConstr(55 * x1 + 30 * x2 + 40 * x3 >= 1000, name="TotalTransport")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total pollution: {:.2f} units".format(model.objval))
    print("Number of trips using horses: {:.2f}".format(x1.x))
    print("Number of trips using bicycles: {:.2f}".format(x2.x))
    print("Number of trips using hand carts: {:.2f}".format(x3.x))
    print("Whether bicycles are chosen: {}".format(int(y2.x)))
    print("Whether hand carts are chosen: {}".format(int(y3.x)))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total pollution and the number of trips using each transportation method.

This script provides a complete example of using the `coptpy` library to solve the farmer's transportation problem while satisfying all the constraints mentioned in the problem.

---

## Case 46  [WRONG_FORMULATION]

**GT:** 530  |  **3B:** 870.0 (Optimal)  |  **8B:** 4240.0

### Question
A hospital requires the following number of nurses during different time periods within a 24-hour day: 2:00-6:00 - 10 nurses, 6:00-10:00 - 15 nurses, 10:00-14:00 - 25 nurses, 14:00-18:00 - 20 nurses, 18:00-22:00 - 18 nurses, 22:00-2:00 - 12 nurses. Nurses work in 6 batches at 2:00, 6:00, 10:00, 14:00, 18:00, and 22:00, and work continuously for 8 hours. Determine if the hospital should hire contract nurses who work the same hours as regular nurses. If the salary for regular nurses is $10/hour and for contract nurses is $15/hour, how many contract nurses should the hospital hire?

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMaximize

# Create a problem
prob = LpProblem("Hospital_Nurse_Planning", LpMinimize)

# Define decision variables: number of contract nurses for each shift
contract_nurses_2_to_6 = LpVariable('contract_nurses_2_to_6', lowBound=0, cat='Continuous')
contract_nurses_6_to_10 = LpVariable('contract_nurses_6_to_10', lowBound=0, cat='Continuous')
contract_nurses_10_to_14 = LpVariable('contract_nurses_10_to_14', lowBound=0, cat='Continuous')
contract_nurses_14_to_18 = LpVariable('contract_nurses_14_to_18', lowBound=0, cat='Continuous')
contract_nurses_18_to_22 = LpVariable('contract_nurses_18_to_22', lowBound=0, cat='Continuous')

# Objective function: minimize the cost of hiring contract nurses
prob += lpSum([15 * (contract_nurses_2_to_6 + contract_nurses_6_to_10 + contract_nurses_10_to_14 + contract_nurses_14_to_18 + contract_nurses_18_to_22)])

# Constraints: number of nurses required during each time period
prob += lpSum([contract_nurses_2_to_6, contract_nurses_6_to_10, contract_nurses_10_to_14, contract_nurses_14_to_18, contract_nurses_18_to_22]) >= 10

prob += lpSum([contract_nurses_2_to_6, contract_nurses_6_to_10]) >= 15

prob += lpSum([contract_nurses_10_to_14, contract_nurses_14_to_18]) >= 25

prob += lpSum([contract_nurses_14_to_18, contract_nurses_18_to_22]) >= 20

prob += lpSum([contract_nurses_18_to_22]) >= 18

# Solve the problem
prob.solve()

# Print the number of contract nurses hired for each shift
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total cost: ${value(prob.objective):.2f}")
```

This code sets up a linear programming model to determine how many contract nurses (working at $15/hour) the hospital should hire, given that regular nurses work at $10/hour and are already sufficient for all required shifts. The total cost is minimized by solving this problem.

### ORLM-8B formulation
## Mathematical Model:
To solve the hospital's nurse scheduling problem, we need to construct a linear programming model to determine if the hospital should hire contract nurses and how many contract nurses should be hired. The model is as follows:

### Decision Variables:
- \(x_j\): The number of regular nurses starting work at time \(j\), where \(j = 1, 2, 3, 4, 5, 6\) corresponds to the start times of 2:00, 6:00, 10:00, 14:00, 18:00, and 22:00, respectively.
- \(y_j\): The number of contract nurses starting work at time \(j\).

### Objective Function:
- Minimize total cost: \[Z = 10 \times 8 \times \sum_{j=1}^{6} x_j + 15 \times 8 \times \sum_{j=1}^{6} y_j\]
  - This function calculates the total cost of regular and contract nurses, where regular nurses are paid $10/hour and contract nurses are paid $15/hour, and both work for 8 hours.

### Constraints:
1. Nurse requirements for each time period:
   - \(x_1 + x_6 + y_1 + y_6 \geq 10\) (2:00-6:00)
   - \(x_1 + x_2 + y_1 + y_2 \geq 15\) (6:00-10:00)
   - \(x_2 + x_3 + y_2 + y_3 \geq 25\) (10:00-14:00)
   - \(x_3 + x_4 + y_3 + y_4 \geq 20\) (14:00-18:00)
   - \(x_4 + x_5 + y_4 + y_5 \geq 18\) (18:00-22:00)
   - \(x_5 + x_6 + y_5 + y_6 \geq 12\) (22:00-2:00)
2. Non-negativity constraints:
   - \(x_j, y_j \geq 0\), for all \(j = 1, 2, 3, 4, 5, 6\)

### Integer Constraints:
- \(x_j, y_j\) must be integers, as the number of nurses cannot be fractional.

Using this model, we can apply linear programming techniques to find the optimal number of regular and contract nurses that minimize the total cost while meeting the nurse requirements for each time period. This will provide the hospital with an economically efficient nurse scheduling strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the hospital nurse scheduling problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("NurseScheduling")

# Define decision variables
x = [model.addVar(vtype=COPT.INTEGER, name=f"x_{j}") for j in range(1, 7)]
y = [model.addVar(vtype=COPT.INTEGER, name=f"y_{j}") for j in range(1, 7)]

# Define the objective function
model.setObjective(10 * 8 * cp.quicksum(x) + 15 * 8 * cp.quicksum(y), sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(x[0] + x[5] + y[0] + y[5] >= 10, name="Demand_2_6")
model.addConstr(x[0] + x[1] + y[0] + y[1] >= 15, name="Demand_6_10")
model.addConstr(x[1] + x[2] + y[1] + y[2] >= 25, name="Demand_10_14")
model.addConstr(x[2] + x[3] + y[2] + y[3] >= 20, name="Demand_14_18")
model.addConstr(x[3] + x[4] + y[3] + y[4] >= 18, name="Demand_18_22")
model.addConstr(x[4] + x[5] + y[4] + y[5] >= 12, name="Demand_22_2")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: ${:.2f}".format(model.objval))
    print("Nurse scheduling:")
    for j in range(6):
        print(f"Start time {j*4+2}:00 - {j*4+6}:00, Regular nurses: {x[j].x}, Contract nurses: {y[j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we define the decision variables `x` and `y`, representing the number of regular and contract nurses starting work at each time period.

Next, the script sets the objective function, which is to minimize the total cost, including the salaries of regular and contract nurses.

Then, the script adds constraints to ensure that the nurse requirements for each time period are met.

Finally, the script solves the model and outputs the minimum total cost and the nurse scheduling for each time period.

Note that the script assumes that the start times for each time period are 2:00, 6:00, 10:00, 14:00, 18:00, and 22:00, and each nurse works for 8 hours. You can adjust the script according to your specific requirements.

---

## Case 47  [WRONG_FORMULATION]

**GT:** 978400  |  **3B:** 541000.0 (Optimal)  |  **8B:** 1169200.0

### Question
A person has a capital of 300,000 yuan and has the following investment projects for the next three years:
(1) Each year at the beginning of the year, the investment can be made, and the profit each year is 20% of the investment amount, and the principal and interest can be used together for the next year's investment;
(2) Only allowed to invest at the beginning of the first year, can be recovered at the end of the second year, and the total principal and interest is 150% of the investment amount, but the investment limit for this type of investment does not exceed 150,000 yuan;
(3) Allowed to invest at the beginning of the second year within three years, can be recovered at the end of the third year, and the total principal and interest is 160% of the investment amount, with an investment limit of 200,000 yuan;
(4) Allowed to invest at the beginning of the third year within three years, recoverable within one year, with a profit of 40% and an investment limit of 100,000 yuan.
Chapter 1 Linear Programming and Simplex Method
Try to determine an investment plan that maximizes the total principal and interest at the end of the third year for this person.

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Investment_Problem", LpMaximize)

# Define decision variables
x1 = LpVariable('Investment_Year1', lowBound=0)
x2 = LpVariable('Investment_Year2', lowBound=0, upBound=200000)
x3 = LpVariable('Investment_Year3', lowBound=0)

# Objective function: Maximize total principal and interest at the end of Year 3
prob += x1 + 0.2 * x1 + (1.5 * x1) + 0.4 * (1.6 * x2 - 0.4 * x2) + 0.4 * (1.4 * x3 - 0.4 * x3)

# Constraints
prob += x1 <= 150000, "Investment_Year1_Constraint"
prob += x2 <= 200000, "Investment_Year2_Constraint"
prob += x3 <= 100000, "Investment_Year3_Constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Principal and Interest at end of Year 3: {prob.objective.value()}")
```

This code sets up a linear programming model to maximize the total principal and interest at the end of the third year, considering all investment options. The constraints ensure that the investments do not exceed their respective limits.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \(x_{ij}\): Represents the amount of funds invested in project \(j\) at the beginning of year \(i\), where \(i = 1, 2, 3\) represents the year, and \(j = 1, 2, 3, 4\) represents the project.

### Constraints:
1. **Initial Capital Constraint**:
   \[
   x_{11} + x_{12} \leq 300,000
   \]
   The total investment amount in the first year does not exceed the initial capital.

2. **Annual Investment Amount Constraint**:
   \[
   x_{21} + x_{23} \leq 300,000 + 0.2 \times x_{11} + 1.5 \times x_{12}
   \]
   \[
   x_{31} + x_{34} \leq 300,000 + 0.2 \times x_{21} + 1.6 \times x_{23}
   \]
   The total investment amount in each year does not exceed the principal and interest from the previous year's investment.

3. **Investment Limit Constraint**:
   \[
   x_{12} \leq 150,000
   \]
   \[
   x_{23} \leq 200,000
   \]
   \[
   x_{34} \leq 100,000
   \]
   The investment amount for each project does not exceed its investment limit.

4. **Non-Negativity Constraint**:
   \[
   x_{ij} \geq 0, \quad \forall i, j
   \]
   All investment amounts must be non-negative.

### Objective:
Maximize the total principal and interest at the end of the third year:
\[
\max Z = 1.2 \times x_{31} + 1.6 \times x_{23} + 1.4 \times x_{34}
\]

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create a COPT environment
env = Envr()

# Create a model
model = env.createModel("Investment Planning")

# Add decision variables
x11 = model.addVar(lb=0, vtype=COPT.CONTINUOUS, name='x11')
x12 = model.addVar(lb=0, ub=150000, vtype=COPT.CONTINUOUS, name='x12')
x21 = model.addVar(lb=0, vtype=COPT.CONTINUOUS, name='x21')
x23 = model.addVar(lb=0, ub=200000, vtype=COPT.CONTINUOUS, name='x23')
x31 = model.addVar(lb=0, vtype=COPT.CONTINUOUS, name='x31')
x34 = model.addVar(lb=0, ub=100000, vtype=COPT.CONTINUOUS, name='x34')

# Set the objective function
model.setObjective(1.2 * x31 + 1.6 * x23 + 1.4 * x34, COPT.MAXIMIZE)

# Add constraints
model.addConstr(x11 + x12 <= 300000, name='InitialInvestment')
model.addConstr(x21 + x23 <= 300000 + 0.2 * x11 + 1.5 * x12, name='SecondYearInvestment')
model.addConstr(x31 + x34 <= 300000 + 0.2 * x21 + 1.6 * x23, name='ThirdYearInvestment')

# Solve the model
model.solve()

# Output the results
print('Optimal Total Return: {:.2f}'.format(model.ObjVal))
print('Investment in Project 1 in Year 1: {:.2f}'.format(x11.x))
print('Investment in Project 2 in Year 1: {:.2f}'.format(x12.x))
print('Investment in Project 1 in Year 2: {:.2f}'.format(x21.x))
print('Investment in Project 3 in Year 2: {:.2f}'.format(x23.x))
print('Investment in Project 1 in Year 3: {:.2f}'.format(x31.x))
print('Investment in Project 4 in Year 3: {:.2f}'.format(x34.x))
```
This script sets up and solves the investment planning problem using the COPT Python API, aiming to maximize the total return at the end of the third year while adhering to the constraints on initial capital, annual investment limits, and project-specific investment caps.

---

## Case 48  [SOLVE_FAILED]

**GT:** 4848  |  **3B:** 22500.000450000003 (Unbounded)  |  **8B:** -0.0

### Question
A candy factory processes raw materials A, B, and C into three different types of candies: A, B, and C. The content of A, B, and C in each type of candy, the cost of raw materials, the monthly limit of each raw material, and the processing fee and selling price of the three types of candies are shown in Table 1-7.
Table 1-7
\begin{tabular}{c|ccc|c|c}
\hline Item & A & B & C & Raw Material Cost (元/kg) & Monthly Limit (kg) \\
\hline A & $\geqslant 60 \%$ & $\geqslant 15 \%$ & & 2.00 & 2000 \\
B & & & & 1.50 & 2500 \\
C & $\leqslant 20 \%$ & $\leqslant 60 \%$ & $\leqslant 50 \%$ & 1.00 & 1200 \\
\hline Processing Fee (元/kg) & 0.50 & 0.40 & 0.30 & & \\
Selling Price (元/kg) & 3.40 & 2.85 & 2.25 & & \\
\hline
\end{tabular}

What is the monthly production of each type of candy in kg that maximizes the profit of the factory?

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Candy_Factory_Profit_Maximization", LpMaximize)

# Define decision variables
x_A = LpVariable('x_A', lowBound=0)
x_B = LpVariable('x_B', lowBound=0)
x_C = LpVariable('x_C', lowBound=0)

# Objective function: maximize profit
profit_function = 3.4 * x_A + 2.85 * x_B + 2.25 * x_C - (2 * x_A + 1.5 * x_B + 1 * x_C)
prob += profit_function

# Constraints for raw materials A, B, and C
constraint_A = 0.6 * x_A + 0.0 * x_B + (-0.2) * x_C <= 2000
prob += constraint_A

constraint_B = 0.0 * x_A + 0.15 * x_B + (-0.6) * x_C <= 2500
prob += constraint_B

constraint_C = (-0.2) * x_A + (-0.4) * x_B + 0.5 * x_C <= 1200
prob += constraint_C

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {value(prob.objective)}")
```

Please note that there are some issues with the formulation of constraints for raw materials A, B, and C. The values provided (60%, 15%, -20%) do not make sense in a linear programming context because they represent percentages or limits on the content of each type of candy rather than direct quantities of raw material usage. In this case, we would need to reformulate these constraints based on how much of A, B, and C are used directly from raw materials A, B, and C. Since no such information is provided in the problem statement, I have assumed that the percentages represent limits on the content rather than quantities of raw material usage. If you can provide more details about how to formulate these constraints correctly, I would be happy to adjust the model accordingly.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem for the candy factory, we will establish a linear programming model to maximize the profit of the factory while satisfying the content requirements of the candies and the monthly limits of the raw materials. The model can be formulated as follows:

### Decision Variables:
- \(x_A, x_B, x_C\): Represent the production of candies A, B, and C in kg, respectively.

### Objective Function:
- Maximize profit: \[Z = (3.40 - 2.00 - 0.50)x_A + (2.85 - 1.50 - 0.40)x_B + (2.25 - 1.00 - 0.30)x_C\]
  - This function calculates the total profit based on the selling price, raw material cost, and processing fee of each type of candy.

### Constraints:
1. Content requirements of the candies:
   - \(x_A \geq 0.6(x_A + x_B + x_C)\)
   - \(x_B \geq 0.15(x_A + x_B + x_C)\)
   - \(x_C \leq 0.2(x_A + x_B + x_C)\)
   - \(x_A \leq 0.5(x_A + x_B + x_C)\)
   - \(x_B \leq 0.6(x_A + x_B + x_C)\)
   - \(x_C \leq 0.5(x_A + x_B + x_C)\)
2. Monthly limits of the raw materials:
   - \(x_A + x_B + x_C \leq 2000\)
   - \(x_B + x_C \leq 2500\)
   - \(x_A + x_C \leq 1200\)

### Non-negativity Constraints:
- \(x_A, x_B, x_C \geq 0\)

Using this model, we can apply linear programming techniques to find the optimal production quantities of each type of candy that maximize the profit of the factory while satisfying the content requirements of the candies and the monthly limits of the raw materials. This will provide the candy factory with an optimized production strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for the candy factory:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("CandyFactoryOptimization")

# Add decision variables
x_A = model.addVar(lb=0, name="x_A")  # Production of candy A
x_B = model.addVar(lb=0, name="x_B")  # Production of candy B
x_C = model.addVar(lb=0, name="x_C")  # Production of candy C

# Objective function: Maximize profit
profit = (3.40 - 2.00 - 0.50) * x_A + (2.85 - 1.50 - 0.40) * x_B + (2.25 - 1.00 - 0.30) * x_C
model.setObjective(profit, sense=COPT.MAXIMIZE)

# Constraints
# Content requirements of the candies
model.addConstr(x_A >= 0.6 * (x_A + x_B + x_C), name="ContentA")
model.addConstr(x_B >= 0.15 * (x_A + x_B + x_C), name="ContentB")
model.addConstr(x_C <= 0.2 * (x_A + x_B + x_C), name="ContentC")
model.addConstr(x_A <= 0.5 * (x_A + x_B + x_C), name="ContentD")
model.addConstr(x_B <= 0.6 * (x_A + x_B + x_C), name="ContentE")
model.addConstr(x_C <= 0.5 * (x_A + x_B + x_C), name="ContentF")

# Monthly limits of the raw materials
model.addConstr(x_A + x_B + x_C <= 2000, name="MaterialA")
model.addConstr(x_B + x_C <= 2500, name="MaterialB")
model.addConstr(x_A + x_C <= 1200, name="MaterialC")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized profit: {:.2f} yuan".format(model.objval))
    print("Production of candy A: {:.2f} kg".format(x_A.x))
    print("Production of candy B: {:.2f} kg".format(x_B.x))
    print("Production of candy C: {:.2f} kg".format(x_C.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add three decision variables `x_A`, `x_B`, and `x_C`, representing the production of candies A, B, and C in kg, respectively.

Next, we define the objective function, which is to maximize the profit. The profit is calculated based on the selling price, raw material cost, and processing fee of each type of candy.

Then, we add the constraints. The first set of constraints ensures the content requirements of the candies, and the second set of constraints ensures the monthly limits of the raw materials.

Finally, we solve the model and output the results. If an optimal solution is found, we print the maximized profit and the production quantities of each type of candy. Otherwise, we print a message indicating that no optimal solution was found.

This script provides a complete example of using the `coptpy` library to solve the optimization problem for the candy factory and outputs the optimal production strategy.

---

## Case 49  [CODE_BUG]

**GT:** 10755  |  **3B:** None (?)  |  **8B:** 70190.0

### Question
The contract booking numbers for three products, I, II, and III, for each quarter of the next year are shown in Table 1-10.

Table 1-10
\begin{tabular}{c|c|c|c|c}
\hline \multirow{2}{*}{ Product } & \multicolumn{4}{|c}{ Quarter } \\
\cline { 2 - 5 } & 1 & 2 & 3 & 4 \\
\hline I & 1500 & 1000 & 2000 & 1200 \\
II & 1500 & 1500 & 1200 & 1500 \\
III & 1000 & 2000 & 1500 & 2500 \\
\hline
\end{tabular}

At the beginning of the first quarter, there is no inventory for any of the three products. It is required to have 150 units of inventory for each product at the end of the fourth quarter. It is known that the factory has 15,000 hours of production time per quarter, and it takes 2, 4, and 3 hours respectively to produce one unit of products I, II, and III. Due to equipment replacement, product I cannot be produced in the second quarter. It is stipulated that if a product cannot be delivered on time, a compensation of $20 per unit per quarter will be paid for products I and II, and $10 for product III. Additionally, for products produced but not delivered in the same quarter, there is a storage cost of $5 per unit per quarter. How should the factory arrange its production to minimize the total compensation and storage costs?

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Production_Planning", LpMinimize)

# Decision variables: production quantities for each product in each quarter
x11, x12, x13, x14 = LpVariable('x11', lowBound=0), LpVariable('x12', lowBound=0), LpVariable('x13', lowBound=0), LpVariable('x14', lowBound=0)
x21, x22, x23, x24 = LpVariable('x21', lowBound=0), LpVariable('x22', lowBound=0), LpVariable('x23', lowBound=0), LpVariable('x24', lowBound=0)
x31, x32, x33, x34 = LpVariable('x31', lowBound=0), LpVariable('x32', lowBound=0), LpVariable('x33', lowBound=0), LpVariable('x34', lowBound=0)

# Objective function: minimize total compensation and storage costs
prob += lpSum[(20 * x12 + 10 * x22 + 5 * (x12 - x21) + 5 * (x22 - x31)) for x12, x22 in [(x12, x22), (x22, x32)] if x12 > 0 or x22 > 0] \
       + lpSum[(20 * x14 + 10 * x24 + 5 * (x14 - x23) + 5 * (x24 - x33)) for x14, x24 in [(x14, x24), (x24, x34)] if x14 > 0 or x24 > 0] \
       + lpSum[3*x11 + 4*x21 + 3*x31 - 150 for i in [x11, x21, x31]]

# Constraints: production quantities
prob += 2*x11 + 4*x21 + 3*x31 <= 15000

# Constraints: inventory at the end of each quarter
prob += 1500 - (x11 + x21 + x31) == 150
prob += 1000 - (x12 + x22 + x32) == 150
prob += 2000 - (x13 + x23 + x33) == 150
prob += 1200 - (x14 + x24 + x34) == 150

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Cost: {value(prob.objective)}")
```

This code sets up and solves a linear programming model to minimize total compensation and storage costs for production planning, considering the constraints provided.

### ORLM-8B formulation
## Mathematical Model:
To solve the production planning problem for the factory, we need to construct a mathematical model to minimize the total compensation and storage costs while satisfying the production time constraint, product demand, and inventory requirements. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): The quantity of product \(i\) produced in quarter \(j\), where \(i\) represents the products (I, II, III) and \(j\) represents the quarters (1, 2, 3, 4).
- \(s_{ij}\): The quantity of product \(i\) stored at the end of quarter \(j\).
- \(d_{ij}\): The quantity of product \(i\) delivered in quarter \(j\).
- \(c_{ij}\): The quantity of product \(i\) for which compensation is paid in quarter \(j\).

### Objective Function:
- Minimize the total compensation and storage costs: \[Z = \sum_{i \in \{I, II, III\}} \sum_{j \in \{1, 2, 3, 4\}} (5s_{ij} + 20c_{i1} + 20c_{i2} + 10c_{i3} + 10c_{i4})\]

### Constraints:
1. Production time constraint: \[\sum_{i \in \{I, II, III\}} \sum_{j \in \{1, 2, 3, 4\}} \text{time}_{i} \cdot x_{ij} \leq 15000\]
2. Product demand satisfaction: \[d_{ij} = \text{demand}_{ij}, \forall i, j\]
3. Inventory balance: \[s_{i, j-1} + x_{ij} - d_{ij} = s_{ij}, \forall i, j\]
4. End-of-year inventory requirement: \[s_{i3} + x_{i4} - d_{i4} = 150, \forall i\]
5. Product I cannot be produced in the second quarter: \[x_{I2} = 0\]
6. Non-negativity constraints: \[x_{ij}, s_{ij}, d_{ij}, c_{ij} \geq 0, \forall i, j\]

### Integer Constraints:
- \(x_{ij}, s_{ij}, d_{ij}, c_{ij}\) must be integers, as the quantities of products cannot be fractions.

Using this model, we can apply integer linear programming techniques to find the optimal production and delivery quantities for each product in each quarter, while minimizing the total compensation and storage costs, while satisfying all production time constraints, product demand, and inventory requirements. This will provide the factory with an optimized production and delivery plan.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the production planning problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ProductionPlanning")

# Define products and quarters
products = ['I', 'II', 'III']
quarters = [1, 2, 3, 4]

# Define demand
demand = {
    'I': [1500, 0, 2000, 1200],
    'II': [1500, 1500, 1200, 1500],
    'III': [1000, 2000, 1500, 2500]
}

# Define production time
production_time = {'I': 2, 'II': 4, 'III': 3}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for i in products for j in quarters}
s = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"s_{i}_{j}") for i in products for j in quarters}
d = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"d_{i}_{j}") for i in products for j in quarters}
c = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"c_{i}_{j}") for i in products for j in quarters}

# Objective function: Minimize total compensation and storage costs
model.setObjective(cp.quicksum(5 * s[i, j] + 20 * c[i, 1] + 20 * c[i, 2] + 10 * c[i, 3] + 10 * c[i, 4] for i in products for j in quarters), sense=COPT.MINIMIZE)

# Constraints
# Production time constraint
model.addConstr(cp.quicksum(production_time[i] * x[i, j] for i in products for j in quarters) <= 15000, name="ProductionTime")

# Product demand satisfaction
for i in products:
    for j in quarters:
        model.addConstr(d[i, j] == demand[i][j-1], name=f"Demand_{i}_{j}")

# Inventory balance
for i in products:
    for j in quarters[1:]:
        model.addConstr(s[i, j-1] + x[i, j] - d[i, j] == s[i, j], name=f"InventoryBalance_{i}_{j}")

# End-of-year inventory requirement
for i in products:
    model.addConstr(s[i, 3] + x[i, 4] - d[i, 4] == 150, name=f"EndOfYearInventory_{i}")

# Product I cannot be produced in the second quarter
model.addConstr(x['I', 2] == 0, name="NoProductionInQ2ForI")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total compensation and storage costs: {:.2f}".format(model.objval))
    for i in products:
        for j in quarters:
            print(f"Quantity of product {i} produced in quarter {j}: {x[i, j].x}")
            print(f"Quantity of product {i} stored at the end of quarter {j}: {s[i, j].x}")
            print(f"Quantity of product {i} delivered in quarter {j}: {d[i, j].x}")
            print(f"Quantity of product {i} for which compensation is paid in quarter {j}: {c[i, j].x}")
else:
    print("No optimal solution found.")
```

This script defines the products, quarters, demand, and production time, and creates decision variables `x`, `s`, `d`, and `c` to represent the production, storage, delivery, and compensation quantities for each product in each quarter.

The objective function is to minimize the total compensation and storage costs, calculated using the `cp.quicksum` function to sum up the storage costs and compensation costs for all products and quarters.

The constraints include the production time constraint, product demand satisfaction, inventory balance, end-of-year inventory requirement, and the constraint that product I cannot be produced in the second quarter.

Finally, the script solves the model and outputs the minimum total compensation and storage costs, as well as the production, storage, delivery, and compensation quantities for each product in each quarter.

Note that this script assumes you have installed the `coptpy` library and have a valid license. If you do not have a license, you can consider using other optimization libraries such as `PuLP` or `OR-Tools`.

---

## Case 50  [SOLVE_FAILED]

**GT:** 118400  |  **3B:** None (Not Solved)  |  **8B:** 294600.0

### Question
A factory needs to rent a warehouse to store materials for the next 4 months. The required warehouse area for each month is listed in Table 1-14.
Table 1-14
\begin{tabular}{c|c|c|c|c}
\hline Month & 1 & 2 & 3 & 4 \\
\hline Required Warehouse Area $/ \mathrm{m}^2$ & 1500 & 1000 & 2000 & 1200 \\
\hline
\end{tabular}

The longer the rental contract period, the greater the discount on warehouse rental fees. The specific data is listed in Table 1-15.
Table 1-15
\begin{tabular}{c|c|c|c|c}
\hline Contract Rental Period $/$ months & 1 & 2 & 3 & 4 \\
\hline \begin{tabular}{c} 
Rental Fee for Warehouse \\
Area within the Contract Period $/ \mathrm{m}^2$
\end{tabular} & 28 & 45 & 60 & 73 \\
\hline
\end{tabular}

The warehouse rental contract can be processed at the beginning of each month, and each contract specifies the rental area and period. Therefore, the factory can rent a contract on any month, and each time, they can sign one contract or multiple contracts with different rental areas and rental periods. The overall goal is to minimize the rental fees paid. Try to establish a linear programming mathematical model based on the above requirements.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Define the problem as an LP problem
prob = LpProblem("Warehouse_Rental_Problem", LpMinimize)

# Define decision variables: x[i,j] where i is month and j is contract period
x12, x13, x14, x22, x23, x24, x33, x34 = LpVariable('x12', lowBound=0), LpVariable('x13', lowBound=0), LpVariable('x14', lowBound=0), LpVariable('x22', lowBound=0), LpVariable('x23', lowBound=0), LpVariable('x24', lowBound=0), LpVariable('x33', lowBound=0), LpVariable('x34', lowBound=0)

# Objective function: Minimize total rental fees
prob += lpSum([60*x13 + 73*x14 + 60*x23 + 73*x24 + 50*x34]), "Total_Rental_Fees"

# Constraints for each month's required warehouse area
prob += 1500*x12 + 1000*x13 + 2000*x14 <= 1500, "Month_1"
prob += 1000*x22 + 2000*x23 + 1200*x24 <= 1000, "Month_2"
prob += 2000*x33 + 1200*x34 <= 2000, "Month_3"
prob += 1200*x43 + 600*x44 <= 1200, "Month_4"

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Rental Fees: {value(prob.objective)}")
```

Note: The above code assumes that the rental fee for a contract period of 1 month is $28/m², and adjusts the initial objective function to reflect this. Please adjust the rental fees in the `prob += lpSum([60*x13 + 73*x14 + 50*x34]), "Total_Rental_Fees"` line if the actual data differs from what is assumed here.

### ORLM-8B formulation
## Mathematical Model:
To solve the warehouse rental problem for the factory, we need to construct a linear programming model to minimize the total rental fees paid while meeting the monthly warehouse area requirements. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The rental area for the \(j\)th month of the \(i\)th contract, where \(i = 1, 2, 3, 4\) represents the contract period and \(j = 1, 2, 3, 4\) represents the month.

### Objective Function:
- Minimize the total rental fees: \[Z = 28x_{11} + 45x_{12} + 60x_{13} + 73x_{14} + 28x_{21} + 45x_{22} + 60x_{23} + 73x_{24} + 28x_{31} + 45x_{32} + 60x_{33} + 73x_{34} + 28x_{41} + 45x_{42} + 60x_{43} + 73x_{44}\]

### Constraints:
1. Monthly warehouse area requirements:
   - \(x_{11} \geq 1500\)
   - \(x_{21} + x_{22} \geq 1500\)
   - \(x_{31} + x_{32} + x_{33} \geq 1500\)
   - \(x_{41} + x_{42} + x_{43} + x_{44} \geq 1500\)
2. Monthly warehouse area requirements:
   - \(x_{12} \geq 1000\)
   - \(x_{22} + x_{23} \geq 1000\)
   - \(x_{32} + x_{33} + x_{34} \geq 1000\)
   - \(x_{42} + x_{43} + x_{44} \geq 1000\)
3. Monthly warehouse area requirements:
   - \(x_{13} \geq 2000\)
   - \(x_{23} + x_{24} \geq 2000\)
   - \(x_{33} + x_{34} \geq 2000\)
   - \(x_{43} + x_{44} \geq 2000\)
4. Monthly warehouse area requirements:
   - \(x_{14} \geq 1200\)
   - \(x_{24} + x_{34} \geq 1200\)
   - \(x_{34} + x_{44} \geq 1200\)
   - \(x_{44} \geq 1200\)
5. Non-negativity constraints:
   - \(x_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply linear programming techniques to find the optimal rental areas for each month and each contract, minimizing the total rental fees paid while meeting the monthly warehouse area requirements. This will provide the factory with an economically efficient warehouse rental strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("WarehouseLeasing")

# Rental fees
rental_costs = [28, 45, 60, 73]

# Required warehouse areas
required_areas = [1500, 1000, 2000, 1200]

# Add decision variables
x = {}
for i in range(1, 5):
    for j in range(1, 5):
        x[i, j] = model.addVar(lb=0, name=f"x_{i}{j}")

# Objective function: Minimize total rental fees
model.setObjective(cp.quicksum(rental_costs[j-1] * x[i, j] for i in range(1, 5) for j in range(1, 5)), sense=COPT.MINIMIZE)

# Constraints
# Monthly warehouse area requirements
for j in range(1, 5):
    model.addConstr(cp.quicksum(x[i, j] for i in range(1, 5-j+1)) >= required_areas[j-1], name=f"AreaReq_Month{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total rental fees: {:.2f} yuan".format(model.objval))
    for i in range(1, 5):
        for j in range(1, 5):
            if x[i, j].x > 0:
                print(f"Rental area for the {j}th month of the {i}th contract: {x[i, j].x:.2f} m^2")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the rental fees and required warehouse areas, and add the decision variables. The objective function is to minimize the total rental fees, calculated using `cp.quicksum` for the sum of rental fees for all contracts and months.

We add constraints to ensure that the monthly warehouse area requirements are met. Finally, we solve the model and output the results of the optimal solution, including the minimum total rental fees and the rental areas for each month and each contract.

This script provides a complete example of using the `coptpy` library to solve the factory's warehouse rental problem while satisfying all the constraints mentioned in the problem.

---

## Case 51  [CODE_BUG]

**GT:** 426.0  |  **3B:** None (?)  |  **8B:** 0.0

### Question
Fighter jets are important combat tools, but in order for them to be effective, there must be enough pilots. Therefore, in addition to a portion of the produced fighter jets being used directly for combat, another portion needs to be allocated for pilot training. It is known that the number of fighter jets produced each year is $a_j(j=1, \cdots, n)$, and each fighter jet can train $k$ pilots per year. How should the production of fighter jets be allocated each year to maximize their contribution to national defense over a period of $n$ years?

### 3B formulation
```python
from pulp import LpMaximize, LpVariable

def optimize_fighter_jets_production(n):
    # Initialize the problem with maximization objective
    prob = LpProblem("Optimization_Problem", LpMaximize)

    # Define decision variables
    production = LpVariable.dicts('Production', range(1, n+1), lowBound=0, cat='Continuous')

    # Objective function: maximize total contribution to national defense over n years
    for j in range(1, n+1):
        prob += production[j] * a_j[j-1], "Year_{}".format(j)

    # Constraint: sum of productions equals the total number of fighter jets produced each year
    constraint = LpConstraint(e=sum(production), sense=LpConstraintEQ, name="Total_Production")
    prob += constraint

    # Solve the problem
    prob.solve()

    # Extract results
    optimal_production = {j: production[j].varValue for j in range(1, n+1)}
    
    return optimal_production

# Example usage (assuming a_j values are provided)
a_j = [50, 60, 70]  # Placeholder for actual data
n = len(a_j)

optimal_production = optimize_fighter_jets_production(n)
print(optimal_production)
```

Please note that the placeholder `a_j` array is used here as a dummy variable. In a real-world scenario, you would replace this with the actual number of fighter jets produced each year. The function `optimize_fighter_jets_production` calculates and returns the optimal production allocation for each year to maximize national defense contribution over the specified period.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of fighter jet production and pilot training, we need to construct a mathematical model to maximize the contribution of fighter jets to national defense over a period of $n$ years. The model can be formulated as follows:

### Decision Variables:
- \(x_j\): The number of fighter jets used for combat in year \(j\).
- \(y_j\): The number of fighter jets used for pilot training in year \(j\).

### Objective Function:
- Maximize the contribution to national defense over \(n\) years: \[Z = \sum_{j=1}^{n} x_j\]
  - This function calculates the total number of fighter jets used for combat over \(n\) years, which is the contribution to national defense.

### Constraints:
1. The number of fighter jets used for pilot training each year cannot exceed the number of fighter jets produced that year: \[y_j \leq a_j, \forall j\]
2. The number of fighter jets used for pilot training each year multiplied by the number of pilots trained per fighter jet per year must be greater than or equal to the number of pilots needed: \[k \cdot y_j \geq \text{Number of pilots needed in year } j, \forall j\]
3. The number of fighter jets used for combat each year must be less than or equal to the total number of fighter jets produced up to that year: \[x_j \leq \sum_{i=1}^{j} a_i - \sum_{i=1}^{j} y_i, \forall j\]
4. The number of fighter jets used for pilot training each year must be less than or equal to the total number of fighter jets produced up to that year: \[y_j \leq \sum_{i=1}^{j} a_i - \sum_{i=1}^{j} x_i, \forall j\]

### Non-negativity Constraints:
- \(x_j, y_j \geq 0, \forall j\)

### Integer Constraints:
- \(x_j, y_j\) must be integers, as the number of fighter jets cannot be fractional.

Using this model, we can apply integer linear programming techniques to find the optimal number of fighter jets used for combat and pilot training each year, maximizing the contribution to national defense over \(n\) years. This will provide an optimized strategy for fighter jet production and pilot training.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the fighter jet production and pilot training problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("FighterJetAllocation")

# Define parameters
n = 5  # Number of years
a = [10, 15, 20, 25, 30]  # Number of fighter jets produced each year
k = 2  # Number of pilots trained per fighter jet per year
pilots_needed = [20, 30, 40, 50, 60]  # Number of pilots needed each year

# Add decision variables
x = [model.addVar(vtype=COPT.INTEGER, name=f"x_{j}") for j in range(1, n+1)]  # Number of fighter jets used for combat each year
y = [model.addVar(vtype=COPT.INTEGER, name=f"y_{j}") for j in range(1, n+1)]  # Number of fighter jets used for pilot training each year

# Objective function: Maximize the contribution to national defense over n years
model.setObjective(cp.quicksum(x), sense=COPT.MAXIMIZE)

# Constraints
# 1. The number of fighter jets used for pilot training each year cannot exceed the number of fighter jets produced that year
for j in range(1, n+1):
    model.addConstr(y[j-1] <= a[j-1], name=f"TrainingLimit_{j}")

# 2. The number of fighter jets used for pilot training each year multiplied by the number of pilots trained per fighter jet per year must be greater than or equal to the number of pilots needed
for j in range(1, n+1):
    model.addConstr(k * y[j-1] >= pilots_needed[j-1], name=f"PilotRequirement_{j}")

# 3. The number of fighter jets used for combat each year must be less than or equal to the total number of fighter jets produced up to that year
for j in range(1, n+1):
    model.addConstr(x[j-1] <= cp.quicksum(a[i-1] for i in range(1, j+1)) - cp.quicksum(y[i-1] for i in range(1, j+1)), name=f"CombatLimit_{j}")

# 4. The number of fighter jets used for pilot training each year must be less than or equal to the total number of fighter jets produced up to that year
for j in range(1, n+1):
    model.addConstr(y[j-1] <= cp.quicksum(a[i-1] for i in range(1, j+1)) - cp.quicksum(x[i-1] for i in range(1, j+1)), name=f"TrainingLimit_{j}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized contribution to national defense over", n, "years:", model.objval)
    for j in range(1, n+1):
        print(f"Number of fighter jets used for combat in year {j}: {x[j-1].x}")
        print(f"Number of fighter jets used for pilot training in year {j}: {y[j-1].x}")
else:
    print("No optimal solution found.")
```

This script defines the parameters of the problem, including the number of years, the number of fighter jets produced each year, the number of pilots trained per fighter jet per year, and the number of pilots needed each year. Then, it creates decision variables to represent the number of fighter jets used for combat and pilot training each year.

The objective function is to maximize the contribution to national defense over \(n\) years, which is the total number of fighter jets used for combat.

The constraints include:
1. The number of fighter jets used for pilot training each year cannot exceed the number of fighter jets produced that year.
2. The number of fighter jets used for pilot training each year multiplied by the number of pilots trained per fighter jet per year must be greater than or equal to the number of pilots needed.
3. The number of fighter jets used for combat each year must be less than or equal to the total number of fighter jets produced up to that year.
4. The number of fighter jets used for pilot training each year must be less than or equal to the total number of fighter jets produced up to that year.

Finally, the script solves the model and outputs the optimal solution (if it exists). The output includes the maximized contribution to national defense over \(n\) years and the number of fighter jets used for combat and pilot training each year.

---

## Case 52  [SOLVE_FAILED]

**GT:** 85  |  **3B:** None (Not Solved)  |  **8B:** 0.0

### Question
Traveling Salesman Problem (TSP) with Specific Values\n\nThe famous traveling salesman problem in operations research can be described as follows: a traveling salesman starts from a certain city and goes to visit other \( n \) cities to sell goods. It is required to visit each city exactly once and then return to the original starting city. The distance between city \( i \) and city \( j \) is given as \( d_{ij} \). What kind of route sequence should the salesman choose to minimize the total travel distance?\n\nWe will establish an integer programming model for this problem using specific values for the number of cities and distances between them. Let's assume there are 5 cities (including the starting city) and the distance matrix \( D \) is given as follows:\n\n\[\nD = \begin{bmatrix}\n0 & 10 & 15 & 20 & 25 \\\n10 & 0 & 35 & 25 & 30 \\\n15 & 35 & 0 & 30 & 20 \\\n20 & 25 & 30 & 0 & 15 \\\n25 & 30 & 20 & 15 & 0\n\end{bmatrix}\n\

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem as a minimization problem
prob = LpProblem("Traveling_Salesman_Problem", LpMinimize)

# Number of cities including the starting city
num_cities = 5

# Initialize binary variables for each route (1 if selected, 0 otherwise)
routes = [LpVariable(f"x_{i}_{j}", lowBound=0, upBound=1, cat='Binary') for i in range(num_cities) for j in range(num_cities)]

# Objective function: minimize total distance
total_distance = lpSum([D[i][j] * routes[idx] for idx, (i, j) in enumerate([(i, j) for i in range(num_cities) for j in range(num_cities)]) if i != j])
prob += total_distance

# Constraints: each city must be visited exactly once
for city in range(num_cities):
    prob += lpSum([routes[idx] for idx in routes if (idx // num_cities == city and idx % num_cities != city)] + [routes[idx] for idx in routes if (idx // num_cities != city and idx % num_cities == city)] ) == 1

# Solve the problem
prob.solve()

# Print the solution
for var in prob.variables():
    print(f"{var.name}: {var.varValue}")

print(f"Total Distance: {prob.objective.value()}")
```

To complete this code, we need to define the distance matrix `D`. Here is how you can do it:

```python
D = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

# Now the full code with the distance matrix
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem as a minimization problem
prob = LpProblem("Traveling_Salesman_Problem", LpMinimize)

# Number of cities including the starting city
num_cities = 5

# Initialize binary variables for each route (1 if selected, 0 otherwise)
routes = [LpVariable(f"x_{i}_{j}", lowBound=0, upBound=1, cat='Binary') for i in range(num_cities) for j in range(num_cities)]

# Objective function: minimize total distance
total_distance = lpSum([D[i][j] * routes[idx] for idx, (i, j) in enumerate([(i, j) for i in range(num_cities) for j in range(num_cities)]) if i != j])
prob += total_distance

# Constraints: each city must be visited exactly once
for city in range(num_cities):
    prob += lpSum([routes[idx] for idx in routes if (idx // num_cities == city and idx % num_cities != city)] + [routes[idx] for idx in routes if (idx // num_cities != city and idx % num_cities == city)] ) == 1

# Solve the problem
prob.solve()

# Print the solution
for var in prob.variables():
    print(f"{var.name}: {var.varValue}")

print(f"Total Distance: {prob.objective.value()}")
```

This code sets up and solves the TSP using PuLP, defining binary variables for each route taken by the salesman. The constraints ensure that each city is visited exactly once, and the objective function minimizes the total distance traveled.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
- \( x_{ij} \): Binary variable that is 1 if the salesman travels directly from city \( i \) to city \( j \), and 0 otherwise.

### Constraints:
1. Each city (including the starting city) is visited exactly once:
   \[
   \sum_{j=1}^{n} x_{ij} = 1, \quad \forall i \in \{1, \ldots, n\}
   \]
2. Each city (including the starting city) is left exactly once:
   \[
   \sum_{i=1}^{n} x_{ij} = 1, \quad \forall j \in \{1, \ldots, n\}
   \]
3. Avoid subcycles (using the Miller-Tucker-Zemlin constraints):
   - Introduce a new integer variable \( u_i \) to represent the order in which the salesman visits city \( i \).
   - For all \( i \) and \( j \) (\( i \neq j \)):
     \[
     u_i - u_j + n \cdot x_{ij} \leq n - 1
     \]

### Objective:
Minimize the total travel distance:
\[
\min \sum_{i=1}^{n} \sum_{j=1}^{n} d_{ij} \cdot x_{ij}
\]

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create a COPT environment
env = Envr()

# Create a model
model = env.createModel("TSP")

# Number of cities
n = 5

# Distance matrix
D = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

# Add decision variables
x = model.addVars(n, n, vtype=COPT.BINARY, nameprefix = "x")
u = model.addVars(n, vtype=COPT.INTEGER, nameprefix = "u")

# Set the objective function
model.setObjective(sum(D[i][j] * x[i, j] for i in range(n) for j in range(n)), COPT.MINIMIZE)

# Add constraints
for i in range(n):
    model.addConstr(sum(x[i, j] for j in range(n)) == 1)
    model.addConstr(sum(x[j, i] for j in range(n)) == 1)

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            model.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)

# Solve the model
model.solve()

# Output the results
print('Optimal solution found with total distance:', model.objval)
for i in range(n):
    for j in range(n):
        if x[i, j].x > 0.5:
            print(f"Travel from city {i} to city {j}")
```

This script uses the COPTPY library to build and solve the traveling salesman problem, outputting the optimal travel route and the total travel distance.

---

## Case 53  [SOLVE_FAILED]

**GT:** 16  |  **3B:** None (Not Solved)  |  **8B:** 472.3

### Question
A certain university computer laboratory hires 4 undergraduate students (code names 1, 2, 3, 4) and 2 graduate students (code names 5, 6) to provide on-duty assistance. It is known that the maximum number of duty hours that each person can be assigned from Monday to Friday, as well as the hourly duty remuneration for each person, are shown in Table 5-9.

Table 5-9:
\begin{tabular}{c|c|c|c|c|c|c}
\hline \multirow{2}{*}{ Student Code } & \multirow{2}{*}{ Remuneration/(¥/h) } & \multicolumn{5}{|c}{ Maximum Duty Time per Day (h) } \
\cline { 3 - 7 } & & Monday & Tuesday & Wednesday & Thursday & Friday \
\hline 1 & 10.0 & 6 & 0 & 6 & 0 & 7 \
\hline 2 & 10.0 & 0 & 6 & 0 & 6 & 0 \
\hline 3 & 9.9 & 4 & 8 & 3 & 0 & 5 \
\hline 4 & 9.8 & 5 & 5 & 6 & 0 & 4 \
\hline 5 & 10.8 & 3 & 0 & 4 & 8 & 0 \
\hline 6 & 11.3 & 0 & 6 & 0 & 6 & 3 \
\hline
\end{tabular}

The laboratory is open from 8:00 AM to 10:00 PM, and there must be one and only one student on duty during the opening hours. It is also stipulated that each undergraduate student must have a minimum of 8 hours of duty per week, and each graduate student must have a minimum of 7 hours of duty per week. Based on the above, the following requirements are added: firstly, each student should not have more than 2 duty shifts per week, and secondly, the number of students assigned to duty each day should not exceed 3. Based on this, establish a new mathematical model.

### 3B formulation
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger

# Define the problem as an LP problem
prob = LpProblem("Computer_Laboratory_Duty_Planning", LpMinimize)

# Define decision variables
x1_mon, x1_tue, x1_wed, x1_thu, x1_fri = LpVariable('x1_mon', 0, None, LpInteger)
x2_mon, x2_tue, x2_wed, x2_thu, x2_fri = LpVariable('x2_mon', 0, None, LpInteger)
x3_mon, x3_tue, x3_wed, x3_thu, x3_frae = LpVariable('x3_mon', 0, None, LpInteger)
x4_mon, x4_tue, x4_wed, x4_thu, x4_frae = LpVariable('x4_mon', 0, None, LpInteger)
x5_mon, x5_tue, x5_wed, x5_thu, x5_frae = LpVariable('x5_mon', 0, None, LpInteger)
x6_mon, x6_tue, x6_wed, x6_thu, x6_frae = LpVariable('x6_mon', 0, None, LpInteger)

# Objective function: minimize total remuneration
prob += lpSum([
    10.0 * (x1_mon + x2_mon + x3_mon + x4_mon + x5_mon + x6_mon),
    10.0 * (x1_tue + x2_tue + x3_tue + x4_tue + x5_tue + x6_tue),
    9.9 * (x1_wed + x2_wed + x3_wed + x4_wed + x5_wed + x6_wed),
    9.8 * (x1_thu + x2_thu + x3_thu + x4_thu + x5_thu + x6_thu),
    10.8 * (x1_frae + x2_frae + x3_frae + x4_frae + x5_frae + x6_frae)
])

# Constraints: duty hours per day
prob += x1_mon + x1_tue + x1_wed + x1_thu + x1_frae <= 8, "Monday_hours"
prob += x2_mon + x2_tue + x2_wed + x2_thu + x2_frae <= 8, "Tuesday_hours"
prob += x3_mon + x3_tue + x3_wed + x3_thu + x3_frae <= 8, "Wednesday_hours"
prob += x4_mon + x4_tue + x4_wed + x4_thu + x4_frae <= 8, "Thursday_hours"
prob += x5_mon + x5_tue + x5_wed + x5_thu + x5_frae <= 8, "Friday_hours"

# Constraints: duty hours per week
prob += lpSum([x1_mon, x2_mon, x3_mon, x4_mon, x5_mon, x6_mon]) >= 8, "Minimum_Weekly_Hours_Student_1"
prob += lpSum([x1_tue, x2_tue, x3_tue, x4_tue, x5_tue, x6_tue]) >= 7, "Minimum_Weekly_Hours_Student_2"
prob += lpSum([x1_wed, x2_wed, x3_wed, x4_wed, x5_wed, x6_wed]) >= 8, "Minimum_Weekly_Hours_Student_3"
prob += lpSum([x1_thu, x2_thu, x3_thu, x4_thu, x5_thu, x6_thu]) >= 7, "Minimum_Weekly_Hours_Student_4"
prob += lpSum([x1_frae, x2_frae, x3_frae, x4_frae, x5_frae, x6_frae]) >= 8, "Minimum_Weekly_Hours_Student_5"

# Constraints: duty shifts per week
prob += lpSum([x1_mon, x2_mon, x3_mon, x4_mon, x5_mon, x6_mon]) <= 2, "Maximum_Duty_Shifts_Student_1"
prob += lpSum([x1_tue, x2_tue, x3_tue, x4_tue, x5_tue, x6_tue]) <= 2, "Maximum_Duty_Shifts_Student_2"
prob += lpSum([x1_wed, x2_wed, x3_wed, x4_wed, x5_wed, x6_wed]) <= 2, "Maximum_Duty_Shifts_Student_3"
prob += lpSum([x1_thu, x2_thu, x3_thu, x4_thu, x5_thu, x6_thu]) <= 2, "Maximum_Duty_Shifts_Student_4"
prob += lpSum([x1_frae, x2_frae, x3_frae, x4_frae, x5_frae, x6_frae]) <= 2, "Maximum_Duty_Shifts_Student_5"

# Constraints: duty shifts per day
prob += lpSum([x1_mon, x2_mon, x3_mon, x4_mon, x5_mon, x6_mon]) <= 3, "Maximum_Duty_Shifts_Per_Day"
prob += lpSum([x1_tue, x2_tue, x3_tue, x4_tue, x5_tue, x6_tue]) <= 3, "Maximum_Duty_Shifts_Per_Day"
prob += lpSum([x1_wed, x2_wed, x3_wed, x4_wed, x5_wed, x6_wed]) <= 3, "Maximum_Duty_Shifts_Per_Day"
prob += lpSum([x1_thu, x2_thu, x3_thu, x4_thu, x5_thu, x6_thu]) <= 3, "Maximum_Duty_Shifts_Per_Day"
prob += lpSum([x1_frae, x2_frae, x3_frae, x4_frae, x5_frae, x6_frae]) <= 3, "Maximum_Duty_Shifts_Per_Day"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Remuneration: {value(prob.objective)}")
```

Please note that this code is a simplified version of what might be needed to solve the given problem, as it does not include all constraints and conditions. The actual implementation may require additional checks or adjustments based on specific requirements.

### ORLM-8B formulation
## Mathematical Model:
To solve the duty assignment problem in the university computer laboratory, we need to construct a mathematical model to minimize the total cost while satisfying the duty time constraints for each student, the minimum duty time requirements, and the constraints on the number of duty shifts and the number of students assigned to duty each day. Here is the model formulation:

### Decision Variables:
- \(x_{ij}\): The number of duty hours for student \(i\) on day \(j\), where \(i\) represents the student code (1 to 6) and \(j\) represents the day of the week (1 to 5).

### Objective Function:
- Minimize the total cost: \[Z = \sum_{i=1}^{6} \sum_{j=1}^{5} c_i \cdot x_{ij}\]
  where \(c_i\) is the hourly duty remuneration for student \(i\).

### Constraints:
1. Maximum duty time per day for each student:
   - \(x_{1j} \leq T_{1j}, \forall j\)
   - \(x_{2j} \leq T_{2j}, \forall j\)
   - \(x_{3j} \leq T_{3j}, \forall j\)
   - \(x_{4j} \leq T_{4j}, \forall j\)
   - \(x_{5j} \leq T_{5j}, \forall j\)
   - \(x_{6j} \leq T_{6j}, \forall j\)
   where \(T_{ij}\) is the maximum duty time for student \(i\) on day \(j\).
2. Minimum duty time per week for each student:
   - \(\sum_{j=1}^{5} x_{1j} \geq 8\)
   - \(\sum_{j=1}^{5} x_{2j} \geq 8\)
   - \(\sum_{j=1}^{5} x_{3j} \geq 8\)
   - \(\sum_{j=1}^{5} x_{4j} \geq 8\)
   - \(\sum_{j=1}^{5} x_{5j} \geq 7\)
   - \(\sum_{j=1}^{5} x_{6j} \geq 7\)
3. Each student should not have more than 2 duty shifts per week:
   - \(\sum_{j=1}^{5} y_{ij} \leq 2, \forall i\)
   where \(y_{ij}\) is a binary variable that equals 1 if student \(i\) has a duty shift on day \(j\), and 0 otherwise.
4. The number of students assigned to duty each day should not exceed 3:
   - \(\sum_{i=1}^{6} y_{ij} \leq 3, \forall j\)

### Non-negativity Constraints:
- \(x_{ij} \geq 0, \forall i, \forall j\)

### Integer Constraints:
- \(x_{ij}\) and \(y_{ij}\) must be integers.

Using this model, we can apply integer linear programming techniques to find the optimal number of duty hours for each student each day, minimizing the total cost while satisfying all duty time constraints, minimum duty time requirements, and constraints on the number of duty shifts and the number of students assigned to duty each day. This will provide the university computer laboratory with an economically efficient duty assignment strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("LabDutyScheduling")

# Student codes
students = list(range(1, 7))

# Days of the week
days = list(range(1, 6))

# Hourly duty remuneration for each student
hourly_wages = {1: 10.0, 2: 10.0, 3: 9.9, 4: 9.8, 5: 10.8, 6: 11.3}

# Maximum duty time per day for each student
max_hours = {
    1: {1: 6, 2: 0, 3: 6, 4: 0, 5: 7},
    2: {1: 0, 2: 6, 3: 0, 4: 6, 5: 0},
    3: {1: 4, 2: 8, 3: 3, 4: 0, 5: 5},
    4: {1: 5, 2: 5, 3: 6, 4: 0, 5: 4},
    5: {1: 3, 2: 0, 3: 4, 4: 8, 5: 0},
    6: {1: 0, 2: 6, 3: 0, 4: 6, 5: 3},
}

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for i in students for j in days}
y = {(i, j): model.addVar(vtype=COPT.BINARY, name=f"y_{i}_{j}") for i in students for j in days}

# Objective function: Minimize total cost
model.setObjective(cp.quicksum(hourly_wages[i] * x[i, j] for i in students for j in days), sense=COPT.MINIMIZE)

# Constraints
# Maximum duty time per day for each student
for i in students:
    for j in days:
        model.addConstr(x[i, j] <= max_hours[i][j], name=f"MaxHours_{i}_{j}")

# Minimum duty time per week for each student
min_hours = {1: 8, 2: 8, 3: 8, 4: 8, 5: 7, 6: 7}
for i in students:
    model.addConstr(cp.quicksum(x[i, j] for j in days) >= min_hours[i], name=f"MinHours_{i}")

# Each student should not have more than 2 duty shifts per week
for i in students:
    model.addConstr(cp.quicksum(y[i, j] for j in days) <= 2, name=f"MaxShifts_{i}")

# The number of students assigned to duty each day should not exceed 3
for j in days:
    model.addConstr(cp.quicksum(y[i, j] for i in students) <= 3, name=f"MaxStudents_{j}")

# Link x and y variables
for i in students:
    for j in days:
        model.addConstr(x[i, j] <= max_hours[i][j] * y[i, j], name=f"Link_{i}_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} ¥".format(model.objval))
    for i in students:
        for j in days:
            if x[i, j].x > 0:
                print(f"Student {i} has {x[i, j].x} hours of duty on day {j}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the student codes, days of the week, hourly duty remuneration for each student, and the maximum duty time per day for each student.

Next, we add decision variables `x` and `y`, representing the number of duty hours for each student each day and whether each student has a duty shift each day, respectively. The objective function is to minimize the total cost, calculated using the `cp.quicksum` function.

We add four sets of constraints:
1. Maximum duty time per day for each student
2. Minimum duty time per week for each student
3. Each student should not have more than 2 duty shifts per week
4. The number of students assigned to duty each day should not exceed 3

Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the number of duty hours for each student each day.

This script provides a complete example of using the `coptpy` library to solve the duty assignment problem in a university computer laboratory, while satisfying all the constraints mentioned in the problem.

---

## Case 54  [WRONG_FORMULATION]

**GT:** 150  |  **3B:** 15900.0 (Optimal)  |  **8B:** 170.0

### Question
For a certain daytime and nighttime service bus route, the number of drivers and crew members required during each time period is given in Table 1-2:
Table 1-2
\begin{tabular}{|c|c|c||c|c|c|}
\hline Shift & Time & Number Required & Shift & Time & Number Required \\
\hline 1 & $6: 00 \sim 10: 00$ & 60 & 4 & $18: 00 \sim 22: 00$ & 50 \\
\hline 2 & $10: 00 \sim 14: 00$ & 70 & 5 & $22: 00 \sim 2: 00$ & 20 \\
\hline 3 & $14: 00 \sim 18: 00$ & 60 & 6 & $2: 00 \sim 6: 00$ & 30 \\
\hline
\end{tabular}

Assuming that the drivers and crew members start working at the beginning of each time period and work continuously for 8 hours, how many drivers and crew members should be assigned to this bus route at least? Write down the linear programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable

# Create a LP Minimization Problem
prob = LpProblem("Bus_Route_Planning", LpMinimize)

# Define decision variables
drivers_1_to_2 = LpVariable('Drivers_1_to_2', lowBound=0)
drivers_2_to_3 = LpVariable('Drivers_2_to_3', lowBound=0)
drivers_3_to_4 = LpVariable('Drivers_3_to_4', lowBound=0)

crew_members_1_to_2 = LpVariable('Crew_Members_1_to_2', lowBound=0)
crew_members_2_to_3 = LpVariable('Crew_Members_2_to_3', lowBound=0)
crew_members_3_to_4 = LpVariable('Crew_Members_3_to_4', lowBound=0)

# Objective function: Minimize the total number of drivers and crew members
prob += 60*drivers_1_to_2 + 70*drivers_2_to_3 + 60*drivers_3_to_4 \
        + 50*crew_members_1_to_2 + 20*crew_members_2_to_3 + 30*crew_members_3_to_4, "Total_Drivers_and_Crew_Members"

# Constraints
prob += drivers_1_to_2 == 60, "Shift_1"
prob += drivers_2_to_3 >= 70, "Shift_2"
prob += drivers_3_to_4 == 60, "Shift_3"
prob += crew_members_1_to_2 == 50, "Shift_4"
prob += crew_members_2_to_3 >= 20, "Shift_5"
prob += crew_members_3_to_4 == 30, "Shift_6"

# Solve the problem
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Drivers and Crew Members Required =", value(prob.objective))
```

This code sets up a linear programming model to determine the minimum number of drivers and crew members required for each shift based on the given constraints. The objective is to minimize the total number of drivers and crew members assigned while satisfying all the requirements specified in Table 1-2.

### ORLM-8B formulation
## Mathematical Model:
To solve the problem of driver and crew member allocation for the bus route, we need to construct a linear programming model to determine the minimum number of drivers and crew members required. Here is the model formulation:

### Decision Variables:
- \(x_j\): The number of drivers and crew members starting work during the \(j\)th time period, where \(j = 1, 2, 3, 4, 5, 6\).

### Objective Function:
- Minimize the total number of drivers and crew members: \[Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6\]

### Constraints:
- Ensure that the number of drivers and crew members during each time period meets the demand:
  - \(x_1 + x_6 \geq 60\) (for the first time period)
  - \(x_1 + x_2 \geq 70\) (for the second time period)
  - \(x_2 + x_3 \geq 60\) (for the third time period)
  - \(x_3 + x_4 \geq 70\) (for the fourth time period)
  - \(x_4 + x_5 \geq 50\) (for the fifth time period)
  - \(x_5 + x_6 \geq 20\) (for the sixth time period)

### Non-negativity Constraints:
- \(x_j \geq 0\), for all \(j = 1, 2, 3, 4, 5, 6\).

Using this model, we can apply linear programming techniques to find the minimum number of drivers and crew members required to meet the demand during each time period. This will provide the bus company with an economically efficient driver and crew member allocation strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem of driver and crew member allocation for the bus route:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("BusCrewAllocation")

# Add decision variables
x = [model.addVar(lb=0, vtype=COPT.INTEGER, name=f"x_{j+1}") for j in range(6)]

# Objective function: Minimize the total number of drivers and crew members
model.setObjective(cp.quicksum(x), sense=COPT.MINIMIZE)

# Constraints: Ensure that the number of drivers and crew members during each time period meets the demand
model.addConstr(x[0] + x[5] >= 60, name="Shift1")
model.addConstr(x[0] + x[1] >= 70, name="Shift2")
model.addConstr(x[1] + x[2] >= 60, name="Shift3")
model.addConstr(x[2] + x[3] >= 70, name="Shift4")
model.addConstr(x[3] + x[4] >= 50, name="Shift5")
model.addConstr(x[4] + x[5] >= 20, name="Shift6")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum number of drivers and crew members required:", model.objval)
    for j in range(6):
        print(f"Number of drivers and crew members starting work during time period {j+1}: {x[j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add 6 decision variables `x[j]`, representing the number of drivers and crew members starting work during each time period.

Next, we define the objective function, which is to minimize the total number of drivers and crew members, using `cp.quicksum(x)` to calculate the sum of all decision variables.

Then, we add 6 constraints to ensure that the number of drivers and crew members during each time period meets the demand. For example, `x[0] + x[5] >= 60` ensures that the demand for the first time period is met.

Finally, we solve the model and output the results. If an optimal solution is found, we print the minimum number of drivers and crew members required and the number of drivers and crew members starting work during each time period. If no optimal solution is found, we output the corresponding message.

This script provides a complete example of using the `coptpy` library to solve the problem of driver and crew member allocation for a bus route, and demonstrates how to build and solve a linear programming model in Python.

---

## Case 55  [SOLVE_FAILED]

**GT:** 1146.57  |  **3B:** 0.0 (Unbounded)  |  **8B:** -0.0

### Question
A factory produces three products, I, II, and III. Each product goes through two processing procedures, A and B. The factory has two types of equipment, A1 and A2, to complete procedure A, and three types of equipment, B1, B2, and B3, to complete procedure B. Product I can be processed on either type of A equipment or any type of B equipment. Product II can be processed on any type of A equipment, but when completing procedure B, it can only be processed on B1 equipment. Product III can only be processed on A2 and B2 equipment. Given the processing time, raw material cost, product selling price, available equipment operating time, and equipment cost at full load for each type of equipment, as shown in Table 1-4, determine the optimal production plan to maximize profit.

Table 1-4
\begin{tabular}{|c|c|c|c|c|c|}
\hline \multirow{2}{*}{ Equipment } & \multicolumn{3}{|c|}{ Product } & \multirow{2}{*}{ Available Equipment Operating Time } & \multirow{2}{*}{ Equipment Cost at Full Load (in yuan) } \\
\cline { 2 - 4 } & I & II & III & & \\
\hline$A_1$ & 5 & 10 & & 6000 & 300 \\
\hline$A_2$ & 7 & 9 & 12 & 10000 & 321 \\
\hline$B_1$ & 6 & 8 & & 4000 & 250 \\
\hline$B_2$ & 4 & & 11 & 7000 & 783 \\
\hline$B_3$ & 7 & & & 4000 & 200 \\
\hline Raw Material Cost (in yuan per unit) & 0.25 & 0.35 & 0.50 & & \\
\hline Unit Price (in yuan per unit) & 1.25 & 2.00 & 2.80 & & \\
\hline
\end{tabular}

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Factory_Optimization_Problem", LpMaximize)

# Decision variables: x1I, x2II, x3III for producing products I, II, and III respectively
x1I = LpVariable('x1I', lowBound=0)
x2II = LpVariable('x2II', lowBound=0)
x3III = LpVariable('x3III', lowBound=0)

# Objective function: Maximize profit
prob += lpSum([1.25*x1I + 2.00*x2II + 2.80*x3III - (0.25*x1I + 0.35*x2II + 0.50*x3III) for x1I, x2II, x3III in [(x1I, x2II, x3III)]]), "Total_Profit"

# Constraints: Equipment and raw material usage
prob += lpSum([5*x1I + 7*x2II + 4*x3III <= 6000]) >= 6000, "A1_Constraint"
prob += lpSum([10*x1I + 9*x2II + 8*x3III <= 4000]) >= 4000, "B1_Constraint"
prob += lpSum([12*x1I + 7*x2II + 11*x3III <= 7000]) >= 7000, "B2_Constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {prob.objective.value()}")
```

This code sets up a linear programming model to maximize profit for the factory production plan, considering constraints on equipment usage and raw material costs. The objective function calculates total profit by subtracting raw material cost from the product selling price multiplied by the number of units produced. Constraints ensure that the available operating time for each type of equipment is not exceeded.

### ORLM-8B formulation
## Mathematical Model:
### Decision Variables:
Let \(x_{ij}\) be the number of units of product \(j\) processed on equipment \(i\), where \(i\) represents the equipment and \(j\) represents the product.

### Objective Function:
Maximize profit:
\[
\max Z = \sum_{j=1}^3 \left( p_j \sum_{i \in I_j} x_{ij} - c_j \sum_{i \in I_j} x_{ij} \right) - \sum_{i=1}^5 c_i \left( \sum_{j=1}^3 t_{ij} x_{ij} \right)
\]
where \(p_j\) is the selling price of product \(j\), \(c_j\) is the raw material cost of product \(j\), \(c_i\) is the equipment cost at full load, and \(t_{ij}\) is the processing time of product \(j\) on equipment \(i\).

### Constraints:
1. Equipment operating time constraints:
   \[
   \sum_{j=1}^3 t_{ij} x_{ij} \leq T_i, \quad \forall i
   \]
   where \(T_i\) is the available equipment operating time for equipment \(i\).

2. Product processing requirements:
   \[
   \sum_{i \in I_j} x_{ij} = D_j, \quad \forall j
   \]
   where \(D_j\) is the demand for product \(j\).

3. Non-negativity constraints:
   \[
   x_{ij} \geq 0, \quad \forall i, j
   \]

## Python Code Solution Using `coptpy`:
```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionOptimization")

# Equipment and product indices
equipments = ['A1', 'A2', 'B1', 'B2', 'B3']
products = ['I', 'II', 'III']

# Equipment processing time
processing_time = {
    'A1': {'I': 5, 'II': 10, 'III': 0},
    'A2': {'I': 7, 'II': 9, 'III': 12},
    'B1': {'I': 6, 'II': 8, 'III': 0},
    'B2': {'I': 4, 'II': 0, 'III': 11},
    'B3': {'I': 7, 'II': 0, 'III': 0}
}

# Equipment available operating time
available_time = {'A1': 6000, 'A2': 10000, 'B1': 4000, 'B2': 7000, 'B3': 4000}

# Equipment cost at full load
equipment_cost = {'A1': 300, 'A2': 321, 'B1': 250, 'B2': 783, 'B3': 200}

# Product selling price and raw material cost
selling_price = {'I': 1.25, 'II': 2.00, 'III': 2.80}
material_cost = {'I': 0.25, 'II': 0.35, 'III': 0.50}

# Product demand
demand = {'I': 0, 'II': 0, 'III': 0}  # Need to be set based on the actual situation

# Add decision variables
x = model.addVars(equipments, products, lb=0, nameprefix="x")

# Objective function: Maximize profit
model.setObjective(
    cp.quicksum(selling_price[j] * cp.quicksum(x[i, j] for i in equipments) - material_cost[j] * cp.quicksum(x[i, j] for i in equipments) for j in products) -
    cp.quicksum(equipment_cost[i] * cp.quicksum(processing_time[i][j] * x[i, j] for j in products) for i in equipments),
    sense=COPT.MAXIMIZE
)

# Constraints
# Equipment operating time constraints
for i in equipments:
    model.addConstr(cp.quicksum(processing_time[i][j] * x[i, j] for j in products) <= available_time[i], name=f"Time_{i}")

# Product processing requirements
for j in products:
    model.addConstr(cp.quicksum(x[i, j] for i in equipments) == demand[j], name=f"Demand_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximum profit: {:.2f} yuan".format(model.objval))
    for i in equipments:
        for j in products:
            if x[i, j].x > 0:
                print(f"Number of units of product {j} processed on equipment {i}: {x[i, j].x:.2f}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the equipment and product indices, processing time, available operating time, equipment cost at full load, product selling price and raw material cost, and product demand. Next, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results, including the maximum profit and the number of units of each product processed on each equipment.

This script provides a complete example of using the `coptpy` library to solve the factory production optimization problem, while satisfying all the constraints mentioned in the problem.

---

## Case 56  [SOLVE_FAILED]

**GT:** 20  |  **3B:** None (Not Solved)  |  **8B:** 0.0

### Question
In a rebar workshop, a batch of rebars (with the same diameter) is being produced. There are 90 rebars with a length of 3 meters and 60 rebars with a length of 4 meters. It is known that each rebar used for cutting is 10 meters long. What is the most efficient way to cut the rebars? Establish a linear programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("rebar_cutting", LpMaximize)

# Define decision variables
x1 = LpVariable('num_3m_rebars', lowBound=0, cat='Integer')
x2 = LpVariable('num_4m_rebars', lowBound=0, cat='Integer')

# Objective function: maximize the number of 10-meter cuts
prob += lpSum[10*x1 + 12*x2], "Total_number_of_cuts"

# Constraints: total rebars used should not exceed available rebars
prob += x1 <= 90, "3m_rebars_constraint"
prob += x2 <= 60, "4m_rebars_constraint"
prob += 3*x1 + 4*x2 >= 10*(x1 + x2), "total_length_constraint"

# Solve the problem
prob.solve()

# Print results
print("Status:", LpProblem.status[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total number of cuts =", value(prob.objective))
```

In this model:
- `x1` represents the number of 3-meter rebars used.
- `x2` represents the number of 4-meter rebars used.
- The objective is to maximize the total number of 10-meter cuts (`10*x1 + 12*x2`).
- Constraints ensure that the total number of rebars used does not exceed available resources and that at least one 10-meter cut must be made.

### ORLM-8B formulation
## Mathematical Model:
To solve the rebar cutting problem, we need to construct a linear programming model to minimize the total length of waste. The model can be formulated as follows:

### Decision Variables:
- \(x_1\): Number of rebars cut into 3 rebars with a length of 1 meter each.
- \(x_2\): Number of rebars cut into 2 rebars with a length of 2 meters each.
- \(x_3\): Number of rebars cut into 1 rebar with a length of 3 meters.
- \(s_1\): Number of rebars with a length of 1 meter left over.
- \(s_2\): Number of rebars with a length of 2 meters left over.
- \(s_3\): Number of rebars with a length of 3 meters left over.

### Objective Function:
- Minimize the total length of waste: \[Z = 10s_1 + 10s_2 + 10s_3\]

### Constraints:
1. Constraint for rebars with a length of 3 meters:
   - \(3x_1 + 2x_2 + s_1 + s_2 + s_3 = 90\)
2. Constraint for rebars with a length of 4 meters:
   - \(x_3 + s_3 = 60\)
3. Non-negativity constraints:
   - \(x_1, x_2, x_3, s_1, s_2, s_3 \geq 0\)

### Integer Constraints:
- \(x_1, x_2, x_3, s_1, s_2, s_3\) must be integers, as the number of rebars cannot be fractional.

Using this model, we can apply linear programming techniques to find the optimal cutting strategy that minimizes the total length of waste. This will provide the rebar workshop with an economically efficient cutting plan.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the rebar cutting problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("RebarCuttingOptimization")

# Add decision variables
x1 = model.addVar(vtype=COPT.INTEGER, name="x1")  # Number of rebars cut into 3 rebars with a length of 1 meter each
x2 = model.addVar(vtype=COPT.INTEGER, name="x2")  # Number of rebars cut into 2 rebars with a length of 2 meters each
x3 = model.addVar(vtype=COPT.INTEGER, name="x3")  # Number of rebars cut into 1 rebar with a length of 3 meters
s1 = model.addVar(vtype=COPT.INTEGER, name="s1")  # Number of rebars with a length of 1 meter left over
s2 = model.addVar(vtype=COPT.INTEGER, name="s2")  # Number of rebars with a length of 2 meters left over
s3 = model.addVar(vtype=COPT.INTEGER, name="s3")  # Number of rebars with a length of 3 meters left over

# Set the objective function
model.setObjective(10 * s1 + 10 * s2 + 10 * s3, sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(3 * x1 + 2 * x2 + s1 + s2 + s3 == 90, name="Constraint_3m")  # Constraint for rebars with a length of 3 meters
model.addConstr(x3 + s3 == 60, name="Constraint_4m")  # Constraint for rebars with a length of 4 meters

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total length of waste: {:.2f} meters".format(model.objval))
    print("Number of rebars cut into 3 rebars with a length of 1 meter each: {}".format(x1.x))
    print("Number of rebars cut into 2 rebars with a length of 2 meters each: {}".format(x2.x))
    print("Number of rebars cut into 1 rebar with a length of 3 meters: {}".format(x3.x))
    print("Number of rebars with a length of 1 meter left over: {}".format(s1.x))
    print("Number of rebars with a length of 2 meters left over: {}".format(s2.x))
    print("Number of rebars with a length of 3 meters left over: {}".format(s3.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add decision variables `x1`, `x2`, `x3`, `s1`, `s2`, and `s3`, representing the number of rebars cut in different ways and the number of rebars left over.

Next, we set the objective function, which is to minimize the total length of waste. We also add two constraints, one for rebars with a length of 3 meters and one for rebars with a length of 4 meters.

Finally, we solve the model and output the results, including the minimum total length of waste and the specific cutting strategy.

This script provides a complete example of using the `coptpy` library to solve the rebar cutting problem, helping the rebar workshop find the most economically efficient cutting plan.

---

## Case 57  [WRONG_FORMULATION]

**GT:** 770.0  |  **3B:** 6000.0 (Optimal)  |  **8B:** 14000000.0

### Question
Assume a paper mill receives three orders for rolls of paper with specified widths and lengths as shown in Table 1.2.

Table 1.2

| Order Number | Width (m) | Length (m) |
| :---: | :---: | :---: |
| 1 | 0.5 | 1000 |
| 2 | 0.7 | 3000 |
| 3 | 0.9 | 2000 |

The mill produces rolls of paper with two standard widths: 1 meter and 2 meters. Assuming the length of the rolls is unlimited, meaning they can be continuously connected to achieve the required length, how should the rolls be cut to minimize the area lost during cutting?

### 3B formulation
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Create a problem
prob = LpProblem("Paper_Mill_Cutting_Problem", LpMinimize)

# Define decision variables
x1_1m = LpVariable('x1_1m', lowBound=0, cat='Continuous')
x2_1m = LpVariable('x2_1m', lowBound=0, cat='Continuous')
x3_1m = LpVariable('x3_1m', lowBound=0, cat='Continuous')

x1_2m = LpVariable('x1_2m', lowBound=0, cat='Continuous')
x2_2m = LpVariable('x2_2m', lowBound=0, cat='Continuous')
x3_2m = LpVariable('x3_2m', lowBound=0, cat='Continuous')

# Objective function: minimize the area lost
prob += lpSum([1 * x1_1m + 4 * x1_2m,
               1 * x2_1m + 4 * x2_2m,
               1 * x3_1m + 4 * x3_2m])

# Constraints: meet the order requirements
prob += x1_1m + 0.5 * x1_2m == 1000, "Order1"
prob += x2_1m + 0.7 * x2_2m == 3000, "Order2"
prob += x3_1m + 0.9 * x3_2m == 2000, "Order3"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total area lost: {value(prob.objective)}")
```

This code sets up a linear programming model to minimize the area lost when cutting rolls of paper with standard widths (1 meter and 2 meters) to meet specified orders. The `PuLP` library is used to define variables, constraints, and the objective function. The solution provides the optimal number of rolls cut from each width that minimizes the total area lost while meeting all order requirements.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem for the paper mill, we will establish a mathematical model to minimize the area lost during cutting while satisfying the width and length requirements of the orders. The model can be formulated as follows:

### Decision Variables:
- \(x_{ij}\): The number of times the \(i\)th width roll is cut to meet the length requirement of the \(j\)th order. Here, \(i\) represents the width (1 meter, 2 meters), and \(j\) represents the order number (1, 2, 3).

### Objective Function:
- Minimize the area lost during cutting: \[Z = \sum_{i \in \{1, 2\}}\sum_{j=1}^{3} (x_{ij} \times \text{width}_i \times \text{length}_j)\]
  - This function calculates the total area lost during cutting based on the number of times each width roll is cut and the width and length of each order.

### Constraints:
1. Meet the length requirement of each order: \[\sum_{i \in \{1, 2\}} (x_{ij} \times \text{width}_i) \geq \text{length}_j, \forall j\]
   - This ensures that the length requirement of each order is met by cutting the rolls of the corresponding width.
2. Non-negativity constraint on the number of cuts: \[x_{ij} \geq 0, \forall i, j\]
   - This ensures that the number of times each width roll is cut is non-negative.

### Integer Constraint:
- \(x_{ij}\) must be integers, as the number of cuts must be integers.

Using this model, we can apply integer linear programming techniques to find the optimal number of times each width roll should be cut to minimize the area lost during cutting while satisfying the width and length requirements of all orders. This will provide the paper mill with an economically efficient cutting strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for the paper mill:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("PaperCuttingOptimization")

# Order data
orders = {
    1: {'width': 0.5, 'length': 1000},
    2: {'width': 0.7, 'length': 3000},
    3: {'width': 0.9, 'length': 2000}
}

# Roll widths
roll_widths = [1, 2]  # 1 meter and 2 meters

# Add decision variables
x = {(i, j): model.addVar(vtype=COPT.INTEGER, name=f"x_{i}_{j}") for i in roll_widths for j in orders}

# Objective function: Minimize area lost during cutting
objective = cp.quicksum(x[i, j] * i * orders[j]['length'] for i in roll_widths for j in orders)
model.setObjective(objective, sense=COPT.MINIMIZE)

# Constraints
# Meet the length requirement of each order
for j in orders:
    model.addConstr(cp.quicksum(x[i, j] * i for i in roll_widths) >= orders[j]['length'], name=f"Demand_{j}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum area lost during cutting: {:.2f} square meters".format(model.objval))
    for i in roll_widths:
        for j in orders:
            if x[i, j].x > 0:
                print(f"Number of times {i} meter width roll is cut for order {j}: {x[i, j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first define the order data and roll widths. Then, we create decision variables `x[i, j]`, representing the number of times the `i`th width roll is cut to meet the length requirement of the `j`th order.

The objective function is to minimize the area lost during cutting, calculated by summing the product of the number of times each width roll is cut and the width and length of each order.

The constraints ensure that the length requirement of each order is met by cutting the rolls of the corresponding width.

Finally, we solve the model and output the minimum area lost during cutting and the number of times each width roll is cut for each order (if greater than 0).

This script provides a complete example of using the `coptpy` library to solve the optimization problem for the paper mill, including the definition of decision variables, the objective function, and constraints, as well as the output of the results.

---

## Case 58  [SOLVE_FAILED]

**GT:** 25  |  **3B:** 115.0 (Infeasible)  |  **8B:** 3.7500000000000004

### Question
A textile factory produces two types of fabrics, one for making clothing and the other for making curtains. The factory operates two shifts, with a weekly production time set at 80 hours. Both types of fabrics are produced at a rate of 1000 meters per hour. Assuming that 70,000 meters of curtain fabric can be sold per week with a profit of 2.5 yuan per meter, and 45,000 meters of clothing fabric can be sold per week with a profit of 1.5 yuan per meter. The factory has the following objectives when formulating its production plan:

$p_{1}$: Use the full 80 hours of production time per week.
$p_{2}$: Overtime hours per week should not exceed 10 hours.
$p_{3}$: Sell no less than 70,000 meters of curtain fabric and 45,000 meters of clothing fabric per week, with profit as the weighting factor.
$p_{4}$: Minimize overtime hours.

Build an objective programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable

# Create a problem
prob = LpProblem("Textile_Factory_Problem", LpMinimize)

# Decision variables
x1 = LpVariable('Clothing_fabric_hours', lowBound=0)  # Clothing fabric production hours per week
x2 = LpVariable('Curtain_fabric_hours', lowBound=0)    # Curtain fabric production hours per week

# Objective function: Minimize overtime hours
prob += x1 + x2, "Total_Overtime_Hours"

# Constraints
# Total production time constraint (80 hours)
prob += x1 + x2 <= 80, 'Production_Time_Constraint'

# Overtime hours constraint (no more than 10 hours)
prob += x1 + x2 <= 90, 'Overtime_Hours_Constraint'

# Curtains fabric production constraint
prob += x2 >= 70000 / 1000, "Curtain_Fabric_Production_Constraint"

# Clothing fabric production constraint
prob += x1 >= 45000 / 1000, "Clothing_Fabric_Production_Constraint"

# Solve the problem
status = prob.solve()

# Check if solution is optimal
if status == 1:
    print(f"Optimal Solution Found: Total Overtime Hours = {value(prob.objective)}")
else:
    print("No feasible solution found.")
```

In this model, we have defined a minimization objective to minimize the total overtime hours. The constraints ensure that the production time is within the limit of 80 hours per week and includes an additional constraint for no more than 10 hours of overtime. We also include constraints ensuring that at least 70,000 meters of curtain fabric and 45,000 meters of clothing fabric are produced each week. The solution will provide the optimal production plan considering all these factors.

### ORLM-8B formulation
## Mathematical Model:
To solve the production planning problem for the textile factory, we need to construct an objective programming model to balance the four objectives. Here is the model formulation:

### Decision Variables:
- \(x_1\): Hours of production for curtain fabric.
- \(x_2\): Hours of production for clothing fabric.
- \(d_1^-\): Negative deviation of actual production time from 80 hours.
- \(d_1^+\): Positive deviation of actual production time from 80 hours.
- \(d_2^-\): Negative deviation of actual overtime hours from 10 hours.
- \(d_2^+\): Positive deviation of actual overtime hours from 10 hours.
- \(d_3^-\): Negative deviation of actual sales of curtain fabric from 70,000 meters.
- \(d_3^+\): Positive deviation of actual sales of curtain fabric from 70,000 meters.
- \(d_4^-\): Negative deviation of actual sales of clothing fabric from 45,000 meters.
- \(d_4^+\): Positive deviation of actual sales of clothing fabric from 45,000 meters.

### Objective Function:
- Minimize the weighted sum of deviations: \[Z = p_1 d_1^- + p_2 d_2^+ + 2.5p_3 d_3^- + 1.5p_3 d_4^- + p_4 d_2^+\]

### Constraints:
1. Total production time constraint: \(x_1 + x_2 + d_1^- - d_1^+ = 80\)
2. Overtime hours constraint: \(x_1 + x_2 - 80 + d_2^- - d_2^+ = 10\)
3. Sales constraint for curtain fabric: \(x_1 + d_3^- - d_3^+ = 70\)
4. Sales constraint for clothing fabric: \(x_2 + d_4^- - d_4^+ = 45\)
5. Non-negativity constraints: \(x_1, x_2, d_i^-, d_i^+ \geq 0, \forall i \in \{1, 2, 3, 4\}\)

Using this model, we can apply objective programming techniques to find the optimal production hours for each type of fabric, while satisfying all production and sales constraints, in order to achieve the best balance between the four objectives. This will provide the textile factory with an optimized production plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("TextileProductionOptimization")

# Add decision variables
x1 = model.addVar(lb=0, name="x1")  # Hours of production for curtain fabric
x2 = model.addVar(lb=0, name="x2")  # Hours of production for clothing fabric
d1_minus = model.addVar(lb=0, name="d1_minus")  # Negative deviation of actual production time from 80 hours
d1_plus = model.addVar(lb=0, name="d1_plus")  # Positive deviation of actual production time from 80 hours
d2_minus = model.addVar(lb=0, name="d2_minus")  # Negative deviation of actual overtime hours from 10 hours
d2_plus = model.addVar(lb=0, name="d2_plus")  # Positive deviation of actual overtime hours from 10 hours
d3_minus = model.addVar(lb=0, name="d3_minus")  # Negative deviation of actual sales of curtain fabric from 70,000 meters
d3_plus = model.addVar(lb=0, name="d3_plus")  # Positive deviation of actual sales of curtain fabric from 70,000 meters
d4_minus = model.addVar(lb=0, name="d4_minus")  # Negative deviation of actual sales of clothing fabric from 45,000 meters
d4_plus = model.addVar(lb=0, name="d4_plus")  # Positive deviation of actual sales of clothing fabric from 45,000 meters

# Set the objective function
model.setObjective(d1_minus + d2_plus + 2.5 * 0.1 * d3_minus + 1.5 * 0.1 * d4_minus + d2_plus, sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(x1 + x2 + d1_minus - d1_plus == 80, name="ProductionTimeConstraint")
model.addConstr(x1 + x2 - 80 + d2_minus - d2_plus == 10, name="OvertimeConstraint")
model.addConstr(x1 + d3_minus - d3_plus == 70, name="CurtainSalesConstraint")
model.addConstr(x2 + d4_minus - d4_plus == 45, name="ClothingSalesConstraint")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Optimal production plan:")
    print(f"Hours of production for curtain fabric: {x1.x:.2f}")
    print(f"Hours of production for clothing fabric: {x2.x:.2f}")
    print("Objective function value: {:.2f}".format(model.objval))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the hours of production for each type of fabric and the objective function value.

This script provides a complete example of using the `coptpy` library to solve the production planning problem for the textile factory, while satisfying all the constraints mentioned in the problem.

---

## Case 59  [SOLVE_FAILED]

**GT:** 5500  |  **3B:** None (Not Solved)  |  **8B:** 2220.0

### Question
A certain shoe store employs 5 full-time salespeople and 4 part-time salespeople. Their working hours and salary information are shown in Table 3.3.

Table 3.3

|  | Monthly Working Hours | Sales Volume (pairs/hour) | Salary (CNY/hour) | Overtime Pay (CNY/hour) |
| :---: | :---: | :---: | :---: | :---: |
| Full-time | 160 | 5 | 1 | 1.5 |
| Part-time | 80 | 2 | 0.6 | 0.7 |

A profit of 0.5 CNY is made for each pair of shoes sold. The store has the following objectives:

$p_{1}$: Monthly sales volume reaches 5500 pairs;
$p_{2}$: Full-time salespeople do not exceed 100 hours of overtime;

$p_{3}$: All salespeople are fully employed, but full-time employees should be given double consideration;

$p_{4}$: Minimize overtime hours as much as possible.

Try to establish an objective programming model for this problem.

### 3B formulation
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Shoe_Store_Optimization", LpMinimize)

# Decision variables
full_time_salespeople_hours = LpVariable('FullTimeSalespeopleHours', 0, None)
part_time_salespeople_hours = LpVariable('PartTimeSalespeopleHours', 0, None)
overtime_full_time_salespeople_hours = LpVariable('OvertimeFullTimeSalespeopleHours', 0, None)

# Objective function
prob += lpSum([full_time_salespeople_hours * 1.5 + overtime_full_time_salespeople_hours * 1.5 +
                part_time_salespeople_hours * 0.7,
                full_time_salespeople_hours * 2 + overtime_full_time_salespeople_hours]) == 0, "Total_Overtime_Hours"

# Constraints
prob += lpSum([full_time_salespeople_hours, part_time_salespeople_hours]) >= 100, "SalesVolumeConstraint"
prob += lpSum([full_time_salespeople_hours, part_time_salespeople_hours]) <= 200, "EmploymentConstraint"
prob += full_time_salespeople_hours + overtime_full_time_salespeople_hours <= 160, "FullTimeOvertimeConstraint"
prob += part_time_salespeople_hours <= 80, "PartTimeHoursConstraint"
prob += lpSum([full_time_salespeople_hours * 5, part_time_salespeople_hours * 2]) >= 5500, "SalesVolumeConstraint"

# Solve the problem
status = prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Cost: ", value(prob.objective))
```

This code sets up a linear programming model to address the given objectives. The constraints ensure that the total sales volume is at least 5500 pairs per month, full-time employees do not exceed 100 hours of overtime, all salespeople are fully employed (with double consideration for full-time employees), and it minimizes the total cost which includes both regular and overtime pay.

Please note that this model assumes a fixed number of full-time and part-time salespeople. If there were variable numbers based on demand or other factors, additional complexity would be required to incorporate those variables into the model.

### ORLM-8B formulation
## Mathematical Model:
To solve the optimization problem for the shoe store, we need to construct an objective programming model to balance the four objectives. The model can be formulated as follows:

### Decision Variables:
- \(x_{1}\): Total working hours of full-time salespeople (including regular working hours and overtime hours);
- \(x_{2}\): Total working hours of part-time salespeople.

### Objective Function:
- Minimize the weighted sum of deviations: \[Z = p_{1}d_{1}^{-} + p_{2}d_{2}^{+} + 2p_{3}d_{3}^{-} + p_{3}d_{4}^{-} + p_{4}d_{2}^{+}\]
  - where \(d_{1}^{-}\) represents the negative deviation of sales volume not reaching the target;
    - \(d_{2}^{+}\) represents the positive deviation of full-time salespeople's overtime hours exceeding 100 hours;
    - \(d_{3}^{-}\) represents the negative deviation of full-time salespeople not being fully employed;
    - \(d_{4}^{-}\) represents the negative deviation of part-time salespeople not being fully employed;
    - \(d_{2}^{+}\) represents the positive deviation of overtime hours.

### Constraints:
1. Sales volume constraint: \[5x_{1} + 2x_{2} \geq 5500\]
2. Full-time salespeople's overtime constraint: \[x_{1} - 160 \leq 100\]
3. Full-time salespeople's working hours constraint: \[x_{1} \geq 160\]
4. Part-time salespeople's working hours constraint: \[x_{2} \geq 80\]
5. Non-negativity constraint: \[x_{1}, x_{2} \geq 0\]

Using this model, we can apply objective programming techniques to find the optimal allocation of working hours for full-time and part-time salespeople, while satisfying all constraints, to achieve the objectives of the shoe store. This will provide the shoe store with an optimized resource allocation strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the objective programming problem for the shoe store:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ShoeStoreOptimization")

# Add decision variables
x1 = model.addVar(lb=0, name="x1")  # Total working hours of full-time salespeople
x2 = model.addVar(lb=0, name="x2")  # Total working hours of part-time salespeople

# Add deviation variables
d1_neg = model.addVar(lb=0, name="d1_neg")  # Negative deviation of sales volume not reaching the target
d2_pos = model.addVar(lb=0, name="d2_pos")  # Positive deviation of full-time salespeople's overtime hours exceeding 100 hours
d3_neg = model.addVar(lb=0, name="d3_neg")  # Negative deviation of full-time salespeople not being fully employed
d4_neg = model.addVar(lb=0, name="d4_neg")  # Negative deviation of part-time salespeople not being fully employed

# Set the objective function
model.setObjective(d1_neg + 100*d2_pos + 2*d3_neg + d4_neg + d2_pos, sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(5*x1 + 2*x2 >= 5500, name="SalesTarget")  # Sales volume constraint
model.addConstr(x1 - 160 <= 100, name="OvertimeLimit")  # Full-time salespeople's overtime constraint
model.addConstr(x1 >= 160, name="FullTimeWork")  # Full-time salespeople's working hours constraint
model.addConstr(x2 >= 80, name="PartTimeWork")  # Part-time salespeople's working hours constraint

# Add deviation constraints
model.addConstr(5*x1 + 2*x2 - 5500 <= d1_neg, name="d1_neg_constr")  # Negative deviation of sales volume not reaching the target
model.addConstr(x1 - 160 - 100 <= d2_pos, name="d2_pos_constr")  # Positive deviation of full-time salespeople's overtime hours exceeding 100 hours
model.addConstr(x1 - 160 <= d3_neg, name="d3_neg_constr")  # Negative deviation of full-time salespeople not being fully employed
model.addConstr(x2 - 80 <= d4_neg, name="d4_neg_constr")  # Negative deviation of part-time salespeople not being fully employed

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Optimal objective value: {:.2f}".format(model.objval))
    print("Total working hours of full-time salespeople: {:.2f}".format(x1.x))
    print("Total working hours of part-time salespeople: {:.2f}".format(x2.x))
    print("Negative deviation of sales volume not reaching the target: {:.2f}".format(d1_neg.x))
    print("Positive deviation of full-time salespeople's overtime hours exceeding 100 hours: {:.2f}".format(d2_pos.x))
    print("Negative deviation of full-time salespeople not being fully employed: {:.2f}".format(d3_neg.x))
    print("Negative deviation of part-time salespeople not being fully employed: {:.2f}".format(d4_neg.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add decision variables `x1` and `x2`, representing the total working hours of full-time and part-time salespeople, respectively.

Next, we add deviation variables `d1_neg`, `d2_pos`, `d3_neg`, and `d4_neg`, representing the negative deviation of sales volume not reaching the target, the positive deviation of full-time salespeople's overtime hours exceeding 100 hours, the negative deviation of full-time salespeople not being fully employed, and the negative deviation of part-time salespeople not being fully employed, respectively.

The objective function is set to minimize the weighted sum of deviations, where the weights are determined based on the problem description.

Then, we add constraints, including the sales volume constraint, the full-time salespeople's overtime constraint, the full-time salespeople's working hours constraint, and the part-time salespeople's working hours constraint.

We also add deviation constraints to ensure that the deviation variables correctly represent the deviations between the actual values and the target values.

Finally, we solve the model and output the results, including the optimal objective value, the total working hours of full-time and part-time salespeople, and the values of the deviation variables.

This script provides a complete example of using the `coptpy` library to solve the objective programming problem for the shoe store, while satisfying all the constraints mentioned in the problem description.

---
