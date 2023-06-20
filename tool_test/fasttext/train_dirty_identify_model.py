import fasttext

TRAIN_FILE = "./data/train.txt"
TEST_FILE = "./data/test.txt"
VALID_FILE = "./data/valid.txt"
MODEL_FILE = "./model/model_cooking.bin"

if __name__ == '__main__':
    model = fasttext.train_supervised(input=TRAIN_FILE)
    model.save_model(MODEL_FILE)
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    print(model.predict("Why not put knives in the dishwasher?"))
    print(model.test(TEST_FILE))