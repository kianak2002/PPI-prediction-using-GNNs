import torch
import math
import torch.nn as nn
import torch.nn.functional as F
import random
from torch_geometric.utils import to_dense_adj

from torch_geometric.nn import GINConv, JumpingKnowledge, global_mean_pool, SAGEConv

class GIN_Net2(torch.nn.Module):
    def __init__(self, in_len=2000, in_feature=13, gin_in_feature=256, num_layers=1, 
                hidden=512, use_jk=False, pool_size=3, cnn_hidden=1, train_eps=True, 
                feature_fusion=None, class_num=7):
        super(GIN_Net2, self).__init__()
        self.use_jk = use_jk
        self.train_eps = train_eps
        self.feature_fusion = feature_fusion

        self.conv1d = nn.Conv1d(in_channels=in_feature, out_channels=cnn_hidden, kernel_size=3, padding=0)
        self.bn1 = nn.BatchNorm1d(cnn_hidden)
        self.biGRU = nn.GRU(cnn_hidden, cnn_hidden, bidirectional=True, batch_first=True, num_layers=1)
        self.maxpool1d = nn.MaxPool1d(pool_size, stride=pool_size)
        self.global_avgpool1d = nn.AdaptiveAvgPool1d(1)
        self.fc1 = nn.Linear(math.floor(in_len / pool_size), gin_in_feature)

        self.gin_conv1 = GINConv( 
            nn.Sequential(
                nn.Linear(gin_in_feature, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.BatchNorm1d(hidden),
            ), train_eps=self.train_eps
        )
        self.gin_convs = torch.nn.ModuleList()
        for i in range(num_layers - 1):
            self.gin_convs.append(
                GINConv(
                    nn.Sequential(
                        nn.Linear(hidden, hidden),
                        nn.ReLU(),
                        nn.Linear(hidden, hidden),
                        nn.ReLU(),
                        nn.BatchNorm1d(hidden),
                    ), train_eps=self.train_eps
                )
            )
        if self.use_jk:
            mode = 'cat'
            self.jump = JumpingKnowledge(mode)
            self.lin1 = nn.Linear(num_layers*hidden, hidden)
        else:
            self.lin1 = nn.Linear(hidden, hidden)
        self.lin2 = nn.Linear(hidden, hidden)
        self.fc2 = nn.Linear(hidden, class_num)
    
    def reset_parameters(self):
        
        self.conv1d.reset_parameters()
        self.fc1.reset_parameters()

        self.gin_conv1.reset_parameters()
        for gin_conv in self.gin_convs:
            gin_conv.reset_parameters()
        
        if self.use_jk:
            self.jump.reset_parameters()
        self.lin1.reset_parameters()
        self.lin2.reset_parameters()

        self.fc2.reset_parameters()
    
    def forward(self, x, edge_index, train_edge_id, p=0.5):
        x = x.transpose(1, 2)
        x = self.conv1d(x)
        x = self.bn1(x)
        x = self.maxpool1d(x)
        x = x.transpose(1, 2)
        x, _ = self.biGRU(x)
        x = self.global_avgpool1d(x)
        x = x.squeeze()
        x = self.fc1(x)

        x = self.gin_conv1(x, edge_index)
        xs = [x]
        for conv in self.gin_convs:
            x = conv(x, edge_index)
            xs += [x]

        if self.use_jk:
            x = self.jump(xs)
        
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=p, training=self.training)
        x = self.lin2(x)
        # x  = torch.add(x, x_)

        node_id = edge_index[:, train_edge_id]
        x1 = x[node_id[0]]
        x2 = x[node_id[1]]

        if self.feature_fusion == 'concat':
            x = torch.cat([x1, x2], dim=1)
        else:
            x = torch.mul(x1, x2)
        x = self.fc2(x)
        return x


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN_Net(torch.nn.Module):
    def __init__(self, in_feature, hidden_dim, num_layers, num_classes, dropout=0.5, feature_fusion='concat'):
        super(GCN_Net, self).__init__()
        self.num_layers = num_layers
        self.dropout = dropout
        self.feature_fusion = feature_fusion

        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(in_feature, hidden_dim))
        for _ in range(num_layers - 1):
            self.convs.append(GCNConv(hidden_dim, hidden_dim))

        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # Adjust the input size of the linear layer

    def forward(self, x, edge_index, train_edge_id):
        # print("SHIT611")
        for conv in self.convs:
            # print("SHIT6111")
            # print(x.shape)
            # print(edge_index.shape)
            x = x.view(-1, x.size(2))
            # print('Input tensor shape:', x.size())
            # print('Weight tensor shape:', conv.lin.weight.size())

            x = conv(x, edge_index)
            # print("SHIT6112")
            x = F.relu(x)
            # print("SHIT6113")
            x = F.dropout(x, p=self.dropout, training=self.training)
            # print("SHIT6114")
        # print("SHIT612")
        node_id = edge_index[:, train_edge_id]
        x1 = x[node_id[0]]
        x2 = x[node_id[1]]
        # print("SHIT613")
        if self.feature_fusion == 'concat':
            x = torch.cat([x1, x2], dim=1)
        else:
            x = torch.mul(x1, x2)
        # print("SHIT614")
        x = self.fc(x)
        return x


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv

class GAT_Net(torch.nn.Module):
    def __init__(self, in_len=2000, in_feature=13, hidden_dim=512, num_layers=1, num_heads=4, dropout=0.5, feature_fusion=None, class_num=7):
        super(GAT_Net, self).__init__()
        self.num_layers = num_layers
        self.dropout = dropout
        self.feature_fusion = feature_fusion

        self.conv1d = nn.Conv1d(in_channels=in_feature, out_channels=hidden_dim, kernel_size=3, padding=0)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.biGRU = nn.GRU(hidden_dim, hidden_dim, bidirectional=True, batch_first=True, num_layers=1)
        self.maxpool1d = nn.MaxPool1d(3, stride=3)
        self.global_avgpool1d = nn.AdaptiveAvgPool1d(1)
        self.fc1 = nn.Linear(math.floor(in_len / 3), hidden_dim)

        self.gat_convs = nn.ModuleList()
        self.gat_convs.append(GATConv(hidden_dim, hidden_dim, heads=num_heads, dropout=dropout))
        for _ in range(num_layers - 1):
            self.gat_convs.append(GATConv(hidden_dim * num_heads, hidden_dim, heads=num_heads, dropout=dropout))

        self.fc2 = nn.Linear(hidden_dim * num_heads, class_num)

    def forward(self, x, edge_index, train_edge_id, p=0.5):
        x = x.transpose(1, 2)
        x = self.conv1d(x)
        x = self.bn1(x)
        x = self.maxpool1d(x)
        x = x.transpose(1, 2)
        x, _ = self.biGRU(x)
        x = self.global_avgpool1d(x)
        x = x.squeeze()
        x = self.fc1(x)

        for conv in self.gat_convs:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)

        node_id = edge_index[:, train_edge_id]
        x1 = x[node_id[0]]
        x2 = x[node_id[1]]

        if self.feature_fusion == 'concat':
            x = torch.cat([x1, x2], dim=1)
        else:
            x = torch.mul(x1, x2)

        x = self.fc2(x)
        return x






