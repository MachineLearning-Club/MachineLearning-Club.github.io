#!/usr/bin/env python3
"""Fix the legacy Week 7 starter notebook: preserve the lesson's two clear models.

No NumPy, Matplotlib, scikit-learn or network packages. This notebook can run
in JupyterLite or a regular Python notebook with only the standard library.
"""
import ast
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def cell(kind,source):
    data={'cell_type':kind,'metadata':{},'source':[line+'\n' for line in source.strip().split('\n')]}
    if kind=='code':
        ast.parse(source)
        data.update(execution_count=None,outputs=[])
    return data
intro='''# Week 7 — XOR representation and a first gradient update

**Machine Learning Club · Self-contained laboratory starter**

The two following demonstrations answer **different questions**:

1. Can a network with hidden neurons represent XOR? We will **supply** weights and trace every value. This demonstrates *representation*, not training.
2. Can a smooth neuron improve by taking gradient steps? We will **train one weight** on one example, print loss changes, and inspect a numerical gradient.

These demonstrations connect to the two more detailed Week 7 laboratory notebooks. Python's standard library is sufficient; there are no hidden downloads or API keys.
'''
xor='''# Supplied weights: OR, AND, then OR minus twice AND.
# These weights were NOT learned by this program.
def threshold(z):
    return int(z >= 0)

def xor_forward(x1, x2):
    h_or = threshold(x1 + x2 - 0.5)
    h_and = threshold(x1 + x2 - 1.5)
    output_sum = h_or - 2 * h_and - 0.5
    predicted = threshold(output_sum)
    return h_or, h_and, output_sum, predicted

for x1, x2, expected in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]:
    h_or, h_and, z, prediction = xor_forward(x1, x2)
    print((x1, x2), "hidden:", (h_or, h_and),
          "output sum:", z, "prediction:", prediction,
          "expected:", expected)
    assert prediction == expected
print("All four XOR cases agree with the truth table.")
'''
train='''# One sigmoid neuron, one supervised training example.
# This is NOT training the hand-constructed XOR network above.
from math import exp

def sigmoid(z):
    return 1.0 / (1.0 + exp(-z))

x, target, bias = 1.0, 1.0, 0.0
weight = 0.0
learning_rate = 0.4
history = []
for step in range(6):
    prediction = sigmoid(weight * x + bias)
    loss = 0.5 * (target - prediction) ** 2
    history.append((step, weight, prediction, loss))
    # Chain rule: dL/dw = (p-target)*p*(1-p)*x.
    gradient = (prediction - target) * prediction * (1.0 - prediction) * x
    print(f"step {step}: w={weight:.5f}, p={prediction:.5f}, loss={loss:.7f}")
    weight -= learning_rate * gradient
assert history[0][2] == 0.5
assert abs(history[1][1] - 0.05) < 1e-12
assert all(history[i+1][3] < history[i][3] for i in range(len(history)-1))
print("The observed loss decreases in this particular small experiment.")
'''
gradient='''# Optional Research: check the chain-rule gradient numerically.
def squared_loss(w):
    p = sigmoid(w)
    return 0.5 * (1.0 - p) ** 2

w = 0.0
p = sigmoid(w)
exact = (p - 1.0) * p * (1.0 - p)
epsilon = 0.001
approx = (squared_loss(w + epsilon) - squared_loss(w - epsilon)) / (2 * epsilon)
print("Chain-rule gradient:", round(exact, 8))
print("Finite-difference estimate:", round(approx, 8))
assert abs(exact - approx) < 0.000001
'''
end='''## What to record

1. For each XOR input, explain the outputs of **both** hidden neurons and the last weighted sum. Which weights were given to you, rather than learned?
2. In the sigmoid experiment, why does the first weight change by exactly **+0.05** with learning rate 0.4?
3. Change the learning rate from **0.4** to **0.1** and compare six loss values. Does a larger learning rate always guarantee better training? Why not?
4. Explain why successful learning on one example does **not** establish that a network learned XOR or can generalise to unseen data.

**Research (3p), optional:** explain why the finite-difference estimate is close to the chain-rule gradient but not necessarily identical.

For the full two-layer differentiable training experiment see the laboratory's *two-layer gradient and training* notebook. Download your edited .ipynb and use the Laboratory submission panel; local ZIP creation is not an upload.
'''
notebook=dict(cells=[cell('markdown',intro),cell('markdown','## A. A network that represents XOR (weights supplied)'),
                     cell('code',xor),cell('markdown','## B. Train one sigmoid weight with gradient descent'),
                     cell('code',train),cell('markdown','## C. Optional — numerically check the gradient'),
                     cell('code',gradient),cell('markdown',end)],
 metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
           'language_info':{'name':'python'}},nbformat=4,nbformat_minor=5)
path=ROOT/'w7/lab/starter.ipynb'
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mirror=ROOT/'jupyter/files/w7-starter.ipynb'
mirror.write_bytes(path.read_bytes())
print('Updated Week 7 standalone starter and JupyterLite copy:',len(notebook['cells']),'cells')
