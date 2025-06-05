# run_rl_loop.py
import time
import matplotlib.pyplot as plt
import pandas as pd
from attack_module import Attacker
from defense_module import Defender
from reward_module import evaluate_response  # make sure the name is correct

# Initialization
attacker = Attacker()
defender = Defender()

NUM_ITERATIONS = 100
log_data, reward_history = [], []

print("🔁 Starting Reinforcement Learning Loop...\n")

# Main loop
for iteration in range(1, NUM_ITERATIONS + 1):
    # Step 1: Attacker generates adversarial prompt
    query = attacker.generate_adversarial_query(iteration)

    # Step 2: Defender responds (with Gemini)
    response = defender.get_response(query)

    # Step 3: Evaluate the defender's response
    reward = evaluate_response(response)
    reward_history.append(reward)

    # Step 4: Log metrics and update attacker (optional)
    log_data.append([iteration, query, response, reward])
    attacker.update_q_values(reward)  # Only if Q-learning logic is implemented

    # Step 5: Calculate metrics
    average_reward = sum(reward_history) / len(reward_history)
    loss = 1 - average_reward
    accuracy = sum(1 for r in reward_history if r >= 0.5) / len(reward_history)


    print(f"Iter {iteration:3d} | Reward: {reward:.2f} | Acc: {accuracy:.2f} | Loss: {loss:.2f}")
    
    # Sleep to respect Gemini API rate limits (15 RPM)
    time.sleep(5) # Adjust sleep time as needed

# Save logs and graph
df = pd.DataFrame(log_data, columns=["Iteration", "Query", "Response", "Reward"])
df.to_csv("data/logs.csv", index=False)

plt.figure(figsize=(10, 4))
plt.plot(reward_history, label="Reward per Iteration", color="blue")
plt.axhline(0.5, linestyle="--", color="red", label="Passing Threshold")
plt.title("Reward Trend over 100 Iterations")
plt.xlabel("Iteration")
plt.ylabel("Reward")
plt.legend()
plt.grid(True)
plt.savefig("data/reward_curve.png")
plt.show()

print("\n✅ Loop completed. Logs saved to 'data/logs.csv'. Reward curve saved to 'data/reward_curve.png'.")
