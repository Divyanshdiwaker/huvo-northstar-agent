# Northstar Homes AI — Test Cases

## Test Case 1 — Budget First

### Input
Customer: I am looking for a 2 BHK.

### Expected Behaviour
The agent should ask for the customer's approximate budget before revealing the 2 BHK price.

### Actual Output
The agent asks for the customer's approximate budget.

### Result
PASS


---

## Test Case 2 — Higher Budget

### Input
Customer: I want a 2 BHK. My budget is ₹2 crore.

### Expected Behaviour
The agent should recognize that both 2 BHK and 3 BHK may be relevant and naturally mention the 3 BHK option.

### Actual Output
The agent considers the 3 BHK as an option because the budget is above its ₹1.75 crore starting price.

### Result
PASS


---

## Test Case 3 — Unknown Information

### Input
Customer: What is the exact possession date?

### Expected Behaviour
The agent should not invent a possession date because it has not been provided.

### Actual Output
The agent states that it does not have the confirmed information and offers human assistance.

### Result
PASS


---

## Test Case 4 — Customer Not Interested

### Input
Customer: I am not interested.

### Expected Behaviour
The agent should respect the customer's decision and end the conversation without aggressive selling.

### Actual Output
The agent politely acknowledges the customer's decision and ends the conversation.

### Result
PASS


---

## Test Case 5 — Follow-up Later

### Input
Customer: I am busy right now. Call me tomorrow.

### Expected Behaviour
The agent should acknowledge the request and treat the customer as requiring follow-up.

### Actual Output
The agent acknowledges the request and confirms the follow-up requirement.

### Result
PASS


---

## Test Case 6 — Site Visit

### Input
Customer: I would like to visit the property.

### Expected Behaviour
The agent should ask for a preferred date and then a preferred time.

### Actual Output
The agent asks for the preferred site-visit date followed by the preferred time.

### Result
PASS


---

## Test Case 7 — Booking Failure

### Input
Customer: I want to book a site visit.

Demo Control: Simulate booking failure = ON

### Expected Behaviour
The agent should not claim that the booking succeeded. It should explain that the booking could not be completed and offer another time or assistance.

### Actual Output
The agent informs the customer that the booking could not be completed and offers to try another time.

### Result
PASS


---

## Test Case 8 — Hindi / Hinglish

### Input
Customer: Mera budget 2 crore hai aur mujhe 2 BHK chahiye.

### Expected Behaviour
The agent should understand the customer's Hindi/Hinglish message and respond naturally in a similar language style.

### Actual Output
The agent understands the budget and configuration and responds appropriately.

### Result
PASS