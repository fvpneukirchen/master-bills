import matplotlib.pyplot as plt

# Survey data
questions = [f'Question {i+1}' for i in range(10)]
categories = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
responses = [
    ["Disagree", "Strongly Agree"],
    ["Strongly Disagree", "Disagree"],
    ["Neutral", "Agree"],
    ["Strongly Disagree", "Neutral"],
    ["Disagree", "Strongly Agree"],
    ["Strongly Disagree", "Disagree"],
    ["Neutral", "Neutral"],
    ["Strongly Disagree", "Disagree"],
    ["Neutral", "Strongly Agree"],
    ["Strongly Disagree", "Neutral"]
]

# RGB colors
colors = {
    "Strongly Disagree": (242/255, 71/255, 38/255),
    "Disagree": (250/255, 199/255, 16/255),
    "Neutral": (254/255, 244/255, 69/255),
    "Agree": (206/255, 231/255, 65/255),
    "Strongly Agree": (143/255, 209/255, 79/255),
}

# Create horizontal bar plot
fig, ax = plt.subplots(figsize=(10, 6))
# for idx, (question, response) in enumerate(zip(questions, responses)):
#     for i, category in enumerate(categories):
#         count = response.count(category)
#         ax.barh(idx, count, color=colors[category], left=sum(response.count(categories[j]) for j in range(i)))
for idx, (question, response) in enumerate(zip(questions, responses)):
    total_responses = len(response)
    left_offset = 0
    for category in categories:
        count = response.count(category)
        percentage = (count / total_responses) * 100
        ax.barh(idx, count, color=colors[category], left=left_offset)
        if count > 0:
            ax.text(left_offset + count / 2, idx, f'{percentage:.1f}%', ha='center', va='center', color='black')
        left_offset += count

ax.set_yticks(range(len(questions)))
ax.set_yticklabels(questions)
# ax.set_xlabel("Number of Responses")
# ax.set_title("Response Distribution by Question")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=color) for color in colors.values()],
          labels=categories, loc="upper right")
plt.tight_layout()
plt.show()
