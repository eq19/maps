import torch

class AddModel(torch.nn.Module):
    def forward(self, a, b):
        return a + b

def build_and_save_model(output_path="add_model.pt"):
    model = AddModel()
    scripted = torch.jit.trace(model, (torch.tensor([1.0]), torch.tensor([2.0])))
    scripted.save(output_path)
