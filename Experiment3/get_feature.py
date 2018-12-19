import numpy as np
import os
import tensorflow as tf
from tensorflow.python.platform import gfile
MODEL_DIR = 'model/'  # inception-v3模型的文件夹
MODEL_FILE = 'tensorflow_inception_graph.pb'  # inception-v3模型文件名
CACHE_DIR = 'F:/SYFeature'  # 图像的特征向量保存地址
file_path = 'F:/Image'
# inception-v3模型参数
BOTTLENECK_TENSOR_SIZE = 2048  # inception-v3模型瓶颈层的节点个数
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'  # inception-v3模型中代表瓶颈层结果的张量名称
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'  # 图像输入张量对应的名称


def run_bottleneck_on_image(sess, image_data, image_data_tensor,bottleneck_tensor):

    bottleneck_values = sess.run(bottleneck_tensor,
                                 {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)  # 将四维数组压缩成一维数组
    return bottleneck_values

def create_bottleneck(sess, jpeg_data_tensor, bottleneck_tensor):
    for root,sub,files in os.walk(file_path):
        for file in files:
            img_path = os.path.join(root, file)
            bottleneck_path = os.path.join(CACHE_DIR, file+'.txt')

            image_data = gfile.FastGFile(img_path, 'rb').read()
            bottleneck_values = run_bottleneck_on_image(
                sess, image_data, jpeg_data_tensor,
                bottleneck_tensor)  # 通过inception-v3计算特征向量
            bottleneck_string = ','.join(str(x) for x in bottleneck_values)
            with open(bottleneck_path, 'w') as bottleneck_file:
                bottleneck_file.write(bottleneck_string)
            print('Creating bottleneck at ' + bottleneck_path)

def create_inception_graph():
    # 读取训练好的inception-v3模型
    with tf.Graph().as_default() as graph:
        with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            # 加载inception-v3模型，并返回数据输入张量和瓶颈层输出张量
            bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
                graph_def, name='',
                return_elements=[
                    BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME
                ])
    return bottleneck_tensor,jpeg_data_tensor, graph

if __name__ =='__main__':
    bottleneck_tensor, jpeg_data_tensor, graph = create_inception_graph()
    with tf.Session(graph=graph) as sess:
        create_bottleneck(sess, jpeg_data_tensor,bottleneck_tensor)

