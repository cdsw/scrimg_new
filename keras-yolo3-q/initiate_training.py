# Initiate training x
# Generate dataset x
# Generate Kmeans from dataset x
# edit cfg file
# run conversion
# set training version
# do training
# overwrite training log

# run detection

import dataset_generator.generate_dataset as gen
import kmeans as km

def generateImage(amount, mode = 'bw'):
    ig = gen.DatasetGenerator()
    ig.generateAllScripts(amount, mode)

def generateKMeans():
    cluster_number = 6 #tiny yolo
    filename = "./dataset_generator/annotation.txt"
    kmeans = km.YOLO_Kmeans(cluster_number, filename)
    kmeans.txt2clusters()

if __name__ == "__main__":
    main()
