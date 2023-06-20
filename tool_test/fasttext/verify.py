import fasttext

TRAIN_FILE = "./data/cooking.train"
TEST_FILE = "./data/cooking.valid"
MODEL_FILE = "./model/model_cooking.bin"
if __name__ == '__main__':
    model = fasttext.load_model(MODEL_FILE)
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    print(model.predict("Why not put knives in the dishwasher?"))
    print(model.test(TEST_FILE))