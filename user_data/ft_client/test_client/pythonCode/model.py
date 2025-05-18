import torch

class AddModel(torch.nn.Module):
    def forward(self, a, b):
        return a + b

# Only run this when executing this script directly
if __name__ == "__main__":
    model = AddModel()
    scripted = torch.jit.trace(model, (torch.tensor([1.0]), torch.tensor([2.0])))
    scripted.save("add_model.pt")
