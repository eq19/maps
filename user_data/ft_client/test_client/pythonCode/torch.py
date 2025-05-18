import torch

class AddModel(torch.nn.Module):
    def forward(self, a, b):
        return a + b

# Create an instance
model = AddModel()

# Convert to TorchScript
scripted = torch.jit.trace(model, (torch.tensor([1.0]), torch.tensor([2.0])))

# Save as TorchScript file
scripted.save("add_model.pt")
