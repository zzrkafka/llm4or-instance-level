# Contrastive pairs (IndustryOR): 3B wrong vs ORLM-8B correct

3B wrong: 88 | of which 8B correct: 29


## Case 1

**Ground truth:** 3050.0  |  **3B answer:** None (Not Solved)  |  **8B answer:** 3050.0

### Question
The Zhang family has 6 children, Harry, Hermione, Ron, Fred, George, and Ginny. The cost of taking Harry is $1200, Hermione is $1650, Ron is $750, Fred is $800, George is $800, and Ginny is $1500. Which children should the couple take to minimize the total cost of taking the children?

They can take a maximum of 4 children on the upcoming trip.

Ginny is the youngest, so the Zhang family will definitely take her.

If the couple takes Harry, they will not take Fred because Harry doesn't get along with him.

If the couple takes Harry, they will not take George because Harry doesn't get along with him.

If they take George, they must also take Fred.

If they take George, they must also take Hermione.

Although this will cost them a lot of money, the Zhang family has decided to take at least three children.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Zhang_Family_Trip", LpMinimize)

# Define decision variables
children = ['Harry', 'Hermione', 'Ron', 'Fred', 'George']
variables = LpVariable.dicts('child', children, 0, None, LpInteger)

# Objective function: minimize total cost
prob += lpSum([variables[child] * costs[child] for child in children], "Total_Cost")

# Constraints
# Constraint 1: At least one child must be taken (Ginny is already included)
prob += variables['Harry'] + variables['Hermione'] + variables['Ron'] + variables['Fred'] + variables['George'] >= 3

# Constraint 2: If Harry is taken, Fred and George cannot be taken
prob += variables['Harry'] <= variables['Ron']
prob += variables['Harry'] <= variables['Hermione']

# Constraint 3: If George is taken, both Fred and Hermione must also be taken
prob += variables['George'] >= variables['Fred']
prob += variables['George'] >= variables['Hermione']

# Constraint 4: Maximum of 4 children can be taken
prob += lpSum(variables.values()) <= 4

# Costs for each child
costs = {
    'Harry': 1200,
    'Hermione': 1650,
    'Ron': 750,
    'Fred': 800,
    'George': 800,
}

# Solve the problem
prob.solve()

# Print which children are taken and total cost
for child in children:
    if variables[child].varValue > 0:
        print(f"Taking: {child}")
print(f"Total Cost: ${variables['Harry'].varValue * costs['Harry'] + variables['Hermione'].varValue * costs['Hermione'] + variables['Ron'].varValue * costs['Ron'] + variables['Fred'].varValue * costs['Fred'] + variables['George'].varValue * costs['George']}")

# Output the result
for child in children:
    if variables[child].varValue > 0:
        print(f"Taking: {child}")
print(f"Total Cost: ${variables['Harry'].varValue * costs['Harry'] + variables['Hermione'].varValue * costs['Hermione'] + variables['Ron'].varValue * costs['Ron'] + variables['Fred'].varValue * costs['Fred'] + variables['George'].varValue * costs['George']}")
```

This code sets up and solves the problem as described, ensuring that the constraints are met while minimizing the total cost.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the Zhang family's problem of taking children, we need to construct an integer programming model to minimize the total cost of taking the children while satisfying the given constraints. Here is the model formulation:

### Decision Variables:
- \(x_H\): 1 if Harry is taken, 0 otherwise.
- \(x_R\): 1 if Hermione is taken, 0 otherwise.
- \(x_W\): 1 if Ron is taken, 0 otherwise.
- \(x_F\): 1 if Fred is taken, 0 otherwise.
- \(x_G\): 1 if George is taken, 0 otherwise.
- \(x_GI\): 1 if Ginny is taken, 0 otherwise.

### Objective Function:
- Minimize the total cost: \(Z = 1200x_H + 1650x_R + 750x_W + 800x_F + 800x_G + 1500x_GI\)

### Constraints:
1. Ginny must be taken: \(x_GI = 1\)
2. If Harry is taken, Fred cannot be taken: \(x_H + x_F \leq 1\)
3. If Harry is taken, George cannot be taken: \(x_H + x_G \leq 1\)
4. If George is taken, Fred must be taken: \(x_G \leq x_F\)
5. If George is taken, Hermione must be taken: \(x_G \leq x_R\)
6. At least three children must be taken: \(x_H + x_R + x_W + x_F + x_G + x_GI \geq 3\)
7. A maximum of 4 children can be taken: \(x_H + x_R + x_W + x_F + x_G + x_GI \leq 4\)

### Binary Constraints:
- \(x_H, x_R, x_W, x_F, x_G, x_GI \in \{0, 1\}\)

Using this model, we can apply integer programming techniques to find the optimal combination of children to take, minimizing the total cost while satisfying all the constraints. This will provide the Zhang family with an economically efficient strategy for taking children.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ZhangFamilyVacation")

# Add decision variables
x_H = model.addVar(vtype=COPT.BINARY, name="x_H")  # Harry
x_R = model.addVar(vtype=COPT.BINARY, name="x_R")  # Hermione
x_W = model.addVar(vtype=COPT.BINARY, name="x_W")  # Ron
x_F = model.addVar(vtype=COPT.BINARY, name="x_F")  # Fred
x_G = model.addVar(vtype=COPT.BINARY, name="x_G")  # George
x_GI = model.addVar(vtype=COPT.BINARY, name="x_GI")  # Ginny

# Set the objective function: minimize total cost
model.setObjective(1200*x_H + 1650*x_R + 750*x_W + 800*x_F + 800*x_G + 1500*x_GI, sense=COPT.MINIMIZE)

# Add constraints
model.addConstr(x_GI == 1, name="GinnyMustBeTaken")
model.addConstr(x_H + x_F <= 1, name="HarryNotWithFred")
model.addConstr(x_H + x_G <= 1, name="HarryNotWithGeorge")
model.addConstr(x_G <= x_F, name="GeorgeImpliesFred")
model.addConstr(x_G <= x_R, name="GeorgeImpliesHermione")
model.addConstr(x_H + x_R + x_W + x_F + x_G + x_GI >= 3, name="AtLeastThreeChildren")
model.addConstr(x_H + x_R + x_W + x_F + x_G + x_GI <= 4, name="AtMostFourChildren")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} dollars".format(model.objval))
    print("Children taken:")
    if x_H.x == 1:
        print("- Harry")
    if x_R.x == 1:
        print("- Hermione")
    if x_W.x == 1:
        print("- Ron")
    if x_F.x == 1:
        print("- Fred")
    if x_G.x == 1:
        print("- George")
    if x_GI.x == 1:
        print("- Ginny")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the children taken.

This script provides a complete example of using the `coptpy` library to solve the Zhang family's problem of taking children, while satisfying all the constraints mentioned in the problem.

---

## Case 2

**Ground truth:** 135000.0  |  **3B answer:** 170500.0 (Optimal)  |  **8B answer:** 135000.0

### Question
The Li family plans to invest their retirement fund in commercial real estate. Property 1 has an annual income of $12,500, Property 2 has an annual income of $35,000, Property 3 has an annual income of $23,000, and Property 4 has an annual income of $100,000. The decision to be made is whether to buy or not buy each property, not the quantity, as there is only one property per property. Help them decide which properties to purchase to maximize their annual income.
Property 1 costs $1.5 million, Property 2 costs $2.1 million, Property 3 costs $2.3 million, and Property 4 costs $4.2 million. The Li family's budget is $7 million.

If they purchase Property 4, then they cannot purchase Property 3.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Li_Family_Investment_Problem", LpMaximize)

# Decision variables: binary variable to indicate whether property is bought (1) or not (0)
x1 = LpVariable('Property_1', cat='Binary')
x2 = LpVariable('Property_2', cat='Binary')
x3 = LpVariable('Property_3', cat='Binary')
x4 = LpVariable('Property_4', cat='Binary')

# Objective function: maximize annual income
prob += 12500 * x1 + 35000 * x2 + 23000 * x3 + 100000 * x4

# Constraints: budget and property purchase restrictions
budget_constraint = 1.5e6 * x1 + 2.1e6 * x2 + 2.3e6 * x3 + 4.2e6 * x4 <= 7000000
property_3_not_if_property_4 = x3 >= 1 - x4

# Solve the problem
prob.solve()

# Print which properties are bought and their total annual income
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")
print(f"Total Annual Income: ${value(prob.objective):.2f}")
```

This code sets up a linear programming model to maximize the Li family's annual income from purchasing commercial real estate, considering their budget and property purchase restrictions. The `PuLP` library is used to define the problem, including decision variables for each property (whether it's bought or not), an objective function that maximizes total annual income, and constraints based on the given conditions.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To help the Li family maximize their annual income, we will construct an integer programming model to determine which properties to purchase. Here is the detailed construction process of the model:

### Decision Variables:
- \(x_1, x_2, x_3, x_4\): These are 0-1 integer variables, where \(x_i = 1\) indicates the purchase of Property \(i\), and \(x_i = 0\) indicates not purchasing Property \(i\).

### Objective Function:
- Maximize annual income: \[Z = 12500x_1 + 35000x_2 + 23000x_3 + 100000x_4\]

### Constraints:
1. Budget constraint: \[1500000x_1 + 2100000x_2 + 2300000x_3 + 4200000x_4 \leq 7000000\]
2. Mutual exclusion constraint between Property 3 and Property 4: \[x_3 + x_4 \leq 1\]

With this model, we can use integer programming techniques to determine which properties the Li family should purchase to maximize their annual income while staying within their budget. This will provide the Li family with an optimal investment decision.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("RealEstateInvestment")

# Add decision variables
x1 = model.addVar(vtype=COPT.BINARY, name="x1")
x2 = model.addVar(vtype=COPT.BINARY, name="x2")
x3 = model.addVar(vtype=COPT.BINARY, name="x3")
x4 = model.addVar(vtype=COPT.BINARY, name="x4")

# Objective function: Maximize annual income
model.setObjective(12500 * x1 + 35000 * x2 + 23000 * x3 + 100000 * x4, sense=COPT.MAXIMIZE)

# Constraints
# Budget constraint
model.addConstr(1500000 * x1 + 2100000 * x2 + 2300000 * x3 + 4200000 * x4 <= 7000000, name="Budget")

# Mutual exclusion constraint between Property 3 and Property 4
model.addConstr(x3 + x4 <= 1, name="MutualExclusion")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized annual income: {:.2f} dollars".format(model.objval))
    print("Purchase decisions:")
    print("Property 1: {}".format("Purchase" if x1.x > 0.5 else "Do not purchase"))
    print("Property 2: {}".format("Purchase" if x2.x > 0.5 else "Do not purchase"))
    print("Property 3: {}".format("Purchase" if x3.x > 0.5 else "Do not purchase"))
    print("Property 4: {}".format("Purchase" if x4.x > 0.5 else "Do not purchase"))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add four binary decision variables representing whether to purchase each property. We set the objective function to maximize annual income and add the budget constraint and mutual exclusion constraint between Property 3 and Property 4. Finally, we solve the model and output the results of the optimal solution, including the maximized annual income and the purchase decisions for each property.

This script provides a complete example of using the `coptpy` library to solve the Li family's real estate investment problem while satisfying all the constraints mentioned in the problem.

---

## Case 3

**Ground truth:** 1600.0  |  **3B answer:** 1400.0 (Optimal)  |  **8B answer:** 1600.0

### Question
The Lee family has 5 children, Alice, Bob, Charlie, Diana, and Ella. The cost of taking Alice is $1000, Bob is $900, Charlie is $600, Diana is $500, and Ella is $700. Which children should the couple take to minimize the total cost of taking the children?
They can take a maximum of 3 children together on the upcoming trip.

Bob is the youngest, so the Lee family will definitely take him.

If the couple takes Alice, they will not take Diana because Alice and Diana do not get along.

If the couple takes Bob, they will not take Charlie because Bob and Charlie do not get along.

If they take Charlie, they must also take Diana.

If they take Diana, they must also take Ella.

Although it will cost them a lot of money, the Lee family has decided to take at least two children.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum

# Create the LP problem
prob = LpProblem("Lee_family_trip", LpMinimize)

# Decision variables: 1 if child is taken, 0 otherwise
alice = LpVariable('Alice', cat='Binary')
bob = LpVariable('Bob', cat='Binary')
charlie = LpVariable('Charlie', cat='Binary')
diana = LpVariable('Diana', cat='Binary')
ella = LpVariable('Ella', cat='Binary')

# Objective function: minimize total cost
prob += lpSum([1000*alice, 900*bob, 600*charlie, 500*diana, 700*ella]), "Total_Cost"

# Constraints
# Bob is definitely taken
prob += bob == 1

# If Alice is taken, Diana cannot be taken
prob += alice + diana <= 1

# If Bob is taken, Charlie cannot be taken
prob += bob + charlie <= 1

# If Charlie is taken, Diana must also be taken
prob += charlie + diana >= 1

# If Diana is taken, Ella must also be taken
prob += diana + ella >= 1

# At least two children are taken
prob += alice + bob + charlie + diana + ella >= 2

# Solve the problem
prob.solve()

# Print results
for variable in prob.variables():
    print(f"{variable.name} = {variable.varValue}")

