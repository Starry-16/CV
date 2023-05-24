import torch
from tqdm import tqdm
import pandas as pd
import Pspnet
 
model = Pspnet(num_classes=32, aux_loss=True)
model = model.cuda()
 
# training loop 100 epochs
epochs_num = 100
# 选用SGD优化器来训练
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
schedule = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50)
 
# 损失函数选用多分类交叉熵损失函数
lossf = torch.nn.CrossEntropyLoss(ignore_index=255)
 
 
def evaluate(net, data_iter, device=torch.device('cuda:0')):
    net.eval()
    metric = torch.Accumulator(3)
    with torch.no_grad():
        for X, y in data_iter:
            if isinstance(X, list):
                X = [x.to(device) for x in X]
            else:
                X = X.to(device)
            y = y.to(device)
            pred = net(X)['output']
            metric.add(torch.accuracy(pred, y), torch.size(y))
            
    return metric[0] / metric[1]
 
 
# 训练函数
def train_ch13(net, train_iter, test_iter, loss_func, optimizer, num_epochs, schedule, devices=torch.try_all_gpus()):
    timer, num_batches = torch.Timer(), len(train_iter)
    animator = torch.Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0, 1], legend=['train loss', 'train acc', 'test acc'])
    net = torch.nn.DataParallel(net, device_ids=devices).to(devices[0])
    # 用来保存一些训练参数
 
    loss_list = []
    train_acc_list = []
    test_acc_list = []
    epochs_list = []
    time_list = []
    lr_list = []
    
 
    for epoch in range(num_epochs):
 
        # metric: loss, accuracy, labels.shape[0], labels.numel(), 0.4*aux_loss
        metric = torch.Accumulator(5)
        for i, (X, labels) in enumerate(train_iter):
            timer.start()
            if isinstance(X, list):
                X = [x.to(devices[0]) for x in X]
            else:
                X = X.to(devices[0])
            gt = labels.long().to(devices[0])
 
            net.train()
            optimizer.zero_grad()
            result = net(X)
            seg_loss = loss_func(result['output'], gt)
            aux_loss = loss_func(result['aux_output'], gt)
 
            loss_sum = seg_loss + 0.4*aux_loss
 
            l = loss_sum
            loss_sum.sum().backward()
            optimizer.step()
 
            acc = torch.accuracy(result['output'], gt)
            metric.add(l, acc, labels.shape[0], labels.numel(), 0.4*aux_loss)
 
            timer.stop()
            if (i + 1) % (num_batches // 5) == 0 or i == num_batches - 1:
                animator.add(epoch + (i + 1) / num_batches, (metric[0] / metric[2], metric[1] / metric[3], None, None))
 
            
        test_acc = evaluate(net, test_iter)
        animator.add(epoch + 1, (None, None, test_acc)) 
        schedule.step()
        print(f"epoch {epoch+1}/{epochs_num} --- loss {metric[0]/metric[2]:.3f} --- aux_loss {metric[4]/metric[2]:.3f} --- train acc {metric[1]/metric[3]:.3f} --- test acc {test_acc:.3f} --- lr {optimizer.state_dict()['param_groups'][0]['lr']} --- cost time {timer.sum()}")
        
        #---------保存训练数据---------------
        df = pd.DataFrame()
        loss_list.append(metric[0] / metric[2])
        train_acc_list.append(metric[1] / metric[3])
        test_acc_list.append(test_acc)
        epochs_list.append(epoch+1)
        time_list.append(timer.sum())
        lr_list.append(optimizer.state_dict()['param_groups'][0]['lr'])
        
        df['epoch'] = epochs_list
        df['loss'] = loss_list
        df['train_acc'] = train_acc_list
        df['test_acc'] = test_acc_list
        df["lr"] = lr_list
        df['time'] = time_list
        
        df.to_excel("../blork_file/savefile/PSPNET.xlsx")
        #----------------保存模型------------------- 
        if torch.np.mod(epoch+1, 5) == 0:
            torch.save(net, f'../blork_file/checkpoints/PSPNET{epoch+1}.pth')
 
    # 保存下最后的model
    torch.save(net, f'../blork_file/checkpoints/PSPNET.pth')