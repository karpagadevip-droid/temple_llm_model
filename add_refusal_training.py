"""
Refusal Training Dataset Augmentation Script
Adds negative examples to teach the model when to say "I don't know"
Prevents hallucination about non-existent temples
"""

import json
import random

# ============================================================
# Load Original Dataset
# ============================================================

with open('temples.json', 'r', encoding='utf-8') as f:
    temples_data = json.load(f)

print(f"Original dataset: {len(temples_data)} examples")

# ============================================================
# Define Refusal Examples
# ============================================================

# Fake temple names (things the model should refuse to answer)
fake_temples = [
    "Helloweeddada Temple",
    "Sparkle Mountain Temple",
    "Dragon Fire Temple",
    "Crystal Palace Temple",
    "Rainbow Bridge Temple",
    "Moonlight Sanctuary",
    "Thunder Valley Temple",
    "Golden Phoenix Temple",
    "Silver Dragon Temple",
    "Emerald Forest Temple",
    "Azure Sky Temple",
    "Crimson Lotus Temple",
]

# Non-temple landmarks (should refuse as out of scope)
non_temples = [
    "Eiffel Tower",
    "Statue of Liberty",
    "Big Ben",
    "Great Wall of China",
    "Taj Mahal Hotel",
    "Burj Khalifa",
    "Sydney Opera House",
    "Colosseum",
    "Machu Picchu",
    "Stonehenge",
    "Christ the Redeemer",
    "Leaning Tower of Pisa",
]

# Refusal response templates
refusal_responses = [
    "I am sorry, I do not have information about that temple in my database.",
    "I don't have any information about that temple. I can only provide details about well-documented Indian temples.",
    "I cannot find information about that temple in my knowledge base. Please ask about a different Indian temple.",
    "That temple is not in my database. I specialize in providing information about established Indian temples.",
]

out_of_scope_responses = [
    "I only answer questions about Indian temples. The {name} is not a temple.",
    "I specialize in Indian temples. {name} is outside my area of expertise.",
    "I can only provide information about Hindu, Jain, Buddhist, and Sikh temples in India. Please ask about an Indian temple.",
    "That's not an Indian temple. I'm trained specifically on Indian temple information.",
]

# ============================================================
# Generate Refusal Examples
# ============================================================

refusal_examples = []

# Generate fake temple refusals
for fake_temple in fake_temples:
    example = {
        "instruction": f"Tell me about {fake_temple}.",
        "input": "Historical site inquiry.",
        "output": random.choice(refusal_responses)
    }
    refusal_examples.append(example)

# Generate out-of-scope refusals
for landmark in non_temples:
    example = {
        "instruction": f"Tell me about {landmark}.",
        "input": "Historical site inquiry.",
        "output": random.choice(out_of_scope_responses).format(name=landmark)
    }
    refusal_examples.append(example)

print(f"Generated {len(refusal_examples)} refusal examples")

# ============================================================
# Combine Datasets with Proper Ratio
# ============================================================

# Recommended ratio: 10 real examples : 1 refusal example
# We have 114 real temples, so we'll add ~11-12 refusal examples

# Calculate how many refusals we need (10% of real examples)
num_refusals_needed = len(temples_data) // 10

# Randomly sample refusal examples
selected_refusals = random.sample(refusal_examples, min(num_refusals_needed, len(refusal_examples)))

# Combine datasets
augmented_dataset = temples_data + selected_refusals

# Shuffle to mix refusals throughout the dataset
random.shuffle(augmented_dataset)

print(f"\nAugmented dataset composition:")
print(f"  Real temples: {len(temples_data)}")
print(f"  Refusal examples: {len(selected_refusals)}")
print(f"  Total: {len(augmented_dataset)}")
print(f"  Ratio: {len(temples_data)}:{len(selected_refusals)} (~10:1)")

# ============================================================
# Save Augmented Dataset
# ============================================================

# Save to new file
output_file = 'temples_with_refusals.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(augmented_dataset, f, indent=2, ensure_ascii=False)

print(f"\n[SUCCESS] Augmented dataset saved to: {output_file}")

# ============================================================
# Show Sample Refusal Examples
# ============================================================

print("\n" + "="*60)
print("Sample Refusal Examples Added:")
print("="*60)

for i, example in enumerate(selected_refusals[:3], 1):
    print(f"\nExample {i}:")
    print(f"  Instruction: {example['instruction']}")
    print(f"  Input: {example['input']}")
    print(f"  Output: {example['output']}")

print("\n" + "="*60)
print("Dataset is ready for fine-tuning!")
print("="*60)
print("\nNext steps:")
print("1. Upload 'temples_with_refusals.json' to Google Colab")
print("2. Update the script to load 'temples_with_refusals.json' instead of 'temples.json'")
print("3. Run the fine-tuning script")
print("4. Test with both real and fake temple names")
