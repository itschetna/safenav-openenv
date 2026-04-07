# SafeNav OpenEnv

AI environment for selecting the safest route between two locations based on crime data.

---

## 🚀 Overview

SafeNav is a real-world inspired reinforcement learning environment where an AI agent must choose the safest route among multiple options.

The agent receives route data including crime scores and distances, and must optimize for safety while optionally performing analysis before making a decision.

---

## 🧠 Tasks

- **Easy**: Choose the safest route among 2 options  
- **Medium**: Choose the safest route among 3 options  
- **Hard**: Perform analysis before selecting the safest route  

---

## ⚙️ Action Space

The agent can take the following actions:

- `analyze`
- `choose_route_1`
- `choose_route_2`
- `choose_route_3`

---

## 👁️ Observation Space

The environment returns:

- Start location
- End location
- List of routes:
  - `route_id`
  - `crime_score` (lower is safer)
  - `distance`
- Step count

---

## 🎯 Reward Function

The reward is designed to reflect real-world decision-making:

- **Safety-based reward**:  
  `reward = 1 - crime_score`

- **Bonus for analysis**:  
  +0.1 if agent performs `analyze` before choosing

- **Invalid actions penalty**:  
  -0.1 for incorrect or invalid actions

- Rewards are always normalized between **0.0 and 1.0**

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python inference.py