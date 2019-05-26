
import utilities.generate_dataset as gen
import utilities.kmeans as km
import utilities.convert_dn2h5 as convd
import utilities.train as tr
from shutil import copyfile, rmtree
class TrainingInitiator:
    def __init__(self, generator, k_means, version, converter ):
        self.generator = generator
        self.k_means = k_means
        self.version = version
        self.converter = converter

    def assignTrainer(self, trainer):
        self.trainer = trainer

    def generateImage(self, amount, mode = 'bw'):
        #Image
        self.generator.generateAllScripts(amount, mode)

        #KMeans
        self.k_means.txt2clusters()

        s = open("./model_data/scrimg_yolov3-24.cfg", "r")
        t = open("./model_data/scrimg_anchors-" + self.version + '.txt', "r")
        list_anchors = t.read()
        lines = s.readlines()
        t.close()
        s.close()

        for i in range(len(lines)):
            if "anchors = " in lines[i]:
                lines[i] = "anchors = " + list_anchors + '\n'

        s = open("./model_data/scrimg_yolov3-24.cfg", "w")
        s.writelines(lines)
        s.close()
        self.k_means.txt2clusters()

        #Generate H5 file
        self.converter.convert()

    def train(self, model_path, tfjs_=False):
        final_model_path, logdir = self.trainer.train(tfjs_)
        copyfile(final_model_path, model_path)
        rmtree(logdir)

if __name__ == "__main__":
    version = "T0518"
    #Generator
    generator = gen.DatasetGenerator(version)

    #K-Means
    cluster_number = 6
    annot_filepath = "./dataset/annotation-" + version + ".txt"
    k_means = km.YOLO_Kmeans(version, cluster_number, annot_filepath)

    #Model Conversion
    config_path = "model_data/scrimg_yolov3-24.cfg"
    weights_path = "model_data/yolov3-tiny.weights"
    output_path = "model_data/yolo-" + version + ".h5"
    output_img = "model_data/yolo-" + version + ".png"
    converter = convd.ModelConverter(version, config_path, weights_path, output_path, output_img)

    #Initial setting
    images_to_generate = 2
    initiator = TrainingInitiator(generator, k_means, version, converter)
    initiator.generateImage(images_to_generate)

    #Training parameters
    training_image_size = 256
    num_epoch_init, num_epoch_full = 1,1
    anchors_path = 'model_data/scrimg_anchors-' + version + '.txt'
    model_path = 'model_data/yolo-' + version + '.h5'
    trainer = tr.Trainer(training_image_size, version, num_epoch_init, num_epoch_full, annot_filepath, anchors_path, model_path)

    #Training start
    initiator.assignTrainer(trainer)
    initiator.train(model_path, True)
