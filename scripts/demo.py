import torch
from segment_anything import SamPredictor, sam_model_registry
import matplotlib.pyplot as plt
import cv2

# Load your model (make sure you have the checkpoint)
sam_checkpoint = "path/to/your/sam_checkpoint.pth"
model_type = "vit_b"  # or vit_h, vit_l depending on your checkpoint
device = "cuda" if torch.cuda.is_available() else "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device)
predictor = SamPredictor(sam)

# Load a test image
image = cv2.imread("path/to/your/image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# Example dummy point to segment
input_point = [[500, 500]]  # x, y pixel
input_label = [1]  # 1 = foreground

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True,
)

# Show result
plt.imshow(image)
plt.imshow(masks[0], alpha=0.5)
plt.title("Predicted Mask")
plt.axis('off')
plt.show()