print(f"Total Cost: ${value(prob.objective):.2f}")
```

This code sets up a linear programming model to solve the given problem using PuLP, and it includes constraints based on the conditions provided for taking children together. The solution will indicate which children are taken and the total cost of the trip.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the Lee family's problem of taking children, we need to construct an integer programming model to minimize the total cost of taking the children while satisfying the given constraints. Here is the model formulation:

### Decision Variables:
- \(x_A\): 1 if Alice is taken, 0 otherwise.
- \(x_B\): 1 if Bob is taken, 0 otherwise.
- \(x_C\): 1 if Charlie is taken, 0 otherwise.
- \(x_D\): 1 if Diana is taken, 0 otherwise.
- \(x_E\): 1 if Ella is taken, 0 otherwise.

### Objective Function:
- Minimize the total cost: \(Z = 1000x_A + 900x_B + 600x_C + 500x_D + 700x_E\)

### Constraints:
1. Bob is the youngest and must be taken: \(x_B = 1\)
2. If Alice is taken, Diana cannot be taken: \(x_A + x_D \leq 1\)
3. If Bob is taken, Charlie cannot be taken: \(x_B + x_C \leq 1\)
4. If Charlie is taken, Diana must be taken: \(x_C \leq x_D\)
5. If Diana is taken, Ella must be taken: \(x_D \leq x_E\)
6. At most 3 children can be taken: \(x_A + x_B + x_C + x_D + x_E \leq 3\)
7. At least 2 children must be taken: \(x_A + x_B + x_C + x_D + x_E \geq 2\)

### Binary Constraints:
- \(x_A, x_B, x_C, x_D, x_E \in \{0, 1\}\)

Using this model, we can apply integer programming techniques to find the optimal solution for which children to take to minimize the total cost while satisfying all the constraints. This will provide the Lee family with an economically efficient strategy for taking children.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("FamilyVacationOptimization")

# Add decision variables
x_A = model.addVar(vtype=COPT.BINARY, name="x_A")  # Alice
x_B = model.addVar(vtype=COPT.BINARY, name="x_B")  # Bob
x_C = model.addVar(vtype=COPT.BINARY, name="x_C")  # Charlie
x_D = model.addVar(vtype=COPT.BINARY, name="x_D")  # Diana
x_E = model.addVar(vtype=COPT.BINARY, name="x_E")  # Ella

# Objective function: Minimize total cost
model.setObjective(1000 * x_A + 900 * x_B + 600 * x_C + 500 * x_D + 700 * x_E, sense=COPT.MINIMIZE)

# Constraints
model.addConstr(x_B == 1, name="BobMandatory")
model.addConstr(x_A + x_D <= 1, name="AliceOrDiana")
model.addConstr(x_B + x_C <= 1, name="BobOrCharlie")
model.addConstr(x_C <= x_D, name="CharlieImpliesDiana")
model.addConstr(x_D <= x_E, name="DianaImpliesElla")
model.addConstr(x_A + x_B + x_C + x_D + x_E <= 3, name="MaxChildren")
model.addConstr(x_A + x_B + x_C + x_D + x_E >= 2, name="MinChildren")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} dollars".format(model.objval))
    print("Children taken:")
    if x_A.x == 1:
        print("- Alice")
    if x_B.x == 1:
        print("- Bob")
    if x_C.x == 1:
        print("- Charlie")
    if x_D.x == 1:
        print("- Diana")
    if x_E.x == 1:
        print("- Ella")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables and set the objective function and constraints. Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the children taken.

This script provides a complete example of using the `coptpy` library to solve the Lee family's problem of taking children while satisfying all the constraints mentioned in the problem.

---

## Case 4

**Ground truth:** 90000.0  |  **3B answer:** 135000.0 (Optimal)  |  **8B answer:** 90000.0

### Question
The Zhang family has decided to invest in several different restaurants. Restaurant A has an annual income of $15,000, Restaurant B has an annual income of $40,000, Restaurant C has an annual income of $30,000, and Restaurant D has an annual income of $50,000. They need to decide whether to purchase each restaurant, and each restaurant can only be purchased once. Help them decide which restaurants to purchase to maximize their annual income.
The cost of Restaurant A is $1.6 million, the cost of Restaurant B is $2.5 million, the cost of Restaurant C is $1.8 million, and the cost of Restaurant D is $3 million. The Zhang family's investment budget is $6 million.

If they purchase Restaurant D, they cannot purchase Restaurant A.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Zhang_Family_Investment_Problem", LpMaximize)

# Define decision variables
purchase_A = LpVariable('A', lowBound=0, cat='Binary')
purchase_B = LpVariable('B', lowBound=0, cat='Binary')
purchase_C = LpVariable('C', lowBound=0, cat='Binary')
purchase_D = LpVariable('D', lowBound=0, cat='Binary')

# Objective function: Maximize total income
prob += 15000*purchase_A + 40000*purchase_B + 30000*purchase_C + 50000*purchase_D

# Constraints:
# Budget constraint
budget_constraint = 1600000*purchase_A + 2500000*purchase_B + 1800000*purchase_C + 3000000*purchase_D <= 6000000

# Restaurant D cannot be purchased if A is purchased
prob += purchase_D >= purchase_A

# Solve the problem
prob.solve()

# Print which restaurants are purchased and their total income
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Income: ${value(prob.objective):.2f}")
```

This code sets up a linear programming model to maximize the Zhang family's annual income given their investment budget constraints, including the constraint that if Restaurant D is purchased, then Restaurant A cannot be purchased.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To help the Zhang family maximize their annual income, we need to construct an integer programming model to determine which restaurants to purchase. Here is the model formulation:

### Decision Variables:
- \( y_A \): 1 if Restaurant A is purchased, 0 otherwise.
- \( y_B \): 1 if Restaurant B is purchased, 0 otherwise.
- \( y_C \): 1 if Restaurant C is purchased, 0 otherwise.
- \( y_D \): 1 if Restaurant D is purchased, 0 otherwise.

### Objective Function:
- Maximize annual income: \[Z = 15000y_A + 40000y_B + 30000y_C + 50000y_D\]

### Constraints:
1. Investment budget constraint:
   - \(160y_A + 250y_B + 180y_C + 300y_D \leq 600\)
2. Restaurant D and Restaurant A purchase exclusion constraint:
   - \(y_D + y_A \leq 1\)

### Binary Constraints:
- \(y_A, y_B, y_C, y_D \in \{0, 1\}\)

With this model, we can use integer programming techniques to determine which restaurants the Zhang family should purchase to maximize their annual income while staying within their investment budget. This will provide the Zhang family with an optimal investment decision.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("RestaurantInvestment")

# Add decision variables
y_A = model.addVar(vtype=COPT.BINARY, name="y_A")  # Whether to purchase Restaurant A
y_B = model.addVar(vtype=COPT.BINARY, name="y_B")  # Whether to purchase Restaurant B
y_C = model.addVar(vtype=COPT.BINARY, name="y_C")  # Whether to purchase Restaurant C
y_D = model.addVar(vtype=COPT.BINARY, name="y_D")  # Whether to purchase Restaurant D

# Objective function: Maximize annual income
model.setObjective(15000 * y_A + 40000 * y_B + 30000 * y_C + 50000 * y_D, sense=COPT.MAXIMIZE)

# Constraints
# Investment budget constraint
model.addConstr(160 * y_A + 250 * y_B + 180 * y_C + 300 * y_D <= 600, name="BudgetConstraint")

# Restaurant D and Restaurant A purchase exclusion constraint
model.addConstr(y_D + y_A <= 1, name="ExclusivePurchase")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Maximized annual income: {:.2f} dollars".format(model.objval))
    print("Purchase Restaurant A: {}".format("Yes" if y_A.x > 0.5 else "No"))
    print("Purchase Restaurant B: {}".format("Yes" if y_B.x > 0.5 else "No"))
    print("Purchase Restaurant C: {}".format("Yes" if y_C.x > 0.5 else "No"))
    print("Purchase Restaurant D: {}".format("Yes" if y_D.x > 0.5 else "No"))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add four binary decision variables representing whether to purchase each restaurant. The objective function is set to maximize annual income, and we add two constraints: the investment budget constraint and the purchase exclusion constraint for Restaurant D and Restaurant A.

Finally, we solve the model and output the results of the optimal solution, including the maximized annual income and the decision of whether to purchase each restaurant.

This script provides a complete example of using the `coptpy` library to solve the Zhang family's restaurant investment problem while satisfying all the constraints mentioned in the problem.

---

## Case 5

**Ground truth:** 38000  |  **3B answer:** 0.0 (Optimal)  |  **8B answer:** 38000.0

### Question
A company needs to decide whether to hire some of the five candidates to join their research and development team. The salary requirements for candidates F, G, H, I, and J are $12,000, $15,000, $18,000, $5,000, and $10,000 respectively. The company wants to minimize the total amount paid to the candidates while staying within the budget.

The company has a budget of $40,000 and wants to hire a maximum of 4 new employees.

The skill levels of the candidates are as follows:
Candidate F: Level 2
Candidate G: Level 3
Candidate H: Level 4
Candidate I: Level 1
Candidate J: Level 2
The company needs to ensure that the total skill level of the hired employees is at least 8.

The project management experience in years for each candidate is as follows:
Candidate F: 1 year
Candidate G: 2 years
Candidate H: 2 years
Candidate I: 5 years
Candidate J: 4 years
They want the total project management experience in the team to be at least 8 years.

Due to the similar technical backgrounds of candidates G and J, the company can only choose one of them at most.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Create a problem
prob = LpProblem("HiringCandidates", LpMinimize)

