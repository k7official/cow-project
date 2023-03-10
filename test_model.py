from ultralytics import YOLO

# Load a model
model = YOLO('best_musa.pt')  # load a pre-trained model (recommended for training)


# Use the model
results = model('scooter.jpg', save=True)  # predict on an image

# print(results)
