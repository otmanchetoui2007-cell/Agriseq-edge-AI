import torch
import torch.nn as nn

class NanoporeBasecaller(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.conv_stack = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=11, stride=4, padding=5),
            nn.BatchNorm1d(64),
            nn.Mish(),
            nn.Conv1d(64, 128, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm1d(128),
            nn.Mish(),
            nn.Conv1d(128, 256, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm1d(256),
            nn.Mish()
        )
        self.lstm = nn.LSTM(
            input_size=256,
            hidden_size=256,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )
        self.fc = nn.Linear(256 * 2, num_classes)
        
    def forward(self, x):
        x = self.conv_stack(x)
        x = x.permute(0, 2, 1)
        lstm_out, _ = self.lstm(x)
        logits = self.fc(lstm_out)
        return torch.log_softmax(logits, dim=-1)
