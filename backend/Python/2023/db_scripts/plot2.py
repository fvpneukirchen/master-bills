import matplotlib.pyplot as plt

# Survey data
questions = [f'Question {i+1}' for i in range(10)]
# questions = [f'{idx + 1} - {a}' for idx, a in enumerate([
#     "I think that I would like to use this system frequently.",
#     "I found the system unnecessarily complex.",
#     "I thought the system was easy to use.",
#     "I think that I would need the support of a technical person to be able to use this system.",
#     "I found the various functions in this system were well integrated.",
#     "I thought there was too much inconsistency in this system.",
#     "I would imagine that most people would learn to use this system very quickly.",
#     "I found the system very cumbersome to use.",
#     "I felt very confident using the system.",
#     "I needed to learn a lot of things before I could get going with this system."
# ])]
categories = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
responses_experts = [
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
responses_non_experts = [
    ["Strongly Disagree",
     "Agree",
     "Neutral",
     "Strongly Disagree",
     "Disagree",
     "Strongly Disagree",
     "Disagree",
     "Neutral",
     "Agree",
     "Neutral",
     "Disagree"
     ],
    ["Strongly Agree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Strongly Agree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Agree",
     "Disagree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Neutral"
     ],
    ["Strongly Disagree",
     "Agree",
     "Agree",
     "Strongly Disagree",
     "Agree",
     "Agree",
     "Disagree",
     "Neutral",
     "Agree",
     "Agree",
     "Neutral"
     ],
    ["Strongly Disagree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Strongly Agree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Agree",
     "Agree",
     "Disagree",
     "Neutral",
     "Strongly Disagree"],
    ["Strongly Disagree",
     "Strongly Agree",
     "Strongly Agree",
     "Strongly Disagree",
     "Agree",
     "Strongly Agree",
     "Neutral",
     "Strongly Agree",
     "Agree",
     "Strongly Agree",
     "Agree"
     ],
    ["Strongly Disagree",
     "Strongly Disagree",
     "Disagree",
     "Neutral",
     "Strongly Disagree",
     "Strongly Disagree",
     "Neutral",
     "Strongly Disagree",
     "Disagree",
     "Disagree",
     "Disagree"
     ],
    ["Strongly Disagree",
     "Agree",
     "Neutral",
     "Strongly Disagree",
     "Neutral",
     "Agree",
     "Disagree",
     "Agree",
     "Agree",
     "Agree",
     "Neutral"
     ],
    ["Strongly Agree",
     "Strongly Disagree",
     "Disagree",
     "Strongly Agree",
     "Strongly Disagree",
     "Disagree",
     "Agree",
     "Neutral",
     "Disagree",
     "Disagree",
     "Neutral"
     ],
    ["Strongly Disagree",
     "Strongly Agree",
     "Strongly Agree",
     "Strongly Disagree",
     "Agree",
     "Agree",
     "Disagree",
     "Neutral",
     "Disagree",
     "Agree",
     "Disagree"
     ],
    ["Neutral",
     "Strongly Disagree",
     "Strongly Disagree",
     "Strongly Agree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Strongly Disagree",
     "Disagree",
     "Strongly Disagree",
     "Disagree",
     "Strongly Disagree"
     ]
]
responses_non_experts_2024 =[
  [
    "Agree",
    "Neutral",
    "Strongly Disagree",
    "Disagree",
    "Strongly Agree",
    "Agree",
    "Agree",
    "Agree",
    "Neutral",
    "Strongly Disagree",
    "Neutral",
    "Disagree",
    "Agree",
    "Neutral"
  ],
  [
    "Disagree",
    "Neutral",
    "Strongly Disagree",
    "Agree",
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Disagree",
    "Disagree",
    "Agree",
    "Strongly Disagree",
    "Disagree",
    "Strongly Disagree",
    "Neutral"
  ],
  [
    "Agree",
    "Strongly Agree",
    "Strongly Disagree",
    "Strongly Disagree",
    "Agree",
    "Agree",
    "Disagree",
    "Agree",
    "Agree",
    "Strongly Disagree",
    "Neutral",
    "Disagree",
    "Strongly Agree",
    "Disagree"
  ],
  [
    "Disagree",
    "Disagree",
    "Strongly Agree",
    "Neutral",
    "Strongly Disagree",
    "Agree",
    "Neutral",
    "Disagree",
    "Strongly Disagree",
    "Strongly Agree",
    "Neutral",
    "Agree",
    "Strongly Disagree",
    "Neutral"
  ],
  [
    "Agree",
    "Disagree",
    "Neutral",
    "Strongly Disagree",
    "Agree",
    "Agree",
    "Neutral",
    "Agree",
    "Agree",
    "Strongly Disagree",
    "Strongly Agree",
    "Agree",
    "Strongly Agree",
    "Agree"
  ],
  [
    "Strongly Disagree",
    "Agree",
    "Agree",
    "Neutral",
    "Strongly Disagree",
    "Strongly Disagree",
    "Disagree",
    "Strongly Disagree",
    "Disagree",
    "Strongly Disagree",
    "Disagree",
    "Disagree",
    "Strongly Disagree",
    "Agree"
  ],
  [
    "Disagree",
    "Strongly Agree",
    "Strongly Disagree",
    "Strongly Disagree",
    "Strongly Agree",
    "Strongly Agree",
    "Strongly Disagree",
    "Strongly Agree",
    "Agree",
    "Neutral",
    "Strongly Agree",
    "Strongly Disagree",
    "Strongly Agree",
    "Agree"
  ],
  [
    "Disagree",
    "Strongly Disagree",
    "Strongly Agree",
    "Agree",
    "Disagree",
    "Strongly Disagree",
    "Agree",
    "Strongly Disagree",
    "Disagree",
    "Agree",
    "Strongly Disagree",
    "Neutral",
    "Strongly Disagree",
    "Neutral"
  ],
  [
    "Agree",
    "Agree",
    "Disagree",
    "Strongly Disagree",
    "Neutral",
    "Strongly Agree",
    "Disagree",
    "Strongly Agree",
    "Neutral",
    "Strongly Disagree",
    "Strongly Agree",
    "Neutral",
    "Agree",
    "Neutral"
  ],
  [
    "Strongly Disagree",
    "Neutral",
    "Disagree",
    "Disagree",
    "Strongly Disagree",
    "Strongly Disagree",
    "Neutral",
    "Strongly Disagree",
    "Agree",
    "Disagree",
    "Strongly Disagree",
    "Strongly Disagree",
    "Disagree",
    "Strongly Disagree"
  ]
]

# responses = responses_non_experts_2024
# responses = responses_non_experts
responses = responses_experts

# RGB colors
colors = {
    "Strongly Disagree": (242 / 255, 71 / 255, 38 / 255),
    "Disagree": (250 / 255, 199 / 255, 16 / 255),
    "Neutral": (254 / 255, 244 / 255, 69 / 255),
    "Agree": (206 / 255, 231 / 255, 65 / 255),
    "Strongly Agree": (143 / 255, 209 / 255, 79 / 255),
}

# # Create horizontal bar plot
# fig, ax = plt.subplots(figsize=(10, 10))
# # for idx, (question, response) in enumerate(zip(questions, responses)):
# #     for i, category in enumerate(categories):
# #         count = response.count(category)
# #         ax.barh(idx, count, color=colors[category], left=sum(response.count(categories[j]) for j in range(i)))
# for idx, (question, response) in enumerate(zip(questions, responses)):
#     total_responses = len(response)
#     left_offset = 0
#     for category in categories:
#         count = response.count(category)
#         percentage = (count / total_responses) * 100
#         ax.barh(idx, count, color=colors[category], left=left_offset)
#         if count > 0:
#             ax.text(left_offset + count / 2, idx, f'{percentage:.1f}%', ha='center', va='center', color='black')
#         left_offset += count
#
# ax.set_yticks(range(len(questions)))
# ax.set_yticklabels(questions)
# # ax.set_xlabel("Number of Responses")
# # ax.set_title("Response Distribution by Question")
# ax.legend(handles=[plt.Rectangle((-10, -10), 1, 1, color=color) for color in colors.values()],
#           labels=categories, loc="upper right")
# plt.tight_layout()
# plt.show()

fig, ax = plt.subplots(figsize=(10, 6))  # Aumentei a largura (12) para mais espaço

# Plotando as barras (mesmo código)
for idx, (question, response) in enumerate(zip(questions, responses)):
    total_responses = len(response)
    left_offset = 0
    for category in categories:
        count = response.count(category)
        percentage = (count / total_responses) * 100
        ax.barh(idx, count, color=colors[category], left=left_offset)
        if count > 0:
            ax.text(left_offset + count / 2, idx, f'{percentage:.1f}%', ha='center', va='center', color='black', fontsize=15)
        left_offset += count

ax.set_xticks([])  # Remove os números do eixo X
ax.set_xlabel('')  # Remove o label do eixo X (caso exista)

# --- Correção dos labels do eixo Y ---
# 1. Definir os ticks e alinhar à esquerda
ax.set_yticks(range(len(questions)))
ax.set_yticklabels(questions, ha='left', va='center', fontsize=15)  # Alinhamento + tamanho da fonte

# 2. Ajustar a posição dos labels sem comprimir o gráfico
# ax.tick_params(axis='y', pad=750)  # Aumenta o espaço entre os labels e o gráfico
ax.tick_params(axis='y', pad=150)  # Aumenta o espaço entre os labels e o gráfico

# 3. Ajustar margens (sem reduzir demais a área do gráfico)
plt.subplots_adjust(left=0.3)  # Valor menor que 0.4, mas com tick_params resolve

# --- Legenda ---
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[cat]) for cat in categories]
ax.legend(
    handles=legend_handles,
    labels=categories,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.1),  # Ajuste fino na posição vertical
    ncol=len(categories),
    fontsize=15
)

plt.tight_layout()  # Ajuste automático adicional
plt.show()