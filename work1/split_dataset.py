import random
import os
from shutil import copy, rmtree


def make_file(file_path):
    if os.path.exists(file_path):
        rmtree(file_path)
    os.mkdir(file_path)


def generate_cls_txt(cls_msg, root_path):
    path = os.path.join(root_path, 'clssses.txt')
    f = open(path, 'w')
    for cls in cls_msg:
        f.writelines(cls + '\n')
    f.close()


def main(root_path, split_ratio):
    assert os.path.isdir(root_path)
    origin_image_path = os.path.join(root_path, 'flower_dataset')
    assert os.path.isdir(origin_image_path)
    cls_msg = [cls for cls in os.listdir(origin_image_path)]
    generate_cls_txt(cls_msg, root_path)

    make_file(os.path.join(root_path, 'train'))
    make_file(os.path.join(root_path, 'val'))

    trian_path = os.path.join(root_path, 'train')
    val_path = os.path.join(root_path, 'val')

    f_train = open(os.path.join(root_path, 'train.txt'), 'w')
    f_val = open(os.path.join(root_path, 'val.txt'), 'w')
    for cls_id, cls_name in enumerate(os.listdir(origin_image_path)):
        image_cls_path = os.path.join(origin_image_path, cls_name)
        train_cls_path = os.path.join(trian_path, cls_name)
        val_cls_path = os.path.join(val_path, cls_name)
        make_file(train_cls_path)
        make_file(val_cls_path)
        image_names = os.listdir(image_cls_path)
        num = len(image_names)
        # 随机采样验证集的索引
        eval_index = random.sample(image_names, k=int(num * split_ratio))
        for idx, name in enumerate(image_names):
            image_path = os.path.join(image_cls_path, name)
            if name in eval_index:
                copy(image_path, val_cls_path)
                f_val.writelines(cls_name + '/' + name + ' ' + str(cls_id) + '\n')
            else:
                copy(image_path, train_cls_path)
                f_train.writelines(cls_name + '/' + name + ' ' + str(cls_id) + '\n')
    f_train.close()
    f_val.close()


if __name__ == '__main__':
    # 数据集根目录
    root_dataset_path = r'C:\PycharmProjects\data\flower'
    # 验证集比例
    val_ratio = 0.2
    main(root_dataset_path, val_ratio)