# Decision variables: 1 if candidate is hired, 0 otherwise
x_F = LpVariable('F', lowBound=0, cat='Continuous')
x_G = LpVariable('G', lowBound=0, cat='Continuous')
x_H = LpVariable('H', lowBound=0, cat='Continuous')
x_I = LpVariable('I', lowBound=0, cat='Continuous')
x_J = LpVariable('J', lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
prob += lpSum([12000*x_F, 15000*x_G, 18000*x_H, 5000*x_I, 10000*x_J])

# Constraints:
# Budget constraint
budget_constraint = prob.addConstraint(lpSum([12000*x_F, 15000*x_G, 18000*x_H, 5000*x_I, 10000*x_J]) <= 40000)

# Maximum hires constraint
max_hires_constraint = prob.addConstraint(lpSum([x_F, x_G, x_H, x_I, x_J]) <= 4)

# Skill level constraint
skill_level_constraint = prob.addConstraint(8 >= lpSum([2*x_F + 3*x_G + 4*x_H + 1*x_I + 2*x_J]))

# Project management experience constraint
experience_constraint = prob.addConstraint(8 >= lpSum([1*x_F + 2*x_G + 2*x_H + 5*x_I + 4*x_J]))

# Constraint to limit G and J at most one
at_most_one_of_G_and_J = prob.addConstraint(x_G + x_J <= 1)

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total cost: ${value(prob.objective):.2f}")
```

Please note that this code uses PuLP to define and solve a linear programming problem based on the given constraints and objective function. The `lpSum` function is used to sum up the contributions of each candidate's salary, skill level, and project management experience towards their respective constraints.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
### Decision Variables:
- \( x_F, x_G, x_H, x_I, x_J \): Binary variables representing whether to hire candidates F, G, H, I, and J. 1 indicates hiring, 0 indicates not hiring.

### Constraints:
1. **Budget Constraint**:
   $$
   12000x_F + 15000x_G + 18000x_H + 5000x_I + 10000x_J \leq 40000
   $$
   Ensures that the total salary does not exceed the budget.

2. **Number of Hired Employees Constraint**:
   $$
   x_F + x_G + x_H + x_I + x_J \leq 4
   $$
   Ensures that the number of hired employees does not exceed 4.

3. **Skill Level Constraint**:
   $$
   2x_F + 3x_G + 4x_H + 1x_I + 2x_J \geq 8
   $$
   Ensures that the total skill level of the hired employees is at least 8.

4. **Project Management Experience Constraint**:
   $$
   1x_F + 2x_G + 2x_H + 5x_I + 4x_J \geq 8
   $$
   Ensures that the total project management experience in the team is at least 8 years.

5. **Mutual Exclusivity Constraint for Candidates G and J**:
   $$
   x_G + x_J \leq 1
   $$
   Ensures that at most one of candidates G and J is hired.

### Objective:
Minimize the total salary:
$$
\min Z = 12000x_F + 15000x_G + 18000x_H + 5000x_I + 10000x_J
$$

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create a COPT environment
env = Envr()

# Create a model
model = env.createModel("Hiring")

# Add decision variables
x_F = model.addVar(vtype=COPT.BINARY, name='x_F')
x_G = model.addVar(vtype=COPT.BINARY, name='x_G')
x_H = model.addVar(vtype=COPT.BINARY, name='x_H')
x_I = model.addVar(vtype=COPT.BINARY, name='x_I')
x_J = model.addVar(vtype=COPT.BINARY, name='x_J')

# Set the objective function
model.setObjective(12000 * x_F + 15000 * x_G + 18000 * x_H + 5000 * x_I + 10000 * x_J, COPT.MINIMIZE)

# Add constraints
model.addConstr(12000 * x_F + 15000 * x_G + 18000 * x_H + 5000 * x_I + 10000 * x_J <= 40000, "Budget")
model.addConstr(x_F + x_G + x_H + x_I + x_J <= 4, "Max_Hires")
model.addConstr(2 * x_F + 3 * x_G + 4 * x_H + 1 * x_I + 2 * x_J >= 8, "Skill_Level")
model.addConstr(1 * x_F + 2 * x_G + 2 * x_H + 5 * x_I + 4 * x_J >= 8, "Experience")
model.addConstr(x_G + x_J <= 1, "Exclusive_G_J")

# Solve the model
model.solve()

# Output the results
print('Optimal hiring strategy:')
print(f' Hire F: {x_F.x}, G: {x_G.x}, H: {x_H.x}, I: {x_I.x}, J: {x_J.x}')
print('Total Cost: ${}'.format(model.objVal))
```

This script uses the COPTPY library to create and solve a linear programming model to determine the optimal hiring strategy that minimizes the total salary while satisfying all constraints.

---

## Case 6

**Ground truth:** 53  |  **3B answer:** None (?)  |  **8B answer:** 53.0

### Question
A certain 24-hour convenience store requires a certain number of salespersons during each time period as follows: 2:00-6:00 - 10 people, 6:00-10:00 - 15 people, 10:00-14:00 - 25 people, 14:00-18:00 - 20 people, 18:00-22:00 - 18 people, 22:00-2:00 - 12 people. Salespersons work at 2:00, 6:00, 10:00, 14:00, 18:00, and 22:00, and work continuously for 8 hours. Determine the minimum number of salespersons needed to meet the requirements.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Create a problem
prob = LpProblem("Salesperson_Distribution", LpMinimize)

# Define decision variables
salespersons = {}
for time in [2, 6, 10, 14, 18, 22]:
    salespersons[time] = LpVariable(f'salespersons_{time}', lowBound=0, cat='Integer')

# Objective function: minimize the number of salespersons
prob += lpSum[salespersons[t] for t in salespersons]

# Constraints based on required salespeople per time period
constraints = [
    (2, 10),
    (6, 15),
    (10, 25),
    (14, 20),
    (18, 18),
    (22, 12)
]

for start_time, required in constraints:
    prob += lpSum[salespersons[t] for t in range(start_time, min(start_time + 8, 24), 4)] >= required

# Solve the problem
prob.solve()

# Print the results
print("Status:", LpProblem.status[prob.status])
for salesperson in salespersons:
    print(f"Salespersons at {salesperson}: {round(value(salespersons[salesperson]))}")
```

Please note that this code uses `value()` to get the value of the variables, which is a method from PuLP. The constraints are formulated based on the requirement that each salesperson works for 8 hours starting from their assigned time slot.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the staffing problem for the convenience store, we need to construct a linear programming model to minimize the total number of salespersons while meeting the staffing requirements for each time period. Here is the model formulation:

### Decision Variables:
- \(x_j\): The number of salespersons starting work at time \(j\), where \(j = 1, 2, 3, 4, 5, 6\) corresponds to the start times 2:00, 6:00, 10:00, 14:00, 18:00, and 22:00.

### Objective Function:
- Minimize the total number of salespersons: \[Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6\]

### Constraints:
- Meet the staffing requirements for each time period:
  - \(x_6 + x_1 \geq 10\) (2:00-6:00)
  - \(x_1 + x_2 \geq 15\) (6:00-10:00)
  - \(x_2 + x_3 \geq 25\) (10:00-14:00)
  - \(x_3 + x_4 \geq 20\) (14:00-18:00)
  - \(x_4 + x_5 \geq 18\) (18:00-22:00)
  - \(x_5 + x_6 \geq 12\) (22:00-2:00)

### Non-negativity Constraints:
- \(x_j \geq 0\), for all \(j = 1, 2, 3, 4, 5, 6\)

Using this model, we can apply linear programming techniques to find the minimum number of salespersons needed to meet the staffing requirements for each time period, while minimizing the total number of salespersons. This will provide the convenience store with an economically efficient staffing strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("StaffingPlan")

# Add decision variables
x = model.addVars(6, vtype=COPT.INTEGER, lb=0, nameprefix="x")

# Objective function: Minimize the total number of salespersons
model.setObjective(cp.quicksum(x[j] for j in range(6)), sense=COPT.MINIMIZE)

# Constraints: Meet the staffing requirements for each time period
model.addConstr(x[5] + x[0] >= 10, name="Staff_2_6")
model.addConstr(x[0] + x[1] >= 15, name="Staff_6_10")
model.addConstr(x[1] + x[2] >= 25, name="Staff_10_14")
model.addConstr(x[2] + x[3] >= 20, name="Staff_14_18")
model.addConstr(x[3] + x[4] >= 18, name="Staff_18_22")
model.addConstr(x[4] + x[5] >= 12, name="Staff_22_2")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum number of salespersons: {}".format(model.objval))
    for j in range(6):
        print("Number of salespersons starting work at {}: {}".format(j*4+2, x[j].x))
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables `x` representing the number of salespersons starting work at each time period. The objective function is to minimize the total number of salespersons, which is the sum of all `x` variables.

We add six constraints to ensure that the staffing requirements for each time period are met. Finally, we solve the model and output the results of the optimal solution, including the minimum number of salespersons and the number of salespersons starting work at each time period.

This script provides a complete example of using the `coptpy` library to solve the staffing problem for the convenience store, while satisfying all the constraints mentioned in the problem.

---

## Case 7

**Ground truth:** 20240  |  **3B answer:** -720.0000000000005 (Optimal)  |  **8B answer:** 20242.0

### Question
A farm has 100 hectares of land and 15,000 yuan available for production development. The farm has a labor force of 3,500 person-days in autumn and winter, and 4,000 person-days in spring and summer. If the labor force is not fully utilized, they can work outside. The wage for hired labor is 2.1 yuan/person-day in spring and summer, and 1.8 yuan/person-day in autumn and winter. The farm grows three crops: soybeans, corn, and wheat, and raises cows and chickens. There is no need for additional investment when planting crops, but for animal farming, it costs 400 yuan per cow and 3 yuan per chicken. When raising cows, 1.5 hectares of land are needed to grow grass for each cow, and it requires 100 person-days of labor in autumn and winter, and 50 person-days in spring and summer. The net income per cow per year is 400 yuan. When raising chickens, no land is needed, but it requires 0.6 person-days of labor in autumn and winter, and 0.3 person-days in spring and summer. The net income per chicken per year is 2 yuan. The farm has a chicken coop that can accommodate up to 3,000 chickens, and a cowshed that can accommodate up to 32 cows. The labor requirements and net income per hectare per year for the three crops are shown in Table 1-9.

Table 1-9
\begin{tabular}{l|c|c|c}
\hline \multicolumn{1}{c}{ Crop } & Soybeans & Corn & Wheat \\
\hline Person-days required in autumn and winter & 20 & 35 & 10 \\
Person-days required in spring and summer & 50 & 75 & 40 \\
Net income per hectare per year (yuan/hm^2) & 175 & 300 & 120 \\
\hline
\end{tabular}

Determine the farm's operating plan to maximize net income per year.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Farm_Operations", LpMaximize)

# Decision variables
x1 = LpVariable('Soybeans', lowBound=0, cat='Continuous')
x2 = LpVariable('Corn', lowBound=0, cat='Continuous')
x3 = LpVariable('Wheat', lowBound=0, cat='Continuous')
x4 = LpVariable('Cows', lowBound=0, cat='Continuous')
x5 = LpVariable('Chickens', lowBound=0, cat='Continuous')

# Objective function: Maximize net income
prob += lpSum([175*x1 + 300*x2 + 120*x3 - 400*x4 - 3*x5]), "Net Income"

# Constraints

# Land constraint
land_constraint = lpSum([x1, x2, x3]) <= 100
prob += land_constraint, "Land Constraint"

# Labor constraint (autumn and winter)
labor_autumn_winter = lpSum([
    20*x1 + 50*x2 + 10*x3,
    1.8*(20*x1 + 50*x2 + 10*x3) <= 3500
])
prob += labor_autumn_winter, "Labor Constraint (Autumn and Winter)"

# Labor constraint (spring and summer)
labor_spring_summer = lpSum([
    35*x1 + 75*x2 + 40*x3,
    1.8*(35*x1 + 75*x2 + 40*x3) <= 4000
])
prob += labor_spring_summer, "Labor Constraint (Spring and Summer)"

# Animal farming constraint: cows and chickens
animal_constraint = lpSum([
    x4,
    1.5*x4,
    0.6*x5 + 0.3*x5 <= 3500
])
prob += animal_constraint, "Animal Farming Constraint"

# Cow capacity constraint
cow_capacity = x4 <= 32
prob += cow_capacity, "Cow Capacity Constraint"

# Chicken capacity constraint
chicken_capacity = x5 <= 3000
prob += chicken_capacity, "Chicken Capacity Constraint"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Maximum Net Income: {value(prob.objective)}")
```

This code sets up and solves a linear programming model using PuLP to determine the optimal allocation of land, labor, and resources for maximizing net income per year on the farm. The constraints include land availability, labor requirements in different seasons, animal farming capacity limits, and production costs.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the farm's operating plan problem, we need to construct a mathematical model to maximize net income while satisfying constraints on land, capital, labor, and animal farming facilities. The model can be formulated as follows:

### Decision Variables:
- \(x_1, x_2, x_3\): Represent the area (in hectares) planted with soybeans, corn, and wheat, respectively.
- \(x_4, x_5\): Represent the number of cows and chickens raised, respectively.
- \(x_6, x_7\): Represent the additional labor force hired in spring and summer, and autumn and winter, respectively.

### Objective Function:
- Maximize net income: \[Z = 175x_1 + 300x_2 + 120x_3 + 400x_4 + 2x_5 + 1.8x_6 + 2.1x_7\]

### Constraints:
1. Land constraint: \[x_1 + x_2 + x_3 + 1.5x_4 \leq 100\]
2. Capital constraint: \[400x_4 + 3x_5 \leq 15000\]
3. Autumn and winter labor constraint: \[20x_1 + 35x_2 + 10x_3 + 100x_4 + 0.6x_5 + x_6 = 3500\]
4. Spring and summer labor constraint: \[50x_1 + 75x_2 + 40x_3 + 50x_4 + 0.3x_5 + x_7 = 4000\]
5. Cowshed constraint: \[x_4 \leq 32\]
6. Chicken coop constraint: \[x_5 \leq 3000\]

### Non-negativity constraints:
- \(x_1, x_2, x_3, x_4, x_5, x_6, x_7 \geq 0\)

### Integer constraints:
- \(x_4, x_5\) must be integers, as the number of cows and chickens cannot be fractional.

Using this model, we can apply linear programming or integer programming techniques to find the optimal areas for planting crops and raising animals, as well as the optimal number of hired laborers, to maximize net income while satisfying all constraints. This will provide the farm with an optimized operating plan.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the farm operating plan problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("FarmOperationPlan")

# Add decision variables
x1 = model.addVar(lb=0, name="x1")  # Area planted with soybeans (hectares)
x2 = model.addVar(lb=0, name="x2")  # Area planted with corn (hectares)
x3 = model.addVar(lb=0, name="x3")  # Area planted with wheat (hectares)
x4 = model.addVar(lb=0, vtype=COPT.INTEGER, name="x4")  # Number of cows raised
x5 = model.addVar(lb=0, vtype=COPT.INTEGER, name="x5")  # Number of chickens raised
x6 = model.addVar(lb=0, name="x6")  # Additional labor force hired in spring and summer (person-days)
x7 = model.addVar(lb=0, name="x7")  # Additional labor force hired in autumn and winter (person-days)

# Set the objective function
model.setObjective(175*x1 + 300*x2 + 120*x3 + 400*x4 + 2*x5 + 1.8*x6 + 2.1*x7, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(x1 + x2 + x3 + 1.5*x4 <= 100, name="LandConstraint")  # Land constraint
model.addConstr(400*x4 + 3*x5 <= 15000, name="CapitalConstraint")  # Capital constraint
model.addConstr(20*x1 + 35*x2 + 10*x3 + 100*x4 + 0.6*x5 + x6 == 3500, name="LaborConstraintAutumnWinter")  # Autumn and winter labor constraint
model.addConstr(50*x1 + 75*x2 + 40*x3 + 50*x4 + 0.3*x5 + x7 == 4000, name="LaborConstraintSpringSummer")  # Spring and summer labor constraint
model.addConstr(x4 <= 32, name="CowshedConstraint")  # Cowshed constraint
model.addConstr(x5 <= 3000, name="ChickenCoopConstraint")  # Chicken coop constraint

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized net income: {:.2f} yuan".format(model.objval))
    print("Operating plan:")
    print("Area planted with soybeans: {:.2f} hectares".format(x1.x))
    print("Area planted with corn: {:.2f} hectares".format(x2.x))
    print("Area planted with wheat: {:.2f} hectares".format(x3.x))
    print("Number of cows raised: {:.0f}".format(x4.x))
    print("Number of chickens raised: {:.0f}".format(x5.x))
    print("Additional labor force hired in spring and summer: {:.2f} person-days".format(x6.x))
    print("Additional labor force hired in autumn and winter: {:.2f} person-days".format(x7.x))
else:
    print("No optimal solution found.")
```

This script first creates a COPT environment and model, then adds decision variables and the objective function. Next, it adds constraints on land, capital, labor, and animal farming facilities. Finally, it solves the model and outputs the optimal solution (if it exists).

The output will include the maximized net income and the optimal areas for planting crops and raising animals, as well as the optimal number of hired laborers. This provides the farm with an optimized operating plan.

---

## Case 8

**Ground truth:** 4700  |  **3B answer:** -280.0 (Optimal)  |  **8B answer:** 4700.0

### Question
A wood storage and transportation company has a large warehouse for storing and selling wood. Due to the fluctuation in wood prices each quarter, the company purchases wood at the beginning of each quarter, sells a portion within the same quarter, and stores the remaining amount for future sales. It is known that the maximum wood storage capacity of the company's warehouse is 200,000 $\mathrm{m}^3$, and the storage cost is $(a+b u)$ yuan per $\mathrm{m}^3$, where $a=70$, $b=100$, and $u$ is the storage time in quarters. The buying and selling prices for each quarter and the projected maximum sales volume are shown in Table 1-18.
Table 1-18
\begin{tabular}{c|c|c|c}
\hline Quarter & Buying Price (10,000 yuan/$10,000 \mathrm{m}^2$) & Selling Price (10,000 yuan/$10,000 \mathrm{m}^2$) & Projected Maximum Sales Volume ($10,000 \mathrm{m}^3$) \\
\hline Winter & 410 & 425 & 100 \\
Spring & 430 & 440 & 140 \\
Summer & 460 & 465 & 200 \\
Autumn & 450 & 455 & 160 \\
\hline
\end{tabular}

Due to the unsuitability of long-term wood storage, all inventory wood should be sold by the end of each autumn. Establish a linear programming model for this problem to maximize the company's annual profit.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Define the decision variables
u_winter = LpVariable('u_winter', lowBound=0)
u_spring = LpVariable('u_spring', lowBound=0)
u_summer = LpVariable('u_summer', lowBound=0)
u_autumn = LpVariable('u_autumn', lowBound=0)

# Define the objective function
prob = LpProblem("Wood_Profit_Maximization", LpMaximize)
prob += lpSum([41 * u_winter + 43 * u_spring + 46 * u_summer + 45 * u_autumn - 
               (70 + 100 * u_winter) - (70 + 100 * u_spring) - (70 + 100 * u_summer) -
               (70 + 100 * u_autumn)])

# Define the constraints
prob += lpSum([u_winter, u_spring, u_summer, u_autumn]) <= 200

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Profit: {prob.objective.value()}")
```

This code sets up a linear programming model to maximize the company's annual profit based on the given conditions. The decision variables represent the storage time for each quarter, and the objective function calculates the total profit by subtracting the buying and selling prices from the storage cost. The constraint ensures that the total storage does not exceed the warehouse capacity of 200,000 $\mathrm{m}^3$.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the optimization problem for the wood storage and transportation company, we will establish a linear programming model to maximize the company's annual profit while considering the buying and selling prices, storage costs, and storage capacity constraints. Here is the detailed formulation of the model:

### Decision Variables:
- \(x_i\): The amount of wood purchased in the \(i\)th quarter (in 10,000 $\mathrm{m}^3$).
- \(y_i\): The amount of wood sold in the \(i\)th quarter (in 10,000 $\mathrm{m}^3$).
- \(s_i\): The amount of wood stored at the end of the \(i\)th quarter (in 10,000 $\mathrm{m}^3$).

### Objective Function:
- Maximize the annual profit: \[Z = \sum_{i=1}^{4} (Selling Price_i \cdot y_i - Buying Price_i \cdot x_i) - Storage Cost \cdot \sum_{i=1}^{4} s_i\]
  - where the storage cost is \(70 + 100 \cdot u_i\), and \(u_i\) is the storage time in quarters.

### Constraints:
1. The storage amount at the end of each quarter does not exceed the maximum storage capacity:
   - \(s_1 = x_1 - y_1 \leq 20\)
   - \(s_2 = s_1 + x_2 - y_2 \leq 20\)
   - \(s_3 = s_2 + x_3 - y_3 \leq 20\)
   - \(s_4 = s_3 + x_4 - y_4 = 0\)
2. The sales amount does not exceed the projected maximum sales volume:
   - \(y_1 \leq 10\)
   - \(y_2 \leq 14\)
   - \(y_3 \leq 20\)
   - \(y_4 \leq 16\)
3. Non-negativity constraints:
   - \(x_i, y_i, s_i \geq 0\), for all \(i\).

### Integer Constraints:
- \(x_i, y_i, s_i\) must be integers, as the amount of wood is measured in 10,000 $\mathrm{m}^3$.

Using this model, we can apply linear programming techniques to find the optimal amounts of wood to purchase, sell, and store in each quarter, maximizing the company's annual profit while satisfying the storage capacity constraints and sales volume constraints. This will provide the company with an optimized wood purchasing, sales, and storage strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the optimization problem for the wood storage and transportation company:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("TimberStorageOptimization")

# Define parameters
seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
buying_prices = [410, 430, 460, 450]
selling_prices = [425, 440, 465, 455]
max_sales = [100, 140, 200, 160]
max_storage = 20
a = 70
b = 100

# Add decision variables
x = [model.addVar(vtype=COPT.INTEGER, name=f"x_{i}") for i in seasons]  # Purchase amount
y = [model.addVar(vtype=COPT.INTEGER, name=f"y_{i}") for i in seasons]  # Sales amount
s = [model.addVar(vtype=COPT.INTEGER, name=f"s_{i}") for i in seasons]  # Storage amount

# Objective function: Maximize annual profit
profit = cp.quicksum(selling_prices[i] * y[i] - buying_prices[i] * x[i] for i in range(4))
storage_cost = cp.quicksum((a + b * (i + 1)) * s[i] for i in range(4))
model.setObjective(profit - storage_cost, sense=COPT.MAXIMIZE)

# Constraints
# Storage amount at the end of each quarter does not exceed the maximum storage capacity
model.addConstr(s[0] == x[0] - y[0], name="Storage_1")
model.addConstr(s[0] <= max_storage, name="MaxStorage_1")
for i in range(1, 4):
    model.addConstr(s[i] == s[i-1] + x[i] - y[i], name=f"Storage_{i+1}")
    model.addConstr(s[i] <= max_storage, name=f"MaxStorage_{i+1}")
model.addConstr(s[3] == 0, name="FinalStorage")

# Sales amount does not exceed the projected maximum sales volume
for i in range(4):
    model.addConstr(y[i] <= max_sales[i], name=f"MaxSales_{seasons[i]}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized annual profit: {:.2f} 10,000 yuan".format(model.objval))
    for i in range(4):
        print(f"Purchase amount in {seasons[i]}: {x[i].x} 10,000 m^3")
        print(f"Sales amount in {seasons[i]}: {y[i].x} 10,000 m^3")
        print(f"Storage amount in {seasons[i]}: {s[i].x} 10,000 m^3")
else:
    print("No optimal solution found.")
```

This script first defines the parameters of the problem, including the seasons, buying and selling prices, maximum sales volume, and storage capacity. Then, it creates decision variables to represent the purchase amount, sales amount, and storage amount for each quarter.

Next, the script sets the objective function, which is to maximize the annual profit, taking into account the sales revenue, purchase cost, and storage cost. The constraints include the storage amount at the end of each quarter not exceeding the maximum storage capacity and the sales amount not exceeding the projected maximum sales volume.

Finally, the script solves the model and outputs the optimal solution (if exists). The output includes the maximized annual profit and the purchase amount, sales amount, and storage amount for each quarter.

This script provides a complete example of using the `coptpy` library to solve the optimization problem for the wood storage and transportation company, considering all the constraints and objectives mentioned in the problem description.

---

## Case 9

**Ground truth:** 37000  |  **3B answer:** None (?)  |  **8B answer:** 37000.0

### Question
A product can be processed on any one of the four devices A, B, C, or D. The setup completion cost for each device when it is activated, the unit cost of production for the product, and the maximum processing capacity for each device are known as shown in Table 5-7. How can the total cost be minimized to produce 2000 units of the product? Try to establish a mathematical model.
Table 5-7
\begin{tabular}{c|c|c|c}
\hline Device & Setup Completion Cost (in yuan) & Production Cost (in yuan per unit) & Maximum Processing Capacity (units) \\\hline A & 1000 & 20 & 900 \
B & 920 & 24 & 1000 \
C & 800 & 16 & 1200 \
D & 700 & 28 & 1600 \
\hline
\end{tabular}

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum, minimize

# Define the problem
prob = LpProblem("MinimizeProductionCost", LpMinimize)

# Define decision variables (binary variables indicating whether a device is used or not)
device_A_used = LpVariable('A', 0, 1, LpInteger)
device_B_used = LpVariable('B', 0, 1, LpInteger)
device_C_used = LpVariable('C', 0, 1, LpInteger)
device_D_used = LpVariable('D', 0, 1, LpInteger)

# Objective function: minimize total cost
total_cost = 1000*device_A_used + 920*device_B_used + 800*device_C_used + 700*device_D_used + \
             20*LpVariable('A_prod', lowBound=0) * device_A_used + 24*LpVariable('B_prod', lowBound=0) * device_B_used + \
             16*LpVariable('C_prod', lowBound=0) * device_C_used + 28*LpVariable('D_prod', lowBound=0) * device_D_used
prob += total_cost

# Constraints: production capacity and units to be produced
capacity_constraints = [
    LpVariable('A_capacity', lowBound=0, upBound=900*device_A_used),
    LpVariable('B_capacity', lowBound=0, upBound=1000*device_B_used),
    LpVariable('C_capacity', lowBound=0, upBound=1200*device_C_used),
    LpVariable('D_capacity', lowBound=0, upBound=1600*device_D_used)
]

prob += lpSum(capacity_constraints) >= 2000

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Cost: {value(prob.objective)}")
```

This code sets up a linear programming model to minimize the total cost of producing 2000 units of the product using devices A, B, C, and D. The binary variables indicate whether each device is used or not, and additional variables represent production from each device. Constraints ensure that the total capacity does not exceed the maximum processing capacities for any given device when it is activated.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the problem of minimizing the total cost of producing the product, we need to construct a mixed integer programming model to determine which devices should be activated and how to allocate the production tasks to minimize the total cost. Here is the model formulation:

### Decision Variables:
- \(x_j\): The quantity of the product produced on device \(j\), where \(j \in \{A, B, C, D\}\).
- \(y_j\): A binary variable indicating whether device \(j\) is activated, where \(y_j = 1\) if device \(j\) is activated, and \(y_j = 0\) otherwise.

### Objective Function:
- Minimize the total cost: \[Z = 1000y_A + 20x_A + 920y_B + 24x_B + 800y_C + 16x_C + 700y_D + 28x_D\]

### Constraints:
1. Total production quantity constraint: \[x_A + x_B + x_C + x_D = 2000\]
2. Maximum processing capacity constraints for each device:
   - \(x_A \leq 900y_A\)
   - \(x_B \leq 1000y_B\)
   - \(x_C \leq 1200y_C\)
   - \(x_D \leq 1600y_D\)
3. Binary constraints for device activation:
   - \(y_A, y_B, y_C, y_D \in \{0, 1\}\)

### Non-negativity constraints:
- \(x_j \geq 0\), for all \(j \in \{A, B, C, D\}\)

Using this model, we can apply mixed integer programming techniques to find the optimal production quantities for each device and the optimal device activation strategy to minimize the total cost. This will provide the company with an economically efficient production plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("ProductionOptimization")

# Device parameters
setup_costs = {'A': 1000, 'B': 920, 'C': 800, 'D': 700}
unit_costs = {'A': 20, 'B': 24, 'C': 16, 'D': 28}
capacities = {'A': 900, 'B': 1000, 'C': 1200, 'D': 1600}

# Add decision variables
x = {j: model.addVar(vtype=COPT.INTEGER, name=f"x_{j}") for j in setup_costs}
y = {j: model.addVar(vtype=COPT.BINARY, name=f"y_{j}") for j in setup_costs}

# Objective function: Minimize total cost
model.setObjective(cp.quicksum(setup_costs[j] * y[j] + unit_costs[j] * x[j] for j in setup_costs), sense=COPT.MINIMIZE)

# Constraints
# Total production quantity constraint
model.addConstr(cp.quicksum(x[j] for j in setup_costs) == 2000, name="TotalProduction")

# Maximum processing capacity constraints for each device
for j in setup_costs:
    model.addConstr(x[j] <= capacities[j] * y[j], name=f"Capacity_{j}")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} yuan".format(model.objval))
    for j in setup_costs:
        print(f"Quantity of the product produced on device {j}: {x[j].x} units")
        print(f"Is device {j} activated? {'Yes' if y[j].x > 0.5 else 'No'}")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we define the device parameters and add the decision variables. The objective function is to minimize the total cost, which includes the setup completion cost and the production cost. We add constraints for the total production quantity and the maximum processing capacity for each device. Finally, we solve the model and output the results of the optimal solution, including the minimum total cost and the quantity of the product produced on each device.

This script provides a complete example of using the `coptpy` library to solve the problem of minimizing the total cost of producing the product, while satisfying all the constraints mentioned in the problem.

---

## Case 10

**Ground truth:** 12  |  **3B answer:** None (?)  |  **8B answer:** 12.0

### Question
There are three different products that need to be processed on three machine tools. Each product must be processed first on machine 1, then sequentially on machine 2 and 3. The order of processing the three products should remain the same on each machine. Assume \( t_{ij} \) represents the time it takes to process the \( i \)th product on the \( j \)th machine.\n\n**Given:**\n\n- \( t_{11} = 5 \) minutes, \( t_{12} = 4 \) minutes, \( t_{13} = 3 \) minutes\n- \( t_{21} = 6 \) minutes, \( t_{22} = 5 \) minutes, \( t_{23} = 4 \) minutes\n- \( t_{31} = 7 \) minutes, \( t_{32} = 6 \) minutes, \( t_{33} = 5 \) minutes

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum, minimize, Problem

# Define the problem
prob = LpProblem("Processing_Order", LpMinimize)

# Define decision variables
x12 = LpVariable('x12', lowBound=0, cat='Continuous')
x13 = LpVariable('x13', lowBound=0, cat='Continuous')
x21 = LpVariable('x21', lowBound=0, cat='Continuous')
x22 = LpVariable('x22', lowBound=0, cat='Continuous')
x23 = LpVariable('x23', lowBound=0, cat='Continuous')
x31 = LpVariable('x31', lowBound=0, cat='Continuous')
x32 = LpVariable('x32', lowBound=0, cat='Continuous')

# Objective function: minimize total processing time
prob += lpSum([t1 * x1j + t2 * x2j + t3 * x3j for t1, t2, t3, x1j, x2j, x3j in [(5, 6, 7, x12, x21, x31), (4, 5, 6, x13, x22, x32), (3, 4, 5, x21, x22, x23)]])

# Constraints: flow shop order
prob += x12 <= x13
prob += x21 <= x22
prob += x22 <= x23

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total processing time: {value(prob.objective)} minutes")
```

In this code, I've defined decision variables for each product's sequence on each machine. The objective is to minimize the total processing time by assigning products to machines in a flow shop order manner. Constraints ensure that the sequence of products remains consistent across all machines. Please note that `t1`, `t2`, and `t3` are not directly used as they represent the times for different products on each machine, which should be defined elsewhere or passed appropriately if this is part of a larger model.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
### Decision Variables:
- \( x_{ij} \): Binary variable indicating whether the \( i \)th product is processed on the \( j \)th machine (1 if true, 0 if false).

### Constraints:
1. **Processing Order Constraint**:
   - \( x_{ij} \leq x_{i, j+1} \quad \forall i \in \{1, 2, 3\}, \quad j \in \{1, 2\} \)
   - Ensures that each product is processed in order on the machine tools.

2. **Processing Completeness Constraint**:
   - \( \sum_{j=1}^{3} x_{ij} = 1 \quad \forall i \in \{1, 2, 3\} \)
   - Ensures that each product is processed on one machine.

### Objective:
- **Minimize Total Processing Time**:
  - $$ \min Z = \sum_{i=1}^{3} \sum_{j=1}^{3} t_{ij} x_{ij} $$
  - Minimizes the total processing time of all products on all machine tools.

## Python Code Solution Using `coptpy`:
Of course, here is the COPT code generated based on the above mathematical model and problem background
```python
from coptpy import *

# Create environment and model
env = Envr()
model = env.createModel("JobScheduling")

# Processing time data
processing_times = {
    (1, 1): 5, (1, 2): 4, (1, 3): 3,
    (2, 1): 6, (2, 2): 5, (2, 3): 4,
    (3, 1): 7, (3, 2): 6, (3, 3): 5
}

# Decision variables
x = model.addVars([(i, j) for i in range(1, 4) for j in range(1, 4)], vtype=COPT.BINARY, nameprefix = "x")

# Constraints
# Processing order constraint
for i in range(1, 4):
    for j in range(1, 3):
        model.addConstr(x[i, j] <= x[i, j + 1])

# Processing completeness constraint
for i in range(1, 4):
    model.addConstr(sum(x[i, j] for j in range(1, 4)) == 1)

# Objective function
model.setObjective(sum(processing_times[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 4)), sense=COPT.MINIMIZE)

# Solve the model
model.solve()

# Output the results
if model.Status == COPT.OPTIMAL:
    print("Optimal solution found with total processing time:", model.objval)
    for i in range(1, 4):
        for j in range(1, 4):
            if x[i, j].x > 0.5:
                print(f"Product {i} is processed on Machine {j}")
```

This script uses the COPTPY library to define and solve the job scheduling problem, ensuring that each product is processed in order on the machine tools and minimizing the total processing time.

---

## Case 11

**Ground truth:** 4  |  **3B answer:** 0.0 (Optimal)  |  **8B answer:** 4.0

### Question
A master's student majoring in Operations Research at a certain university is required to take two math courses, two operations research courses, and two computer courses out of a total of seven courses: calculus, operations research, data structures, management statistics, computer simulation, computer programming, and forecasting. Some courses belong to only one category: calculus belongs to the math category, and computer programming belongs to the computer category. However, some courses are cross-categories: operations research belongs to both the operations research and math categories, data structures belong to both the computer and math categories, management statistics belongs to both the math and operations research categories, computer simulation belongs to both the computer and operations research categories, and forecasting belongs to both the operations research and math categories. For courses that belong to two categories, taking the course can be considered as taking one course in each category. In addition, some courses require prerequisite courses: computer simulation or data structures must be taken after taking computer programming, management statistics must be taken after taking calculus, and forecasting must be taken after taking management statistics. The question is: how many and which courses should a master's student take at minimum to meet the above requirements?

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Define the problem
prob = LpProblem("Master_Science_Courses_Selection", LpMinimize)

# Define decision variables
courses = ['calculus', 'operations_research', 'data_structures', 
           'management_statistics', 'computer_simulation', 
           'computer_programming', 'forecasting']
variables = {course: LpVariable(course, lowBound=0) for course in courses}

# Constraints
# Courses that belong to only one category
prob += variables['calculus'] <= 1
prob += variables['operations_research'] <= 1
prob += variables['data_structures'] <= 1
prob += variables['management_statistics'] <= 1
prob += variables['computer_simulation'] <= 1
prob += variables['computer_programming'] <= 1
prob += variables['forecasting'] <= 1

# Courses that belong to two categories and must be taken in both categories
prob += variables['operations_research'] + variables['management_statistics'] - 2*variables['data_structures'] >= 0
prob += variables['computer_simulation'] + variables['forecasting'] - 2*variables['computer_programming'] >= 0

# Prerequisite constraints
prob += variables['computer_simulation'] + variables['data_structures'] <= variables['computer_programming']
prob += variables['management_statistics'] <= variables['calculus']
prob += variables['forecasting'] <= variables['management_statistics']

# Objective: Minimize the number of courses taken
prob += lpSum(variables.values()) 

# Solve the problem
status = prob.solve()

# Print the solution
for course, var in variables.items():
    if var.varValue > 0:
        print(f"{course}: {var.varValue}")

print("Total minimum courses to be taken:", len([var for var in variables.values() if var.value() > 0]))
```

This code sets up a linear programming problem where the objective is to minimize the number of courses taken while satisfying all given constraints. The solution will indicate which courses should be taken and how many are needed.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the course selection problem for the master's student, we need to construct a mathematical model to minimize the number of courses taken while satisfying the course category requirements and prerequisite course requirements. The model can be formulated as follows:

### Decision Variables:
- \(x_i\): Whether to take course \(i\), where \(i\) represents the courses (calculus, operations research, data structures, management statistics, computer simulation, computer programming, forecasting). If course \(i\) is taken, \(x_i = 1\); otherwise, \(x_i = 0\).

### Objective Function:
- Minimize the number of courses taken: \[Z = \sum_{i \in \{calculus, operations research, data structures, management statistics, computer simulation, computer programming, forecasting\}} x_i\]
  - This function calculates the total number of courses taken based on whether each course is taken.

### Constraints:
1. Math course requirements: \[x_{calculus} + x_{operations research} + x_{data structures} + x_{management statistics} + x_{forecasting} \geq 2\]
   - This ensures that the student takes at least two math courses.
2. Operations research course requirements: \[x_{operations research} + x_{management statistics} + x_{computer simulation} + x_{forecasting} \geq 2\]
   - This ensures that the student takes at least two operations research courses.
3. Computer course requirements: \[x_{data structures} + x_{computer simulation} + x_{computer programming} \geq 2\]
   - This ensures that the student takes at least two computer courses.
4. Prerequisite course requirements:
   - \(x_{computer simulation} \leq x_{computer programming}\)
   - \(x_{management statistics} \leq x_{calculus}\)
   - \(x_{forecasting} \leq x_{management statistics}\)

### Binary Constraints:
- \(x_i \in \{0, 1\}\), for all \(i\), ensuring that the decision variables can only take the values 0 or 1, representing whether a course is taken.

Using this model, we can apply integer linear programming techniques to find the optimal course selection that satisfies the course category requirements and prerequisite course requirements while minimizing the number of courses taken. This will provide the master's student with an optimal course selection strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the course selection problem for the master's student:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("CourseSelectionOptimization")

# Define the list of courses
courses = ["calculus", "operations research", "data structures", "management statistics", "computer simulation", "computer programming", "forecasting"]

# Add decision variables
x = {course: model.addVar(vtype=COPT.BINARY, name=f"x_{course}") for course in courses}

# Objective function: minimize the number of courses taken
objective = cp.quicksum(x[course] for course in courses)
model.setObjective(objective, sense=COPT.MINIMIZE)

# Constraints
# Math course requirements
model.addConstr(x["calculus"] + x["operations research"] + x["data structures"] + x["management statistics"] + x["forecasting"] >= 2, name="MathCourses")

# Operations research course requirements
model.addConstr(x["operations research"] + x["management statistics"] + x["computer simulation"] + x["forecasting"] >= 2, name="ORCourses")

# Computer course requirements
model.addConstr(x["data structures"] + x["computer simulation"] + x["computer programming"] >= 2, name="CompCourses")

# Prerequisite course requirements
model.addConstr(x["computer simulation"] <= x["computer programming"], name="CompSimPrereq")
model.addConstr(x["management statistics"] <= x["calculus"], name="StatsPrereq")
model.addConstr(x["forecasting"] <= x["management statistics"], name="ForecastPrereq")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum number of courses taken:", model.objval)
    print("Selected courses:")
    for course in courses:
        if x[course].x == 1:
            print(course)
else:
    print("No optimal solution found.")
```

This script first creates a COPT environment and model. Then, it defines a list of courses and adds a binary decision variable for each course, representing whether the course is taken.

Next, the script sets the objective function, which is to minimize the number of courses taken.

Then, the script adds the constraints, including the math course requirements, operations research course requirements, computer course requirements, and prerequisite course requirements.

Finally, the script solves the model and outputs the minimum number of courses taken and the selected courses (if an optimal solution is found).

This script provides a complete example of using the `coptpy` library to solve the course selection problem for a master's student, considering all the course category requirements and prerequisite course requirements.

---

## Case 12

**Ground truth:** 43700  |  **3B answer:** None (?)  |  **8B answer:** 43300.0

### Question
Red Star Plastic Factory produces 6 types of plastic containers, with their capacities, demands, and variable costs shown in Table 5-11.
Table 5-11
\begin{tabular}{c|c|c|c|c|c|c}
\hline Container Code & 1 & 2 & 3 & 4 & 5 & 6 \
\hline Capacity $(\mathrm{cm}^3)$ & 1500 & 2500 & 4000 & 6000 & 9000 & 12000 \
Demand/units & 500 & 550 & 700 & 900 & 400 & 300 \
Variable Cost/(¥/unit) & 5 & 8 & 10 & 12 & 16 & 18 \
\hline
\end{tabular}

Each type of container is produced using different dedicated equipment, with a fixed cost of ¥1200. When the quantity of a certain container cannot meet the demand, containers with larger capacities can be used as substitutes. How should production be organized to minimize the total cost while meeting the demand?

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Define the problem
prob = LpProblem("Plastic_Factory_Operations", LpMinimize)

# Define decision variables
x1, x2, x3, x4, x5, x6 = [LpVariable(f"x{i}", lowBound=0) for i in range(1, 7)]

# Objective function: Minimize total cost (variable + fixed)
prob += lpSum([5*x1 + 8*x2 + 10*x3 + 12*x4 + 16*x5 + 18*x6 + 1200*(x1+x2+x3+x4+x5+x6)])

# Constraints: Meet demand for each container
prob += x1 >= 500, "Demand_Container_1"
prob += x2 >= 550, "Demand_Container_2"
prob += x3 >= 700, "Demand_Container_3"
prob += x4 >= 900, "Demand_Container_4"
prob += x5 >= 400, "Demand_Container_5"
prob += x6 >= 300, "Demand_Container_6"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")
print(f"Total Cost: {value(prob.objective))}")
```

Note: The `value()` function is used to get the value of the objective function after solving. Please replace `value` with the correct method if `PuLP` does not have a direct `value` method for retrieving variable values or problem objectives.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the production problem for the Red Star Plastic Factory, we need to construct a mathematical model to minimize the total cost while meeting the demand for each type of container. The model can be formulated as follows:

### Decision Variables:
- \(x_i\): The quantity of container \(i\) produced, where \(i\) represents the container type (1, 2, 3, 4, 5, 6).

### Objective Function:
- Minimize the total cost: \[Z = \sum_{i=1}^{6} (variable\_cost_i \times x_i) + \sum_{i=1}^{6} (fixed\_cost \times y_i)\]
  - This function calculates the total cost based on the quantity of each container produced and their respective variable costs and fixed costs.

### Constraints:
1. Meet the demand for each type of container: \[x_i \geq demand_i, \forall i\]
   - This ensures that the quantity of each container produced meets or exceeds the demand.
2. If the quantity of a certain container cannot meet the demand, containers with larger capacities can be used as substitutes: \[x_i \geq x_{i+1}, \forall i \in \{1, 2, 3, 4, 5\}\]
   - This allows containers with larger capacities to be used as substitutes if the quantity of a certain container cannot meet the demand.

### Non-negativity and Integer Constraints:
- \(x_i, y_i \geq 0\) and must be integers, as the quantity of containers must be integers.

Using this model, we can apply integer linear programming techniques to find the optimal quantities of each type of container to produce, minimizing the total cost while meeting the demand for each type of container. This will provide the Red Star Plastic Factory with an economically efficient production strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the production problem for the Red Star Plastic Factory:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("PlasticContainerProduction")

# Container types
container_types = range(1, 7)

# Container capacities (cm^3)
capacity = {1: 1500, 2: 2500, 3: 4000, 4: 6000, 5: 9000, 6: 12000}

# Container demands (units)
demand = {1: 500, 2: 550, 3: 700, 4: 900, 5: 400, 6: 300}

# Variable costs (¥/unit)
variable_cost = {1: 5, 2: 8, 3: 10, 4: 12, 5: 16, 6: 18}

# Fixed cost (¥)
fixed_cost = 1200

# Add decision variables
x = {i: model.addVar(vtype=COPT.INTEGER, name=f"x_{i}") for i in container_types}
y = {i: model.addVar(vtype=COPT.BINARY, name=f"y_{i}") for i in container_types}

# Objective function: Minimize total cost
objective = cp.quicksum(variable_cost[i] * x[i] for i in container_types) + cp.quicksum(fixed_cost * y[i] for i in container_types)
model.setObjective(objective, sense=COPT.MINIMIZE)

# Constraints
# Meet the demand for each type of container
for i in container_types:
    model.addConstr(x[i] >= demand[i], name=f"Demand_{i}")

# If the quantity of a certain container cannot meet the demand, containers with larger capacities can be used as substitutes
for i in range(1, 6):
    model.addConstr(x[i] >= x[i+1], name=f"Substitution_{i}")

# If the demand for a certain container cannot be met, produce the next larger capacity container
for i in range(1, 6):
    model.addConstr(x[i] + y[i] * 10000 >= demand[i], name=f"Production_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum total cost: {:.2f} ¥".format(model.objval))
    for i in container_types:
        print(f"Quantity of container {i} produced: {x[i].x} units")
else:
    print("No optimal solution found.")
```

In this script, we first define the container types, capacities, demands, variable costs, and fixed costs. Then, it creates two decision variables: `x[i]` represents the quantity of container `i` produced, and `y[i]` is a binary variable indicating whether container `i` is produced.

The objective function is to minimize the total cost, including the variable costs and fixed costs. The constraints ensure that the quantity of each container produced meets or exceeds the demand and allows containers with larger capacities to be used as substitutes if the quantity of a certain container cannot meet the demand.

Finally, the script solves the model and outputs the minimum total cost and the quantity of each container produced. This script provides the Red Star Plastic Factory with an economically efficient production strategy.

---

## Case 13

**Ground truth:** 135.27  |  **3B answer:** 125.4 (Optimal)  |  **8B answer:** 135.26666666666668

### Question
A factory plans to produce three types of products, I, II, and III, which require processing on devices A, B, and C, respectively. The data is shown in Table 2-3.
Table 2-3
\begin{tabular}{|c|c|c|c|c|}
\hline Device Code & I & II & III & Monthly Device Capacity \\
\hline A & 8 & 2 & 10 & 300 \\
\hline B & 10 & 5 & 8 & 400 \\
\hline C & 2 & 13 & 10 & 420 \\
\hline Unit Product Profit (in thousands) & 3 & 2 & 2.9 & \\
\hline
\end{tabular}
How can the factory fully utilize the capacity of the devices to maximize profit?

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Product_Profit_Maximization", LpMaximize)

# Define decision variables
x1 = LpVariable('Prod_I', lowBound=0, cat='Continuous')
x2 = LpVariable('Prod_II', lowBound=0, cat='Continuous')
x3 = LpVariable('Prod_III', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
prob += 3 * x1 + 2 * x2 + 2.9 * x3

# Constraints for each device capacity
prob += 8 * x1 + 10 * x2 + 2 * x3 <= 300, "Device_A"
prob += 2 * x1 + 5 * x2 + 13 * x3 <= 400, "Device_B"
prob += 10 * x1 + 8 * x2 + 10 * x3 <= 420, "Device_C"

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: {LpProblem.value(prob)}")
```

This code sets up a linear programming model to maximize profit for products I, II, and III given the constraints of device capacities A, B, and C. The `PuLP` library is used to define the problem, variables, objective function, and constraints. After solving, it prints out the optimal production quantities for each product and the maximum total profit.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the factory's production planning problem, we need to construct a linear programming model to maximize profit while ensuring that the capacity of each device is fully utilized. Here is the model formulation:

### Decision Variables:
- \(x_1\): Number of units of product I produced.
- \(x_2\): Number of units of product II produced.
- \(x_3\): Number of units of product III produced.

### Objective Function:
- Maximize total profit: \(Z = 3x_1 + 2x_2 + 2.9x_3\)
  - This function calculates the total profit based on the unit product profit and the number of units produced for each product.

### Constraints:
1. Device A capacity constraint: \(8x_1 + 2x_2 + 10x_3 \leq 300\)
2. Device B capacity constraint: \(10x_1 + 5x_2 + 8x_3 \leq 400\)
3. Device C capacity constraint: \(2x_1 + 13x_2 + 10x_3 \leq 420\)

### Non-negativity Constraints:
- \(x_1, x_2, x_3 \geq 0\), ensuring that the number of units produced is non-negative.

Using this model, we can apply linear programming techniques to find the optimal number of units to produce for each product, maximizing total profit while ensuring that the capacity of each device is fully utilized. This will provide the factory with an economically efficient production plan.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the factory production planning problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("FactoryProductionPlan")

# Add decision variables
x1 = model.addVar(lb=0, name="x1")  # Number of units of product I produced
x2 = model.addVar(lb=0, name="x2")  # Number of units of product II produced
x3 = model.addVar(lb=0, name="x3")  # Number of units of product III produced

# Set the objective function: Maximize total profit
model.setObjective(3*x1 + 2*x2 + 2.9*x3, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(8*x1 + 2*x2 + 10*x3 <= 300, name="CapacityA")  # Device A capacity constraint
model.addConstr(10*x1 + 5*x2 + 8*x3 <= 400, name="CapacityB")  # Device B capacity constraint
model.addConstr(2*x1 + 13*x2 + 10*x3 <= 420, name="CapacityC")  # Device C capacity constraint

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: {:.2f} thousand yuan".format(model.objval))
    print("Number of units of product I produced: {:.2f}".format(x1.x))
    print("Number of units of product II produced: {:.2f}".format(x2.x))
    print("Number of units of product III produced: {:.2f}".format(x3.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add three decision variables `x1`, `x2`, and `x3`, representing the number of units produced for products I, II, and III, respectively.

Next, we set the objective function, which is to maximize total profit. The coefficients in the objective function correspond to the unit product profit.

Then, we add three constraints, each representing the capacity constraint of a device. The coefficients in the constraints correspond to the processing time required for each product on each device.

Finally, we solve the model and output the results. If an optimal solution is found, we print the maximized total profit and the number of units produced for each product. If no optimal solution is found, we output the corresponding message.

This script provides a complete example of using the `coptpy` library to solve the factory production planning problem, helping the factory maximize profit while ensuring that the capacity of each device is fully utilized.

---

## Case 14

**Ground truth:** 150  |  **3B answer:** 1730.0 (Optimal)  |  **8B answer:** 150.0

### Question
The number of drivers and crew members required for each time period of a certain day and night service bus route is shown in Table 1-17.
Table 1-17
\begin{tabular}{c|c|c}
\hline Shift & Time & Number Required \\
\hline 1 & $6: 00 \sim 10: 00$ & 60 \\
\hline 2 & $10: 00 \sim 14: 00$ & 70 \\
\hline 3 & $14: 00 \sim 18: 00$ & 60 \\
\hline 4 & $22: 00 \sim 22: 00$ & 50 \\
\hline 5 & $22: 00 \sim 2: 00$ & 20 \\
\hline 6 & $2: 00 \sim 6: 00$ & 30 \\
\hline
\end{tabular}

Assuming the drivers and crew members start working at the beginning of each time period and work continuously for eight hours, how many drivers and crew members should be equipped for this bus route at least? Provide the linear programming model for this problem.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum

# Create a LP Problem
prob = LpProblem("BusRouteStaffing", LpMinimize)

# Define decision variables
drivers = {}
crew_members = {}

for shift in range(1, 7):
    drivers[shift] = LpVariable(f'drivers_{shift}', lowBound=0, cat='Continuous')
    crew_members[shift] = LpVariable(f'crew_members_{shift}', lowBound=0, cat='Continuous')

# Define the objective function (minimize total number of staff)
prob += lpSum([drivers[shift] + crew_members[shift] for shift in range(1, 7)])

# Define constraints based on required numbers
constraints = [
    drivers[1] - lpSum([drivers[shift] for shift in range(2, 6)]) == 60,
    drivers[2] - lpSum([drivers[shift] for shift in [3, 4]]) == 70,
    drivers[3] - lpSum([drivers[shift] for shift in [4, 5]]) == 60,
    drivers[4] - lpSum([crew_members[shift] for shift in [1, 2]]) == 50,
    crew_members[5] - lpSum([drivers[shift] for shift in [1, 2, 3]]) == 20,
    crew_members[6] - lpSum([drivers[shift] for shift in [4, 5]]) == 30
]

# Add constraints to the problem
for constraint in constraints:
    prob += constraint

# Solve the model
prob.solve()

# Print results
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total number of staff required =", value(prob.objective))
```

This code sets up and solves a linear programming problem to determine the minimum number of drivers and crew members needed for each time period. The objective is to minimize the total number of staff while satisfying the constraints based on the required numbers provided in Table 1-17.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the problem of driver and crew member requirements for the bus route, we need to construct a linear programming model to determine the minimum number of drivers and crew members required. Here is the model formulation:

### Decision Variables:
- \(x_j\): The number of drivers and crew members starting work at the beginning of the \(j\)th time period, where \(j = 1, 2, \ldots, 6\).

### Objective Function:
- Minimize the total number of drivers and crew members: \[Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6\]

### Constraints:
- Ensure that the number of drivers and crew members required for each time period is met:
  - \(x_6 + x_1 \geq 60\) (Shift 1)
  - \(x_1 + x_2 \geq 70\) (Shift 2)
  - \(x_2 + x_3 \geq 60\) (Shift 3)
  - \(x_3 + x_4 \geq 50\) (Shift 4)
  - \(x_4 + x_5 \geq 20\) (Shift 5)
  - \(x_5 + x_6 \geq 30\) (Shift 6)

### Non-negativity Constraints:
- \(x_j \geq 0\), for all \(j = 1, 2, \ldots, 6\).

Using this model, we can apply linear programming techniques to find the minimum number of drivers and crew members required to meet the requirements for each time period. This will provide the bus company with an economically efficient driver and crew member scheduling strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem of driver and crew member requirements for the bus route:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("BusCrewOptimization")

# Add decision variables
x = [model.addVar(lb=0, vtype=COPT.INTEGER, name=f"x_{j+1}") for j in range(6)]

# Objective function: Minimize the total number of drivers and crew members
model.setObjective(cp.quicksum(x), sense=COPT.MINIMIZE)

# Constraints: Ensure that the number of drivers and crew members required for each time period is met
model.addConstr(x[5] + x[0] >= 60, name="Shift_1")
model.addConstr(x[0] + x[1] >= 70, name="Shift_2")
model.addConstr(x[1] + x[2] >= 60, name="Shift_3")
model.addConstr(x[2] + x[3] >= 50, name="Shift_4")
model.addConstr(x[3] + x[4] >= 20, name="Shift_5")
model.addConstr(x[4] + x[5] >= 30, name="Shift_6")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Minimum number of drivers and crew members required:", model.objval)
    for j in range(6):
        print(f"Number of drivers and crew members starting work at the beginning of Shift {j+1}: {x[j].x}")
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add six decision variables `x[j]`, representing the number of drivers and crew members starting work at the beginning of each time period.

Next, we define the objective function, which is to minimize the total number of drivers and crew members.

Then, we add six constraints to ensure that the number of drivers and crew members required for each time period is met.

Finally, we solve the model and output the results. If an optimal solution is found, we print the minimum number of drivers and crew members required and the number of drivers and crew members starting work at the beginning of each time period. If no optimal solution is found, we output the corresponding message.

This script provides a complete example of using the `coptpy` library to solve the problem of driver and crew member requirements for a bus route, and demonstrates how to build and solve a linear programming model in Python.

---

## Case 15

**Ground truth:** 1030  |  **3B answer:** 1225.0 (Optimal)  |  **8B answer:** 1030.0

### Question
There are two coal mines, A and B, with monthly coal supplies of at least 80 tons and 100 tons, respectively. They are responsible for supplying coal to three residential areas, which require 55 tons, 75 tons, and 50 tons of coal per month, respectively. The distances between mine A and these three residential areas are 10 kilometers, 5 kilometers, and 6 kilometers. The distances between mine B and these three residential areas are 4 kilometers, 8 kilometers, and 15 kilometers. How should these two coal mines distribute the coal to the three residential areas to minimize the ton-kilometers of transportation?

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Create a problem
prob = LpProblem("Coal_Supply_Problem", LpMinimize)

# Decision variables: x11, x12, x13 for mine A to residential areas 1, 2, 3 respectively
x11 = LpVariable('x11', lowBound=0)
x12 = LpVariable('x12', lowBound=0)
x13 = LpVariable('x13', lowBound=0)

# Decision variables: x21, x22, x23 for mine B to residential areas 1, 2, 3 respectively
x21 = LpVariable('x21', lowBound=0)
x22 = LpVariable('x22', lowBound=0)
x23 = LpVariable('x23', lowBound=0)

# Constraints for coal supply from mines A and B
constraint_A_supply = lpSum([x11, x12, x13]) == 80
constraint_B_supply = lpSum([x21, x22, x23]) == 100

# Constraints for residential area demands
demand_constraint_1 = lpSum([x11, x21]) == 55
demand_constraint_2 = lpSum([x12, x22]) == 75
demand_constraint_3 = lpSum([x13, x23]) == 50

# Objective function: minimize ton-kilometers of transportation
objective_function = lpSum([(x11 + x21) * 10 + (x12 + x22) * 5 + (x13 + x23) * 6])

# Add the objective and constraints to the problem
prob += constraint_A_supply, "Supply_constraint_A"
prob += constraint_B_supply, "Supply_constraint_B"
prob += demand_constraint_1, "Demand_Constraint_1"
prob += demand_constraint_2, "Demand_Constraint_2"
prob += demand_constraint_3, "Demand_Constraint_3"
prob += objective_function, "Total_Ton_Kilometers"

# Solve the problem
prob.solve()

# Print the results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Total Ton-Kilometers: {value(prob.objective)}")
```

This code sets up a linear programming model to minimize the total ton-kilometers of transportation from two coal mines (A and B) to three residential areas, given their supply constraints and demand requirements. The distances between each mine and residential area are also considered in the objective function.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the problem of coal distribution from the two mines to the three residential areas, we need to construct a linear programming model to minimize the total ton-kilometers of transportation while satisfying the supply constraints of the mines and the demand of the residential areas. Here is the model:

### Decision Variables:
- \(x_{ij}\): The amount of coal transported from mine \(i\) to residential area \(j\), where \(i \in \{A, B\}\) represents the mine and \(j \in \{1, 2, 3\}\) represents the residential area.

### Objective Function:
- Minimize the total ton-kilometers of transportation: \[Z = 10x_{A1} + 5x_{A2} + 6x_{A3} + 4x_{B1} + 8x_{B2} + 15x_{B3}\]

### Constraints:
1. Supply constraints of the mines:
   - \(x_{A1} + x_{A2} + x_{A3} \geq 80\)
   - \(x_{B1} + x_{B2} + x_{B3} \geq 100\)
2. Demand constraints of the residential areas:
   - \(x_{A1} + x_{B1} = 55\)
   - \(x_{A2} + x_{B2} = 75\)
   - \(x_{A3} + x_{B3} = 50\)
3. Non-negativity constraints:
   - \(x_{ij} \geq 0\), for all \(i, j\).

Using this model, we can apply linear programming techniques to find the optimal distribution of coal from the two mines to the three residential areas, minimizing the total ton-kilometers of transportation while satisfying the supply constraints of the mines and the demand of the residential areas. This will provide an economically efficient coal distribution strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create the model
model = env.createModel("CoalDistribution")

# Add decision variables
x = model.addVars(['A', 'B'], [1, 2, 3], lb=0, nameprefix="x")

# Objective function: Minimize total ton-kilometers of transportation
model.setObjective(10*x['A', 1] + 5*x['A', 2] + 6*x['A', 3] + 4*x['B', 1] + 8*x['B', 2] + 15*x['B', 3], sense=COPT.MINIMIZE)

# Constraints
# Supply constraints of the mines
model.addConstr(x['A', 1] + x['A', 2] + x['A', 3] >= 80, name="SupplyA")
model.addConstr(x['B', 1] + x['B', 2] + x['B', 3] >= 100, name="SupplyB")

# Demand constraints of the residential areas
model.addConstr(x['A', 1] + x['B', 1] == 55, name="Demand1")
model.addConstr(x['A', 2] + x['B', 2] == 75, name="Demand2")
model.addConstr(x['A', 3] + x['B', 3] == 50, name="Demand3")

# Solve the model
model.solve()

# Output results
if model.status == COPT.OPTIMAL:
    print("Minimum total ton-kilometers of transportation: {:.2f}".format(model.objval))
    for i in ['A', 'B']:
        for j in [1, 2, 3]:
            print(f"Amount of coal transported from mine {i} to residential area {j}: {x[i, j].x:.2f} tons")
else:
    print("No optimal solution found.")
```

In this script, we first create a `COPT` environment and model. Then, we add decision variables `x` representing the amount of coal transported from each mine to each residential area. The objective function is to minimize the total ton-kilometers of transportation, calculated based on the distances and transportation amounts.

We add two sets of constraints: the supply constraints of the mines and the demand constraints of the residential areas. Finally, we solve the model and output the results of the optimal solution, including the minimum total ton-kilometers of transportation and the specific transportation amounts from each mine to each residential area.

This script provides a complete example of using the `coptpy` library to solve the problem of coal distribution from two mines to three residential areas, while satisfying all the constraints mentioned in the problem.

---

## Case 16

**Ground truth:** 57  |  **3B answer:** None (Optimal)  |  **8B answer:** 57.0

### Question
There are two products, A and B, which both require two chemical reaction processes: one before and one after. Each unit of product A requires 2 hours for the front process and 3 hours for the back process. Each unit of product B requires 3 hours for the front process and 4 hours for the back process. There are 16 hours available for the front process and 24 hours available for the back process.

For each unit of product B produced, two units of byproduct C are generated, which do not require any additional cost. Up to 5 units of byproduct C can be sold, while the remaining units must be disposed of, with a disposal cost of $2 per unit.

Selling one unit of product A yields a profit of $4, selling one unit of product B yields a profit of $10, and selling one unit of byproduct C yields a profit of $3.

To maximize the total profit obtained, establish the linear programming model for this problem.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Create the LP problem
prob = LpProblem("Chemical_Process_Profit_Maximization", LpMaximize)

# Define decision variables
x_A = LpVariable('ProductA_units', lowBound=0, cat='Continuous')
x_B = LpVariable('ProductB_units', lowBound=0, cat='Continuous')

# Front process constraint
front_process_constraint = 2 * x_A + 3 * x_B <= 16

# Back process constraint
back_process_constraint = 3 * x_A + 4 * x_B <= 24

# Byproduct C generation and disposal constraint
byproduct_C_generation = 2 * x_B >= 0
byproduct_C_disposal = LpVariable('ByproductC_units', lowBound=0, cat='Continuous')

# Objective function: maximize total profit
objective_function = 4 * x_A + 10 * x_B + 3 * byproduct_C_disposal

# Add constraints to the problem
prob += front_process_constraint
prob += back_process_constraint
prob += byproduct_C_generation
prob += byproduct_C_disposal >= 0

# Solve the LP problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit: ${value(prob.objective)}")
```

This code sets up and solves the linear programming model for the given operations research question using PuLP. The total profit is maximized by deciding how many units of products A, B, and the generated byproduct C to produce or dispose of.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve this production planning problem, we need to construct a linear programming model to maximize the total profit while satisfying the time constraints of the production processes and the sales and disposal limits of the byproduct. The model can be formulated as follows:

### Decision Variables:
- \(x_A\): Number of units of product A produced.
- \(x_B\): Number of units of product B produced.
- \(x_C\): Number of units of byproduct C sold.
- \(x_D\): Number of units of byproduct C disposed of.

### Objective Function:
- Maximize total profit: \[Z = 4x_A + 10x_B + 3x_C - 2x_D\]
  - This function calculates the total profit based on the profits of each product and byproduct.

### Constraints:
1. Time constraints for the front process: \[2x_A + 3x_B \leq 16\]
2. Time constraints for the back process: \[3x_A + 4x_B \leq 24\]
3. Sales limit for byproduct C: \[x_C \leq 5\]
4. Relationship between byproduct C and product B: \[2x_B = x_C + x_D\]
5. Non-negativity constraints: \[x_A, x_B, x_C, x_D \geq 0\]

### Integer Constraints:
- \(x_A, x_B, x_C, x_D\) must be integers, as the quantities of products and byproducts cannot be fractions.

Using this model, we can apply linear programming techniques to find the optimal quantities of each product and byproduct to produce and sell, maximizing the total profit while satisfying the time constraints of the production processes and the sales and disposal limits of the byproduct. This will provide the company with an optimized production and sales strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve this linear programming problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a COPT model
model = env.createModel("ProductionPlanning")

# Add decision variables
x_A = model.addVar(vtype=COPT.INTEGER, name="x_A")
x_B = model.addVar(vtype=COPT.INTEGER, name="x_B")
x_C = model.addVar(vtype=COPT.INTEGER, name="x_C")
x_D = model.addVar(vtype=COPT.INTEGER, name="x_D")

# Add constraints
model.addConstr(2*x_A + 3*x_B <= 16, name="FrontProcessTime")
model.addConstr(3*x_A + 4*x_B <= 24, name="BackProcessTime")
model.addConstr(x_C <= 5, name="ByproductCSalesLimit")
model.addConstr(2*x_B == x_C + x_D, name="ByproductCRelation")

# Set the objective function
model.setObjective(4*x_A + 10*x_B + 3*x_C - 2*x_D, sense=COPT.MAXIMIZE)

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: {}".format(model.objval))
    print("Number of units of product A produced: {}".format(x_A.x))
    print("Number of units of product B produced: {}".format(x_B.x))
    print("Number of units of byproduct C sold: {}".format(x_C.x))
    print("Number of units of byproduct C disposed of: {}".format(x_D.x))
else:
    print("No optimal solution found.")
```

This script first creates a COPT environment and model. Then, it defines four decision variables: `x_A`, `x_B`, `x_C`, and `x_D`, representing the number of units of product A produced, the number of units of product B produced, the number of units of byproduct C sold, and the number of units of byproduct C disposed of, respectively.

Next, the script adds four constraints:
1. Time constraints for the front process: `2*x_A + 3*x_B <= 16`
2. Time constraints for the back process: `3*x_A + 4*x_B <= 24`
3. Sales limit for byproduct C: `x_C <= 5`
4. Relationship between byproduct C and product B: `2*x_B == x_C + x_D`

Then, the script sets the objective function, which is to maximize the total profit: `4*x_A + 10*x_B + 3*x_C - 2*x_D`.

Finally, the script solves the model and outputs the results, including the maximized total profit and the optimal values of each decision variable.

By running this script, you can obtain the optimal solution for the production planning problem, maximizing the total profit while satisfying the time constraints of the production processes and the sales and disposal limits of the byproduct.

---

## Case 17

**Ground truth:** 623.0  |  **3B answer:** 0.0 (Unbounded)  |  **8B answer:** 623.0

### Question
Haus Toys can manufacture and sell toy trucks, toy planes, toy boats, and toy trains. The profit from selling one truck is $5, from one plane is $10, from one boat is $8, and from one train is $7. How many types of toys should Haus Toys manufacture to maximize profit?

There are 890 units of wood available. Manufacturing one truck requires 12 units of wood, one plane requires 20 units of wood, one boat requires 15 units of wood, and one train requires 10 units of wood.

There are 500 units of steel available. Manufacturing one plane requires 3 units of steel, one boat requires 5 units of steel, one train requires 4 units of steel, and one truck requires 6 units of steel.

If Haus Toys manufactures trucks, then they will not manufacture trains.

However, if they manufacture boats, they will also manufacture planes.

The number of toy boats manufactured cannot exceed the number of toy trains manufactured.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Toy_Manufacturing_Problem", LpMaximize)

# Define decision variables
x_truck = LpVariable('x_truck', lowBound=0)
x_plane = LpVariable('x_plane', lowBound=0)
x_boat = LpVariable('x_boat', lowBound=0)
x_train = LpVariable('x_train', lowBound=0)

# Objective function: Maximize profit
prob += x_truck * 5 + x_plane * 10 + x_boat * 8 + x_train * 7, "Total_Profit"

# Constraints
# Wood constraint
wood_constraint = 12*x_truck + 20*x_plane + 15*x_boat + 10*x_train <= 890

# Steel constraint
steel_constraint = 3*x_plane + 5*x_boat + 4*x_train + 6*x_truck <= 500

# Constraint: No trains if trucks are manufactured
no_trains_if_trucks = x_train <= 0

# Constraint: Planes and boats relationship
planes_and_boats_constraint = x_plane >= x_boat

# Constraint: Boats cannot exceed trains
boats_not_exceed_trains = x_boat <= x_train

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Profit = {prob.objective.value()}")
```

This code sets up and solves a linear programming problem to determine how many types of toys Haus Toys should manufacture to maximize profit, given the constraints on wood and steel usage.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the optimization problem for Haus Toys, we will establish a linear programming model focused on maximizing profit while satisfying the given constraints. The following is the formulation of the model:

### Decision Variables:
- \(x_T\): Number of toy trucks manufactured.
- \(x_P\): Number of toy planes manufactured.
- \(x_B\): Number of toy boats manufactured.
- \(x_R\): Number of toy trains manufactured.
- \(y_T\): Indicator variable for manufacturing toy trucks (1 = yes, 0 = no).
- \(y_P\): Indicator variable for manufacturing toy planes (1 = yes, 0 = no).
- \(y_B\): Indicator variable for manufacturing toy boats (1 = yes, 0 = no).
- \(y_R\): Indicator variable for manufacturing toy trains (1 = yes, 0 = no).

### Objective Function:
- Maximize total profit: \(Z = 5x_T + 10x_P + 8x_B + 7x_R\)

### Constraints:
1. Wood usage constraint: \(12x_T + 20x_P + 15x_B + 10x_R \leq 890\)
2. Steel usage constraint: \(6x_T + 3x_P + 5x_B + 4x_R \leq 500\)
3. If toy trucks are manufactured, toy trains cannot be manufactured: \(y_T + y_R \leq 1\)
4. If toy boats are manufactured, toy planes must be manufactured: \(y_B \leq y_P\)
5. The number of toy boats manufactured cannot exceed the number of toy trains manufactured: \(x_B \leq x_R\)
6. If toy trucks are manufactured, \(x_T\) must be greater than 0: \(x_T \geq y_T\)
7. If toy planes are manufactured, \(x_P\) must be greater than 0: \(x_P \geq y_P\)
8. If toy boats are manufactured, \(x_B\) must be greater than 0: \(x_B \geq y_B\)
9. If toy trains are manufactured, \(x_R\) must be greater than 0: \(x_R \geq y_R\)

### Non-negativity and Integer Constraints:
- \(x_T, x_P, x_B, x_R \geq 0\) and must be integers, as the quantities of toys cannot be negative or fractional.
- \(y_T, y_P, y_B, y_R \in \{0, 1\}\), as these are binary decision variables representing whether a certain toy is manufactured.

Using this model, we can apply integer programming techniques to find the optimal quantities of each toy to manufacture, maximizing total profit while satisfying all resource constraints and logical constraints. This will provide Haus Toys with an optimal manufacturing strategy.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for Haus Toys:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a COPT model for Haus Toys
model = env.createModel("HausToysOptimization")

# Add decision variables
x_T = model.addVar(vtype=COPT.INTEGER, name="x_T")  # Number of toy trucks
x_P = model.addVar(vtype=COPT.INTEGER, name="x_P")  # Number of toy planes
x_B = model.addVar(vtype=COPT.INTEGER, name="x_B")  # Number of toy boats
x_R = model.addVar(vtype=COPT.INTEGER, name="x_R")  # Number of toy trains
y_T = model.addVar(vtype=COPT.BINARY, name="y_T")   # Indicator variable for manufacturing toy trucks
y_P = model.addVar(vtype=COPT.BINARY, name="y_P")   # Indicator variable for manufacturing toy planes
y_B = model.addVar(vtype=COPT.BINARY, name="y_B")   # Indicator variable for manufacturing toy boats
y_R = model.addVar(vtype=COPT.BINARY, name="y_R")   # Indicator variable for manufacturing toy trains

# Set the objective function to maximize total profit
model.setObjective(5*x_T + 10*x_P + 8*x_B + 7*x_R, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(12*x_T + 20*x_P + 15*x_B + 10*x_R <= 890, name="WoodConstraint")
model.addConstr(6*x_T + 3*x_P + 5*x_B + 4*x_R <= 500, name="SteelConstraint")
model.addConstr(y_T + y_R <= 1, name="TruckTrainConstraint")
model.addConstr(y_B <= y_P, name="BoatPlaneConstraint")
model.addConstr(x_B <= x_R, name="BoatTrainConstraint")
model.addConstr(x_T >= y_T, name="TruckIndicator")
model.addConstr(x_P >= y_P, name="PlaneIndicator")
model.addConstr(x_B >= y_B, name="BoatIndicator")
model.addConstr(x_R >= y_R, name="TrainIndicator")

# Solve the model
model.solve()

# Analyze the solution
if model.status == COPT.OPTIMAL:
    print(f"Maximized total profit: ${model.objval}")
    print(f"Number of toy trucks: {x_T.x}")
    print(f"Number of toy planes: {x_P.x}")
    print(f"Number of toy boats: {x_B.x}")
    print(f"Number of toy trains: {x_R.x}")
else:
    print("No optimal solution found.")
```

This script first creates a COPT environment and model. Then, it adds decision variables, including the quantities of each toy and binary variables indicating whether each toy is manufactured. Next, it sets the objective function to maximize total profit and adds all necessary constraints. Finally, it solves the model and analyzes the solution, printing out the maximized total profit and the optimal quantities of each toy.

This script provides a complete example of using the `coptpy` library to solve the optimization problem for Haus Toys, considering all the given constraints and objectives.

---

## Case 18

**Ground truth:** 365.0  |  **3B answer:** None (Not Solved)  |  **8B answer:** 365.0

### Question
A furniture store can choose to order chairs from three different manufacturers, A, B, and C. The cost of ordering each chair from manufacturer A is $50, from manufacturer B is $45, and from manufacturer C is $40. The furniture store needs to minimize the total cost of the orders.

Additionally, each order from manufacturer A will include 15 chairs, while orders from B and C will include 10 chairs each. The order quantities can only be integers. The furniture store needs to order at least 100 chairs.

Each order from manufacturer A will include 15 chairs, while orders from manufacturers B and C will include 10 chairs each. The furniture store needs to order a maximum of 500 chairs.

If the furniture store decides to order chairs from manufacturer A, it must also order at least 10 chairs from manufacturer B.

Additionally, if the furniture store decides to order chairs from manufacturer B, it must also order chairs from manufacturer C.

### 3B formulation (WRONG)
```python
from pulp import LpProblem, LpVariable, lpSum, LpInteger

# Create a problem
prob = LpProblem("Furniture_Store_Operations", LpMinimize)

# Decision variables: number of orders for each manufacturer
x_A = LpVariable('x_A', lowBound=0, cat='Continuous')
x_B = LpVariable('x_B', lowBound=0, cat='Continuous')
x_C = LpVariable('x_C', lowBound=0, cat='Continuous')

# Objective function: minimize total cost
prob += lpSum([50*x_A + 45*x_B + 40*x_C]), "Total Cost"

# Constraints
# Minimum number of chairs to be ordered
prob += x_A + 1.0 * x_B + 1.0 * x_C >= 100, "Min_Chairs_Constraint"
# Maximum number of chairs to be ordered
prob += x_A + 1.0 * x_B + 1.0 * x_C <= 500, "Max_Chairs_Constraint"

# If A is ordered, then B must also be ordered (at least one chair)
prob += x_A >= 1 if x_B > 0 else None, "Constraint_AB"
# If B is ordered, then C must also be ordered (at least one chair)
prob += x_B >= 1 if x_C > 0 else None, "Constraint_BC"

# Solve the problem
status = prob.solve()

# Check if the problem was solved successfully
if status == 1:
    print(f"Optimal Solution Found: Total Cost = {value(prob.objective)}")
else:
    print("No solution found.")
```

Please note that the constraints and objective function need to be adjusted based on the specific requirements of the question. The current formulation assumes continuous variables for orders, which might not align with the requirement for integer values unless explicitly converted or handled differently.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the optimization problem for the furniture store, we will establish a linear programming model focused on minimizing the total cost of the orders while meeting the demand and adhering to the given constraints. The model can be formulated as follows:

### Decision Variables:
- \(x_A\): Number of orders from manufacturer A.
- \(x_B\): Number of orders from manufacturer B.
- \(x_C\): Number of orders from manufacturer C.

These variables represent the number of orders from each manufacturer to meet the chair demand.

### Objective Function:
- Minimize total cost: \(Z = 50x_A + 45x_B + 40x_C\)
  - This function calculates the total cost based on the number of orders from each manufacturer and their respective costs.

### Constraints:
1. Meet the chair demand: \(15x_A + 10x_B + 10x_C \geq 100\)
   - This ensures that the total number of chairs ordered meets or exceeds the demand of 100 chairs.
2. Maximum chair quantity: \(15x_A + 10x_B + 10x_C \leq 500\)
   - This constraint reflects the maximum chair quantity that the furniture store can order.
3. If chairs are ordered from manufacturer A, at least 10 chairs must be ordered from manufacturer B: \(x_A \leq 10x_B\)
4. If chairs are ordered from manufacturer B, chairs must also be ordered from manufacturer C: \(x_B \leq 10x_C\)

### Non-negativity and Integer Constraints:
- \(x_A, x_B, x_C \geq 0\) and must be integers, as the order quantities cannot be fractional.

Using this model, linear programming techniques can be applied to find the optimal quantities of chairs to order from each manufacturer, minimizing the total cost while meeting the chair demand and adhering to the ordering constraints. This will provide the furniture store with the most cost-effective strategy to allocate its purchasing resources.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the optimization problem for the furniture store:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a COPT model for the furniture store problem
model = env.createModel("FurnitureStoreOptimization")

# Add variables
x_A = model.addVar(lb=0, vtype=COPT.INTEGER, name="x_A")  # Number of orders from manufacturer A
x_B = model.addVar(lb=0, vtype=COPT.INTEGER, name="x_B")  # Number of orders from manufacturer B
x_C = model.addVar(lb=0, vtype=COPT.INTEGER, name="x_C")  # Number of orders from manufacturer C

# Add constraints
model.addConstr(15*x_A + 10*x_B + 10*x_C >= 100, name="DemandConstraint")  # Meet the chair demand
model.addConstr(15*x_A + 10*x_B + 10*x_C <= 500, name="MaxQuantityConstraint")  # Maximum chair quantity
model.addConstr(x_A <= 10*x_B, name="ManufacturerAConstraint")  # If chairs are ordered from manufacturer A, at least 10 chairs must be ordered from manufacturer B
model.addConstr(x_B <= 10*x_C, name="ManufacturerBConstraint")  # If chairs are ordered from manufacturer B, chairs must also be ordered from manufacturer C

# Set the objective function to minimize total cost
model.setObjective(50*x_A + 45*x_B + 40*x_C, sense=COPT.MINIMIZE)

# Solve the model
model.solve()

# Analyze the solution
if model.status == COPT.OPTIMAL:
    print(f"Minimum total cost: ${model.objval}")
    print(f"Number of orders from manufacturer A: {x_A.x}")
    print(f"Number of orders from manufacturer B: {x_B.x}")
    print(f"Number of orders from manufacturer C: {x_C.x}")
else:
    print("No optimal solution found.")
```

This script performs the following steps:

1. Imports the `coptpy` library and creates a COPT environment.
2. Creates a COPT model named "FurnitureStoreOptimization" for the furniture store problem.
3. Adds three integer decision variables, `x_A`, `x_B`, and `x_C`, representing the number of orders from manufacturers A, B, and C, respectively.
4. Adds four constraint conditions:
   - Meets the chair demand: The total number of chairs ordered must be greater than or equal to 100.
   - Maximum chair quantity: The total number of chairs ordered must be less than or equal to 500.
   - If chairs are ordered from manufacturer A, at least 10 chairs must be ordered from manufacturer B.
   - If chairs are ordered from manufacturer B, chairs must also be ordered from manufacturer C.
5. Sets the objective function to minimize the total cost, which is the sum of the costs of the orders from each manufacturer.
6. Solves the model.
7. Analyzes the solution:
   - If an optimal solution is found, prints the minimum total cost and the number of orders from each manufacturer.
   - If no optimal solution is found, prints the corresponding message.

This script provides a method to solve the optimization problem for the furniture store using the `coptpy` library, considering all the given constraints and objectives.

---

## Case 19

**Ground truth:** 960.0  |  **3B answer:** 800.0 (Optimal)  |  **8B answer:** 960.0

### Question
Bright Future Toys wants to build and sell robots, model cars, building blocks, and dolls. The profit from selling one robot is $15, from one model car is $8, from one set of building blocks is $12, and from one doll is $5. How many types of toys should Bright Future Toys manufacture to maximize profit?

There are 1200 units of plastic available. Manufacturing one robot requires 30 units of plastic, one model car requires 10 units of plastic, one set of building blocks requires 20 units of plastic, and one doll requires 15 units of plastic.

There are 800 units of electronic components available. Manufacturing one robot requires 8 units of electronic components, one model car requires 5 units of electronic components, one set of building blocks requires 3 units of electronic components, and one doll requires 2 units of electronic components.

If Bright Future Toys manufactures robots, then they will not manufacture dolls.

However, if they manufacture model cars, they will also manufacture building blocks.

The number of dolls manufactured cannot exceed the number of model cars manufactured.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Initialize the problem
prob = LpProblem("Bright_Future_Toys_Profit_Maximization", LpMaximize)

# Define decision variables
robots = LpVariable('Robots', lowBound=0, cat='Continuous')
model_cars = LpVariable('Model_Cars', lowBound=0, cat='Continuous')
building_blocks = LpVariable('Building_Blocks', lowBound=0, cat='Continuous')
dolls = LpVariable('Dolls', lowBound=0, cat='Continuous')

# Add the objective function
prob += robots*15 + model_cars*8 + building_blocks*12 + dolls*5

# Define constraints
# Plastic constraint
prob += 30*robots + 10*model_cars + 20*building_blocks + 15*dolls <= 1200

# Electronic components constraint
prob += 8*robots + 5*model_cars + 3*building_blocks + 2*dolls <= 800

# Constraint for robots and dolls
prob += robots >= dolls

# Constraint for model cars and building blocks
prob += building_blocks >= model_cars

# Constraint for dolls not exceeding model cars
prob += dolls <= model_cars

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Maximum Profit: ${value(prob.objective)}")
```

This code sets up and solves a linear programming problem to maximize Bright Future Toys' profit given the constraints on plastic, electronic components, and production limits.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the toy manufacturing problem for Bright Future Toys, we need to construct an integer programming model to maximize profit while satisfying the constraints of plastic and electronic components usage, as well as the logical relationships between toy types. Here is the model formulation:

### Decision Variables:
- \(x_R\): Number of robots manufactured.
- \(x_C\): Number of model cars manufactured.
- \(x_B\): Number of sets of building blocks manufactured.
- \(x_D\): Number of dolls manufactured.
- \(y_R\): Whether to manufacture robots (1 = yes, 0 = no).
- \(y_C\): Whether to manufacture model cars (1 = yes, 0 = no).
- \(y_B\): Whether to manufacture building blocks (1 = yes, 0 = no).
- \(y_D\): Whether to manufacture dolls (1 = yes, 0 = no).

### Objective Function:
- Maximize total profit: \[Z = 15x_R + 8x_C + 12x_B + 5x_D\]

### Constraints:
1. Plastic usage constraint: \[30x_R + 10x_C + 20x_B + 15x_D \leq 1200\]
2. Electronic components usage constraint: \[8x_R + 5x_C + 3x_B + 2x_D \leq 800\]
3. If robots are manufactured, dolls cannot be manufactured: \[y_R + y_D \leq 1\]
4. If model cars are manufactured, building blocks must be manufactured: \[y_C \leq y_B\]
5. The number of dolls manufactured cannot exceed the number of model cars manufactured: \[x_D \leq x_C\]
6. If a decision is made to manufacture a toy, the corresponding quantity must be greater than 0:
   - \(x_R \geq y_R\)
   - \(x_C \geq y_C\)
   - \(x_B \geq y_B\)
   - \(x_D \geq y_D\)

### Non-negativity and Integer Constraints:
- \(x_R, x_C, x_B, x_D \geq 0\) and must be integers.
- \(y_R, y_C, y_B, y_D \in \{0, 1\}\)

Using this model, we can apply integer programming techniques to find the optimal quantities of each toy to manufacture, maximizing total profit while satisfying all material usage and logical constraints. This will provide Bright Future Toys with an optimal toy manufacturing strategy.

## Python Code Solution Using `coptpy`:
Here is a Python script using the `coptpy` library to solve the toy manufacturing problem for Bright Future Toys:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ToyManufacturingOptimization")

# Add decision variables
x_R = model.addVar(vtype=COPT.INTEGER, name="x_R")  # Number of robots manufactured
x_C = model.addVar(vtype=COPT.INTEGER, name="x_C")  # Number of model cars manufactured
x_B = model.addVar(vtype=COPT.INTEGER, name="x_B")  # Number of sets of building blocks manufactured
x_D = model.addVar(vtype=COPT.INTEGER, name="x_D")  # Number of dolls manufactured

y_R = model.addVar(vtype=COPT.BINARY, name="y_R")   # Whether to manufacture robots
y_C = model.addVar(vtype=COPT.BINARY, name="y_C")   # Whether to manufacture model cars
y_B = model.addVar(vtype=COPT.BINARY, name="y_B")   # Whether to manufacture building blocks
y_D = model.addVar(vtype=COPT.BINARY, name="y_D")   # Whether to manufacture dolls

# Set the objective function: Maximize total profit
model.setObjective(15*x_R + 8*x_C + 12*x_B + 5*x_D, sense=COPT.MAXIMIZE)

# Add constraints
model.addConstr(30*x_R + 10*x_C + 20*x_B + 15*x_D <= 1200, name="PlasticConstraint")
model.addConstr(8*x_R + 5*x_C + 3*x_B + 2*x_D <= 800, name="ElectronicComponentsConstraint")
model.addConstr(y_R + y_D <= 1, name="RobotDollConstraint")
model.addConstr(y_C <= y_B, name="CarBlockConstraint")
model.addConstr(x_D <= x_C, name="DollCarConstraint")
model.addConstr(x_R >= y_R, name="RobotDecisionConstraint")
model.addConstr(x_C >= y_C, name="CarDecisionConstraint")
model.addConstr(x_B >= y_B, name="BlockDecisionConstraint")
model.addConstr(x_D >= y_D, name="DollDecisionConstraint")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total profit: ${}".format(model.objval))
    print("Number of robots manufactured: {}".format(x_R.x))
    print("Number of model cars manufactured: {}".format(x_C.x))
    print("Number of sets of building blocks manufactured: {}".format(x_B.x))
    print("Number of dolls manufactured: {}".format(x_D.x))
else:
    print("No optimal solution found.")
```

In this script, we first create a COPT environment and model. Then, we add decision variables, including the quantities of each toy manufactured and binary variables indicating whether each toy is manufactured.

Next, we set the objective function to maximize total profit and add all necessary constraints, including material usage constraints, logical constraints, and constraints ensuring that if a decision is made to manufacture a toy, the corresponding quantity is greater than 0.

Finally, we solve the model and output the results, including the maximized total profit and the quantities of each toy manufactured.

This script provides a complete example of using the `coptpy` library to solve the toy manufacturing problem for Bright Future Toys, considering all given constraints and objectives.

---

## Case 20

**Ground truth:** 368999.99999999994  |  **3B answer:** None (?)  |  **8B answer:** 368999.99999999994

### Question
A company plans to produce three products $A_{1}, A_{2}, A_{3}$. It can produce for 22 days in a month. The table below gives the maximum demand (in units of 100 kg), prices ($\$/100 \mathrm{~Kg}$), production costs (per 100 kg of product), and production quotas (the maximum number of units of 100 kg of product that can be produced in a day if all production lines are dedicated to that product).

| Product | $A_{1}$ | $A_{2}$ | $A_{3}$ |
| :---: | :---: | :---: | :---: |
| Maximum Demand | 5300 | 4500 | 5400 |
| Selling Price | $\$ 124$ | $\$ 109$ | $\$ 115$ |
| Production Cost | $\$ 73.30$ | $\$ 52.90$ | $\$ 65.40$ |
| Production Quota | 500 | 450 | 550 |

The fixed activation cost for each production line is as follows:

| Product | $A_{1}$ | $A_{2}$ | $A_{3}$ |
| :---: | :---: | :---: | :---: |
| Activation Cost | $\$ 170000$ | $\$ 150000$ | $\$ 100000$ |

The minimum production batch sizes are as follows:
$$
\begin{array}{c|ccc}
\text { Product } & A_{1} & A_{2} & A_{3} \\
\hline \text { Minimum Batch Size } & 20 & 20 & 16
\end{array}
$$
Please formulate an operations research model to determine the production plan that maximizes total revenue while accommodating the fixed activation costs and minimum production batch size restrictions.

### 3B formulation (WRONG)
```python
from pulp import LpMaximize, LpVariable

# Define the problem
prob = LpProblem("Production_Planning_Problem", LpMaximize)

# Decision variables: binary variables for whether a product is produced each day
x1 = [LpVariable(f'x1_{i}', 0, None) for i in range(22)]
x2 = [LpVariable(f'x2_{i}', 0, None) for i in range(22)]
x3 = [LpVariable(f'x3_{i}', 0, None) for i in range(22)]

# Objective function: maximize total revenue
revenue = sum((124/100 * (100 + 100*x1[i]) - 73.3/100 * (100 + 100*x1[i]) -
                52.9/100 * (100 + 100*x2[i]) - 65.4/100 * (100 + 100*x3[i])) *
               min(1, i+1) for i in range(22))
prob += revenue

# Constraints: demand constraints
demand_constraints = [
    sum(x1[i] for i in range(j*22, j*22+22)) - 5300 <= 0,
    sum(x2[i] for i in range(j*22, j*22+22)) - 4500 <= 0,
    sum(x3[i] for i in range(j*22, j*22+22)) - 5400 <= 0
    for j in range(1)
]

# Constraints: production quotas
production_quotas = [
    sum(x1[i] for i in range(j*22, j*22+22)) <= 500,
    sum(x2[i] for i in range(j*22, j*22+22)) <= 450,
    sum(x3[i] for i in range(j*22, j*22+22)) <= 550
]

# Constraints: activation costs
activation_costs = [
    (170000/100000 * x1[j] + 150000/100000 * x2[j] + 100000/100000 * x3[j]) <= j
    for j in range(1)
]

# Constraints: minimum production batch sizes
batch_sizes = [
    (x1[i] - 20) / 20 >= 0,
    (x2[i] - 20) / 20 >= 0,
    (x3[i] - 16) / 16 >= 0
    for i in range(22)
]

# Solve the problem
prob.solve()

# Print results
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

print(f"Total Revenue: ${value(prob.objective):.2f}")
```

This code formulates and solves a production planning model using PuLP to maximize total revenue while considering demand constraints, fixed activation costs, and minimum batch size restrictions for each product.

### ORLM-8B formulation (CORRECT)
## Mathematical Model:
To solve the company's production planning problem, we need to construct a mathematical model to maximize total revenue while considering production costs, production quotas, maximum demand, fixed activation costs, and minimum production batch sizes. The model can be formulated as follows:

### Decision Variables:
- \(x_i\): The quantity of product \(i\) produced, where \(i \in \{A_1, A_2, A_3\}\).
- \(y_i\): Whether to activate the production line for product \(i\), where \(i \in \{A_1, A_2, A_3\}\). If activated, \(y_i = 1\); otherwise, \(y_i = 0\).

### Objective Function:
- Maximize total revenue: \[Z = \sum_{i \in \{A_1, A_2, A_3\}} (Selling Price_i \times x_i - Production Cost_i \times x_i - Activation Cost_i \times y_i)\]
  - This function calculates the total revenue based on the selling price, production cost, production quantity, and activation status of each product.

### Constraints:
1. Production quota constraint: \[\frac{x_i}{Production Quota_i} \leq 22 \times y_i, \forall i \in \{A_1, A_2, A_3\}\]
   - This ensures that the production quantity of each product does not exceed the production quota multiplied by the number of production days and the activation status.
2. Maximum demand constraint: \[x_i \leq Maximum Demand_i, \forall i \in \{A_1, A_2, A_3\}\]
   - This ensures that the production quantity of each product does not exceed the maximum demand.
3. Minimum production batch size constraint: \[x_i \geq Minimum Batch Size_i \times y_i, \forall i \in \{A_1, A_2, A_3\}\]
   - This ensures that if the production line for a product is activated, the production quantity is at least the minimum production batch size.

### Non-negativity and Integer Constraints:
- \(x_i \geq 0, \forall i \in \{A_1, A_2, A_3\}\) and must be integers, as the production quantity of products must be integers.
- \(y_i \in \{0, 1\}, \forall i \in \{A_1, A_2, A_3\}\), as the activation status of the production line is binary.

Using this model, we can apply integer programming techniques to find the optimal production quantities and activation statuses for each product, maximizing total revenue while satisfying the production quota, maximum demand, and minimum production batch size constraints. This will provide the company with an economically efficient production plan.

## Python Code Solution Using `coptpy`:
Below is a Python script using the `coptpy` library to solve the production planning problem:

```python
import coptpy as cp
from coptpy import COPT

# Create a COPT environment
env = cp.Envr()

# Create a model
model = env.createModel("ProductionPlanning")

# Define the data
products = ["A1", "A2", "A3"]
max_demand = {"A1": 5300, "A2": 4500, "A3": 5400}
selling_price = {"A1": 124, "A2": 109, "A3": 115}
production_cost = {"A1": 73.30, "A2": 52.90, "A3": 65.40}
production_quota = {"A1": 500, "A2": 450, "A3": 550}
activation_cost = {"A1": 170000, "A2": 150000, "A3": 100000}
min_batch = {"A1": 20, "A2": 20, "A3": 16}
production_days = 22

# Add decision variables
x = {i: model.addVar(vtype=COPT.INTEGER, name=f"x_{i}") for i in products}
y = {i: model.addVar(vtype=COPT.BINARY, name=f"y_{i}") for i in products}

# Set the objective function
model.setObjective(cp.quicksum((selling_price[i] - production_cost[i]) * x[i] - activation_cost[i] * y[i] for i in products), sense=COPT.MAXIMIZE)

# Add constraints
for i in products:
    model.addConstr(x[i] / production_quota[i] <= production_days * y[i], name=f"ProductionQuota_{i}")
    model.addConstr(x[i] <= max_demand[i], name=f"MaxDemand_{i}")
    model.addConstr(x[i] >= min_batch[i] * y[i], name=f"MinBatch_{i}")

# Solve the model
model.solve()

# Output the results
if model.status == COPT.OPTIMAL:
    print("Maximized total revenue: {:.2f} dollars".format(model.objval))
    print("Production plan:")
    for i in products:
        if y[i].x > 0.5:  # If y_i is greater than 0.5, consider the production line for that product activated
            print(f"Product {i}: Produce {x[i].x:.0f} units")
else:
    print("No optimal solution found.")
```

In this script, we first define the data for the problem, including the product list, maximum demand, selling price, production cost, production quota, activation cost, and minimum production batch size. Then, it creates decision variables `x` and `y`, representing the production quantity and activation status of each product.

Next, the script sets the objective function, which is to maximize total revenue, and adds constraints, including the production quota constraint, maximum demand constraint, and minimum production batch size constraint.

Finally, the script solves the model and outputs the maximized total revenue and the production plan. If an optimal solution is found, it prints the production quantity for each activated product; otherwise, it indicates that no optimal solution was found.

This script provides a complete example of using the `coptpy` library to solve the production planning problem, considering all the given constraints and objectives.

---
