from predict import predict_plan

# Example input (must match training order)
sample = [22, 1, 1.75, 75, 24.5, 1, 2, 0]

# Fat loss case
sample1 = [30, 1, 1.65, 90, 33.0, 0, 0, 0]

# Muscle gain case
sample2 = [22, 1, 1.80, 60, 18.5, 1, 2, 0]

result = predict_plan(sample)


print(result)



